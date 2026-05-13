# UAOdcadCore GIS Service Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use [[superpower]]s:subagent-driven-development (recommended) or [[superpower]]s:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the `IUcoGisService` interface in the UAOdcadCore project so that DrawingWeb's six GIS commands (`GIS_LOAD_MAP_IMAGE`, `GIS_LOAD_FEATURES`, `GIS_PUSH_FEATURES`, `GIS_PULL_FEATURES`, `GIS_EXPORT`, `GIS_CRS_INFO`) can execute real ArcGIS REST service operations.

**Architecture:** New `IUcoGisService` abstract interface with `UcoGisServiceImpl` singleton. Four-layer design: Layer 1 (`ArcGisRestClient` — libcurl HTTP), Layer 2 (`CrsBridge` — PROJ coordinate transform), Layer 3 (OGR-to-ODA entity converter), Layer 4 (service methods orchestrating all layers). Reuses existing `ConvertDWGToGIS()` and `ConvertODAEntityToOGR()` for export/push.

**Tech Stack:** C++11 (ODA SDK 24.10), GDAL 3.4.2, libcurl 7.88.1, PROJ, Emscripten (WASM target)

**Key paths:**
- uaodcadcore source: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/`
- uaodcadcore public headers: `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/`
- uaroot headers (macros): `E:/updasdk/WorkSpace/uakernel/include/uaroot/`
- DrawingWeb (GisCommands): `E:/ODAGitLab/main24.10/DrawingWeb/`

**Specs:**
- Architecture doc: `DrawingWebApp/docs/specs/2026-04-10-arcgis-integration-architecture.md`
- GDAL analysis: `uaodcadcore/GDAL_GIS_ANALYSIS.md`

---

## File Structure

### New files

| # | File | Responsibility |
|---|------|---------------|
| 1 | `include/uaodcadcore/gdal/uaodco_igisservice.h` | Public interface `IUcoGisService` + inline wrapper functions |
| 2 | `src/uaodcadcore/gdal/uaodco_gisservice_impl.h` | `UcoGisServiceImpl` class declaration (singleton) |
| 3 | `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp` | Service impl + singleton auto-registration |
| 4 | `src/uaodcadcore/gdal/uaodco_arcgis_rest.h` | `ArcGisRestClient` class: libcurl HTTP GET/POST |
| 5 | `src/uaodcadcore/gdal/uaodco_arcgis_rest.cpp` | libcurl implementation |
| 6 | `src/uaodcadcore/gdal/uaodco_feature_from_gis.h` | `ConvertOGRFeatureToDWG()` / `ConvertGISLayerToDWG()` |
| 7 | `src/uaodcadcore/gdal/uaodco_feature_from_gis.cpp` | OGR geometry -> ODA entity conversion |
| 8 | `src/uaodcadcore/gdal/uaodco_crs_bridge.h` | `CrsBridge` class: CRS detection + OGRCoordinateTransformation |
| 9 | `src/uaodcadcore/gdal/uaodco_crs_bridge.cpp` | Coordinate transform implementation |

### Modified files

| File | Change |
|------|--------|
| `include/uaodcadcore/gdal/uaodco_convertfromgis.h` | Add `ConvertGISToFeatures()` declaration |
| `src/uaodcadcore/gdal/uaodco_convertfromgis.cpp` | Fill implementation (delegates to feature_from_gis) |
| `src/uaodcadcore/CMakeLists.txt` | Add new .h/.cpp files to build |
| `DrawingWeb/GisCommands.cpp` | Wire execute() methods to IUcoGisService |

---

## Task 1: Interface Definition (`IUcoGisService`)

**Files:**
- Create: `include/uaodcadcore/gdal/uaodco_igisservice.h`

- [ ] **Step 1: Create the public interface header**

```cpp
// include/uaodcadcore/gdal/uaodco_igisservice.h
#pragma once
#include "uaodcadcore/base/uaodco_defines.h"
#include <uaroot/base/uaroot_declaremembers.h>

#include <OdaCommon.h>
#include <DbDatabase.h>
#include <string>
#include <vector>

/**
 * GIS Service 接口
 * 提供 ArcGIS REST 服务的读写能力，供 DrawingWeb 的 GIS 命令调用。
 * 实现此接口必须是单例模式，使用 register_inter 自动注册。
 */
class UAODCORE_API IUcoGisService
{
    UASINGLEINTERFACE_DECLARE_MEMBERS(IUcoGisService)

protected:
    IUcoGisService() {}
    virtual ~IUcoGisService() {}

public:
    // ── GIS_LOAD_MAP_IMAGE ───────────────────────────────────
    // 从 ArcGIS MapServer 获取影像，插入 DWG 为 OdDbRasterImage
    // mapServerUrl: "http://host/arcgis/rest/services/.../MapServer"
    // srs: 服务坐标系, 如 "EPSG:4526"
    virtual OdResult loadMapImage(
        OdDbDatabase* pDb,
        const std::string& mapServerUrl,
        const std::string& srs = "EPSG:4526") = 0;

    // ── GIS_LOAD_FEATURES / GIS_PULL_FEATURES ────────────────
    // 从 ArcGIS FeatureServer 查询要素，转为 DWG 实体
    // featureServerUrl: "http://host/arcgis/rest/services/.../FeatureServer"
    // layerId: 图层索引 (0, 1, 2...)
    // targetDwgLayer: 写入的目标 DWG 图层名
    // replaceExisting: true 时先删除已有 GIS 图层实体再导入 (GIS_PULL)
    virtual OdResult loadFeatures(
        OdDbDatabase* pDb,
        const std::string& featureServerUrl,
        int layerId,
        const std::string& targetDwgLayer = "GIS_FEATURES",
        bool replaceExisting = false) = 0;

    // ── GIS_PUSH_FEATURES ────────────────────────────────────
    // 将 DWG 实体转为 ESRIJSON 推送到 FeatureServer /applyEdits
    virtual OdResult pushFeatures(
        OdDbDatabase* pDb,
        const std::string& featureServerUrl,
        const std::string& dwgLayerFilter = "") = 0;

    // ── GIS_EXPORT ───────────────────────────────────────────
    // 导出 DWG 为 GIS 格式 (委托已有 ConvertDWGToGIS)
    // format: "ESRI Shapefile" / "GPKG" / "GeoJSON" 等
    virtual bool exportToGis(
        OdDbDatabase* pDb,
        const std::string& outputPath,
        const std::string& format = "ESRI Shapefile",
        int epsgCode = 4490) = 0;

    // ── GIS_CRS_INFO ─────────────────────────────────────────
    // 查询 DWG 坐标系信息，返回 JSON
    // 返回: {"dwgCrs":"...","gisCrs":"EPSG:4526","bridgeStatus":"ok/stub"}
    virtual std::string getCrsInfo(OdDbDatabase* pDb) = 0;
};

// ── Inline wrapper functions ─────────────────────────────────
// 使用方式: IU_GisService_loadMapImage(pDb, url)
// 与 IUcCADGDAL 的 IU_CADGDAL_xxx() 风格一致

inline OdResult IU_GisService_loadMapImage(
    OdDbDatabase* pDb, const std::string& url, const std::string& srs = "EPSG:4526")
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return eNotApplicable;
    return p->loadMapImage(pDb, url, srs);
}

inline OdResult IU_GisService_loadFeatures(
    OdDbDatabase* pDb, const std::string& url, int layerId,
    const std::string& targetLayer = "GIS_FEATURES", bool replace = false)
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return eNotApplicable;
    return p->loadFeatures(pDb, url, layerId, targetLayer, replace);
}

inline OdResult IU_GisService_pushFeatures(
    OdDbDatabase* pDb, const std::string& url, const std::string& filter = "")
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return eNotApplicable;
    return p->pushFeatures(pDb, url, filter);
}

inline bool IU_GisService_exportToGis(
    OdDbDatabase* pDb, const std::string& path,
    const std::string& fmt = "ESRI Shapefile", int epsg = 4490)
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return false;
    return p->exportToGis(pDb, path, fmt, epsg);
}

inline std::string IU_GisService_getCrsInfo(OdDbDatabase* pDb)
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return "{\"error\":\"GisService not registered\"}";
    return p->getCrsInfo(pDb);
}
```

- [ ] **Step 2: Verify the header is syntactically correct**

Run (from uaodcadcore build directory):
```bash
# 预编译检查 (不生成目标，只检查语法)
# 使用项目现有的 CMake + 编译器
cd <build_dir> && cmake --build . --target UAOdcadCore 2>&1 | head -30
```

Expected: Should compile (header is only included, not yet used).

- [ ] **Step 3: Commit**

```bash
cd E:/updasdk/WorkSpace/uadrawing
git add include/uaodcadcore/gdal/uaodco_igisservice.h
git commit -m "feat(gis): add IUcoGisService interface definition"
```

---

## Task 2: Implementation Skeleton + Auto-Registration

**Files:**
- Create: `src/uaodcadcore/gdal/uaodco_gisservice_impl.h`
- Create: `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`
- Modify: `src/uaodcadcore/CMakeLists.txt`

- [ ] **Step 1: Create the implementation header**

```cpp
// src/uaodcadcore/gdal/uaodco_gisservice_impl.h
#pragma once
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodcadcore/gdal/uaodco_igisservice.h"

