# quzhen 审查批注功能同步 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `origin/quzhen` 分支的审查批注、iframe 嵌入协议、控规参数弹窗、UI 可见性控制等功能通过 `git merge -X ours` + 手动补丁合并至 `feat-zfs` 分支。

**Architecture:** 使用 `git merge -X ours origin/quzhen` 自动处理无冲突文件（新建组件直接并入），再对 7 个双边均有改动的共享文件逐一手动补丁，以 [[feat-zfs]] 现有代码为基础插入 quzhen 的批注/审图/嵌入协议代码块。

**Tech Stack:** React 19, MobX 6, Vite 7, Ant Design 6, postMessage API

---

## Task 1: git merge + 验证新文件

**Files:**
- 无需创建/修改，git 自动处理

- [ ] **Step 1: 执行 merge**

```powershell
cd D:\CODE\UPDA\Drawing2026\DrawingWebApp
git merge -X ours origin/quzhen --no-edit
```

预期输出：显示 `Merge made by the 'ort' strategy.` 以及合并的文件列表，无 `CONFLICT` 行。

- [ ] **Step 2: 验证新文件已并入**

```powershell
Test-Path src\components\AnnotationListPanel\AnnotationListPanel.jsx
Test-Path src\components\ReviewControlParamsModal\ReviewControlParamsModal.jsx
Test-Path src\components\ReviewReportPanel\ReviewReportPanel.jsx
```

预期输出：三行均为 `True`。

- [ ] **Step 3: 确认无冲突标记**

```powershell
git diff --check
```

预期输出：无输出（无冲突标记）。

- [ ] **Step 4: Commit**

```powershell
git add -A
git commit -m "chore: merge origin/quzhen with -X ours strategy"
```

---

## Task 2: 新增 ReviewStore.js + 注册到 RootStore

**Files:**
- Create: `src/stores/ReviewStore.js`
- Modify: `src/stores/RootStore.js`

- [ ] **Step 1: 创建 ReviewStore.js**

新建 `src/stores/ReviewStore.js`，内容如下：

```js
import { makeAutoObservable } from 'mobx'

class ReviewStore {
  report = null
  layerSemantics = []
  metrics = null
  compliance = []
  findings = []
  dimensionCoverage = {}
  qualityScore = 0
  reportVisible = false
  isAnalyzing = false
  analysisProgress = null
  sessionId = null
  sseError = false
  warnings = []

  constructor(rootStore) {
    this.rootStore = rootStore
    makeAutoObservable(this, { rootStore: false })
  }

  setReport(data) { this.report = data }
  setLayerSemantics(semantics) { this.layerSemantics = semantics || [] }
  setMetrics(metrics) { this.metrics = metrics }
  setCompliance(compliance) { this.compliance = compliance || [] }
  setFindings(findings) { this.findings = findings || [] }
  setDimensionCoverage(coverage) { this.dimensionCoverage = coverage || {} }
  setQualityScore(score) { this.qualityScore = score ?? 0 }

  toggleReportPanel() { this.reportVisible = !this.reportVisible }
  showReportPanel() { this.reportVisible = true }
  hideReportPanel() { this.reportVisible = false }

  setAnalyzing(isAnalyzing, progress = null) {
    this.isAnalyzing = isAnalyzing
    this.analysisProgress = progress
  }

  setProgress(message, percent) {
    this.analysisProgress = { message, percent }
  }

  setSessionId(id) { this.sessionId = id }
  setSseError(flag) { this.sseError = flag }
  addWarning(message) {
    if (this.warnings.length >= 100) this.warnings.shift()
    this.warnings.push(message)
  }
  clearWarnings() { this.warnings = [] }

  clearReport() {
    this.report = null
    this.layerSemantics = []
    this.metrics = null
    this.compliance = []
    this.findings = []
    this.dimensionCoverage = {}
    this.qualityScore = 0
    this.reportVisible = false
    this.isAnalyzing = false
    this.analysisProgress = null
    this.sessionId = null
    this.sseError = false
    this.warnings = []
  }

  toJSON() {
    return {
      report: this.report,
      layerSemantics: this.layerSemantics,
      metrics: this.metrics,
      compliance: this.compliance,
      findings: this.findings,
      dimensionCoverage: this.dimensionCoverage,
      qualityScore: this.qualityScore,
      sessionId: this.sessionId,
      warnings: this.warnings,
    }
  }
}

export default ReviewStore
```

