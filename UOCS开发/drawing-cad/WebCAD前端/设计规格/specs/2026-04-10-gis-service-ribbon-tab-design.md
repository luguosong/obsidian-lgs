# GIS服务 Ribbon 标签页设计规格

> **日期**: 2026-04-10
> **范围**: ReviewRibbon 中新增"GIS服务"标签页的 UI 设计
> **前置依赖**: [ArcGIS 集成 C++ 架构](2026-04-10-arcgis-integration-architecture.md)
> **状态**: 设计确认

---

## 概述

在审图模式（ReviewRibbon）的"签章"标签页右侧新增"GIS服务"标签页，为 WebUACAD 提供 ArcGIS Web 服务的双向互操作能力。该标签页是 C++ 四层 GIS 集成架构在前端的操作入口。

### 设计决策记录

| 维度 | 决策 | 理由 |
|------|------|------|
| 功能范围 | 双向完整版（GIS→DWG + DWG→GIS） | 审图场景需要同时查看 GIS 数据和回写编辑结果 |
| 要素编辑 | 读+写（可同步回 FeatureServer） | 对标 ArcGIS for AutoCAD 的 Push/Pull 模式 |
| 服务连接 | 预配置快速连接 + 手动 URL 输入 | 兼顾内网固定服务和临时连接需求 |
| 坐标系 | 自动识别 + 信息查看按钮 | 减少操作复杂度，冲突时才需手动介入 |
| 图层样式 | 基础样式映射（图层名/颜色/线型） | 满足审图叠加需求，不需要完整 GIS 符号化 |
| 分组方案 | 按数据类型 4 组 | 紧凑，与现有 Tab（签章、测量各 4 组）风格统一 |

---

## TabBar 变更

在 `REVIEW_TABS` 数组中，"签章"后面插入"GIS服务"：

```
之前: ['主页', '比对', '测量', '签章', '审查流程', 'BIM审查', '输出']
之后: ['主页', '比对', '测量', '签章', 'GIS服务', '审查流程', 'BIM审查', '输出']
```

---

## 工具条总览

**4 个分组 · 19 个按钮**

```
┌─────────────────┬────────────────┬──────────────────────────────────────┬───────────────┐
│     连接 (5)     │  地图影像 (4)  │            要素数据 (7)               │   工具 (3)    │
├─────────────────┼────────────────┼──────────────────────────────────────┼───────────────┤
│ [常用服务]  P    │ [加载底图]  P  │ [加载要素] P  │ [推送修改] G  │ [坐标系信息]  │
│ [添加服务]       │ [刷新影像]     │ [属性查询]    │ [拉取更新] G  │ [导出GIS]  P  │
│ [浏览目录]       │ [透明度]       │ [空间查询]    │ [同步状态]    │ [操作日志]    │
│ ── 分隔线 ──     │ ── 分隔线 ──   │ [样式映射] A  │               │               │
│ [认证管理]       │ [移除底图]  D  │ ── 分隔线 ──  │               │               │
│ [断开连接]  D    │                │               │               │               │
└─────────────────┴────────────────┴──────────────────────────────────────┴───────────────┘

P = primary (蓝色强调)    D = danger (红色警告)
G = green (绿色同步)      A = amber (橙色配置)
```

---

## 分组 1：连接

管理与 ArcGIS Server / Portal 的服务连接。

| # | 按钮 | 样式 | 功能 | 交互方式 | C++ 对应 |
|---|------|------|------|----------|----------|
| 1 | 常用服务 | primary | 下拉菜单展示预配置的 ArcGIS Server 列表，一键连接 | Dropdown 下拉菜单 | `ArcGisRestClient::getLayerInfo()` |
| 2 | 添加服务 | — | 弹窗输入 MapServer / FeatureServer REST URL | Modal 对话框 | `MapImageLayerReader::open()` / `FeatureLayerReader::open()` |
| 3 | 浏览目录 | — | 连接 ArcGIS Server REST 端点后，树形浏览服务目录并勾选图层 | Drawer 侧边面板 | `ArcGisRestClient::getLayerInfo()` |
| 4 | 认证管理 | — | 管理 Token 认证和用户名/密码凭证。支持 ArcGIS Server 和 Portal 认证 | Modal 对话框 | `ArcGisRestClient::generateToken()` |
| 5 | 断开连接 | danger | 断开当前 ArcGIS 服务连接，清理本地缓存 | 确认弹窗 | `*Reader::close()` |

**预配置服务格式**（存储在前端配置或后端）：

```json
[
  {
    "name": "东莞规划地理信息",
    "mapServerUrl": "http://kjgh.dg:30088/.../MapServer",
    "featureServerUrl": "http://kjgh.dg:30088/.../FeatureServer",
    "srs": "EPSG:4526"
  }
]
```

