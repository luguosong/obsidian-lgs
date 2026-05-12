# GIS 目录面板 + 调图/属性查询 设计文档

**日期**：2026-04-18  
**状态**：已批准，待实施  
**分支**：[[feat-zfs]]

---

## 背景

`GisStore.presetServices` 中存在文件夹型 URL（如 `http://106.14.254.175:6081/arcgis/rest/services/upda/`），该 URL 并非单一 MapServer/FeatureServer，而是一个 ArcGIS REST 服务文件夹，内含多个服务。当前代码在点击此类预置服务时会因 `mapServerUrl` 为空而静默失败。

本文档描述两个新功能的完整设计：

1. **GIS [[目录面板]]**：连接文件夹型 URL 后，在左侧固定面板中自动展开可勾选的目录树。
2. **调图 + 属性查询**：用户在目录树中勾选图层后，通过底部按钮执行空间范围加载或属性表查看。

---

## 约束

- **审图模式**（Review Mode）无命令行输入框，所有参数必须通过 UI 传递给 C++ 命令。
- 不改变绘图模式（Drawing Mode）下的现有行为。
- 画布 WebGL viewport 尺寸不能因面板插入而受影响。

---

## 架构决策

| 决策点 | 选择 | 理由 |
|---|---|---|
| 面板位置 | App 级 LeftSidebar | 与 RightSidebar 对称，GisStore 集中管控 |
| 树深度 | 深树（到图层级） | 精细勾选，懒加载展开避免初始开销 |
| 框选交互 | 复用 `startAreaPick()` | 已有 C++ snap + 橙红矩形 overlay，零新代码 |
| 多边形交互 | 新增 `startPolygonPick()` | 仿 `startAreaPick` 结构，约 40 行 |
| 属性查询 | 只读 Modal Table | 展示要素属性，不加载到 DWG |

---

## 功能一：GIS 目录面板

### 1.1 布局变更（App.jsx）

在 `mainRow` 的 `centerCol` **左侧**插入 `GisCatalogPanel`，由 `gisStore.catalogOpen` 控制显隐：

```jsx
<div className={s.mainRow}>
  {gisStore.catalogOpen && <GisCatalogPanel />}   {/* 新增 */}
  <div className={s.centerCol}>
    <CanvasArea />
    ...
  </div>
  <div style={disabledStyle}>
    <RightSidebar />
  </div>
</div>
```

面板默认宽度 240px，可拖拽（右侧 resize handle），持久化到 `localStorage`（key: `DrawingWebApp:leftCatalogWidth`）。最小宽度 180px，最大 400px。

### 1.2 GisCatalogPanel 组件

**文件**：`src/components/GisService/GisCatalogPanel.jsx`

结构：
```
GisCatalogPanel
├── 面板头部：标题"空间数据库" + 服务 URL（截断显示） + 刷新按钮 + 关闭按钮
├── Ant Design Tree（checkable, loadData 懒加载）
│   ├── 服务节点（key="svc:{i}"，isLeaf=false）
│   │   └── 图层节点（key="lyr:{svcI}:{layerId}"，isLeaf=true）
└── 底部操作区
    ├── 「📐 调图」按钮（Ant Design Popover）
    └── 「🔍 属性查询」按钮
```

**树节点数据结构**：
```js
{
  key: string,          // "svc:0" | "lyr:0:3"
  title: string,        // 显示名称
  serviceUrl: string,   // 该节点所属服务的 REST URL
  layerId: number,      // 图层 ID（仅图层节点有效）
  isLeaf: boolean,
}
```

**半选（half-checked）**：Ant Design Tree 自动处理父节点 CheckBox 状态。

### 1.3 ArcGIS REST 遍历

**Step 1 — 初始化（读取文件夹）**：
```
GET {folderUrl}?f=json
→ resp.services[]  每条: { name: "upda/china", type: "MapServer" }
→ 构造服务节点列表，isLeaf=false
```

服务完整 URL 推导规则：
```js
// name="upda/china", type="MapServer"
// folderUrl="http://host/arcgis/rest/services/upda/"
// → serviceUrl = "http://host/arcgis/rest/services/upda/china/MapServer"
// svc.name 已包含文件夹前缀，直接从 /services/ 根拼接
const servicesBase = folderUrl.substring(
  0, folderUrl.indexOf('/services/') + '/services/'.length
)
const serviceUrl = `${servicesBase}${svc.name}/${svc.type}`
```

**Step 2 — 懒加载（展开服务节点时）**：
```
GET {serviceUrl}?f=json
→ resp.layers[]  每条: { id, name, geometryType, subLayerIds }
→ 过滤掉 subLayerIds.length > 0 的分组节点（只保留叶子图层）
→ 构造图层节点列表，isLeaf=true
```

所有请求通过后端代理：`/api/gis/proxy?url={encodeURIComponent(targetUrl)}`（与现有代码一致）。

### 1.4 连接触发逻辑（GisServiceTab.jsx）

在 `handlePresetClick` 中检测文件夹型 URL：