- [ ] **Step 2: 在 RootStore.js 中注册 ReviewStore**

打开 `src/stores/RootStore.js`，当前内容为：

```js
import AppStore from './AppStore'
import EditorStore from './EditorStore'
import CompareStore from './CompareStore'
import AnalysisStore from './AnalysisStore'
import GisStore from './GisStore'
import LicenseStore from './LicenseStore'
import AnnotationStore from './AnnotationStore'
import MeasureStore from './MeasureStore'

class RootStore {
  constructor() {
    this.appStore = new AppStore(this)
    this.editorStore = new EditorStore(this)
    this.compareStore = new CompareStore(this)
    this.analysisStore = new AnalysisStore(this)
    this.gisStore = new GisStore(this)
    this.licenseStore = new LicenseStore(this)
    this.annotationStore = new AnnotationStore(this)
    this.measureStore = new MeasureStore(this)
  }
}

export default RootStore
```

在 `import MeasureStore` 后添加一行，并在 constructor 末尾添加实例化：

```js
import AppStore from './AppStore'
import EditorStore from './EditorStore'
import CompareStore from './CompareStore'
import AnalysisStore from './AnalysisStore'
import GisStore from './GisStore'
import LicenseStore from './LicenseStore'
import AnnotationStore from './AnnotationStore'
import MeasureStore from './MeasureStore'
import ReviewStore from './ReviewStore'

class RootStore {
  constructor() {
    this.appStore = new AppStore(this)
    this.editorStore = new EditorStore(this)
    this.compareStore = new CompareStore(this)
    this.analysisStore = new AnalysisStore(this)
    this.gisStore = new GisStore(this)
    this.licenseStore = new LicenseStore(this)
    this.annotationStore = new AnnotationStore(this)
    this.measureStore = new MeasureStore(this)
    this.reviewStore = new ReviewStore(this)
  }
}

export default RootStore
```

- [ ] **Step 3: Commit**

```powershell
git add src/stores/ReviewStore.js src/stores/RootStore.js
git commit -m "feat(store): add ReviewStore, register in RootStore"
```

---

## Task 3: 补丁 AnnotationStore.js

**Files:**
- Modify: `src/stores/AnnotationStore.js`

quzhen 在 [[feat-zfs]] 基础上新增：`DRAG_TOOLS` 导出常量、`pendingAnnotationParams` / `author` / `authorId` / `readOnly` / `hasUnsavedChanges` / `historyUrls` / `historyItems` / `historyLoading` / `historySets` 字段，以及 `setAuthor` / `setReadOnly` / `setHistoryUrls` / `setHistoryItems` / `loadHistoryAnnotations` / `persistToParent` 六个方法，并修改 `currentToolHint` getter、`startAnnotationTool`、`cancelAnnotationTool` 以支持 `pendingAnnotationParams`。

- [ ] **Step 1: 在 TOOL_HINTS 之前添加 DRAG_TOOLS 导出常量**

在 `src/stores/AnnotationStore.js` 第 16 行（`const TOOL_POINT_REQUIREMENTS` 之前），插入：

```js
/** 拖拽绘制工具（mousedown→dragEnd），不走 handleCanvasClick 的单击流程 */
export const DRAG_TOOLS = ['cloud', 'rect', 'circle']
```

- [ ] **Step 2: 在类字段中添加新字段**

找到当前 class 内的字段声明区域（`waitingForTextInput` 之后，`constructor` 之前）：

```js
  waitingForTextInput = false
  textInputPosition = null
  textInputScreenPos = null

  constructor(rootStore) {
```

替换为：

