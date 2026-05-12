# WebUACAD AI Agent 全面分析报告

> 分析日期：2026-04-02
> 项目：DrawingWebApp（[[WebUACAD]]）

---

## 整体架构

```
用户 ──→ AiAssistant (React UI)
           │
           ├─ 工具栏附件: 拾取点 / 选择对象 / 区域 / 截图 / 引用文件(📎)
           │                │
           │                └─ /workspace/ 文件 ←── FsViewerPanel (上传/浏览/删除)
           │                                              ↑
           │                                         TopBar 文件夹按钮
           │
           ├─ useChat (@ai-sdk/react) ──→ POST /api/ai/chat
           │   + DrawingStateTransport        │
           │   + userAttachments              │
           │                              Server (Express + Vercel AI SDK)
           │                                    │
           │                              ┌─────┴─────┐
           │                              │ streamText │ ← System Prompt + Tools
           │                              │ maxSteps:10│   + drawingState + attachments
           │                              └─────┬─────┘   (ReAct 多步推理循环)
           │                                    │
           │                              LLM (GPT-4o / DeepSeek / Qwen)
           │                                    │
           │                              Tool Calls (11 个工具)
           │                                    │
           ├─ CommandExecutor (分发器) ←────────┘
           │      │
           │      ├─ cadCode / cadQueryCode → CadCodeExecutor (JS 沙箱)
           │      ├─ lispCode              → viewer.appCore.ExecuteLisp()
           │      ├─ cadCommand            → viewer.execute() → appCore.ExecuteCommand()
           │      ├─ captureRequest        → 截图 → 发回 LLM Vision 分析
           │      └─ plan / search         → 纯服务端记录
           │
           └─ 反馈闭环: [系统反馈] / [查询结果] / 截图 → 发回 LLM 自纠
```

### 关键模块

| 模块 | 文件路径 | 职责 |
|------|----------|------|
| AI Server | `server/index.js` | Express 服务器，持有 LLM API Key，流式返回 |
| 工具定义 | `server/tools/cadTools.js` | 7 个核心工具 + System Prompt |
| 分析工具 | `server/tools/analysisTools.js` | 4 个图纸分析工具 |
| 命令分发器 | `src/services/CommandExecutor.js` | 解析 tool 输出，路由到三条执行路径 |
| JS 沙箱 | `src/services/CadCodeExecutor.js` | 白名单沙箱执行 LLM 生成的 JS 代码 |
| Viewer 服务 | `src/services/ViewerService.js` | WASM 封装层，`appCore` = CadCore |
| AI 助手 UI | `src/components/AiAssistant/AiAssistant.jsx` | useChat + drawingState + 附件系统 + 反馈闭环 |
| 工作文件夹面板 | `src/components/FsViewerPanel/FsViewerPanel.jsx` | `/workspace/` 文件管理（上传/浏览/删除） |
| 顶栏 | `src/components/TopBar/TopBar.jsx` | [[文件操作]] + 工作文件夹入口 |
| 应用状态 | `src/stores/AppStore.js` | WASM 状态 + 工作文件夹面板/文件列表 |
| RAG 索引 | `server/rag/build_index.py` | ChromaDB 向量索引构建 |
| RAG 服务 | `server/rag/rag_server.py` | FastAPI 检索服务（端口 3002） |

---

## 当前 11 个工具一览

| # | 工具名 | 类别 | 执行位置 | 功能 |
|---|--------|------|----------|------|
| 1 | `execute_js_code` | **执行** | 前端沙箱 | JS 代码操作 DWG（绘图/修改/查询） |
| 2 | `execute_lisp_code` | **执行** | 前端 WASM | AutoLISP 代码执行 |
| 3 | `execute_command` | **执行** | 前端 WASM | WASM 命令执行（TRIM/FILLET 等） |
| 4 | `plan_task` | **规划** | 服务端 | 复杂任务分解为步骤 |
| 5 | `capture_viewport` | **视觉** | 前端截图 | 截取视图供 [[Vision]] 分析 |
| 6 | `search_code_examples` | **RAG** | 服务端→ChromaDB | 检索 ODA API 代码示例（32 个） |
| 7 | `search_help_docs` | **RAG** | 服务端→ChromaDB | 检索 [[WebUACAD]] 帮助文档 |
| 8 | `analyze_drawing` | **分析** | 前端沙箱+截图 | 综合图纸分析 |
| 9 | `detect_title_blocks` | **分析** | 前端管线 | 图框检测（双路径并行） |
| 10 | `extract_building_info` | **分析** | 前端沙箱+截图 | 建筑信息提取 |
| 11 | `measure_entities` | **分析** | 前端沙箱 | 距离/面积测量 |

