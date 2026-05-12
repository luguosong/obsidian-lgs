# GIS File Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Allow users to open Shapefile/GDB/ZIP files in the browser, convert to DWG for editing, and save back to the original GIS format.

**Architecture:** Extend `IUcoGisService` with `queryGisFile()` and `importGisFile()`. GDAL handles format detection and `/vsizip/` ZIP reading. Frontend provides `ImportGisModal` for layer selection + CRS confirmation, tracks source in `GisStore.sourceInfo`, and supports one-click save-back via `fflate` ZIP download.

**Tech Stack:** C++11 (ODA SDK 24.10), GDAL 3.4.2, PROJ, Emscripten WASM, React 19, Ant Design 6, MobX 6, fflate

**Key paths:**
- uaodcadcore source: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/`
- uaodcadcore public headers: `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/`
- DrawingWeb (commands): `E:/ODAGitLab/main24.10/DrawingWeb/`
- DrawingWebApp: `e:/ODAGitLab/main24.10/DrawingWebApp/`

**Spec:** `DrawingWebApp/docs/specs/2026-04-12-gis-file-import-design.md`

---

## File Structure

### Modified files

| # | File | Change |
|---|------|--------|
| 1 | `include/uaodcadcore/gdal/uaodco_igisservice.h` | Add `queryGisFile()` + `importGisFile()` virtual methods and inline wrappers |
| 2 | `src/uaodcadcore/gdal/uaodco_gisservice_impl.h` | Add 2 override declarations |
| 3 | `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp` | Implement both new methods |
| 4 | `DrawingWeb/GisCommands.h` | Add `Cmd_GIS_QUERY_FILE` + `Cmd_GIS_IMPORT_FILE` classes |
| 5 | `DrawingWeb/GisCommands.cpp` | Implement 2 new command `execute()` methods |
| 6 | `DrawingWebApp/src/stores/GisStore.js` | Add `sourceInfo` + `saveBackToGis()` + `clearSourceInfo()` |
| 7 | `DrawingWebApp/src/hooks/useWasmModule.js` | Register `__onGisFileInfo` + `__onGisImportComplete` callbacks |
| 8 | `DrawingWebApp/src/components/TopBar/TopBar.jsx` | Add GIS import menu items + file input handlers |
| 9 | `DrawingWebApp/src/services/ViewerService.js` | Add `handleOpenGisFolder()` + `handleOpenGisZip()` + `handleGisSaveBack()` |
| 10 | `DrawingWebApp/package.json` | Add `fflate` dependency |

### New files

| # | File | Responsibility |
|---|------|---------------|
| 1 | `DrawingWebApp/src/components/GisService/ImportGisModal.jsx` | Layer selection + CRS confirmation modal |

---

## Task 1: Extend IUcoGisService Interface

**Files:**
- Modify: `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/gdal/uaodco_igisservice.h`
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.h`

- [ ] **Step 1: Add 2 new virtual methods to IUcoGisService**

In `uaodco_igisservice.h`, add after the existing `getCrsInfo` pure virtual (before the closing `};` of the class):

```cpp
    virtual std::string queryGisFile(const std::string& fsPath) = 0;

    virtual OdResult importGisFile(
        OdDbDatabase* pDb,
        const std::string& fsPath,
        const std::string& layerNames,
        int targetEpsg) = 0;
```

- [ ] **Step 2: Add 2 inline wrapper functions**

In `uaodco_igisservice.h`, add after the existing `IU_GisService_getCrsInfo` inline function:

```cpp
inline std::string IU_GisService_queryGisFile(const std::string& path)
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return "{\"error\":\"GisService not registered\"}";
    return p->queryGisFile(path);
}

inline OdResult IU_GisService_importGisFile(
    OdDbDatabase* pDb, const std::string& path,
    const std::string& layers = "", int epsg = 0)
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return eNotApplicable;
    return p->importGisFile(pDb, path, layers, epsg);
}
```

- [ ] **Step 3: Add override declarations to UcoGisServiceImpl**

In `uaodco_gisservice_impl.h`, add after the `getCrsInfo` override declaration:

```cpp
    std::string queryGisFile(const std::string& fsPath) override;
    OdResult importGisFile(OdDbDatabase* pDb, const std::string& fsPath,
                           const std::string& layerNames, int targetEpsg) override;
```

- [ ] **Step 4: Commit**

```bash
git add include/uaodcadcore/gdal/uaodco_igisservice.h src/uaodcadcore/gdal/uaodco_gisservice_impl.h
git commit -m "feat(gis): add queryGisFile + importGisFile to IUcoGisService interface"
```

---

## Task 2: Implement queryGisFile