```js
  waitingForTextInput = false
  textInputPosition = null
  textInputScreenPos = null
  /** 图形工具完成绘制后，等待用户输入说明文字时暂存的图形参数 */
  pendingAnnotationParams = null

  /** 当前用户姓名，由父页面通过 postMessage OPEN_FILE 传入 */
  author = ''
  /** 当前用户 ID，由父页面通过 postMessage OPEN_FILE 传入 */
  authorId = null
  /** 只读模式：true 时隐藏批注工具栏，不允许添加/删除 */
  readOnly = false

  /** 有未持久化到服务端的批注变更 */
  hasUnsavedChanges = false

  /** 历史轮次批注文件预签名 URL 列表 */
  historyUrls = []
  /** 历史批注条目（含元数据）：[{ url, round, taskName, assigneeName, savedAt }] */
  historyItems = []
  /** 历史批注加载状态 */
  historyLoading = false
  /** 已加载的历史批注组：[{ url, annotations: Annotation[] }] */
  historySets = []

  constructor(rootStore) {
```

- [ ] **Step 3: 修改 currentToolHint getter**

找到：

```js
  get currentToolHint() {
    if (!this.activeAnnotationTool) return null
    if (this.waitingForTextInput) return '输入批注文字后按 Enter 确认'
```

替换为：

```js
  get currentToolHint() {
    if (!this.activeAnnotationTool) return null
    if (this.waitingForTextInput) {
      return this.pendingAnnotationParams !== null
        ? '输入批注说明（可选，直接 Enter 跳过）'
        : '输入批注文字后按 Enter 确认'
    }
```

- [ ] **Step 4: 修改 startAnnotationTool 和 cancelAnnotationTool**

找到：

```js
  startAnnotationTool(tool) {
    this.activeAnnotationTool = tool
    this.pendingPoints = []
    this.waitingForTextInput = false
    this.textInputPosition = null
    this.textInputScreenPos = null
    this.isAnnotationMode = true
  }

  cancelAnnotationTool() {
    this.activeAnnotationTool = null
    this.pendingPoints = []
    this.waitingForTextInput = false
    this.textInputPosition = null
    this.textInputScreenPos = null
  }
```

替换为：

```js
  startAnnotationTool(tool) {
    this.activeAnnotationTool = tool
    this.pendingPoints = []
    this.waitingForTextInput = false
    this.textInputPosition = null
    this.textInputScreenPos = null
    this.pendingAnnotationParams = null
    this.isAnnotationMode = true
  }

  cancelAnnotationTool() {
    this.activeAnnotationTool = null
    this.pendingPoints = []
    this.waitingForTextInput = false
    this.textInputPosition = null
    this.textInputScreenPos = null
    this.pendingAnnotationParams = null
  }
```

- [ ] **Step 5: 在 setAnnotationColor 之后插入新方法**

找到：

```js
  setAnnotationColor(colorIndex) {
    this.annotationColor = colorIndex
  }

  // ==================== 交互式绘制状态机 ====================
```

替换为：

```js
  setAnnotationColor(colorIndex) {
    this.annotationColor = colorIndex
  }

  /** 设置当前批注用户信息（由父页面在 OPEN_FILE 时传入） */
  setAuthor(name, id) {
    this.author = name || ''
    this.authorId = id || null
  }

  /** 切换只读模式（true = 非当前审查人，隐藏编辑工具栏） */
  setReadOnly(flag) {
    this.readOnly = !!flag
  }

  /** 设置历史轮次批注 URL（OPEN_FILE 时由 App.jsx 注入） */
  setHistoryUrls(urls) {
    this.historyUrls = Array.isArray(urls) ? urls : []
    this.historyItems = []
    this.historySets = []
    this.historyLoading = false
  }

  /** 设置含元数据的历史批注条目（优先于 setHistoryUrls） */
  setHistoryItems(items) {
    this.historyItems = Array.isArray(items) ? items : []
    this.historyUrls = this.historyItems.map(it => it.url).filter(Boolean)
    this.historySets = []
    this.historyLoading = false
  }

  /** 按需加载历史批注（用户点击"历史批注"时调用） */
  async loadHistoryAnnotations() {
    if (this.historyUrls.length === 0 || this.historyLoading) return
    this.historyLoading = true
    this.historySets = []
    try {
      const results = await Promise.all(
        this.historyUrls.map(async (url, idx) => {
          try {
            const resp = await fetch(url)
            if (!resp.ok) return { url, annotations: [], error: `HTTP ${resp.status}` }
            const data = await resp.json()
            return { url, annotations: data?.annotations ?? [] }
          } catch (e) {
            console.warn('[AnnotationStore] 历史批注加载失败 idx=', idx, e)
            return { url, annotations: [], error: e.message }
          }
        })
      )
      runInAction(() => { this.historySets = results })
    } finally {
      runInAction(() => { this.historyLoading = false })
    }
  }

  /**
   * 将批注 JSON 通过 postMessage 上报给父页面（iframe 嵌入场景）。
   * 必须通过 JSON.parse(JSON.stringify(...)) 将 MobX observable 转为纯对象，
   * 否则 postMessage 结构化克隆会抛 DataCloneError。
   */
  persistToParent() {
    const plainJson = JSON.parse(JSON.stringify(this.toJSON()))
    window.parent.postMessage(
      { source: 'drawing-viewer', type: 'SAVE_ANNOTATIONS', json: plainJson },
      '*'
    )
    this.hasUnsavedChanges = false
  }

  // ==================== 交互式绘制状态机 ====================
```

