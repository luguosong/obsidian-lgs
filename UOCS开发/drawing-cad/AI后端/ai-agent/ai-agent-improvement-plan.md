# CAD AI Agent 改进计划

> 创建日期: 2026-03-17
> 最后更新: 2026-03-17 (Phase 2 增强：双路径并行图框分析)
> 状态: Phase 1-2 已完成，Phase 3-4 待实施

## 改进目标

1. **工具重组**：去掉 11 个碎片化 `draw_xxx` 命令工具，统一用 JS 代码 / LISP 代码模式
2. **多步 ReAct**：服务端 `maxSteps` 从 1 提升至 10，支持"检索→生成→执行→评估→修正"闭环
3. **分析能力增强**：图框识别、建筑轮廓提取、Vision 截图分析
4. **规范合规检查**：基于建筑设计规范的自动审查
5. **多 Agent 编排**：Router → Drawing / Analysis / Modeling / Compliance Agent
6. **C++ WASM 扩展**：支撑上层分析、建模需求的底层 API

## 参考项目

| 项目 | 路径 | 借鉴点 |
|------|------|--------|
| Text2CAD | `E:\DrawingsInWEB\Text2CAD` | 多 Agent 流水线 (Architect→Implementer→Evaluator→Replanner)、视觉评估、Lessons Learned |
| AutoCAD MCP | `E:\DrawingsInWEB\autocadmcp` | 统一通过代码执行（不需要碎片化命令工具）、MCP 标准协议 |

## 实施阶段

### Phase 1: 工具重组 + 多步 ReAct ✅

**目标**: 删除 `draw_xxx` 命令工具，统一代码执行模式，启用服务端多步推理

**改动文件**:

| 文件 | 改动内容 |
|------|---------|
| `server/tools/cadTools.js` | 删除 11 个 draw_xxx 工具；合并 query_drawing 为 execute_js_code 的 isQuery 参数；新增 plan_task；重写 CORE_PROMPT |
| `server/index.js` | maxSteps 从 1 改为 10 |
| `src/services/CommandExecutor.js` | 简化分发逻辑，去掉 cadCommand 分支（标记 deprecated） |

**完成状态**: ✅ 已完成 (2026-03-17)

**变更详情**:

1. **工具从 16 个减少为 7 个** (`server/tools/cadTools.js`):
   - `execute_js_code` — JS 代码执行（绘图 + 修改 + 查询，通过 isQuery 参数区分）
   - `execute_lisp_code` — LISP 代码执行
   - `execute_command` — WASM 命令执行（预留，用于 TRIM/FILLET 等复杂命令）
   - `plan_task` — 任务分解规划
   - `capture_viewport` — 截取当前视图供 Vision 分析
   - `search_code_examples` — RAG 代码示例检索
   - `search_help_docs` — RAG 帮助文档检索
   - ~~draw_line, draw_circle, draw_rectangle, draw_polyline, draw_arc, draw_arc_center, draw_ellipse, draw_polygon, draw_text, draw_mtext, draw_donut~~ (已删除)

2. **CORE_PROMPT 重写** (`server/tools/cadTools.js`):
   - 核心原则：代码优先、先查后做、任务分解、执行验证、错误修正
   - 工具选择策略表格化：场景→工具→说明
   - ODA API 参考保留（实体类、几何类、工具类、枚举）
   - 新增 plan_task / capture_viewport 使用指南
   - 新增查询代码模板（统计实体、查询图层）

3. **maxSteps 提升** (`server/index.js`):
   - 从 1 改为 10，启用服务端 ReAct 循环
   - LLM 现在可以在一次请求中完成：search_code_examples → execute_js_code 的连续调用

4. **CommandExecutor 重构** (`src/services/CommandExecutor.js`):
   - 提取 `_classifyOutput()` 分类函数，统一判断 output 类型
   - 新增 `_handleCapture()`、`_handlePlan()` 处理器
   - 保持对旧格式（cadCommand）的向后兼容

5. **AiAssistant 更新** (`src/components/AiAssistant/AiAssistant.jsx`):
   - TOOL_LABELS 映射更新为新工具名（保留旧名兼容）
   - resolveToolName() 适配新的 output 格式
   - ToolCallBadge 支持 plan_task / capture_viewport 状态显示
   - 截图请求处理：收到 captureRequest 时自动截图并发送给 LLM
   - 提取 `_sendWhenReady()` 辅助函数减少重复

6. **Cursor 规则更新** (`.cursor/rules/ai-server.mdc`):
   - 工具列表更新为 7 个
   - 执行模式表格更新
   - maxSteps 更新为 10

---

### Phase 2: 分析能力增强 ✅

**目标**: 增强图纸分析能力 — 图框双路径并行分析、区域截图、Vision 精细分析

**改动文件**:

| 文件 | 改动内容 |
|------|---------|
| `server/tools/analysisTools.js` (新) | analyze_drawing, detect_title_blocks, extract_building_info, measure_entities 工具 |
| `src/services/ScreenshotService.js` (新) | 截图服务：captureCurrentView, captureFullExtents, captureRegion, captureMultipleRegions, saveViewState, restoreViewState |
| `src/services/TitleBlockAnalyzer.js` (新) | 图框分析管线：双路径并行采集 → 交叉验证 → 逐框截图 → Vision 精细分析 |
| `src/services/CadCodeExecutor.js` | 沙箱新增: OdDbAttribute, OdDbAttributeDefinition, OdDbViewport |
| `src/services/CommandExecutor.js` | 查询结果传递 needsScreenshot, analysisType 标记 |
| `src/components/AiAssistant/AiAssistant.jsx` | 图框分析按钮 + AnalysisPanel（进度/确认/结果 UI） |
| `src/components/AiAssistant/AiAssistant.module.css` | 分析面板样式（进度、确认卡片、结果展示） |
| `server/index.js` | 新增 /api/ai/vision-analyze 端点（一次性 Vision 分析） |
| `server/tools/cadTools.js` | CORE_PROMPT 更新双路径分析指南；导入 analysisTools |

**完成状态**: ✅ 已完成 (2026-03-17)

**变更详情**:

1. **新增 4 个分析工具** (`server/tools/analysisTools.js`):
   - `analyze_drawing` — 综合图纸分析（程序化查询 + Vision 截图）
   - `detect_title_blocks` — 图框检测（双路径并行分析管线）
   - `extract_building_info` — 建筑信息提取（轮廓线 + 文字标注 + 图层筛选）
   - `measure_entities` — 实体测量（距离、面积计算）
   - 所有分析工具返回 `cadQueryCode` + `needsScreenshot` 标记

2. **ScreenshotService 增强** (`src/services/ScreenshotService.js`):
   - `captureCurrentView()` — 截取当前视图
   - `captureFullExtents(viewer)` — ZoomExtents 后截取全图
   - `saveViewState(viewer)` — 保存 GS 视图相机参数（position, target, upVector, fieldWidth, fieldHeight）
   - `restoreViewState(viewer, state)` — 恢复视图状态并释放 embind 几何对象
   - `captureRegion(viewer, extents)` — 缩放到指定矩形区域后截图（基于 ZoomToRect）
   - `captureMultipleRegions(viewer, regions)` — 批量区域截图（自动保存/恢复视图）
   - `extractBase64()` — 提取纯 base64（Vercel AI SDK 需要）
   - `buildScreenshotParts()` — 构建截图消息 parts

3. **新增图框分析管线** (`src/services/TitleBlockAnalyzer.js`):
   - **Phase 1: 并行采集** — `Promise.allSettled` 同时启动 Vision 和 WASM 路径
     - Vision 路径：截取当前视图 + 全图 → `/api/ai/vision-analyze` → 识别图框数量
     - WASM 路径：内置查询代码遍历 BlockReference + Attribute + getGeomExtents
     - 先完成的立即通过 `onProgress` 回调通知前端
   - **Phase 2: 交叉验证** — 比对图框数量，不一致时返回 `needsConfirmation: true`
   - **Phase 3: 逐框截图** — 调用 `captureMultipleRegions()` 对每个图框 ZoomToRect 截图
   - **Phase 4: Vision 精细分析** — 所有图框截图 + API 属性数据 → Vision LLM 分析标签栏详情
   - 支持 `cancel()` 中止和 `continueWithBlocks()` 用户确认后继续

4. **新增 Vision 分析端点** (`server/index.js`):
   - `POST /api/ai/vision-analyze` — 一次性 `generateText` 调用（非流式）
   - 接收 images(base64[]) + prompt + apiData，返回结构化 JSON
   - 自动从 LLM 返回文本中提取 JSON 对象

5. **AiAssistant 集成** (`src/components/AiAssistant/AiAssistant.jsx`):
   - Header 新增"图框分析"按钮（BlockOutlined 图标）
   - `handleTitleBlockAnalysis` — 创建 TitleBlockAnalyzer 启动管线
   - `handleMismatchChoice` — 用户选择后继续分析
   - `AnalysisPanel` 组件 — 根据 phase 展示不同 UI：
     - collecting/zooming/analyzing → 进度指示器
     - visionDone/apiDone → 单路径完成通知
     - mismatch → 确认卡片（显示两条路径数量 + 三个按钮）
     - done → 结果展示（摘要 + 每个图框的属性和 Vision 分析）
     - error → 错误信息

6. **CORE_PROMPT 更新**:
   - detect_title_blocks 描述更新为"双路径并行分析"
   - 新增管线流程说明（4 个 Phase）
   - 说明前端 UI 按钮也可直接触发

7. **CadCodeExecutor 沙箱扩展** (`src/services/CadCodeExecutor.js`):
   - 新增 `OdDbAttribute` — 属性读取（tag, textString）
   - 新增 `OdDbAttributeDefinition` — 属性定义读取
   - 新增 `OdDbViewport` — 视口信息读取

