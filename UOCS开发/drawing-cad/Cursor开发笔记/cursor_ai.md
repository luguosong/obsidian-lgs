# AI助手功能开发方向
_Exported on 2026/3/11 at GMT+8 11:26:50 from Cursor (2.6.13)_

---

**User**

如果我想在DrawingWebApp中增加 一个AI助手功能，希望实现Agent智能体的功能，用户可以根据描述，我就可以在当前图纸中画图。能给我一个开发方向吗？ 或者，互联网上有没有可以直接利用，后期我可以继续改进的文件，因为我的程序是模仿[[AutoCAD]]的，所有[[AutoCAD]]二维功能我都将实现的。

---

**Cursor**

我来先了解一下你现有的代码架构，特别是已经开始的 AI 助手组件和绘图服务接口。

现在我对你的代码架构有了很好的了解。让我再看一下你的绘图命令面板来了解已有的命令。

好的，我已经完整分析了你的代码架构。以下是基于你现有系统的详细开发方向。

---

## 你的现有基础

通过分析代码，你已经具备了非常好的基础：

1. **命令执行系统已完备** — `Viewer.execute(cmdName, args)` 可以调用所有 [[AutoCAD]] 命令（LINE, PLINE, CIRCLE, ARC, HATCH 等）
2. **命令交互流程清晰** — 命令启动后通过 `providePointToCommandFromScreen()`、`provideKeywordToCommand()`、`provideEmptyInput()` 提供参数/坐标
3. **全局 API 已暴露** — `window.__odaUi.safeExecute(cmd)` 和 `window.execute(name, args)` 可直接调用
4. **AI 助手 UI 外壳已就位** — `AiAssistant.jsx` 已有基本的对话框架

---

## 开发方向：AI Agent 绘图智能体架构

### 核心思路：自然语言 → 命令序列 → 逐步执行

整个系统分三层：

```
用户自然语言描述
       ↓
   LLM Agent（规划层）
       ↓
   命令序列 JSON（中间表示）
       ↓
   命令执行器（驱动 Viewer）
```

### 第一层：命令抽象层（Command Abstraction Layer）

你需要建立一个 **命令描述 Schema**，让 LLM 知道能调用什么。类似这样的定义：

```javascript
const CAD_COMMANDS = {
  LINE: {
    description: "绘制直线，从起点到终点",
    params: [
      { name: "startPoint", type: "point2d", desc: "起点坐标 (x,y)" },
      { name: "endPoint", type: "point2d", desc: "终点坐标 (x,y)" },
    ],
    execution: "sequential_points", // 需要依次提供坐标点
  },
  CIRCLE: {
    description: "绘制圆，指定圆心和半径",
    params: [
      { name: "center", type: "point2d", desc: "圆心坐标" },
      { name: "radius", type: "number", desc: "半径" },
    ],
  },
  PLINE: {
    description: "绘制多段线，依次指定各顶点",
    params: [
      { name: "points", type: "point2d[]", desc: "顶点坐标数组" },
      { name: "closed", type: "boolean", desc: "是否闭合", optional: true },
    ],
  },
  RECTANGLE: {
    description: "绘制矩形",
    params: [
      { name: "corner1", type: "point2d" },
      { name: "corner2", type: "point2d" },
    ],
  },
  // ... 注释、标注、修改命令等
}
```

### 第二层：LLM Agent 层（规划与推理）

这是核心。LLM 需要把用户描述翻译成命令序列。你有两种主要方案：

#### 方案 A：调用云端大模型 API（推荐起步）

使用 OpenAI / Claude / 通义千问等 API 的 **Function Calling / Tool Use** 功能：

