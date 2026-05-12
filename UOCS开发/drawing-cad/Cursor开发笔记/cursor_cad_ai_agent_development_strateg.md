# CAD AI Agent development strategy
_Exported on 2026/3/13 at GMT+8 16:57:57 from Cursor (2.6.13)_

---

**User**

我现在开发的CAD AI Agent的目标是: 能智能画图，各种复杂的图形，还要能分析当前图纸，智能分析出图纸上的信息。我目前采用的是：“`streamText()` 将消息 + System Prompt + Tool 定义发给 LLM”这种路线，是不是非常难实现。 将来应该用什么最好的路线，例如，是不是我们要建立自己的小模型，因为不可能把所有的ODA 的JS代码都汇总给"System Prompt"吧，你有什么好的建议。

---

**Cursor**

这是一个非常好的架构问题。让我先深入了解你当前的实现，然后给出系统性的建议。

非常好的问题。我仔细看了你整个架构的实现，包括 `cadTools.js` (664行)、`CadCodeExecutor.js` (398行)、`server/index.js`、`AiAssistant.jsx` 以及架构文档。下面是我的系统性分析和建议。

---

## 一、当前方案评估：并不"非常难"，方向是对的

你当前的架构其实**已经是业界主流的 AI Agent 模式**，而且设计得相当不错：

| 你已经做到的 | 评价 |
|---|---|
| `streamText()` + Tool Calling | 标准的 Function Calling Agent 模式 |
| 快捷工具 + `execute_cad_code` 混合模式 | **非常聪明**的设计 — 简单图形用可靠工具，复杂图形用代码生成 |
| 沙箱执行 + 自动内存管理 | 安全且实用 |
| RAG 知识检索 | 已经走在正确的方向上 |

**核心矛盾不在路线上，而在 System Prompt 的"信息密度瓶颈"。** 你当前的 `SYSTEM_PROMPT` 大约 370 行 / ~15KB，里面塞了 ODA API 参考、12 个代码示例、规则说明等。这是可以工作的，但确实不可能把所有 ODA JS API 都放进去。

---

## 二、核心问题：不需要自己的小模型，需要的是"动态知识注入"

### 为什么**不建议**训练自己的小模型？

| 方案 | 成本 | 维护难度 | 效果 |
|---|---|---|---|
| Fine-tune 小模型 | 高（数据标注 + 训练 + GPU） | 极高（ODA API 更新就要重新训练） | 窄领域可以，但泛化差 |
| 大模型 + 动态 RAG + Few-Shot | 低 | 低（更新文档即可） | 泛化好，覆盖面广 |

**训练小模型的问题**：
1. ODA API 有上百个类、数千个方法，标注训练数据量巨大
2. ODA SDK 版本更新，模型就要重新训练
3. 小模型在"理解用户自然语言描述 → 分解为绘图步骤"这件事上远不如 GPT-4o / Claude 等大模型
4. 小模型的代码生成能力有限，对复杂图形的推理能力不足

---

## 三、推荐的演进路线：分层动态 Agent 架构

### 架构图

```
用户自然语言 → [意图识别/路由层]
                    │
        ┌───────────┼───────────────┐
        ▼           ▼               ▼
    [绘图 Agent]  [分析 Agent]  [修改 Agent]
        │           │               │
        ▼           ▼               ▼
   [动态 Prompt 组装器]
        │
        ├─ 基础规则 (固定, ~50行)
        ├─ RAG: ODA API 文档 (按需检索)
        ├─ RAG: 代码示例库 (Few-Shot, 按需匹配)
        └─ 当前图纸状态 (动态注入)
        │
        ▼
   [LLM (GPT-4o / Claude)]
        │
        ▼
   [execute_cad_code 沙箱]
```

### 关键改进点

### 1. **将 System Prompt 拆分为"固定核心 + 动态注入"**

现在你的 System Prompt 是一个巨大的静态字符串。建议改为：

```javascript
// 固定核心：只保留最基本的规则（~50行）
const CORE_PROMPT = `你是 CAD 绘图智能助手...
## 基本规则
1. 坐标系使用 WCS...
2. 创建实体的标准流程: createObject → setDatabaseDefaults → appendOdDbEntity
3. 设置颜色: new OdCmColor() → setRGB() → setColor()
...`

// 动态部分：根据用户意图，从 RAG 检索相关 API 文档和示例
async function buildDynamicPrompt(userMessage, drawingState) {
  const relevantAPIs = await ragSearch(userMessage)     // "用户想画阵列" → 检索阵列 API
  const relevantExamples = await exampleSearch(userMessage)  // 匹配最相关的 2-3 个代码示例
  const stateInfo = formatDrawingState(drawingState)    // 当前图纸上有什么

  return `${CORE_PROMPT}

## 当前图纸状态
${stateInfo}

## 相关 API 参考
${relevantAPIs}

## 代码示例
${relevantExamples}`
}
```

**好处**：
- System Prompt 从 15KB 降到 ~3KB 固定 + ~5KB 动态
- LLM 看到的信息都是高度相关的，不会被无关 API 干扰
- 可以覆盖无限多的 ODA API，不受 Prompt 长度限制

### 2. **建立 ODA API 代码示例库（Few-Shot RAG）**

这是**最高 ROI 的改进**。与其把所有示例塞进 System Prompt，不如：