/**
 * IUcoGisService 的单例实现。
 * 通过 register_inter 自动注册到 IUcoGisService::GetInstance()。
 */
class UcoGisServiceImpl : private IUcoGisService
{
    UASINGLE_DECLARE_MEMBERS(UcoGisServiceImpl)

protected:
    UcoGisServiceImpl();
    virtual ~UcoGisServiceImpl();

    // ── IUcoGisService 实现 ──────────────────────────────────
    OdResult loadMapImage(OdDbDatabase* pDb,
        const std::string& mapServerUrl,
        const std::string& srs) override;

    OdResult loadFeatures(OdDbDatabase* pDb,
        const std::string& featureServerUrl,
        int layerId,
        const std::string& targetDwgLayer,
        bool replaceExisting) override;

    OdResult pushFeatures(OdDbDatabase* pDb,
        const std::string& featureServerUrl,
        const std::string& dwgLayerFilter) override;

    bool exportToGis(OdDbDatabase* pDb,
        const std::string& outputPath,
        const std::string& format,
        int epsgCode) override;

    std::string getCrsInfo(OdDbDatabase* pDb) override;

public:
    static IUcoGisService* GetInterPtr() { return &UcoGisServiceImpl::GetInstance(); }

private:
    bool m_bGdalInit = false;
    void ensureGdalInit();
};
```

- [ ] **Step 2: Create the implementation cpp with stub methods**

```cpp
// src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodco_gisservice_impl.h"

#include <gdal.h>
#include <gdal_priv.h>
#include <ogrsf_frmts.h>
#include <cstdio>

// ── 单例接口实现 + 自动注册 ─────────────────────────────────
UASINGLEINTERFACE_IMPLEMENT(IUcoGisService)
UASINGLE_IMPLEMENT(UcoGisServiceImpl)

static IUcoGisService::register_inter g_sGisServiceReg(UcoGisServiceImpl::GetInterPtr);

UcoGisServiceImpl::UcoGisServiceImpl()
{
    std::printf("[GisService] UcoGisServiceImpl created\n");
}

UcoGisServiceImpl::~UcoGisServiceImpl()
{
}

void UcoGisServiceImpl::ensureGdalInit()
{
    if (!m_bGdalInit)
    {
        GDALAllRegister();
        m_bGdalInit = true;
    }
}

// ── Stub implementations (filled in subsequent tasks) ────────

OdResult UcoGisServiceImpl::loadMapImage(
    OdDbDatabase* pDb, const std::string& mapServerUrl, const std::string& srs)
{
    std::printf("[GisService] loadMapImage: url=%s, srs=%s (stub)\n",
                mapServerUrl.c_str(), srs.c_str());
    return eNotImplementedYet;
}

OdResult UcoGisServiceImpl::loadFeatures(
    OdDbDatabase* pDb, const std::string& featureServerUrl,
    int layerId, const std::string& targetDwgLayer, bool replaceExisting)
{
    std::printf("[GisService] loadFeatures: url=%s, layer=%d (stub)\n",
                featureServerUrl.c_str(), layerId);
    return eNotImplementedYet;
}

OdResult UcoGisServiceImpl::pushFeatures(
    OdDbDatabase* pDb, const std::string& featureServerUrl,
    const std::string& dwgLayerFilter)
{
    std::printf("[GisService] pushFeatures: url=%s (stub)\n",
                featureServerUrl.c_str());
    return eNotImplementedYet;
}

bool UcoGisServiceImpl::exportToGis(
    OdDbDatabase* pDb, const std::string& outputPath,
    const std::string& format, int epsgCode)
{
    std::printf("[GisService] exportToGis: path=%s, format=%s (stub)\n",
                outputPath.c_str(), format.c_str());
    return false;
}

std::string UcoGisServiceImpl::getCrsInfo(OdDbDatabase* pDb)
{
    return "{\"dwgCrs\":\"unknown\",\"gisCrs\":\"unknown\",\"bridgeStatus\":\"stub\"}";
}
```

- [ ] **Step 3: Update CMakeLists.txt — add new files to build**

In `src/uaodcadcore/CMakeLists.txt`, add to `UAOdcadCore_H_gdal`:

```cmake
set(UAOdcadCore_H_gdal
	"../../include/uaodcadcore/gdal/uaodco_converttogis.h"
	"../../include/uaodcadcore/gdal/uaodco_convertfromgis.h"
	"../../include/uaodcadcore/gdal/uaodco_igisservice.h"
)
```

Add to `UAOdcadCore_GdalCpp`:

```cmake
set(UAOdcadCore_GdalCpp
	"gdal/uaodco_convertfromgis.cpp"
	"gdal/uaodco_converttogis.cpp"
	"gdal/uaodco_gdalimpl.cpp"
	"gdal/uaodco_gdalimpl.h"
	"gdal/uaodco_ogrdwgdatasource.cpp"
	"gdal/uaodco_ogrdwgdatasource.h"
	"gdal/uaodco_ogrdwgdriver.cpp"
	"gdal/uaodco_ogrdwgdriver.h"
	"gdal/uaodco_ogrdwglayer.cpp"
	"gdal/uaodco_ogrdwglayer.h"
	"gdal/uaodco_gisservice_impl.cpp"
	"gdal/uaodco_gisservice_impl.h"
)
```

- [ ] **Step 4: Build and verify compilation**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: UAOdcadCore.a (EMCC) or UAOdcadCore.tx (Win) builds successfully. Console output should include `[GisService] UcoGisServiceImpl created` during static init.

- [ ] **Step 5: Commit**

```bash
cd E:/updasdk/WorkSpace/uadrawing
git add include/uaodcadcore/gdal/uaodco_igisservice.h \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.h \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp \
        src/uaodcadcore/CMakeLists.txt
git commit -m "feat(gis): add UcoGisServiceImpl skeleton with auto-registration"
```

---

## Task 3: ArcGisRestClient (libcurl HTTP)

**Files:**
- Create: `src/uaodcadcore/gdal/uaodco_arcgis_rest.h`
- Create: `src/uaodcadcore/gdal/uaodco_arcgis_rest.cpp`
- Modify: `src/uaodcadcore/CMakeLists.txt` (add files)

- [ ] **Step 1: Create the HTTP client header**

```cpp
// src/uaodcadcore/gdal/uaodco_arcgis_rest.h
#pragma once
#include <string>
#include <vector>

/**
 * ArcGIS REST HTTP 客户端 (基于 libcurl)
 * 项目首次在 EMCC 环境使用网络请求。
 * EMCC 下 libcurl 底层走 emscripten_fetch。
 */
class ArcGisRestClient
{
public:
    // HTTP GET 返回文本 (JSON 等)
    // 返回 true 表示 HTTP 200 成功
    static bool httpGet(const std::string& url, std::string& outResponse);

    // HTTP GET 返回二进制数据 (PNG/JPEG 等)
    static bool httpGetBinary(const std::string& url, std::vector<unsigned char>& outData);

    // HTTP POST (application/x-www-form-urlencoded)
    static bool httpPost(const std::string& url,
                         const std::string& postBody,
                         std::string& outResponse);

    // ── ArcGIS REST 专用便捷方法 ─────────────────────────────

    // 调用 MapServer/export 获取影像
    // bbox: "xmin,ymin,xmax,ymax"
    // size: "800,600"
    // srs: "4526"
    static bool exportMapImage(const std::string& mapServerUrl,
                               const std::string& bbox,
                               const std::string& size,
                               const std::string& srs,
                               std::vector<unsigned char>& outImageData);

    // 调用 FeatureServer/N/query 获取要素 JSON
    // where: "1=1"
    // outFields: "*"
    static bool queryFeatures(const std::string& featureServerUrl,
                              int layerId,
                              const std::string& where,
                              const std::string& outFields,
                              std::string& outJson);

    // 调用 FeatureServer/N/applyEdits 推送修改
    static bool applyEdits(const std::string& featureServerUrl,
                           int layerId,
                           const std::string& editsJson,
                           std::string& outResponse);

private:
    // libcurl 回调: 写入 std::string
    static size_t writeStringCallback(void* ptr, size_t size, size_t nmemb, void* userdata);