```js
function isFolderUrl(url) {
  return url && !url.includes('MapServer') && !url.includes('FeatureServer')
}

// handlePresetClick 中
const svc = gisStore.presetServices[Number(key)]
if (isFolderUrl(svc.featureServerUrl)) {
  gisStore.addService(svc)
  gisStore.setConnectionState('connected')
  gisStore.openCatalog(svc.featureServerUrl)
  message.success(`已连接: ${svc.name}，正在加载目录…`)
  return
}
// 原有 MapServer 路径不变
```

### 1.5 GisStore 新增字段

```js
// 目录面板状态
catalogOpen = false
catalogServiceUrl = ''
drawingMode = null  // 'bbox' | 'polygon' | null

openCatalog(url) {
  this.catalogServiceUrl = url
  this.catalogOpen = true
}
closeCatalog() {
  this.catalogOpen = false
  this.catalogServiceUrl = ''
}
setDrawingMode(mode) {
  this.drawingMode = mode
}
```

---

## 功能二：调图

### 2.1 调图 Popover 菜单

点击「调图」按钮弹出 Ant Design Popover，内含三个选项：

| 选项 | 图标 | 行为 |
|---|---|---|
| 全部范围 | 🌐 | 直接以服务 `fullExtent` 调用 C++ 命令 |
| 框选范围 | ⬚ | 关闭 Popover，调用 `viewer.startAreaPick(onBboxPicked)` |
| 任意多边形 | ⬡ | 关闭 Popover，调用 `viewer.startPolygonPick(onPolygonPicked)` |

选中已勾选图层的所有 `layerId`，作为命令参数之一传入。

### 2.2 框选范围（复用 startAreaPick）

`startAreaPick(callback)` 已在 `ViewerService.js:2328` 完整实现：
- 两次点击捕获两角点
- 每个点经 `_snapScreenPoint()` 做 C++ 级别捕捉
- 实时绘制橙红虚线矩形 overlay（`_drawAreaPickRect`）
- 回调 `{ mode: 'rectangle', bounds: { minX, minY, maxX, maxY }, points: [...] }`

GisCatalogPanel 调用方式：
```js
gisStore.setDrawingMode('bbox')
viewer.startAreaPick(({ bounds }) => {
  gisStore.setDrawingMode(null)
  const checkedLayerIds = getCheckedLayerIds()  // 从树 checkedKeys 提取
  viewer.execute('GIS_LOAD_FEATURES_BBOX', [
    serviceUrl,
    JSON.stringify(checkedLayerIds),
    bounds.minX, bounds.minY, bounds.maxX, bounds.maxY,
  ])
})
```

### 2.3 任意多边形（新增 startPolygonPick）

在 `ViewerService.js` 新增，完全仿 `startAreaPick` 结构：

```js
startPolygonPick(callback) {
  // 状态初始化
  this._polyPickVertices = []      // 世界坐标点数组
  this._polyPickScreenPts = []     // 屏幕坐标（用于绘制）
  this._polyPickCallback = callback
  // 监听 mousemove（橡皮筋）和 dblclick（收口）
  this._polyPickMoveHandler = (ev) => this._onPolyPickMouseMove(ev)
  this._polyPickClickHandler = (ev) => this._onPolyPickClick(ev)
  this._polyPickDblHandler = (ev) => this._onPolyPickDblClick(ev)
  canvas.addEventListener('mousemove', this._polyPickMoveHandler)
  canvas.addEventListener('click', this._polyPickClickHandler)
  canvas.addEventListener('dblclick', this._polyPickDblHandler)
}

_onPolyPickMouseMove(ev) {
  if (!this._polyPickScreenPts.length) return
  this._polyPickCurrentScreen = { x: ev.offsetX, y: ev.offsetY }
  this._drawPolyPickOverlay()  // 用虚线橡皮筋更新 overlay
}

_onPolyPickClick(ev) {
  if (ev.detail > 1) return  // 排除双击的第一次单击
  const coords = this.getCanvasCoords(ev)
  const snapped = this._snapScreenPoint(coords.x, coords.y)
  this._polyPickVertices.push(snapped)
  this._polyPickScreenPts.push({ x: coords.x, y: coords.y })
  this._drawPolyPickOverlay()
}

_onPolyPickDblClick(ev) {
  if (this._polyPickVertices.length < 3) {
    message.warning('至少需要 3 个点')
    return
  }
  const vertices = [...this._polyPickVertices]
  const cb = this._polyPickCallback
  this.cancelPolygonPick()
  cb(vertices)
}

cancelPolygonPick() {
  canvas.removeEventListener('mousemove', this._polyPickMoveHandler)
  canvas.removeEventListener('click', this._polyPickClickHandler)
  canvas.removeEventListener('dblclick', this._polyPickDblHandler)
  this._clearPolyPickOverlay()
  this._polyPickVertices = []
  this._polyPickScreenPts = []
  this._polyPickCallback = null
}

_drawPolyPickOverlay() {
  // 复用 _areaPickCanvas 同类方案创建 canvas overlay
  // 绘制：已有顶点的蓝色实线路径 + 虚线橡皮筋到鼠标当前位置
  // 最后一段虚线从最后顶点连回第一顶点（预览闭合）
}
```