```javascript
// services/AiAgentService.js
class AiAgentService {
  constructor(viewerRef) {
    this.viewer = viewerRef
    this.conversationHistory = []
  }

  async processUserInput(userMessage) {
    this.conversationHistory.push({ role: 'user', content: userMessage })

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'gpt-4o',
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          ...this.conversationHistory
        ],
        tools: CAD_TOOL_DEFINITIONS,  // Function Calling 的 tools 参数
        tool_choice: 'auto',
      })
    })

    const result = await response.json()
    return this.handleAgentResponse(result)
  }

  async handleAgentResponse(result) {
    const message = result.choices[0].message

    if (message.tool_calls) {
      // Agent 决定调用绘图命令
      for (const call of message.tool_calls) {
        const { name, arguments: args } = call.function
        await this.executeDrawCommand(name, JSON.parse(args))
      }
    }

    return message.content // 返回给用户的文字说明
  }
}
```

#### 方案 B：本地小模型 + 规则混合

对于简单指令用正则/模板匹配，复杂需求调 LLM。适合离线或低延迟场景。

### 第三层：命令执行器（Command Executor）

这是连接 AI 输出和你现有 `Viewer` 的桥梁。**关键难点**在于你的命令系统是**交互式的**（命令启动后等待用户逐步输入坐标），而 AI 需要**程序化地**驱动它：

```javascript
// services/CommandExecutor.js
class CommandExecutor {
  constructor(viewer) {
    this.viewer = viewer
  }

  async drawLine(startPoint, endPoint) {
    // 方案1: 如果 execute 支持传参
    await this.viewer.execute('LINE', [
      `${startPoint.x},${startPoint.y}`,
      `${endPoint.x},${endPoint.y}`,
      '' // 空字符串结束命令
    ])
  }

  async drawCircle(center, radius) {
    await this.viewer.execute('CIRCLE', [
      `${center.x},${center.y}`,
      `${radius}`
    ])
  }

  async drawRectangle(corner1, corner2) {
    await this.viewer.execute('RECTANG', [
      `${corner1.x},${corner1.y}`,
      `${corner2.x},${corner2.y}`
    ])
  }

  async drawPolyline(points, closed = false) {
    const args = points.map(p => `${p.x},${p.y}`)
    if (closed) args.push('C')  // 闭合关键字
    else args.push('')          // 空输入结束
    await this.viewer.execute('PLINE', args)
  }
}
```

**注意**：根据你现有代码，`executeCommandInternal` 调用 `appCore.ExecuteCommand(cmdName, vec)` 时传入的是 `VectorString`。你需要验证你的 C++ 后端是否支持 **一次性传入所有参数**（非[[交互模式]]），还是必须通过 `ProvideKeyword` / `ProvidePointFromScreen` 逐步喂入。如果是后者，你需要一个更复杂的序列化执行器，模拟用户的逐步交互。

### System Prompt 设计（最关键的部分）

```text
你是一个 AutoCAD 绘图助手。用户会用自然语言描述想要绘制的图形，
你需要将其转换为精确的 CAD 命令序列。

规则：
1. 所有坐标使用世界坐标系 (WCS)，单位为绘图单位
2. 用户未指定坐标时，你需要合理推算（如"在原点画一个半径10的圆"→ 圆心(0,0) 半径10）
3. 复杂图形需要分解为基本命令序列
4. 你可以使用的命令有：LINE, PLINE, CIRCLE, ARC, ELLIPSE, RECTANG, POLYGON,
   HATCH, TEXT, MTEXT, DIMLINEAR, DIMRADIUS, MOVE, COPY, MIRROR, ROTATE, SCALE,
   TRIM, EXTEND, FILLET, CHAMFER, OFFSET, ARRAY, ERASE, LAYER 等

示例：
用户: "画一个100x50的矩形，左下角在(0,0)"
→ RECTANG (0,0) (100,50)

用户: "在矩形中心画一个直径20的圆"
→ CIRCLE (50,25) 10

用户: "画一个简单的房子正面轮廓"
→ PLINE (0,0) (100,0) (100,80) (50,120) (0,80) C  // 五边形房子
→ RECTANG (35,0) (65,40)  // 门
→ CIRCLE (80,50) 8  // 窗户
```

