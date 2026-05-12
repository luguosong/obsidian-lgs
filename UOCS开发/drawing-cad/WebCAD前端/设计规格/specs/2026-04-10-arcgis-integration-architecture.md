# ArcGIS Web 服务集成 — C++ 实施架构

> **日期**: 2026-04-10  
> **目标**: 基于 ODA SDK + GDAL 3.4.2，实现 ArcGIS Web 服务与 DWG 的双向互操作  
> **前置依赖**: ODA SDK 24.10、GDAL 3.4.2（含 PROJ）、libcurl

---

## 总体架构：四层分离

```
┌─────────────────────────────────────────────────────────────────────┐
│                        你的 C++ 应用程序                             │
│   (Qt GUI / 命令行 / 服务进程)                                       │
├─────────────────────────────────────────────────────────────────────┤
│  Layer 4 │  DWG ↔ GIS 双向转换层                                    │
│          │  DwgToGisExporter / GisToDwgImporter / MscWriter         │
├──────────┼──────────────────────────────────────────────────────────┤
│  Layer 3 │  ODA DWG 实体操作层                                      │
│          │  OdArcGisGeoMapPE / FeatureToDwgConverter                │
│          │  OdDbGeoData / OdDbGeoMap / OdDbRasterImage / ...        │
├──────────┼──────────────────────────────────────────────────────────┤
│  Layer 2 │  坐标桥接层 (CrsBridge)                                  │
│          │  ODA CS-Map ↔ GDAL/PROJ 双向转换                         │
├──────────┼──────────────────────────────────────────────────────────┤
│  Layer 1 │  ArcGIS 服务接入层 (GDAL 3.4.2)                         │
│          │  MapImageLayerReader / FeatureLayerReader                 │
│          │  ArcGisRestClient (libcurl + JSON)                       │
└──────────┴──────────────────────────────────────────────────────────┘
```

---

## Layer 1 — ArcGIS 服务接入层

负责从 ArcGIS REST API 获取栅格瓦片和矢量要素。GDAL 3.4.2 自带两个关键驱动。

### `MapImageLayerReader` — 读取地图影像图层

利用 GDAL 的 `WMS` 驱动 + `AGS` minidriver，直接对接 ArcGIS MapServer。

```cpp
class MapImageLayerReader
{
public:
    struct TileRequest {
        OdGeExtents2d   bbox;        // WGS84 或投影坐标 bbox
        int             width;       // 输出像素宽
        int             height;      // 输出像素高
        OdString        srs;         // "EPSG:4526" 等
    };

    // 通过 GDAL AGS minidriver 打开 MapServer
    // url 示例: "http://kjgh.dg:30088/.../MapServer"
    OdResult open(const OdAnsiString& mapServerUrl, const OdAnsiString& srs);

    // 按 bbox 导出影像为内存 RGBA 像素块
    OdResult exportImage(const TileRequest& req, OdBinaryData& pixelData,
                         OdUInt32& outWidth, OdUInt32& outHeight);

    // 按 LOD+TileXY 导出单张瓦片 (ArcGIS Tile 方案)
    OdResult exportTile(int lod, int tileRow, int tileCol,
                        OdGiRasterImagePtr& outImage);

    void close();

private:
    GDALDatasetH  m_hDataset = nullptr;   // GDAL WMS dataset handle
    OdAnsiString  m_baseUrl;
};
```

**实现要点**：

- GDAL 打开方式有两种：
  - **方式 A**：生成 WMS XML 描述文件，`ServerUrl` 填 MapServer URL，`Type` 设为 `AGS`
  - **方式 B**：直接用 open syntax `"http://server/arcgis/rest/services/.../MapServer?f=json"`
- `GDALRasterIO()` 按 bbox 读取后，拼成 ODA 的 `OdBinaryData`（RGBA）

### `FeatureLayerReader` — 读取要素图层

利用 GDAL 的 `ESRIJSON / FeatureService` 驱动，对接 ArcGIS FeatureServer。