---

## 三条执行路径详解

### 路径 1：JS 代码执行（主力路径）

- **入口**：`CadCodeExecutor.executeCadCode(code, Module, viewer)`
- **机制**：构建白名单沙箱，注入约 **60+ ODA WASM 类**
- **预置变量**：`pDb`（数据库）、`modelSpace`（模型空间）、`OpenAs()`、`setResult()`
- **[[内存管理]]**：embind 对象自动追踪，执行结束统一 `.delete()`
- **撤销支持**：执行前自动 `pDb.startUndoRecord()`
- **视图刷新**：成功后自动 `appCore.Update()` + `ZoomExtents()`
- **查询模式**：`isQuery=true` 时代码须调用 `setResult(data)` 返回结构化数据

**沙箱注入的 ODA 类（完整列表）**：

```
实体类（createObject 静态方法）：
  OdDbLine, OdDbCircle, OdDbArc, OdDbEllipse, OdDbPolyline,
  OdDb2dPolyline, OdDb3dPolyline, OdDb2dVertex, OdDb3dPolylineVertex,
  OdDbText, OdDbMText, OdDbHatch,
  OdDbAlignedDimension, OdDbRotatedDimension, OdDbRadialDimension,
  OdDbDiametricDimension, OdDb3dSolid, OdDbRegion,
  OdDbPoint, OdDbTrace, OdDbSolid, OdDbFace, OdDbSpline,
  OdDbBlockReference, OdDbMInsertBlock,
  OdDbRasterImage, OdDbRasterImageDef

表/记录类：
  OdDbBlockTableRecord, OdDbBlockTable,
  OdDbLayerTable, OdDbLayerTableRecord,
  OdDbLinetypeTable, OdDbLinetypeTableRecord,
  OdDbTextStyleTable, OdDbTextStyleTableRecord,
  OdDbDimStyleTable, OdDbDimStyleTableRecord,
  OdDbEntity, OdDbDictionary

几何类（new 构造）：
  OdGePoint3d, OdGePoint2d, OdGeVector3d, OdGeVector2d,
  OdGeMatrix3d, OdGePoint3dArray, OdGePoint2dArray,
  OdGeCircArc2d, OdGeTol, OdGePlane

工具类（new 构造）：
  OdCmColor, OdString, OdResBuf, EdgeArray,
  OdDbObjectIdArray, OdDbObjectId, VectorString

枚举：
  OpenMode, HatchPatternType, HatchLoopType, HatchStyle,
  ACIcolorMethod, LineWeight, ValueType

模块级函数：
  odcmAcadPalette, createPolarArrayParameters, createPathArrayParameters,
  createEdgeRefFromEntity, createPolarArrayInstance,
  setPathForPathParameters, releaseEdgeRef,
  oddbCreateEdgesFromEntity, oddbAppendLoopFromPickPoint
```

### 路径 2：AutoLISP 执行

- **引擎**：ODA 内置 `OdLspInterpreter`
- **入口**：`viewer.appCore.ExecuteLisp(code)`
- **支持**：`(command "NAME" ...)` 调用 ODA 注册命令、`tblsearch`/`tblnext` 表遍历
- **不支持**：VLA/VLAX 函数、交互函数（getpoint、getstring 等）、UI 函数
- **错误处理**：返回 JSON 格式的错误信息

### 路径 3：WASM 命令执行

