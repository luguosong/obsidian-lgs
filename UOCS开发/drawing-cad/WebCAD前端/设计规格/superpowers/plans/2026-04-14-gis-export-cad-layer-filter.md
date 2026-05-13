# DWG 导出 GIS 按 CAD 图层过滤 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use [[superpower]]s:subagent-driven-development (recommended) or [[superpower]]s:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让用户在"导出 GIS"对话框中勾选具体 CAD 图层，只导出所选图层的实体。

**Architecture:** 在 C++ 转换核心 `ConvertDWGToGIS` 增加可选的 `dwgLayerFilter`（逗号分隔图层名）参数；通过 `IUcoGisService` 接口 → WASM 命令 `Cmd_GIS_EXPORT` 一路透传。前端 `ExportGisModal` 改为从 `viewer.getLayersWithInfo()` 读取当前 DWG 的 CAD 图层，Checkbox 列表渲染图层名及 可见/冻结/锁定 状态图标，默认勾选 `on && !frozen` 的图层。

**Tech Stack:** C++17 / ODA SDK / GDAL / Emscripten；React 19 / Ant Design / MobX。

**Spec:** [docs/superpowers/specs/2026-04-14-gis-export-cad-layer-filter-design.md](../specs/2026-04-14-gis-export-cad-layer-filter-design.md)

**关于测试：** 本仓库此区域无自动化测试基础设施（WASM 需 Emscripten 重建，前端无 Jest 配置）。计划采用"改动 → 构建 → 手工端到端验证"的节奏；每个 Task 结束即提交。

---

## 文件结构

本次改动涉及 4 处代码仓（3 处 C++、1 处前端）：

| 文件 | 动作 | 职责 |
|-----|-----|------|
| `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/gdal/uaodco_converttogis.h` | 修改 | `ConvertDWGToGIS` 声明新增 `dwgLayerFilter` |
| `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_converttogis.cpp` | 修改 | 实现过滤逻辑 |
| `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/gdal/uaodco_igisservice.h` | 修改 | `IUcoGisService::exportToGis` 虚函数签名 + `IU_GisService_exportToGis` 封装 |
| `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.h` | 修改 | 匹配新签名 |
| `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp` | 修改 | 转调 `ConvertDWGToGIS` 传递 filter |
| `e:/ODAGitLab/main24.10/DrawingWeb/GisCommands.cpp` | 修改 | `Cmd_GIS_EXPORT::execute` 读取第 3 参 |
| `e:/ODAGitLab/main24.10/DrawingWebApp/src/services/ViewerService.js` | 修改 | `handleGisSaveBack` 显式传 `""` 保持兼容 |
| `e:/ODAGitLab/main24.10/DrawingWebApp/src/components/GisService/ExportGisModal.jsx` | 修改 | 列表改为 CAD 图层 + 状态图标 |

---

## Task 1: C++ 核心 —— `ConvertDWGToGIS` 支持图层过滤

**Files:**
- Modify: `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/gdal/uaodco_converttogis.h:21`
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_converttogis.cpp:647-716`

- [ ] **Step 1: 扩展 `ConvertDWGToGIS` 声明**

编辑 `uaodco_converttogis.h` 第 21 行附近：

```cpp
UAODCORE_API bool ConvertDWGToGIS(
    OdDbDatabase* poDb,
    const char* pszOutputFile,
    const char* pszFormat = "ESRI Shapefile",
    int iEPSGCode = 0,
    const std::string& dwgLayerFilter = "");
```

同时确保文件顶部已 `#include <string>`、`#include <set>`（如缺则补）。

- [ ] **Step 2: 修改 `ConvertDWGToGIS` 实现，在入口解析过滤集**

编辑 `uaodco_converttogis.cpp` 第 647 行的函数定义：

```cpp
bool ConvertDWGToGIS(OdDbDatabase* poDb, const char* pszOutputFile,
                     const char* pszFormat, int iEPSGCode,
                     const std::string& dwgLayerFilter)
{
    if (poDb == 0)
        return false;

    // 解析过滤集（空 = 不过滤）
    std::set<std::string> filterSet;
    if (!dwgLayerFilter.empty())
    {
        size_t start = 0;
        while (start < dwgLayerFilter.size())
        {
            size_t comma = dwgLayerFilter.find(',', start);
            std::string token = dwgLayerFilter.substr(
                start, (comma == std::string::npos ? dwgLayerFilter.size() : comma) - start);
            size_t l = token.find_first_not_of(" \t");
            size_t r = token.find_last_not_of(" \t");
            if (l != std::string::npos)
                filterSet.insert(token.substr(l, r - l + 1));
            if (comma == std::string::npos) break;
            start = comma + 1;
        }
    }

    // 1. 初始化 GDAL
    GDALAllRegister();
    // ... 余下现有代码不变，直到 ModelSpace 遍历循环 ...
```

