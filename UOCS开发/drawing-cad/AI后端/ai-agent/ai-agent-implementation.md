# AI 绘图助手 — 实现文档

## 架构总览

```
┌──────────────────────────────────────────────────────────────┐
│  前端 (React + Vite, port 3000)                               │
│                                                               │
│  AiAssistant.jsx                                              │
│    ├─ useChat (from @ai-sdk/react)                            │
│    │    POST /api/ai/chat ─── Vite proxy ──┐                  │
│    │    请求体包含 messages + drawingState                     │
│    ├─ DrawingStateTransport (自定义 transport)                 │
│    │    └─ 每次请求自动注入当前图纸状态                         │
│    ├─ 截图分析按钮 (CameraOutlined)                            │
│    │    └─ canvas.toDataURL() → 多模态消息发送给 LLM           │
│    ├─ 执行反馈注入                                             │
│    │    └─ 失败/查询结果 → 自动追加 [系统反馈] 消息给 LLM      │
│    ├─ 渲染消息列表 + 工具调用状态                               │
│    └─ CommandExecutor                                          │
│         ├─ cadCommand 模式: viewer.execute(name, args)         │
│         ├─ cadCode 模式: CadCodeExecutor.executeCadCode(code)  │
│         └─ cadQueryCode 模式: 执行查询代码 + setResult()        │
└──────────────────────────────────┬────────────────────────────┘
                                   │ HTTP (UI Message Stream)
┌──────────────────────────────────▼────────────────────────────┐
│  后端 (Express + Vercel AI SDK, port 3001)                    │
│                                                               │
│  index.js                                                     │
│    ├─ API Key 安全保管 (.env)                                  │
│    ├─ 动态 System Prompt 组装                                  │
│    │    ├─ CORE_PROMPT（固定核心规则 ~120 行）                  │
│    │    └─ buildSystemPrompt(drawingState) 注入图纸状态        │
│    ├─ streamText() 调用 LLM                                   │
│    │    ├─ system: 动态 System Prompt                          │
│    │    ├─ tools: 16 个工具                                    │
│    │    ├─ maxSteps: 15 (多轮工具调用 / ReAct 循环)            │
│    │    └─ 支持多模态消息 (text + image)                       │
│    └─ pipeUIMessageStreamToResponse()                         │
│                                                               │
│  tools/cadTools.js                                            │
│    ├─ 11 个快捷绘图工具 (draw_line, draw_circle, ...)          │
│    ├─ 1 个 JS 代码生成工具 (execute_cad_code)                  │
│    ├─ 1 个图纸查询工具 (query_drawing)                         │
│    ├─ 1 个 RAG 知识检索工具 (search_cad_knowledge)             │
│    ├─ 1 个 RAG 代码示例检索工具 (search_cad_code_examples)     │
│    ├─ CORE_PROMPT + buildSystemPrompt()                        │
│    └─ SYSTEM_PROMPT (向后兼容)                                 │
└──────────────────────────────────┬────────────────────────────┘
                                   │
              ┌────────────────────▼───────────────────┐
              │  LLM (GPT-4o, 支持多模态)               │
              │  Function Call + Vision                 │
              └────────────────────┬───────────────────┘
                                   │
              ┌────────────────────▼───────────────────┐
              │  RAG 微服务 (FastAPI + ChromaDB, :3002) │
              │  /search      — 帮助文档检索            │
              │  /search_code — 代码示例检索            │
              └────────────────────────────────────────┘
```

### 三种执行模式

| 模式 | 触发工具 | 前端执行方式 | 适用场景 |
|---|---|---|---|
| **命令模式** | `draw_line`, `draw_circle` 等 | `viewer.execute(name, args)` | 简单基础图形 |
| **代码模式** | `execute_cad_code` | `CadCodeExecutor.executeCadCode(code)` | 复杂图形、属性设置、图层操作 |
| **查询模式** | `query_drawing` | `CadCodeExecutor` + `setResult()` | 图纸信息查询、实体分析 |

