# 审图批注沙箱 API 设计

> **日期**: 2026-05-06
> **状态**: 待实现
> **范围**: CadCodeExecutor 沙箱中注入受限的瞬态标注 API，让 AI 代码在审图模式下可直接创建批注

---

## 背景与动机

### 问题

当前 AI 代码在 CadCodeExecutor 沙箱中执行时，只能操作 OdDb* 数据库实体（永久写入 DWG 文件）。审图模式下需要的"批注标注"属于瞬态图形（不修改原始 DWG），但沙箱出于安全考虑未注入 `viewer` 对象，因此无法调用 `viewer.addTransientLeader()` 等瞬态 API。

### 现有架构分层

| 层 | 职责 | 可访问 |
|----|------|--------|
| CadCodeExecutor 沙箱 | 操作 OdDb* 数据库实体 | pDb, modelSpace, ODA 类 |
| AnnotationStore | 通过 ViewerService 管理瞬态标注 | viewer, transient API |

两层之间没有通道。AI 要创建审图批注，只能走"AI 返回数据 → 前端后处理"的路径，但这样 AI 无法精确控制标注位置（偏移、避让等）。

### 方案选择

经讨论排除了两个极端方案：
- **直接注入 viewer**：打破沙箱安全边界，风险过高
- **沙箱外后处理**：AI 无法控制标注位置，灵活性不足

**采用折中方案**：在沙箱中注入一个受限的 `addReviewAnnotation()` 函数，内部通过闭包捕获 `viewer` 和 `annotationStore`，做参数校验后转发给 AnnotationStore。

---

## API 设计

### `addReviewAnnotation(params)` 函数签名

沙箱中注入的统一入口函数，通过 `type` 字段区分 6 种标注类型：

```javascript
addReviewAnnotation({
  type: string,          // 必填：'leader' | 'text' | 'arrow' | 'circle' | 'rect' | 'cloud'
  colorIndex?: number,   // 可选，ACI 颜色索引 1-255，默认 1（红色）
  comment?: string,      // 可选，批注说明（显示在标注管理列表中）

  // ── leader 专属字段 ──
  from?: { x, y },       // 箭头尖端（指向问题位置）
  to?:   { x, y },       // 文字端点
  text?: string,         // 标注文字
  textHeight?: number,   // 可选，默认 3.0
  arrowSize?: number,    // 可选，默认 2.0

  // ── text 专属字段 ──
  position?: { x, y },   // 文字位置
  content?: string,      // 文字内容
  height?: number,       // 文字高度，默认 3.0

  // ── arrow 专属字段 ──
  from?: { x, y },       // 起点
  to?:   { x, y },       // 终点

  // ── circle 专属字段 ──
  center?: { x, y },     // 圆心
  radius?: number,       // 半径

  // ── rect 专属字段 ──
  p1?: { x, y },         // 对角点 1
  p2?: { x, y },         // 对角点 2

  // ── cloud 专属字段 ──
  points?: Array<{ x, y }>,  // 多边形顶点（≥3 个）
  arcLength?: number,        // 弧段长度
})
```

**返回值**: `string | null` — 成功返回 annotationId (UUID)，失败返回 null。

### 各类型必填字段

| type | 必填字段 |
|------|---------|
| `leader` | `from`, `to`, `text` |
| `text` | `position`, `content` |
| `arrow` | `from`, `to` |
| `circle` | `center`, `radius` |
| `rect` | `p1`, `p2` |
| `cloud` | `points` (长度 ≥ 3) |

### 参数校验规则

| 校验项 | 规则 | 失败行为 |
|--------|------|---------|
| `type` | 必须是 6 种之一 | 返回 null，console.warn |
| 坐标值 (x, y, radius) | `Number.isFinite()` | 返回 null，console.warn |
| `cloud.points` | 数组且长度 ≥ 3 | 返回 null，console.warn |
| `leader.text` / `text.content` | 非空字符串 | 返回 null，console.warn |
| `colorIndex` | 整数 1–255 | 越界则默认 1 |
| 单次执行累计上限 | ≤ 50 条 | 超出后 console.warn 并忽略 |

---

## 沙箱注入机制

### 注入位置与时序