- [ ] **Step 3: 在 ModelSpace 遍历循环中增加过滤判断**

定位到原第 706-716 行的循环（`for (poEntIter->start(); !poEntIter->done(); ...)`），在 `OdString osLayerName = poEntity->layer();` **之后**、`oLayerEntities[sLayerName].push_back(...)` **之前**增加：

```cpp
OdString osLayerName = poEntity->layer();
std::string sLayerName = (const char*)osLayerName;

// 图层过滤
if (!filterSet.empty() && filterSet.find(sLayerName) == filterSet.end())
    continue;

oLayerEntities[sLayerName].push_back(poEntIter->objectId());
```

- [ ] **Step 4: 构建 uaodcadcore 验证编译**

在 uaodcadcore 工程的 CMake 构建目录运行（具体命令取决于环境，示例）：

```bash
cmake --build out/build --target uaodcadcore --config Debug
```

Expected: 编译通过，无 warning。

- [ ] **Step 5: Commit**

```bash
cd E:/updasdk/WorkSpace/uadrawing
git add include/uaodcadcore/gdal/uaodco_converttogis.h src/uaodcadcore/gdal/uaodco_converttogis.cpp
git commit -m "feat(gis): ConvertDWGToGIS support CAD layer filter"
```

---

## Task 2: 服务层 —— `IUcoGisService::exportToGis` 扩展签名

**Files:**
- Modify: `E:/updasdk/WorkSpace/uadrawing/include/uaodcadcore/gdal/uaodco_igisservice.h:41-49, 94-101`
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.h:16`
- Modify: `E:/updasdk/WorkSpace/uadrawing/src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp:354-366`

- [ ] **Step 1: 扩展接口虚函数**

编辑 `uaodco_igisservice.h` 第 41 行附近：

```cpp
virtual bool exportToGis(
    OdDbDatabase* pDb,
    const std::string& outputPath,
    const std::string& format,
    int epsgCode = 0,
    const std::string& dwgLayerFilter = "") = 0;
```

- [ ] **Step 2: 扩展 inline 封装**

编辑同文件第 94-101 行 `IU_GisService_exportToGis`：

```cpp
inline bool IU_GisService_exportToGis(
    OdDbDatabase* pDb, const std::string& path,
    const std::string& fmt = "ESRI Shapefile",
    int epsg = 0,
    const std::string& dwgLayerFilter = "")
{
    IUcoGisService* p = IUcoGisService::GetInstance();
    if (!p) return false;
    return p->exportToGis(pDb, path, fmt, epsg, dwgLayerFilter);
}
```

- [ ] **Step 3: 更新实现类声明**

编辑 `uaodco_gisservice_impl.h` 第 16 行：

```cpp
bool exportToGis(OdDbDatabase* pDb, const std::string& outputPath,
                 const std::string& format, int epsgCode,
                 const std::string& dwgLayerFilter) override;
```

- [ ] **Step 4: 更新实现定义，传递 filter**

编辑 `uaodco_gisservice_impl.cpp` 第 354-366 行：

```cpp
bool UcoGisServiceImpl::exportToGis(
    OdDbDatabase* pDb,
    const std::string& outputPath,
    const std::string& format,
    int epsgCode,
    const std::string& dwgLayerFilter)
{
    if (!pDb)
        return false;

    ensureGdalInit();

    return uodgdal::ConvertDWGToGIS(
        pDb, outputPath.c_str(), format.c_str(), epsgCode, dwgLayerFilter);
}
```

- [ ] **Step 5: 确认内部 pushFeatures 调用向后兼容**

查看 `uaodco_gisservice_impl.cpp` 第 321 行 `pushFeatures` 内调用：
```cpp
bool ok = uodgdal::ConvertDWGToGIS(pDb, vsimemPath, "GeoJSON", 0);
```
此调用依赖默认参数 `dwgLayerFilter = ""`，**无需改动**，验证编译通过即可。

- [ ] **Step 6: 构建验证**

```bash
cmake --build out/build --target uaodcadcore --config Debug
```

Expected: 编译通过。

- [ ] **Step 7: Commit**

```bash
cd E:/updasdk/WorkSpace/uadrawing
git add include/uaodcadcore/gdal/uaodco_igisservice.h \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.h \
        src/uaodcadcore/gdal/uaodco_gisservice_impl.cpp