```cpp
class FeatureLayerReader
{
public:
    struct FeatureRecord {
        OdGePoint3dArray    geometry;     // 点/线/面坐标
        OGRwkbGeometryType  geomType;     // wkbPoint / wkbLineString / wkbPolygon ...
        std::map<OdString, OdString>  attributes;  // 字段名 → 值
    };

    // url 示例:
    //   "ESRIJSON:http://kjgh.dg:30088/.../FeatureServer/0/query?where=1=1&outFields=*&f=pjson"
    OdResult open(const OdAnsiString& featureServerUrl, int layerIndex = 0);

    // 按空间范围查询要素
    OdResult queryByExtent(const OdGeExtents2d& bbox,
                           OdArray<FeatureRecord>& outFeatures);

    // 按属性过滤查询要素
    OdResult queryByWhere(const OdAnsiString& whereClause,
                          OdArray<FeatureRecord>& outFeatures);

    // 获取图层 schema (字段列表)
    OdResult getSchema(OdStringArray& fieldNames,
                       OdArray<OGRFieldType>& fieldTypes);

    void close();

private:
    GDALDatasetH   m_hDataset = nullptr;
    OGRLayerH      m_hLayer   = nullptr;
    OdAnsiString   m_baseUrl;

    // GDAL 3.4.2 需要手动拼 /query URL
    OdAnsiString buildQueryUrl(const OdAnsiString& baseUrl,
                               int layerIndex,
                               const OdAnsiString& where,
                               const OdGeExtents2d* bbox);
};
```

**关键注意**：GDAL 3.4.2 的 `ESRIJSON` 驱动不能直接打开裸 `FeatureServer/0` URL，需要自己拼完整的 `/query?where=1%3D1&outFields=*&f=pjson` 查询串。`buildQueryUrl` 负责此逻辑。如果将来升级 GDAL，这部分可以简化。

### `ArcGisRestClient` — 辅助 HTTP/JSON 工具

对于 GDAL 驱动覆盖不到的 REST 操作（例如获取图层元数据、legend 信息、token 认证），可以用 libcurl + JSON 解析做补充：

```cpp
class ArcGisRestClient
{
public:
    OdResult getLayerInfo(const OdAnsiString& serviceUrl, int layerIndex,
                          /* out */ OdAnsiString& jsonResponse);

    OdResult getLegendInfo(const OdAnsiString& serviceUrl,
                           /* out */ OdAnsiString& jsonResponse);

    // ArcGIS Server token 认证 (如果服务需要)
    OdResult generateToken(const OdAnsiString& tokenUrl,
                           const OdAnsiString& username,
                           const OdAnsiString& password,
                           /* out */ OdAnsiString& token);
private:
    static size_t curlWriteCallback(void* ptr, size_t size,
                                    size_t nmemb, void* userdata);
};
```

---

## Layer 2 — 坐标桥接层

ODA 内核走 **CS-Map**（`OdSpatialReference` + `OdDbGeoCoordinateSystem`），GDAL 走 **PROJ**。两者对同一坐标系的定义可能有微小差异。这一层确保统一。

```cpp
class CrsBridge
{
public:
    // 从 ODA 坐标系 ID 转换为 GDAL/PROJ 可识别的格式
    // csMapId: ODA 风格坐标系 (如 "CGCS2000-GK-13")
    // 返回: EPSG code 或 WKT
    static OdResult odaCrsToGdalSrs(const OdString& csMapId,
                                     OGRSpatialReferenceH& outSrs);

    // 从 GDAL SRS 转换为 ODA CS-Map ID
    static OdResult gdalSrsToOdaCrs(OGRSpatialReferenceH srs,
                                     OdString& outCsMapId);

    // 坐标点批量转换: srcSrs → dstSrs
    static OdResult transformPoints(OGRSpatialReferenceH srcSrs,
                                     OGRSpatialReferenceH dstSrs,
                                     OdGePoint3dArray& points);

    // 利用 ODA 内置 GeoData 做坐标转换 (当只跑 ODA 管线时)
    static OdResult transformViaGeoData(const OdDbGeoData* pGeoData,
                                         const OdGePoint3d& ptLonLatAlt,
                                         OdGePoint3d& ptDesign);
};
```