- **入口**：`viewer.execute(name, args)` → `appCore.ExecuteCommand(name, vecArgs)`
- **命令注册**：ODA 内部 `odedRegCmds()->executeCommand`
- **别名映射**：`resolveCommandAlias` 支持 [[AutoCAD]] 风格命令别名（如 `DIMDIAMETER` → `DimDiametric`）
- **系统变量**：`TryExecuteAsSysVar` 处理同名系统变量的读写
- **命令列表**：`GetCommandNames()` 返回所有可用命令名（大写）

---

## WASM 导出的 CAD 能力（AutoCAD 功能对照）

### CadCore（App）主要方法

| 方法组 | 方法 | 说明 |
|--------|------|------|
| 文件 | `OpenFile`, `Update`, `Resize`, `Redraw`, `regenAll` | [[文件操作]]与显示刷新 |
| 视图 | `Zoom`, `ZoomExtents`, `Dolly`, `Orbit` | 视图控制 |
| 命令 | `ExecuteCommand` (Asyncify) | 执行 ODA 注册命令 |
| 交互 | `ProvidePoint`, `ProvideEmptyInput`, `ProvideCancel`, `ProvideKeyword` | 命令交互输入 |
| 坐标 | `ScreenToWorld`, `WorldToScreen`, `SnapScreenPoint` | 坐标变换 |
| 捕捉 | `SetSnapMode`, `GetSnapMode`, `SetSnapEnabled`, `GetSnapEnabled` | 对象捕捉 |
| 选择 | `HoverHighlight`, `ClearHoverHighlight`, `SetPickfirst` | 选择集 |
| 布局 | `GetLayoutNames`, `GetActiveLayoutName`, `SwitchLayout` | 布局管理 |
| CDA | `GetEntityProperties`, `SetEntityProperty`, `GetEntityClassName` | 属性读写 |
| LISP | `ExecuteLisp` | AutoLISP 执行 |
| 比对 | `StartCompare`, `StartObjectCompare`, `ExitCompare` | DWG 比对 |
| 命令名 | `GetCommandNames`, `GetHatchPatternNames` | 命令/图案查询 |
| 字体 | `GetMissingFonts`, `GetAvailableFonts`, `ApplyFontSubstitution` | 字体管理 |

### AutoCAD 功能对照表

| 能力域 | 已导出的 ODA WASM 类 | [[AutoCAD]] 对应命令 |
|--------|---------------------|-----------------|
| **基本绘图** | OdDbLine, OdDbCircle, OdDbArc, OdDbEllipse, [[OdDbPolyline]], OdDbSpline, OdDbPoint | LINE, CIRCLE, ARC, ELLIPSE, PLINE, SPLINE, POINT |
| **高级绘图** | OdDbHatch, OdDbRegion, OdDb3dSolid, OdDbSurface, OdDbSubDMesh | HATCH, REGION, BOX/CYLINDER, SURFACE, MESH |
| **文字** | OdDbText, OdDbMText, OdDbTable | TEXT, MTEXT, TABLE |
| **标注** | OdDbAlignedDimension, OdDbRotatedDimension, OdDbRadialDimension, OdDbDiametricDimension, OdDbOrdinateDimension | DIMALIGNED, DIMLINEAR, DIMRADIUS, DIMDIAMETER, DIMORDINATE |
| **块与引用** | OdDbBlockTable, OdDbBlockTableRecord, OdDbBlockReference, OdDbMInsertBlock | BLOCK, INSERT, MINSERT |
| **属性** | OdDbAttribute, OdDbAttributeDefinition | ATTDEF, ATT |
| **图层** | OdDbLayerTable, OdDbLayerTableRecord | LAYER |
| **线型** | OdDbLinetypeTable, OdDbLinetypeTableRecord | LINETYPE |
| **文字样式** | OdDbTextStyleTable, OdDbTextStyleTableRecord | STYLE |
| **标注样式** | OdDbDimStyleTable, OdDbDimStyleTableRecord | DIMSTYLE |
| **颜色** | OdCmColor (RGB/ACI) | COLOR |
| **阵列** | OdDbAssocArrayPolarParameters, OdDbAssocArrayPathParameters | ARRAYPOLAR, ARRAYPATH |
| **变换** | OdGeMatrix3d (移动/旋转/缩放/镜像) | MOVE, ROTATE, SCALE, MIRROR |
| **外部参照** | OdDbXRefMan, OdDbXRefManExt | XREF |
| **光栅图像** | OdDbRasterImage, OdDbRasterImageDef | IMAGEATTACH |
| **视口** | OdDbViewport, OdDbViewportTableRecord | VPORTS |
| **布局** | GetLayoutNames, SwitchLayout | LAYOUT |
| **选择** | OdDbSelectionSet, HoverHighlight, SetPickfirst | SELECT |
| **捕捉** | SetSnapMode/GetSnapMode, OsnapMode 枚举 | OSNAP |
| **比对** | StartCompare, StartObjectCompare | DWGCOMPARE |
| **撤销/重做** | Undo/Redo | UNDO, REDO |
| **LISP** | ExecuteLisp + OdLspInterpreter | AutoLISP |
| **CDA 属性** | Get[[Entity]]Properties, Set[[Entity]]Property | PROPERTIES |