git commit -m "feat(gis): IUcoGisService::exportToGis support layer filter"
```

---

## Task 3: WASM 命令 —— `Cmd_GIS_EXPORT` 读取第 3 参数

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWeb/GisCommands.cpp:249-267`

- [ ] **Step 1: 修改 `Cmd_GIS_EXPORT::execute`，新增第 3 个参数读取**

编辑 `DrawingWeb/GisCommands.cpp` 第 249-267 行：

```cpp
void Cmd_GIS_EXPORT::execute(OdEdCommandContext* pCmdCtx)
{
    OdDbCommandContextPtr pDbCmdCtx(pCmdCtx);
    OdDbUserIO* pIO = pDbCmdCtx->dbUserIO();
    OdDbDatabase* pDb = pDbCmdCtx->database();
    OdString format      = pIO->getString(L"Export format");
    OdString path        = pIO->getString(L"Export path");
    OdString layerFilter = pIO->getString(L"Layer filter (comma-separated, empty = all)");
    std::string sFormat = toUtf8(format);
    std::string sPath   = toUtf8(path);
    std::string sFilter = toUtf8(layerFilter);

    std::printf("[GIS] GIS_EXPORT: format=%s, path=%s, filter=%s\n",
                sFormat.c_str(), sPath.c_str(), sFilter.c_str());

    bool ok = IU_GisService_exportToGis(pDb, sPath, sFormat, 0, sFilter);

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "export", ok ? 0 : 1);
}
```

- [ ] **Step 2: 重建 WASM 模块**

按本仓 `CLAUDE.md` 指引重建 DrawingJs：

```bash
# 具体命令依赖 Emscripten 环境的配置，参考 DrawingWeb 构建脚本
cd e:/ODAGitLab/main24.10/DrawingWeb
# 示例：
#   emcmake cmake -S . -B build-wasm
#   cmake --build build-wasm --config Release
```

将产物 `DrawingJs.{js,wasm,data}` 更新到 `DrawingWebApp/public/`（若使用符号链接/构建脚本则自动完成）。

Expected: 产物正确生成并可被前端加载。

- [ ] **Step 3: Commit DrawingWeb 源码改动**

```bash
cd e:/ODAGitLab/main24.10/DrawingWeb
git add GisCommands.cpp
git commit -m "feat(gis): Cmd_GIS_EXPORT accept layer filter argument"
```

（WASM 产物的提交按本仓现有规范处理 —— 如果 `DrawingJs.*` 由 CI 生成则无需提交，否则在 DrawingWebApp 侧提交更新后的 `public/DrawingJs.*`。）

---

## Task 4: 更新 `ViewerService.js` 的 `handleGisSaveBack` 调用

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/services/ViewerService.js:1215`

**原因：** `handleGisSaveBack` 目前只传两个参数给 `GIS_EXPORT`。新命令会等待第三个 `getString`，导致命令挂起。必须显式补传空串。

- [ ] **Step 1: 改动调用处**

将第 1215 行：
```javascript
await this.execute('GIS_EXPORT', [fmtInfo.format, exportPath])
```
改为：
```javascript
await this.execute('GIS_EXPORT', [fmtInfo.format, exportPath, ''])
```

- [ ] **Step 2: Lint**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
npm run lint
```

Expected: 无新增 lint 错误。

