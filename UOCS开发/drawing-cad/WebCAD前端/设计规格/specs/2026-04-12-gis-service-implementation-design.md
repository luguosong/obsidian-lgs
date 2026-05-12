# GIS服务 Ribbon 标签页 — 后续实施设计

> **日期**: 2026-04-12
> **范围**: 基于已确认的 UI Shell，实施组件拆分、状态管理和 WASM 桥接
> **前置**: [GIS服务 Ribbon 设计规格](2026-04-10-gis-service-ribbon-tab-design.md) + [UI Shell 实施计划](2026-04-10-gis-service-ribbon-tab-plan.md)
> **状态**: 设计确认

---

## 概述

UI Shell 阶段已完成（19 个桩按钮内联在 ReviewRibbon.jsx 中）。本阶段将：

1. **前端组件层** — 将 GisServiceTab 提取为独立组件体系，实现各弹窗/面板 UI 外壳
2. **状态管理层** — 新建 GisStore（MobX），注入 RootStore
3. **WASM 桥接层** — 在 DrawingWeb 中创建 GIS 命令桩（C++ 侧），预留真实功能接口

### 关键设计决策

| 维度 | 决策 | 理由 |
|------|------|------|
| 组件拆分 | 独立目录 `src/components/GisService/` + 8 个文件 | 职责清晰，便于后续逐个实现真实功能 |
| WASM 命令文件 | 新建 `GisCommands.h/cpp` | GIS 是独立功能域，不膨胀现有 Commands 文件 |
| 桩实现 | printf + EM_ASM JS 回调 | 前端可验证调用链路，C++ 真实功能在另一工程实现 |

---

## 前端组件层

### 文件结构

```
src/components/GisService/
  GisServiceTab.jsx         ← 主组件（从 ReviewRibbon.jsx 提取）
  AddServiceModal.jsx       ← "添加服务"弹窗（URL 输入）
  ServiceBrowser.jsx        ← "浏览目录"侧边面板（树形服务目录）
  AuthManager.jsx           ← "认证管理"弹窗
  StyleMappingModal.jsx     ← "样式映射"配置弹窗
  ExportGisModal.jsx        ← "导出GIS"弹窗（格式+图层+路径）
  SyncStatusPanel.jsx       ← "同步状态"侧边面板
  GisLogPanel.jsx           ← "操作日志"侧边面板
```

### 组件职责

| 组件 | 触发按钮 | UI 形式 | 核心交互 |
|------|---------|---------|---------|
| AddServiceModal | 添加服务 | Modal 对话框 | 输入 MapServer/FeatureServer URL，确认后调用 `viewer.execute('GIS_LOAD_MAP_IMAGE'/'GIS_LOAD_FEATURES', [url])` |
| ServiceBrowser | 浏览目录 | Drawer 侧边面板 | 树形展示服务目录，勾选图层 |
| AuthManager | 认证管理 | Modal 对话框 | Token/用户名密码管理 |
| StyleMappingModal | 样式映射 | Modal 对话框 | 表格式映射配置（图层名/颜色/线型） |
| ExportGisModal | 导出GIS | Modal 对话框 | 选择格式 + 图层 + 路径，确认后调用 `viewer.execute('GIS_EXPORT', [...])` |
| SyncStatusPanel | 同步状态 | Drawer 侧边面板 | 显示 modified/pending/conflicts 列表 |
| GisLogPanel | 操作日志 | Drawer 侧边面板 | 时间线展示所有 GIS 操作日志 |

### ReviewRibbon.jsx 变更

- 删除内联的 `GisServiceTab` 函数定义
- 替换为 `import GisServiceTab from '../GisService/GisServiceTab'`
- switch case 保持不变

---

## 状态管理层

### GisStore

```js
// src/stores/GisStore.js
class GisStore {
  connectionState = 'disconnected'  // 'disconnected' | 'connecting' | 'connected'
  activeServices = []               // 当前连接的服务列表
  presetServices = [                // 预配置常用服务
    {
      name: '东莞规划地理信息',
      mapServerUrl: 'http://kjgh.dg:30088/.../MapServer',
      featureServerUrl: 'http://kjgh.dg:30088/.../FeatureServer',
      srs: 'EPSG:4526'
    }
  ]
  mapImageLayers = []               // 已加载的底图影像列表
  featureLayers = []                // 已加载的要素图层列表
  syncStatus = { modified: [], pending: [], conflicts: [] }
  coordinateInfo = { dwgCrs: '', gisCrs: '', bridgeStatus: 'unknown' }
  operationLog = []                 // 操作日志条目
}
```

### RootStore 变更

```js
import GisStore from './GisStore'

class RootStore {
  constructor() {
    // ... 现有 stores
    this.gisStore = new GisStore(this)
  }
}
```

---

## WASM 桥接层（DrawingWeb）

### 命令定义

| 命令名 | 参数 | 桩行为 | JS 回调 |
|--------|------|--------|---------|
| `GIS_LOAD_MAP_IMAGE` | url, bbox (可选) | printf 参数 → `__onGisLoadProgress(100)` → `__onGisConnected` | `__onGisConnected` |
| `GIS_LOAD_FEATURES` | url, layerId, where (可选) | printf 参数 → `__onGisLoadProgress(100)` | `__onGisLoadProgress` |
| `GIS_PUSH_FEATURES` | entityIds (逗号分隔) | printf 参数 → `__onGisSyncComplete('push', count)` | `__onGisSyncComplete` |
| `GIS_PULL_FEATURES` | layerId | printf 参数 → `__onGisSyncComplete('pull', count)` | `__onGisSyncComplete` |
| `GIS_EXPORT` | format, path, layers (可选) | printf 参数 → `__onGisSyncComplete('export', 0)` | `__onGisSyncComplete` |
| `GIS_CRS_INFO` | (无) | printf → `__onGisCrsInfo(json)` 返回坐标系 JSON | `__onGisCrsInfo` |

### JS 回调（C++ → JS）

```cpp
// 通过 EM_ASM 调用，与现有 __onCommandComplete 模式一致
window.__onGisConnected(serviceUrl)       // 服务连接成功
window.__onGisLoadProgress(percent)       // 加载进度 0-100
window.__onGisSyncComplete(action, count) // 同步完成
window.__onGisError(message)              // 错误回调
window.__onGisCrsInfo(jsonString)         // 坐标系信息
```

### 文件变更

| 文件 | 操作 |
|------|------|
| `DrawingWeb/GisCommands.h` | 新建：6 个命令类声明 |
| `DrawingWeb/GisCommands.cpp` | 新建：桩实现 |
| `DrawingWeb/CadCore.cpp` | 修改：注册 GIS 命令 |
| `DrawingWeb/CMakeLists.txt` | 修改：添加 GisCommands.cpp |