GisCatalogPanel 调用方式：
```js
gisStore.setDrawingMode('polygon')
viewer.startPolygonPick((vertices) => {
  gisStore.setDrawingMode(null)
  const points = vertices.map(v => `${v.x},${v.y}`).join(';')
  viewer.execute('GIS_LOAD_FEATURES_POLYGON', [
    serviceUrl,
    JSON.stringify(checkedLayerIds),
    points,
  ])
})
```

### 2.4 ESC 取消绘制模式

在 `GisCatalogPanel` 监听 `keydown` 事件：
```js
useEffect(() => {
  const onKey = (ev) => {
    if (ev.key === 'Escape' && gisStore.drawingMode) {
      if (gisStore.drawingMode === 'bbox') viewer.cancelAreaPick()
      if (gisStore.drawingMode === 'polygon') viewer.cancelPolygonPick()
      gisStore.setDrawingMode(null)
    }
  }
  window.addEventListener('keydown', onKey)
  return () => window.removeEventListener('keydown', onKey)
}, [gisStore.drawingMode])
```

---

## 功能三：属性查询

点击「属性查询」按钮，对勾选的每个图层并行请求：

```
GET {serviceUrl}/{layerId}/query?where=1=1&outFields=*&f=json&resultRecordCount=500
```

通过后端代理。响应解析：
- `resp.fields[]` → Table 列定义（`{ alias, name, type }`）
- `resp.features[]` → Table 数据行（`feature.attributes`）

UI：Ant Design Modal（宽度 800px）+ Table：
- 列宽可拖拽
- 支持本地文本过滤（`antd Input + filterDropdown`）
- 「导出 CSV」按钮（前端纯 JS 生成，不依赖后端）
- 多图层时 Modal 内用 Tabs 切换

---

## 改动文件清单

| 文件 | 类型 | 改动说明 |
|---|---|---|
| `src/App.jsx` | 改 | mainRow 中插入 GisCatalogPanel，受 gisStore.catalogOpen 控制 |
| `src/App.module.css` | 改 | 左侧宽度 CSS 变量（参考现有 RightSidebar 模式） |
| `src/stores/GisStore.js` | 改 | 新增 3 字段（catalogOpen/catalogServiceUrl/drawingMode）+ 3 方法 |
| `src/components/GisService/GisServiceTab.jsx` | 改 | handlePresetClick 检测文件夹 URL → openCatalog |
| `src/services/ViewerService.js` | 改 | 新增 startPolygonPick / cancelPolygonPick / _drawPolyPickOverlay |
| `src/components/GisService/GisCatalogPanel.jsx` | 新增 | 主面板（Tree + 调图 Popover + 属性查询 Modal） |
| `src/components/GisService/GisCatalogPanel.module.css` | 新增 | 面板样式（宽度变量、拖拽 handle、resize 逻辑） |

**不改动**：`ServiceBrowser.jsx`、`ImportGisModal.jsx`、其余 GIS 组件。

---

## 不在本次范围内

- C++ 侧新增 `GIS_LOAD_FEATURES_BBOX` / `GIS_LOAD_FEATURES_POLYGON` 命令（假设已存在或由 C++ 团队实现；若不存在，JS 侧将坐标转换后复用现有 `GIS_LOAD_FEATURES` 命令并追加参数）
- 属性表行点击高亮 DWG 对应要素
- 多文件夹嵌套递归展开
- 认证（Token/用户名密码）集成到[[目录面板]]

---

## 测试验证要点

1. 连接 `http://106.14.254.175:6081/arcgis/rest/services/upda/` → 左侧面板自动展开，根节点显示"空间数据库"
2. 展开 `china (MapServer)` → 懒加载图层列表，不报错
3. 勾选若干图层 → 调图 → 全部范围 → C++ 命令收到正确参数
4. 调图 → 框选范围 → 画布出现十字光标 + 橙红矩形 overlay → ESC 取消无残留
5. 调图 → 任意多边形 → 逐点点击 → 双击收口 → 命令收到坐标点数组
6. 属性查询 → Modal 展示要素属性表，导出 CSV 可用
7. 关闭面板 → 左侧空间归还画布，无布局抖动
8. 连接非文件夹类 URL 的预置服务 → 原有 MapServer 流程不受影响

## 相关笔记

- [[specs]]
- [[DWG 导出 GIS 按 CAD 图层过滤 — 设计文档]]
- [[Legend Analysis Redesign: Programmatic Region Scan + Vision]]
- [[Industry Standards RAG Knowledge Base Design]]
- [[WASM License Gate 设计（DrawingWebApp）]]
- [[审图批注沙箱 API 设计]]
- [[设计文档：同步 quzhen 分支审查批注功能至 feat-zfs]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