- [ ] **Step 6: 构建验证**

```powershell
cd D:\CODE\UPDA\Drawing2026\DrawingWebApp
npm run build 2>&1 | Select-String -Pattern "error|Error" | Select-Object -First 20
```

预期：无 error 输出。

- [ ] **Step 7: Commit**

```powershell
git add src/stores/AnnotationStore.js
git commit -m "feat(store): add DRAG_TOOLS, author/readOnly/history fields and methods to AnnotationStore"
```

---

## Task 4: 补丁 AppStore.js

**Files:**
- Modify: `src/stores/AppStore.js`

- [ ] **Step 1: 添加 reviewMode 字段**

在 `src/stores/AppStore.js` 中，找到：

```js
  isDarkTheme = true
  statusText = 'Downloading...'
```

替换为：

```js
  isDarkTheme = true
  reviewMode = false
  statusText = 'Downloading...'
```

- [ ] **Step 2: 添加 setReviewMode 方法**

找到：

```js
  toggleTheme() {
```

在其前插入：

```js
  setReviewMode(v) {
    this.reviewMode = !!v
  }

```

- [ ] **Step 3: Commit**

```powershell
git add src/stores/AppStore.js
git commit -m "feat(store): add reviewMode field and setReviewMode to AppStore"
```

---

## Task 5: 补丁 App.jsx（iframe 嵌入协议 + UI 隐藏）

**Files:**
- Modify: `src/App.jsx`

- [ ] **Step 1: 更新 import 区域**

将 `src/App.jsx` 第 1 行：

```js
import { useMemo } from 'react'
```

替换为：

```js
import { useMemo, useEffect } from 'react'
```

在 `import GisCatalogPanel` 之后添加：

```js
import ReviewReportPanel from './components/ReviewReportPanel/ReviewReportPanel'
```

- [ ] **Step 2: 解构 viewerRef**

找到：

```js
  const { rootStore } = useStores()
  const { appStore, editorStore } = rootStore
  const { gisStore } = rootStore
```

替换为：

```js
  const { rootStore, viewerRef } = useStores()
  const { appStore, editorStore } = rootStore
  const { gisStore } = rootStore
```

- [ ] **Step 3: 插入两个 useEffect（iframe 嵌入协议）**

在 `const antdTheme = useMemo(` 之前插入：