### 命令别名映射（CadCore resolveCommandAlias）

```
ARC_CSE       → Arc
ARC_SCE       → Arc
ARC_SCA       → Arc
ARC_CSL       → Arc
ARC_CSA       → Arc
ARC_SCL       → Arc
ARC_SEA       → Arc
ARC_SER       → Arc
CIRCLE_2P     → Circle
CIRCLE_3P     → Circle
CIRCLE_TTR    → Circle
CIRCLE_TTT    → Circle
DIMDIAMETER   → DimDiametric
DIMCENTER     → CenterMark
LEADER_A      → LEADER
ELLIPSE_AE    → Ellipse
ELLIPSE_C     → Ellipse
POINT_S       → Point
REVCLOUD_*    → RevCloud
```

---

## RAG 代码示例库

### 示例列表（32 个）

| 类别 | 示例文件 |
|------|----------|
| 基本图元 | `basic_line.js`, `basic_arc.js`, `basic_circle.js`, `basic_ellipse.js` |
| 多段线 | `polyline_lightweight.js`, `polyline_2d_width.js`, `polyline_3d.js` |
| 点/样条 | `point_create.js`, `spline_create.js` |
| 文字 | `text_single.js`, `text_multi.js` |
| 标注 | `dimension_aligned.js`, `dimension_rotated.js`, `dimension_radial.js` |
| 填充 | `hatch_pattern.js`, `hatch_solid.js`, `hatch_polyline_boundary.js` |
| 图层/颜色 | `layer_create.js`, `layer_multiple.js`, `color_set.js` |
| 块 | `block_create.js` |
| 阵列 | `array_rectangular.js`, `array_polar.js`, `array_path.js` |
| 三维 | `solid_3d_box.js`, `solid_3d_cylinder.js`, `solid_trace.js` |
| 变换 | `transform_move.js` |
| 查询 | `query_drawing_info.js`, `query_layers.js` |
| 编辑 | `entity_erase.js`, `entity_iterate.js` |

### 示例元数据格式

```javascript
// @title: 创建直线
// @tags: line, 直线, 基本图形, OdDbLine
// @api: OdDbLine, OdGePoint3d
// @description: 使用 OdDbLine 创建一条直线
```

### 索引构建

```bash
cd server/rag && python build_index.py --code-source ./code_examples
```

---

## System Prompt 分析

### 当前结构