### 数据流

1. 用户在 AI 助手面板输入自然语言描述（如 "画一个带砖块填充的圆"）
2. `useChat` 通过 `DrawingStateTransport` POST 到 `/api/ai/chat`，请求体自动包含 `drawingState`（实体统计、图层列表）
3. Vite proxy 转发请求到后端 `http://localhost:3001/api/ai/chat`
4. 后端 `buildSystemPrompt(drawingState)` 动态组装 System Prompt（核心规则 + 图纸状态）
5. `streamText()` 将消息 + 动态 System Prompt + 16 个 Tool 定义发给 LLM
6. LLM 根据任务复杂度选择工具：
   - 简单图形 → 调用 `draw_line` 等快捷工具
   - 复杂图形 → 先调用 `search_cad_code_examples` 获取参考代码，再调用 `execute_cad_code` 生成 JS 代码
   - 图纸分析 → 调用 `query_drawing` 生成查询代码
   - 知识查询 → 调用 `search_cad_knowledge` 检索帮助文档
7. 后端 tool 的 `execute` 函数运行，返回结果：
   - 快捷工具 → `{ cadCommand: { name, args }, description }`
   - 代码工具 → `{ cadCode: "...js code...", description }`
   - 查询工具 → `{ cadQueryCode: "...js code...", isQuery: true, description }`
   - RAG 工具 → `{ context / codeExamples, description }`
8. 结果回传给 LLM，LLM 生成最终文字回复
9. 整个过程通过 UI Message Stream 协议流式推送给前端
10. 前端 `CommandExecutor` 检测到新的 tool result，分发执行：
    - `cadCommand` → `viewer.execute()`
    - `cadCode` → `CadCodeExecutor.executeCadCode()`
    - `cadQueryCode` → `CadCodeExecutor.executeCadCode()` + 收集 `setResult()` 数据
11. **执行反馈**：如果代码执行失败，或查询产生结果，自动将反馈注入对话（附带截图），LLM 可据此自我修正（ReAct 循环）

### 关键设计决策

- **API Key 在后端** — 前端不接触任何密钥
- **Tool 定义在后端** — LLM 的 Function Calling Schema 由后端控制
- **命令执行在前端** — 因为 WASM viewer 在浏览器中运行
- **混合模式** — 简单图形用命令模式（可靠快速），复杂图形用代码模式（灵活强大），分析用查询模式
- **动态 Prompt** — 核心规则固定 (~120 行)，图纸状态动态注入，代码示例按需 RAG 检索
- **沙箱安全** — JS 代码在受控环境中执行，黑名单机制禁止危险 API
- **自动内存管理** — 沙箱自动追踪和释放 ODA embind 对象
- **执行反馈闭环** — 失败信息和查询结果自动回传 LLM，支持自我修正
- **多模态分析** — 支持截图发送给 LLM，让 AI "看到"图纸进行分析

---

## 文件结构

