# 设计文档：同步 quzhen 分支审查批注功能至 feat-zfs

**日期**：2026-05-07  
**目标分支**：`feat-zfs`  
**来源分支**：`origin/quzhen`  
**作者**：admin@webuacad.com

---

## 背景

`quzhen` 分支实现了完整的审查批注功能（多轮次历史、iframe 嵌入协议、只读模式、控规参数弹窗、审图报告面板扩展），需同步至 `feat-zfs` 主开发分支。

两个分支均有各自独立改动，不能直接 `git merge`，采用 **`git merge -X ours` + 手动补丁**策略。

---

## 第一节：文件分类与处理策略

### ① 纯新增文件（直接接受 quzhen 版本）

| 文件 | 说明 |
|------|------|
| `src/components/AnnotationListPanel/AnnotationListPanel.jsx` | 批注列表面板组件 |
| `src/components/AnnotationListPanel/AnnotationListPanel.module.css` | 批注列表样式 |
| `src/components/ReviewControlParamsModal/ReviewControlParamsModal.jsx` | 控规参数补填弹窗 |
| `src/components/ReviewReportPanel/ReviewReportPanel.jsx` | 审图报告面板（多标签扩展版） |
| `src/components/ReviewReportPanel/ReviewReportPanel.module.css` | 审图报告样式 |

### ② 纯 feat-zfs 独有文件（`-X ours` 自动保留）

- `src/services/memory/`（RedlinePipeline、[[Vision]]MemoryPipeline 等）
- `src/components/AiAssistant/DrawingMemoryPanel/`（MainAreaSection、CandidateObjectsList）
- `src/stores/AppStore.js` 中内存管线相关状态
- 其他 AI/内存管线相关文件（约 50 个）

### ③ 双边均有改动的共享文件（需手动补丁，共 7 个）

| 文件 | feat-zfs 改动 | 需从 [[quzhen]] 插入的内容 |
|------|-------------|----------------------|
| `src/stores/AnnotationStore.js` | 基础批注工具 | `DRAG_TOOLS` 常量、`author`/`authorId`/`readOnly`/`hasUnsavedChanges` 字段、`historyUrls`/`historyItems`/`historySets` 历史字段、`setAuthor`/`setReadOnly`/`setHistoryUrls`/`setHistoryItems`/`persistToParent` 方法 |
| `src/stores/ReviewStore.js` | 基础审图 Store | `findings`/`dimensionCoverage`/`qualityScore` 字段、`showReportPanel`/`hideReportPanel`/`setFindings` 等方法 |
| `src/App.jsx` | 基本结构 | 两个 `useEffect`（VIEWER_READY 通知 + OPEN_FILE/CLOSE_FILE/REQUEST_SAVE postMessage 处理）、`waitForDbOpen` helper、`ReviewReportPanel` 渲染、`TopBar`/`TabBar`/`BottomDock`/`StatusBar` 的 `reviewMode` 条件渲染 |
| `src/stores/AppStore.js` | 内存管线状态 | `reviewMode` 字段 + `setReviewMode` 方法 |
| `src/components/Ribbon/ReviewRibbon.jsx` | 审图工具条 | `ReviewControlParamsModal` import + 触发逻辑；`HomeTab` 中批注工具和管理按钮的 `{!readOnly && (...)}` 包裹；批注列表从 Popover 改为右侧面板按钮；`SmartReviewTab` 移除，"AI 智能审图"按钮移入 `ReviewFlowTab` |
| `src/components/RightSidebar/RightSidebar.jsx` | 基础侧边栏 | `AnnotationListPanel` import、批注面板入口按钮（带角标）、`AnnotationListPanel` 条件渲染 |
| `src/stores/RootStore.js` | 全局 Store | 验证 `AnnotationStore` 已注册，如缺失则补充 |

---

## 第二节：执行流程

### Step 1：执行 merge

```bash
git merge -X ours origin/quzhen --no-edit
```

自动处理所有无冲突文件，冲突文件以 feat-zfs 为准。完成后检查状态确认无遗留冲突标记。

### Step 2：验证新文件已并入

确认以下目录/文件已出现在工作区：
- `src/components/AnnotationListPanel/`
- `src/components/ReviewControlParamsModal/`
- `src/components/ReviewReportPanel/`

### Step 3：手动补丁（按顺序）

