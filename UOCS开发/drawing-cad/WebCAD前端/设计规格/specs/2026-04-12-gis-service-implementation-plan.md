# GIS服务后续实施 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 GIS 服务 UI Shell 升级为完整组件体系：独立组件拆分 + MobX 状态管理 + DrawingWeb WASM 桥接命令桩。

**Architecture:** GisServiceTab 从 ReviewRibbon.jsx 内联提取为 `src/components/GisService/` 独立目录，8 个组件文件各自管理一个弹窗/面板。GisStore（MobX）集中管理 GIS 连接、图层、同步状态，注入 RootStore。DrawingWeb 侧新建 GisCommands.h/cpp 注册 6 个桩命令，通过 EM_ASM 回调 JS 窗口函数。

**Tech Stack:** React 19, MobX, Ant Design (Modal/Drawer/Form/Input/Select/Table/Timeline), Emscripten (C++17), OdEdCommand

**Design Spec:** `docs/specs/2026-04-12-gis-service-implementation-design.md`

---

## File Structure

| 文件 | 操作 | 职责 |
|------|------|------|
| `src/stores/GisStore.js` | 新建 | GIS 状态管理（连接、图层、同步、日志） |
| `src/stores/RootStore.js` | 修改 | 注入 gisStore |
| `src/components/GisService/GisServiceTab.jsx` | 新建 | 主组件（从 ReviewRibbon 提取 + 集成弹窗/面板） |
| `src/components/GisService/AddServiceModal.jsx` | 新建 | "添加服务"弹窗 |
| `src/components/GisService/ServiceBrowser.jsx` | 新建 | "浏览目录"Drawer 面板 |
| `src/components/GisService/AuthManager.jsx` | 新建 | "认证管理"弹窗 |
| `src/components/GisService/StyleMappingModal.jsx` | 新建 | "样式映射"配置弹窗 |
| `src/components/GisService/ExportGisModal.jsx` | 新建 | "导出GIS"弹窗 |
| `src/components/GisService/SyncStatusPanel.jsx` | 新建 | "同步状态"Drawer 面板 |
| `src/components/GisService/GisLogPanel.jsx` | 新建 | "操作日志"Drawer 面板 |
| `src/components/Ribbon/ReviewRibbon.jsx` | 修改 | 删除内联 GisServiceTab，改为 import |
| `DrawingWeb/GisCommands.h` | 新建 | 6 个 GIS 命令类声明 |
| `DrawingWeb/GisCommands.cpp` | 新建 | 桩实现（printf + EM_ASM 回调） |
| `DrawingWeb/CadCore.cpp` | 修改 | 注册 GIS 命令到命令栈 |
| `DrawingWeb/CMakeLists.txt` | 修改 | 添加 GisCommands.cpp 源文件 |

---

### Task 1: 创建 GisStore

**Files:**
- Create: `src/stores/GisStore.js`
- Modify: `src/stores/RootStore.js`

- [ ] **Step 1: 创建 GisStore.js**

创建 `src/stores/GisStore.js`：

```js
import { makeAutoObservable } from 'mobx'

class GisStore {
  connectionState = 'disconnected'  // 'disconnected' | 'connecting' | 'connected'
  activeServices = []
  presetServices = [
    {
      name: '东莞规划地理信息',
      mapServerUrl: 'http://kjgh.dg:30088/arcgis/rest/services/DG_GHDT/MapServer',
      featureServerUrl: 'http://kjgh.dg:30088/arcgis/rest/services/DG_GHDT/FeatureServer',
      srs: 'EPSG:4526',
    },
  ]
  mapImageLayers = []
  featureLayers = []
  syncStatus = { modified: [], pending: [], conflicts: [] }
  coordinateInfo = { dwgCrs: '', gisCrs: '', bridgeStatus: 'unknown' }
  operationLog = []

  constructor(rootStore) {
    this.rootStore = rootStore
    makeAutoObservable(this, { rootStore: false })
  }

  setConnectionState(state) {
    this.connectionState = state
  }

  addService(service) {
    this.activeServices.push(service)
    this.addLog('connect', `连接服务: ${service.name || service.url}`)
  }

  removeService(index) {
    const removed = this.activeServices.splice(index, 1)
    if (removed.length) this.addLog('disconnect', `断开服务: ${removed[0].name || removed[0].url}`)
  }

  clearServices() {
    this.activeServices = []
    this.connectionState = 'disconnected'
    this.addLog('disconnect', '断开所有服务')
  }

  addMapImageLayer(layer) {
    this.mapImageLayers.push(layer)
    this.addLog('load', `加载底图: ${layer.name || layer.url}`)
  }

  removeMapImageLayer(index) {
    const removed = this.mapImageLayers.splice(index, 1)
    if (removed.length) this.addLog('remove', `移除底图: ${removed[0].name || removed[0].url}`)
  }

  addFeatureLayer(layer) {
    this.featureLayers.push(layer)
    this.addLog('load', `加载要素图层: ${layer.name || layer.id}`)
  }

  removeFeatureLayer(index) {
    this.featureLayers.splice(index, 1)
  }

  setSyncStatus(status) {
    this.syncStatus = { ...this.syncStatus, ...status }
  }

  setCoordinateInfo(info) {
    this.coordinateInfo = { ...this.coordinateInfo, ...info }
  }

  addLog(type, detail) {
    this.operationLog.unshift({
      id: Date.now(),
      type,
      detail,
      timestamp: new Date().toISOString(),
    })
  }

  clearLog() {
    this.operationLog = []
  }
}

export default GisStore
```

- [ ] **Step 2: 修改 RootStore.js 注入 gisStore**