```
DrawingWebApp/
├── server/                          # AI 后端服务
│   ├── package.json
│   ├── .env.example                 # API Key 配置模板
│   ├── .env                         # 实际配置（不提交 git）
│   ├── .gitignore
│   ├── index.js                     # Express 入口（动态 Prompt + 多模态支持）
│   ├── rag/                         # RAG 知识库微服务
│   │   ├── build_index.py           # 文档 + 代码示例索引构建
│   │   ├── rag_server.py            # FastAPI 检索服务（/search + /search_code）
│   │   ├── requirements.txt
│   │   ├── chroma_db/               # ChromaDB 持久化数据
│   │   └── code_examples/           # ODA API 代码示例库（31 个文件）
│   │       ├── basic_line.js
│   │       ├── basic_circle.js
│   │       ├── polyline_lightweight.js
│   │       ├── hatch_pattern.js
│   │       ├── dimension_aligned.js
│   │       ├── array_polar.js
│   │       ├── layer_create.js
│   │       ├── entity_iterate.js
│   │       ├── query_drawing_info.js
│   │       ├── query_layers.js
│   │       └── ... (31 files total)
│   └── tools/
│       └── cadTools.js              # CAD 工具定义 + CORE_PROMPT + buildSystemPrompt
│
├── src/
│   ├── components/
│   │   └── AiAssistant/
│   │       ├── AiAssistant.jsx      # AI 助手面板（图纸状态 + 截图 + 反馈）
│   │       └── AiAssistant.module.css
│   ├── context/
│   │   └── ViewerContext.jsx        # 提供 viewerRef + moduleRef
│   └── services/
│       ├── CommandExecutor.js       # CAD 命令/代码/查询 分发执行器
│       ├── CadCodeExecutor.js       # JS 代码沙箱执行器（含 setResult）
│       └── ViewerService.js         # CAD Viewer 核心服务
│
├── docs/
│   ├── ai-agent-implementation.md   # 本文档
│   └── rag-knowledge-base.md        # RAG 知识库文档
│
├── vite.config.js                   # 添加了 /api proxy
└── package.json                     # 添加了 @ai-sdk/react 依赖
```

---

## 快速启动

### 前置条件

- Node.js 18+
- Python 3.10+（RAG 服务需要）
- OpenAI API Key（或兼容接口的 Key）

### 步骤

```bash
# 配置 API Key
cd DrawingWebApp/server
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

# 安装后端依赖（首次）
cd DrawingWebApp/server
npm install

# 构建代码示例索引（首次或示例更新后）
cd DrawingWebApp/server/rag
pip install -r requirements.txt
python build_index.py --code-source ./code_examples

# 启动 RAG 服务
python rag_server.py
# 输出: 📚 WebUACAD RAG 知识库服务启动中... 端口: 3002

# 启动后端（另一个终端）
cd DrawingWebApp/server
npm run dev
# 输出: 🤖 WebUACAD CAD AI Server running at http://localhost:3001

# 启动前端（另一个终端）
cd DrawingWebApp
npm run dev
# 输出: Vite dev server running at http://localhost:3000

# 打开浏览器 → 点击右侧 AI 按钮 → 开始对话
```

### 验证后端

```bash
curl http://localhost:3001/api/ai/health
# 返回: {"status":"ok","model":"gpt-4o","tools":["draw_line",...,"query_drawing","search_cad_code_examples"]}

curl http://localhost:3002/health
# 返回: {"status":"ok","chunks":...,"code_examples":31,...}
```

---

## 可用工具列表

### 快捷绘图工具（命令模式）

| 工具名 | 说明 | CAD 命令 | 参数 |
|---|---|---|---|
| `draw_line` | 直线 | `LINE` | start_point, end_point |
| `draw_circle` | 圆 | `CIRCLE` | center, radius |
| `draw_rectangle` | 矩形 | `RECTANG` | corner1, corner2 |
| `draw_polyline` | 多段线 | `PLINE` | points[], closed |
| `draw_arc` | 圆弧(三点) | `ARC` | start_point, through_point, end_point |
| `draw_arc_center` | 圆弧(圆心) | `ARC_SCA` | start_point, center, angle |
| `draw_ellipse` | 椭圆 | `ELLIPSE` | axis_endpoint1, axis_endpoint2, minor_axis_length |
| `draw_polygon` | 正多边形 | `POLYGON` | sides, center, radius |
| `draw_text` | 单行文字 | `TEXT` | position, text, height, rotation |
| `draw_mtext` | 多行文字 | `MTEXT` | position, text, width, height |
| `draw_donut` | 圆环 | `DONUT` | inner_radius, outer_radius, center |

### JS 代码生成工具（代码模式）

| 工具名 | 说明 | 参数 |
|---|---|---|
| `execute_cad_code` | 生成 JS 代码直接调用 ODA WASM API | code, description |

