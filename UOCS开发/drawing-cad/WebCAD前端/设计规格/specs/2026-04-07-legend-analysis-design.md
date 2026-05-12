# 图例分析功能设计规格

> 日期: 2026-04-07
> 状态: 已批准，待实施

## 概述

让 AI 助手能够"读懂"DWG 规划总平面图：通过识别图例建立**语义映射**（颜色+图层 → 含义），然后用该映射分析整个图纸，生成结构化的分析报告。分析结果持久化后，用户可直接提问（如"统计所有规划建筑面积"），AI 无需重新分析即可精确查询。

## 用户工作流

```
1. 用户打开 DWG 文件
2. 用户对 AI 说："根据图例分析整个 DWG"
3. AI 提示用户框选图例所在区域
4. AI 通过 Vision + 程序化双路径识别图例
5. AI 用图例映射扫描全图，生成统计报告
6. 分析结果注入对话上下文 + 保存为 Markdown 文件
7. 用户直接提问后续查询（如"规划建筑总面积"）
```

## 架构方案

**方案 A：LLM ReAct 编排**——不写新的前端管线，让 LLM 通过现有 ReAct 循环（maxSteps: 10）自行编排分析流程。新增最少量代码：1 个工具 + 1 个 Store + 提示词引导。

选择理由：
- 现有 ReAct 循环 + 工具链已足够编排多步任务
- 图例格式多变（块参照 / 松散实体），LLM 灵活判断优于固定管线
- 失败回退天然支持——LLM 可自主调整策略或提示用户

## 需求约束

- 图例格式：支持块参照 (OdDbBlockReference) 和松散实体两种
- 识别方式：[[Vision]] 先识别语义，程序化精确提取属性映射
- 匹配策略：**颜色 AND 图层必须同时满足**才判定为某图例类型
- 存储：混合方案——注入当前对话上下文（即时可用）+ 保存文件（持久化）
- 分析深度：基础层（图例映射表）+ 统计层（实体数量/面积/长度）
- 失败处理：说明原因，或提示用户交互选择补充信息

## 模块设计

### AnalysisStore（MobX 状态存储）

**文件**: `src/stores/AnalysisStore.js`（新建），挂载到 `RootStore`

```javascript
class AnalysisStore {
  // 图例映射表
  legendMapping = []
  // 格式: [{ meaning: "规划建筑", layer: "0-建筑", colorIndex: 2, rgb: [255,255,0],
  //          linetype: "Continuous", sampleEntityType: "OdDbPolyline" }, ...]

  // 统计数据
  statistics = {}
  // 格式: { "规划建筑": { count: 12, totalArea: 5832.5, layers: ["0-建筑"],
  //                       entities: [{handle, type, area?, length?}] },
  //         "用地红线": { count: 3, totalLength: 1200.5, ... }, ... }

  // 元信息
  sourceFileName = ''      // 关联的 DWG 文件名
  analysisTimestamp = null  // 分析时间
  isLoaded = false          // 是否已加载分析结果
}
```

对外方法:
- `setAnalysis(data)` — 存入分析结果，设 `isLoaded = true`
- `clearAnalysis()` — 清空全部数据
- `toMarkdown()` — 导出为结构化 Markdown 字符串
- `toJSON()` / `fromJSON(obj)` — 序列化/反序列化（用于文件存储）

### save_analysis 工具

**文件**: `server/tools/cadTools.js` 中新增

```javascript
save_analysis = tool({
  description: '保存图纸分析结果（图例映射 + 统计数据）。分析完成后调用此工具，结果会自动保存并注入后续对话上下文。',
  parameters: z.object({
    legendMapping: z.array(z.object({
      meaning: z.string().describe('图例含义，如"规划建筑"'),
      layer: z.string().describe('图层名，如"0-建筑"'),
      color: z.string().describe('颜色描述，如"yellow"或"rgb(255,255,0)"'),
      linetype: z.string().optional().describe('线型名（可选）'),
    })),
    statistics: z.record(z.object({
      count: z.number().describe('该类型实体数量'),
      totalArea: z.number().optional().describe('总面积（封闭曲线）'),
      totalLength: z.number().optional().describe('总长度（非封闭曲线）'),
    })),
    summary: z.string().describe('人类可读的分析摘要'),
  }),
  execute: async (args) => ({
    analysisResult: args,
    description: '保存图纸分析结果',
  }),
})
```

### 前端处理链（CommandExecutor 扩展）

