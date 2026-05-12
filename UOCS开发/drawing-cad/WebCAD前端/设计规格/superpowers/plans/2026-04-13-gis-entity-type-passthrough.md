# GIS 导入实体类型透传 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让前端 ImportGisModal 中用户选择的实体类型（如 OdDbHatch / [[OdDbPolyline]]）能正确传递到 C++ 端，并据此创建对应的 DWG 实体。

**Architecture:** 将 `GisStyleMap` 的键从 `gisType` 改为 `layerName` 以支持 per-layer 配置；在 `GisStyleEntry` 中增加 `dwgEntity` 字段；`ConvertOGRFeatureToDWG` 改为接收直接解析好的 `GisStyleEntry*`；新增 `convertPolygonAsHatch()` 函数实现 OGRPolygon → OdDbHatch 转换。

**Tech Stack:** C++ (ODA SDK)、GDAL/OGR、Boost.PropertyTree (JSON 解析)

---

## 文件变更清单

| 操作 | 文件 | 职责 |
|------|------|------|
| 修改 | `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_feature_from_gis.h` | `GisStyleEntry` 增加 `dwgEntity`，`ConvertOGRFeatureToDWG` 签名改为接收 `const GisStyleEntry*` |
| 修改 | `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_feature_from_gis.cpp` | 新增 `convertPolygonAsHatch()`，修改 `ConvertOGRFeatureToDWG()` 按 `dwgEntity` 分支 |
| 修改 | `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_gisservice_impl.cpp` | `parseStyleJson()` 改用 `layerName` 做键并提取 `dwgEntity`，`importGisFile()` 按图层名查找样式 |

---

### Task 1: 扩展 GisStyleEntry 结构体并修改函数签名

**Files:**
- Modify: `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_feature_from_gis.h:12-27`

- [ ] **Step 1: 在 GisStyleEntry 中增加 dwg[[Entity]] 字段**

将 `uaodco_feature_from_gis.h` 中的 `GisStyleEntry` 和 `ConvertOGRFeatureToDWG` 声明改为：

```cpp
// 单个几何类型的样式配置
struct GisStyleEntry
{
    std::string layer;      // 目标图层名
    int         colorIndex; // AutoCAD 颜色索引 (1-7)
    std::string linetype;   // 线型名 ("Continuous", "DASHED", ...)
    std::string dwgEntity;  // 目标 DWG 实体类型 ("OdDbHatch", "OdDbPolyline", ...)
};

// key = GIS 图层名 (layerName)
typedef std::map<std::string, GisStyleEntry> GisStyleMap;

OdDbObjectId ConvertOGRFeatureToDWG(
    OdDbBlockTableRecord* pBTR,
    OGRFeature* poFeature,
    const std::string& targetLayerName,
    const GisStyleEntry* pStyle = nullptr);
```

具体变更点：
- `GisStyleEntry` 新增 `std::string dwgEntity;` 成员（第 17 行后插入）
- `GisStyleMap` 注释改为 `key = GIS 图层名 (layerName)`
- `ConvertOGRFeatureToDWG` 第 4 个参数从 `const GisStyleMap& styleMap = GisStyleMap()` 改为 `const GisStyleEntry* pStyle = nullptr`

- [ ] **Step 2: 编译验证头文件变更**

此时 `.cpp` 文件会编译失败（因为实现还未同步），仅确认头文件本身无语法错误。

- [ ] **Step 3: Commit**

```bash
git add uaodco_feature_from_gis.h
git commit -m "refactor(gis): add dwgEntity to GisStyleEntry, change ConvertOGRFeatureToDWG signature to accept GisStyleEntry*"
```

---

### Task 2: 实现 convertPolygonAsHatch() 函数

**Files:**
- Modify: `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_feature_from_gis.cpp:96-115`

- [ ] **Step 1: 在 convertPolygon() 函数之后新增 convertPolygonAsHatch()**

在 `uaodco_feature_from_gis.cpp` 的 `convertPolygon()` 函数（第 115 行）之后插入：

