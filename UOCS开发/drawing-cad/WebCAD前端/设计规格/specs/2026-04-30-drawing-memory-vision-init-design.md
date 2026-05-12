# 首次打开图纸自动归纳 — 视觉化重构设计

> **状态**: 设计稿 (待审)
> **日期**: 2026-04-30
> **作者**: 协作产出 (zhoufs1205@gmail.com + Claude)
> **范围**: 前端 + 后端 (DrawingWebApp + drawing-ai-server)
> **关联文档**:
> - 现状分析: `drawing-ai-server/docs/架构设计/图纸记忆-流程与问题分析.md`
> - 用地红线视觉测试 (本设计的子能力来源): `DrawingWebApp/docs/2026-04-26-land-boundary-vision-test-design.md`
> - 退让距离审查 (后续审图主线之一): `DrawingWebApp/docs/specs/2026-04-26-setback-distance-review-design.md`

---

## 1. 背景与问题

CAD AI 智能审图当前的"首次打开图纸自动归纳"流程存在三类问题:

### 1.1 速度问题
- 前端 `extractComprehensive` 全量扫描 → 后端 LLM 纯文本归纳异步链路,前端要轮询 180 秒才超时
- LLM "复读"前端预处理小作文,产出 `layerSemantics` / `keyFacts` 整体耗时常态 30-90 秒

### 1.2 准确性问题
- **基于图层名猜类型不可靠** —— DWG 中经常有对象不在它"应该"的图层上;前端 `_aggregateSiteAreas` 用正则识别"红线 / 绿地",汇总面积时把杂项算进去
- **嵌套块只穿透第 0 个 reference**(`extractComprehensive:1426`),导致同一块插入 N 次时面积只算 1/N
- **LLM 幻觉污染** —— prompt 例子里的 `analysis.areaByCategory` 字段在前端代码里根本不存在,但 LLM 把它当真实字段写进 keyFact

### 1.3 视觉模型未充分利用
- 视觉模型仅在 Stage 1(图纸类型分类)启用,Stage 2 的 `layerSemantics` / `keyFacts` 完全是纯文本归纳
- 全图截屏只用了一次(分类),即"看图"和"产出语义"是两条不通气的链路

### 1.4 重复劳动
- DWG 打开时,ODA WASM 已经把 `OdDbDatabase` 装进内存,**`viewer.getLayersWithInfo()` 可在 50ms 内返回完整图层列表**(已验证)
- `extractComprehensive` 中真正贵的操作是"扫遍 ModelSpace 实体 + 文字 + 标注 + 块",首次归纳实际只需要图层骨架

---

## 2. 设计目标与范围

### 2.1 目标
1. **视觉模型主导归纳** —— `layerSemantics` / `keyFacts` 来自视觉模型直接读图(图例 + 技经表),而非 LLM 复读文本
2. **零成本元数据** —— 用 `getLayersWithInfo()` 替代 `extractComprehensive` 在归纳链路的调用
3. **数值自验证** —— Stage C 提取的几何对象,用技经表中的指标值反向验证(用地面积、建筑面积、建筑数量)
4. **优雅降级** —— 找不到关键区域、视觉读取失败、验证不通过 → 标 staleness,不阻断流程

### 2.2 范围(Scope)
**In scope:**
- "首次打开图纸"这一刻触发的归纳流程的全栈重构 — Stage A(全图分析) + Stage B(区域精读) (前端 + 后端 + Redis schema)
- **Stage C(对象提取)的通用管线 + 验证规则注册表**,但 Stage C **不在首次打开时自动执行**(见 §7.4),仅作为后续审图按钮"按需触发"的能力
- 已有的 `LandBoundaryVisionTest.js` / `LandBoundaryAnalyzer.js` 在本次落地后**收敛进 Stage C 通用管线**
- 删除 `_aggregateSiteAreas` / `_categorizeSiteLayer` / Stage 2 纯文本归纳
- 改造 `extractComprehensive` 的调用关系: 从"init 时扫" → "对话工具按需扫"

**Out of scope (后续单独立项):**
- Stage C 的"按需触发"具体接入点 — ribbon 按钮如何调用 Stage C / 审图清单状态机如何调度,本次只交付能力,接入点单独立项
- Tool 体系收敛 (后端 50+ @Tool 的合并/删除)
- 审图清单的状态机 (清单驱动的审图流程)
- 申请表 PDF 解析的优化
- 多图纸对比 / 批量审查

### 2.3 非功能要求
- 首次打开 → 记忆可用的总耗时 ≤ 30 秒 (P50)
- 视觉调用失败时,降级路径不超过 5 秒
- 不破坏现有 Redis schema(向后兼容,字段只增不删)

---

## 3. 关键决策记录

| # | 决策 | 选择 | 理由 |
|---|---|---|---|
| D1 | Stage B 调度权 | **前端调度** | 后端无 session 状态;失败可单独重试;复用 `LandBoundaryVisionTest` 现成代码 |
| D2 | 局部放大方式 | **ODA 重渲** | `viewer.zoomTo(bbox) + captureCurrentView()` 得到无损高清局部图,文字识别率高 |
| D3 | Region 类型 (v1) | **技经表 + 图例 + 总平面图主体区** | 覆盖 80% 关键信息;3 次视觉调用可控 |
| D4 | 找不到目标区域 | **优雅降级 + staleness 标记** | 不弹错误,UI 上标"未找到 X,部分指标待补充" |
| D5 | 单位策略 | **drawingType 决定 unit** | 规划/总平面 = 米;建筑单体 = 毫米;不再从数据分析 |
| D6 | 元数据来源 | **`getLayersWithInfo()` 替代 `extractComprehensive`** | 零成本(<50ms),只取图层名 + 颜色 + 线型,不扫实体 |
| D7 | 主体区输出 | **场景描述 + 关键标注 + 候选对象 bbox 全要** | 主体区是 Stage A 与 Stage C 的"路标地图" |
| D8 | Stage C 形态 | **视觉定位 + ODA 单点选择 + 技经表数值验证** | 复用 LandBoundaryVisionTest 已验证的代码;数值验证消除"看着像"的误识别 |
| D9 | 长区域分屏 | **Stage A 预判 splitStrategy + Stage B 多图单次调用 + 兜底重读** | 视觉模型有全局视野判文字密度;多图单次调用让模型理解"切片连贯";兜底防误判 |
| D10 | 图框自适应 | **扩展 Stage A prompt + 条件重跑 (最多 1 次)** | 正常场景零额外开销;`small` 时 zoom 重截+整体重跑;`not_visible` 时 AI 面板提示用户手动放大 |