在 `src/stores/RootStore.js` 中添加：

第 1 行区域添加 import：
```js
import GisStore from './GisStore'
```

在 constructor 中 `this.analysisStore = new AnalysisStore(this)` 后添加：
```js
    this.gisStore = new GisStore(this)
```

- [ ] **Step 3: 验证语法**

Run: `npx eslint src/stores/GisStore.js src/stores/RootStore.js --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 4: Commit**

```bash
git add src/stores/GisStore.js src/stores/RootStore.js
git commit -m "feat: add GisStore MobX store and inject into RootStore"
```

---

### Task 2: 创建子组件 — AddServiceModal

**Files:**
- Create: `src/components/GisService/AddServiceModal.jsx`

- [ ] **Step 1: 创建 AddServiceModal.jsx**

```jsx
import { useState } from 'react'
import { Modal, Input, Radio, Form, message } from 'antd'

function AddServiceModal({ open, onClose, gisStore, viewerRef }) {
  const [url, setUrl] = useState('')
  const [serviceType, setServiceType] = useState('MapServer')

  const handleOk = () => {
    if (!url.trim()) {
      message.warning('请输入服务 URL')
      return
    }
    const svc = { url: url.trim(), type: serviceType, name: url.trim().split('/').slice(-2, -1)[0] || 'GIS服务' }
    gisStore.addService(svc)
    gisStore.setConnectionState('connected')

    if (viewerRef?.current) {
      const cmd = serviceType === 'MapServer' ? 'GIS_LOAD_MAP_IMAGE' : 'GIS_LOAD_FEATURES'
      viewerRef.current.execute(cmd, [url.trim()])
    }

    setUrl('')
    onClose()
  }

  return (
    <Modal title="添加 GIS 服务" open={open} onOk={handleOk} onCancel={onClose}
      okText="连接" cancelText="取消" destroyOnClose>
      <Form layout="vertical" style={{ marginTop: 16 }}>
        <Form.Item label="服务类型">
          <Radio.Group value={serviceType} onChange={e => setServiceType(e.target.value)}>
            <Radio value="MapServer">MapServer（影像底图）</Radio>
            <Radio value="FeatureServer">FeatureServer（矢量要素）</Radio>
          </Radio.Group>
        </Form.Item>
        <Form.Item label="REST URL">
          <Input placeholder="http://server/arcgis/rest/services/.../MapServer"
            value={url} onChange={e => setUrl(e.target.value)} onPressEnter={handleOk} />
        </Form.Item>
      </Form>
    </Modal>
  )
}

export default AddServiceModal
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/AddServiceModal.jsx
git commit -m "feat: add AddServiceModal component for GIS service URL input"
```

---

### Task 3: 创建子组件 — ServiceBrowser

**Files:**
- Create: `src/components/GisService/ServiceBrowser.jsx`

- [ ] **Step 1: 创建 ServiceBrowser.jsx**

```jsx
import { useState } from 'react'
import { Drawer, Tree, Button, Input, Empty, message } from 'antd'

function ServiceBrowser({ open, onClose, gisStore, viewerRef }) {
  const [endpoint, setEndpoint] = useState('')
  const [treeData, setTreeData] = useState([])
  const [checkedKeys, setCheckedKeys] = useState([])
  const [loading, setLoading] = useState(false)

  const handleBrowse = async () => {
    if (!endpoint.trim()) { message.warning('请输入 ArcGIS Server REST 端点 URL'); return }
    setLoading(true)
    // 桩：模拟加载服务目录树
    setTreeData([
      {
        title: endpoint.split('/').pop() || '服务根目录',
        key: 'root',
        children: [
          { title: 'Layer 0 — 用地规划', key: '0', isLeaf: true },
          { title: 'Layer 1 — 道路红线', key: '1', isLeaf: true },
          { title: 'Layer 2 — 建筑轮廓', key: '2', isLeaf: true },
        ],
      },
    ])
    setLoading(false)
    gisStore.addLog('browse', `浏览目录: ${endpoint.trim()}`)
  }

  const handleLoad = () => {
    if (!checkedKeys.length) { message.warning('请勾选至少一个图层'); return }
    checkedKeys.forEach(key => {
      if (key === 'root') return
      gisStore.addFeatureLayer({ id: key, name: `Layer ${key}`, url: endpoint.trim() })
      if (viewerRef?.current) {
        viewerRef.current.execute('GIS_LOAD_FEATURES', [endpoint.trim(), key])
      }
    })
    message.success(`已加载 ${checkedKeys.filter(k => k !== 'root').length} 个图层`)
    onClose()
  }

  return (
    <Drawer title="浏览 GIS 服务目录" open={open} onClose={onClose} width={400}
      extra={<Button type="primary" onClick={handleLoad} disabled={!checkedKeys.length}>加载选中图层</Button>}>
      <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
        <Input placeholder="http://server/arcgis/rest/services" value={endpoint}
          onChange={e => setEndpoint(e.target.value)} onPressEnter={handleBrowse} style={{ flex: 1 }} />
        <Button onClick={handleBrowse} loading={loading}>浏览</Button>
      </div>
      {treeData.length > 0 ? (
        <Tree checkable treeData={treeData} checkedKeys={checkedKeys}
          onCheck={setCheckedKeys} defaultExpandAll />
      ) : (
        <Empty description="输入 REST 端点后点击浏览" />
      )}
    </Drawer>
  )
}

export default ServiceBrowser
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/ServiceBrowser.jsx
git commit -m "feat: add ServiceBrowser drawer for GIS layer tree browsing"
```

---

### Task 4: 创建子组件 — AuthManager

**Files:**
- Create: `src/components/GisService/AuthManager.jsx`

- [ ] **Step 1: 创建 AuthManager.jsx**

```jsx
import { useState } from 'react'
import { Modal, Tabs, Form, Input, Button, message } from 'antd'