**支持的功能远超快捷工具**：填充(Hatch)、标注(Dimension)、三维实体(3D Solid)、
极坐标/路径/矩形阵列(Array)、带宽度的多段线、自定义线型、图层创建和设置、
颜色/线宽/线型属性、实体变换(Transform)等。

### 图纸查询工具

| 工具名 | 说明 | 参数 |
|---|---|---|
| `query_drawing` | 查询图纸信息（图层、实体统计、属性等） | code, description |

查询代码在沙箱中执行，最后调用 `setResult(data)` 返回结构化结果给 LLM。

### 知识检索工具

| 工具名 | 说明 | 参数 |
|---|---|---|
| `search_cad_knowledge` | 检索 WebUACAD 帮助文档 | query |
| `search_cad_code_examples` | 检索 ODA API 代码示例库 | query |

`search_cad_code_examples` 从包含 31 个代码示例的向量库中检索最相关的代码片段，
LLM 以此作为参考生成更准确的 ODA WASM API 代码。

---

## CadCodeExecutor 沙箱设计

### 安全策略：黑名单机制

采用黑名单而非白名单，因为：
- 当前需要画图，后期还需要分析和修改图纸
- 黑名单允许访问所有 ODA API，只禁止危险的浏览器/系统 API
- 随着功能扩展，不需要频繁修改白名单

**禁止的全局对象**：
```
eval, Function, setTimeout, setInterval, setImmediate,
XMLHttpRequest, fetch, WebSocket, Worker, SharedWorker,
importScripts, require, process,
localStorage, sessionStorage, indexedDB, caches,
alert, confirm, prompt, location, history, navigator,
document, window, globalThis, self, top, parent, frames
```

### 内存管理：自动追踪 + cleanup

ODA WASM 的 embind 对象需要手动调用 `.delete()` 释放 C++ 内存。
沙箱通过 Proxy 拦截 `createObject()` 和构造函数调用，自动追踪所有分配的对象，
执行结束后统一 cleanup。

**LLM 生成的代码无需调用 `.delete()`**，大幅降低出错概率。

### 注入的沙箱上下文

```javascript
// 预置变量
pDb          // 当前数据库
modelSpace   // 模型空间 (kForWrite)
OpenMode     // 枚举
OpenAs(id, type, openMode)  // 辅助打开函数
getModelSpace()             // 获取新 modelSpace 引用
setResult(data)             // 返回查询结果给 AI（query_drawing 使用）

// ODA 实体类 (自动追踪 .createObject())
OdDbLine, OdDbCircle, OdDbArc, OdDbHatch, OdDb3dSolid, ...

// 几何类 (自动追踪 new)
OdGePoint3d, OdGePoint2d, OdGeVector3d, OdCmColor, OdString, ...

// 枚举
HatchPatternType, ACIcolorMethod, LineWeight, ...

// 阵列辅助函数
createPolarArrayParameters(), createPolarArrayInstance(), ...

// 标准库
console, Math, JSON, parseInt, parseFloat, ...
```

---

## 动态 System Prompt 架构

### 从静态到动态

旧架构使用一个 ~370 行的静态 `SYSTEM_PROMPT`，硬编码了所有 API 列表和 12 个代码示例。
新架构将其拆分为：

| 组件 | 大小 | 内容 | 来源 |
|---|---|---|---|
| `CORE_PROMPT` | ~120 行 | 绘图规则、工具选择策略、API 类列表、重要规则、ReAct 指导 | 固定 |
| 图纸状态 | 动态 | 实体数、图层列表、实体类型统计 | 前端每次请求传入 |
| 代码示例 | 按需 | 最相关的 3 个代码片段 | RAG `search_cad_code_examples` 工具检索 |

### buildSystemPrompt(drawingState)

```javascript
export function buildSystemPrompt(drawingState) {
  let prompt = CORE_PROMPT
  if (drawingState) {
    // 动态注入: 实体总数、图层数、实体类型分布、图层列表
    prompt += '\n\n## 当前图纸状态\n' + formatState(drawingState)
  }
  return prompt
}
```