---

## 4. 总体架构 — 三段式流程

```
首次打开图纸 (用户操作)
  │
  ├── ① 前端零成本元数据拉取 (替代 extractComprehensive)
  │     viewer.getLayersWithInfo()   <50ms
  │     viewer.getLayoutNames() / getActiveLayoutName()
  │     viewer.getDb() 上的 extents / 文件名等
  │     → metadata = { layers[], layouts[], extents, fileName }
  │
  ├── ② 前端 captureFullExtents (全图截屏)
  │     → fullScreenshot = base64 (压缩到 ~1 MB)
  │
  └── ③ POST /api/drawing-memory/{client}/{file}/init  (新版 schema)
       body: { metadata, fullScreenshot }
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │ Stage A — 视觉:全图分析 (1 次后端调用 → 1 次视觉 LLM)    │
  │                                                          │
  │ 输入: fullScreenshot + metadata                         │
  │ 视觉 LLM 输出 (StageAResult):                           │
  │   {                                                      │
  │     drawingType,        // 决定 unit                    │
  │     drawingUnit,        // 由 drawingType 派生          │
  │     drawingLayout,      // 自然语言全图布局描述         │
  │     keyRegions: [                                       │
  │       {                                                  │
  │         type: '技经表'|'图例'|'主体区',                 │
  │         bbox: [x1, y1, x2, y2],   // 屏幕像素坐标       │
  │         splitStrategy: 'single'|'vertical-N'|...,       │
  │         splitReason                                      │
  │       }                                                  │
  │     ]                                                    │
  │   }                                                      │
  └─────────────────────────────────────────────────────────┘
        │
        ▼ (前端拿到 keyRegions,开始并行处理)
        │
  ┌─────────────────────────────────────────────────────────┐
  │ Stage B — 视觉:逐区精读 (3 次后端调用,可并行)            │
  │                                                          │
  │ for each region in keyRegions:                          │
  │   if splitStrategy === 'single':                        │
  │     viewer.zoomTo(bbox) + captureCurrentView()          │
  │     → 1 张高清切片                                      │
  │   else:                                                  │
  │     按 splitStrategy 切 bbox → N 个子 bbox              │
  │     for each sub-bbox:                                  │
  │       viewer.zoomTo + captureCurrentView                │
  │     → N 张高清切片                                      │
  │   POST /api/drawing-memory/.../region                   │
  │   body: { regionType, images: [base64...] }             │
  │   后端按 regionType 分发到专用 prompt                   │
  │   视觉 LLM 输出 (按类型不同):                           │
  │     技经表 → keyFacts                                   │
  │     图例   → layerSemantics                             │
  │     主体区 → mainAreaDescription + keyAnnotations       │
  │             + candidateObjects                          │
  └─────────────────────────────────────────────────────────┘
        │
        ▼
  写入 DrawingMemory (Redis)
  UI 提示"图纸记忆已建立 (基础信息)"
        │
   ─── 「全图分析」结束 ───
        │
        ▼
  ┌─────────────────────────────────────────────────────────┐
  │ Stage C — 对象提取 (按需触发,逐对象循环)                 │
  │                                                          │
  │ 输入: candidateObjects (Stage B 主体区给) + keyFacts    │
  │                                                          │
  │ for each (objectType, candidateBbox) in candidates:     │
  │   ① zoomTo(candidateBbox) + captureCurrentView          │
  │   ② 视觉精读: "在这张图里精确框出 {objectType}"          │
  │      → 屏幕坐标 (single point or polygon outline)       │
  │   ③ 屏幕→世界坐标转换                                   │
  │   ④ ODA selectByPoint(world_x, world_y, mode=7)         │
  │      → handles[] (嵌套穿透)                            │
  │   ⑤ 数值验证 (按 objectType 切换规则):                  │
  │      用地红线 → 闭合面积 vs keyFacts.totalLandArea      │
  │      建筑单体 → 数量 vs keyFacts.buildingCount          │
  │                 总面积 vs keyFacts.totalBuildingArea    │
  │      退让线   → 与红线偏移 vs keyFacts.setbackDistance  │
  │      道路线   → 弱验证 (宽度 / 与红线相邻)              │
  │   ⑥ 验证通过: 写 spatial-constraints (handles + area)  │
  │      验证失败: staleness 标 'xxx_validation_failed'     │
  │   ⑦ flashByHandles 高亮回馈用户                         │
  └─────────────────────────────────────────────────────────┘
```

---

## 5. Stage A — 视觉全图分析 详细设计

### 5.1 输入

```typescript
{
  metadata: {
    layers: Array<{name, color, frozen, locked, linetype, lineweight}>,
    layouts: Array<string>,
    extents: { minX, minY, maxX, maxY },
    fileName: string
  },
  fullScreenshot: string  // base64 jpeg, quality 0.8, ~1MB
}
```

### 5.2 视觉模型 prompt 骨架

`DrawingTypeAndLayoutPrompt`(替代现有 `DrawingTypeSkillProvider.CLASSIFICATION_SYSTEM_PROMPT_WITH_VISION`):