```js
  // WASM 就绪时通知父窗口（iframe 嵌入场景）
  useEffect(() => {
    if (appStore.wasmReady) {
      window.parent.postMessage({ source: 'drawing-viewer', type: 'VIEWER_READY' }, '*')
    }
  }, [appStore.wasmReady])

  // 监听父窗口 postMessage：支持远程打开/关闭图纸及批注加载
  useEffect(() => {
    const handler = async (e) => {
      if (e.data?.source !== 'drawing-viewer') return

      async function waitForDbOpen(v, maxMs = 5000) {
        const start = Date.now()
        while (!v.isDatabaseOpen) {
          if (Date.now() - start > maxMs) {
            console.warn('[App] waitForDbOpen timeout after', maxMs, 'ms')
            return false
          }
          await new Promise(r => setTimeout(r, 50))
        }
        return true
      }

      if (e.data.type === 'OPEN_FILE') {
        const viewer = viewerRef.current
        if (!viewer) return

        appStore.setReviewMode(!!e.data.reviewMode)

        const { annotationStore } = rootStore
        annotationStore.setAuthor(e.data.author || '', e.data.authorId || null)
        annotationStore.setReadOnly(!!e.data.readOnly)

        try {
          const resp = await fetch(e.data.fileUrl)
          if (!resp.ok) throw new Error('fetch failed: ' + resp.status)
          const blob = await resp.blob()
          const file = new File([blob], e.data.fileName || 'drawing.dwg')
          await viewer.handleOpenDwgFile(file)
          window.parent.postMessage(
            { source: 'drawing-viewer', type: 'FILE_LOADED', success: true },
            '*'
          )

          const hasCurrentUrl = !!e.data.annotationUrl
          const historyUrls = Array.isArray(e.data.annotationHistoryUrls) ? e.data.annotationHistoryUrls : []
          const historyItems = Array.isArray(e.data.annotationHistoryItems) ? e.data.annotationHistoryItems : []

          if (hasCurrentUrl || historyUrls.length > 0 || historyItems.length > 0) {
            const ready = await waitForDbOpen(viewer)
            if (!ready) {
              console.warn('[App] waitForDbOpen timeout, skip annotation load')
            } else {
              if (historyItems.length > 0) {
                annotationStore.setHistoryItems(historyItems)
              } else if (historyUrls.length > 0) {
                annotationStore.setHistoryUrls(historyUrls)
              }

              if (hasCurrentUrl) {
                try {
                  const annResp = await fetch(e.data.annotationUrl)
                  if (annResp.ok) {
                    const annData = await annResp.json()
                    annotationStore.loadAnnotations(viewer, annData)
                    if (annotationStore.annotationCount > 0) {
                      editorStore.openRightPanel('annotations')
                    }
                    window.parent.postMessage(
                      { source: 'drawing-viewer', type: 'ANNOTATIONS_LOADED', count: annotationStore.annotationCount },
                      '*'
                    )
                  }
                } catch (annErr) {
                  console.warn('[App] 当前批注加载失败:', annErr)
                }
              }
            }
          }
        } catch (err) {
          console.error('[App] OPEN_FILE 失败:', err)
          window.parent.postMessage(
            { source: 'drawing-viewer', type: 'FILE_LOADED', success: false, error: err.message },
            '*'
          )
        }
      }

      if (e.data.type === 'CLOSE_FILE') {
        const viewer = viewerRef.current
        if (viewer?.isDatabaseOpen) {
          await viewer.closeFile()
        }
        appStore.setReviewMode(false)
      }

      if (e.data.type === 'REQUEST_SAVE') {
        const { annotationStore } = rootStore
        if (window.parent !== window) {
          annotationStore.persistToParent()
        }
      }
    }

    window.addEventListener('message', handler)
    return () => window.removeEventListener('message', handler)
  }, [viewerRef, rootStore, appStore, editorStore])

```

- [ ] **Step 4: 添加 reviewMode 条件渲染（隐藏 TopBar/TabBar/BottomDock/StatusBar）**

找到：

```jsx
        <TopBar />
        <TabBar />
        <Ribbon />
```

替换为：

```jsx
        {!appStore.reviewMode && <TopBar />}
        {!appStore.reviewMode && <TabBar />}
        <Ribbon />
```

找到：

```jsx
          {editorStore.isDrawingMode && <BottomDock />}
          {editorStore.isDrawingMode && <StatusBar />}
```

替换为：

```jsx
          {editorStore.isDrawingMode && !appStore.reviewMode && <BottomDock />}
          {editorStore.isDrawingMode && !appStore.reviewMode && <StatusBar />}
```

- [ ] **Step 5: 添加 ReviewReportPanel 渲染**

找到：

```jsx
      <PointStyleDialog />
```

在其前插入：

```jsx
      <ReviewReportPanel />
```

- [ ] **Step 6: 构建验证**

```powershell
npm run build 2>&1 | Select-String -Pattern "error|Error" | Select-Object -First 20
```

预期：无 error 输出。

- [ ] **Step 7: Commit**

```powershell
git add src/App.jsx
git commit -m "feat(app): add iframe embedding protocol (OPEN_FILE/CLOSE_FILE/REQUEST_SAVE), reviewMode UI hiding, ReviewReportPanel"
```