function AuthManager({ open, onClose, gisStore }) {
  const [authType, setAuthType] = useState('token')
  const [token, setToken] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSave = () => {
    if (authType === 'token' && !token.trim()) { message.warning('请输入 Token'); return }
    if (authType === 'credentials' && (!username.trim() || !password.trim())) {
      message.warning('请输入用户名和密码'); return
    }
    gisStore.addLog('auth', `保存${authType === 'token' ? 'Token' : '用户名/密码'}认证`)
    message.success('认证信息已保存')
    onClose()
  }

  const items = [
    {
      key: 'token',
      label: 'Token 认证',
      children: (
        <Form layout="vertical">
          <Form.Item label="ArcGIS Token">
            <Input.TextArea rows={3} placeholder="粘贴 Token..." value={token}
              onChange={e => setToken(e.target.value)} />
          </Form.Item>
        </Form>
      ),
    },
    {
      key: 'credentials',
      label: '用户名/密码',
      children: (
        <Form layout="vertical">
          <Form.Item label="用户名">
            <Input value={username} onChange={e => setUsername(e.target.value)} />
          </Form.Item>
          <Form.Item label="密码">
            <Input.Password value={password} onChange={e => setPassword(e.target.value)} />
          </Form.Item>
        </Form>
      ),
    },
  ]

  return (
    <Modal title="认证管理" open={open} onOk={handleSave} onCancel={onClose}
      okText="保存" cancelText="取消" destroyOnClose>
      <Tabs activeKey={authType} onChange={setAuthType} items={items} />
    </Modal>
  )
}

export default AuthManager
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/AuthManager.jsx
git commit -m "feat: add AuthManager modal for GIS token/credential management"
```

---

### Task 5: 创建子组件 — StyleMappingModal

**Files:**
- Create: `src/components/GisService/StyleMappingModal.jsx`

- [ ] **Step 1: 创建 StyleMappingModal.jsx**

```jsx
import { useState } from 'react'
import { Modal, Table, Input, Select, message } from 'antd'

const DEFAULT_MAPPINGS = [
  { key: 'point', gisType: 'Point', dwgEntity: 'OdDbPoint', layer: 'GIS_Points', color: '黄色 (2)', linetype: 'Continuous' },
  { key: 'line', gisType: 'LineString', dwgEntity: 'OdDbPolyline', layer: 'GIS_Lines', color: '绿色 (3)', linetype: 'Continuous' },
  { key: 'polygon', gisType: 'Polygon', dwgEntity: 'OdDbHatch', layer: 'GIS_Polygons', color: '青色 (4)', linetype: 'Continuous' },
]

function StyleMappingModal({ open, onClose, gisStore }) {
  const [mappings, setMappings] = useState(DEFAULT_MAPPINGS)

  const updateMapping = (key, field, value) => {
    setMappings(prev => prev.map(m => m.key === key ? { ...m, [field]: value } : m))
  }

  const handleOk = () => {
    gisStore.addLog('config', '更新样式映射配置')
    message.success('样式映射已保存')
    onClose()
  }

  const columns = [
    { title: 'GIS 几何类型', dataIndex: 'gisType', width: 110 },
    { title: 'DWG 实体', dataIndex: 'dwgEntity', width: 120 },
    {
      title: '目标图层', dataIndex: 'layer', width: 140,
      render: (val, row) => <Input size="small" value={val} onChange={e => updateMapping(row.key, 'layer', e.target.value)} />,
    },
    {
      title: '颜色', dataIndex: 'color', width: 130,
      render: (val, row) => (
        <Select size="small" value={val} onChange={v => updateMapping(row.key, 'color', v)} style={{ width: '100%' }}
          options={['红色 (1)', '黄色 (2)', '绿色 (3)', '青色 (4)', '蓝色 (5)', '品红 (6)', '白色 (7)'].map(c => ({ label: c, value: c }))} />
      ),
    },
    {
      title: '线型', dataIndex: 'linetype', width: 130,
      render: (val, row) => (
        <Select size="small" value={val} onChange={v => updateMapping(row.key, 'linetype', v)} style={{ width: '100%' }}
          options={['Continuous', 'DASHED', 'CENTER', 'HIDDEN', 'PHANTOM'].map(l => ({ label: l, value: l }))} />
      ),
    },
  ]

  return (
    <Modal title="样式映射配置" open={open} onOk={handleOk} onCancel={onClose}
      okText="保存" cancelText="取消" width={700} destroyOnClose>
      <p style={{ marginBottom: 12, color: '#999', fontSize: 12 }}>设置 GIS 要素 → DWG 实体的图层、颜色、线型映射规则</p>
      <Table dataSource={mappings} columns={columns} pagination={false} size="small" bordered />
    </Modal>
  )
}

export default StyleMappingModal
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/StyleMappingModal.jsx
git commit -m "feat: add StyleMappingModal for GIS-to-DWG style mapping config"
```

---

### Task 6: 创建子组件 — ExportGisModal

**Files:**
- Create: `src/components/GisService/ExportGisModal.jsx`

- [ ] **Step 1: 创建 ExportGisModal.jsx**

```jsx
import { useState } from 'react'
import { Modal, Form, Select, Input, Checkbox, message } from 'antd'

const FORMAT_OPTIONS = [
  { label: 'GeoPackage (.gpkg)', value: 'gpkg' },
  { label: 'Shapefile (.shp)', value: 'shp' },
  { label: 'GeoJSON (.geojson)', value: 'geojson' },
  { label: 'FileGDB (.gdb)', value: 'fgdb' },
]