```
你是 CAD 图纸分析专家。请基于全图截屏 + 图层列表,完成以下任务:

任务 1 — 判断图纸类型 (drawingType):
  - REGULATORY_PLAN (控规图)
  - SITE_PLAN (总平面图)
  - ARCHITECTURAL_DESIGN (建筑单体设计图)
  - MUNICIPAL_ENGINEERING (市政图)
  - LANDSCAPE (景观图)
  - OTHER

任务 2 — 由 drawingType 派生 drawingUnit:
  REGULATORY_PLAN / SITE_PLAN / LANDSCAPE → meter
  ARCHITECTURAL_DESIGN → millimeter
  MUNICIPAL_ENGINEERING → meter
  OTHER → unknown

任务 3 — 描述全图布局 drawingLayout (≤200 字)。

任务 4 — 识别关键区域 keyRegions,只识别以下三类:
  - 技经表: "技术经济指标表" / "经济指标" / "Indicators" 等
  - 图例: "图例" / "Legend" / 符号说明
  - 主体区: 总平面图的核心绘制区域 (建筑/道路/绿地的主分布区)

  对每个 region 输出:
    type, bbox (屏幕像素坐标 [x1,y1,x2,y2]),
    splitStrategy:
      - 'single': 区域不大或文字不密集,单次重渲足以读清
      - 'vertical-N' (N=2-4): 区域细长,按高度切 N 段
      - 'horizontal-N' (N=2-4): 区域扁平,按宽度切 N 段
      - 'grid-MxN': 区域大且密集,按 M 行 N 列网格切
    splitReason: 一句话说明分屏理由 (若 single 则填 'no split needed')

  评估 splitStrategy 的标准:
    - 估算 bbox 在原图的像素尺寸
    - 若区域内文字行数 > 15 且高/宽 > 2 → vertical
    - 若区域内文字列数 > 8 且宽/高 > 2 → horizontal
    - 若两者都大且密集 → grid
    - 其他 → single

返回严格 JSON,字段全部填,不能输出 markdown fence。
```

### 5.3 输出 schema (StageAResult)

```typescript
{
  frameStatus: 'full' | 'small' | 'not_visible',  // 图框状态 (§5.5)
  frameBbox: [number, number, number, number] | null,  // 仅 'small' 时有值
  drawingType: 'REGULATORY_PLAN' | 'SITE_PLAN' | 'ARCHITECTURAL_DESIGN'
             | 'MUNICIPAL_ENGINEERING' | 'LANDSCAPE' | 'OTHER',
  drawingUnit: 'meter' | 'millimeter' | 'unknown',
  drawingLayout: string,                       // 自然语言描述
  keyRegions: Array<{
    type: '技经表' | '图例' | '主体区',
    bbox: [number, number, number, number],   // 屏幕像素坐标
    splitStrategy: 'single' | `vertical-${number}` | `horizontal-${number}` | `grid-${number}x${number}`,
    splitReason: string,
    confidence: 'high' | 'mid' | 'low'
  }>
}
```

### 5.4 失败处理
- **JSON 解析失败**: 重试 1 次,仍失败则 → drawingType='OTHER', keyRegions=[],staleness='stage_a_parse_failed'
- **视觉模型超时 (>30s)**: 直接降级,只填 metadata 进 summary,staleness='stage_a_timeout'
- **keyRegions 为空**: 不阻断,直接进 Stage C 跳过(无 candidateObjects 也跳过 Stage C)

### 5.5 图框自适应检测 (Frame Detection)

#### 5.5.1 问题

不同设计师的画图习惯导致 `ZoomExtents` 后图框可能不占满屏幕:

| 场景 | ZoomExtents 效果 | 后果 |
|------|-----------------|------|
| **正常** (`full`) | 图框占满屏幕大部分 | Stage A 正常分析 |
| **偏小** (`small`) | 图框只占屏幕一小部分 (远处有散落实体) | LLM 看到的文字极小,识别率断崖式下降 |
| **不可见** (`not_visible`) | 图框在远处或极小,散落对象占据视野 | LLM 完全无法分析 |

#### 5.5.2 方案

在 Stage A prompt 中增加**任务 0 — 评估图框状态**,让 LLM 在同一次视觉调用中判断图框是否正常显示。

Stage A 输出新增两个字段:
```typescript
{
  // ... 原有字段 ...
  frameStatus: 'full' | 'small' | 'not_visible',
  frameBbox: [number, number, number, number] | null  // 仅 'small' 时有值,归一化坐标
}
```

#### 5.5.3 前端处理流程

```
ZoomExtents → 截全图 → POST /init (Stage A)
  │
  ├── frameStatus === 'full'
  │     └── 正常进入 Stage B
  │
  ├── frameStatus === 'small' (且 frameBbox 有值)
  │     ├── 前端 zoom 到 frameBbox 对应的世界坐标
  │     ├── 重新截全图
  │     └── 重跑 Stage A (第二次; 不再检查 frameStatus, 直接进 Stage B)
  │
  └── frameStatus === 'not_visible'
        └── 前端在 AI 面板提示用户手动放大图框
            用户确认后 → 重新截屏 → 重跑 Stage A (仅 1 次机会)
```

#### 5.5.4 关键约束

- **重跑上限: 1 次** — 第一次 `small` 或用户手动放大后重跑的 Stage A 不再判 frameStatus,直接采纳结果进 Stage B
- **不复用首次结果** — 重跑时整体重跑 Stage A (包括 drawingType/keyRegions),因为 keyRegions 的 bbox 是屏幕像素坐标,zoom 后坐标系变了
- **`not_visible` 交互** — AI 面板发消息 + 「重新分析」按钮,不弹 Modal

#### 5.5.5 prompt 变更 (任务 0)

在 Stage A SYSTEM_PROMPT 最前面增加:

```
任务 0 — 评估图框状态 (frameStatus):
  观察截屏中是否存在矩形的图框（图纸外边框）。
  - 'full':   图框占据了屏幕的大部分面积 (>50%),内容清晰可读
  - 'small':  能看到图框,但它只占屏幕的一小部分 (<30%),同时给出 frameBbox
  - 'not_visible': 截屏中看不到明显的图框矩形

  frameBbox: 仅当 frameStatus='small' 时填写,格式 [x1, y1, x2, y2] 归一化坐标 0.0-1.0。
             frameStatus='full' 或 'not_visible' 时填 null。
```