---

## 互联网上可直接利用的资源

### 1. **OpenAI Function Calling** — 最成熟的方案

你的 [[AutoCAD]] 命令天然适合作为 "tools/functions" 定义。OpenAI、Claude、Gemini 都支持 Function Calling，可以直接让 LLM 输出结构化的命令调用。

### 2. **LangChain.js** — Agent 框架

- GitHub: `langchain-ai/langchainjs`
- 提供 Agent、Tool、Chain 的完整抽象
- 可以用它构建 **ReAct Agent**（推理→行动循环），适合多步骤绘图任务
- 支持 memory（记住之前画了什么），支持多种 LLM 后端

```bash
npm install langchain @langchain/openai
```

### 3. **Vercel AI SDK** — 轻量级前端 AI 集成

- GitHub: `vercel/ai`
- 提供 `useChat`、`useCompletion` 等 React Hooks
- 内置流式输出支持，UX 体验好
- 支持 tool calling

```bash
npm install ai @ai-sdk/openai
```

这个可能是最适合你的，因为它与 React 集成最好，而且你已经有了 AI 助手的 UI 外壳。

### 4. **AutoCAD 相关的 AI 参考项目**

- **BlenderGPT** (GitHub: `gd3kr/BlenderGPT`) — 用 GPT-4 在 Blender 中生成 3D 模型的 Python 脚本。虽然是 3D，但架构思路完全相同：自然语言 → LLM → API 调用
- **ChatCAD** — 学术界有相关论文，探索 LLM 驱动 CAD 建模
- **CadQuery / Build123d** + LLM — Python 参数化 CAD，已有人用 LLM 生成代码

### 5. **DXF/AutoCAD 命令参考数据**

你可以整理一份命令手册给 LLM 作为 system prompt 的一部分，或用 RAG（检索增强生成）方式。[[AutoCAD]] 的命令文档非常标准化，适合作为知识库。

---

## 建议的实施路线图

| 阶段 | 内容 | 工作量 |
|---|---|---|
| **Phase 1** | 在现有 `AiAssistant.jsx` 中集成 Vercel AI SDK 的 `useChat`，后端接 OpenAI API，实现基本对话 | 1-2 天 |
| **Phase 2** | 定义 CAD 命令的 Tool Schema，让 LLM 能输出结构化的绘图指令 | 2-3 天 |
| **Phase 3** | 实现 `CommandExecutor`，对接 `viewer.execute()`，验证 LINE/CIRCLE/PLINE/RECTANG 等基本命令 | 3-5 天 |
| **Phase 4** | 添加上下文感知 — 让 AI 知道当前图纸中已有什么（图层、实体列表） | 3-5 天 |
| **Phase 5** | 复杂场景 — 多步骤规划、修改已有实体、标注、填充等高级命令 | 持续迭代 |

---

## 最关键的技术决策点

1. **命令参数传递方式** — 你需要确认 C++ 后端的 `ExecuteCommand(cmdName, vectorString)` 是否支持一次性传入所有坐标参数（如 `["0,0", "100,50"]`），还是必须通过 `ProvideKeyword`/`ProvidePointFromScreen` 逐步交互。这决定了 CommandExecutor 的复杂度。

2. **后端代理还是纯前端** — 如果 API Key 不想暴露在前端，需要一个简单的 Node.js/Python 后端做代理。Vercel AI SDK 自带这个能力。

3. **坐标系统** — AI 输出的是世界坐标，但你的 `providePointToCommandFromScreen` 接收的是屏幕坐标。你可能需要一个 `provideWorldPoint` 方法（或确认 `execute` 的 args 支持世界坐标字符串）。

综上，**Vercel AI SDK + OpenAI Function Calling + 你现有的 `viewer.execute()` 命令系统** 是最快的落地路径。你已有的 UI 和命令体系是非常好的基础，核心工作是建立 LLM 和命令系统之间的桥接层。

---