```
DrawingWebApp/server/rag/
├── knowledge_base/
│   ├── help_docs/          # 你已有的帮助文档
│   └── code_examples/      # 新增：ODA API 代码示例库
│       ├── basic_line.js
│       ├── basic_circle.js
│       ├── hatch_brick.js
│       ├── polar_array.js
│       ├── path_array.js
│       ├── aligned_dimension.js
│       ├── 3d_solid_box.js
│       ├── layer_creation.js
│       ├── complex_building_facade.js
│       ├── mechanical_part_drawing.js
│       └── ... (可以有数百个)
```

每个示例文件包含：
```javascript
// @title: 极坐标阵列 - 环形排列圆
// @tags: array, polar, circle, 阵列, 环形
// @description: 将圆沿圆周均匀排列

const pCircle = OdDbCircle.createObject();
pCircle.setDatabaseDefaults(pDb, true);
// ... 完整代码
```

用户说"环形排列 8 个圆"时，RAG 自动检索到这个示例，注入 System Prompt。**LLM 看到几乎一模一样的示例代码，生成质量会大幅提升。**

### 3. **添加"图纸感知"能力（分析功能的基础）**

你的文档里 Phase 3 提到了这个方向。具体实现：

```javascript
// 新工具：查询当前图纸状态
export const getDrawingInfo = tool({
  description: '获取当前图纸的基本信息（图层列表、实体统计等）',
  parameters: z.object({}),
  execute: async () => {
    // 这个工具需要前端配合，通过 execute_cad_code 实现
    return {
      cadCode: `
        // 遍历图层
        const layerTable = OpenAs(pDb.getLayerTableId(), OdDbLayerTable, OpenMode.kForRead);
        // 遍历实体
        const ms = getModelSpace();
        const iter = ms.newIterator(true, true, false);
        // ... 收集信息并 return
      `,
      isQuery: true,  // 标记这是查询，不是绘图
    }
  }
})
```

或者更好的方式——**让 LLM 自己通过 `execute_cad_code` 生成查询代码**：

```
用户: "这张图纸上有什么？"
LLM → execute_cad_code: 生成遍历 modelSpace 的代码，收集实体信息
执行结果 → 返回给 LLM
LLM: "当前图纸包含 3 条直线、2 个圆、1 个矩形..."
```

**关键：让 `execute_cad_code` 支持返回值**。你现在的沙箱只有"执行"没有"查询返回"机制。建议增加：

```javascript
// 沙箱中注入一个结果收集器
sandbox.__result = null
sandbox.setResult = (data) => { sandbox.__result = data }

// 执行后检查返回值
fn(...scopeValues)
const queryResult = sandbox.__result  // LLM 生成的代码调用 setResult(info)
```

### 4. **利用多模态能力做图纸分析**

GPT-4o 和 Claude 都支持图片输入。你可以：

```javascript
// 截取当前视图截图
const screenshot = viewer.captureScreenshot()  // canvas.toDataURL()

// 发送给 LLM 做视觉分析
const messages = [
  { role: 'user', content: [
    { type: 'text', text: '分析这张图纸上有什么' },
    { type: 'image', image: screenshot }
  ]}
]
```

这对于"智能分析图纸信息"来说是**最直接有效**的方式，因为：
- 不需要写复杂的实体遍历代码
- LLM 可以直接"看到"图纸的布局、比例、标注等
- 可以理解设计意图（"这看起来像一个平面图"）

### 5. **Agent 循环（ReAct 模式）：规划 → 执行 → 观察 → 修正**

你现在的 `maxSteps: 15` 已经支持多步推理，但还可以增强：

```
用户: "画一栋两层楼的建筑正面图"

Step 1 (规划): LLM 输出思考过程，分解为地基、一楼墙壁、窗户、门...
Step 2 (执行): execute_cad_code → 画地基和一楼
Step 3 (观察): 截图 → 发给 LLM "看看画得对不对"
Step 4 (修正): LLM 发现比例不对 → 再次 execute_cad_code 调整
Step 5 (继续): 画二楼、屋顶...
```

---

## 四、具体行动建议（优先级排序）

| 优先级 | 改进 | 难度 | 预期效果 |
|---|---|---|---|
| **P0** | 建立 ODA API 代码示例库 + Few-Shot RAG | 中 | 代码生成质量大幅提升 |
| **P0** | System Prompt 动态组装（固定核心 + RAG注入） | 中 | 解决 Prompt 容量瓶颈 |
| **P1** | `execute_cad_code` 支持返回查询结果 | 低 | 解锁图纸分析能力 |
| **P1** | 多模态图纸截图分析 | 中 | 最直观的图纸分析方式 |
| **P2** | Agent Loop 增强（执行→截图→观察→修正） | 中高 | 复杂图形质量大幅提升 |
| **P3** | 意图路由层（绘图/分析/修改分流） | 中 | 更好的用户体验 |
| **不推荐** | 训练自己的小模型 | 极高 | ROI 太低 |

---

## 五、总结

你当前的架构**方向完全正确**，`streamText()` + Tool Calling + `execute_cad_code` 代码生成的混合模式是非常聪明的设计。**不需要训练自己的小模型**。

核心突破口是：**从"静态大 Prompt"演进到"动态知识注入"** — 用 RAG 检索 ODA API 文档和代码示例，按需组装 Prompt。这样你可以覆盖 ODA 的所有 API，同时保持 LLM 上下文窗口的高效利用。

对于"图纸分析"这个目标，**多模态（视觉）+ 查询代码生成** 的组合是最实用的路线，远比训练专门模型性价比高。

---