| 模块 | 行数（约） | 内容 | 评价 |
|------|-----------|------|------|
| 角色定义 | 1-3 | "DrawingWebApp 的 CAD 智能助手" | ⚠️ 定位模糊，未明确等同 [[AutoCAD]] |
| 视觉能力 | 5-7 | [[Vision]] 图像分析 | ✅ 良好 |
| 核心原则 | 9-14 | 代码优先、先查后做、任务分解、执行验证、错误修正 | ✅ 良好 |
| 工具选择表 | 16-30 | 11 个工具的场景映射 | ✅ 良好 |
| 坐标与单位 | 32-36 | WCS、默认尺寸参考 | ✅ 良好 |
| JS 代码指南 | 38-150 | 预置变量、类列表、关键规则、代码示例 | ✅ 较完整 |
| LISP 指南 | 152-185 | 适用场景、禁止函数、代码风格 | ✅ 良好 |
| 规划指南 | 187-200 | plan_task 使用示例 | ✅ 良好 |
| 分析工具指南 | 202-295 | 图框/建筑/测量详细指南 | ✅ 良好 |
| 知识库 | 297-302 | RAG 使用策略 | ✅ 良好 |
| ReAct 循环 | 304-312 | 规划→检索→执行→观察→修正→验证 | ✅ 良好 |
| 示例 | 314-330 | 常见操作示例 | ✅ 良好 |

### 动态部分

`buildSystemPrompt(drawingState)` 根据当前图纸状态动态追加：
- 实体总数
- 图层数
- 实体类型分布
- 图层列表

---

## 前端执行管线详解

### CommandExecutor 分发逻辑

```
tool output → _classifyOutput() → 分类
  │
  ├─ cadQueryCode   → CadCodeExecutor.executeCadCode() → queryResult
  ├─ cadCode        → CadCodeExecutor.executeCadCode() → entityCount
  ├─ lispCode       → CadCodeExecutor.executeAutoLisp() → result
  ├─ cadCommand     → viewer.execute(name, args) → result
  ├─ captureRequest → 标记（AiAssistant 后续截图）
  ├─ plan           → 记录（不执行 WASM）
  └─ codeExamples/context → 记录（RAG 检索结果）
```

### AiAssistant 工具栏（附件系统）

AI 助手面板 Header 提供了丰富的交互工具按钮，用户可以在发送消息前附加多种上下文数据：

| # | 按钮 | 图标 | 功能 | 附件类型 | 传递给 LLM 的数据 |
|---|------|------|------|----------|-------------------|
| 1 | **拾取点** | `AimOutlined` | 在图形中点击拾取一个世界坐标点 | `point` | `{ x, y, z }` 世界坐标 |
| 2 | **选择对象** | `SelectOutlined` | 在图形中框选/点选多个实体 | `selection` | `{ count, handles[], classNames[], summary }` |
| 3 | **择取范围** | `GatewayOutlined` | 在图形中框选一个矩形区域 | `region` | `{ mode, points[], bounds: {minX,minY,maxX,maxY} }` |
| 4 | **截图附件** | `CameraOutlined` | 截取当前视图图片 | `screenshot` | `dataUrl`（Base64 图片，发送为 image part） |
| 5 | **引用文件** | `PaperClipOutlined` | 从 `/workspace/` 选择文件引用 | `file` | 文本文件：`{ path, name, size, content }`；二进制文件：`{ path, name, size }` |
| 6 | **清空对话** | `DeleteOutlined` | 清除所有消息和附件 | — | — |
| 7 | **关闭面板** | `CloseOutlined` | 关闭 AI 助手面板 | — | — |

#### 引用文件功能详解

引用文件按钮 (📎) 点击后展开 `WorkspaceFilePicker` 子组件，显示 `/workspace/` 目录的树形文件列表：

- **文本文件**（`.txt/.json/.csv/.xml/.js/.py/.md/.yaml` 等）：前端直接从 Emscripten FS 读取内容（上限 50KB），内容作为附件发送给后端，后端将文件内容以代码块格式注入到 LLM 的用户消息中
- **二进制文件**（`.dwg/.dxf/.pdf` 等 CAD 文件）：仅发送文件路径和元信息，后端提示 LLM 可通过 `execute_js_code` 工具使用 [[WASM API]]（如 `Module.CadCore.ReadFile(path)`）打开和分析该文件
- 工作文件夹为空时，提供"打开文件夹管理"快捷入口，跳转到 TopBar 的 FsViewerPanel

#### 工作文件夹（/workspace/）

TopBar 新增了 **文件夹** 按钮（`FolderOpenOutlined`），点击弹出 `FsViewerPanel` 文件管理器面板：