**User**

 你能不能去GitHub查找有没有现成的CAD命令抽象层（Command Abstraction Layer）的 命令描述 Schema， 因为ODA的Drawing使用很广泛，都是参考[[AutoCAD]]命令的。或者有没有"System Prompt 设计"

---

**Cursor**

好的，我来帮你搜索现有的资源。

找到了好几个很有价值的项目！让我深入看看其中最相关的几个。

太棒了！找到了非常有价值的项目。让我进一步获取它们的具体命令 Schema 定义和 System Prompt。

非常好，我找到了大量现成的资源！以下是详细的汇总。

---

## 一、现成的 CAD 命令 Schema（可直接参考或复用）

### 1. **daobataotie/CAD-MCP** — 最直接可参考的中文项目（240 Stars）

GitHub: https://github.com/daobataotie/CAD-MCP

这个项目包含了**完整的 MCP Tool Schema 定义**，是 JSON Schema 格式，可以直接复用到你的 OpenAI Function Calling 中。它的 `server.py` 中定义了所有绘图工具的 `inputSchema`，我已经完整获取到了源码。以下是核心的 Schema 示例：

```javascript
// draw_line
{
  type: "object",
  properties: {
    start_point: { type: "array", description: "起点坐标 [x, y, z]", items: { type: "number" }, minItems: 2, maxItems: 3 },
    end_point:   { type: "array", description: "终点坐标 [x, y, z]", items: { type: "number" }, minItems: 2, maxItems: 3 },
    layer:       { type: "string", description: "图层名称（可选）" },
    color:       { type: "string", description: "颜色名称（可选）" },
    lineweight:  { type: "number", description: "线宽（可选）" }
  },
  required: ["start_point", "end_point"]
}

// draw_circle
{
  type: "object",
  properties: {
    center: { type: "array", description: "圆心坐标 [x, y, z]", items: { type: "number" }, minItems: 2, maxItems: 3 },
    radius: { type: "number", description: "圆的半径" },
    layer: ..., color: ..., lineweight: ...
  },
  required: ["center", "radius"]
}

// draw_polyline
{
  type: "object",
  properties: {
    points: { type: "array", description: "点集 [[x1,y1,z1], [x2,y2,z2], ...]",
      items: { type: "array", items: { type: "number" }, minItems: 2, maxItems: 3 }, minItems: 2 },
    closed: { type: "boolean", description: "是否闭合" },
    layer: ..., color: ..., lineweight: ...
  },
  required: ["points"]
}
```

它涵盖了以下绘图工具的完整 Schema：

| 工具 | 必要参数 | 可选参数 |
|---|---|---|
| `draw_line` | start_point, end_point | layer, color, lineweight |
| `draw_circle` | center, radius | layer, color, lineweight |
| `draw_arc` | center, radius, start_angle, end_angle | layer, color, lineweight |
| `draw_ellipse` | center, major_axis, minor_axis | rotation, layer, color, lineweight |
| `draw_polyline` | points | closed, layer, color, lineweight |
| `draw_rectangle` | corner1, corner2 | layer, color, lineweight |
| `draw_text` | position, text | height, rotation, layer, color |
| `draw_hatch` | points (>=3) | pattern_name, scale, layer, color |
| `add_dimension` | start_point, end_point | text_position, textheight, layer, color |
| `process_command` | command (自然语言) | — |

它还包含了**完整的 NLP 自然语言处理器** (`nlp_processor.py`)，支持中文命令解析，包括颜色识别、坐标提取、形状关键字映射等，非常适合你的中文 CAD 场景。

### 2. **ngk0/autocad-mcp** — 最全面的（19 Tools, ~120 Operations）

GitHub: https://github.com/ngk0/autocad-mcp

这是 hvkshetry/autocad-mcp 的扩展 fork，包含 **19 个工具类别、约 120 种操作**：