function ExportGisModal({ open, onClose, gisStore, viewerRef }) {
  const [format, setFormat] = useState('gpkg')
  const [path, setPath] = useState('export')
  const [selectedLayers, setSelectedLayers] = useState([])

  const layerOptions = gisStore.featureLayers.map(l => ({
    label: l.name || `Layer ${l.id}`,
    value: l.id,
  }))

  const handleOk = () => {
    if (!path.trim()) { message.warning('请输入导出路径'); return }
    const layers = selectedLayers.length ? selectedLayers.join(',') : 'all'
    if (viewerRef?.current) {
      viewerRef.current.execute('GIS_EXPORT', [format, path.trim(), layers])
    }
    gisStore.addLog('export', `导出 ${format.toUpperCase()} → ${path.trim()}`)
    message.success('导出任务已提交')
    onClose()
  }

  return (
    <Modal title="导出 GIS 数据" open={open} onOk={handleOk} onCancel={onClose}
      okText="导出" cancelText="取消" destroyOnClose>
      <Form layout="vertical" style={{ marginTop: 16 }}>
        <Form.Item label="输出格式">
          <Select value={format} onChange={setFormat} options={FORMAT_OPTIONS} />
        </Form.Item>
        <Form.Item label="导出路径">
          <Input value={path} onChange={e => setPath(e.target.value)} placeholder="export" />
        </Form.Item>
        {layerOptions.length > 0 && (
          <Form.Item label="选择图层（留空导出全部）">
            <Checkbox.Group options={layerOptions} value={selectedLayers} onChange={setSelectedLayers} />
          </Form.Item>
        )}
      </Form>
    </Modal>
  )
}

export default ExportGisModal
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/ExportGisModal.jsx
git commit -m "feat: add ExportGisModal for GIS format export dialog"
```

---

### Task 7: 创建子组件 — SyncStatusPanel

**Files:**
- Create: `src/components/GisService/SyncStatusPanel.jsx`

- [ ] **Step 1: 创建 SyncStatusPanel.jsx**

```jsx
import { observer } from 'mobx-react-lite'
import { Drawer, List, Tag, Empty } from 'antd'

const TYPE_TAG = {
  modified: { color: 'orange', label: '已修改' },
  pending: { color: 'blue', label: '待推送' },
  conflicts: { color: 'red', label: '冲突' },
}

const SyncStatusPanel = observer(function SyncStatusPanel({ open, onClose, gisStore }) {
  const { modified, pending, conflicts } = gisStore.syncStatus
  const allItems = [
    ...modified.map(item => ({ ...item, _type: 'modified' })),
    ...pending.map(item => ({ ...item, _type: 'pending' })),
    ...conflicts.map(item => ({ ...item, _type: 'conflicts' })),
  ]

  return (
    <Drawer title="同步状态" open={open} onClose={onClose} width={380}>
      <div style={{ marginBottom: 12, display: 'flex', gap: 8 }}>
        <Tag color="orange">已修改 {modified.length}</Tag>
        <Tag color="blue">待推送 {pending.length}</Tag>
        <Tag color="red">冲突 {conflicts.length}</Tag>
      </div>
      {allItems.length > 0 ? (
        <List dataSource={allItems} size="small"
          renderItem={item => (
            <List.Item>
              <Tag color={TYPE_TAG[item._type].color}>{TYPE_TAG[item._type].label}</Tag>
              {item.id || item.name || '未知实体'}
            </List.Item>
          )}
        />
      ) : (
        <Empty description="当前无待同步的要素" />
      )}
    </Drawer>
  )
})

export default SyncStatusPanel
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/SyncStatusPanel.jsx
git commit -m "feat: add SyncStatusPanel drawer for GIS sync status display"
```

---

### Task 8: 创建子组件 — GisLogPanel

**Files:**
- Create: `src/components/GisService/GisLogPanel.jsx`

- [ ] **Step 1: 创建 GisLogPanel.jsx**

```jsx
import { observer } from 'mobx-react-lite'
import { Drawer, Timeline, Tag, Button, Empty } from 'antd'

const TYPE_COLOR = {
  connect: 'green',
  disconnect: 'red',
  load: 'blue',
  remove: 'orange',
  export: 'purple',
  auth: 'cyan',
  config: 'gold',
  browse: 'geekblue',
  push: 'green',
  pull: 'blue',
  error: 'red',
}

const GisLogPanel = observer(function GisLogPanel({ open, onClose, gisStore }) {
  const items = gisStore.operationLog.map(entry => ({
    key: entry.id,
    color: TYPE_COLOR[entry.type] || 'gray',
    children: (
      <>
        <Tag color={TYPE_COLOR[entry.type] || 'default'} style={{ marginRight: 8 }}>{entry.type}</Tag>
        {entry.detail}
        <div style={{ color: '#666', fontSize: 11, marginTop: 2 }}>
          {new Date(entry.timestamp).toLocaleString('zh-CN')}
        </div>
      </>
    ),
  }))

  return (
    <Drawer title="GIS 操作日志" open={open} onClose={onClose} width={420}
      extra={<Button size="small" onClick={() => gisStore.clearLog()} disabled={!gisStore.operationLog.length}>清空</Button>}>
      {items.length > 0 ? (
        <Timeline items={items} />
      ) : (
        <Empty description="暂无操作日志" />
      )}
    </Drawer>
  )
})