```cpp
static OdDbObjectId convertPolygonAsHatch(
    OdDbBlockTableRecord* pBTR, OGRPolygon* poPoly, OdDbObjectId layerId)
{
    OGRLinearRing* poExterior = poPoly->getExteriorRing();
    if (!poExterior || poExterior->getNumPoints() < 3)
        return OdDbObjectId::kNull;

    OdDbHatchPtr pHatch = OdDbHatch::createObject();
    pHatch->setDatabaseDefaults(pBTR->database());
    pHatch->setNormal(OdGeVector3d::kZAxis);
    pHatch->setPattern(OdDbHatch::kPreDefined, OD_T("SOLID"));
    pHatch->setAssociative(false);
    pHatch->setLayer(layerId);

    // 辅助 lambda: OGRLinearRing → OdGePoint2dArray + OdGeDoubleArray
    auto ringToArrays = [](OGRLinearRing* poRing,
                           OdGePoint2dArray& vertices,
                           OdGeDoubleArray& bulges)
    {
        int numPts = poRing->getNumPoints();
        for (int i = 0; i < numPts; i++)
        {
            OGRPoint pt;
            poRing->getPoint(i, &pt);
            vertices.append(OdGePoint2d(pt.getX(), pt.getY()));
            bulges.append(0.0);
        }
    };

    // 外环 → kExternal
    {
        OdGePoint2dArray vertices;
        OdGeDoubleArray bulges;
        ringToArrays(poExterior, vertices, bulges);
        pHatch->appendLoop(
            OdDbHatch::kExternal | OdDbHatch::kPolyline,
            vertices, bulges);
    }

    // 内环（孔洞）→ kDefault（内部环）
    int numInterior = poPoly->getNumInteriorRings();
    for (int i = 0; i < numInterior; i++)
    {
        OGRLinearRing* poInner = poPoly->getInteriorRing(i);
        if (!poInner || poInner->getNumPoints() < 3) continue;

        OdGePoint2dArray vertices;
        OdGeDoubleArray bulges;
        ringToArrays(poInner, vertices, bulges);
        pHatch->appendLoop(
            OdDbHatch::kDefault | OdDbHatch::kPolyline,
            vertices, bulges);
    }

    OdDbObjectId entId = pBTR->appendOdDbEntity(pHatch);
    pHatch->evaluateHatch();
    return entId;
}
```

**参考来源：**
- Hatch 创建流程: `Drawing/Examples/ExCommands/ExTxtExp.cpp:327-451`
- Loop 类型标志: `kExternal | kPolyline` = 外环多段线, `kDefault | kPolyline` = 内环多段线
- `evaluateHatch()`: 计算填充几何，必须在 appendLoop 之后调用
- `setAssociative(false)`: GIS 导入的 Hatch 无需关联边界实体

**注意：** `OdGeVector3d::kZAxis` 可能需要额外 include `<Ge/GeVector3d.h>`，如果编译报错则在文件头增加该 include。

- [ ] **Step 2: Commit**

```bash
git add uaodco_feature_from_gis.cpp
git commit -m "feat(gis): add convertPolygonAsHatch() for OGRPolygon to OdDbHatch conversion"
```

---

### Task 3: 修改 ConvertOGRFeatureToDWG() 使用 dwgEntity 分支

**Files:**
- Modify: `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_feature_from_gis.cpp:172-257`

- [ ] **Step 1: 重写 ConvertOGRFeatureToDWG 函数体**

将 `ConvertOGRFeatureToDWG` 的签名和函数体改为：