**关键设计原则**：

- **写入 DWG 的坐标**：统一走 ODA 的 `OdDbGeoData::transformFromLonLatAlt()` / `transformToLonLatAlt()`，保证与 ODA 渲染管线一致
- **读/写 GIS 格式的坐标**：统一走 GDAL/PROJ 的 `OGRCoordinateTransformation`
- 两者之间只在"跨界点"做一次桥接，不要在同一条数据流里混用

---

## Layer 3 — ODA DWG 实体操作层

### `OdArcGisGeoMapPE` — 替换 Bing Maps 的 PE 实现

ODA 已有 `OdDbGeoMapPE` 这个 Protocol Extension 抽象类，当前的 `OdDbGeoMapPEImpl` 硬连了 Bing Maps。可以写一个新的 PE 实现，注册后 ODA 引擎就会用它来获取底图瓦片。

```cpp
// 对标 OdDbGeoMapPEImpl，但数据源改为 ArcGIS MapServer
class OdArcGisGeoMapPE : public OdDbGeoMapPE
{
public:
    ODRX_DECLARE_MEMBERS(OdArcGisGeoMapPE);

    OdResult updateMapImage(OdDbGeoMap* pGeoMap, bool bReset) override;

    void setMapServerUrl(const OdAnsiString& url);
    void setApiKey(const OdAnsiString& key);

private:
    MapImageLayerReader  m_reader;
    OdAnsiString         m_mapServerUrl;
    OdAnsiString         m_apiKey;

    OdResult getOptimalLOD(double vpDiag, double mapDiag,
                           const OdDbGeoData* pGeoData, OdInt8& lod);
    OdResult fetchAndCompositeImage(const OdDbGeoMap* pGeoMap,
                                     const OdDbGeoData* pGeoData,
                                     OdInt8 lod,
                                     OdBinaryData& outPixelData);
};
```

**注册方式**（在 Module 初始化时）：

```cpp
void MyGisModule::initApp()
{
    // 卸载 ODA 默认的 Bing PE (如果已加载)
    OdDbGeoMapPE::desc()->delX(OdDbGeoMapPEImpl::desc());

    // 注册 ArcGIS PE
    OdDbGeoMapPE::desc()->addX(OdArcGisGeoMapPE::desc(),
                                &m_arcGisGeoMapPE);
}
```

`updateMapImage` 的核心流程完全参照 `DbGeoMapPEImpl.cpp` 的模式，只需把 `OdBingMapsCache::getTiles()` 替换为 `MapImageLayerReader::exportImage()`。

#### `updateMapImage` 实现参考

| 步骤 | Bing Maps 原版 (OdDbGeoMapPEImpl) | ArcGIS 版 (OdArcGisGeoMapPE) |
|------|---|---|
| 1. 获取 GeoData | `oddbGetGeoDataObjId()` → `OdDbGeoData` | 相同 |
| 2. 计算 LOD | `OdDbGeoMapHelper::getOptimalLOD()` | 相同逻辑，可复用 |
| 3. 计算图像尺寸 | `OdDbGeoMapHelper::getImageSize()` | 相同逻辑，可复用 |
| 4. **获取瓦片** | `OdBingMapsCache::getTiles()` → Bing QuadKey | `MapImageLayerReader::exportImage()` → ArcGIS REST export |
| 5. 合成像素数据 | `OdDbGeoMapHelper::getMap()` → Bitmap | GDAL `GDALRasterIO()` → `OdBinaryData` |
| 6. 设置 GeoMap 字段 | `ext->setPixelData()` etc. | 相同 |