---

## 6. Stage B — 视觉逐区精读 详细设计

### 6.1 前端流程 (`VisionMemoryPipeline.js`,新建)

```javascript
async function runStageB(viewer, keyRegions) {
  const promises = keyRegions.map(region => processRegion(viewer, region))
  const results = await Promise.allSettled(promises)
  return aggregateResults(results)
}

async function processRegion(viewer, region) {
  const { type, bbox, splitStrategy } = region
  const tiles = sliceBbox(bbox, splitStrategy)  // 1 个或 N 个子 bbox
  const images = []
  for (const tile of tiles) {
    await viewer.zoomTo(tile)
    const shot = captureCurrentView(viewer, { quality: 0.85, format: 'image/jpeg' })
    images.push(shot.dataUrl)
  }
  return await postRegionToBackend(type, images)
}
```

### 6.2 切片函数 (`sliceBbox`)

```javascript
function sliceBbox(bbox, strategy) {
  const [x1, y1, x2, y2] = bbox
  if (strategy === 'single') return [bbox]

  const verticalMatch = strategy.match(/^vertical-(\d+)$/)
  if (verticalMatch) {
    const n = +verticalMatch[1]
    const h = (y2 - y1) / n
    return Array.from({length: n}, (_, i) => [x1, y1 + i*h, x2, y1 + (i+1)*h])
  }

  const horizontalMatch = strategy.match(/^horizontal-(\d+)$/)
  if (horizontalMatch) {
    const n = +horizontalMatch[1]
    const w = (x2 - x1) / n
    return Array.from({length: n}, (_, i) => [x1 + i*w, y1, x1 + (i+1)*w, y2])
  }

  const gridMatch = strategy.match(/^grid-(\d+)x(\d+)$/)
  if (gridMatch) {
    const [m, n] = [+gridMatch[1], +gridMatch[2]]
    const w = (x2 - x1) / n, h = (y2 - y1) / m
    const tiles = []
    for (let r = 0; r < m; r++) for (let c = 0; c < n; c++) {
      tiles.push([x1 + c*w, y1 + r*h, x1 + (c+1)*w, y1 + (r+1)*h])
    }
    return tiles
  }

  // fallback: single
  return [bbox]
}
```

### 6.3 后端按 regionType 分发的 prompt

#### 6.3.1 技经表 prompt
```
你看到的是一张技术经济指标表的截图 (可能由 N 个切片拼接,从上到下 / 从左到右排列)。

请把表格中**所有可见的行**逐项提取(不论是常见规范指标、项目特异指标、备注、公式、引用条文、文字说明等),
输出 keyFacts 列表,每项:
  { name, value, unit, confidence }

字段说明:
- name:  表格行的名称(原文,不要意译)
- value:
    * 数值型: 输出数字 (12345 而非 "12345 ㎡")
    * 文本型: 直接输出字符串 (如 "居住用地" / "甲级" / "见图签" / "≥50%")
    * 含范围: 如 "1.0~1.5" 直接作为字符串
- unit:  单位 (㎡ / m / % / 栋 / kV / dB ...);无单位时填空字符串
- confidence: high | mid | low

约束:
- **完整性优先**:不要遗漏任何一行,包括备注栏、合计栏、表头说明
- 同名行多次出现,各自独立 entry,可在 name 末尾加序号 (如 "建筑高度 #2")
- 模糊不清或多义的标 confidence='low' 但仍要输出
- 严格 JSON,不要 markdown 代码块

额外字段(必填):
  "_meta": {
    "extractedComplete": true | false,
    "suggestedReSlice": null | "vertical-N" | "horizontal-N" | "grid-MxN"
  }
```

#### 6.3.2 图例 prompt
```
你看到的是图例区域的截图。

请提取每个图例条目,**只输出视觉信息**(描述 + 颜色 + 形状),
**不要尝试与图纸图层名匹配**——图例标注的是视觉约定,与实际图层名常不一致。

输出 legendItems 列表,每项:
  {
    description: 图例右侧文字描述 (原文,如 "规划用地红线" / "建筑退线" / "园区道路"),
    visualKind:  'line' | 'symbol' | 'pattern',
    color:       16 进制 #RRGGBB,看不清填 ""(尽量给主色),
    lineType:    仅当 visualKind='line' 时填: 'solid' | 'dashed' | 'dot-dash' | 'dotted' | 'double',
    symbol:      仅当 visualKind='symbol' 时填: 简短形状描述 (如 "红色实心箭头" / "黄色三角形" / "绿色三角"),
    pattern:     仅当 visualKind='pattern' 时填: 简短描述 (如 "绿色斜线填充" / "橙色网格" / "石头堆叠"),
    confidence: high | mid | low
  }

约束:
- 输出顺序按图例从上到下、从左到右
- 多列布局的图例(本图常见左右两列)按列内顺序输出
- 颜色尽量用 #RRGGBB 表达,实在辨别不清才填空字符串
- 不输出空行 / 表头 / 边框
- 严格 JSON,不要 markdown 代码块

额外字段(必填):
  "_meta": {
    "extractedComplete": true | false,
    "suggestedReSlice": null | "vertical-N" | "horizontal-N" | "grid-MxN"
  }
```

#### 6.3.3 主体区 prompt
```
你看到的是总平面图的主体绘制区。

请同时输出三件事:

任务 1 — 场景描述 (mainAreaDescription, ≤300 字):
  描述场地形状 / 主入口位置 / 建筑分布 / 绿地分布 / 道路网络 / 特殊元素

任务 2 — 关键标注 (keyAnnotations):
  [{ text: '住宅楼 1F=4.5m', confidence: 'high' }, ...]
  捕捉建筑功能 / 层数 / 高度 / 道路宽度 / 绿地名称等图面文字标注

任务 3 — 候选对象 bbox (candidateObjects):
  [
    {
      guess: '用地红线' | '建筑退让线' | '建筑单体' | '道路' | '绿地'
           | '广场' | '停车场' | '其他',
      bbox: [x1, y1, x2, y2],     // 屏幕像素坐标
      count: number,              // 该类型对象的数量 (建筑单体 5 栋则 count=5)
      confidence: 'high' | 'mid' | 'low'
    },
    ...
  ]
  candidateObjects 是 Stage C 的输入,要求:
  - 精确度优先 (能给单个 bbox 就不给整片)
  - 可重复 (同类型多个对象,每个独立 entry)
  - bbox 要紧贴对象,不要包含周围空白

严格 JSON。
```

