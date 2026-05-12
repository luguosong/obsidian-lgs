# GIS File Import / Save-Back Design

## Goal

Allow DrawingWebApp users to open GIS files (Shapefile folder, File GDB folder, or ZIP archive) directly in the browser, convert them to DWG for editing, and save back to the original GIS format — all client-side via WASM, no server involvement.

## Architecture

Extend the existing `IUcoGisService` C++ interface with two new methods (`queryGisFile` and `importGisFile`). GDAL handles format detection, ZIP reading (via `/vsizip/`), layer enumeration, and geometry conversion. The frontend provides a layer-selection + CRS-confirmation modal, tracks source metadata in MobX state, and offers one-click save-back with browser download.

## Tech Stack

- C++11 (ODA SDK 24.10) + GDAL 3.4.2 + PROJ (Emscripten WASM)
- React 19 + Ant Design + MobX (DrawingWebApp frontend)
- `fflate` (~8KB) for JS-side ZIP packaging on download

---

## User Flow

### Import Flow

```
TopBar [打开 ▾] → "导入GIS文件夹" 或 "导入GIS压缩包"
  → 浏览器文件选择器 (webkitdirectory / accept=".zip")
    → JS writes files to Emscripten FS: /workspace/gis_import/...
      → viewer.execute("GIS_QUERY_FILE", fsPath)
        → C++ GDAL opens file → returns layer list + CRS as JSON
          → __onGisFileInfo(json) callback
            → ImportGisModal opens:
              - Shows layer list with checkboxes
              - Shows detected CRS, allows target CRS selection
              - "New DWG" / "Current DWG" radio (if DWG is open)
            → User clicks "导入"
              → viewer.execute("GIS_IMPORT_FILE", path, layers, epsg)
                → C++ imports selected layers as DWG entities
                  → __onGisImportComplete(count, format) callback
                    → GisStore records sourceInfo
                    → View refreshes
```

### Save-Back Flow

```
User clicks "保存为GIS" button
  → GisStore.saveBackToGis()
    → viewer.execute("GIS_EXPORT", sourceFormat, "/tmp/gis_export/output")
      → C++ exports DWG → GIS files in Emscripten FS
        → __onGisSyncComplete callback
          → JS reads files from FS via Module.FS.readFile()
            → fflate creates ZIP (for Shapefile/GDB multi-file formats)
              → Browser triggers download
```

---

## C++ Interface Extension

### IUcoGisService — 2 new methods

```cpp
// Query a GIS file: returns JSON with format, layers, CRS info
virtual std::string queryGisFile(const std::string& fsPath) = 0;

// Import selected layers from a GIS file into a DWG database
// pDb = nullptr → create new empty DWG
// layerNames = "" → import all layers
// targetEpsg = 0 → no CRS transformation
virtual OdResult importGisFile(
    OdDbDatabase* pDb,
    const std::string& fsPath,
    const std::string& layerNames,
    int targetEpsg) = 0;
```

### Inline wrappers (same pattern as existing)

```cpp
inline std::string IU_GisService_queryGisFile(const std::string& path) { ... }
inline OdResult IU_GisService_importGisFile(OdDbDatabase* pDb, ...) { ... }
```

### queryGisFile return JSON

```json
{
  "format": "ESRI Shapefile",
  "sourcePath": "/workspace/gis_import/mydata.zip",
  "crs": {
    "epsg": 4490,
    "name": "CGCS2000"
  },
  "layers": [
    {
      "name": "roads",
      "featureCount": 1523,
      "geomType": "LineString"
    },
    {
      "name": "buildings",
      "featureCount": 456,
      "geomType": "Polygon"
    }
  ]
}
```

### importGisFile implementation outline

1. Detect ZIP: if `fsPath` ends with `.zip`, prepend `/vsizip/`
2. `GDALOpenEx(path, GDAL_OF_VECTOR | GDAL_OF_READONLY)`
3. Parse `layerNames` (comma-separated) to determine which layers to import
4. For each selected layer:
   a. Read source SRS from the layer
   b. If `targetEpsg != 0` and differs from source, create `OGRCoordinateTransformation` via `CrsBridge::createTransform()`
   c. Iterate features, transform coordinates if needed
   d. Call `ConvertGISLayerToDWG()` (from `uaodco_feature_from_gis`) to create DWG entities