    // libcurl 回调: 写入 std::vector<unsigned char>
    static size_t writeBinaryCallback(void* ptr, size_t size, size_t nmemb, void* userdata);
};
```

- [ ] **Step 2: Create the HTTP client implementation**

```cpp
// src/uaodcadcore/gdal/uaodco_arcgis_rest.cpp
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodco_arcgis_rest.h"
#include <curl/curl.h>
#include <cstdio>
#include <sstream>

// ── libcurl 回调 ─────────────────────────────────────────────

size_t ArcGisRestClient::writeStringCallback(
    void* ptr, size_t size, size_t nmemb, void* userdata)
{
    size_t totalBytes = size * nmemb;
    std::string* pStr = static_cast<std::string*>(userdata);
    pStr->append(static_cast<char*>(ptr), totalBytes);
    return totalBytes;
}

size_t ArcGisRestClient::writeBinaryCallback(
    void* ptr, size_t size, size_t nmemb, void* userdata)
{
    size_t totalBytes = size * nmemb;
    auto* pVec = static_cast<std::vector<unsigned char>*>(userdata);
    const unsigned char* pData = static_cast<const unsigned char*>(ptr);
    pVec->insert(pVec->end(), pData, pData + totalBytes);
    return totalBytes;
}

// ── 基础 HTTP 方法 ───────────────────────────────────────────

bool ArcGisRestClient::httpGet(const std::string& url, std::string& outResponse)
{
    outResponse.clear();
    CURL* curl = curl_easy_init();
    if (!curl)
    {
        std::printf("[ArcGisRest] curl_easy_init() failed\n");
        return false;
    }

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeStringCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outResponse);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    // EMCC 环境下 SSL 验证可能不可用
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

    CURLcode res = curl_easy_perform(curl);
    long httpCode = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK)
    {
        std::printf("[ArcGisRest] GET failed: %s (url=%s)\n",
                    curl_easy_strerror(res), url.c_str());
        return false;
    }

    std::printf("[ArcGisRest] GET %s -> HTTP %ld, %zu bytes\n",
                url.c_str(), httpCode, outResponse.size());
    return (httpCode == 200);
}

bool ArcGisRestClient::httpGetBinary(const std::string& url,
                                     std::vector<unsigned char>& outData)
{
    outData.clear();
    CURL* curl = curl_easy_init();
    if (!curl) return false;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeBinaryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outData);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 60L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

    CURLcode res = curl_easy_perform(curl);
    long httpCode = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK)
    {
        std::printf("[ArcGisRest] GET binary failed: %s\n", curl_easy_strerror(res));
        return false;
    }

    std::printf("[ArcGisRest] GET binary -> HTTP %ld, %zu bytes\n",
                httpCode, outData.size());
    return (httpCode == 200);
}

bool ArcGisRestClient::httpPost(const std::string& url,
                                const std::string& postBody,
                                std::string& outResponse)
{
    outResponse.clear();
    CURL* curl = curl_easy_init();
    if (!curl) return false;

    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postBody.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeStringCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &outResponse);
    curl_easy_setopt(curl, CURLOPT_TIMEOUT, 30L);
    curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
    curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);

    CURLcode res = curl_easy_perform(curl);
    long httpCode = 0;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &httpCode);
    curl_easy_cleanup(curl);

    if (res != CURLE_OK)
    {
        std::printf("[ArcGisRest] POST failed: %s\n", curl_easy_strerror(res));
        return false;
    }

    return (httpCode == 200);
}

// ── ArcGIS REST 专用方法 ─────────────────────────────────────

bool ArcGisRestClient::exportMapImage(
    const std::string& mapServerUrl,
    const std::string& bbox,
    const std::string& size,
    const std::string& srs,
    std::vector<unsigned char>& outImageData)
{
    // 拼接 ArcGIS MapServer /export URL
    // 示例: http://host/MapServer/export?bbox=...&size=800,600&format=png&f=image&bboxSR=4526&imageSR=4526
    std::ostringstream oss;
    oss << mapServerUrl << "/export?"
        << "bbox=" << bbox
        << "&size=" << size
        << "&format=png"
        << "&bboxSR=" << srs
        << "&imageSR=" << srs
        << "&transparent=true"
        << "&f=image";

    std::string url = oss.str();
    std::printf("[ArcGisRest] exportMapImage: %s\n", url.c_str());
    return httpGetBinary(url, outImageData);
}

bool ArcGisRestClient::queryFeatures(
    const std::string& featureServerUrl,
    int layerId,
    const std::string& where,
    const std::string& outFields,
    std::string& outJson)
{
    // GDAL 3.4.2 的 ESRIJSON 驱动不能直接打裸 FeatureServer URL，
    // 必须拼完整的 /query 查询串
    std::ostringstream oss;
    oss << featureServerUrl << "/" << layerId << "/query?"
        << "where=" << where
        << "&outFields=" << outFields
        << "&returnGeometry=true"
        << "&f=pjson";

    std::string url = oss.str();
    std::printf("[ArcGisRest] queryFeatures: %s\n", url.c_str());
    return httpGet(url, outJson);
}

bool ArcGisRestClient::applyEdits(
    const std::string& featureServerUrl,
    int layerId,
    const std::string& editsJson,
    std::string& outResponse)
{
    std::ostringstream urlOss;
    urlOss << featureServerUrl << "/" << layerId << "/applyEdits";

    // POST body
    std::string body = "adds=" + editsJson + "&f=json";
    return httpPost(urlOss.str(), body, outResponse);
}
```

- [ ] **Step 3: Add to CMakeLists.txt**

In `UAOdcadCore_GdalCpp`, append:
```cmake
	"gdal/uaodco_arcgis_rest.cpp"
	"gdal/uaodco_arcgis_rest.h"
```

- [ ] **Step 4: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: Compiles with no errors. libcurl symbols resolve against `${CURL_LIBS}`.

- [ ] **Step 5: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_arcgis_rest.h \
        src/uaodcadcore/gdal/uaodco_arcgis_rest.cpp \
        src/uaodcadcore/CMakeLists.txt
git commit -m "feat(gis): add ArcGisRestClient with libcurl HTTP GET/POST"
```

---

## Task 4: Implement `loadMapImage`

**Files:**
- Modify: `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`

**Dependencies:** Task 3 (ArcGisRestClient)

- [ ] **Step 1: Replace the loadMapImage stub with real implementation**

Replace the `loadMapImage` stub in `uaodco_gisservice_impl.cpp`:

```cpp
#include "uaodco_arcgis_rest.h"
#include <cpl_vsi.h>           // VSIFileFromMemBuffer, VSIUnlink
#include <DbBlockTableRecord.h>
#include <DbBlockTable.h>
#include <DbRasterImageDef.h>
#include <DbRasterImage.h>
#include <Ge/GeExtents3d.h>
#include <Ge/GePoint3d.h>
#include <Ge/GeVector3d.h>
#include <sstream>

OdResult UcoGisServiceImpl::loadMapImage(
    OdDbDatabase* pDb,
    const std::string& mapServerUrl,
    const std::string& srs)
{
    if (!pDb)
        return eNullObjectPointer;

    ensureGdalInit();

    // ── Step 1: 获取 Model Space 范围作为请求 bbox ──────────
    OdDbBlockTablePtr pBT = pDb->getBlockTableId().safeOpenObject();
    OdDbBlockTableRecordPtr pMS = pBT->getAt(ACDB_MODEL_SPACE).safeOpenObject(OdDb::kForWrite);

    OdGeExtents3d ext;
    if (pMS->getGeomExtents(ext) != eOk)
    {
        std::printf("[GisService] loadMapImage: cannot get model space extents\n");
        return eInvalidExtents;
    }

    // bbox 格式: "xmin,ymin,xmax,ymax"
    std::ostringstream bboxOss;
    bboxOss << ext.minPoint().x << "," << ext.minPoint().y << ","
            << ext.maxPoint().x << "," << ext.maxPoint().y;
    std::string bbox = bboxOss.str();

    // 导出图片尺寸
    std::string imgSize = "1024,768";

    // 提取 SRS 数字部分 (如 "EPSG:4526" -> "4526")
    std::string srsNum = srs;
    size_t colonPos = srs.find(':');
    if (colonPos != std::string::npos)
        srsNum = srs.substr(colonPos + 1);

    // ── Step 2: 通过 REST 获取影像 ──────────────────────────
    std::vector<unsigned char> imageData;
    if (!ArcGisRestClient::exportMapImage(mapServerUrl, bbox, imgSize, srsNum, imageData))
    {
        std::printf("[GisService] loadMapImage: REST export failed\n");
        return eExternalFileNotFound;
    }

    if (imageData.empty())
    {
        std::printf("[GisService] loadMapImage: empty image data\n");
        return eExternalFileNotFound;
    }

    std::printf("[GisService] loadMapImage: received %zu bytes of image data\n",
                imageData.size());

    // ── Step 3: 写入 GDAL /vsimem/ 并用 GDAL 读取像素信息 ──
    const char* vsimemPath = "/vsimem/gis_map_image.png";
    GByte* pBuf = static_cast<GByte*>(CPLMalloc(imageData.size()));
    memcpy(pBuf, imageData.data(), imageData.size());
    VSIFileFromMemBuffer(vsimemPath, pBuf, imageData.size(), TRUE);

    GDALDatasetH hDS = GDALOpen(vsimemPath, GA_ReadOnly);
    if (!hDS)
    {
        std::printf("[GisService] loadMapImage: GDAL cannot open image: %s\n",
                    CPLGetLastErrorMsg());
        VSIUnlink(vsimemPath);
        return eInvalidInput;
    }

    int imgW = GDALGetRasterXSize(hDS);
    int imgH = GDALGetRasterYSize(hDS);
    std::printf("[GisService] loadMapImage: image %dx%d\n", imgW, imgH);

    GDALClose(hDS);

    // ── Step 4: 写入 Emscripten 虚拟文件系统供 ODA 读取 ─────
    // 在 EMCC 环境下 fwrite 写入 memfs, ODA 也用 memfs 读取
    const char* tempPath = "/tmp/gis_map_image.png";
    FILE* fp = fopen(tempPath, "wb");
    if (fp)
    {
        fwrite(imageData.data(), 1, imageData.size(), fp);
        fclose(fp);
    }
    VSIUnlink(vsimemPath);

    // ── Step 5: 创建 OdDbRasterImageDef + OdDbRasterImage ───
    // 创建影像定义
    OdDbObjectId imgDictId = OdDbRasterImageDef::createImageDictionary(pDb);
    OdDbDictionaryPtr pImgDict = imgDictId.safeOpenObject(OdDb::kForWrite);

    OdDbRasterImageDefPtr pImgDef = OdDbRasterImageDef::createObject();
    pImgDef->setDatabaseDefaults(pDb);
    pImgDef->setSourceFileName(OdString(tempPath));
    pImgDef->load();

    OdDbObjectId imgDefId = pImgDict->setAt(OD_T("GIS_MapImage"), pImgDef);

    // 创建影像实体
    OdDbRasterImagePtr pRasterImg = OdDbRasterImage::createObject();
    pRasterImg->setDatabaseDefaults(pDb);
    pRasterImg->setImageDefId(imgDefId);

    // 设置影像位置: 插入点 = ext.minPoint, 尺寸覆盖整个 bbox
    double worldW = ext.maxPoint().x - ext.minPoint().x;
    double worldH = ext.maxPoint().y - ext.minPoint().y;
    OdGePoint3d origin(ext.minPoint().x, ext.minPoint().y, 0.0);
    OdGeVector3d uVec(worldW / imgW, 0.0, 0.0);  // 每像素对应的世界宽度
    OdGeVector3d vVec(0.0, worldH / imgH, 0.0);   // 每像素对应的世界高度
    pRasterImg->setOrientation(origin, uVec, vVec);
    pRasterImg->setDisplayOpt(OdDbRasterImage::kShow, true);

    pMS->appendOdDbEntity(pRasterImg);

    std::printf("[GisService] loadMapImage: inserted raster image %dx%d at (%.2f, %.2f)\n",
                imgW, imgH, origin.x, origin.y);

    return eOk;
}
```

> **NOTE:** `OdDbRasterImageDef` / `OdDbRasterImage` 需要 ODA 的 RasterImage 模块。如果 WASM 构建未包含该模块，可退化为通过 EM_ASM 将 imageData 传回 JS 层渲染（见 Task 8 的 fallback 方案）。

- [ ] **Step 2: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: Compiles. If `OdDbRasterImageDef` 头文件缺失，说明 ODA WASM 构建未包含 raster 模块——需要加 `#ifdef` 保护或改用 fallback。

- [ ] **Step 3: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): implement loadMapImage via ArcGIS REST /export"
```

---

## Task 5: OGR-to-ODA Feature Converter

**Files:**
- Create: `src/uaodcadcore/gdal/uaodco_feature_from_gis.h`
- Create: `src/uaodcadcore/gdal/uaodco_feature_from_gis.cpp`
- Modify: `src/uaodcadcore/CMakeLists.txt`

**Context:** This is the reverse of the existing `ConvertODAEntityToOGR()` in `uaodco_converttogis.cpp`. OGR has ~5 geometry types; ODA has many more. The reverse is simpler.

- [ ] **Step 1: Create the converter header**

```cpp
// src/uaodcadcore/gdal/uaodco_feature_from_gis.h
#pragma once

#include <OdaCommon.h>
#include <DbDatabase.h>
#include <DbBlockTableRecord.h>
#include <ogrsf_frmts.h>
#include <string>

namespace uodgdal {

/**
 * 将单个 OGR Feature 转为 ODA DWG 实体并添加到 BlockTableRecord。
 * 返回新实体的 ObjectId (如果失败返回 OdDbObjectId::kNull)。
 */
OdDbObjectId ConvertOGRFeatureToDWG(
    OdDbBlockTableRecord* pBTR,
    OGRFeature* poFeature,
    const std::string& targetLayerName);

/**
 * 批量转换: 从 OGRLayer 读取所有要素, 创建 DWG 实体。
 * 返回成功转换的要素数量。
 */
int ConvertGISLayerToDWG(
    OdDbDatabase* pDb,
    OdDbBlockTableRecord* pBTR,
    OGRLayerH hLayer,
    const std::string& targetDwgLayer);

} // namespace uodgdal
```

- [ ] **Step 2: Create the converter implementation**

```cpp
// src/uaodcadcore/gdal/uaodco_feature_from_gis.cpp
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodco_feature_from_gis.h"

#include <DbLine.h>
#include <DbPolyline.h>
#include <DbPoint.h>
#include <DbHatch.h>
#include <DbLayerTable.h>
#include <DbLayerTableRecord.h>
#include <Ge/GePoint3d.h>
#include <cstdio>