### `FeatureToDwgConverter` — ArcGIS 要素 → DWG 实体

```cpp
class FeatureToDwgConverter
{
public:
    struct ConvertOptions {
        OdString        targetLayer;         // 目标 DWG 图层名
        bool            createMscXData;      // 是否写 MSC 兼容扩展数据
        bool            mapFieldsToAttribs;  // 字段 → Block 属性 或 XData
        double          defaultElevation;    // Z 值 (如果源数据是 2D)
        OdCmColor       defaultColor;
    };

    // 主入口: 批量转换 FeatureRecord → DWG 实体
    OdResult convert(OdDbDatabase* pDb,
                     OdDbBlockTableRecord* pModelSpace,
                     const OdDbGeoData* pGeoData,
                     const OdArray<FeatureLayerReader::FeatureRecord>& features,
                     const ConvertOptions& opts);

private:
    // --- 几何转换 ---
    // OGR Point → OdDbPoint 或 OdDbBlockReference
    OdDbObjectId convertPoint(OdDbBlockTableRecord* pBTR,
                              const OdGePoint3d& pt,
                              const ConvertOptions& opts);

    // OGR LineString → OdDbPolyline (LWPolyline)
    OdDbObjectId convertPolyline(OdDbBlockTableRecord* pBTR,
                                 const OdGePoint3dArray& pts,
                                 const ConvertOptions& opts);

    // OGR Polygon → OdDbHatch (填充) + OdDbPolyline (边界)
    OdDbObjectId convertPolygon(OdDbBlockTableRecord* pBTR,
                                const OdGePoint3dArray& outerRing,
                                const OdArray<OdGePoint3dArray>& innerRings,
                                const ConvertOptions& opts);

    // --- 属性附加 ---
    void attachXData(OdDbEntity* pEnt,
                     const std::map<OdString, OdString>& attrs);

    void attachMscData(OdDbEntity* pEnt,
                       const OdString& featureClassName,
                       const std::map<OdString, OdString>& attrs);

    // 坐标从 WGS84/投影 → DWG 设计坐标
    OdGePoint3d reprojectToDesign(const OdDbGeoData* pGeoData,
                                  const OdGePoint3d& ptLonLat);
};
```

### `MscWriter` — MSC 兼容数据写入

MSC（Mapping Specification for CAD）的核心是在 DWG 的 **Named Object Dictionary** 中写入特定结构：

```cpp
class MscWriter
{
public:
    // 在 DWG 中创建/更新 ESRI_ATTRIBUTES 字典
    static OdResult writeFeatureClass(
        OdDbDatabase* pDb,
        const OdString& featureClassName,    // 如 "建筑红线"
        OdDb::GeomType geomType,             // Point/Polyline/Polygon
        const OdStringArray& fieldNames,
        const OdStringArray& fieldTypes);

    // 为单个实体写 MSC 属性 (ESRI_ATTRIBUTES XRecord)
    static OdResult writeEntityAttributes(
        OdDbEntity* pEnt,
        const OdString& featureClassName,
        const std::map<OdString, OdString>& attrs);

    // 写坐标系信息 (ESRI_PRJ)
    static OdResult writeCoordinateSystem(
        OdDbDatabase* pDb,
        const OdAnsiString& wktPrj);  // WKT 格式投影定义
};
```

**MSC 最小要求**（使 ArcGIS Desktop/Pro 能 direct-read 识别 DWG 为 GIS feature class）：

1. DWG Named Object Dictionary 中有 `ESRI_ATTRIBUTES` 字典
2. 每个 feature class 定义一个 XRecord，包含字段 schema
3. 每个实体的扩展字典中有对应的 `ESRI_ATTRIBUTES` XRecord，写入属性值
4. DWG 中嵌入 `.prj` WKT 坐标系字符串（通过 `ESRI_PRJ` 命名对象）

---

## Layer 4 — DWG ↔ GIS 双向转换层