`CommandExecutor.js` 收到包含 `analysisResult` 的工具结果后:
1. 调用 `rootStore.analysisStore.setAnalysis(data)` — 注入当前对话上下文
2. 调用 `analysisStore.toMarkdown()` 生成 Markdown
3. 触发浏览器下载，文件名: `{dwgFileName}_analysis_{YYYYMMDD}.md`

### drawingState 集成

**前端侧** — `AiAssistant.jsx` 的 `getDrawingStateSafe()`:
- 当 `analysisStore.isLoaded === true` 时，在 `drawingState` 中附带:

```javascript
drawingState.legendAnalysis = {
  mappingCount: analysisStore.legendMapping.length,
  mapping: analysisStore.legendMapping,
  statisticsSummary: analysisStore.statistics,
}
```

**后端侧** — `cadTools.js` 的 `buildSystemPrompt(drawingState)`:
- 当 `drawingState.legendAnalysis` 存在时，追加:

```
## 当前图纸已分析的图例映射
以下映射已通过图例分析确认，可直接用于筛选实体：
| 含义 | 图层 | 颜色 |
|---|---|---|
| 规划建筑 | 0-建筑 | 黄色 |
| 用地红线 | 0-红线 | 红色 |
| ... | ... | ... |

查询时使用条件：图层 AND 颜色同时匹配。
可直接调用 execute_js_code，无需重新分析图例。
```

### CORE_PROMPT 图例分析策略指引

在 `CORE_PROMPT` 中新增章节"图例分析[[工作流"]]，指导 LLM 的 ReAct 编排:

**第一步：获取图例区域**
- 提示用户框选图例所在区域（引导点击"区域选择"按钮）
- 如果用户直接提供了截图，跳过框选

**第二步：[[Vision]] 识别图例语义**
- 调用 capture_viewport 截取当前视图（确保图例可见）
- 分析截图中每个图例项的视觉特征和对应文字标签

**第三步：程序化验证与精确映射**
- 用 execute_js_code 扫描框选区域内实体属性（图层、颜色、线型）
- 将 [[Vision]] 语义与程序化属性做匹配
- 生成精确映射表：含义 ↔ (图层 AND 颜色)

**第四步：全图扫描统计**
- 用映射表遍历整个模型空间（包括块参照内的子实体）
- 图层 AND 颜色**同时匹配**才归入该类型
- 封闭曲线计算面积，非封闭曲线计算长度
- 块内实体面积需乘以缩放系数: `Math.abs(sf.sx * sf.sy)`

**第五步：保存分析结果**
- 调用 save_analysis 工具

**失败处理**:
- [[Vision]] 无法识别某图例项 → 标注"未识别"，提示用户手动补充
- 程序化扫描与 [[Vision]] 不匹配 → 提示用户确认
- 区域内图例实体不足 → 提示用户重新框选

### 加载已有分析

第一版不做自动检测/自动加载。用户可通过 AI 对话中的附件上传功能，上传之前保存的 `_analysis_*.md` 文件。后端通过现有的 `file` 类型 attachment 将内容注入对话上下文，LLM 识别后可调用 save_analysis 恢复到 AnalysisStore。

## 涉及文件变更清单

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `src/stores/AnalysisStore.js` | 新建 | MobX 分析结果存储 |
| `src/stores/RootStore.js` | 修改 | 挂载 AnalysisStore |
| `server/tools/cadTools.js` | 修改 | 新增 save_analysis 工具 + CORE_PROMPT 图例分析章节 + buildSystemPrompt 扩展 |
| `src/services/CommandExecutor.js` | 修改 | 处理 analysisResult → AnalysisStore + 文件下载 |
| `src/components/AiAssistant/AiAssistant.jsx` | 修改 | getDrawingStateSafe 附带 legendAnalysis |

## 不在本次范围内

- 自动检测/加载已有分析文件（后续迭代）
- 几何层分析（实体坐标范围、空间关系）
- 语义层分析（楼层数、标高、退让距离）
- 交互式子实体选择（kEnableSubents 模式）
- 图例分析 UI 按钮（当前通过对话文字触发）

## 相关笔记

- [[specs]]
- [[首次打开图纸自动归纳 — 视觉化重构设计]]
- [[ArcGIS Web 服务集成 — C++ 实施架构]]
- [[GIS服务 Ribbon 标签页设计规格]]
- [[GIS服务 Ribbon 标签页 Implementation Plan]]
- [[GIS File Import / Save-Back Design]]
- [[GIS服务 Ribbon 标签页 — 后续实施设计]]
- [[GIS服务后续实施 Implementation Plan]]