```cpp
OdDbObjectId ConvertOGRFeatureToDWG(
    OdDbBlockTableRecord* pBTR,
    OGRFeature* poFeature,
    const std::string& targetLayerName,
    const GisStyleEntry* pStyle)
{
    if (!pBTR || !poFeature) return OdDbObjectId::kNull;

    OGRGeometry* poGeom = poFeature->GetGeometryRef();
    if (!poGeom) return OdDbObjectId::kNull;

    OdDbDatabase* pDb = pBTR->database();
    OGRwkbGeometryType eType = wkbFlatten(poGeom->getGeometryType());

    // 从 pStyle 读取样式; 若为 nullptr 则使用默认值
    std::string effectiveLayer = targetLayerName;
    int colorIndex = 0;
    OdDbObjectId linetypeId;
    std::string dwgEntity;

    if (pStyle)
    {
        if (!pStyle->layer.empty())
            effectiveLayer = pStyle->layer;
        colorIndex = pStyle->colorIndex;
        linetypeId = findLinetype(pDb, pStyle->linetype);
        dwgEntity  = pStyle->dwgEntity;
    }

    OdDbObjectId layerId = ensureLayer(pDb, fromGdalString(effectiveLayer.c_str()));
    OdDbObjectId entId = OdDbObjectId::kNull;

    switch (eType)
    {
    case wkbPoint:
        entId = convertPoint(pBTR, static_cast<OGRPoint*>(poGeom), layerId);
        break;
    case wkbLineString:
        entId = convertLineString(pBTR, static_cast<OGRLineString*>(poGeom), layerId);
        break;
    case wkbPolygon:
        if (dwgEntity == "OdDbHatch")
            entId = convertPolygonAsHatch(pBTR, static_cast<OGRPolygon*>(poGeom), layerId);
        else
            entId = convertPolygon(pBTR, static_cast<OGRPolygon*>(poGeom), layerId);
        break;
    case wkbMultiPoint:
    {
        OGRMultiPoint* poMP = static_cast<OGRMultiPoint*>(poGeom);
        for (int i = 0; i < poMP->getNumGeometries(); i++)
            entId = convertPoint(pBTR, static_cast<OGRPoint*>(poMP->getGeometryRef(i)), layerId);
        break;
    }
    case wkbMultiLineString:
    {
        OGRMultiLineString* poMLS = static_cast<OGRMultiLineString*>(poGeom);
        for (int i = 0; i < poMLS->getNumGeometries(); i++)
            entId = convertLineString(pBTR,
                static_cast<OGRLineString*>(poMLS->getGeometryRef(i)), layerId);
        break;
    }
    case wkbMultiPolygon:
    {
        OGRMultiPolygon* poMPoly = static_cast<OGRMultiPolygon*>(poGeom);
        for (int i = 0; i < poMPoly->getNumGeometries(); i++)
        {
            if (dwgEntity == "OdDbHatch")
                entId = convertPolygonAsHatch(pBTR,
                    static_cast<OGRPolygon*>(poMPoly->getGeometryRef(i)), layerId);
            else
                entId = convertPolygon(pBTR,
                    static_cast<OGRPolygon*>(poMPoly->getGeometryRef(i)), layerId);
        }
        break;
    }
    default:
        std::printf("[GisService] ConvertOGRFeatureToDWG: unsupported geometry type %d\n",
                    (int)eType);
        return OdDbObjectId::kNull;
    }

    if (!entId.isNull())
    {
        OdDbEntityPtr pEnt = entId.safeOpenObject(OdDb::kForWrite);
        applyStyle(pEnt, colorIndex, linetypeId);
        attachFieldsAsXData(pEnt, poFeature);
    }

    return entId;
}
```

关键变更：
- 第 4 个参数从 `const GisStyleMap& styleMap` → `const GisStyleEntry* pStyle`
- 删除了 `geomTypeKey` + `styleMap.find()` 查找逻辑，改为直接从 `pStyle` 读取
- `wkbPolygon` 和 `wkbMultiPolygon` 分支增加 `dwgEntity == "OdDbHatch"` 判断

- [ ] **Step 2: 同步修改 ConvertGISLayerToDWG**

`ConvertGISLayerToDWG`（第 259-281 行）调用 `ConvertOGRFeatureToDWG` 时只传 3 个参数：

```cpp
OdDbObjectId id = ConvertOGRFeatureToDWG(pBTR, poFeature, targetDwgLayer);
```

由于新签名的第 4 个参数默认为 `nullptr`，此处**无需修改**，编译器自动使用默认值。确认不需改动即可。