在 `CadCodeExecutor.executeCadCode()` 中，`buildSandbox()` 返回后、`fn()` 执行前，构造闭包注入：

```
executeCadCode(code, Module, viewer, { annotationStore } = {})
  │
  ├─ pDb = viewer.appCore.getDb()
  ├─ sandbox = buildSandbox(Module, pDb, allocated)       // 现有逻辑不动
  │
  ├─ 【新增】if (annotationStore && viewer) {
  │     const _reviewAnnotations = []
  │     let _annotationCount = 0
  │     const MAX_ANNOTATIONS = 50
  │
  │     sandbox.addReviewAnnotation = (params) => {
  │       // 1. 计数检查
  │       // 2. 参数校验
  │       // 3. 构造 AnnotationStore.addAnnotation() 的参数
  │       // 4. 调用 annotationStore.addAnnotation(viewer, annoParams)
  │       // 5. 收集 { annotationId, type, comment } 到 _reviewAnnotations
  │       // 6. 返回 annotationId
  │     }
  │   }
  │
  ├─ fn(...scopeNames, code)(...scopeValues)              // 执行 AI 代码
  │
  ├─ viewer.appCore.Update()                              // 刷新视口
  └─ return { success, queryResult, reviewAnnotations: _reviewAnnotations }
```

### `executeCadCode()` 签名变更

```javascript
// 之前
executeCadCode(code, Module, viewer)

// 之后
executeCadCode(code, Module, viewer, { annotationStore = null } = {})
```

第四参数为可选 options 对象，向后兼容。当 `annotationStore` 为 null 时，沙箱中不注入 `addReviewAnnotation`（非审图场景不受影响）。

### 返回值扩展

```javascript
// 之前
return { success, entityCount, allocatedCount, queryResult }

// 之后
return { success, entityCount, allocatedCount, queryResult, reviewAnnotations }
// reviewAnnotations: Array<{ annotationId: string, type: string, comment: string }>
```

---

## 调用链适配

### 上溯传参路径

```
AiAssistant.jsx  onToolCall()
  │  rootStore.annotationStore  ← 从 MobX context 获取
  ▼
executeToolCallDirect(toolName, args, viewer, Module, toolCallId, { annotationStore })
  │
  ▼
CommandExecutor._executeCode() / _executeQuery()
  │  透传 annotationStore
  ▼
CadCodeExecutor.executeCadCode(code, Module, viewer, { annotationStore })
```

### CommandExecutor 修改

`_executeCode()` 和 `_executeQuery()` 的返回结构中新增 `reviewAnnotations` 字段：

```javascript
return {
  toolCallId,
  toolName,
  success: result.success,
  queryResult: result.queryResult,
  reviewAnnotations: result.reviewAnnotations,   // 【新增】
  // ...其余字段不变
}
```

### AiAssistant.jsx 修改

在 `onToolCall()` 中：
1. 获取 `rootStore.annotationStore` 并传入调用链
2. 从返回结果中读取 `reviewAnnotations`，可在聊天消息中展示"已创建 N 条审图批注"

---

## code_example 新增

### `review_annotation.js`

新增一个 code_example，让 RAG 检索到 `addReviewAnnotation` 的用法：

```javascript
/**
 * @scene 审图模式下计算距离并对不合规处创建瞬态批注标注
 * @apis addReviewAnnotation, OdGeCurve3d, OdGeTol
 * @intent CREATE
 * @prereqs 需要已有曲线实体，且在审图模式下执行
 * @result 对不满足距离要求的位置创建瞬态引线标注，不写入 DWG
 */
// @title: 审图批注 — 计算距离并对不合规处创建瞬态引线标注
// @tags: 审图, review, 批注, annotation, 瞬态, transient, addReviewAnnotation,
//        leader, 退缩, setback, 违规, violation, 间距, 不合规
// @api: addReviewAnnotation, distanceTo, closestPointTo, OdGeCurve3d,
//       OdGeTol, OdGePoint3d, forEachEntity, setResult
// @description: 在审图模式下，计算两组曲线间的最短距离，对不满足要求的位置
//   调用 addReviewAnnotation 创建瞬态引线标注（不写入 DWG 文件）。
//   支持 6 种标注类型：leader/text/arrow/circle/rect/cloud。
//   如需创建永久 DWG 标注实体请使用 leader_create 或 dimension_aligned。
```