| 类别 | 操作 |
|---|---|
| **entity** | create_line, create_circle, create_polyline, create_rectangle, create_arc, create_ellipse, create_mtext, create_hatch + list, count, get + copy, move, rotate, scale, mirror, offset, array, fillet, chamfer, erase, explode, join, extend, trim, break_at |
| **layer** | list, create, set_current, set_properties, freeze, thaw, lock, unlock, visibility, rename, merge |
| **annotation** | create_text, create_dimension_linear/aligned/angular/radius, create_leader |
| **query** | entity_properties, entity_geometry, drawing_summary, layer_summary, text_styles, dimension_styles, linetypes, block_tree, drawing_metadata |
| **search** | text, by_attribute, by_window, by_proximity, by_type_and_layer, by_block_name |
| **geometry** | distance, length, area, bounding_box, polyline_info |
| **validate** | layer_standards, text_standards, orphaned_entities, attribute_completeness, connectivity, duplicates, zero_length, qc_report |
| **select** | filter, bulk_move, bulk_copy, bulk_set_property, bulk_erase, find_replace_text |
| **block** | list, insert, insert_with_attributes, get_attributes, update_attribute, define |
| **view** | zoom_extents, zoom_window, zoom_center, zoom_scale, pan, get_screenshot |

### 3. **AnCode666/multiCAD-mcp** — 多 CAD 支持架构（46 Tools）

GitHub: https://github.com/AnCode666/multiCAD-mcp

三层[[架构设计]]，支持 [[AutoCAD]]/ZWCAD/GstarCAD/BricsCAD。它定义了**抽象接口 `CADInterface`**：

```python
# core/cad_interface.py — Abstract base class
class CADInterface:
    # Connection
    connect(), disconnect(), is_connected()
    # Drawing
    draw_line(), draw_circle(), draw_arc(), draw_rectangle(),
    draw_polyline(), draw_text(), draw_ellipse(), draw_hatch()
    # Layers
    create_layer(), list_layers(), delete_layer(), rename_layer()
    # Files
    save_drawing(), new_drawing(), close_drawing()
    # Selection
    select_by_color(), select_by_layer(), select_by_type()
    # Manipulation
    move_entities(), rotate_entities(), scale_entities(), copy(), paste()
```

---

## 二、System Prompt 设计

### 已找到的现成 Prompt Template

**CAD-MCP 项目的 PROMPT_TEMPLATE**（来自 `daobataotie/CAD-MCP/src/server.py`）：

```text
助手的目标是演示如何使用CAD MCP服务。通过这个服务，您可以直接在对话中控制CAD软件，
创建和修改图形。

此服务器提供以下基本绘图工具：
"draw_line": 在CAD中绘制直线
"draw_circle": 在CAD中绘制圆
"draw_arc": 在CAD中绘制弧
"draw_ellipse": 在CAD中绘制椭圆
"draw_polyline": 在CAD中绘制多段线
"draw_rectangle": 在CAD中绘制矩形
"draw_text": 在CAD中添加文本
"draw_hatch": 在CAD中绘制填充
"save_drawing": 保存当前图纸
"add_dimension": 在CAD中添加线性标注
"process_command": 处理自然语言命令并转换为CAD操作
```

### 针对你的 DrawingWebApp 的建议 System Prompt

结合你现有的 `viewer.execute(cmdName, args)` 命令系统，建议如下：