**Files:**
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`

**Context:** `queryGisFile` opens a GIS file with GDAL, enumerates layers, reads CRS, and returns a JSON string. ZIP files are accessed via GDAL's `/vsizip/` virtual filesystem prefix.

- [ ] **Step 1: Add queryGisFile implementation**

Add at the end of `uaodco_gisservice_impl.cpp`, before the closing (or after `getCrsInfo`):

```cpp
///////////////////////////////////////////////////////////////////////////
// queryGisFile — enumerate layers + CRS from a GIS file
///////////////////////////////////////////////////////////////////////////
std::string UcoGisServiceImpl::queryGisFile(const std::string& fsPath)
{
    ensureGdalInit();

    // ZIP 文件使用 /vsizip/ 前缀
    std::string gdalPath = fsPath;
    bool isZip = (fsPath.size() >= 4 &&
        (fsPath.substr(fsPath.size() - 4) == ".zip" ||
         fsPath.substr(fsPath.size() - 4) == ".ZIP"));
    if (isZip)
        gdalPath = "/vsizip/" + fsPath;

    GDALDatasetH hDS = GDALOpenEx(gdalPath.c_str(),
        GDAL_OF_VECTOR | GDAL_OF_READONLY, nullptr, nullptr, nullptr);
    if (!hDS)
    {
        std::printf("[GisService] queryGisFile: GDAL cannot open '%s': %s\n",
                    gdalPath.c_str(), CPLGetLastErrorMsg());
        return "{\"error\":\"cannot open file\",\"detail\":\""
               + std::string(CPLGetLastErrorMsg()) + "\"}";
    }

    // 获取驱动名
    GDALDriverH hDriver = GDALGetDatasetDriver(hDS);
    const char* driverName = GDALGetDriverShortName(hDriver);
    std::string format = driverName ? driverName : "unknown";

    // 遍历图层
    int layerCount = GDALDatasetGetLayerCount(hDS);
    std::ostringstream layersJson;
    layersJson << "[";

    int crsEpsg = 0;
    std::string crsName = "unknown";

    for (int i = 0; i < layerCount; i++)
    {
        OGRLayerH hLayer = GDALDatasetGetLayer(hDS, i);
        if (!hLayer) continue;

        const char* name = OGR_L_GetName(hLayer);
        int featureCount = (int)OGR_L_GetFeatureCount(hLayer, FALSE);
        OGRwkbGeometryType geomType = OGR_L_GetGeomType(hLayer);
        const char* geomName = OGRGeometryTypeToName(geomType);

        // 读取第一个图层的 CRS
        if (i == 0)
        {
            OGRSpatialReferenceH hSRS = OGR_L_GetSpatialRef(hLayer);
            if (hSRS)
            {
                const char* code = OSRGetAuthorityCode(hSRS, nullptr);
                if (code) crsEpsg = std::atoi(code);
                const char* authName = OSRGetAuthorityName(hSRS, nullptr);
                if (authName) crsName = authName;
            }
        }

        if (i > 0) layersJson << ",";
        layersJson << "{\"name\":\"" << (name ? name : "")
                   << "\",\"featureCount\":" << featureCount
                   << ",\"geomType\":\"" << (geomName ? geomName : "unknown")
                   << "\"}";
    }
    layersJson << "]";

    GDALClose(hDS);

    // 组装完整 JSON
    std::ostringstream result;
    result << "{\"format\":\"" << format
           << "\",\"sourcePath\":\"" << fsPath
           << "\",\"crs\":{\"epsg\":" << crsEpsg
           << ",\"name\":\"" << crsName
           << "\"},\"layers\":" << layersJson.str() << "}";

    std::printf("[GisService] queryGisFile: %s → %d layers, CRS=%d\n",
                fsPath.c_str(), layerCount, crsEpsg);

    return result.str();
}
```

- [ ] **Step 2: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

Expected: Compiles without errors.

- [ ] **Step 3: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): implement queryGisFile with GDAL layer enumeration"
```

---

## Task 3: Implement importGisFile