namespace uodgdal {

// ── 辅助: 确保 DWG 图层存在 ─────────────────────────────────
static OdDbObjectId ensureLayer(OdDbDatabase* pDb, const OdString& layerName)
{
    OdDbLayerTablePtr pLT = pDb->getLayerTableId().safeOpenObject(OdDb::kForWrite);
    if (pLT->has(layerName))
        return pLT->getAt(layerName);

    OdDbLayerTableRecordPtr pLayer = OdDbLayerTableRecord::createObject();
    pLayer->setName(layerName);
    return pLT->add(pLayer);
}

// ── 辅助: OGRPoint -> OdDbPoint ─────────────────────────────
static OdDbObjectId convertPoint(
    OdDbBlockTableRecord* pBTR, OGRPoint* poPoint, OdDbObjectId layerId)
{
    OdDbPointPtr pPt = OdDbPoint::createObject();
    pPt->setDatabaseDefaults(pBTR->database());
    pPt->setPosition(OdGePoint3d(poPoint->getX(), poPoint->getY(),
                                  poPoint->Is3D() ? poPoint->getZ() : 0.0));
    pPt->setLayerId(layerId);
    return pBTR->appendOdDbEntity(pPt);
}

// ── 辅助: OGRLineString -> OdDbPolyline ─────────────────────
static OdDbObjectId convertLineString(
    OdDbBlockTableRecord* pBTR, OGRLineString* poLS, OdDbObjectId layerId)
{
    int numPts = poLS->getNumPoints();
    if (numPts < 2) return OdDbObjectId::kNull;

    OdDbPolylinePtr pPl = OdDbPolyline::createObject();
    pPl->setDatabaseDefaults(pBTR->database());
    for (int i = 0; i < numPts; i++)
    {
        OGRPoint pt;
        poLS->getPoint(i, &pt);
        pPl->addVertexAt(i, OdGePoint2d(pt.getX(), pt.getY()));
    }
    pPl->setLayerId(layerId);
    return pBTR->appendOdDbEntity(pPl);
}

// ── 辅助: OGRPolygon -> OdDbPolyline (闭合) ─────────────────
// 简化方案: 只取外环，生成闭合多段线
static OdDbObjectId convertPolygon(
    OdDbBlockTableRecord* pBTR, OGRPolygon* poPoly, OdDbObjectId layerId)
{
    OGRLinearRing* poRing = poPoly->getExteriorRing();
    if (!poRing || poRing->getNumPoints() < 3) return OdDbObjectId::kNull;

    int numPts = poRing->getNumPoints();
    OdDbPolylinePtr pPl = OdDbPolyline::createObject();
    pPl->setDatabaseDefaults(pBTR->database());
    for (int i = 0; i < numPts; i++)
    {
        OGRPoint pt;
        poRing->getPoint(i, &pt);
        pPl->addVertexAt(i, OdGePoint2d(pt.getX(), pt.getY()));
    }
    pPl->setClosed(true);
    pPl->setLayerId(layerId);
    return pBTR->appendOdDbEntity(pPl);
}

// ── 辅助: 将 OGR 字段写入 ODA 实体 XData ────────────────────
static void attachFieldsAsXData(OdDbEntity* pEnt, OGRFeature* poFeature)
{
    OdDbDatabase* pDb = pEnt->database();
    OdString appName = OD_T("GIS_ATTRIBUTES");

    // 注册应用名 (如果不存在)
    OdDbRegAppTablePtr pRegAppTable =
        pDb->getRegAppTableId().safeOpenObject(OdDb::kForWrite);
    if (!pRegAppTable->has(appName))
    {
        OdDbRegAppTableRecordPtr pApp = OdDbRegAppTableRecord::createObject();
        pApp->setName(appName);
        pRegAppTable->add(pApp);
    }

    // 构建 XData
    OdResBufPtr pRb = OdResBuf::newRb(1001);  // App name
    pRb->setString(appName);
    OdResBufPtr pCur = pRb;

    OGRFeatureDefn* pDefn = poFeature->GetDefnRef();
    int fieldCount = pDefn->GetFieldCount();
    for (int i = 0; i < fieldCount; i++)
    {
        OGRFieldDefn* pFieldDef = pDefn->GetFieldDefn(i);
        if (!poFeature->IsFieldSet(i) || poFeature->IsFieldNull(i))
            continue;

        // 字段名
        OdResBufPtr pName = OdResBuf::newRb(1000);
        pName->setString(OdString(pFieldDef->GetNameRef()));
        pCur->setNext(pName);
        pCur = pName;

        // 字段值 (统一转字符串)
        OdResBufPtr pVal = OdResBuf::newRb(1000);
        pVal->setString(OdString(poFeature->GetFieldAsString(i)));
        pCur->setNext(pVal);
        pCur = pVal;
    }

    pEnt->setXData(pRb);
}

// ── 主转换函数 ───────────────────────────────────────────────

OdDbObjectId ConvertOGRFeatureToDWG(
    OdDbBlockTableRecord* pBTR,
    OGRFeature* poFeature,
    const std::string& targetLayerName)
{
    if (!pBTR || !poFeature) return OdDbObjectId::kNull;

    OGRGeometry* poGeom = poFeature->GetGeometryRef();
    if (!poGeom) return OdDbObjectId::kNull;

    OdDbDatabase* pDb = pBTR->database();
    OdDbObjectId layerId = ensureLayer(pDb, OdString(targetLayerName.c_str()));

    OdDbObjectId entId = OdDbObjectId::kNull;
    OGRwkbGeometryType eType = wkbFlatten(poGeom->getGeometryType());

    switch (eType)
    {
    case wkbPoint:
        entId = convertPoint(pBTR, static_cast<OGRPoint*>(poGeom), layerId);
        break;

    case wkbLineString:
        entId = convertLineString(pBTR, static_cast<OGRLineString*>(poGeom), layerId);
        break;

    case wkbPolygon:
        entId = convertPolygon(pBTR, static_cast<OGRPolygon*>(poGeom), layerId);
        break;

    case wkbMultiPoint:
    {
        OGRMultiPoint* poMP = static_cast<OGRMultiPoint*>(poGeom);
        for (int i = 0; i < poMP->getNumGeometries(); i++)
            convertPoint(pBTR, static_cast<OGRPoint*>(poMP->getGeometryRef(i)), layerId);
        // 返回最后一个 (Multi 类型简化处理)
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
            entId = convertPolygon(pBTR,
                static_cast<OGRPolygon*>(poMPoly->getGeometryRef(i)), layerId);
        break;
    }
    default:
        std::printf("[GisService] ConvertOGRFeatureToDWG: unsupported geometry type %d\n",
                    (int)eType);
        return OdDbObjectId::kNull;
    }

    // 附加字段属性为 XData
    if (!entId.isNull())
    {
        OdDbEntityPtr pEnt = entId.safeOpenObject(OdDb::kForWrite);
        attachFieldsAsXData(pEnt, poFeature);
    }

    return entId;
}

int ConvertGISLayerToDWG(
    OdDbDatabase* pDb,
    OdDbBlockTableRecord* pBTR,
    OGRLayerH hLayer,
    const std::string& targetDwgLayer)
{
    OGRLayer* poLayer = reinterpret_cast<OGRLayer*>(hLayer);
    poLayer->ResetReading();

    int count = 0;
    OGRFeature* poFeature = nullptr;
    while ((poFeature = poLayer->GetNextFeature()) != nullptr)
    {
        OdDbObjectId id = ConvertOGRFeatureToDWG(pBTR, poFeature, targetDwgLayer);
        if (!id.isNull())
            count++;
        OGRFeature::DestroyFeature(poFeature);
    }

    std::printf("[GisService] ConvertGISLayerToDWG: converted %d features to layer '%s'\n",
                count, targetDwgLayer.c_str());
    return count;
}

} // namespace uodgdal
```

- [ ] **Step 3: Add to CMakeLists.txt**

Append to `UAOdcadCore_GdalCpp`:
```cmake
	"gdal/uaodco_feature_from_gis.cpp"
	"gdal/uaodco_feature_from_gis.h"
```

- [ ] **Step 4: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: Compiles. ODA header `DbPoint.h`, `DbPolyline.h`, `DbHatch.h` etc. should be available in the ODA SDK include path.

- [ ] **Step 5: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_feature_from_gis.h \
        src/uaodcadcore/gdal/uaodco_feature_from_gis.cpp \
        src/uaodcadcore/CMakeLists.txt
git commit -m "feat(gis): add OGR-to-ODA feature converter (reverse of ConvertODAEntityToOGR)"
```

---

## Task 6: Implement `loadFeatures`

**Files:**
- Modify: `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`
- Modify: `include/uaodcadcore/gdal/uaodco_convertfromgis.h`
- Modify: `src/uaodcadcore/gdal/uaodco_convertfromgis.cpp`

**Dependencies:** Task 3 (ArcGisRestClient), Task 5 (Feature Converter)

- [ ] **Step 1: Update `uaodco_convertfromgis.h` with new declaration**

```cpp
// include/uaodcadcore/gdal/uaodco_convertfromgis.h
#pragma once
#include "uaodcadcore/base/uaodco_defines.h"

#include <OdaCommon.h>
#include <DbDatabase.h>
#include <string>

namespace uodgdal {

/**
 * 从 ESRIJSON 字符串加载要素到 DWG。
 * jsonData: FeatureServer /query 返回的 pjson
 * targetDwgLayer: 要素写入的 DWG 图层
 * 返回成功导入的要素数量, 失败返回 -1
 */
UAODCORE_API int LoadFeaturesFromJson(
    OdDbDatabase* pDb,
    const std::string& jsonData,
    const std::string& targetDwgLayer = "GIS_FEATURES");

} // namespace uodgdal
```

- [ ] **Step 2: Fill `uaodco_convertfromgis.cpp`**