### DrawingStateTransport

前端使用自定义 `DrawingStateTransport` 扩展 `DefaultChatTransport`，
在每次 `sendMessages` 时自动调用 `getDrawingStateSafe()` 收集当前图纸信息，
注入到请求 body 的 `drawingState` 字段。

---

## RAG 代码示例库

### 代码示例格式

每个示例文件使用 `@metadata` 头部标注：

```javascript
// @title: 极坐标阵列 Polar Array
// @tags: array, polar, 阵列, 极坐标, 环形, 排列
// @api: OdDbCircle, OdDbVertexRef, createPolarArrayParameters, createPolarArrayInstance
// @description: 将一个圆沿圆周环形排列 8 份

const pCircle = OdDbCircle.createObject();
pCircle.setDatabaseDefaults(pDb, true);
// ... 完整代码
```

### 索引构建

```bash
cd server/rag
python build_index.py --code-source ./code_examples
```

`build_index.py` 解析 `@title`、`@tags`、`@api`、`@description` 元数据，
使用 `BAAI/bge-small-zh-v1.5` 本地模型生成向量，
存入 ChromaDB 的 `cad_code_examples` collection。

### 检索端点

`rag_server.py` 提供 `POST /search_code` 端点，
接收 `{ query, top_k }` 参数，返回最相关的代码示例。

### 当前示例库覆盖（31 个文件）

| 类别 | 示例文件 |
|---|---|
| 基础图形 | basic_line, basic_circle, basic_arc, basic_ellipse, point_create |
| 多段线 | polyline_lightweight, polyline_2d_width, polyline_3d |
| 文字 | text_single, text_multi |
| 填充 | hatch_pattern, hatch_solid |
| 标注 | dimension_aligned, dimension_rotated, dimension_radial |
| 3D 实体 | solid_3d_box, solid_3d_cylinder, solid_trace |
| 阵列 | array_polar, array_path, array_rectangular |
| 图层/颜色 | layer_create, layer_multiple, color_set |
| 块 | block_create |
| 变换 | transform_move |
| 样条线 | spline_create |
| 查询 | entity_iterate, entity_erase, query_layers, query_drawing_info |

---

## 执行反馈与 ReAct 循环

### 执行结果回传

`CommandExecutor` 执行完毕后，`AiAssistant.jsx` 检查执行结果：

- **失败** → 自动追加 `[系统反馈] 执行失败: <错误信息>` 消息给 LLM
- **查询结果** → 自动追加 `[查询结果] <JSON 数据>` 消息给 LLM
- **失败 + 绘图操作** → 同时附带截图，让 LLM 能视觉观察结果

### ReAct 循环（执行-观察-修正）

对于复杂绘图任务，AI 的工作流程：

1. **规划**：分析用户需求，分解步骤
2. **检索**：调用 `search_cad_code_examples` 获取参考代码
3. **执行**：调用 `execute_cad_code` 生成并执行代码
4. **观察**：接收系统反馈（执行结果 + 可选截图）
5. **修正**：如果失败，根据错误信息修正代码并重新执行

后端 `maxSteps: 15` 支持多轮工具调用，足够完成复杂的规划-检索-执行-修正循环。

---

## 多模态图纸分析

### 截图分析

用户点击 AI 助手面板的相机图标按钮，触发：

1. `canvas.toDataURL('image/png')` 截取当前图纸画面
2. 构建多模态消息 `{ parts: [{ type: 'text', text: '请分析...' }, { type: 'image', image: dataUrl }] }`
3. 通过 `sendMessage` 发送给 LLM
4. GPT-4o 的视觉能力分析截图内容，描述图纸上的图形

### 后端支持

- `express.json({ limit: '10mb' })` 支持 base64 图片传输
- Vercel AI SDK 的 `convertToModelMessages` 原生支持多部分消息
- GPT-4o 原生支持 `{ type: 'image', image: base64 }` 格式

---

## 技术选型说明

### 为什么用 Vercel AI SDK？