- [ ] **Step 3: Commit**

```bash
git add uaodco_feature_from_gis.cpp
git commit -m "feat(gis): branch entity creation by dwgEntity in ConvertOGRFeatureToDWG"
```

---

### Task 4: 修改 parseStyleJson() 改用 layerName 做键并提取 dwgEntity

**Files:**
- Modify: `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_gisservice_impl.cpp:411-451`

- [ ] **Step 1: 重写 parseStyleJson()**

将 `parseStyleJson` 函数改为：

```cpp
///////////////////////////////////////////////////////////////////////////
// importGisFile — import selected layers from a GIS file into DWG
///////////////////////////////////////////////////////////////////////////
// 从前端样式配置 JSON 数组构建 GisStyleMap (按 layerName 索引)
// 输入格式: [{"layerName":"roads","gisType":"Polygon","dwgEntity":"OdDbHatch","layer":"GIS_Roads","color":"青色 (4)","linetype":"Continuous"}, ...]
static uodgdal::GisStyleMap parseStyleJson(const std::string& json)
{
    uodgdal::GisStyleMap result;
    if (json.empty()) return result;

    // 颜色名称 → AutoCAD 颜色索引：从 "黄色 (2)" 中提取括号里的数字
    auto parseColorIndex = [](const std::string& colorStr) -> int {
        size_t lp = colorStr.find('(');
        size_t rp = colorStr.find(')');
        if (lp != std::string::npos && rp != std::string::npos && rp > lp + 1)
            return std::atoi(colorStr.substr(lp + 1, rp - lp - 1).c_str());
        return 0;
    };

    // 使用 uaroot 的 JSON 解析
    TBoostPtree root;
    if (!uajson::StdString2BPtreeJson(json, root))
    {
        std::printf("[GisService] parseStyleJson: JSON parse failed\n");
        return result;
    }

    // JSON 数组在 Boost.PropertyTree 中表现为空键名的子节点
    for (auto& item : root)
    {
        auto& obj = item.second;
        std::string layerName = obj.get<std::string>("layerName", "");
        if (layerName.empty()) continue;

        uodgdal::GisStyleEntry entry;
        entry.layer      = obj.get<std::string>("layer", "");
        entry.colorIndex = parseColorIndex(obj.get<std::string>("color", ""));
        entry.linetype   = obj.get<std::string>("linetype", "");
        entry.dwgEntity  = obj.get<std::string>("dwgEntity", "");
        result[layerName] = entry;
    }

    std::printf("[GisService] parseStyleJson: parsed %d style entries\n", (int)result.size());
    return result;
}
```

变更点：
- 注释更新：键改为 `layerName`，输入格式示例包含 `dwgEntity`
- `obj.get<std::string>("gisType", "")` → `obj.get<std::string>("layerName", "")`
- `result[gisType]` → `result[layerName]`
- 新增 `entry.dwgEntity = obj.get<std::string>("dwgEntity", "");`

- [ ] **Step 2: Commit**

```bash
git add uaodco_gisservice_impl.cpp
git commit -m "refactor(gis): parseStyleJson key changed from gisType to layerName, extract dwgEntity"
```

---

### Task 5: 修改 importGisFile() 按图层名查找样式并传递给转换函数

**Files:**
- Modify: `E:\updasdk\WorkSpace\uadrawing\src\uaodcadcore\gdal\uaodco_gisservice_impl.cpp:540-570`

- [ ] **Step 1: 修改 importGisFile 中的图层循环**

将 `importGisFile()` 函数中第 540-570 行的「逐要素转换」部分改为：