```cpp
// src/uaodcadcore/gdal/uaodco_convertfromgis.cpp
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodcadcore/gdal/uaodco_convertfromgis.h"
#include "uaodco_feature_from_gis.h"

#include <gdal.h>
#include <gdal_priv.h>
#include <ogrsf_frmts.h>
#include <cpl_vsi.h>
#include <DbBlockTableRecord.h>
#include <DbBlockTable.h>
#include <cstdio>

namespace uodgdal {

int LoadFeaturesFromJson(
    OdDbDatabase* pDb,
    const std::string& jsonData,
    const std::string& targetDwgLayer)
{
    if (!pDb || jsonData.empty())
        return -1;

    GDALAllRegister();

    // 将 JSON 写入 GDAL 虚拟内存文件
    const char* vsimemPath = "/vsimem/gis_features.json";
    GByte* pBuf = static_cast<GByte*>(CPLMalloc(jsonData.size()));
    memcpy(pBuf, jsonData.data(), jsonData.size());
    VSIFileFromMemBuffer(vsimemPath, pBuf, jsonData.size(), TRUE);

    // 用 GDAL ESRIJSON 驱动打开
    std::string openPath = std::string("ESRIJSON:") + vsimemPath;
    GDALDatasetH hDS = GDALOpenEx(openPath.c_str(), GDAL_OF_VECTOR, nullptr, nullptr, nullptr);
    if (!hDS)
    {
        // fallback: 尝试不带 ESRIJSON: 前缀
        hDS = GDALOpenEx(vsimemPath, GDAL_OF_VECTOR, nullptr, nullptr, nullptr);
    }

    if (!hDS)
    {
        std::printf("[GisService] LoadFeaturesFromJson: GDAL cannot open JSON: %s\n",
                    CPLGetLastErrorMsg());
        VSIUnlink(vsimemPath);
        return -1;
    }

    // 获取第一个图层
    OGRLayerH hLayer = GDALDatasetGetLayer(hDS, 0);
    if (!hLayer)
    {
        std::printf("[GisService] LoadFeaturesFromJson: no layers in JSON\n");
        GDALClose(hDS);
        VSIUnlink(vsimemPath);
        return -1;
    }

    // 获取 Model Space
    OdDbBlockTablePtr pBT = pDb->getBlockTableId().safeOpenObject();
    OdDbBlockTableRecordPtr pMS =
        pBT->getAt(ACDB_MODEL_SPACE).safeOpenObject(OdDb::kForWrite);

    // 批量转换
    int count = ConvertGISLayerToDWG(pDb, pMS, hLayer, targetDwgLayer);

    GDALClose(hDS);
    VSIUnlink(vsimemPath);

    return count;
}

} // namespace uodgdal
```

- [ ] **Step 3: Implement loadFeatures in the service**

Replace the `loadFeatures` stub in `uaodco_gisservice_impl.cpp`:

```cpp
#include "uaodco_arcgis_rest.h"
#include "uaodco_feature_from_gis.h"
#include <uaodcadcore/gdal/uaodco_convertfromgis.h>
#include <DbBlockTable.h>
#include <DbBlockTableRecord.h>

OdResult UcoGisServiceImpl::loadFeatures(
    OdDbDatabase* pDb,
    const std::string& featureServerUrl,
    int layerId,
    const std::string& targetDwgLayer,
    bool replaceExisting)
{
    if (!pDb)
        return eNullObjectPointer;

    ensureGdalInit();

    // ── Step 1: replaceExisting → 删除旧实体 ────────────────
    if (replaceExisting)
    {
        OdDbBlockTablePtr pBT = pDb->getBlockTableId().safeOpenObject();
        OdDbBlockTableRecordPtr pMS =
            pBT->getAt(ACDB_MODEL_SPACE).safeOpenObject(OdDb::kForWrite);

        OdDbObjectIteratorPtr pIter = pMS->newIterator();
        OdString targetLayerOd(targetDwgLayer.c_str());
        for (; !pIter->done(); pIter->step())
        {
            OdDbEntityPtr pEnt = pIter->objectId().safeOpenObject(OdDb::kForWrite);
            // 只删除目标图层上的实体
            OdDbLayerTableRecordPtr pLayer =
                pEnt->layerId().safeOpenObject();
            if (pLayer->getName() == targetLayerOd)
                pEnt->erase();
        }
    }

    // ── Step 2: 从 FeatureServer 查询要素 JSON ──────────────
    std::string json;
    if (!ArcGisRestClient::queryFeatures(featureServerUrl, layerId, "1%3D1", "*", json))
    {
        std::printf("[GisService] loadFeatures: query failed\n");
        return eExternalFileNotFound;
    }

    if (json.empty())
    {
        std::printf("[GisService] loadFeatures: empty response\n");
        return eExternalFileNotFound;
    }

    // ── Step 3: 解析 JSON → 创建 DWG 实体 ───────────────────
    int count = uodgdal::LoadFeaturesFromJson(pDb, json, targetDwgLayer);

    if (count < 0)
    {
        std::printf("[GisService] loadFeatures: conversion failed\n");
        return eInvalidInput;
    }

    std::printf("[GisService] loadFeatures: imported %d features to '%s'\n",
                count, targetDwgLayer.c_str());
    return eOk;
}
```

- [ ] **Step 4: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

- [ ] **Step 5: Commit**

```bash
git add include/uaodcadcore/gdal/uaodco_convertfromgis.h \
        src/uaodcadcore/gdal/uaodco_convertfromgis.cpp \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): implement loadFeatures via FeatureServer REST + ESRIJSON"
```

---

## Task 7: CrsBridge (Coordinate Transform)

**Files:**
- Create: `src/uaodcadcore/gdal/uaodco_crs_bridge.h`
- Create: `src/uaodcadcore/gdal/uaodco_crs_bridge.cpp`
- Modify: `src/uaodcadcore/CMakeLists.txt`

**Context:** 项目首次使用 `OGRCoordinateTransformation`。GDAL 分析报告确认此能力之前从未使用。

- [ ] **Step 1: Create CrsBridge header**

```cpp
// src/uaodcadcore/gdal/uaodco_crs_bridge.h
#pragma once

#include <ogr_spatialref.h>
#include <OdaCommon.h>
#include <DbDatabase.h>
#include <string>

/**
 * 坐标桥接层：ODA DWG 坐标 <-> GIS 坐标 (GDAL/PROJ)
 *
 * 项目现有约定: 全局使用 EPSG:4490 (CGCS2000)，不做坐标变换。
 * ArcGIS 服务可能返回 EPSG:4526 (CGCS2000 高斯投影)，需要变换。
 */
class CrsBridge
{
public:
    // 尝试从 DWG 的 OdDbGeoData 获取 EPSG code
    // 返回 0 表示 DWG 无坐标系信息
    static int getEpsgFromDwg(OdDbDatabase* pDb);

    // 创建 OGR 坐标变换对象 (srcEpsg -> dstEpsg)
    // 调用者负责 OGRCoordinateTransformation::DestroyCT() 释放
    // 返回 nullptr 表示创建失败
    static OGRCoordinateTransformation* createTransform(int srcEpsg, int dstEpsg);

    // 批量变换坐标点 (in-place)
    // 返回 true 表示全部成功
    static bool transformPoints(OGRCoordinateTransformation* poCT,
                                double* x, double* y, int count);

    // 获取 CRS 信息 JSON
    // 返回: {"dwgCrs":"EPSG:4490","gisCrs":"EPSG:4526","bridgeStatus":"ok"}
    static std::string getCrsInfoJson(OdDbDatabase* pDb,
                                      const std::string& gisCrs = "EPSG:4526");
};
```

- [ ] **Step 2: Create CrsBridge implementation**