**Files:**
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp`

**Context:** `importGisFile` opens a GIS file, iterates selected layers, optionally transforms coordinates via `CrsBridge`, and converts features to DWG entities via `ConvertGISLayerToDWG`. The header `uaodco_crs_bridge.h` provides `CrsBridge::createTransform()` and `uaodco_feature_from_gis.h` provides `uodgdal::ConvertGISLayerToDWG()`.

- [ ] **Step 1: Add importGisFile implementation**

Add after `queryGisFile` in `uaodco_gisservice_impl.cpp`:

```cpp
///////////////////////////////////////////////////////////////////////////
// importGisFile — import selected layers from a GIS file into DWG
///////////////////////////////////////////////////////////////////////////
OdResult UcoGisServiceImpl::importGisFile(
    OdDbDatabase* pDb,
    const std::string& fsPath,
    const std::string& layerNames,
    int targetEpsg)
{
    if (!pDb)
        return eNullObjectPointer;

    ensureGdalInit();

    // ZIP 文件使用 /vsizip/ 前缀
    std::string gdalPath = fsPath;
    bool isZip = (fsPath.size() >= 4 &&
        (fsPath.substr(fsPath.size() - 4) == ".zip" ||
         fsPath.substr(fsPath.size() - 4) == ".ZIP"));
    if (isZip)
        gdalPath = "/vsizip/" + fsPath;

    GDALDatasetH hDS = GDALOpenEx(gdalPath.c_str(),
        GDAL_OF_VECTOR | GDAL_OF_READONLY, nullptr, nullptr, nullptr);
    if (!hDS)
    {
        std::printf("[GisService] importGisFile: cannot open '%s': %s\n",
                    gdalPath.c_str(), CPLGetLastErrorMsg());
        return eInvalidInput;
    }

    // 解析选定的图层名列表 (逗号分隔, 空字符串 = 全部)
    std::vector<std::string> selectedNames;
    if (!layerNames.empty())
    {
        std::istringstream iss(layerNames);
        std::string token;
        while (std::getline(iss, token, ','))
        {
            // 去除首尾空格
            size_t start = token.find_first_not_of(' ');
            size_t end = token.find_last_not_of(' ');
            if (start != std::string::npos)
                selectedNames.push_back(token.substr(start, end - start + 1));
        }
    }

    // 获取 Model Space
    OdDbBlockTablePtr pBT = pDb->getBlockTableId().safeOpenObject();
    OdDbBlockTableRecordPtr pMS =
        pBT->getAt(ACDB_MODEL_SPACE).safeOpenObject(OdDb::kForWrite);

    int totalCount = 0;
    int layerCount = GDALDatasetGetLayerCount(hDS);

    for (int i = 0; i < layerCount; i++)
    {
        OGRLayerH hLayer = GDALDatasetGetLayer(hDS, i);
        if (!hLayer) continue;

        const char* name = OGR_L_GetName(hLayer);
        std::string layerName = name ? name : "";

        // 如果指定了图层列表, 跳过未选中的
        if (!selectedNames.empty())
        {
            bool found = false;
            for (const auto& sel : selectedNames)
            {
                if (sel == layerName) { found = true; break; }
            }
            if (!found) continue;
        }

        // CRS 转换: 如果指定了 targetEpsg 且来源 CRS 不同
        OGRCoordinateTransformation* poCT = nullptr;
        if (targetEpsg > 0)
        {
            OGRSpatialReferenceH hSRS = OGR_L_GetSpatialRef(hLayer);
            if (hSRS)
            {
                const char* code = OSRGetAuthorityCode(hSRS, nullptr);
                int srcEpsg = code ? std::atoi(code) : 0;
                if (srcEpsg > 0 && srcEpsg != targetEpsg)
                    poCT = CrsBridge::createTransform(srcEpsg, targetEpsg);
            }
        }

        // 逐要素转换
        OGRLayer* poLayer = reinterpret_cast<OGRLayer*>(hLayer);
        poLayer->ResetReading();
        OGRFeature* poFeature = nullptr;
        int layerFeatureCount = 0;

        while ((poFeature = poLayer->GetNextFeature()) != nullptr)
        {
            // 坐标转换
            if (poCT)
            {
                OGRGeometry* poGeom = poFeature->GetGeometryRef();
                if (poGeom)
                    poGeom->transform(poCT);
            }

            OdDbObjectId id = uodgdal::ConvertOGRFeatureToDWG(
                pMS, poFeature, layerName.empty() ? "GIS_IMPORT" : layerName);
            if (!id.isNull())
                layerFeatureCount++;

            OGRFeature::DestroyFeature(poFeature);
        }

        if (poCT)
            OGRCoordinateTransformation::DestroyCT(poCT);

        totalCount += layerFeatureCount;
        std::printf("[GisService] importGisFile: layer '%s' → %d features\n",
                    layerName.c_str(), layerFeatureCount);
    }

    GDALClose(hDS);

    std::printf("[GisService] importGisFile: total %d features imported from '%s'\n",
                totalCount, fsPath.c_str());
    return eOk;
}
```

- [ ] **Step 2: Build and verify**

```bash
cd <build_dir> && cmake --build . --target UAOdcadCore
```

- [ ] **Step 3: Commit**

```bash
git add src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): implement importGisFile with CRS transform + layer selection"
```

---

## Task 4: DrawingWeb Commands

**Files:**
- Modify: `E:/ODAGitLab/main24.10/DrawingWeb/GisCommands.h`
- Modify: `E:/ODAGitLab/main24.10/DrawingWeb/GisCommands.cpp`

**Context:** Follow the existing command pattern. Each command class has `name()`, `groupName()`, `globalName()`, `execute()`. Commands read parameters from `OdDbUserIO`, call the `IU_GisService_*` inline wrapper, and fire JS callbacks via `EM_ASM`. Note: use `pDbCmdCtx->database()` (not `.get()`).

- [ ] **Step 1: Add 2 new command classes to GisCommands.h**

Add before the closing `#endif` or at the end of `GisCommands.h`:

```cpp
// 查询GIS文件: 返回图层列表 + CRS 信息
class Cmd_GIS_QUERY_FILE : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};
// 导入GIS文件: 将选定图层转为DWG实体
class Cmd_GIS_IMPORT_FILE : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};
```

- [ ] **Step 2: Implement the 2 commands in GisCommands.cpp**

Add at the end of `GisCommands.cpp`:

```cpp
/////////////////////////////////////////////////////////////////////////
// GIS_QUERY_FILE
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_QUERY_FILE::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_QUERY_FILE::name() { return L"GIS_QUERY_FILE"; }
const OdString Cmd_GIS_QUERY_FILE::globalName() const { return name(); }

void Cmd_GIS_QUERY_FILE::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdString filePath = pIO->getString(L"GIS file path");
    std::string sPath = toUtf8(filePath);

    std::printf("[GIS] GIS_QUERY_FILE: path=%s\n", sPath.c_str());

    std::string json = IU_GisService_queryGisFile(sPath);

    EM_ASM({
        if (typeof window.__onGisFileInfo === 'function')
            window.__onGisFileInfo(UTF8ToString($0));
    }, json.c_str());
}

/////////////////////////////////////////////////////////////////////////
// GIS_IMPORT_FILE
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_IMPORT_FILE::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_IMPORT_FILE::name() { return L"GIS_IMPORT_FILE"; }
const OdString Cmd_GIS_IMPORT_FILE::globalName() const { return name(); }

void Cmd_GIS_IMPORT_FILE::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database();
    OdString filePath = pIO->getString(L"GIS file path");
    OdString layers = pIO->getString(L"Layer names");
    OdString epsgStr = pIO->getString(L"Target EPSG");
    std::string sPath = toUtf8(filePath);
    std::string sLayers = toUtf8(layers);
    int nEpsg = std::atoi(toUtf8(epsgStr).c_str());

    std::printf("[GIS] GIS_IMPORT_FILE: path=%s, layers=%s, epsg=%d\n",
                sPath.c_str(), sLayers.c_str(), nEpsg);

    OdResult res = IU_GisService_importGisFile(pDb, sPath, sLayers, nEpsg);

    // 获取驱动格式名 (从 queryGisFile 的结果中复用)
    std::string formatStr = "unknown";
    std::string queryJson = IU_GisService_queryGisFile(sPath);
    // 简单提取 format 字段
    size_t fmtPos = queryJson.find("\"format\":\"");
    if (fmtPos != std::string::npos)
    {
        fmtPos += 10;
        size_t fmtEnd = queryJson.find("\"", fmtPos);
        if (fmtEnd != std::string::npos)
            formatStr = queryJson.substr(fmtPos, fmtEnd - fmtPos);
    }

    EM_ASM({
        if (typeof window.__onGisImportComplete === 'function')
            window.__onGisImportComplete($0, UTF8ToString($1));
    }, (int)res, formatStr.c_str());
}
```

- [ ] **Step 3: Register the 2 new commands in the command registration section**

Find the file where GIS commands are registered (likely `CadCore.cpp` or a registration function) and add:

```cpp
pCmdStack->addCommand(&m_cmdGisQueryFile);
pCmdStack->addCommand(&m_cmdGisImportFile);
```

With member declarations:

```cpp
Cmd_GIS_QUERY_FILE   m_cmdGisQueryFile;
Cmd_GIS_IMPORT_FILE  m_cmdGisImportFile;
```

Follow the exact pattern used for the existing 6 GIS commands.

- [ ] **Step 4: Commit**

```bash
cd E:/ODAGitLab/main24.10/DrawingWeb
git add GisCommands.h GisCommands.cpp CadCore.cpp
git commit -m "feat(gis): add GIS_QUERY_FILE + GIS_IMPORT_FILE commands"
```

---