export default GisLogPanel
```

- [ ] **Step 2: Commit**

```bash
git add src/components/GisService/GisLogPanel.jsx
git commit -m "feat: add GisLogPanel drawer with operation timeline"
```

---

### Task 9: 创建 GisServiceTab 主组件并替换 ReviewRibbon 内联版

**Files:**
- Create: `src/components/GisService/GisServiceTab.jsx`
- Modify: `src/components/Ribbon/ReviewRibbon.jsx`

- [ ] **Step 1: 创建 GisServiceTab.jsx**

注意：该组件需要从 ReviewRibbon.jsx 中引用 `RvBtn`、`RvGroup`、`Divider`、`I`（图标集）。由于这些目前是 ReviewRibbon.jsx 的内部定义，我们通过 props 传入 `onNotImpl` 和 store/viewer refs，从 ReviewRibbon 导入共享组件。

由于 `RvBtn`、`RvGroup`、`Divider`、`I` 并未从 ReviewRibbon.jsx 导出，GisServiceTab 需要自行导入或内联。最简方案：**在 ReviewRibbon.jsx 中添加 named exports**，然后在 GisServiceTab 中 import。

先在 ReviewRibbon.jsx 的文件末尾 `export default ReviewRibbon` 之前，添加：

```js
export { RvBtn, RvGroup, Divider, I }
```

然后创建 `src/components/GisService/GisServiceTab.jsx`：

```jsx
import { useState, useCallback } from 'react'
import { Dropdown, message } from 'antd'
import { observer } from 'mobx-react-lite'
import { useStores } from '../../context/ViewerContext'
import { RvBtn, RvGroup, Divider, I } from '../Ribbon/ReviewRibbon'
import AddServiceModal from './AddServiceModal'
import ServiceBrowser from './ServiceBrowser'
import AuthManager from './AuthManager'
import StyleMappingModal from './StyleMappingModal'
import ExportGisModal from './ExportGisModal'
import SyncStatusPanel from './SyncStatusPanel'
import GisLogPanel from './GisLogPanel'