### 与现有 example 的检索区分

| 用户意图 | 应命中的 example | 关键区分词 |
|----------|-----------------|-----------|
| "算一下两条线距离多少" | `curve_distance.js` | 距离、度量、distanceTo |
| "最近点在哪里" | `curve_distance_with_points.js` | 坐标、最近点、closestPointTo |
| "画一个对齐标注" | `dimension_aligned.js` | 标注、dimension、永久实体 |
| "审图时标记不合规的地方" | `review_annotation.js` (新增) | 审图、批注、瞬态、violation |
| "画一条引线" | `leader_create.js` | 引线、OdDbLeader、永久实体 |

---

## 数据流总览

```
用户在 AI 面板发起审图请求（如"检查建筑退缩距离"）
  │
  ▼
drawing-ai-server 生成 JS 代码（含 addReviewAnnotation 调用）
  │
  ▼
AiAssistant.jsx onToolCall()
  ├─ 获取 rootStore.annotationStore
  └─ 调用 executeToolCallDirect(..., { annotationStore })
       │
       ▼
CommandExecutor._executeCode() / _executeQuery()
  └─ 调用 executeCadCode(code, Module, viewer, { annotationStore })
       │
       ▼
CadCodeExecutor.executeCadCode()
  ├─ sandbox = buildSandbox(Module, pDb, allocated)
  ├─ 构造 addReviewAnnotation 闭包 → 注入 sandbox
  ├─ fn() 执行 AI 代码
  │   ├─ 计算距离
  │   ├─ 发现违规 → addReviewAnnotation({ type:'leader', ... })
  │   │   ├─ 校验参数
  │   │   ├─ viewer.addTransientLeader(...) → 画面上立即出现标注
  │   │   └─ annotationStore.addAnnotation(...) → 注册到标注管理列表
  │   └─ setResult({ violations: [...] })
  ├─ viewer.appCore.Update()
  └─ return { success, queryResult, reviewAnnotations }
       │
       ▼
AiAssistant.jsx
  ├─ buildToolOutputString 中包含 "已创建 N 条审图批注"
  └─ _setOutput(outputStr) → 结果回传给 LLM
       │
       ▼
LLM 生成总结："发现 3 处退缩距离不足，已在图纸上标注"
       │
       ▼
用户在画布上看到红色引线标注，在 AnnotationStore 列表中可管理
```

---

## 涉及修改的文件

| 文件 | 修改内容 |
|------|---------|
| `DrawingWebApp/src/services/CadCodeExecutor.js` | `executeCadCode()` 新增 `annotationStore` 参数；构造 `addReviewAnnotation` 闭包注入沙箱；返回值增加 `reviewAnnotations` |
| `DrawingWebApp/src/services/CommandExecutor.js` | `_executeCode()` / `_executeQuery()` 透传 `annotationStore`；结果中携带 `reviewAnnotations` |
| `DrawingWebApp/src/components/AiAssistant/AiAssistant.jsx` | `onToolCall()` 中取 `rootStore.annotationStore` 传入调用链 |
| **新增** `drawing-ai-server/.../code_examples/review_annotation.js` | 审图批注 code_example |
| drawing-ai-server prompt 模板 | 补充 `addReviewAnnotation` API 说明（实现阶段确认具体文件） |

## 不需要修改的文件

| 文件 | 原因 |
|------|------|
| `DrawingWebApp/src/stores/AnnotationStore.js` | 现有 `addAnnotation()` 已完整支持 6 种类型 |
| `DrawingWebApp/src/services/ViewerService.js` | 现有瞬态 API 不变 |
| `DrawingWeb/CadCoreAnnotation.cpp` | C++ 瞬态实现不变 |

---

## 已完成的前置改动

在本次设计讨论中，已经完成了 code_examples 的职责拆分：

| 操作 | 文件 |
|------|------|
| 新增 | `curve_distance.js` — 纯距离计算（distanceTo，仅返回数值） |
| 新增 | `curve_distance_with_points.js` — 距离 + 最近点坐标（closestPointTo） |
| 删除 | `curve_closest_point.js`（旧，职责模糊） |
| 删除 | `curve_distance_annotate.js`（旧，计算与标注耦合） |