## Task 5: Frontend — GisStore Extension

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/stores/GisStore.js`

- [ ] **Step 1: Add sourceInfo state and new actions**

In `GisStore.js`, add after `operationLog = []` (line 18):

```javascript
  // GIS 文件导入来源信息 (用于一键回写)
  sourceInfo = {
    sourcePath: '',
    sourceFormat: '',
    sourceCrs: 0,
    importedLayers: [],
    isGisImport: false,
  }

  // GIS 文件查询结果 (用于 ImportGisModal 展示)
  fileQueryResult = null
```

Add these actions after `clearLog()` (line 81-83):

```javascript
  setSourceInfo(info) {
    this.sourceInfo = { ...this.sourceInfo, ...info, isGisImport: true }
    this.addLog('import', `导入 GIS 文件: ${info.sourceFormat} → DWG`)
  }

  clearSourceInfo() {
    this.sourceInfo = {
      sourcePath: '',
      sourceFormat: '',
      sourceCrs: 0,
      importedLayers: [],
      isGisImport: false,
    }
  }

  setFileQueryResult(result) {
    this.fileQueryResult = result
  }

  clearFileQueryResult() {
    this.fileQueryResult = null
  }

  get canSaveBack() {
    return this.sourceInfo.isGisImport && this.sourceInfo.sourceFormat !== ''
  }
```

- [ ] **Step 2: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
git add src/stores/GisStore.js
git commit -m "feat(gis): add sourceInfo + fileQueryResult to GisStore"
```

---

## Task 6: Frontend — useWasmModule Callbacks

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/hooks/useWasmModule.js`

**Context:** GIS callbacks are at lines 414-429. The `gisStore` is accessible via `rootStore.gisStore`. The hook receives `rootStore` as a parameter.

- [ ] **Step 1: Add __onGisFileInfo and __onGisImportComplete callbacks**

In `useWasmModule.js`, add after the existing `window.__onGisCrsInfo` callback (line 429):

```javascript
      window.__onGisFileInfo = (jsonStr) => {
        console.log('[GIS] 文件信息:', jsonStr)
        try {
          const result = JSON.parse(jsonStr)
          rootStore.gisStore.setFileQueryResult(result)
        } catch (e) {
          console.error('[GIS] 解析文件信息失败:', e)
        }
      }
      window.__onGisImportComplete = (resultCode, formatStr) => {
        console.log('[GIS] 导入完成: result=', resultCode, 'format=', formatStr)
        if (resultCode === 0) {
          rootStore.gisStore.addLog('import', `导入完成: ${formatStr}`)
        } else {
          rootStore.gisStore.addLog('error', `导入失败: code=${resultCode}`)
        }
      }
```

- [ ] **Step 2: Commit**

```bash
git add src/hooks/useWasmModule.js
git commit -m "feat(gis): register __onGisFileInfo + __onGisImportComplete callbacks"
```

---

## Task 7: Frontend — ImportGisModal

**Files:**
- Create: `e:/ODAGitLab/main24.10/DrawingWebApp/src/components/GisService/ImportGisModal.jsx`

**Context:** Follow the `ExportGisModal.jsx` pattern: observer component, Ant Design Modal + Form, viewer.execute for commands. The `fileQueryResult` from GisStore contains `{ format, sourcePath, crs: { epsg, name }, layers: [{ name, featureCount, geomType }] }`.

- [ ] **Step 1: Create ImportGisModal.jsx**

```jsx
import { useState, useEffect } from 'react'
import { Modal, Form, Select, Checkbox, Radio, Typography, message } from 'antd'
import { observer } from 'mobx-react-lite'

const { Text } = Typography

const CRS_OPTIONS = [
  { label: 'EPSG:4490 (CGCS2000)', value: 4490 },
  { label: 'EPSG:4326 (WGS 84)', value: 4326 },
  { label: 'EPSG:4547 (CGCS2000 / 3-degree Zone 39)', value: 4547 },
  { label: 'EPSG:4526 (CGCS2000 / 3-degree Zone 38)', value: 4526 },
  { label: 'EPSG:3857 (Web Mercator)', value: 3857 },
]