const GisServiceTab = observer(function GisServiceTab({ onNotImpl }) {
  const { rootStore, viewerRef } = useStores()
  const gisStore = rootStore.gisStore

  // 弹窗/面板状态
  const [showAddService, setShowAddService] = useState(false)
  const [showBrowser, setShowBrowser] = useState(false)
  const [showAuth, setShowAuth] = useState(false)
  const [showStyleMapping, setShowStyleMapping] = useState(false)
  const [showExport, setShowExport] = useState(false)
  const [showSyncStatus, setShowSyncStatus] = useState(false)
  const [showLog, setShowLog] = useState(false)

  // 常用服务下拉菜单
  const presetMenuItems = gisStore.presetServices.map((svc, i) => ({
    key: String(i),
    label: svc.name,
  }))

  const handlePresetClick = useCallback(({ key }) => {
    const svc = gisStore.presetServices[Number(key)]
    if (!svc) return
    gisStore.addService(svc)
    gisStore.setConnectionState('connected')
    if (viewerRef.current) {
      viewerRef.current.execute('GIS_LOAD_MAP_IMAGE', [svc.mapServerUrl])
    }
    message.success(`已连接: ${svc.name}`)
  }, [gisStore, viewerRef])

  // WASM 桥接操作
  const handleLoadMap = useCallback(() => {
    if (!gisStore.activeServices.length) { message.warning('请先连接 GIS 服务'); return }
    const svc = gisStore.activeServices[0]
    const url = svc.mapServerUrl || svc.url
    if (viewerRef.current) viewerRef.current.execute('GIS_LOAD_MAP_IMAGE', [url])
    gisStore.addMapImageLayer({ name: svc.name, url })
  }, [gisStore, viewerRef])

  const handleRefreshImage = useCallback(() => {
    if (viewerRef.current) viewerRef.current.execute('GIS_LOAD_MAP_IMAGE', ['refresh'])
    gisStore.addLog('load', '刷新影像')
  }, [gisStore, viewerRef])

  const handleRemoveMap = useCallback(() => {
    if (!gisStore.mapImageLayers.length) { message.warning('当前无底图可移除'); return }
    gisStore.removeMapImageLayer(0)
  }, [gisStore])

  const handleLoadFeatures = useCallback(() => {
    if (!gisStore.activeServices.length) { message.warning('请先连接 GIS 服务'); return }
    const svc = gisStore.activeServices[0]
    const url = svc.featureServerUrl || svc.url
    if (viewerRef.current) viewerRef.current.execute('GIS_LOAD_FEATURES', [url, '0'])
    gisStore.addFeatureLayer({ id: '0', name: 'Layer 0', url })
  }, [gisStore, viewerRef])

  const handlePush = useCallback(() => {
    if (viewerRef.current) viewerRef.current.execute('GIS_PUSH_FEATURES', [])
    gisStore.addLog('push', '推送要素修改')
  }, [gisStore, viewerRef])

  const handlePull = useCallback(() => {
    if (viewerRef.current) viewerRef.current.execute('GIS_PULL_FEATURES', [])
    gisStore.addLog('pull', '拉取要素更新')
  }, [gisStore, viewerRef])

  const handleDisconnect = useCallback(() => {
    gisStore.clearServices()
    message.info('已断开所有 GIS 服务')
  }, [gisStore])

  const handleCrsInfo = useCallback(() => {
    if (viewerRef.current) viewerRef.current.execute('GIS_CRS_INFO', [])
    gisStore.addLog('config', '查询坐标系信息')
  }, [gisStore, viewerRef])

  return (
    <>
      <RvGroup label="连接">
        <Dropdown menu={{ items: presetMenuItems, onClick: handlePresetClick }} placement="bottomLeft">
          <span><RvBtn icon={I.gisService} label="常用服务" primary title="从预配置列表快速连接 ArcGIS 服务" /></span>
        </Dropdown>
        <RvBtn icon={I.gisAdd} label="添加服务" title="手动输入 MapServer/FeatureServer REST URL" onClick={() => setShowAddService(true)} />
        <RvBtn icon={I.gisBrowse} label="浏览目录" title="浏览 ArcGIS Server 服务目录并勾选图层" onClick={() => setShowBrowser(true)} />
        <Divider />
        <RvBtn icon={I.gisAuth} label="认证管理" title="管理 Token 认证和用户名/密码凭证" onClick={() => setShowAuth(true)} />
        <RvBtn icon={I.gisDisconnect} label="断开连接" danger title="断开当前 ArcGIS 服务连接" onClick={handleDisconnect} />
      </RvGroup>

      <RvGroup label="地图影像">
        <RvBtn icon={I.gisLoadMap} label="加载底图" primary title="从 MapServer 加载影像底图叠加到视口" onClick={handleLoadMap} />
        <RvBtn icon={I.gisRefresh} label="刷新影像" title="按当前视口范围重新获取影像瓦片" onClick={handleRefreshImage} />
        <RvBtn icon={I.gisOpacity} label="透明度" title="调节底图影像透明度 (0-100%)" onClick={() => onNotImpl('透明度')} />
        <Divider />
        <RvBtn icon={I.gisRemoveMap} label="移除底图" danger title="移除已加载的 GIS 底图影像" onClick={handleRemoveMap} />
      </RvGroup>

      <RvGroup label="要素数据">
        <RvBtn icon={I.gisLoadFeature} label="加载要素" primary title="从 FeatureServer 加载矢量要素到 DWG" onClick={handleLoadFeatures} />
        <RvBtn icon={I.gisAttrQuery} label="属性查询" title="输入 WHERE 条件过滤要素" onClick={() => onNotImpl('属性查询')} />
        <RvBtn icon={I.gisSpatialQuery} label="空间查询" title="框选范围查询要素" onClick={() => onNotImpl('空间查询')} />
        <RvBtn icon={I.gisStyleMap} label="样式映射" amber title="设置要素→DWG 图层/颜色/线型映射规则" onClick={() => setShowStyleMapping(true)} />
        <Divider />
        <RvBtn icon={I.gisPush} label="推送修改" green title="将编辑的要素同步回 FeatureServer" onClick={handlePush} />
        <RvBtn icon={I.gisPull} label="拉取更新" green title="从 FeatureServer 获取最新数据" onClick={handlePull} />
        <RvBtn icon={I.gisSyncStatus} label="同步状态" title="查看已修改/待推送/冲突的要素" onClick={() => setShowSyncStatus(true)} />
      </RvGroup>

      <RvGroup label="工具">
        <RvBtn icon={I.gisCrs} label="坐标系信息" title="查看 DWG 与 GIS 服务坐标系状态" onClick={handleCrsInfo} />
        <RvBtn icon={I.gisExport} label="导出GIS" primary title="导出为 GeoPackage/Shapefile/GeoJSON" onClick={() => setShowExport(true)} />
        <RvBtn icon={I.gisLog} label="操作日志" title="查看 GIS 操作详细日志" onClick={() => setShowLog(true)} />
      </RvGroup>

      {/* 弹窗和面板 */}
      <AddServiceModal open={showAddService} onClose={() => setShowAddService(false)} gisStore={gisStore} viewerRef={viewerRef} />
      <ServiceBrowser open={showBrowser} onClose={() => setShowBrowser(false)} gisStore={gisStore} viewerRef={viewerRef} />
      <AuthManager open={showAuth} onClose={() => setShowAuth(false)} gisStore={gisStore} />
      <StyleMappingModal open={showStyleMapping} onClose={() => setShowStyleMapping(false)} gisStore={gisStore} />
      <ExportGisModal open={showExport} onClose={() => setShowExport(false)} gisStore={gisStore} viewerRef={viewerRef} />
      <SyncStatusPanel open={showSyncStatus} onClose={() => setShowSyncStatus(false)} gisStore={gisStore} />
      <GisLogPanel open={showLog} onClose={() => setShowLog(false)} gisStore={gisStore} />
    </>
  )
})

export default GisServiceTab
```

- [ ] **Step 2: 在 ReviewRibbon.jsx 末尾添加 named exports**

在 `src/components/Ribbon/ReviewRibbon.jsx` 最后一行 `export default ReviewRibbon` 之前，添加：

```js
export { RvBtn, RvGroup, Divider, I }
```

- [ ] **Step 3: 在 ReviewRibbon.jsx 中替换内联 GisServiceTab 为 import**

在文件顶部 import 区域（第 7 行 `import { ColorPicker, RGBColorPicker } from ...` 之后）添加：

```js
import GisServiceTab from '../GisService/GisServiceTab'
```

然后删除 ReviewRibbon.jsx 中的内联 GisServiceTab 函数定义（第 764–804 行，从 `// ===== GIS服务 Tab =====` 到 `}` 闭合花括号之后的空行）。

switch case 行 `case 'GIS服务': return <GisServiceTab onNotImpl={handleNotImpl} />` 无需修改。

- [ ] **Step 4: 验证语法**

Run: `npx eslint src/components/GisService/ src/components/Ribbon/ReviewRibbon.jsx --no-error-on-unmatched-pattern`
Expected: 无错误

- [ ] **Step 5: Commit**

```bash
git add src/components/GisService/GisServiceTab.jsx src/components/Ribbon/ReviewRibbon.jsx
git commit -m "feat: extract GisServiceTab to standalone component with modal/panel integration"
```

---

### Task 10: 创建 WASM 桥接 — GisCommands.h