### `GisToDwgImporter` — 加载 ArcGIS 图层到 DWG（综合调度）

```cpp
class GisToDwgImporter
{
public:
    struct ImportOptions {
        OdAnsiString   mapServerUrl;       // MapServer REST URL
        OdAnsiString   featureServerUrl;   // FeatureServer REST URL
        OdAnsiString   srs;               // 如 "EPSG:4526"
        OdGeExtents2d  importExtent;       // 导入范围
        bool           importRaster;       // 是否导入底图影像
        bool           importFeatures;     // 是否导入矢量要素
        OdArray<int>   featureLayerIds;    // 要导入的图层 ID 列表
        bool           writeMsc;           // 是否写 MSC 兼容数据
    };

    OdResult execute(OdDbDatabase* pDb, const ImportOptions& opts);

private:
    // Step 1: 确保 DWG 有 GeoData
    OdResult ensureGeoData(OdDbDatabase* pDb, const OdAnsiString& srs);

    // Step 2: 导入底图影像 → OdDbRasterImage
    OdResult importMapImage(OdDbDatabase* pDb,
                            OdDbBlockTableRecord* pModelSpace,
                            const OdDbGeoData* pGeoData,
                            const ImportOptions& opts);

    // Step 3: 导入矢量图层 → OdDb 实体 + 属性
    OdResult importFeatureLayer(OdDbDatabase* pDb,
                                OdDbBlockTableRecord* pModelSpace,
                                const OdDbGeoData* pGeoData,
                                int layerId,
                                const ImportOptions& opts);

    MapImageLayerReader      m_rasterReader;
    FeatureLayerReader       m_featureReader;
    FeatureToDwgConverter    m_converter;
    MscWriter                m_mscWriter;
};
```

### `DwgToGisExporter` — DWG 数据转 GIS

```cpp
class DwgToGisExporter
{
public:
    enum OutputFormat {
        kGeoPackage,     // .gpkg (推荐，支持混合几何)
        kShapefile,      // .shp (经典格式，但限制多)
        kGeoJSON,        // .geojson
        kFileGDB,        // Esri File Geodatabase (需 FileGDB SDK 或 OpenFileGDB)
    };

    struct ExportOptions {
        OutputFormat    format;
        OdAnsiString   outputPath;         // 输出文件路径
        OdAnsiString   targetSrs;          // 目标坐标系 "EPSG:4326"
        bool           readMscAttributes;  // 优先读 MSC 扩展属性
        bool           readXData;          // 读 XData 作为字段
        OdStringArray   layerFilter;       // 只导出指定 DWG 图层
    };

    OdResult execute(OdDbDatabase* pDb, const ExportOptions& opts);

private:
    // 遍历 ModelSpace 实体
    OdResult iterateEntities(OdDbBlockTableRecord* pModelSpace,
                              const OdDbGeoData* pGeoData,
                              OGRLayerH hLayer,
                              const ExportOptions& opts);

    // OdDbPolyline → OGRFeature (LineString/Polygon)
    OdResult exportPolyline(OdDbPolyline* pPline,
                            const OdDbGeoData* pGeoData,
                            OGRLayerH hLayer);

    // OdDbHatch → OGRFeature (Polygon)
    OdResult exportHatch(OdDbHatch* pHatch,
                         const OdDbGeoData* pGeoData,
                         OGRLayerH hLayer);

    // OdDbPoint / OdDbBlockReference → OGRFeature (Point)
    OdResult exportPoint(OdDbEntity* pEnt,
                         const OdDbGeoData* pGeoData,
                         OGRLayerH hLayer);

    // OdDbText / OdDbMText → OGRFeature (Point + 文本属性)
    OdResult exportText(OdDbEntity* pEnt,
                        const OdDbGeoData* pGeoData,
                        OGRLayerH hLayer);

    // 读实体的 MSC/XData 属性
    void readAttributes(OdDbEntity* pEnt,
                        const ExportOptions& opts,
                        std::map<OdString, OdString>& attrs);
};
```