### 6.4 Stage B 错误处理与兜底重读

每个 region prompt(§6.3.1 / §6.3.2 / §6.3.3)在已列出的字段之外,**必须额外要求模型输出两个元字段**:

```
"_meta": {
  "extractedComplete": true | false,    // 是否完整提取所有可见信息
  "suggestedReSlice":                    // 仅当 extractedComplete=false 时填
    'vertical-N' | 'horizontal-N' | 'grid-MxN' | null
}
```

错误处理规则:
- **某个 region 整体失败 (网络 / 解析 / 超时)** → 该 region 的产出留空,`staleness` 标 `region_xxx_failed`
- **`_meta.extractedComplete === false`(模型自评不完整)** → 前端按 `suggestedReSlice` 重新切片重读一次。重读后仍 `false` 则采纳已读到的部分,`staleness` 标 `extracted_partial_xxx`
- **整体输出 confidence 偏低**(由后端聚合 keyFacts/layerSemantics 中各项 confidence 算出,low 占比 > 50%) → 仍写入,`staleness` 标 `low_confidence_xxx`

---

## 7. Stage C — 对象提取 详细设计

### 7.1 前提
Stage C 的输入来自 Stage B 主体区的 `candidateObjects`。如果 `candidateObjects` 为空 (Stage A 未识别主体区,或 Stage B 主体区精读失败),Stage C 整段跳过。

### 7.2 通用管线 (`ObjectExtractionPipeline.js`,新建)

抽象自现有 `LandBoundaryVisionTest.js` 的 8 阶段管线。

**对象提取的依赖顺序**: 部分对象类型的验证规则需要其他对象的 handles(例如"建筑退让线"需要先有"用地红线"才能验证偏移距离)。因此 Stage C 引入 `ExtractionContext` 作为**会话级上下文**,记录已提取并验证通过的对象 handles,后续提取可读取。

```javascript
// 会话级上下文,贯穿同一图纸下的多次 Stage C 调用
const context = {
  fileId,
  extractedObjects: {
    // 提取成功并验证通过的对象在此累积 (来源: 内存 + spatial-constraints 持久化)
    '用地红线': { handles: [...], area: 12345 },
    '建筑单体': { handles: [...], count: 5, totalArea: 8765 },
    // ...
  },
  keyFacts: [/* 从 DrawingMemory 加载 */]
}

async function extractObject(viewer, context, candidateBbox, objectType) {
  // 阶段 1: 重渲到候选区域
  await viewer.zoomTo(candidateBbox)
  const sharpShot = captureCurrentView(viewer)

  // 阶段 2: 视觉精读
  const result = await postObjectLocateRequest({
    objectType,
    image: sharpShot.dataUrl,
    layoutHint: '在这张图里精确定位 ' + objectType
  })
  // result: { screenPoints: [[x,y],...], confidence }

  // 阶段 3: 屏幕→世界坐标
  const worldPoints = result.screenPoints.map(p =>
    viewer.screenToWorld(p[0], p[1])
  )

  // 阶段 4: ODA 单点选择 (mode=7 嵌套穿透)
  const handles = []
  for (const wp of worldPoints) {
    const picked = viewer.selectByPoint(wp.x, wp.y, 7)
    if (picked) handles.push(...picked)
  }
  const uniqueHandles = [...new Set(handles)]

  // 阶段 5: 数值验证 (验证规则可读 context.extractedObjects 拿前置依赖)
  const rule = VALIDATION_RULES[objectType]
  const validation = rule
    ? rule({ viewer, handles: uniqueHandles, keyFacts: context.keyFacts, context })
    : { passed: null, reason: 'no_rule_for_type' }

  // 阶段 6: 高亮回馈 + 写回 context (供后续依赖此对象的提取使用)
  if (validation.passed) {
    viewer.flashByHandles(uniqueHandles)
    context.extractedObjects[objectType] = {
      handles: uniqueHandles,
      ...validation.measured ? { measured: validation.measured } : {}
    }
  }

  return {
    objectType,
    handles: uniqueHandles,
    validation,
    confidence: result.confidence
  }
}
```

**调用方负责的对象提取顺序约束**:
- "建筑退让线" 必须在 "用地红线" 之后调用
- "绿地" 验证依赖 "总用地面积" keyFact (无依赖其他对象)
- 调用方(如 ribbon 按钮触发器或审图清单调度器)按拓扑顺序调用 `extractObject`

### 7.3 数值验证规则 (按 objectType 切换)

每条规则签名统一为 `({ viewer, handles, keyFacts, context }) => ValidationResult`。前置依赖通过 `context.extractedObjects` 取得,而非额外参数。