1. **`AnnotationStore.js`** — 追加 `DRAG_TOOLS`、author/readOnly/history 字段和相关方法
2. **`ReviewStore.js`** — 追加 findings/dimensionCoverage/qualityScore 字段及 show/hideReportPanel 方法
3. **`AppStore.js`** — 追加 `reviewMode` 字段 + `setReviewMode` 方法
4. **`App.jsx`** — 插入 iframe 嵌入协议（两个 useEffect + waitForDbOpen helper）、ReviewReportPanel 渲染、UI 条件隐藏
5. **`ReviewRibbon.jsx`** — 插入 ReviewControlParamsModal、readOnly 条件渲染、批注列表改为右侧面板、移除 SmartReviewTab
6. **`RightSidebar.jsx`** — 插入 AnnotationListPanel import、批注面板入口和角标
7. **`RootStore.js`** — 验证 AnnotationStore 注册

### Step 4：构建验证

```bash
npm run lint
npm run build
```

### Step 5：提交

一条描述性 commit 记录本次同步内容。

---

## 第三节：验证标准

### 批注功能

- [ ] 审图模式下可切换批注工具（云线/箭头/矩形/圆/文字/引线）
- [ ] 拖拽绘制 DRAG_TOOLS（cloud/rect/circle）正常工作
- [ ] 绘制完成后弹出说明文字输入框
- [ ] 右侧边栏批注列表面板可打开，角标显示批注数量
- [ ] 批注列表支持过滤（全部/待审查/已解决/已关闭）
- [ ] 点击"定位"跳转到图纸对应批注位置
- [ ] 点击"解决"变更批注状态

### iframe 嵌入协议

- [ ] WASM 就绪后向父窗口发送 `VIEWER_READY`
- [ ] 收到 `OPEN_FILE` 能正确打开图纸并加载批注
- [ ] 收到 `CLOSE_FILE` 能正确关闭图纸并重置 reviewMode
- [ ] `REQUEST_SAVE` 触发 `persistToParent`，批注数据上报父窗口

### 历史批注

- [ ] AnnotationListPanel 中可展开历史轮次面板
- [ ] 历史批注只读显示，不可编辑

### 控规参数弹窗

- [ ] 审图前若未读取到控规限值，弹出 ReviewControlParamsModal
- [ ] 手动填写容积率/建筑密度等参数后可继续审图

### UI 可见性控制

- [ ] `reviewMode=true` 时，TopBar/TabBar/BottomDock/StatusBar 均不渲染
- [ ] `readOnly=true` 时，ReviewRibbon 的"图形批注"工具组和"导出/导入/清除"按钮不显示
- [ ] `readOnly=false` 时，上述工具正常显示

### 构建

- [ ] `npm run lint` 无错误
- [ ] `npm run build` 成功

---

## 第四节：UI 可见性控制详情

### reviewMode（iframe 嵌入场景）

由 `AppStore.reviewMode` 控制，通过 `OPEN_FILE` postMessage 设置。

```jsx
// App.jsx
{!appStore.reviewMode && <TopBar />}
{!appStore.reviewMode && <TabBar />}
{editorStore.isDrawingMode && !appStore.reviewMode && <BottomDock />}
{editorStore.isDrawingMode && !appStore.reviewMode && <StatusBar />}
```

### readOnly（非当前审查人场景）

由 `AnnotationStore.readOnly` 控制，通过 `OPEN_FILE` postMessage 设置。

```jsx
// ReviewRibbon.jsx - HomeTab
{!readOnly && (
  <RvGroup label="图形批注">
    {/* 云线/箭头/矩形/圆/文字/引线工具 */}
  </RvGroup>
)}
{!readOnly && (
  <>
    <Divider />
    {/* 导出/导入/清除按钮 */}
  </>
)}
```

---

## 冲突解决原则

- **feat-zfs 优先**：所有 AI/内存管线/视觉记忆相关代码保持 feat-zfs 版本
- **[[quzhen]] 叠加**：批注/审图/嵌入协议相关代码以 [[quzhen]] 版本为准，插入 feat-zfs 版本中
- **SmartReviewTab**：[[quzhen]] 中已移除该 Tab，"AI 智能审图"按钮移入 ReviewFlowTab，遵循此决定

## 相关笔记

- [[specs]]
- [[Legend Analysis Redesign: Programmatic Region Scan + Vision]]
- [[Industry Standards RAG Knowledge Base Design]]
- [[DWG 导出 GIS 按 CAD 图层过滤 — 设计文档]]
- [[WASM License Gate 设计（DrawingWebApp）]]
- [[GIS 目录面板 + 调图/属性查询 设计文档]]
- [[审图批注沙箱 API 设计]]
- [[WebUACAD AI Agent 全面分析报告]]