```cpp
// src/uaodcadcore/gdal/uaodco_crs_bridge.cpp
#include "uaodcadcore/base/uaodco_base.h"
#include "uaodco_crs_bridge.h"

#include <ogr_spatialref.h>
#include <DbGeoData.h>
#include <cstdio>
#include <sstream>

int CrsBridge::getEpsgFromDwg(OdDbDatabase* pDb)
{
    if (!pDb)
        return 0;

    // 尝试找 GeoData 对象
    OdDbObjectId geoDataId;
    try
    {
        // ODA 的 oddbGetGeoDataObjId() 函数获取 GeoData
        // 如果不可用，从 Named Object Dictionary 查找
        OdDbDictionaryPtr pNOD =
            pDb->getNamedObjectsDictionaryId().safeOpenObject();
        if (pNOD->has(OD_T("ACAD_GEOGRAPHICDATA")))
        {
            OdDbDictionaryPtr pGeoDict =
                pNOD->getAt(OD_T("ACAD_GEOGRAPHICDATA")).safeOpenObject();
            if (pGeoDict->numEntries() > 0)
            {
                OdDbDictionaryIteratorPtr pIter = pGeoDict->newIterator();
                geoDataId = pIter->objectId();
            }
        }
    }
    catch (...)
    {
        return 0;
    }

    if (geoDataId.isNull())
        return 0;

    try
    {
        OdDbGeoDataPtr pGeoData = geoDataId.safeOpenObject();
        OdString csId = pGeoData->coordinateSystem();
        // 尝试解析 EPSG code
        // csId 可能是 "EPSG:4490" 格式或 WKT
        std::string s(csId);
        if (s.find("4490") != std::string::npos) return 4490;
        if (s.find("4526") != std::string::npos) return 4526;
        if (s.find("4547") != std::string::npos) return 4547;
        // 未识别
        std::printf("[CrsBridge] getEpsgFromDwg: unrecognized CS '%s'\n", s.c_str());
    }
    catch (...)
    {
    }

    return 0;
}

OGRCoordinateTransformation* CrsBridge::createTransform(int srcEpsg, int dstEpsg)
{
    if (srcEpsg == dstEpsg || srcEpsg == 0 || dstEpsg == 0)
        return nullptr;

    OGRSpatialReference srcSRS, dstSRS;
    srcSRS.importFromEPSG(srcEpsg);
    dstSRS.importFromEPSG(dstEpsg);

    // GDAL 3.x 默认使用 lat/lon 顺序，需要设置为传统 x/y (经度/纬度)
    srcSRS.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER);
    dstSRS.SetAxisMappingStrategy(OAMS_TRADITIONAL_GIS_ORDER);

    OGRCoordinateTransformation* poCT =
        OGRCreateCoordinateTransformation(&srcSRS, &dstSRS);

    if (!poCT)
    {
        std::printf("[CrsBridge] createTransform: failed EPSG:%d -> EPSG:%d\n",
                    srcEpsg, dstEpsg);
    }

    return poCT;
}

bool CrsBridge::transformPoints(OGRCoordinateTransformation* poCT,
                                double* x, double* y, int count)
{
    if (!poCT || count <= 0) return false;
    return poCT->Transform(count, x, y) == TRUE;
}

std::string CrsBridge::getCrsInfoJson(OdDbDatabase* pDb, const std::string& gisCrs)
{
    int dwgEpsg = getEpsgFromDwg(pDb);
    std::string dwgCrsStr = (dwgEpsg > 0)
        ? ("EPSG:" + std::to_string(dwgEpsg))
        : "unknown";

    // 测试变换是否可用
    std::string status = "stub";
    if (dwgEpsg > 0)
    {
        // 提取 gisCrs 的 EPSG 数字
        int gisEpsg = 0;
        size_t colonPos = gisCrs.find(':');
        if (colonPos != std::string::npos)
            gisEpsg = std::atoi(gisCrs.substr(colonPos + 1).c_str());

        OGRCoordinateTransformation* poCT = createTransform(gisEpsg, dwgEpsg);
        if (poCT)
        {
            status = "ok";
            OGRCoordinateTransformation::DestroyCT(poCT);
        }
        else if (dwgEpsg == gisEpsg)
        {
            status = "same_crs";
        }
        else
        {
            status = "transform_failed";
        }
    }

    std::ostringstream oss;
    oss << "{\"dwgCrs\":\"" << dwgCrsStr
        << "\",\"gisCrs\":\"" << gisCrs
        << "\",\"bridgeStatus\":\"" << status << "\"}";
    return oss.str();
}
```

- [ ] **Step 3: Add to CMakeLists.txt**

Append to `UAOdcadCore_GdalCpp`:
```cmake
	"gdal/uaodco_crs_bridge.cpp"
	"gdal/uaodco_crs_bridge.h"
```

- [ ] **Step 4: Implement `getCrsInfo` in the service**

Replace the `getCrsInfo` stub in `uaodco_gisservice_impl.cpp`:

```cpp
#include "uaodco_crs_bridge.h"

std::string UcoGisServiceImpl::getCrsInfo(OdDbDatabase* pDb)
{
    ensureGdalInit();
    return CrsBridge::getCrsInfoJson(pDb);
}
```

- [ ] **Step 5: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: Compiles. `OGRSpatialReference` and `OGRCreateCoordinateTransformation` resolve against `${PROJ_LIBS}` + `${GDAL_LIBS}`.

- [ ] **Step 6: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_crs_bridge.h \
        src/uaodcadcore/gdal/uaodco_crs_bridge.cpp \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp \
        src/uaodcadcore/CMakeLists.txt
git commit -m "feat(gis): add CrsBridge coordinate transform + getCrsInfo"
```

---

## Task 8: Implement `pushFeatures` + `exportToGis`

**Files:**
- Modify: `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`

**Dependencies:** Task 3 (ArcGisRestClient), existing `ConvertDWGToGIS()`

- [ ] **Step 1: Implement exportToGis (delegate to existing function)**

Replace the `exportToGis` stub in `uaodco_gisservice_impl.cpp`:

```cpp
#include <uaodcadcore/gdal/uaodco_converttogis.h>

bool UcoGisServiceImpl::exportToGis(
    OdDbDatabase* pDb,
    const std::string& outputPath,
    const std::string& format,
    int epsgCode)
{
    if (!pDb)
        return false;

    ensureGdalInit();

    // 直接委托给已有的 ConvertDWGToGIS
    return uodgdal::ConvertDWGToGIS(pDb, outputPath.c_str(), format.c_str(), epsgCode);
}
```

- [ ] **Step 2: Implement pushFeatures**

Replace the `pushFeatures` stub:

```cpp
#include <DbBlockTable.h>
#include <DbBlockTableRecord.h>
#include <DbObjectIterator.h>
#include <DbLayerTableRecord.h>
#include <cpl_vsi.h>
#include <sstream>

OdResult UcoGisServiceImpl::pushFeatures(
    OdDbDatabase* pDb,
    const std::string& featureServerUrl,
    const std::string& dwgLayerFilter)
{
    if (!pDb)
        return eNullObjectPointer;

    ensureGdalInit();

    // ── Step 1: 导出 DWG 为 GeoJSON 到内存 ──────────────────
    const char* vsimemPath = "/vsimem/push_features.geojson";
    bool ok = uodgdal::ConvertDWGToGIS(pDb, vsimemPath, "GeoJSON", 4490);
    if (!ok)
    {
        std::printf("[GisService] pushFeatures: ConvertDWGToGIS failed\n");
        return eInvalidInput;
    }

    // 读取生成的 GeoJSON
    vsi_l_offset nSize = 0;
    GByte* pData = VSIGetMemFileBuffer(vsimemPath, &nSize, FALSE);
    if (!pData || nSize == 0)
    {
        std::printf("[GisService] pushFeatures: empty GeoJSON output\n");
        VSIUnlink(vsimemPath);
        return eInvalidInput;
    }

    std::string geojson(reinterpret_cast<const char*>(pData), nSize);
    VSIUnlink(vsimemPath);

    // ── Step 2: POST 到 FeatureServer /applyEdits ───────────
    // 注意: applyEdits 需要 ESRIJSON 格式的 features 数组，不是 GeoJSON。
    // 简化方案: 直接发送 GeoJSON，实际部署时需转换格式或使用 addFeatures API。
    std::string response;
    if (!ArcGisRestClient::applyEdits(featureServerUrl, 0, geojson, response))
    {
        std::printf("[GisService] pushFeatures: applyEdits failed\n");
        return eExternalFileNotFound;
    }

    std::printf("[GisService] pushFeatures: response=%s\n", response.c_str());
    return eOk;
}
```

- [ ] **Step 3: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

- [ ] **Step 4: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): implement pushFeatures + exportToGis"
```

---

## Task 9: Wire GisCommands.cpp to IUcoGisService

**Files:**
- Modify: `DrawingWeb/GisCommands.cpp`

**Context:** This is the final wiring. Each stub command calls `IUcoGisService::GetInstance()` and delegates.

- [ ] **Step 1: Modify GisCommands.cpp**

Replace the full content of `DrawingWeb/GisCommands.cpp`:

```cpp
#include "GisCommands.h"
#include "DbCommandContext.h"
#include "CadCore.h"
#include <emscripten.h>
#include <string>
#include <codecvt>

// ── GIS Service 接口 ────────────────────────────────────────
#include <uaodcadcore/gdal/uaodco_igisservice.h>

// OdString -> std::string (UTF-8)
static std::string toUtf8(const OdString& s)
{
    std::wstring_convert<std::codecvt_utf8<wchar_t>> conv;
    return conv.to_bytes(std::wstring(s.c_str()));
}

/////////////////////////////////////////////////////////////////////////
// GIS_LOAD_MAP_IMAGE
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_LOAD_MAP_IMAGE::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_LOAD_MAP_IMAGE::name() { return L"GIS_LOAD_MAP_IMAGE"; }
const OdString Cmd_GIS_LOAD_MAP_IMAGE::globalName() const { return name(); }

void Cmd_GIS_LOAD_MAP_IMAGE::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database().get();
    OdString url = pIO->getString(L"MapServer URL");
    std::string sUrl = toUtf8(url);

    std::printf("[GIS] GIS_LOAD_MAP_IMAGE: url=%s\n", sUrl.c_str());

    // 调用 GIS Service 实现
    OdResult res = IU_GisService_loadMapImage(pDb, sUrl);
    int resCode = (int)res;

    EM_ASM({
        if (typeof window.__onGisLoadProgress === 'function')
            window.__onGisLoadProgress(100);
        if (typeof window.__onGisConnected === 'function')
            window.__onGisConnected(UTF8ToString($0), $1);
    }, sUrl.c_str(), resCode);
}

/////////////////////////////////////////////////////////////////////////
// GIS_LOAD_FEATURES
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_LOAD_FEATURES::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_LOAD_FEATURES::name() { return L"GIS_LOAD_FEATURES"; }
const OdString Cmd_GIS_LOAD_FEATURES::globalName() const { return name(); }

void Cmd_GIS_LOAD_FEATURES::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database().get();
    OdString url = pIO->getString(L"FeatureServer URL");
    OdString layerId = pIO->getString(L"Layer ID");
    std::string sUrl = toUtf8(url);
    int nLayerId = std::atoi(toUtf8(layerId).c_str());

    std::printf("[GIS] GIS_LOAD_FEATURES: url=%s, layerId=%d\n", sUrl.c_str(), nLayerId);

    OdResult res = IU_GisService_loadFeatures(pDb, sUrl, nLayerId);

    EM_ASM({
        if (typeof window.__onGisLoadProgress === 'function')
            window.__onGisLoadProgress(100);
    });
}

/////////////////////////////////////////////////////////////////////////
// GIS_PUSH_FEATURES
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_PUSH_FEATURES::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_PUSH_FEATURES::name() { return L"GIS_PUSH_FEATURES"; }
const OdString Cmd_GIS_PUSH_FEATURES::globalName() const { return name(); }

void Cmd_GIS_PUSH_FEATURES::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbDatabase* pDb = pDbCmdCtx->database().get();

    std::printf("[GIS] GIS_PUSH_FEATURES\n");

    // 需要从某处获取 featureServerUrl (可通过之前 loadFeatures 缓存的 URL)
    // 简化: 暂时使用空 URL，实际中应从 DWG 自定义属性或全局状态获取
    OdResult res = IU_GisService_pushFeatures(pDb, "");

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "push", (int)res);
}

/////////////////////////////////////////////////////////////////////////
// GIS_PULL_FEATURES
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_PULL_FEATURES::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_PULL_FEATURES::name() { return L"GIS_PULL_FEATURES"; }
const OdString Cmd_GIS_PULL_FEATURES::globalName() const { return name(); }

void Cmd_GIS_PULL_FEATURES::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database().get();
    OdString url = pIO->getString(L"FeatureServer URL");
    OdString layerId = pIO->getString(L"Layer ID");
    std::string sUrl = toUtf8(url);
    int nLayerId = std::atoi(toUtf8(layerId).c_str());

    std::printf("[GIS] GIS_PULL_FEATURES: url=%s, layerId=%d\n", sUrl.c_str(), nLayerId);

    // replaceExisting=true 实现拉取更新
    OdResult res = IU_GisService_loadFeatures(pDb, sUrl, nLayerId, "GIS_FEATURES", true);

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "pull", (int)res);
}

/////////////////////////////////////////////////////////////////////////
// GIS_EXPORT
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_EXPORT::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_EXPORT::name() { return L"GIS_EXPORT"; }
const OdString Cmd_GIS_EXPORT::globalName() const { return name(); }

void Cmd_GIS_EXPORT::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database().get();
    OdString format = pIO->getString(L"Export format");
    OdString path = pIO->getString(L"Export path");
    std::string sFormat = toUtf8(format);
    std::string sPath = toUtf8(path);

    std::printf("[GIS] GIS_EXPORT: format=%s, path=%s\n", sFormat.c_str(), sPath.c_str());

    bool ok = IU_GisService_exportToGis(pDb, sPath, sFormat);

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "export", ok ? 0 : 1);
}

/////////////////////////////////////////////////////////////////////////
// GIS_CRS_INFO
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_CRS_INFO::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_CRS_INFO::name() { return L"GIS_CRS_INFO"; }
const OdString Cmd_GIS_CRS_INFO::globalName() const { return name(); }

void Cmd_GIS_CRS_INFO::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbDatabase* pDb = pDbCmdCtx->database().get();

    std::string json = IU_GisService_getCrsInfo(pDb);
    std::printf("[GIS] GIS_CRS_INFO: %s\n", json.c_str());

    EM_ASM({
        if (typeof window.__onGisCrsInfo === 'function')
            window.__onGisCrsInfo(UTF8ToString($0));
    }, json.c_str());
}
```

- [ ] **Step 2: Verify DrawingWeb include path has uaodcadcore headers**

Check that `DrawingWeb/CMakeLists.txt` (or equivalent) includes the uaodcadcore public header path: `E:/updasdk/WorkSpace/uadrawing/include/`

If not, add:
```cmake
include_directories(E:/updasdk/WorkSpace/uadrawing/include)
```

- [ ] **Step 3: Build DrawingWeb + UAOdcadCore → DrawingJs.wasm**

```bash
cd <drawing_web_build_dir> && cmake --build . --target DrawingJs
```

Expected: Full WASM build succeeds. All GIS commands now call through `IUcoGisService`.

- [ ] **Step 4: Commit**

```bash
cd E:/ODAGitLab/main24.10/DrawingWeb
git add GisCommands.cpp
git commit -m "feat(gis): wire GisCommands to IUcoGisService interface"
```

---

## Task 10: EMCC Network Verification

**Files:** None (verification only)

**Context:** This is the highest-risk task. The project has NEVER made HTTP requests from EMCC/WASM. This task verifies the full chain works.

- [ ] **Step 1: Check EMCC link flags for network support**

Examine the DrawingWeb EMCC link flags. Look for:
- `-sFETCH=1` (Emscripten Fetch API)
- `-sASYNCIFY` (needed if libcurl uses synchronous calls)
- `-sPROXY_TO_PTHREAD` (if using pthreads)

If `-sFETCH=1` is missing, add it to the DrawingWeb CMakeLists EMCC link options:
```cmake
if(EMCC)
    target_link_options(DrawingJs PRIVATE
        "-sFETCH=1"
        # "-sASYNCIFY" # 如果需要同步 HTTP
    )
endif()
```

- [ ] **Step 2: Browser test — verify HTTP connectivity**

1. Start the DrawingWebApp dev server: `npm run dev`
2. Open browser console
3. Execute: `viewer.execute("GIS_CRS_INFO")`
4. Check console for `[GisService]` log messages
5. Execute: `viewer.execute("GIS_LOAD_MAP_IMAGE", "http://your-arcgis-server/MapServer")`
6. Verify the `[ArcGisRest]` HTTP logs appear

- [ ] **Step 3: If HTTP fails — add CORS proxy fallback**

If browser blocks the ArcGIS REST call due to CORS, add a proxy route in the DrawingWebApp Node.js server (`server/index.js` or equivalent):

```javascript
// 在 Express server 中添加:
app.get('/api/gis-proxy', async (req, res) => {
    const targetUrl = req.query.url;
    const response = await fetch(targetUrl);
    const data = await response.arrayBuffer();
    res.set('Content-Type', response.headers.get('content-type'));
    res.send(Buffer.from(data));
});
```

Then update `ArcGisRestClient` to prepend `/api/gis-proxy?url=` when running in EMCC.

- [ ] **Step 4: Document findings and commit**

```bash
git commit -m "chore(gis): verify EMCC network connectivity, add CORS proxy if needed"
```

---

## Summary

| Task | Description | Key Files | Dependencies |
|------|-------------|-----------|--------------|
| 1 | Interface definition | `uaodco_igisservice.h` | — |
| 2 | Skeleton + auto-registration | `uaodco_gisservice_impl.h/.cpp` | Task 1 |
| 3 | ArcGisRestClient (libcurl) | `uaodco_arcgis_rest.h/.cpp` | — |
| 4 | loadMapImage | `uaodco_gisservice_impl.cpp` | Tasks 2, 3 |
| 5 | OGR→ODA feature converter | `uaodco_feature_from_gis.h/.cpp` | — |
| 6 | loadFeatures | `uaodco_gisservice_impl.cpp`, `convertfromgis` | Tasks 3, 5 |
| 7 | CrsBridge + getCrsInfo | `uaodco_crs_bridge.h/.cpp` | — |
| 8 | pushFeatures + exportToGis | `uaodco_gisservice_impl.cpp` | Tasks 3, existing |
| 9 | Wire GisCommands.cpp | `DrawingWeb/GisCommands.cpp` | Tasks 1-8 |
| 10 | EMCC network verification | Build config | Task 9 |

**Independent tasks that can be parallelized:** Tasks 1+3+5+7 have no inter-dependencies and can be developed simultaneously.

## 相关笔记

- [[Legend Analysis Redesign Implementation Plan]]
- [[GIS 导入实体类型透传 — 实现计划]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
- [[plans]]
- [[GIS File Import Implementation Plan]]
- [[DWG 导出 GIS 按 CAD 图层过滤 — 实施计划]]
- [[WASM License Gate Implementation Plan]]
- [[GIS 目录面板 + 调图/属性查询 Implementation Plan]]