| 特性 | 自己写 SSE | Vercel AI SDK |
|---|---|---|
| 流式传输 | 手动解析 | `pipeUIMessageStreamToResponse()` 自动处理 |
| 消息管理 | 手动维护数组 | `useChat` Hook 自动管理 |
| Tool Calling | 手动解析 JSON | `tool()` + Zod Schema，类型安全 |
| 多步推理 | 手动循环 | `maxSteps` 参数自动处理 |
| 多模态 | 手动组装格式 | 原生支持 text + image parts |

### 为什么采用混合模式（命令 + 代码生成 + 查询）？

| 维度 | 纯命令模式 | 纯代码模式 | 混合模式 ✓ |
|---|---|---|---|
| 简单图形可靠性 | 高 | 中 | 高（用命令） |
| 复杂图形支持 | 低 | 高 | 高（用代码） |
| 图纸分析 | 不支持 | 可以 | 专用查询工具 |
| LLM Token 消耗 | 低 | 中 | 优化 |
| 扩展性 | 每种实体一个 tool | 无限 | 无限 |

### 为什么用 RAG 而不是训练自己的小模型？

| 方案 | 开发成本 | 维护成本 | 泛化能力 | API 更新 |
|---|---|---|---|---|
| 训练小模型 | 极高 (数据标注+训练) | 高 (每次更新重训) | 低 (只懂训练数据) | 重新训练 |
| 大模型 + RAG ✓ | 低 (整理示例即可) | 低 (添加新示例) | 高 (大模型通用能力) | 添加新示例 |

### LLM 选择

默认使用 OpenAI `gpt-4o`（Function Calling 最成熟，代码生成质量高，支持多模态）。

通过 `.env` 可切换到任何 OpenAI 兼容接口：

```env
# DeepSeek
OPENAI_API_KEY=sk-your-deepseek-key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 通义千问
OPENAI_API_KEY=sk-your-qwen-key
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-max
```

---

## 核心代码解读

### 后端：动态 System Prompt 组装

```javascript
// server/tools/cadTools.js
export const CORE_PROMPT = `你是 DrawingWebApp 的 CAD 绘图智能助手...`  // ~120 行核心规则

export function buildSystemPrompt(drawingState) {
  let prompt = CORE_PROMPT
  if (drawingState) {
    prompt += '\n\n## 当前图纸状态\n'
    // 注入实体数、图层数、实体类型分布、图层列表
  }
  return prompt
}

// server/index.js
app.post('/api/ai/chat', async (req, res) => {
  const { messages, drawingState } = req.body
  const systemPrompt = drawingState ? buildSystemPrompt(drawingState) : SYSTEM_PROMPT
  const result = streamText({
    model: openai.chat(MODEL),
    system: systemPrompt,
    messages: modelMessages,
    tools: cadTools,       // 16 个工具
    maxSteps: 15,          // 支持 ReAct 循环
  })
})
```

### 后端：query_drawing 工具定义

```javascript
// server/tools/cadTools.js
export const queryDrawing = tool({
  description: '查询当前图纸的信息（图层列表、实体统计、特定实体属性等）',
  parameters: z.object({
    code: z.string().describe('查询代码，最后必须调用 setResult(data) 返回结果'),
    description: z.string().describe('查询目的'),
  }),
  execute: async ({ code, description }) => ({
    cadQueryCode: code,
    isQuery: true,
    description,
  }),
})
```

### 前端：CadCodeExecutor 沙箱（含 setResult）

```javascript
// src/services/CadCodeExecutor.js
sandbox.__queryResult = undefined
sandbox.setResult = (data) => {
  sandbox.__queryResult = JSON.parse(JSON.stringify(data))
}

// executeCadCode 返回值
return { success: true, entityCount, queryResult: sandbox.__queryResult }
```

### 前端：CommandExecutor 三模式分发