8. **WASM 导出现状确认**:
   - OdDbBlockReference: ✅ (position, rotation, scaleFactors, blockTableRecord, attributeIds)
   - OdDbAttribute: ✅ (tag, textString via OdDbText inheritance)
   - OdDbAttributeDefinition: ✅ (tag, prompt, textString)
   - OdDbEntity.getGeomExtents(): ✅
   - CadCore.ZoomToRect(minX, minY, maxX, maxY): ✅
   - CadCore.getViewAt0() → position/target/upVector/fieldWidth/fieldHeight/setView: ✅
   - OdDbLayout: ❌ (需要 P0 级 C++ 新增，暂不影响基本分析功能)

---

### Phase 3: 规范合规系统（待实施）

**目标**: 基于建筑设计规范（GB 50016 防火、GB 50352 通则等）的自动合规检查

**计划改动**:

| 文件 | 改动内容 |
|------|---------|
| `server/rag/standards/` (新目录) | 规范条文数据 |
| `server/rag/build_standards_index.py` (新) | 规范知识库索引 |
| `server/tools/complianceTools.js` (新) | check_compliance, search_building_standards |

**完成状态**: ⬜ 待实施

---

### Phase 4: 多 Agent 编排 + 3D 建模（待实施）

**目标**: Router 路由 → 专业 Agent 分工，支持 2D→3D 建模

**计划改动**:

| 文件 | 改动内容 |
|------|---------|
| `server/agents/router.js` (新) | 意图识别 + 路由 |
| `server/agents/drawingAgent.js` (新) | 绘图 Agent |
| `server/agents/analysisAgent.js` (新) | 分析 Agent |
| `server/agents/modelingAgent.js` (新) | 建模 Agent |
| `server/agents/complianceAgent.js` (新) | 合规 Agent |

**完成状态**: ⬜ 待实施

---

## C++ WASM 开发计划 (DrawingWeb)

### P0: 图纸分析基础（支持图框识别）

| 功能 | Wrapper 文件 | 导出 API |
|------|-------------|----------|
| OdDbAttribute 读取 | `OdDbAttributeWrapper.cpp` (新) | `tag()`, `textString()`, `position()`, `layer()` |
| OdDbAttributeDefinition | 同上 | `tag()`, `prompt()`, `textString()` |
| OdDbBlockReference 增强 | 已有，需补充 | `attributeIterator()` — 遍历属性 |
| Layout / Paper Space | `OdDbLayoutWrapper.cpp` (新) | `getLayoutName()`, `getTabOrder()`, `getBlockTableRecordId()` |
| Viewport 信息 | `OdDbViewportWrapper.cpp` (新) | `viewCenter()`, `viewHeight()`, `width()`, `height()` |
| OdDbDatabase 扩展 | 已有，需补充 | `getLayoutDictionaryId()`, `getPaperSpaceId()` |

### P1: 几何分析（支持建筑轮廓提取）

| 功能 | 说明 |
|------|------|
| 实体 BoundingBox | 各实体 `getGeomExtents()` |
| 闭合多段线面积 | `OdDbPolyline::getArea()` |
| XData 读取 | `xData()` / `getXData()` |
| 块内实体遍历 | `OdDbBlockTableRecord::newIterator()` |
| 多段线坐标提取 | `getPoint2dAt(index)`, `numVerts()` |

### P2: 三维建模（支持 2D→3D 拉伸）

| 功能 | 说明 |
|------|------|
| OdDbRegion 创建 | `createFromCurves(entityArray)` |
| OdDb3dSolid 拉伸 | `createExtrudedSolid(region, direction, sweepOptions)` |
| OdDb3dSolid 布尔 | `booleanOper(BoolOperType, solid)` |
| 变换矩阵 | `setToTranslation(vector)` |

### P3: 高级分析（支持规范检查）

| 功能 | 说明 |
|------|------|
| 标注值读取 | `getMeasurement()`, `getDimText()` |
| 面积计算 | `OdDbHatch/Region::getArea()` |
| 距离计算 | `OdGePoint3d::distanceTo()` |
| 文字搜索 | `textString()`, `contents()` |
| 图层过滤 | `isOff()`, `isFrozen()`, `colorIndex()` |

---

## 执行模式对比

### 改造前 (4 种模式, 16 个工具)

```
├── 命令模式 (11 个 draw_xxx)     ← 碎片化，LLM 选择困难
├── JS 代码模式 (execute_cad_code)
├── JS 查询模式 (query_drawing)
├── LISP 代码模式 (execute_autolisp)
├── RAG 检索 (2 个)
```

### 改造后 (2+1 种模式, 11 个工具)

```
├── JS 代码模式 (execute_js_code)        ← 主力，绘图/修改/查询
├── LISP 代码模式 (execute_lisp_code)     ← 辅助，适合 (command ...) 场景
├── WASM 命令模式 (execute_command)       ← 预留，将来用于复杂命令
├── 分析工具 (4 个)
│   ├── analyze_drawing                  ← 综合分析（查询+截图）
│   ├── detect_title_blocks              ← 图框检测
│   ├── extract_building_info            ← 建筑信息提取
│   └── measure_entities                 ← 实体测量
├── 任务规划 (plan_task)
├── 视图截取 (capture_viewport)
├── RAG 检索 (2 个)
```