| 功能 | 说明 |
|------|------|
| **上传文件** | `<input type="file" multiple>` 多选任意格式文件，写入 `/workspace/` |
| **上传文件夹** | `<input type="file" webkitdirectory>` 整个文件夹递归上传，保留子目录结构 |
| **树形浏览** | 递归展示 `/workspace/` 下所有文件和目录，显示文件大小 |
| **删除** | 单个文件或递归删除整个文件夹 |
| **刷新** | 手动刷新文件列表 |

工作文件夹的设计目标是为 AI 助手提供**多文件工作区**——用户可以上传多个 DWG/参考文件，AI 在分析当前打开的图纸时，可以同时读取/对比工作文件夹中的其他文件。

**Emscripten FS 目录结构**：

```
/                          ← FS 根目录（当前打开的 DWG 文件在此）
/workspace/                ← 工作文件夹（用户上传的参考文件）
│   ├── B.dwg
│   ├── specs.json
│   └── 子目录/
│       └── detail.dwg
/uacad/
    ├── Configure/         ← 配置文件 (uacad.json)
    ├── Data/              ← ODA 数据
    ├── References/        ← ODA 引用
    └── Cache/logs/        ← 缓存/日志
```

#### 附件传输机制

所有附件通过 `DrawingStateTransport` 自定义 transport 发送：

1. 用户点击发送时，非截图附件的结构化数据写入 `pendingAttachmentsRef`
2. `DrawingStateTransport.sendMessages()` 将附件注入请求 body 的 `userAttachments` 字段
3. 后端 `POST /api/ai/chat` 解析 `userAttachments`，将每种类型转为自然语言描述注入到最后一条用户消息中

| 附件类型 | 后端注入内容 |
|----------|-------------|
| `point` | 世界坐标 + "请使用此坐标作为位置参数" |
| `selection` | handles 数组 + "使用 `pDb.getOdDbObjectId(handle)` 获取 ObjectId" |
| `region` | 顶点坐标 + 包围盒 + "可用于筛选区域内实体" |
| `file`（文本） | 文件路径 + 完整内容（代码块格式）+ "请根据文件内容回答" |
| `file`（二进制） | 文件路径 + "可通过 [[WASM API]] 打开分析" |
| `screenshot` | "见消息中的图片部分" + Base64 图片作为 image part |

### AiAssistant 反馈闭环

1. **消息到达** → `useEffect` 触发 `executePendingCommands()`
2. **执行成功** → 写入 `appStore.appendOutput` 日志
3. **执行失败** → 组装 `[系统反馈]` + 可选截图 → 发回 LLM 自纠
4. **查询成功** → 组装 `[查询结果]` JSON → 发回 LLM 总结
5. **截图请求** → `captureCurrentView()` / `captureFullExtents()` → 图片发回 LLM [[Vision]] 分析
6. **drawingState** → 每次请求通过 `DrawingStateTransport` 附带当前图纸状态

### CadCodeExecutor 安全机制

- **黑名单**：`eval`, `fetch`, `document`, `window`, `XMLHttpRequest`, `WebSocket` 等危险全局被屏蔽
- **白名单 API**：仅注入上述 ODA 类 + 受限的 `Math`/`JSON`/`Array` 等
- **内存追踪**：Proxy 包装 `createObject` 和 `new` 操作，统一 `.delete()`
- **`patchOptionalArgs`**：为 `OdDbPolyline.addVertexAt` 等方法补默认参数

---

## 改进记录

### 已完成的改进（2026-04-02）