---

## 数据流总图

### 需求(1): ArcGIS → DWG（地图影像 + 要素）

```
  ArcGIS MapServer                    ArcGIS FeatureServer
  (kjgh.dg:30088/.../MapServer)       (/FeatureServer/0,1,2...)
        │                                     │
        │ HTTP/REST                            │ HTTP/REST + /query
        ▼                                     ▼
  ┌──────────────┐                   ┌──────────────────┐
  │ GDAL WMS/AGS │                   │ GDAL ESRIJSON    │
  │ minidriver   │                   │ driver           │
  └──────┬───────┘                   └────────┬─────────┘
         │ GDALRasterIO()                     │ OGR_L_GetNextFeature()
         ▼                                     ▼
  ┌──────────────────┐               ┌─────────────────────┐
  │ MapImageLayer    │               │ FeatureLayerReader   │
  │ Reader           │               │ (OGR→FeatureRecord)  │
  └──────┬───────────┘               └────────┬────────────┘
         │ OdBinaryData (RGBA)                │ OdGePoint3dArray
         │                                     │ + attributes
         ▼                                     ▼
  ┌──────────────────┐   CrsBridge   ┌─────────────────────┐
  │ OdDbRasterImage  │◄─────────────►│ FeatureToDwg        │
  │ (或 OdDbGeoMap)  │   坐标转换    │ Converter           │
  └──────┬───────────┘               └────────┬────────────┘
         │                                     │
         ▼                                     ▼
  ┌───────────────────────────────────────────────────────┐
  │                   OdDbDatabase (DWG)                   │
  │  ┌─────────────┐  ┌────────────┐  ┌───────────────┐  │
  │  │ OdDbGeoData │  │ OdDbLayer  │  │ ESRI_ATTRIBUTES│  │
  │  │ (坐标系)    │  │ "建筑红线" │  │ (MSC XRecord)  │  │
  │  └─────────────┘  └────────────┘  └───────────────┘  │
  └───────────────────────────────────────────────────────┘
```

### 需求(2): DWG → GIS

```
  ┌───────────────────────────────────────────────────────┐
  │                   OdDbDatabase (DWG)                   │
  │  OdDbPolyline, OdDbHatch, OdDbBlockReference, ...     │
  │  + OdDbGeoData (坐标系) + XData/MSC 属性              │
  └──────────────────────┬────────────────────────────────┘
                         │ ODA API 遍历实体
                         ▼
               ┌──────────────────┐
               │ DwgToGisExporter │
               │  读几何 + 属性   │
               └────────┬─────────┘
                        │ OdGePoint3d → OGR Geometry
                        │ (经 CrsBridge 重投影)
                        ▼
               ┌──────────────────┐
               │ GDAL/OGR 写出    │
               │ OGR_DS_CreateLayer│
               │ OGR_F_SetGeometry│
               └────────┬─────────┘
                        │
                ┌───────┼───────┬───────────┐
                ▼       ▼       ▼           ▼
            .gpkg    .shp    .geojson    FileGDB
```

---

## 文件 / 模块组织建议

```
YourProject/
├── GisIntegration/                    ← 新模块
│   ├── CMakeLists.txt
│   ├── Layer1_ServiceAccess/
│   │   ├── ArcGisRestClient.h / .cpp
│   │   ├── MapImageLayerReader.h / .cpp
│   │   └── FeatureLayerReader.h / .cpp
│   ├── Layer2_CrsBridge/
│   │   └── CrsBridge.h / .cpp
│   ├── Layer3_DwgOps/
│   │   ├── OdArcGisGeoMapPE.h / .cpp  ← 继承 OdDbGeoMapPE
│   │   ├── FeatureToDwgConverter.h / .cpp
│   │   └── MscWriter.h / .cpp
│   ├── Layer4_Convert/
│   │   ├── GisToDwgImporter.h / .cpp   ← 调度入口
│   │   └── DwgToGisExporter.h / .cpp   ← 调度入口
│   └── GisIntegrationModule.h / .cpp   ← ODA Tx Module 注册
├── ... (现有代码)
```