```cpp
        // 查找该 GIS 图层对应的样式配置
        const uodgdal::GisStyleEntry* pLayerStyle = nullptr;
        auto styleIt = styleMap.find(layerName);
        if (styleIt != styleMap.end())
            pLayerStyle = &styleIt->second;

        // 确定目标 DWG 图层名 (样式配置中的 layer 优先, fallback 到 GIS 图层名)
        std::string effectiveDwgLayer = layerName.empty() ? "GIS_IMPORT" : layerName;
        if (pLayerStyle && !pLayerStyle->layer.empty())
            effectiveDwgLayer = pLayerStyle->layer;

        // 逐要素转换
        OGRLayer* poLayer = reinterpret_cast<OGRLayer*>(hLayer);
        poLayer->ResetReading();
        OGRFeature* poFeature = nullptr;
        int layerFeatureCount = 0;

        while ((poFeature = poLayer->GetNextFeature()) != nullptr)
        {
            if (poCT)
            {
                OGRGeometry* poGeom = poFeature->GetGeometryRef();
                if (poGeom)
                    poGeom->transform(poCT);
            }

            OdDbObjectId id = uodgdal::ConvertOGRFeatureToDWG(
                pMS, poFeature, effectiveDwgLayer, pLayerStyle);
            if (!id.isNull())
                layerFeatureCount++;

            OGRFeature::DestroyFeature(poFeature);
        }
```

关键变更：
- 在要素循环之前，用 `styleMap.find(layerName)` 查找 per-layer 样式
- DWG 图层名现在在循环外一次性解析（从 `pLayerStyle->layer`）
- `ConvertOGRFeatureToDWG` 调用改为传递 `pLayerStyle` 指针而非整个 `styleMap`

- [ ] **Step 2: 全量编译验证**

编译整个 uaodcadcore 模块，确保所有改动一起编译通过。

- [ ] **Step 3: Commit**

```bash
git add uaodco_gisservice_impl.cpp
git commit -m "feat(gis): importGisFile resolves per-layer style and passes to ConvertOGRFeatureToDWG"
```

---

### Task 6: 端到端测试验证

- [ ] **Step 1: 编译 WASM**

重新编译 DrawingWeb (Emscripten WASM build)，将产出的 `DrawingJs.js`、`DrawingJs.wasm`、`DrawingJs.data` 复制到 `DrawingWebApp/public/`。

- [ ] **Step 2: 测试用例 — Polygon 选 OdDbHatch (面域)**

1. 启动 `npm run dev`
2. 导入一个包含 Polygon 图层的 Shapefile
3. 在 ImportGisModal 中，将实体类型设为 **面域** (OdDbHatch)
4. 点击导入
5. 验证：DWG 中生成的实体应为 **OdDbHatch (SOLID 填充)**，而非闭合多段线

- [ ] **Step 3: 测试用例 — Polygon 选 [[OdDbPolyline]] (多段线)**

1. 同一 Shapefile，实体类型改为 **多段线** ([[OdDbPolyline]])
2. 导入后验证：DWG 中生成的实体应为闭合 **[[OdDbPolyline]]**

- [ ] **Step 4: 测试用例 — 多图层不同实体类型**

1. 导入包含 2 个 Polygon 图层的文件
2. 图层 A 选 OdDbHatch，图层 B 选 [[OdDbPolyline]]
3. 验证两个图层分别生成正确的实体类型

- [ ] **Step 5: 回归测试 — Point / LineString 图层**

1. 导入包含 Point 和 LineString 图层的 Shapefile
2. 验证它们仍然正常生成 OdDbPoint 和 [[OdDbPolyline]]

- [ ] **Step 6: 回归测试 — 颜色、线型、图层名**

1. 在 ImportGisModal 中修改颜色、线型、CAD 图层名
2. 验证这些属性仍然正确应用到生成的实体上

- [ ] **Step 7: Final Commit**

```bash
git commit -m "test(gis): verify entity type passthrough for GIS import"
```

## 相关笔记

- [[plans]]
- [[Legend Analysis Redesign Implementation Plan]]
- [[GIS File Import Implementation Plan]]
- [[UAOdcadCore GIS Service Implementation Plan]]
- [[DWG 导出 GIS 按 CAD 图层过滤 — 实施计划]]
- [[WASM License Gate Implementation Plan]]
- [[GIS 目录面板 + 调图/属性查询 Implementation Plan]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