---

## 分组 2：地图影像

操作栅格/瓦片底图影像图层（对应 C++ `MapImageLayerReader` + `OdArcGisGeoMapPE`）。

| # | 按钮 | 样式 | 功能 | 交互方式 | C++ 对应 |
|---|------|------|------|----------|----------|
| 1 | 加载底图 | primary | 从已连接的 MapServer 加载影像底图，叠加到当前 DWG 视口 | 点击即执行（需已连接服务） | `MapImageLayerReader::exportImage()` → `OdArcGisGeoMapPE::updateMapImage()` |
| 2 | 刷新影像 | — | 按当前视口范围和缩放级别重新获取影像瓦片 | 点击即执行 | `MapImageLayerReader::exportTile()` |
| 3 | 透明度 | — | 滑块调节底图影像透明度（0%–100%） | Popover 滑块 | `OdDbRasterImage` 透明度属性 |
| 4 | 移除底图 | danger | 从当前图纸中移除已加载的 GIS 底图影像 | 确认弹窗 | `OdDbRasterImage::erase()` |

---

## 分组 3：要素数据

操作矢量要素图层，包含加载/查询和同步两个子区域，以分隔线分开。

### 加载与查询（分隔线上方）

| # | 按钮 | 样式 | 功能 | 交互方式 | C++ 对应 |
|---|------|------|------|----------|----------|
| 1 | 加载要素 | primary | 从 FeatureServer 拉取矢量要素，转换为 DWG 实体（点→OdDbPoint，线→OdDbPolyline，面→OdDbHatch） | Drawer：图层列表 + 勾选 | `FeatureLayerReader::open()` → `FeatureToDwgConverter::convert()` |
| 2 | 属性查询 | — | 输入 WHERE 条件过滤要素（如 `用地类型='R2'`） | Modal：输入 WHERE 子句 | `FeatureLayerReader::queryByWhere()` |
| 3 | 空间查询 | — | 框选范围或输入 bbox 坐标，仅加载该范围内的要素 | 画布框选 + 执行 | `FeatureLayerReader::queryByExtent()` |
| 4 | 样式映射 | amber | 设置要素 → DWG 的映射规则：目标图层名、颜色、线型 | Modal 对话框（表格式映射配置） | `FeatureToDwgConverter::ConvertOptions` |

### 数据同步（分隔线下方）

| # | 按钮 | 样式 | 功能 | 交互方式 | C++ 对应 |
|---|------|------|------|----------|----------|
| 5 | 推送修改 | green | 将 DWG 中编辑过的要素同步回 ArcGIS FeatureServer（Push） | 确认弹窗 → 执行 | `DwgToGisExporter`（FeatureServer 写入通道） |
| 6 | 拉取更新 | green | 从 FeatureServer 重新获取最新数据，更新 DWG 中对应实体（Pull） | 确认弹窗 → 执行 | `FeatureLayerReader` + 增量更新逻辑 |
| 7 | 同步状态 | — | 查看已修改/待推送/冲突的要素列表 | Drawer 侧边面板 | `GisToDwgImporter` 状态管理 |

**几何类型映射规则**：

| OGR 几何类型 | DWG 实体 | 说明 |
|-------------|---------|------|
| `wkbPoint` | `OdDbPoint` 或 `OdDbBlockReference` | 可选块参照以区分点类型 |
| `wkbLineString` / `wkbMultiLineString` | `OdDbPolyline` (LWPolyline) | 保留顶点精度 |
| `wkbPolygon` / `wkbMultiPolygon` | `OdDbHatch` + `OdDbPolyline` | 填充 + 边界 |

---

## 分组 4：工具

坐标系查看、GIS 格式导出、操作日志。

| # | 按钮 | 样式 | 功能 | 交互方式 | C++ 对应 |
|---|------|------|------|----------|----------|
| 1 | 坐标系信息 | — | 查看当前图纸坐标系 + GIS 服务坐标系 + 桥接状态。坐标系冲突时弹出选择对话框 | Popover 信息卡片 | `CrsBridge::odaCrsToGdalSrs()` / `OdDbGeoData` |
| 2 | 导出GIS | primary | 将 DWG 实体导出为 GIS 格式，支持 GeoPackage / Shapefile / GeoJSON / FileGDB | Modal：选择格式 + 图层 + 路径 | `DwgToGisExporter::execute()` |
| 3 | 操作日志 | — | 查看所有 GIS 操作的详细日志：连接、加载、同步、导出时间线 | Drawer 侧边面板 | `GisIntegrationModule` 日志 |