```javascript
const VALIDATION_RULES = {
  '用地红线': ({ viewer, handles, keyFacts }) => {
    const totalArea = sumPolygonArea(viewer, handles)
    const expected = keyFacts.find(k => k.name === '总用地面积')?.value
    if (!expected) return { passed: null, reason: 'no_keyfact_to_validate' }
    const tolerance = 0.05  // 5%
    const error = Math.abs(totalArea - expected) / expected
    return {
      passed: error < tolerance,
      measured: totalArea,
      expected,
      errorPct: error * 100,
      reason: error < tolerance ? 'area_match' : 'area_mismatch'
    }
  },

  '建筑单体': ({ viewer, handles, keyFacts }) => {
    const count = handles.length
    const expectedCount = keyFacts.find(k => k.name === '建筑数量')?.value
    const totalArea = sumPolygonArea(viewer, handles)
    const expectedArea = keyFacts.find(k => k.name === '总建筑面积')?.value
    // 弱验证: 数量和面积都匹配为 'high';单个匹配为 'mid';都不匹配为 'low'
    const countOk = expectedCount && Math.abs(count - expectedCount) <= 1
    const areaOk = expectedArea && Math.abs(totalArea - expectedArea) / expectedArea < 0.15
    const passed = countOk && areaOk ? true : (countOk || areaOk ? null : false)
    return { passed, count, expectedCount, totalArea, expectedArea }
  },

  '建筑退让线': ({ viewer, handles, keyFacts, context }) => {
    // 依赖 context: 必须在"用地红线"提取并验证通过后调用
    const redLineHandles = context.extractedObjects['用地红线']?.handles
    if (!redLineHandles?.length) return { passed: null, reason: 'no_redline_to_compare' }
    const expectedSetback = keyFacts.find(k => k.name === '退让距离')?.value
    if (!expectedSetback) return { passed: null, reason: 'no_keyfact_to_validate' }
    const measuredOffset = computeOffsetFromRedline(viewer, handles, redLineHandles)
    const tolerance = 0.5  // 米
    return {
      passed: Math.abs(measuredOffset - expectedSetback) < tolerance,
      measured: measuredOffset,
      expected: expectedSetback
    }
  },

  '道路': ({ viewer, handles, keyFacts }) => {
    // 弱验证: 仅检查是否有合理宽度的线性对象
    return { passed: null, reason: 'weak_validation_only' }
  },

  '绿地': ({ viewer, handles, keyFacts }) => {
    const totalArea = sumPolygonArea(viewer, handles)
    const greenRatio = keyFacts.find(k => k.name === '绿地率')?.value
    const totalLandArea = keyFacts.find(k => k.name === '总用地面积')?.value
    if (!greenRatio || !totalLandArea) return { passed: null, reason: 'no_keyfact_to_validate' }
    const expectedGreenArea = totalLandArea * greenRatio / 100
    const tolerance = 0.1
    return {
      passed: Math.abs(totalArea - expectedGreenArea) / expectedGreenArea < tolerance,
      measured: totalArea,
      expected: expectedGreenArea
    }
  }
}
```

### 7.4 Stage C 不在首次打开自动跑

**重要边界**: Stage C 的视觉调用 + ODA 计算 + 验证耗时较长 (每个对象 5-15 秒,N 个对象总耗时 30-90 秒)。**首次打开图纸时不自动执行 Stage C**,而是:

- Stage A + Stage B 完成后,UI 提示"图纸记忆已建立 (基础信息),可开始审图"
- Stage C 在以下时机触发:
  - 用户点击 "智能审图" ribbon 上的具体审查按钮 (如 "建筑退线") 时,系统先确保红线已提取 → 触发 Stage C 提取该对象
  - 用户在 AI 助手中明确要求 "找一下用地红线" 时
  - 后续审图清单(本次设计 out of scope)按需调度

这种"懒加载"策略让首次打开 ≤ 30s 目标可达,同时把昂贵的 Stage C 推迟到真正需要时。

---

## 8. 数据模型变化 (DrawingMemory schema)

### 8.1 现有字段 (保留)
- `summary` — 增加 `drawingUnit` 字段
- `layerSemantics` — **保留但来源变更**:**不再由 Stage B 填**(图例与图层名常错配,强行匹配会污染);仅由 LLM 在对话中通过 `update_drawing_memory` 工具按需写入(LLM 在对话中实际查询了图层并确认匹配后才写)
- `keyFacts` — 来源从 LLM 文本归纳改为 Stage B 技经表视觉读取
- `metadata` — 保留 (createdAt, updatedAt, updateCount)
- `staleness` — 保留 + 新增多种 reason
- `application-form` — 保留
- `spatial-constraints` — 保留 (Stage C 写入)
- `qa-cache` — 保留

### 8.2 新增字段
```java
// DrawingMemory.java 新增
public record DrawingMemoryV2(
    Summary summary,
    List<LayerSemantic> layerSemantics,
    List<KeyFact> keyFacts,
    Map<String, Object> metadata,
    Staleness staleness,
    ApplicationForm applicationForm,
    Map<String, Object> spatialConstraints,
    Map<String, Object> qaCache,

    // === 新增 ===
    String mainAreaDescription,            // Stage B 主体区: 场景描述
    List<KeyAnnotation> keyAnnotations,    // Stage B 主体区: 关键标注
    List<CandidateObject> candidateObjects,// Stage B 主体区: Stage C 的路标
    List<LegendItem> legendItems           // Stage B 图例: 视觉约定 (无图层映射)
) {}

public record CandidateObject(
    String guess,              // 用地红线 / 建筑退让线 / 建筑单体 / 道路 / 绿地 / ...
    int[] bbox,                // 屏幕像素坐标
    int count,                 // 数量
    String confidence
) {}

public record LegendItem(
    String description,        // 图例右侧文字 (原文)
    String visualKind,         // 'line' | 'symbol' | 'pattern'
    String color,              // #RRGGBB 或 ""
    String lineType,           // 仅 visualKind=line 时填: solid|dashed|dot-dash|dotted|double
    String symbol,             // 仅 visualKind=symbol 时填
    String pattern,            // 仅 visualKind=pattern 时填
    String confidence
) {}
```

### 8.3 staleness reason 枚举 (新增)
- `stage_a_parse_failed`
- `stage_a_timeout`
- `region_技经表_failed` / `region_图例_failed` / `region_主体区_failed`
- `low_confidence_技经表` / `low_confidence_图例` / `low_confidence_主体区`
- `extracted_partial_技经表` / `extracted_partial_图例` / `extracted_partial_主体区` (Stage B 兜底重读后仍部分缺失)
- `用地红线_validation_failed` / `建筑单体_validation_failed` / `建筑退让线_validation_failed` / `绿地_validation_failed` (Stage C 验证不通过)

---

## 9. API 契约变化

### 9.1 POST `/api/drawing-memory/{client}/{file}/init` (改造)