**Files:**
- Create: `DrawingWeb/GisCommands.h`

注意：此文件在 `DrawingWeb/` 目录下（另一个工作目录 `e:\ODAGitLab\main24.10\DrawingWeb\`）。

- [ ] **Step 1: 创建 GisCommands.h**

```cpp
#pragma once

#include "OdaCommon.h"
#include "Ed/EdCommandStack.h"

class CadCore;

/************************************************************************/
/* GIS 桥接命令 — 桩实现                                                 */
/* 真实功能在另外的 C++ 工程中实现，此处仅注册命令名 + JS 回调              */
/************************************************************************/

class Cmd_GIS_LOAD_MAP_IMAGE : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};

class Cmd_GIS_LOAD_FEATURES : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};

class Cmd_GIS_PUSH_FEATURES : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};

class Cmd_GIS_PULL_FEATURES : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};

class Cmd_GIS_EXPORT : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};

class Cmd_GIS_CRS_INFO : public OdEdCommand
{
public:
  CadCore* m_pCadCore = nullptr;
  static const OdString name();
  const OdString groupName() const;
  const OdString globalName() const;
  void execute(OdEdCommandContext* pCommandContext);
};
```

- [ ] **Step 2: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWeb
git add GisCommands.h
git commit -m "feat: add GIS command class declarations (WASM bridge stubs)"
```

---

### Task 11: 创建 WASM 桥接 — GisCommands.cpp

**Files:**
- Create: `DrawingWeb/GisCommands.cpp`

- [ ] **Step 1: 创建 GisCommands.cpp**

```cpp
#include "GisCommands.h"
#include "DbCommandContext.h"
#include "CadCore.h"
#include <emscripten.h>
#include <string>
#include <codecvt>

// 辅助：OdString → std::string (UTF-8)
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
    OdString url = pIO->getString(L"MapServer URL");
    std::string sUrl = toUtf8(url);

    std::printf("[GIS] GIS_LOAD_MAP_IMAGE: url=%s\n", sUrl.c_str());

    EM_ASM({
        if (typeof window.__onGisLoadProgress === 'function')
            window.__onGisLoadProgress(100);
        if (typeof window.__onGisConnected === 'function')
            window.__onGisConnected(UTF8ToString($0));
    }, sUrl.c_str());
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
    OdString url = pIO->getString(L"FeatureServer URL");
    OdString layerId = pIO->getString(L"Layer ID");
    std::string sUrl = toUtf8(url);
    std::string sLayerId = toUtf8(layerId);

    std::printf("[GIS] GIS_LOAD_FEATURES: url=%s, layerId=%s\n", sUrl.c_str(), sLayerId.c_str());

    EM_ASM({
        if (typeof window.__onGisLoadProgress === 'function')
            window.__onGisLoadProgress(100);
    }, 0);
}

/////////////////////////////////////////////////////////////////////////
// GIS_PUSH_FEATURES
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_PUSH_FEATURES::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_PUSH_FEATURES::name() { return L"GIS_PUSH_FEATURES"; }
const OdString Cmd_GIS_PUSH_FEATURES::globalName() const { return name(); }

void Cmd_GIS_PUSH_FEATURES::execute(OdEdCommandContext* pCmdCtx)
{
    std::printf("[GIS] GIS_PUSH_FEATURES: stub — push modified entities to FeatureServer\n");

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "push", 0);
}

/////////////////////////////////////////////////////////////////////////
// GIS_PULL_FEATURES
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_PULL_FEATURES::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_PULL_FEATURES::name() { return L"GIS_PULL_FEATURES"; }
const OdString Cmd_GIS_PULL_FEATURES::globalName() const { return name(); }

void Cmd_GIS_PULL_FEATURES::execute(OdEdCommandContext* pCmdCtx)
{
    std::printf("[GIS] GIS_PULL_FEATURES: stub — pull latest from FeatureServer\n");

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "pull", 0);
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
    OdString format = pIO->getString(L"Export format");
    OdString path = pIO->getString(L"Export path");
    std::string sFormat = toUtf8(format);
    std::string sPath = toUtf8(path);

    std::printf("[GIS] GIS_EXPORT: format=%s, path=%s\n", sFormat.c_str(), sPath.c_str());

    EM_ASM({
        if (typeof window.__onGisSyncComplete === 'function')
            window.__onGisSyncComplete(UTF8ToString($0), $1);
    }, "export", 0);
}

/////////////////////////////////////////////////////////////////////////
// GIS_CRS_INFO
/////////////////////////////////////////////////////////////////////////
const OdString Cmd_GIS_CRS_INFO::groupName() const { return L"GIS"; }
const OdString Cmd_GIS_CRS_INFO::name() { return L"GIS_CRS_INFO"; }
const OdString Cmd_GIS_CRS_INFO::globalName() const { return name(); }

void Cmd_GIS_CRS_INFO::execute(OdEdCommandContext* pCmdCtx)
{
    std::printf("[GIS] GIS_CRS_INFO: stub — returning placeholder CRS info\n");

    const char* json = "{\"dwgCrs\":\"unknown\",\"gisCrs\":\"EPSG:4326\",\"bridgeStatus\":\"stub\"}";

    EM_ASM({
        if (typeof window.__onGisCrsInfo === 'function')
            window.__onGisCrsInfo(UTF8ToString($0));
    }, json);
}
```

- [ ] **Step 2: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWeb
git add GisCommands.cpp
git commit -m "feat: add GIS command stub implementations with EM_ASM JS callbacks"
```

---

### Task 12: 注册 GIS 命令到 CadCore 并更新 CMakeLists

**Files:**
- Modify: `DrawingWeb/CadCore.cpp` (~line 265-280)
- Modify: `DrawingWeb/CMakeLists.txt` (~line 272)

- [ ] **Step 1: 在 CadCore.cpp 中添加 include 和注册 GIS 命令**

在 `CadCore.cpp` 顶部 `#include "Commands.h"` 后（约第 3–4 行区域）添加：

