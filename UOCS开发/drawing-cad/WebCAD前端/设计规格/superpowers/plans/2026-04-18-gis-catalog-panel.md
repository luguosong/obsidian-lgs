# GIS 目录面板 + 调图/属性查询 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use [[superpower]]s:subagent-driven-development (recommended) or [[superpower]]s:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 App 左侧新增固定目录树面板，连接文件夹型 ArcGIS REST URL 后自动展开，支持勾选图层后执行调图（框选/多边形/全部）或属性查询。

**Architecture:** App-level LeftSidebar（与 RightSidebar 对称），`GisCatalogPanel` 组件通过 `gisStore.catalogOpen` 控制显隐；框选复用现有 `startAreaPick()`；多边形新增 `startPolygonPick()`（仿现有区域拾取结构）；属性查询调 FeatureServer `/query` 接口，结果展示在 Modal Table 中。

**Tech Stack:** React 19, MobX (makeAutoObservable), Ant Design (Tree/Modal/Table/Popover), CSS Modules, ArcGIS REST API（通过 `/api/gis/proxy` 代理）

**Spec:** `docs/superpowers/specs/2026-04-18-gis-catalog-panel-design.md`

---

## 文件清单

| 路径 | 操作 | 说明 |
|---|---|---|
| `src/stores/GisStore.js` | 改 | 新增 3 字段 + 3 方法 |
| `src/services/ViewerService.js` | 改 | 新增 startPolygonPick / cancelPolygonPick / _onPolyPickMouseMove / _onPolyPickClick / _onPolyPickDblClick / _drawPolyPickOverlay / _clearPolyPickOverlay |
| `src/components/GisService/GisCatalogPanel.jsx` | 新增 | 主面板（Tree + 调图 Popover + 属性查询 Modal） |
| `src/components/GisService/GisCatalogPanel.module.css` | 新增 | 面板样式 + resize handle |
| `src/App.jsx` | 改 | mainRow 插入 GisCatalogPanel |
| `src/components/GisService/GisServiceTab.jsx` | 改 | handlePresetClick 检测文件夹 URL |

---

## Task 1：GisStore 新增目录面板状态

**Files:**
- Modify: `src/stores/GisStore.js`

- [ ] **Step 1: 在 GisStore 的字段声明区（第 6 行 presetServices 之后）新增三个字段**

  打开 [src/stores/GisStore.js](src/stores/GisStore.js)，在 `activeServices = []` 这行**之前**插入：

  ```js
  // 目录面板状态
  catalogOpen = false
  catalogServiceUrl = ''
  drawingMode = null  // 'bbox' | 'polygon' | null
  ```