---

## Task 6: 补丁 ReviewRibbon.jsx

**Files:**
- Modify: `src/components/Ribbon/ReviewRibbon.jsx`

变更清单：①新增 import；②新增 state 和 handler；③`HomeTab` 批注工具加 readOnly 条件；④批注列表从 Popover 改为右侧面板按钮；⑤`ReviewFlowTab` 新增 "AI 智能审图" 按钮；⑥删除 `SmartReviewTab` 组件；⑦删除 `case '智能审图'`；⑧末尾添加 `ReviewControlParamsModal`。

- [ ] **Step 1: 添加 import**

在 `src/components/Ribbon/ReviewRibbon.jsx` 顶部，找到：

```js
import s from './Ribbon.module.css'
```

在其后插入：

```js
import { startReview } from '../../services/ReviewService'
import { ReviewControlParamsModal } from '../ReviewControlParamsModal/ReviewControlParamsModal'
```

- [ ] **Step 2: 在 ReviewRibbon 组件内添加控规弹窗 state 和 handlers**

在 `src/components/Ribbon/ReviewRibbon.jsx` 中，找到 `const ReviewRibbon = observer(() => {` 所在的组件体，找到以下 state 声明区块末尾（`const [availableLayers, setAvailableLayers] = useState([])` 之后）：

```js
  const [availableLayers, setAvailableLayers] = useState([])

  // ===== 固定视图组 handlers =====
```

替换为：

```js
  const [availableLayers, setAvailableLayers] = useState([])
  const [paramsModalOpen, setParamsModalOpen] = useState(false)
  const [paramsModalResolve, setParamsModalResolve] = useState(null)

  const showParamsModal = (resolve) => {
    setParamsModalResolve(() => resolve)
    setParamsModalOpen(true)
  }

  const handleParamsConfirm = (params) => {
    setParamsModalOpen(false)
    paramsModalResolve?.(params)
  }

  const handleParamsSkip = () => {
    setParamsModalOpen(false)
    paramsModalResolve?.(null)
  }

  const handleStartReview = useCallback(async () => {
    const viewer = viewerRef.current
    const Module = moduleRef.current
    if (!viewer || !Module) {
      console.warn('[ReviewRibbon] viewer 或 Module 未就绪')
      return
    }
    await startReview(viewer, Module, rootStore, showParamsModal)
  }, [viewerRef, moduleRef, rootStore])

  // ===== 固定视图组 handlers =====
```

- [ ] **Step 3: 为 HomeTab 组件添加 readOnly prop**

找到 `HomeTab` 组件的函数签名（约在第 317 行附近）：

```js
const HomeTab = observer(function HomeTab({ onExec, onNotImpl, editorStore, viewerRef, annotationStore, onStartAnnotTool, onClearAnnotations, onExportAnnotations, onImportAnnotations }) {
  const activeTool = annotationStore.activeAnnotationTool
  const count = annotationStore.annotationCount
```

替换为：

```js
const HomeTab = observer(function HomeTab({ onExec, onNotImpl, editorStore, viewerRef, annotationStore, onStartAnnotTool, onClearAnnotations, onExportAnnotations, onImportAnnotations }) {
  const activeTool = annotationStore.activeAnnotationTool
  const count = annotationStore.annotationCount
  const readOnly = annotationStore.readOnly
```

- [ ] **Step 4: 将"图形批注"工具组用 readOnly 条件包裹**

在 `HomeTab` JSX 中，找到 `<RvGroup label="图形批注">` 开始到对应 `</RvGroup>` 结束的整个块。该块内部的按钮**内容不变**，只在外层添加 `{!readOnly && (...)}` 包裹：

将：
```jsx
      <RvGroup label="图形批注">
        ...（原有按钮不变）...
      </RvGroup>
```

改为：
```jsx
      {!readOnly && (
        <RvGroup label="图形批注">
          ...（原有按钮不变）...
        </RvGroup>
      )}
```

具体操作：在 `<RvGroup label="图形批注">` 前插入 `{!readOnly && (`，在对应的 `</RvGroup>` 后插入 `)}`，内部按钮一行不改。