| 问题 | 改进内容 |
|------|---------|
| **产品定位不清** | ✅ 新增"关于 [[WebUACAD]]"章节，明确定义为"功能完备的在线 CAD 系统，等同于 [[AutoCAD]]" |
| **[[AutoCAD]] 命令映射缺失** | ✅ 新增完整的"[[AutoCAD]] 命令 → [[WebUACAD]] 实现方式"映射表（7 个分类，50+ 命令） |
| **JS API 能力边界不明** | ✅ 新增"你的能力"章节 + "三条执行路径"详细说明，明确路径选择策略 |
| **execute_command 工具未充分利用** | ✅ 在修改命令映射表中明确标注 TRIM/FILLET/CHAMFER/OFFSET 等走 LISP/CMD 路径 |
| **缺少常用操作映射表** | ✅ 示例部分按 [[AutoCAD]] 术语分类（绘图/修改/图层/三维/查询/LISP），覆盖用户常见表达 |
| **核心原则不完整** | ✅ 新增第 2 条"命令兜底"原则，明确 JS 无法实现时的降级策略 |

### 已完成的改进（2026-04-02 #2）

| 问题 | 改进内容 |
|------|---------|
| **AI 助手缺少文件引用能力** | ✅ 新增引用文件按钮 (📎)，支持从 `/workspace/` 选择文件，文本文件内容直接注入 LLM 上下文，二进制文件提供 WASM 路径 |
| **缺少多文件工作区** | ✅ 新增工作文件夹 (`/workspace/`)，TopBar 增加文件夹按钮 + FsViewerPanel 管理面板，支持上传文件/文件夹（保留目录结构）、浏览、删除 |
| **AI 助手工具栏能力不完整** | ✅ 工具栏现包含 7 个按钮：拾取点、选择对象、择取范围、截图附件、引用文件、清空对话、关闭面板 |
| **附件系统缺少文件类型** | ✅ 附件类型扩展为 5 种：`point`、`selection`、`region`、`screenshot`、`file`，后端均有对应的上下文注入逻辑 |

### 待改进项

| 问题 | 建议 |
|------|------|
| **RAG 示例缺少部分常见操作** | 可补充 COPY、MIRROR、OFFSET、FILLET 等编辑操作的 JS/LISP 示例 |
| **Viewer 层能力未暴露给 LLM** | 可考虑补充 ViewerService 可直接调用的高级 API（如图层管理、属性修改等快捷方法） |
| **二进制文件 AI 分析路径待完善** | 引用 DWG 文件时 AI 目前只能获得路径提示，后续可在 [[CadCodeExecutor 沙箱]]中暴露 `openDatabase(path)` 等便捷 API |
| **工作文件夹持久化** | `/workspace/` 内容在页面刷新后丢失（Emscripten FS 为内存文件系统），可考虑 IndexedDB 持久化或 OPFS 支持 |

---

## 总结

WebUA[[CAD AI Agent]] 架构已经相当完善：

1. **三条执行路径**（JS 沙箱 / AutoLISP / WASM 命令）覆盖了从精细 API 操作到高级命令执行的全部层次
2. **11 个工具**覆盖了绘图、修改、查询、分析、测量、规划、检索等完整的 CAD 工作流
3. **WASM 导出了 100+ ODA 类**，涵盖了 [[AutoCAD]] 的绝大部分核心功能
4. **ReAct 多步推理** + **[[Vision]] 视觉分析** + **RAG 代码检索** 的闭环机制很成熟
5. **反馈闭环**（执行→反馈→修正→验证）保证了代码执行的可靠性
6. **5 种附件类型**（拾取点/选择对象/区域/截图/引用文件）提供了丰富的用户→AI 上下文传递通道
7. **工作文件夹** (`/workspace/`) 实现了多文件工作区，AI 可跨文件分析和操作

**核心改进方向**：在 System Prompt 中明确告诉 LLM——[[WebUACAD]] 就是 [[AutoCAD]] 的在线版本，具备完整的 [[AutoCAD]] 功能，并提供清晰的 [[AutoCAD]] 命令 → [[WebUACAD]] 实现路径映射。

## 相关笔记

- [[AI 绘图助手 — 实现文档]]
- [[CAD AI Agent 改进计划]]
- [[规划审图 AI 智能体解决方案]]
- [[ai-agent]]
- [[DWG Skill 架构设计]]
- [[RAG 知识库 — AutoCAD 帮助文档检索系统]]
- [[GIS服务 Ribbon 标签页设计规格]]
- [[瞬态批注系统设计文档]]