```text
你是 DrawingWebApp 的 CAD 绘图智能助手。用户用自然语言描述图形，你将其转化为
精确的 CAD 命令序列并执行。

## 可用命令

### 绘图命令
- LINE: 直线。参数: 起点x,y 终点x,y (可连续输入多个端点，空字符串结束)
- PLINE: 多段线。参数: 依次各顶点x,y，"C"闭合或空字符串结束
- CIRCLE: 圆（圆心+半径）。参数: 圆心x,y 半径值
- CIRCLE_D: 圆（圆心+直径）。参数: 圆心x,y 直径值
- CIRCLE_2P: 圆（两点）。参数: 第一点x,y 第二点x,y
- CIRCLE_3P: 圆（三点）。参数: 三个点的x,y
- ARC: 圆弧（三点）。参数: 起点x,y 第二点x,y 端点x,y
- ARC_SCE: 圆弧（起点-圆心-端点）。参数: 起点x,y 圆心x,y 端点x,y
- ELLIPSE: 椭圆。参数: 轴端点1 x,y 轴端点2 x,y 另一半轴距离
- RECTANG: 矩形。参数: 对角点1 x,y 对角点2 x,y
- POLYGON: 正多边形。参数: 边数 中心x,y 半径
- HATCH: 图案填充
- DONUT: 圆环。参数: 内径 外径 圆心x,y
- MTEXT: 多行文字
- TEXT: 单行文字

### 修改命令
- ERASE: 删除选中实体
- MOVE: 移动。参数: 基点x,y 位移点x,y
- COPY: 复制
- MIRROR: 镜像
- ROTATE: 旋转
- SCALE: 缩放
- STRETCH: 拉伸
- FILLET: 圆角
- CHAMFER: 倒角
- OFFSET: 偏移
- TRIM: 修剪
- EXTEND: 延伸
- ARRAY: 阵列
- EXPLODE: 分解
- JOIN: 合并
- BREAK: 打断

### 注释命令
- DIMLINEAR: 线性标注
- DIMRADIUS: 半径标注
- DIMANGULAR: 角度标注

## 规则
1. 坐标使用世界坐标系 (WCS)，格式为 "x,y"
2. 用户未指定坐标时，你需要根据描述合理推算
3. 复杂图形分解为基本命令序列
4. 每条命令返回 { command: "CMD_NAME", args: ["x,y", "x,y", ...] }
5. 多条命令用数组包装
6. 先确认理解用户需求，再执行

## 输出格式
返回 JSON 命令数组：
[
  { "command": "LINE", "args": ["0,0", "100,0"] },
  { "command": "LINE", "args": ["100,0", "100,50"] },
  { "command": "CIRCLE", "args": ["50,25", "10"] }
]

## 示例
用户: "画一个100x50的矩形，左下角在原点"
→ [{ "command": "RECTANG", "args": ["0,0", "100,50"] }]

用户: "在矩形中心画一个半径10的圆"
→ [{ "command": "CIRCLE", "args": ["50,25", "10"] }]

用户: "画一个简单的房子正面"
→ [
  { "command": "PLINE", "args": ["0,0", "100,0", "100,80", "50,120", "0,80", "C"] },
  { "command": "RECTANG", "args": ["35,0", "65,40"] },
  { "command": "CIRCLE", "args": ["80,50", "8"] }
]
```

---

## 三、推荐的实施策略

根据你的实际情况（基于 WASM 的 ODA Drawing、浏览器端渲染、`viewer.execute()` API），我建议：

1. **直接参考 `daobataotie/CAD-MCP` 的 Tool Schema** — 它的 `inputSchema` 定义和你需要的完全一致，而且是中文友好的。你只需要把它的 JSON Schema 转换成 OpenAI Function Calling 的 `tools` 格式。

2. **复用它的 `nlp_processor.py` 逻辑** — 中文颜色名映射、坐标提取正则、形状关键字等可以直接移植到 JavaScript。

3. **关键差异**：这些 MCP 项目都是通过 COM 接口或 AutoLISP 与桌面 [[AutoCAD]] 通信的，而你是通过 **WASM + `viewer.execute(cmdName, vectorString)`** 调用的。所以你不需要 MCP 协议层，只需要把 LLM 输出的命令直接传给 `viewer.execute()` 即可。

4. **最快路径**：在你的 `AiAssistant.jsx` 中集成 LLM API，用上述 System Prompt + Tool Schema，LLM 返回命令 JSON → 逐条调用 `window.__odaUi.safeExecute(cmd)` 或 `viewer.execute(name, args)` 执行。