- [ ] **Step 5: 将批注列表从 Popover 改为右侧面板按钮，管理区用 readOnly 包裹**

在 `HomeTab` 的 `<RvGroup label="批注管理">` 内，删除原有的两个 `<Popover>` 组件（列表 Popover 和筛选 Popover），替换为：

```jsx
      <RvGroup label="批注管理">
        {/* 批注列表：点击打开右侧面板 */}
        <RvBtn
          icon={I.list}
          label={count > 0 ? `批注列表(${count})` : '批注列表'}
          primary
          active={editorStore.activeRightPanel === 'annotations'}
          title="在右侧面板中查看所有批注"
          onClick={() => editorStore.setActiveRightPanel('annotations')}
        />
        {!readOnly && (
          <>
            <Divider />
            <RvBtn icon={I.exportFile} label="导出" title="导出批注为 JSON 文件" onClick={onExportAnnotations} />
            <input ref={importInputRef} type="file" accept=".json"
              style={{ display: 'none' }} onChange={e => {
                const file = e.target.files?.[0]
                if (file) onImportAnnotations(file)
                e.target.value = ''
              }} />
            <RvBtn icon={I.loadFile} label="导入" title="从 JSON 文件导入批注" onClick={() => importInputRef.current?.click()} />
            <Divider />
            <RvBtn icon={I.trash} label="全部清除" danger
              disabled={count === 0}
              title="清除所有批注" onClick={onClearAnnotations} />
          </>
        )}
      </RvGroup>
```

同时删除 `HomeTab` 内不再使用的 `showListPopover`、`showFilterPopover`、`statusFilter` 三个 state 变量。

- [ ] **Step 6: 为 ReviewFlowTab 添加 onStartReview prop 和"AI 智能审图"按钮**

找到：

```js
function ReviewFlowTab({ onNotImpl }) {
```

替换为：

```js
function ReviewFlowTab({ onNotImpl, onStartReview }) {
```

在该函数的 `<RvGroup label="报告">` 内，在第一个 `<RvBtn>` 之前插入：

```jsx
          <RvBtn
            icon={I.tableDoc}
            label="AI 智能审图"
            title="启动 AI 四阶段规划审图（密度/退距/用地边界）"
            primary
            onClick={onStartReview}
          />
```

- [ ] **Step 7: 在 renderTab 中将 ReviewFlowTab 传入 onStartReview**

找到：

```jsx
        case '审查流程': return <ReviewFlowTab onNotImpl={handleNotImpl} />
```

替换为：

```jsx
        case '审查流程': return <ReviewFlowTab onNotImpl={handleNotImpl} onStartReview={handleStartReview} />
```

- [ ] **Step 8: 删除 SmartReviewTab 组件和对应 case**

删除整个 `function SmartReviewTab(...)` 函数定义（约 1182-1250 行）。

找到并删除：

```jsx
        case '智能审图': return <SmartReviewTab onNotImpl={handleNotImpl} onSendToAi={handleSendToAi} viewerRef={viewerRef} appStore={appStore} />
```

- [ ] **Step 9: 在组件 JSX 末尾添加 ReviewControlParamsModal**

在 ReviewRibbon 的 JSX return 末尾，找到最后一个 `</div>` 之前，插入：

```jsx
        <ReviewControlParamsModal
          open={paramsModalOpen}
          onConfirm={handleParamsConfirm}
          onSkip={handleParamsSkip}
        />
```

- [ ] **Step 10: 构建验证**

```powershell
npm run build 2>&1 | Select-String -Pattern "error|Error" | Select-Object -First 20
```

预期：无 error 输出。

- [ ] **Step 11: Commit**

```powershell
git add src/components/Ribbon/ReviewRibbon.jsx
git commit -m "feat(ribbon): integrate ReviewControlParamsModal, readOnly annotation gating, annotation list as right panel, remove SmartReviewTab"
```

---

## Task 7: 补丁 RightSidebar.jsx（批注列表面板入口）

**Files:**
- Modify: `src/components/RightSidebar/RightSidebar.jsx`

- [ ] **Step 1: 添加 import**

在 `src/components/RightSidebar/RightSidebar.jsx` 顶部，找到：