5. Return `eOk` with total feature count via callback

### queryGisFile implementation outline

1. Detect ZIP → `/vsizip/` prefix
2. `GDALOpenEx(path, GDAL_OF_VECTOR | GDAL_OF_READONLY)`
3. Get driver name → `"format"` field
4. For each layer:
   - `OGR_L_GetName()` → name
   - `OGR_L_GetFeatureCount()` → count
   - `OGR_L_GetGeomType()` → geometry type string
5. Read SRS from first layer → `exportToProj4` / `GetAuthorityCode` → EPSG
6. Build JSON string, return

---

## DrawingWeb Commands

### New commands in GisCommands.h / GisCommands.cpp

| Command | Parameters (from UserIO) | JS Callback |
|---------|--------------------------|-------------|
| `GIS_QUERY_FILE` | `filePath` | `window.__onGisFileInfo(jsonStr)` |
| `GIS_IMPORT_FILE` | `filePath`, `layerNames`, `targetEpsg` | `window.__onGisImportComplete(count, formatStr)` |

Both commands follow the existing pattern: read parameters from `OdDbUserIO`, call `IUcoGisService` inline wrapper, report result via `EM_ASM`.

`GIS_IMPORT_FILE` handles the "no database" case: if user selects "New DWG", the frontend first calls `viewer.execute("NEW")` to create a blank DWG (using the existing NEW command), then calls `GIS_IMPORT_FILE` on the newly created database. This avoids creating a detached database in C++ and reuses the viewer's existing file lifecycle.

---

## Frontend Components

### TopBar.jsx — Modified

Expand the existing "打开" button into a dropdown menu:

```
[打开 ▾]
  ├── 打开DWG文件        (existing, unchanged)
  ├── 导入GIS文件夹      (webkitdirectory folder picker)
  └── 导入GIS压缩包      (accept=".zip" file picker)
```

GIS upload handler:
1. Write uploaded files to Emscripten FS at `/workspace/gis_import/<name>/`
2. Determine the GDAL-accessible path:
   - Folder upload: find the `.shp` file or `.gdb` folder within
   - ZIP upload: use the `.zip` file path directly
3. Call `viewer.execute("GIS_QUERY_FILE", fsPath)`

### ImportGisModal.jsx — New

Ant Design Modal with:
- File name and detected format display
- Layer list with checkboxes (default: all checked)
  - Each row shows: layer name, feature count, geometry type
- Source CRS display (auto-detected, read-only)
- Target CRS selector (Ant Design Select, default = source CRS)
  - Common options: EPSG:4490, EPSG:4326, EPSG:4547, EPSG:3857
- "Import to" radio group: "New DWG" / "Current DWG" (only when DWG is open)
- Cancel / Import buttons

### GisStore — Extended

New observable state:

```javascript
sourceInfo = {
  sourcePath: '',      // Emscripten FS path
  sourceFormat: '',    // GDAL driver name (e.g., "ESRI Shapefile")
  sourceCrs: 0,        // EPSG code
  importedLayers: [],  // layer names that were imported
  isGisImport: false   // whether current DWG originated from GIS import
}
```

New actions:
- `setSourceInfo(info)` — called after successful import
- `clearSourceInfo()` — called when DWG is closed
- `saveBackToGis()` — triggers export + download flow

Computed:
- `canSaveBack` — true if `isGisImport && sourceFormat !== ''`

### useWasmModule.js — Modified

Register two new callbacks:

```javascript
window.__onGisFileInfo = (jsonStr) => { ... }
window.__onGisImportComplete = (count, formatStr) => { ... }
```

### ViewerService.js — Modified

New methods:

```javascript
handleOpenGisFolder(fileList)   // processes folder FileList → FS write → GIS_QUERY_FILE
handleOpenGisZip(file)          // processes ZIP File → FS write → GIS_QUERY_FILE
handleGisSaveBack(sourceInfo)   // GIS_EXPORT → FS read → fflate ZIP → download
```