---

## 组件架构

### 新增组件

```
src/components/Ribbon/
  ReviewRibbon.jsx          ← 修改：新增 GisServiceTab 引用 + case 分支

src/components/GisService/  ← 新建目录
  GisServiceTab.jsx         ← GIS服务标签页主组件（4 个 RvGroup）
  AddServiceModal.jsx       ← "添加服务"弹窗
  ServiceBrowser.jsx        ← "浏览目录"侧边面板（树形服务目录）
  AuthManager.jsx           ← "认证管理"弹窗
  StyleMappingModal.jsx     ← "样式映射"配置弹窗
  ExportGisModal.jsx        ← "导出GIS"弹窗（格式+图层+路径选择）
  SyncStatusPanel.jsx       ← "同步状态"侧边面板
  GisLogPanel.jsx           ← "操作日志"侧边面板
```

### 状态管理

在 `RootStore` 中新增 `GisStore`（MobX store），管理：

```
GisStore
├── connectionState        // 'disconnected' | 'connecting' | 'connected'
├── activeServices[]       // 当前连接的服务列表
├── presetServices[]       // 预配置常用服务
├── mapImageLayers[]       // 已加载的底图影像列表
├── featureLayers[]        // 已加载的要素图层列表
├── syncStatus             // { modified: [], pending: [], conflicts: [] }
├── coordinateInfo         // { dwgCrs, gisCrs, bridgeStatus }
└── operationLog[]         // 操作日志条目
```

### WASM 桥接

GIS 操作通过 `viewer.execute()` 调用 C++ 侧命令，命名约定：

| 前端操作 | WASM 命令名 | 说明 |
|---------|------------|------|
| 加载底图 | `GIS_LOAD_MAP_IMAGE` | 传入 MapServer URL + bbox |
| 加载要素 | `GIS_LOAD_FEATURES` | 传入 FeatureServer URL + 图层 ID + 查询条件 |
| 推送修改 | `GIS_PUSH_FEATURES` | 传入修改的实体 ID 列表 |
| 拉取更新 | `GIS_PULL_FEATURES` | 传入图层 ID |
| 导出GIS | `GIS_EXPORT` | 传入格式 + 路径 + 图层筛选 |
| 坐标系查询 | `GIS_CRS_INFO` | 返回坐标系信息 JSON |

C++ → JS 回调注册（与现有模式一致）：

```
window.__onGisConnected      // 服务连接成功
window.__onGisLoadProgress   // 加载进度
window.__onGisSyncComplete   // 同步完成
window.__onGisError          // 错误回调
```

---

## 文件修改清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `src/components/TabBar/TabBar.jsx` | 修改 | `REVIEW_TABS` 数组插入 `'GIS服务'` |
| `src/components/Ribbon/ReviewRibbon.jsx` | 修改 | 新增 `case 'GIS服务'` 分支 + 导入 GisServiceTab + 新增 SVG 图标 |
| `src/components/GisService/GisServiceTab.jsx` | 新建 | 标签页主组件 |
| `src/components/GisService/AddServiceModal.jsx` | 新建 | 添加服务弹窗 |
| `src/components/GisService/ServiceBrowser.jsx` | 新建 | 服务目录浏览面板 |
| `src/components/GisService/AuthManager.jsx` | 新建 | 认证管理弹窗 |
| `src/components/GisService/StyleMappingModal.jsx` | 新建 | 样式映射配置弹窗 |
| `src/components/GisService/ExportGisModal.jsx` | 新建 | GIS 导出弹窗 |
| `src/components/GisService/SyncStatusPanel.jsx` | 新建 | 同步状态面板 |
| `src/components/GisService/GisLogPanel.jsx` | 新建 | 操作日志面板 |
| `src/stores/GisStore.js` | 新建 | GIS 状态管理 |
| `src/stores/RootStore.js` | 修改 | 注入 GisStore |
| `src/context/ViewerContext.js` | 修改 | 暴露 GisStore（如需） |

---

## 与 C++ 架构的映射关系

```
前端 UI 分组           C++ 架构层               核心类
─────────────        ──────────────           ────────────
连接                → Layer 1 (服务接入)      → ArcGisRestClient
地图影像            → Layer 1 + Layer 3.1     → MapImageLayerReader + OdArcGisGeoMapPE
要素数据 (加载)     → Layer 1 + Layer 3.2     → FeatureLayerReader + FeatureToDwgConverter
要素数据 (同步)     → Layer 4                 → GisToDwgImporter / DwgToGisExporter
工具 (坐标系)       → Layer 2                 → CrsBridge
工具 (导出)         → Layer 4.2               → DwgToGisExporter
```