```js
import {
  ProfileOutlined,
  BlockOutlined,
  RobotOutlined,
} from '@ant-design/icons'
```

替换为：

```js
import {
  ProfileOutlined,
  BlockOutlined,
  RobotOutlined,
  CommentOutlined,
} from '@ant-design/icons'
```

在 `import ReviewLayerPanel` 之后添加：

```js
import AnnotationListPanel from '../AnnotationListPanel/AnnotationListPanel'
```

- [ ] **Step 2: 解构 annotationStore 和 annotationCount**

找到：

```js
  const { rootStore } = useStores()
  const { appStore, editorStore } = rootStore
  const active = editorStore.activeRightPanel
  const hasDoc = appStore.isDatabaseOpen
```

替换为：

```js
  const { rootStore } = useStores()
  const { appStore, editorStore, annotationStore } = rootStore
  const active = editorStore.activeRightPanel
  const hasDoc = appStore.isDatabaseOpen
  const annotationCount = annotationStore.annotationCount
```

- [ ] **Step 3: 在 panelArea 内添加 AnnotationListPanel 条件渲染**

找到：

```jsx
          {active === 'ai' && (
            <AiAssistant onClose={close} />
          )}
```

在其后插入：

```jsx
          {active === 'annotations' && hasDoc && (
            <AnnotationListPanel onClose={close} />
          )}
```

- [ ] **Step 4: 在 buttonBar 中添加批注列表按钮**

找到：

```jsx
        <Tooltip title="AI 助手" placement="left">
          <button
            className={`${s.sideBtn} ${active === 'ai' ? s.sideBtnActive : ''}`}
            onClick={() => toggle('ai')}
          >
            <RobotOutlined className={s.sideBtnIcon} />
            <span className={s.sideBtnLabel}>AI</span>
          </button>
        </Tooltip>
```

在其前插入（仍在 `{hasDoc && (...)}` 块内，放在图层按钮后）：

```jsx
            <Tooltip title="批注列表" placement="left">
              <button
                className={`${s.sideBtn} ${active === 'annotations' ? s.sideBtnActive : ''}`}
                onClick={() => toggle('annotations')}
                style={{ position: 'relative' }}
              >
                <CommentOutlined className={s.sideBtnIcon} />
                <span className={s.sideBtnLabel}>批注</span>
                {annotationCount > 0 && (
                  <span style={{
                    position: 'absolute', top: 4, right: 4,
                    background: '#ff4d4f', color: '#fff',
                    borderRadius: '50%', width: 14, height: 14,
                    fontSize: 9, fontWeight: 700,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    lineHeight: 1,
                  }}>
                    {annotationCount > 99 ? '99+' : annotationCount}
                  </span>
                )}
              </button>
            </Tooltip>
```

- [ ] **Step 5: 构建验证**

```powershell
npm run build 2>&1 | Select-String -Pattern "error|Error" | Select-Object -First 20
```

预期：无 error 输出。

- [ ] **Step 6: Commit**

```powershell
git add src/components/RightSidebar/RightSidebar.jsx
git commit -m "feat(sidebar): add AnnotationListPanel entry with badge to RightSidebar"
```

---

## Task 8: 最终构建验证与 lint

**Files:** 无

- [ ] **Step 1: 运行 lint**

```powershell
cd D:\CODE\UPDA\Drawing2026\DrawingWebApp
npm run lint 2>&1 | Select-String -Pattern "error|warning" | Select-Object -First 30
```

预期：无 error 级别报告（warning 可接受）。

- [ ] **Step 2: 运行完整构建**

```powershell
npm run build
```

预期：输出 `built in Xs`，无 error。

- [ ] **Step 3: 验证新组件文件存在**

```powershell
Test-Path src\components\AnnotationListPanel\AnnotationListPanel.jsx
Test-Path src\components\ReviewControlParamsModal\ReviewControlParamsModal.jsx
Test-Path src\components\ReviewReportPanel\ReviewReportPanel.jsx
Test-Path src\stores\ReviewStore.js
```

预期：四行均为 `True`。

- [ ] **Step 4: 验证 git log 包含所有任务 commit**

```powershell
git log --oneline -8
```

预期：能看到 Task 1-7 对应的 7 条 commit 记录。