### package.json — Modified

Add dependency: `fflate` (for ZIP creation on download).

---

## File Upload → Emscripten FS Mapping

| Upload Type | JS Processing | FS Target Path | GDAL Open Path |
|-------------|---------------|----------------|-----------------|
| Shapefile folder | Iterate FileList, `FS.writeFile` each | `/workspace/gis_import/<folder>/` | `/workspace/gis_import/<folder>/<name>.shp` |
| GDB folder | Iterate FileList, `FS.writeFile` each | `/workspace/gis_import/<name>.gdb/` | `/workspace/gis_import/<name>.gdb` |
| ZIP file | Single `FS.writeFile` | `/workspace/gis_import/<name>.zip` | `/vsizip//workspace/gis_import/<name>.zip` |

**ZIP path note:** GDAL's `/vsizip/` prefix uses double slash: `/vsizip//absolute/path/to/file.zip`. If the ZIP contains a subdirectory (e.g., `data/roads.shp`), GDAL can auto-detect the first layer, or we scan with `GDALOpenEx` which handles this transparently.

**Cleanup:** Files in `/workspace/gis_import/` persist until the user imports a new GIS file or closes the page. On new import, the old `/workspace/gis_import/` is removed first.

---

## Save-Back Download Strategy

| Source Format | Export produces | Download format |
|---------------|-----------------|-----------------|
| ESRI Shapefile | .shp + .dbf + .prj + .shx | ZIP archive |
| OpenFileGDB | .gdb/ folder (multiple files) | ZIP archive |
| GeoJSON | single .geojson file | Direct file download |
| GeoPackage | single .gpkg file | Direct file download |

JS-side flow:
1. `GIS_EXPORT` writes to `/tmp/gis_export/` in Emscripten FS
2. JS lists files in the export directory via `Module.FS.readdir()`
3. If single file → `Blob` → `URL.createObjectURL` → `<a download>` click
4. If multiple files → `fflate.zipSync()` → `Blob` → download

---

## Scope Exclusions

- **Server-side processing:** All conversion happens client-side in WASM
- **Raster GIS import:** Only vector data (Shapefile/GDB/GeoJSON/GeoPackage); raster basemaps use the existing `GIS_LOAD_MAP_IMAGE` command
- **Streaming/pagination:** No support for very large GIS files that exceed browser memory; suitable for typical project-scale data (< 100MB)
- **Edit tracking:** No per-feature change tracking for selective push-back; save-back exports the entire DWG content

---

## File Change Summary

### UAOdcadCore (C++ GIS engine)

| Action | File | Change |
|--------|------|--------|
| Modify | `include/uaodcadcore/gdal/uaodco_igisservice.h` | Add `queryGisFile()` + `importGisFile()` virtual methods and inline wrappers |
| Modify | `src/uaodcadcore/gdal/uaodco_gisservice_impl.h` | Add 2 override declarations |
| Modify | `src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp` | Implement `queryGisFile()` + `importGisFile()` |

### DrawingWeb (WASM command layer)

| Action | File | Change |
|--------|------|--------|
| Modify | `GisCommands.h` | Add `Cmd_GIS_QUERY_FILE` + `Cmd_GIS_IMPORT_FILE` classes |
| Modify | `GisCommands.cpp` | Implement 2 new command execute() methods |

### DrawingWebApp (React frontend)

| Action | File | Change |
|--------|------|--------|
| Modify | `src/components/TopBar/TopBar.jsx` | Open button → dropdown menu with GIS upload entries |
| Create | `src/components/GisService/ImportGisModal.jsx` | Layer selection + CRS confirmation modal |
| Modify | `src/stores/GisStore.js` | Add `sourceInfo` state + `saveBackToGis()` action |
| Modify | `src/hooks/useWasmModule.js` | Register `__onGisFileInfo` + `__onGisImportComplete` callbacks |
| Modify | `src/services/ViewerService.js` | Add `handleOpenGisFolder()` + `handleOpenGisZip()` + `handleGisSaveBack()` |
| Modify | `package.json` | Add `fflate` dependency |