**Before:**
```json
{
  "summary": "前端预处理的 5000 字摘要",
  "screenshotBase64": "..."
}
```

**After:**
```json
{
  "metadata": {
    "layers": [...],
    "layouts": [...],
    "extents": {...},
    "fileName": "..."
  },
  "fullScreenshot": "base64 jpeg"
}
```

返回 (同步):
```json
{
  "initialized": true,
  "stageA": {
    "drawingType": "...",
    "drawingUnit": "...",
    "drawingLayout": "...",
    "keyRegions": [...]
  }
}
```

### 9.2 POST `/api/drawing-memory/{client}/{file}/region` (新增)

```json
{
  "regionType": "技经表" | "图例" | "主体区",
  "images": ["base64...", "base64..."]   // 多图(切片) 或单图
}
```

返回 (同步):
```json
{
  "regionType": "...",
  "result": {
    // 按 regionType 不同
    // 技经表: { keyFacts: [...], _meta }
    // 图例:   { legendItems: [...], _meta }
    // 主体区: { mainAreaDescription, keyAnnotations, candidateObjects, _meta }
  },
  "confidence": "high|mid|low",
  "stalenessReasons": []
}
```

> **变更说明**: 图例输出从 `layerSemantics` 改为 `legendItems`。理由见 §6.3.2 — 图例描述与图层名常不一致,不做图层映射;`layerSemantics` 段改由 LLM 对话工具按需填充。

### 9.3 POST `/api/drawing-memory/{client}/{file}/object-locate` (新增,Stage C 用)

```json
{
  "objectType": "用地红线" | ...,
  "image": "base64 (重渲后的局部高清图)"
}
```

返回:
```json
{
  "screenPoints": [[x, y], ...],
  "confidence": "high|mid|low"
}
```

---

## 10. 删除清单

### 10.1 前端删除
| 文件 / 函数 | 删除理由 |
|---|---|
| `DwgResultSummarizer.js#_aggregateSiteAreas` | 用图层名猜类型再算面积 = 不可靠 (D6/D7) |
| `DwgResultSummarizer.js#summarizeForMemoryInit` 中"绿地: 合计 X ㎡"等聚合段落 | 同上 |
| `DwgReadAdapter.js#_categorizeSiteLayer` | 同上 |
| `LandBoundaryVisionTest.js` | 功能并入 `ObjectExtractionPipeline` |
| `LandBoundaryAnalyzer.js` | 功能并入新管线 |
| `siteAnalyzers/_shared/layerHints.js` 中"红线/绿地"猜测部分 | 同 _categorizeSiteLayer |
| `AiAssistant.jsx` 中 `RUN_LAND_BOUNDARY_TEST` 常量 | 落地后删 (临时保留至本设计落地) |
| `AiAssistant.jsx` 中 `AUTO_DRAWING_ANALYSIS_ENABLED` 守卫 | 新流程默认开启,删守卫 |

### 10.2 后端删除
| 文件 / 类 | 删除理由 |
|---|---|
| `DrawingMemoryInitService.SYSTEM_PROMPT` (Stage 2 纯文本归纳) | 被 Stage A + Stage B 视觉链路替代 |
| `DrawingMemoryInitService#doStage2` | 同上 |
| `DrawingTypeSkillProvider#classify` (单独的图纸类型分类) | 合并进 Stage A 一次调用 |
| `DrawingTypeSkillProvider.CLASSIFICATION_SYSTEM_PROMPT_WITH_VISION` | 替换为 `DrawingTypeAndLayoutPrompt` |

### 10.3 不删但改造
| 文件 / 函数 | 改造内容 |
|---|---|
| `DwgReadAdapter.extractComprehensive` | **保留**,但仅供对话中 LLM 工具按需调用,**首次打开链路不再调用** |
| `DwgReadTools.java` 全套 @Tool | 不动,作为对话中"按需深挖"的能力(Tool 体系收敛后续单独立项) |
| `DrawingMemoryStore` | 兼容新 schema 字段(mainAreaDescription / keyAnnotations / candidateObjects) |
| `DrawingMemoryPanel.jsx` | UI 增加新字段展示 |

---

## 11. 新增组件清单

### 11.1 前端
- `src/services/memory/VisionMemoryPipeline.js` — Stage A/B 调度主类
- `src/services/memory/sliceBbox.js` — 切片函数
- `src/services/memory/ObjectExtractionPipeline.js` — Stage C 通用管线 (抽象自 LandBoundaryVisionTest)
- `src/services/memory/validationRules.js` — Stage C 验证规则注册表

### 11.2 后端
- `memory/vision/StageAService.java` — Stage A 视觉全图分析
- `memory/vision/StageBService.java` — Stage B 区域精读分发器
- `memory/vision/regions/IndicatorTablePrompt.java` — 技经表 prompt
- `memory/vision/regions/LegendPrompt.java` — 图例 prompt
- `memory/vision/regions/MainAreaPrompt.java` — 主体区 prompt
- `memory/vision/ObjectLocateService.java` — Stage C 视觉精确定位
- `controller/DrawingMemoryController` 新增 endpoint: `/region`, `/object-locate`

---

## 12. 错误处理与降级策略汇总

| 失败点 | 行为 | UI 表现 |
|---|---|---|
| Stage A 视觉超时 (>30s) | 只填 metadata 进 summary,跳过 Stage B/C | "图纸记忆建立失败,基础元数据已保存" |
| Stage A JSON 解析失败 | 重试 1 次;再失败同上 | 同上 |
| Stage A keyRegions 为空 | 跳过 Stage B/C,只写 drawingType | "未识别到关键区域,请在对话中手动询问" |
| Stage B 某 region 失败 | 该 region 产出留空,其他正常 | 该字段标 staleness 灰显 |
| Stage B 兜底重读后仍 partial | 部分写入,标 `extracted_partial` | UI 提示"部分指标待确认" |
| Stage C 候选 bbox 为空 | 跳过 Stage C 整段 | UI 不显示"已识别对象"区 |
| Stage C 视觉精读失败 | 单个对象跳过 | 该对象不写 spatial-constraints |
| Stage C ODA selectByPoint 返 null | 单个对象跳过 | 同上 |
| Stage C 验证不通过 | 仍写 handles,但标 `xxx_validation_failed` | UI 红字提示"验证未通过" |