- [ ] **Step 3: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
git add src/services/ViewerService.js
git commit -m "fix(gis): pass empty layer filter to GIS_EXPORT in save-back"
```

---

## Task 5: 重写 `ExportGisModal` 使用 CAD 图层列表

**Files:**
- Modify: `e:/ODAGitLab/main24.10/DrawingWebApp/src/components/GisService/ExportGisModal.jsx`

- [ ] **Step 1: 用 frontend-design skill 设计新 UI**

根据用户记忆的偏好，修改前端页面时调用 `frontend-design` skill，确认列表 UI 与 Ant Design 风格一致、状态图标视觉协调。产出后再回到本 Task 实施代码。

- [ ] **Step 2: 替换 imports 与状态**

修改文件顶部（替换第 1-4 行）：

```jsx
/* global FS */
import { useState, useEffect, useCallback } from 'react'
import { Modal, Form, Select, Checkbox, message, Tooltip } from 'antd'
import {
  EyeOutlined,
  EyeInvisibleOutlined,
  LockOutlined,
  UnlockOutlined,
} from '@ant-design/icons'
import { observer } from 'mobx-react-lite'
```

添加 LayerManagerDialog 同款雪花图标（在 `const FORMAT_OPTIONS` 之前）：

```jsx
const SnowflakeIcon = ({ size = 14 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
       stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="2" x2="12" y2="22" />
    <line x1="2" y1="12" x2="22" y2="12" />
    <line x1="5" y1="5" x2="19" y2="19" />
    <line x1="19" y1="5" x2="5" y2="19" />
  </svg>
)
```

- [ ] **Step 3: 在组件中新增 CAD 图层 state 与加载逻辑**

在 `const ExportGisModal = observer(function ExportGisModal({ open, onClose, gisStore, viewerRef })` 函数体开头（原第 62-64 行）修改为：

```jsx
const [format, setFormat] = useState('GPKG')
const [cadLayers, setCadLayers] = useState([])
const [selectedCadLayers, setSelectedCadLayers] = useState([])
const [exporting, setExporting] = useState(false)

useEffect(() => {
  if (!open || !viewerRef?.current) return
  try {
    const list = viewerRef.current.getLayersWithInfo() || []
    setCadLayers(list)
    // 默认勾选：可见 && 未冻结
    setSelectedCadLayers(list.filter(l => l.on && !l.frozen).map(l => l.name))
  } catch (e) {
    console.warn('[GIS] getLayersWithInfo failed:', e)
    setCadLayers([])
    setSelectedCadLayers([])
  }
}, [open, viewerRef])
```

删除原有基于 `gisStore.featureLayers` 的 `layerOptions` 计算（原第 66-69 行）。

- [ ] **Step 4: 修改 `handleOk` 的 filter 传参逻辑**

将原第 85 行：
```jsx
const layers = selectedLayers.length ? selectedLayers.join(',') : 'all'
viewerRef.current.execute('GIS_EXPORT', [format, exportPath, layers])
```

改为：

```jsx
// "全选"或"完全不选"两种极端情况都传空串，语义 = 全部导出
const allSelected = selectedCadLayers.length === 0
  || selectedCadLayers.length === cadLayers.length
const layerFilter = allSelected ? '' : selectedCadLayers.join(',')
viewerRef.current.execute('GIS_EXPORT', [format, exportPath, layerFilter])
```

- [ ] **Step 5: 用自定义 Checkbox 列表替换原 `Checkbox.Group`**

删除原第 134-139 行的 `Form.Item`（`layerOptions.length > 0 && ...`），替换为：

```jsx
{cadLayers.length > 0 && (
  <Form.Item label="选择要导出的 CAD 图层（全选或全不选均导出全部）">
    <div style={{
      maxHeight: 240, overflowY: 'auto',
      border: '1px solid #424242', borderRadius: 4, padding: 8,
    }}>
      <div style={{ marginBottom: 8, paddingBottom: 8, borderBottom: '1px solid #303030' }}>
        <Checkbox
          disabled={exporting}
          checked={selectedCadLayers.length === cadLayers.length && cadLayers.length > 0}
          indeterminate={selectedCadLayers.length > 0 && selectedCadLayers.length < cadLayers.length}
          onChange={e => setSelectedCadLayers(
            e.target.checked ? cadLayers.map(l => l.name) : []
          )}
        >
          全选 ({selectedCadLayers.length}/{cadLayers.length})
        </Checkbox>
      </div>
      {cadLayers.map(layer => (
        <div key={layer.name} style={{
          display: 'flex', alignItems: 'center', padding: '4px 0',
        }}>
          <Checkbox
            disabled={exporting}
            checked={selectedCadLayers.includes(layer.name)}
            onChange={e => setSelectedCadLayers(prev =>
              e.target.checked
                ? [...prev, layer.name]
                : prev.filter(n => n !== layer.name)
            )}
            style={{ flex: 1 }}
          >
            {layer.name}
          </Checkbox>
          <div style={{ display: 'flex', gap: 8, color: '#888' }}>
            <Tooltip title={layer.on ? '可见' : '隐藏'}>
              {layer.on
                ? <EyeOutlined style={{ color: '#4ea4f6' }} />
                : <EyeInvisibleOutlined />}
            </Tooltip>
            <Tooltip title={layer.frozen ? '已冻结' : '未冻结'}>
              <span style={{ opacity: layer.frozen ? 1 : 0.25 }}>
                <SnowflakeIcon />
              </span>
            </Tooltip>
            <Tooltip title={layer.locked ? '已锁定' : '未锁定'}>
              {layer.locked
                ? <LockOutlined style={{ color: '#faad14' }} />
                : <UnlockOutlined style={{ opacity: 0.25 }} />}
            </Tooltip>
          </div>
        </div>
      ))}
    </div>
  </Form.Item>
)}
```

- [ ] **Step 6: 更新 `handleOk` 依赖数组**

将第 120 行：
```jsx
}, [viewerRef, format, fmtInfo, selectedLayers, gisStore, onClose])
```
改为：
```jsx
}, [viewerRef, format, fmtInfo, selectedCadLayers, cadLayers, gisStore, onClose])
```

- [ ] **Step 7: Lint**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
npm run lint
```