const ImportGisModal = observer(function ImportGisModal({ open, onClose, gisStore, viewerRef, hasOpenDwg }) {
  const [selectedLayers, setSelectedLayers] = useState([])
  const [targetEpsg, setTargetEpsg] = useState(0)
  const [importTarget, setImportTarget] = useState('new')

  const queryResult = gisStore.fileQueryResult

  // 当查询结果更新时, 默认选中全部图层 + 设置目标CRS为来源CRS
  useEffect(() => {
    if (queryResult && queryResult.layers) {
      setSelectedLayers(queryResult.layers.map(l => l.name))
      setTargetEpsg(queryResult.crs?.epsg || 0)
      setImportTarget(hasOpenDwg ? 'current' : 'new')
    }
  }, [queryResult, hasOpenDwg])

  const layerOptions = queryResult?.layers?.map(l => ({
    label: `${l.name} (${l.featureCount} 要素, ${l.geomType})`,
    value: l.name,
  })) || []

  // 如果目标CRS在预设列表中不存在, 动态添加
  const crsOptions = [...CRS_OPTIONS]
  const srcEpsg = queryResult?.crs?.epsg || 0
  if (srcEpsg > 0 && !crsOptions.find(o => o.value === srcEpsg)) {
    crsOptions.unshift({ label: `EPSG:${srcEpsg} (来源坐标系)`, value: srcEpsg })
  }

  const handleOk = async () => {
    if (selectedLayers.length === 0) {
      message.warning('请至少选择一个图层')
      return
    }
    if (!viewerRef?.current) return

    // 如果选择新建DWG, 先执行 NEW 命令
    if (importTarget === 'new') {
      await viewerRef.current.execute('NEW')
    }

    const layerStr = selectedLayers.join(',')
    const epsgStr = String(targetEpsg)
    await viewerRef.current.execute('GIS_IMPORT_FILE', [
      queryResult.sourcePath,
      layerStr,
      epsgStr,
    ])

    // 记录来源信息 (用于一键回写)
    gisStore.setSourceInfo({
      sourcePath: queryResult.sourcePath,
      sourceFormat: queryResult.format,
      sourceCrs: srcEpsg,
      importedLayers: selectedLayers,
    })

    message.success(`已导入 ${selectedLayers.length} 个图层`)
    gisStore.clearFileQueryResult()
    onClose()
  }

  const handleCancel = () => {
    gisStore.clearFileQueryResult()
    onClose()
  }

  return (
    <Modal
      title="导入 GIS 数据"
      open={open}
      onOk={handleOk}
      onCancel={handleCancel}
      okText="导入"
      cancelText="取消"
      destroyOnClose
      width={520}
    >
      {queryResult && (
        <Form layout="vertical" style={{ marginTop: 16 }}>
          <Form.Item label="文件信息">
            <Text type="secondary">
              格式: {queryResult.format} &nbsp;|&nbsp;
              坐标系: EPSG:{srcEpsg} ({queryResult.crs?.name || '未知'})
            </Text>
          </Form.Item>

          <Form.Item label="选择图层">
            <Checkbox.Group
              options={layerOptions}
              value={selectedLayers}
              onChange={setSelectedLayers}
            />
          </Form.Item>

          <Form.Item label="目标坐标系">
            <Select
              value={targetEpsg}
              onChange={setTargetEpsg}
              options={crsOptions}
              style={{ width: '100%' }}
            />
          </Form.Item>

          {hasOpenDwg && (
            <Form.Item label="导入到">
              <Radio.Group value={importTarget} onChange={e => setImportTarget(e.target.value)}>
                <Radio value="new">新建 DWG</Radio>
                <Radio value="current">当前 DWG</Radio>
              </Radio.Group>
            </Form.Item>
          )}
        </Form>
      )}
    </Modal>
  )
})

export default ImportGisModal
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/ImportGisModal.jsx
git commit -m "feat(gis): create ImportGisModal with layer selection + CRS confirmation"
```

---

## Task 8: Frontend — TopBar GIS Upload

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/components/TopBar/TopBar.jsx`

**Context:** The TopBar already has a dropdown menu (line 70-82) with a non-functional "导入" item (line 76). The "打开" button (line 106-118) uses a hidden `<input type="file">`. We need to: (1) replace the "导入" menu item with submenu for GIS import, (2) add hidden file inputs for folder and ZIP, (3) add handlers, (4) render ImportGisModal.

- [ ] **Step 1: Add imports and refs**

In `TopBar.jsx`, add to imports (line 0):

```jsx
import { useState } from 'react'
```

Update the `antd` import (line 3) to include `message`:

```jsx
import { Button, Dropdown, Progress, Space, Tooltip, message } from 'antd'
```

Add import for ImportGisModal after the FsViewerPanel import (line 14):

```jsx
import ImportGisModal from '../GisService/ImportGisModal'
```

- [ ] **Step 2: Add state and refs for GIS import**

Inside the `TopBar` component (after line 20), add:

```jsx
  const gisFolderInputRef = useRef(null)
  const gisZipInputRef = useRef(null)
  const [showImportGisModal, setShowImportGisModal] = useState(false)
```

- [ ] **Step 3: Add GIS file upload handlers**

After `handleFileChange` (line 26), add:

```jsx
  const handleGisFolderChange = useCallback((ev) => {
    const files = ev.target.files
    if (!files || files.length === 0) return
    const viewer = viewerRef.current
    if (!viewer) return

    // 清理旧的导入目录
    try { viewer.Module.FS.rmdir('/workspace/gis_import') } catch (e) { /* ignore */ }

    // 创建目录并写入文件
    const dirs = new Set()
    dirs.add('/workspace/gis_import')
    for (const file of files) {
      const fsPath = '/workspace/gis_import/' + file.webkitRelativePath
      const dir = fsPath.substring(0, fsPath.lastIndexOf('/'))
      dirs.add(dir)
    }
    // 逐级创建目录
    for (const dir of [...dirs].sort()) {
      try { viewer.Module.FS.mkdir(dir) } catch (e) { /* exists */ }
    }

    const writePromises = [...files].map(async (file) => {
      const buffer = await file.arrayBuffer()
      const fsPath = '/workspace/gis_import/' + file.webkitRelativePath
      viewer.Module.FS.writeFile(fsPath, new Uint8Array(buffer))
    })

    Promise.all(writePromises).then(() => {
      // 检测 GIS 文件路径: 找 .shp 或 .gdb 文件夹
      let gisPath = '/workspace/gis_import'
      for (const file of files) {
        const rel = file.webkitRelativePath
        if (rel.endsWith('.shp')) {
          gisPath = '/workspace/gis_import/' + rel
          break
        }
        if (rel.includes('.gdb/')) {
          const gdbIdx = rel.indexOf('.gdb/')
          gisPath = '/workspace/gis_import/' + rel.substring(0, gdbIdx + 4)
          break
        }
      }
      viewer.execute('GIS_QUERY_FILE', [gisPath])
      setShowImportGisModal(true)
    })

    ev.target.value = ''
  }, [viewerRef])

  const handleGisZipChange = useCallback((ev) => {
    const file = ev.target.files[0]
    if (!file || !viewerRef.current) return
    const viewer = viewerRef.current

    file.arrayBuffer().then((buffer) => {
      const fsPath = '/workspace/gis_import/' + file.name
      try { viewer.Module.FS.mkdir('/workspace/gis_import') } catch (e) { /* exists */ }
      try { viewer.Module.FS.unlink(fsPath) } catch (e) { /* not exists */ }
      viewer.Module.FS.writeFile(fsPath, new Uint8Array(buffer))

      viewer.execute('GIS_QUERY_FILE', [fsPath])
      setShowImportGisModal(true)
    })

    ev.target.value = ''
  }, [viewerRef])
```

- [ ] **Step 4: Update menu items to add GIS import submenu**

Replace the "导入" menu item (line 76) with:

```jsx
    {
      key: '导入', label: '导入', icon: <ImportOutlined />,
      children: [
        { key: '导入GIS文件夹', label: '导入 GIS 文件夹 (Shapefile/GDB)' },
        { key: '导入GIS压缩包', label: '导入 GIS 压缩包 (.zip)' },
      ],
    },
```

- [ ] **Step 5: Update handleMenuClick to handle GIS import actions**

Replace `handleMenuClick` (line 84-86) with:

```jsx
  const handleMenuClick = useCallback(({ key }) => {
    if (key === '导入GIS文件夹') {
      gisFolderInputRef.current?.click()
    } else if (key === '导入GIS压缩包') {
      gisZipInputRef.current?.click()
    } else {
      handleMenuAction(key)
    }
  }, [handleMenuAction])
```

- [ ] **Step 6: Add hidden file inputs and ImportGisModal in JSX**

After the existing hidden file input (line 119-124), add:

```jsx
            <input
              ref={gisFolderInputRef}
              type="file"
              webkitdirectory=""
              directory=""
              style={{ display: 'none' }}
              onChange={handleGisFolderChange}
            />
            <input
              ref={gisZipInputRef}
              type="file"
              accept=".zip"
              style={{ display: 'none' }}
              onChange={handleGisZipChange}
            />
```

At the end of the component, before the final closing `</div>` and after all other JSX, add:

```jsx
      <ImportGisModal
        open={showImportGisModal}
        onClose={() => setShowImportGisModal(false)}
        gisStore={rootStore.gisStore}
        viewerRef={viewerRef}
        hasOpenDwg={editorStore.hasOpenFile}
      />
```

- [ ] **Step 7: Commit**

```bash
git add src/components/TopBar/TopBar.jsx
git commit -m "feat(gis): add GIS folder/ZIP import entries to TopBar dropdown"
```

---

## Task 9: Frontend — ViewerService Save-Back + fflate Download

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/package.json`
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/services/ViewerService.js`