---

## 13. 性能预估

| 阶段 | 耗时 (P50) | 备注 |
|---|---|---|
| ① getLayersWithInfo | < 50ms | WASM 同步 |
| ② captureFullExtents | < 500ms | ODA 重渲全图 |
| Stage A | 8-15s | 视觉模型 (含网络) |
| Stage B (3 region 并行) | 8-15s | 取最慢一项,多图调用比单图慢 ~30% |
| 写 Redis | < 200ms | |
| **首次打开总耗时** | **18-30s** | 满足 ≤ 30s 目标 |
| Stage C (按需,每对象) | 5-15s | 不计入首次打开 |

---

## 14. 已知风险与应对

### 14.1 视觉模型识别错误
- **风险**: Stage A 把图签当技经表,把图例当主体区
- **应对**: confidence='low' 时不写入 keyFacts/layerSemantics 关键字段,只写描述字段

### 14.2 splitStrategy 误判
- **风险**: 模型判 single 但实际文字小,数字读错
- **应对**: 兜底重读机制 (Stage B 模型回 partial 时前端切片重读)
- **应对 2**: keyFacts 中关键指标(用地面积/建筑面积)在 Stage C 验证时会反查,数字明显错会被验证拦截

### 14.3 ODA selectByPoint 选错
- **风险**: mode=7 嵌套穿透选到块内子实体,而非整体红线
- **应对**: 验证规则中的"闭合面积"会校验,选错块内子实体时面积通常对不上 → 验证失败 → staleness

### 14.4 Stage B 主体区 candidateObjects 噪声多
- **风险**: 视觉模型框出大量 confidence=low 的候选,污染 Stage C 输入
- **应对**: Stage C 只处理 confidence='high' / 'mid';low 进 candidateObjects 但 Stage C 跳过

### 14.5 没有技经表的图纸
- **风险**: 单体建筑图通常无技经表,Stage C 验证规则失效
- **应对**: 验证规则按 drawingType 切换;ARCHITECTURAL_DESIGN 时 Stage C 默认跳过 (本设计的核心场景是规划/总平面图)

### 14.6 大尺寸 DWG 重渲性能
- **风险**: 复杂图纸 zoomTo + capture 单次 > 1s,Stage B 多次重渲累计耗时高
- **应对**: 预渲染策略 - Stage A 返回 keyRegions 后,前端可异步预渲染下一个 region 重叠 LLM 调用

---

## 15. 实施阶段建议(粗排,详细计划见后续 plan)

| 阶段 | 内容 | 依赖 |
|---|---|---|
| P1 — 基础重构 | 删除 `_aggregateSiteAreas` / `_categorizeSiteLayer` / Stage 2 prompt;前端 init 链路改用 `getLayersWithInfo` | (已关闭旧自动分析) |
| P2 — Stage A | Stage A prompt + schema + 后端 service + 前端调用;DrawingMemory schema 加 drawingUnit | P1 |
| P3 — Stage B | 三类 region 的 prompt + 切片函数 + 多图调用 + 兜底重读 + Memory schema 加 mainAreaDescription/keyAnnotations/candidateObjects | P2 |
| P4 — UI 适配 | DrawingMemoryPanel 显示新字段;接入新 init 流程 | P3 |
| P5 — Stage C | 抽象 `ObjectExtractionPipeline`;实现 5 类 validationRules;接入审图 ribbon 按钮的"按需触发" | P3 (Stage B candidateObjects 输出后) |
| P6 — 化石清理 | 删 LandBoundaryVisionTest / LandBoundaryAnalyzer / `RUN_LAND_BOUNDARY_TEST` / `AUTO_DRAWING_ANALYSIS_ENABLED` | P2-P5 落地 |

---

## 16. 与全栈重设计的关系

本设计是**全栈重设计**的第一站,聚焦"首次打开图纸自动归纳"这一条链路。后续单独立项的子项目(粗略路线图):

- **子项目 2**: Tool 体系收敛(后端 50+ @Tool 合并/删除),消除 read/write/atomic 重叠
- **子项目 3**: 审图清单状态机(checklist-driven review) — 把 ribbon 上的几十个审查按钮统一进同一个 session 模型
- **子项目 4**: 申请表 PDF 解析的优化与单元测试
- **子项目 5**: 多图纸对比 / 批量审查

---

## 17. 待确认 (本设计落地前需要)

无。所有架构决策已对齐 (D1-D9 均已选定)。

---

## 18. 设计验收标准

落地后需通过以下验证:

1. **功能验收**
   - 打开 3 张控规图,Stage A drawingType 全部正确
   - 打开 3 张总平面图,Stage B 提取的 keyFacts 中 "总用地面积/容积率/绿地率" 与人工核对误差 ≤ 5%
   - 打开 1 张包含图例的总平面图,Stage B 提取的 layerSemantics 与图例标注一致率 ≥ 80%
   - Stage C 提取用地红线,数值验证通过率 ≥ 90% (在已知技经表正确的前提下)

2. **性能验收**
   - 首次打开到记忆可用 P50 ≤ 30s
   - Stage C 单对象提取 P50 ≤ 15s

3. **降级验收**
   - 关闭网络后打开图纸,Stage A 失败,UI 正常提示,记忆有 metadata 占位
   - 故意上传无技经表的图纸,Stage B 技经表 region 失败,其他 region 正常
   - 故意上传与申请表数值不符的图纸,Stage C 验证失败,staleness 标记正确

4. **化石清理验收**
   - `AUTO_DRAWING_ANALYSIS_ENABLED` / `RUN_LAND_BOUNDARY_TEST` 两个开关已删除
   - `LandBoundaryVisionTest.js` / `LandBoundaryAnalyzer.js` 已删除
   - `_aggregateSiteAreas` / `_categorizeSiteLayer` 已删除