**CMake 依赖关系**：

```cmake
target_link_libraries(GisIntegration
    # ODA 库
    ${TD_DB_LIB}
    ${TD_DBROOT_LIB}
    ${TD_GE_LIB}
    ${TD_GI_LIB}
    ${TD_ROOT_LIB}
    ${TD_GEOLOCATIONOBJ_LIB}   # OdDbGeoData, OdDbGeoMap, OdDbGeoMapPE
    ${TH_CURL_LIB}             # HTTP 请求

    # GDAL
    GDAL::GDAL                  # gdal 3.4.2
)
```

---

## 关于坐标系

示例服务 `Spatial Reference: 4526` 对应 **CGCS2000 / 3-degree Gauss-Kruger zone 13**。ODA 的 CS-Map 应当能识别此坐标系。建议在 `CrsBridge` 初始化时做一次双向验证：

```cpp
// 验证 ODA CS-Map 和 GDAL PROJ 对同一 EPSG 的定义一致性
OdGePoint3d testPt(113.75, 23.05, 0.0);  // 东莞附近经纬度
OdGePoint3d resultOda, resultGdal;
// 分别用两条链转换后比较差异，确保 < 0.001m
```

---

## 建议的实施顺序

| 阶段 | 内容 | 预估工作量 |
|------|------|-----------|
| **Phase 1** | Layer 1: `MapImageLayerReader` + GDAL WMS/AGS 打通 | 2-3 天 |
| **Phase 2** | Layer 3.1: `OdArcGisGeoMapPE` 替换 Bing PE，DWG 中能看到 ArcGIS 底图 | 3-4 天 |
| **Phase 3** | Layer 1: `FeatureLayerReader` + GDAL ESRIJSON 打通 | 2 天 |
| **Phase 4** | Layer 3.2 + 3.3: `FeatureToDwgConverter` + `MscWriter`，矢量要素落 DWG | 4-5 天 |
| **Phase 5** | Layer 4.2: `DwgToGisExporter`，DWG → GeoPackage/Shapefile | 3-4 天 |
| **Phase 6** | Layer 2: `CrsBridge` 精细化 + 端到端坐标验证 | 2 天 |
| **Phase 7** | Layer 4.1: `GisToDwgImporter` 综合调度 + UI 集成 | 2-3 天 |

总计约 **18-23 个工作日**，可根据实际优先级调整顺序。如果暂时不需要 MSC 兼容（即不需要 ArcGIS Desktop 直接读 DWG），Phase 4 中的 `MscWriter` 可以推迟。

---

## 参考资料

- [ODA Drawings SDK 路线图](https://www.opendesign.com/products/teigha-drawings) — 2024: "New ESRI provider"；2025: "Azure Maps support in OdDbGeoMap"
- [ODA Map SDK](https://www.opendesign.com/products/map3d) — FDO provider 支持 SHP / SDF / SQLite / WFS / PostGIS
- [Esri in ODA](https://www.opendesign.com/member-showcase/esri) — Esri 使用 ODA/Teigha 构建 CAD 互操作
- [GDAL WMS / AGS minidriver](https://gdal.org/en/stable/drivers/raster/wms.html) — 支持 ArcGIS REST MapServer
- [GDAL ESRIJSON driver](https://gdal.org/en/stable/drivers/vector/esrijson.html) — 读取 ArcGIS FeatureService JSON
- [MSC 规范](https://doc.arcgis.com/en/arcgis-for-autocad/latest/commands-api/what-is-maping-specification-for-cad-.htm) — Mapping Specification for CAD
- [ArcGIS direct-read CAD 数据模型](https://desktop.arcgis.com/en/arcmap/latest/manage-data/cad/the-direct-read-cad-data-model.htm)