```cpp
#include "GisCommands.h"
```

在 CadCore 构造函数中，找到现有命令注册代码（约第 266–279 行）：

```cpp
    OdSmartPtr<Cmd_SAVE> save = OdRxObjectImpl<Cmd_SAVE>::createObject();
    OdSmartPtr<Cmd_SAVEAS> saveAs = OdRxObjectImpl<Cmd_SAVEAS>::createObject();

    OdSmartPtr<Cmd_REGEN> regen = OdRxObjectImpl<Cmd_REGEN>::createObject();
    regen->m_pCadCore = this;
    
    OdSmartPtr<Cmd_REDRAW> redraw = OdRxObjectImpl<Cmd_REDRAW>::createObject();
    redraw->m_pCadCore = this;

    OdEdCommandStackPtr pCommands = odedRegCmds();
    pCommands->addCommand(save);
    pCommands->addCommand(saveAs);
    pCommands->addCommand(regen);
    pCommands->addCommand(redraw);
```

在 `pCommands->addCommand(redraw);` 之后、`pCommands->addReactor(&m_undoReactor);` 之前，插入：

```cpp

    // GIS 桥接命令
    OdSmartPtr<Cmd_GIS_LOAD_MAP_IMAGE> gisLoadMap = OdRxObjectImpl<Cmd_GIS_LOAD_MAP_IMAGE>::createObject();
    gisLoadMap->m_pCadCore = this;
    OdSmartPtr<Cmd_GIS_LOAD_FEATURES> gisLoadFeatures = OdRxObjectImpl<Cmd_GIS_LOAD_FEATURES>::createObject();
    gisLoadFeatures->m_pCadCore = this;
    OdSmartPtr<Cmd_GIS_PUSH_FEATURES> gisPush = OdRxObjectImpl<Cmd_GIS_PUSH_FEATURES>::createObject();
    gisPush->m_pCadCore = this;
    OdSmartPtr<Cmd_GIS_PULL_FEATURES> gisPull = OdRxObjectImpl<Cmd_GIS_PULL_FEATURES>::createObject();
    gisPull->m_pCadCore = this;
    OdSmartPtr<Cmd_GIS_EXPORT> gisExport = OdRxObjectImpl<Cmd_GIS_EXPORT>::createObject();
    gisExport->m_pCadCore = this;
    OdSmartPtr<Cmd_GIS_CRS_INFO> gisCrsInfo = OdRxObjectImpl<Cmd_GIS_CRS_INFO>::createObject();
    gisCrsInfo->m_pCadCore = this;

    pCommands->addCommand(gisLoadMap);
    pCommands->addCommand(gisLoadFeatures);
    pCommands->addCommand(gisPush);
    pCommands->addCommand(gisPull);
    pCommands->addCommand(gisExport);
    pCommands->addCommand(gisCrsInfo);
```

- [ ] **Step 2: 在 CMakeLists.txt 中添加 GisCommands.cpp**

在 `DrawingWeb/CMakeLists.txt` 的 `oda_sources` 列表中，找到 `Commands.cpp`（第 272 行），在其后添加：

```cmake
    GisCommands.cpp
```

最终该区域应为：

```cmake
    Commands.cpp
    GisCommands.cpp
    ${WRAPPERS_CPP}
```

- [ ] **Step 3: Commit**

```bash
cd e:/ODAGitLab/main24.10/DrawingWeb
git add CadCore.cpp CMakeLists.txt
git commit -m "feat: register 6 GIS commands in CadCore and add GisCommands.cpp to build"
```

---

### Task 13: 注册 JS 回调并验证前端 lint

**Files:**
- Modify: `src/hooks/useWasmModule.js` (约 window callback 注册区域)

- [ ] **Step 1: 在 useWasmModule.js 中注册 GIS 回调**

找到 `useWasmModule.js` 中注册 `window.__onCommandComplete` 等回调的区域，在其后添加 GIS 回调注册：

```js
      // GIS 回调
      window.__onGisConnected = (serviceUrl) => {
        console.log('[GIS] 服务已连接:', serviceUrl)
      }
      window.__onGisLoadProgress = (percent) => {
        console.log('[GIS] 加载进度:', percent + '%')
      }
      window.__onGisSyncComplete = (action, count) => {
        console.log('[GIS] 同步完成:', action, 'count:', count)
      }
      window.__onGisError = (msg) => {
        console.error('[GIS] 错误:', msg)
      }
      window.__onGisCrsInfo = (jsonStr) => {
        console.log('[GIS] 坐标系信息:', jsonStr)
      }
```

- [ ] **Step 2: 前端完整 lint 检查**

Run: `npm run lint`
Expected: 无新增错误

- [ ] **Step 3: Commit**

```bash
git add src/hooks/useWasmModule.js
git commit -m "feat: register GIS WASM callback handlers in useWasmModule"
```

---

### Task 14: 最终验证

- [ ] **Step 1: 运行完整 lint 检查**

Run: `npm run lint`
Expected: 无新增错误

- [ ] **Step 2: 如有 lint 错误则修复并提交**

```bash
git add -A
git commit -m "fix: resolve lint issues in GIS service implementation"
```

- [ ] **Step 3: 验证开发服务器可启动**

Run: `npm run dev` (手动验证页面可加载，切换到审图模式可看到"GIS服务"标签，点击按钮可弹出各弹窗/面板)