Expected: 无新增 lint 错误（可能有警告，注意未使用变量 `selectedLayers` 是否完全清除）。

- [ ] **Step 8: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
git add src/components/GisService/ExportGisModal.jsx
git commit -m "feat(gis): select CAD layers in export dialog with status icons"
```

---

## Task 6: 端到端手工验证

**Files:** 无代码改动，验证产物。

- [ ] **Step 1: 启动前后端**

```bash
cd e:/ODAGitLab/main24.10/DrawingWebApp
npm run dev
# 新终端
cd e:/ODAGitLab/main24.10/DrawingWebApp/server
npm run dev
```

- [ ] **Step 2: 场景 A —— 默认勾选正确性**

1. 打开一个含多个 CAD 图层的 DWG，其中手动隐藏/冻结 2-3 个图层
2. 点击"GIS 服务 → 导出"
3. 验证：Modal 中列出所有 CAD 图层；隐藏/冻结图层**未**被默认勾选；其它图层默认勾选；图标状态与实际一致

- [ ] **Step 3: 场景 B —— 部分导出**

1. 仅勾选 2-3 个图层，导出 GPKG
2. 用 QGIS / `ogrinfo -al` 打开，验证只有所选图层存在
3. 图层名为中文的场景也要测一次（确认 UTF-8 通路无误）

- [ ] **Step 4: 场景 C —— 全选 / 全不选 = 全部**

1. 点"全选"Checkbox，导出
2. 验证结果包含所有图层
3. 再点"全选"取消全部，导出
4. 验证结果仍为全部图层（兼容原"留空=全部"语义）

- [ ] **Step 5: 场景 D —— 回归一键回写**

1. 先导入一个 .shp，再触发"一键回写"
2. 验证导出成功（`handleGisSaveBack` 传空串 → 全部导出）

- [ ] **Step 6: 场景 E —— AI 助手兼容**

在 AI 助手面板让它执行"导出当前图纸为 GeoJSON"之类自然语言指令；验证生成的 `viewer.execute('GIS_EXPORT', [...])` 调用能正常完成（若只传 2 参，命令会因第 3 个 getString 等待输入而挂起 —— 这是预期的破坏，需要后续更新 RAG 示例或工具定义，列入 follow-up）。

- [ ] **Step 7: 创建 Follow-up（如必要）**

若 AI 助手的 `cadTools.js` 或 RAG 示例中包含仅传 2 参的 `GIS_EXPORT` 调用，创建单独 issue / plan 跟进。当前 grep 未在 `server/` 命中该调用，暂无需处理。

---

## Self-Review Checklist

- [x] Spec 每个设计决策都映射到具体 Task（决策 1 → Task 5；决策 2 → Task 5 Step 3；决策 3 → Task 5 Step 5；决策 4 → Task 1-3）
- [x] 无 TBD/TODO/占位符
- [x] 跨 Task 类型/参数命名一致：`dwgLayerFilter` 在 C++ 侧统一，`layerFilter` 在 JS/WASM 命令侧统一
- [x] 每个代码改动都给出具体文件路径 + 行号 + 完整代码块
- [x] 向后兼容路径明确（`handleGisSaveBack` 单独修复）
- [x] 前端修改使用 frontend-design skill 的约束已在 Task 5 Step 1 明示

## 相关笔记

- [[Legend Analysis Redesign Implementation Plan]]
- [[GIS 导入实体类型透传 — 实现计划]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
- [[plans]]
- [[GIS File Import Implementation Plan]]
- [[UAOdcadCore GIS Service Implementation Plan]]
- [[WASM License Gate Implementation Plan]]
- [[GIS 目录面板 + 调图/属性查询 Implementation Plan]]