- [ ] **Step 2: 在 `clearLog()` 方法之后新增三个方法**

  ```js
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

- [ ] **Step 3: 验证**

  在浏览器 DevTools Console 执行：
  ```js
  const store = window.__odaUi?.rootStore?.gisStore
  store.openCatalog('http://test/')
  console.log(store.catalogOpen, store.catalogServiceUrl)
  // 期望: true  "http://test/"
  store.closeCatalog()
  console.log(store.catalogOpen)
  // 期望: false
  ```

- [ ] **Step 4: 提交**

  ```bash
  git add src/stores/GisStore.js
  git commit -m "feat(gis): add catalogOpen/catalogServiceUrl/drawingMode to GisStore"
  ```

---

## Task 2：ViewerService 新增多边形拾取模式

**Files:**
- Modify: `src/services/ViewerService.js`（在 `cancelAreaPick` 方法之后，约第 2347 行）

- [ ] **Step 1: 在 `cancelAreaPick()` 方法结束的 `}` 之后（约 2347 行），插入整块多边形拾取代码**

  ```js
  // ==================== 多边形拾取模式 ====================
  startPolygonPick(callback) {
    this._polyPickVertices = []
    this._polyPickScreenPts = []
    this._polyPickCurrentScreen = null
    this._polyPickCallback = callback

    if (!this._polyPickCanvas) {
      this._polyPickCanvas = document.createElement('canvas')
      this._polyPickCanvas.style.cssText =
        'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:102'
      const container = canvas?.parentElement || document.body
      container.appendChild(this._polyPickCanvas)
    }
    if (canvas) {
      this._polyPickCanvas.width = canvas.width
      this._polyPickCanvas.height = canvas.height
    }

    this._polyPickMoveHandler = (ev) => this._onPolyPickMouseMove(ev)
    this._polyPickClickHandler = (ev) => this._onPolyPickClick(ev)
    this._polyPickDblHandler = (ev) => this._onPolyPickDblClick(ev)
    canvas?.addEventListener('mousemove', this._polyPickMoveHandler)
    canvas?.addEventListener('click', this._polyPickClickHandler)
    canvas?.addEventListener('dblclick', this._polyPickDblHandler)
  }

  cancelPolygonPick() {
    canvas?.removeEventListener('mousemove', this._polyPickMoveHandler)
    canvas?.removeEventListener('click', this._polyPickClickHandler)
    canvas?.removeEventListener('dblclick', this._polyPickDblHandler)
    this._polyPickMoveHandler = null
    this._polyPickClickHandler = null
    this._polyPickDblHandler = null
    this._clearPolyPickOverlay()
    this._polyPickVertices = []
    this._polyPickScreenPts = []
    this._polyPickCurrentScreen = null
    this._polyPickCallback = null
  }

  _onPolyPickMouseMove(ev) {
    if (!this._polyPickScreenPts.length) return
    this._polyPickCurrentScreen = { x: ev.offsetX, y: ev.offsetY }
    this._drawPolyPickOverlay()
  }

  _onPolyPickClick(ev) {
    if (ev.detail > 1) return  // 排除双击触发的单击事件
    const coords = this.getCanvasCoords(ev)
    const snapped = this._snapScreenPoint(coords.x, coords.y)
    this._polyPickVertices.push(snapped)
    this._polyPickScreenPts.push({ x: coords.x, y: coords.y })
    this._drawPolyPickOverlay()
  }

  _onPolyPickDblClick() {
    if (this._polyPickVertices.length < 3) return  // 至少 3 点成多边形
    const vertices = [...this._polyPickVertices]
    const cb = this._polyPickCallback
    this.cancelPolygonPick()
    if (cb) cb(vertices)
  }

  _drawPolyPickOverlay() {
    const c = this._polyPickCanvas
    if (!c || !canvas) return
    if (c.width !== canvas.width) c.width = canvas.width
    if (c.height !== canvas.height) c.height = canvas.height

    const ctx = c.getContext('2d')
    ctx.clearRect(0, 0, c.width, c.height)
    const pts = this._polyPickScreenPts
    if (!pts.length) return

    // 已有路径（实线蓝色）
    ctx.beginPath()
    ctx.moveTo(pts[0].x, pts[0].y)
    for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i].x, pts[i].y)
    ctx.strokeStyle = 'rgba(24,144,255,0.9)'
    ctx.lineWidth = 1.5
    ctx.setLineDash([])
    ctx.stroke()

    // 橡皮筋线：最后顶点 → 鼠标（虚线）
    if (this._polyPickCurrentScreen) {
      const last = pts[pts.length - 1]
      ctx.beginPath()
      ctx.moveTo(last.x, last.y)
      ctx.lineTo(this._polyPickCurrentScreen.x, this._polyPickCurrentScreen.y)
      ctx.setLineDash([6, 4])
      ctx.strokeStyle = 'rgba(24,144,255,0.5)'
      ctx.stroke()

      // 预闭合线：鼠标 → 第一顶点（更淡虚线，pts.length >= 2 才有意义）
      if (pts.length >= 2) {
        ctx.beginPath()
        ctx.moveTo(this._polyPickCurrentScreen.x, this._polyPickCurrentScreen.y)
        ctx.lineTo(pts[0].x, pts[0].y)
        ctx.setLineDash([3, 6])
        ctx.strokeStyle = 'rgba(24,144,255,0.25)'
        ctx.stroke()
      }
    }

    // 顶点圆点
    ctx.setLineDash([])
    pts.forEach(p => {
      ctx.beginPath()
      ctx.arc(p.x, p.y, 4, 0, Math.PI * 2)
      ctx.fillStyle = 'rgba(24,144,255,0.9)'
      ctx.fill()
    })
  }

  _clearPolyPickOverlay() {
    if (this._polyPickCanvas) {
      const ctx = this._polyPickCanvas.getContext('2d')
      ctx?.clearRect(0, 0, this._polyPickCanvas.width, this._polyPickCanvas.height)
    }
  }
  ```

- [ ] **Step 2: 手动验证（dev server 运行中）**

  DevTools Console：
  ```js
  const viewer = window.__odaUi?.viewer
  viewer.startPolygonPick((pts) => console.log('polygon:', pts))
  // 在画布上点击 3+ 次，观察蓝色路径绘制
  // 双击收口，Console 输出坐标数组
  // 期望: 无 JS 错误，overlay 绘制正常，双击后 callback 收到 [{x,y,z}, ...]
  ```

- [ ] **Step 3: 验证 cancelPolygonPick**

  ```js
  viewer.startPolygonPick(() => {})
  // 点击几次
  viewer.cancelPolygonPick()
  // 期望: overlay 清除，画布无残留
  ```

- [ ] **Step 4: 提交**

  ```bash
  git add src/services/ViewerService.js
  git commit -m "feat(viewer): add startPolygonPick/cancelPolygonPick with snap + canvas overlay"
  ```

---

## Task 3：GisCatalogPanel — CSS + 骨架 + Tree 懒加载

**Files:**
- Create: `src/components/GisService/GisCatalogPanel.module.css`
- Create: `src/components/GisService/GisCatalogPanel.jsx`

- [ ] **Step 1: 创建 CSS 文件**

  新建 `src/components/GisService/GisCatalogPanel.module.css`：

  ```css
  .panel {
    display: flex;
    flex-direction: column;
    width: var(--leftCatalogWidth, 240px);
    min-width: 180px;
    max-width: 400px;
    background: var(--ant-color-bg-container, #1e2235);
    border-right: 1px solid var(--ant-color-border, #303040);
    overflow: hidden;
    flex-shrink: 0;
    position: relative;
  }

  .resizer {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    cursor: col-resize;
    z-index: 10;
  }
  .resizer:hover,
  .resizerActive {
    background: rgba(24, 144, 255, 0.3);
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 8px 10px 8px 12px;
    border-bottom: 1px solid var(--ant-color-border, #303040);
    flex-shrink: 0;
  }

  .title {
    font-size: 13px;
    font-weight: 600;
    color: var(--ant-color-primary, #1890ff);
  }

  .url {
    font-size: 10px;
    color: #888;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 150px;
    margin-top: 2px;
  }

  .headerActions {
    display: flex;
    gap: 2px;
    flex-shrink: 0;
    margin-left: 4px;
  }

  .iconBtn {
    background: none;
    border: none;
    color: #888;
    cursor: pointer;
    font-size: 14px;
    padding: 2px 5px;
    border-radius: 3px;
    line-height: 1;
  }
  .iconBtn:hover {
    color: #bbb;
    background: rgba(255, 255, 255, 0.06);
  }

  .treeWrap {
    flex: 1;
    overflow-y: auto;
    padding: 4px 2px;
    min-height: 0;
  }

  .centered {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80px;
  }

  .footer {
    display: flex;
    gap: 6px;
    padding: 8px 10px;
    border-top: 1px solid var(--ant-color-border, #303040);
    flex-shrink: 0;
  }

  .popoverMenu {
    width: 164px;
  }

  .popoverItem {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 10px;
    cursor: pointer;
    border-radius: 4px;
    font-size: 13px;
    transition: background 0.15s;
  }
  .popoverItem:hover {
    background: rgba(24, 144, 255, 0.1);
  }

  .popoverIcon {
    font-size: 16px;
    width: 20px;
    text-align: center;
    flex-shrink: 0;
  }

  .popoverLabel {
    font-size: 12px;
  }

  .popoverHint {
    font-size: 10px;
    color: #888;
    margin-top: 1px;
  }
  ```

- [ ] **Step 2: 创建组件骨架（只含 Tree + 懒加载，暂无调图/属性查询）**

  新建 `src/components/GisService/GisCatalogPanel.jsx`：

  ```jsx
  import { useState, useEffect, useCallback, useRef } from 'react'
  import { Tree, Button, Spin, message, Popover, Modal, Table, Tabs } from 'antd'
  import { observer } from 'mobx-react-lite'
  import { useStores } from '../../context/ViewerContext'
  import s from './GisCatalogPanel.module.css'

  const WIDTH_KEY = 'DrawingWebApp:leftCatalogWidth'
  const clamp = (n, min, max) => Math.max(min, Math.min(max, n))

  function buildServiceUrl(folderUrl, name, type) {
    const servicesBase = folderUrl.substring(
      0, folderUrl.indexOf('/services/') + '/services/'.length
    )
    return `${servicesBase}${name}/${type}`
  }

  function updateTreeData(list, targetKey, children) {
    return list.map(node => {
      if (node.key === targetKey) return { ...node, children }
      if (node.children) return { ...node, children: updateTreeData(node.children, targetKey, children) }
      return node
    })
  }

  const GisCatalogPanel = observer(function GisCatalogPanel() {
    const { rootStore, viewerRef } = useStores()
    const gisStore = rootStore.gisStore
    const containerRef = useRef(null)
    const [isResizing, setIsResizing] = useState(false)

    const [treeData, setTreeData] = useState([])
    const [checkedKeys, setCheckedKeys] = useState([])
    const [loading, setLoading] = useState(false)
    const [popoverOpen, setPopoverOpen] = useState(false)
    const [showAttrModal, setShowAttrModal] = useState(false)
    const [attrData, setAttrData] = useState([])
    const [attrLoading, setAttrLoading] = useState(false)

    // 初始宽度
    const setPanelWidthVar = useCallback((px) => {
      const el = containerRef.current
      if (el) el.style.setProperty('--leftCatalogWidth', `${px}px`)
    }, [])

    useEffect(() => {
      let w = 240
      try {
        const raw = window.localStorage.getItem(WIDTH_KEY)
        const n = raw ? parseInt(raw, 10) : NaN
        if (!Number.isNaN(n)) w = n
      } catch { /* ignore */ }
      setPanelWidthVar(clamp(w, 180, 400))
    }, [setPanelWidthVar])

    // Resize handle（右侧边缘拖拽）
    const onStartResize = useCallback((ev) => {
      ev.preventDefault()
      ev.stopPropagation()
      setIsResizing(true)
      const startX = ev.clientX
      const el = containerRef.current
      const startWidth = el
        ? parseInt(getComputedStyle(el).getPropertyValue('--leftCatalogWidth') || '240', 10)
        : 240
      const onMove = (e) => {
        const dx = e.clientX - startX
        const next = clamp(startWidth + dx, 180, 400)
        setPanelWidthVar(next)
        try { window.localStorage.setItem(WIDTH_KEY, String(next)) } catch { /* ignore */ }
      }
      const onUp = () => {
        setIsResizing(false)
        window.removeEventListener('mousemove', onMove, true)
        window.removeEventListener('mouseup', onUp, true)
      }
      window.addEventListener('mousemove', onMove, true)
      window.addEventListener('mouseup', onUp, true)
    }, [setPanelWidthVar])

    // 加载文件夹
    const fetchFolder = useCallback(async (folderUrl) => {
      if (!folderUrl) return
      setLoading(true)
      setTreeData([])
      setCheckedKeys([])
      try {
        const proxyUrl = `/api/gis/proxy?url=${encodeURIComponent(folderUrl + '?f=json')}`
        const resp = await fetch(proxyUrl)
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        const data = await resp.json()
        const services = Array.isArray(data.services) ? data.services : []
        if (services.length === 0) throw new Error('该文件夹下没有服务')
        const nodes = services.map((svc, i) => ({
          key: `svc:${i}`,
          title: `${svc.name.split('/').pop()} (${svc.type})`,
          serviceUrl: buildServiceUrl(folderUrl, svc.name, svc.type),
          layerId: null,
          isLeaf: false,
        }))
        setTreeData(nodes)
        gisStore.addLog('browse', `加载目录: ${folderUrl} → ${services.length} 个服务`)
      } catch (err) {
        message.error(`加载目录失败: ${err.message}`)
      } finally {
        setLoading(false)
      }
    }, [gisStore])

    // URL 变化时重新加载
    useEffect(() => {
      if (gisStore.catalogServiceUrl) fetchFolder(gisStore.catalogServiceUrl)
    }, [gisStore.catalogServiceUrl, fetchFolder])

    // 懒加载图层
    const loadData = useCallback(async (node) => {
      if (node.children) return
      const proxyUrl = `/api/gis/proxy?url=${encodeURIComponent(node.serviceUrl + '?f=json')}`
      const resp = await fetch(proxyUrl)
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const data = await resp.json()
      const rawLayers = Array.isArray(data.layers) ? data.layers : []
      const svcIndex = node.key.split(':')[1]
      const children = rawLayers
        .filter(l => !l.subLayerIds || l.subLayerIds.length === 0)
        .map(l => ({
          key: `lyr:${svcIndex}:${l.id}`,
          title: `Layer ${l.id} — ${l.name}`,
          serviceUrl: node.serviceUrl,
          layerId: l.id,
          isLeaf: true,
        }))
      setTreeData(prev => updateTreeData(prev, node.key, children))
    }, [])

    // 获取已勾选的图层节点（只收 isLeaf 节点）
    const getCheckedLayers = useCallback(() => {
      const result = []
      const traverse = (nodes) => {
        nodes.forEach(n => {
          if (n.isLeaf && checkedKeys.includes(n.key)) {
            result.push({ serviceUrl: n.serviceUrl, layerId: n.layerId, title: n.title })
          }
          if (n.children) traverse(n.children)
        })
      }
      traverse(treeData)
      return result
    }, [checkedKeys, treeData])

    // TODO: 调图和属性查询在 Task 4/5 实现
    const handleDiaotuAll = () => {}
    const handleDiaotuBbox = () => {}
    const handleDiaotuPolygon = () => {}
    const handleAttrQuery = () => {}

    const popoverContent = (
      <div className={s.popoverMenu}>
        <div className={s.popoverItem} onClick={handleDiaotuAll}>
          <span className={s.popoverIcon}>🌐</span>
          <div><div className={s.popoverLabel}>全部范围</div><div className={s.popoverHint}>加载全部要素</div></div>
        </div>
        <div className={s.popoverItem} onClick={handleDiaotuBbox}>
          <span className={s.popoverIcon}>⬚</span>
          <div><div className={s.popoverLabel}>框选范围</div><div className={s.popoverHint}>两点矩形</div></div>
        </div>
        <div className={s.popoverItem} onClick={handleDiaotuPolygon}>
          <span className={s.popoverIcon}>⬡</span>
          <div><div className={s.popoverLabel}>任意多边形</div><div className={s.popoverHint}>逐点，双击收口</div></div>
        </div>
      </div>
    )

    return (
      <div className={s.panel} ref={containerRef}>
        <div
          className={`${s.resizer} ${isResizing ? s.resizerActive : ''}`}
          onMouseDown={onStartResize}
          title="拖拽调整面板宽度"
        />

        <div className={s.header}>
          <div>
            <div className={s.title}>📂 空间数据库</div>
            <div className={s.url} title={gisStore.catalogServiceUrl}>
              {gisStore.catalogServiceUrl}
            </div>
          </div>
          <div className={s.headerActions}>
            <button
              className={s.iconBtn}
              onClick={() => fetchFolder(gisStore.catalogServiceUrl)}
              title="刷新"
            >↺</button>
            <button
              className={s.iconBtn}
              onClick={() => gisStore.closeCatalog()}
              title="关闭"
            >✕</button>
          </div>
        </div>

        <div className={s.treeWrap}>
          {loading
            ? <div className={s.centered}><Spin /></div>
            : <Tree
                checkable
                loadData={loadData}
                treeData={treeData}
                checkedKeys={checkedKeys}
                onCheck={(keys) => setCheckedKeys(Array.isArray(keys) ? keys : keys.checked)}
              />
          }
        </div>

        <div className={s.footer}>
          <Popover
            content={popoverContent}
            trigger="click"
            open={popoverOpen}
            onOpenChange={setPopoverOpen}
            placement="topLeft"
          >
            <Button
              type="primary"
              size="small"
              style={{ flex: 1 }}
              disabled={!checkedKeys.length || !!gisStore.drawingMode}
            >
              📐 调图
            </Button>
          </Popover>
          <Button
            size="small"
            style={{ flex: 1 }}
            onClick={handleAttrQuery}
            disabled={!checkedKeys.length}
          >
            🔍 属性查询
          </Button>
        </div>

        <Modal
          title="属性查询结果"
          open={showAttrModal}
          onCancel={() => setShowAttrModal(false)}
          footer={null}
          width={900}
          styles={{ body: { maxHeight: '70vh', overflow: 'auto' } }}
        >
          {attrLoading
            ? <div style={{ textAlign: 'center', padding: 32 }}><Spin /></div>
            : attrData.length === 0
              ? null
              : attrData.length === 1
                ? <Table columns={attrData[0].columns} dataSource={attrData[0].rows} rowKey="_key" size="small" scroll={{ x: true }} pagination={{ pageSize: 20 }} />
                : <Tabs items={attrData.map((d, i) => ({
                    key: String(i), label: d.layerName,
                    children: <Table columns={d.columns} dataSource={d.rows} rowKey="_key" size="small" scroll={{ x: true }} pagination={{ pageSize: 20 }} />,
                  }))} />
          }
        </Modal>
      </div>
    )
  })

  export default GisCatalogPanel
  ```

- [ ] **Step 3: 挂载到 App.jsx，验证树能展开**

  在 `src/App.jsx` 顶部 import 区加入：
  ```jsx
  import GisCatalogPanel from './components/GisService/GisCatalogPanel'
  ```

  在 `const { appStore, editorStore } = rootStore` 之后加：
  ```jsx
  const { gisStore } = rootStore
  ```

  在 `<div className={s.mainRow}>` 的**第一个子元素位置**插入：
  ```jsx
  {gisStore.catalogOpen && <GisCatalogPanel />}
  ```

  完整的 `mainRow` 变成：
  ```jsx
  <div className={s.mainRow}>
    {gisStore.catalogOpen && <GisCatalogPanel />}
    <div className={s.centerCol}>
      <div className={s.appCanvasWrap}>
        <CanvasArea />
        {!editorStore.isDrawingMode && <CompareResultPanel />}
      </div>
      {editorStore.isDrawingMode && <BottomDock />}
      {editorStore.isDrawingMode && <StatusBar />}
    </div>
    <div style={disabledStyle}>
      <RightSidebar />
    </div>
  </div>
  ```

- [ ] **Step 4: DevTools 验证树展示**

  ```js
  const store = window.__odaUi?.rootStore?.gisStore
  store.openCatalog('http://106.14.254.175:6081/arcgis/rest/services/upda/')
  // 期望：左侧出现"空间数据库"面板，加载后显示 china (MapServer) 等服务节点
  // 展开服务节点，期望懒加载图层列表
  ```

- [ ] **Step 5: 提交**

  ```bash
  git add src/components/GisService/GisCatalogPanel.jsx \
          src/components/GisService/GisCatalogPanel.module.css \
          src/App.jsx
  git commit -m "feat(gis): add GisCatalogPanel with ArcGIS folder tree and lazy-load layers"
  ```

---

## Task 4：调图 Popover — 全部 / 框选 / 多边形

**Files:**
- Modify: `src/components/GisService/GisCatalogPanel.jsx`

  用下面三个完整实现替换 Task 3 里的三个空函数 `handleDiaotuAll / handleDiaotuBbox / handleDiaotuPolygon`：

- [ ] **Step 1: 实现 handleDiaotuAll**

  ```jsx
  const handleDiaotuAll = useCallback(() => {
    setPopoverOpen(false)
    const layers = getCheckedLayers()
    if (!layers.length) { message.warning('请先勾选图层'); return }
    const viewer = viewerRef.current
    if (!viewer) return
    layers.forEach(l => {
      viewer.execute('GIS_LOAD_FEATURES', [l.serviceUrl, String(l.layerId)])
    })
    message.success(`调图（全部）：${layers.length} 个图层`)
  }, [getCheckedLayers, viewerRef])
  ```

- [ ] **Step 2: 实现 handleDiaotuBbox（复用 startAreaPick）**

  ```jsx
  const handleDiaotuBbox = useCallback(() => {
    setPopoverOpen(false)
    const layers = getCheckedLayers()
    if (!layers.length) { message.warning('请先勾选图层'); return }
    const viewer = viewerRef.current
    if (!viewer) return
    gisStore.setDrawingMode('bbox')
    message.info('请在画布上拖拽框选范围，ESC 取消', 3)
    viewer.startAreaPick(({ bounds }) => {
      gisStore.setDrawingMode(null)
      layers.forEach(l => {
        viewer.execute('GIS_LOAD_FEATURES', [
          l.serviceUrl, String(l.layerId),
          String(bounds.minX), String(bounds.minY),
          String(bounds.maxX), String(bounds.maxY),
        ])
      })
      message.success(`调图（框选）：${layers.length} 个图层`)
    })
  }, [getCheckedLayers, gisStore, viewerRef])
  ```

- [ ] **Step 3: 实现 handleDiaotuPolygon（使用新增的 startPolygonPick）**

  ```jsx
  const handleDiaotuPolygon = useCallback(() => {
    setPopoverOpen(false)
    const layers = getCheckedLayers()
    if (!layers.length) { message.warning('请先勾选图层'); return }
    const viewer = viewerRef.current
    if (!viewer) return
    gisStore.setDrawingMode('polygon')
    message.info('逐点单击绘制多边形，双击收口，ESC 取消', 4)
    viewer.startPolygonPick((vertices) => {
      gisStore.setDrawingMode(null)
      const points = vertices.map(v => `${v.x},${v.y}`).join(';')
      layers.forEach(l => {
        viewer.execute('GIS_LOAD_FEATURES', [l.serviceUrl, String(l.layerId), points])
      })
      message.success(`调图（多边形）：${layers.length} 个图层`)
    })
  }, [getCheckedLayers, gisStore, viewerRef])
  ```

- [ ] **Step 4: 在组件内新增 ESC 取消绘制模式的 useEffect**

  在 `loadData` 的 `useCallback` 之后插入：

  ```jsx
  // ESC 取消绘制模式
  useEffect(() => {
    const onKey = (ev) => {
      if (ev.key !== 'Escape' || !gisStore.drawingMode) return
      const viewer = viewerRef.current
      if (gisStore.drawingMode === 'bbox') viewer?.cancelAreaPick?.()
      if (gisStore.drawingMode === 'polygon') viewer?.cancelPolygonPick?.()
      gisStore.setDrawingMode(null)
      message.info('已取消')
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [gisStore, viewerRef])
  ```

- [ ] **Step 5: 手动验证调图**

  1. `store.openCatalog('http://106.14.254.175:6081/arcgis/rest/services/upda/')`
  2. 展开服务节点，勾选一个图层
  3. 点击「调图」→ 选「框选范围」→ 画布拖拽 → 观察橙红矩形 overlay 正常出现
  4. 松开鼠标 → DevTools Network 看到 `GIS_LOAD_FEATURES` 命令被调用（或 Console 无报错）
  5. 按 ESC → overlay 清除，`gisStore.drawingMode` 变回 null

- [ ] **Step 6: 提交**

  ```bash
  git add src/components/GisService/GisCatalogPanel.jsx
  git commit -m "feat(gis): implement 调图 popover with 全部/框选/多边形 canvas interaction"
  ```

---

## Task 5：属性查询 Modal

**Files:**
- Modify: `src/components/GisService/GisCatalogPanel.jsx`

  用下面的完整实现替换 Task 3 里的空函数 `handleAttrQuery`：

- [ ] **Step 1: 实现 handleAttrQuery**

  ```jsx
  const handleAttrQuery = useCallback(async () => {
    const layers = getCheckedLayers()
    if (!layers.length) { message.warning('请先勾选图层'); return }
    setShowAttrModal(true)
    setAttrLoading(true)
    setAttrData([])
    try {
      const results = await Promise.all(layers.map(async (l) => {
        const queryUrl = `${l.serviceUrl}/${l.layerId}/query` +
          `?where=1%3D1&outFields=*&f=json&resultRecordCount=500`
        const proxyUrl = `/api/gis/proxy?url=${encodeURIComponent(queryUrl)}`
        const resp = await fetch(proxyUrl)
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        const data = await resp.json()
        const columns = (data.fields || []).map(f => ({
          title: f.alias || f.name,
          dataIndex: f.name,
          key: f.name,
          ellipsis: true,
          width: 120,
        }))
        const rows = (data.features || []).map((f, i) => ({ ...f.attributes, _key: i }))
        return { layerName: l.title, columns, rows }
      }))
      setAttrData(results)
    } catch (err) {
      message.error(`属性查询失败: ${err.message}`)
      setShowAttrModal(false)
    } finally {
      setAttrLoading(false)
    }
  }, [getCheckedLayers])
  ```

- [ ] **Step 2: 手动验证属性查询**

  1. 勾选一个图层
  2. 点击「🔍 属性查询」
  3. Modal 弹出，显示 Spin，随后出现属性表（OBJECTID、NAME、AREA 等字段）
  4. 勾选多个图层时，Modal 内显示 Tabs 切换不同图层结果
  5. 期望：网络请求通过 `/api/gis/proxy` 成功返回，无 CORS 报错

- [ ] **Step 3: 提交**

  ```bash
  git add src/components/GisService/GisCatalogPanel.jsx
  git commit -m "feat(gis): implement 属性查询 modal with FeatureServer /query + Ant Table"
  ```

---

## Task 6：GisServiceTab — 预置服务自动触发目录面板

**Files:**
- Modify: `src/components/GisService/GisServiceTab.jsx`

- [ ] **Step 1: 在文件顶部（import 之后，组件函数之前）新增辅助函数**

  ```js
  // 检测文件夹型 URL（无 MapServer / FeatureServer 后缀）
  function isFolderUrl(url) {
    return !!url && !url.includes('MapServer') && !url.includes('FeatureServer')
  }
  ```

- [ ] **Step 2: 在 handlePresetClick 的 useCallback 函数体最前面插入分支**

  找到：
  ```js
  const handlePresetClick = useCallback(async ({ key }) => {
    const svc = gisStore.presetServices[Number(key)]
    if (!svc) return
    gisStore.addService(svc)
    gisStore.setConnectionState('connected')
    const viewer = viewerRef.current
    if (!viewer) return
    if (!viewer.isDatabaseOpen) viewer.createNewFile()
    const hide = message.loading(`连接 ${svc.name} 中...`, 0)
  ```

  在 `if (!svc) return` 之后，原有逻辑之前，插入：

  ```js
  // 文件夹型 URL：打开目录面板而非直接加载底图
  if (isFolderUrl(svc.featureServerUrl)) {
    gisStore.addService(svc)
    gisStore.setConnectionState('connected')
    gisStore.openCatalog(svc.featureServerUrl)
    message.success(`已连接: ${svc.name}，目录加载中…`)
    return
  }
  ```

- [ ] **Step 3: 端到端验证**

  1. 启动 dev server：`cd DrawingWebApp && npm run dev`
  2. 打开应用，切换到「GIS 服务」Ribbon Tab
  3. 点击「常用服务」下拉 → 选择「东莞规划地理信息」
  4. **期望**：左侧面板自动弹出，标题"📂 空间数据库"，加载后显示 `china (MapServer)` 服务节点
  5. 展开 `china` → 显示图层列表
  6. 勾选图层 → 「调图」按钮激活
  7. 选「框选范围」→ 画布出现十字样式，拖拽出橙红矩形，松手后命令被调用
  8. 选「任意多边形」→ 逐点点击，蓝色路径出现，双击收口，命令被调用
  9. 「属性查询」→ Modal 展示属性表
  10. 点击面板右上角「✕」→ 面板关闭，画布恢复全宽
  11. 点击「绿建科技苏州内网测试」（非文件夹 URL）→ 原有底图加载流程不受影响

- [ ] **Step 4: 提交**

  ```bash
  git add src/components/GisService/GisServiceTab.jsx
  git commit -m "feat(gis): auto-open catalog panel for folder-type preset services"
  ```

---

## 自查：Spec 覆盖检查

| Spec 要求 | 对应 Task |
|---|---|
| 连接文件夹 URL 后自动展开目录树 | Task 6 Step 2 |
| 根节点"空间数据库"，遍历所有 Services | Task 3 Step 2 (fetchFolder) |
| 深树：展开服务节点懒加载图层 | Task 3 Step 2 (loadData) |
| CheckBox 复选框 | Task 3 Step 2 (`checkable`) |
| 左侧固定面板，宽度可拖拽 | Task 3 Step 1/2 (resize handle) |
| 调图按钮 + Popover 三选项 | Task 4 |
| 框选复用 startAreaPick | Task 4 Step 2 |
| 多边形新增 startPolygonPick | Task 2 |
| ESC 取消绘制模式 | Task 4 Step 4 |
| 属性查询 Modal Table | Task 5 |
| GisStore 新增三字段 | Task 1 |
| 非文件夹 URL 原有流程不变 | Task 6 Step 2（isFolderUrl 分支仅拦截文件夹） |

## 相关笔记

- [[Legend Analysis Redesign Implementation Plan]]
- [[GIS 导入实体类型透传 — 实现计划]]
- [[quzhen 审查批注功能同步 Implementation Plan]]
- [[plans]]
- [[GIS File Import Implementation Plan]]
- [[UAOdcadCore GIS Service Implementation Plan]]
- [[DWG 导出 GIS 按 CAD 图层过滤 — 实施计划]]
- [[WASM License Gate Implementation Plan]]