```javascript
// src/services/CommandExecutor.js
if (hasCadQueryCode) {
  // 查询模式：执行查询代码，收集 setResult 数据
  const result = executeCadCode(part.output.cadQueryCode, Module, viewer)
  // result.queryResult 包含查询结果
} else if (hasCadCode) {
  // 代码模式：沙箱执行 JS 代码
  const result = executeCadCode(part.output.cadCode, Module, viewer)
} else {
  // 命令模式：viewer.execute() 执行命令
  await viewer.execute(name, args)
}
```

### 前端：执行反馈与截图

```javascript
// src/components/AiAssistant/AiAssistant.jsx
if (hasErrors || hasQueryResults) {
  const parts = [{ type: 'text', text: `[系统反馈]\n${feedbackText}` }]
  if (hasErrors) {
    // 附带截图，让 LLM 能视觉观察执行结果
    parts.push({ type: 'image', image: canvas.toDataURL('image/png') })
  }
  sendMessage({ role: 'user', parts })  // 自动触发 LLM 修正
}
```

---

## 后续扩展方向

### 更多代码示例

向 `server/rag/code_examples/` 添加更多 ODA API 示例文件，运行 `build_index.py --code-source ./code_examples` 重建索引即可。LLM 立即获得新的代码参考能力。

### 服务端 CAD 执行

将 tool 的 `execute` 函数改为调用服务端 CAD 程序，实现不依赖前端 WASM 的后台批量绘图、文件生成等。

### 更精细的 Agent Loop

- 每次执行绘图代码后自动截图反馈（不仅限于失败时）
- LLM 主动规划多步绘图策略并按步骤执行验证
- 支持 "画完后检查一下" 这样的用户指令

### 会话记忆

当前通过 `useChat` 的 messages 保持会话上下文。如需跨会话记忆，可在后端加数据库存储。

---

## 常见问题

### Q: 如何切换 LLM 模型？

编辑 `server/.env`：
```env
OPENAI_MODEL=gpt-4o-mini   # 更便宜
OPENAI_MODEL=gpt-4o        # 更强（推荐，支持多模态）
```

### Q: 命令执行顺序有保证吗？

是的。`maxSteps` 控制的多步推理是串行的：LLM 调用工具 → 等待结果 → 再调下一个。
`CommandExecutor` 也是按消息顺序扫描执行的。

### Q: execute_cad_code 生成的代码是安全的吗？

是的。代码在受控沙箱中执行：
- **黑名单机制** 禁止访问 `document`, `window`, `fetch`, `eval` 等危险 API
- 只能访问 ODA 绘图类、几何类和基本工具函数
- 自动内存管理防止内存泄漏
- `"use strict"` 模式阻止隐式全局变量

### Q: LLM 什么时候用快捷工具，什么时候生成代码？

CORE_PROMPT 中有明确的策略指导：
- 简单基础图形（线、圆、矩形等）→ 快捷 draw_xxx 工具
- 复杂图形（填充、标注、3D实体、阵列、带属性的实体）→ 先 `search_cad_code_examples`，再 `execute_cad_code`
- 图纸查询（图层列表、实体统计）→ `query_drawing`
- LLM 会根据任务复杂度自动选择

### Q: 如何添加新的绘图能力？

**最简单**：无需修改代码！向 `server/rag/code_examples/` 添加新的 JS 示例文件，重建索引。LLM 通过 `search_cad_code_examples` 检索到新示例后就能使用新 API。

**如果需要修改核心规则**：
1. 编辑 `server/tools/cadTools.js` 的 `CORE_PROMPT`
2. 重启后端即可

### Q: RAG 服务必须启动吗？

RAG 服务未启动时，`search_cad_knowledge` 和 `search_cad_code_examples` 工具会返回"检索失败"提示，LLM 仍能正常工作，但代码质量可能降低。建议始终启动 RAG 服务。

### Q: 截图分析功能需要什么 LLM？

需要支持多模态（Vision）的 LLM，如 GPT-4o。使用不支持视觉的模型时，截图功能将无法正常工作。