- [ ] **Step 1: Install fflate**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp && npm install fflate
```

- [ ] **Step 2: Add handleGisSaveBack method to ViewerService**

In `ViewerService.js`, inside the `Viewer` class (find a good location near `handleOpenDwgFile`), add:

```javascript
    async handleGisSaveBack(sourceInfo) {
      if (!sourceInfo || !sourceInfo.isGisImport) return

      const { sourceFormat, sourcePath } = sourceInfo

      // 映射 GDAL 驱动名 → 导出格式参数 + 文件扩展名
      const FORMAT_MAP = {
        'ESRI Shapefile': { format: 'ESRI Shapefile', ext: '.shp', multi: true },
        'OpenFileGDB': { format: 'FileGDB', ext: '.gdb', multi: true },
        'GeoJSON': { format: 'GeoJSON', ext: '.geojson', multi: false },
        'GPKG': { format: 'GPKG', ext: '.gpkg', multi: false },
      }

      const fmtInfo = FORMAT_MAP[sourceFormat] || FORMAT_MAP['GeoJSON']
      const exportDir = '/tmp/gis_export'
      const baseName = 'export' + fmtInfo.ext
      const exportPath = exportDir + '/' + baseName

      // 清理并创建导出目录
      try { this.Module.FS.rmdir(exportDir) } catch (e) { /* ignore */ }
      try { this.Module.FS.mkdir(exportDir) } catch (e) { /* exists */ }

      // 执行导出
      await this.execute('GIS_EXPORT', [fmtInfo.format, exportPath])

      // 读取导出结果
      let entries
      try {
        entries = this.Module.FS.readdir(exportDir).filter(n => n !== '.' && n !== '..')
      } catch (e) {
        console.error('[GIS] 读取导出目录失败:', e)
        return
      }

      if (entries.length === 0) {
        console.error('[GIS] 导出目录为空')
        return
      }

      if (fmtInfo.multi || entries.length > 1) {
        // 多文件格式: 用 fflate 打包为 ZIP
        const { zipSync } = await import('fflate')
        const zipData = {}
        for (const name of entries) {
          const data = this.Module.FS.readFile(exportDir + '/' + name)
          zipData[name] = data
        }
        const zipped = zipSync(zipData)
        const blob = new Blob([zipped], { type: 'application/zip' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'export.zip'
        a.click()
        URL.revokeObjectURL(url)
      } else {
        // 单文件: 直接下载
        const fileName = entries[0]
        const data = this.Module.FS.readFile(exportDir + '/' + fileName)
        const blob = new Blob([data])
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = fileName
        a.click()
        URL.revokeObjectURL(url)
      }
    }
```

- [ ] **Step 3: Bind the method in the Viewer constructor**

Find the constructor binding section (near line 431) and add:

```javascript
      this.handleGisSaveBack = this.handleGisSaveBack.bind(this)
```

- [ ] **Step 4: Commit**

```bash
git add package.json package-lock.json src/services/ViewerService.js
git commit -m "feat(gis): add handleGisSaveBack with fflate ZIP download"
```

---

## Self-Review Checklist

### Spec Coverage

| Spec Requirement | Task |
|-----------------|------|
| IUcoGisService extension (queryGisFile + importGisFile) | Task 1 |
| queryGisFile: GDAL format detection, layer enum, CRS | Task 2 |
| importGisFile: layer selection, CRS transform, /vsizip/ | Task 3 |
| GIS_QUERY_FILE + GIS_IMPORT_FILE commands | Task 4 |
| GisStore sourceInfo + saveBackToGis state | Task 5 |
| useWasmModule new callbacks | Task 6 |
| ImportGisModal (layer selection + CRS + import target) | Task 7 |
| TopBar dropdown with GIS folder/ZIP upload | Task 8 |
| fflate + save-back download flow | Task 9 |

### Type Consistency Check

- `queryGisFile(const std::string& fsPath)` → consistent across interface, impl, and inline wrapper
- `importGisFile(OdDbDatabase* pDb, const std::string& fsPath, const std::string& layerNames, int targetEpsg)` → consistent across interface, impl, inline wrapper, and GIS_IMPORT_FILE command
- `gisStore.fileQueryResult` → set in useWasmModule callback, read in ImportGisModal, cleared on close
- `gisStore.sourceInfo` → set after import in ImportGisModal, read in handleGisSaveBack
- `window.__onGisFileInfo(jsonStr)` → registered in useWasmModule, called in GIS_QUERY_FILE C++ command
- `window.__onGisImportComplete(resultCode, formatStr)` → registered in useWasmModule, called in GIS_IMPORT_FILE C++ command
