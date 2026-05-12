# 审查建筑退线距离 — 实现详细说明

> **状态**: 已实现 (P0 完成)
> **日期**: 2026-05-03
> **作者**: 协作产出 (zhoufs1205@gmail.com + Claude)
> **范围**: 前端 + 后端 (DrawingWebApp + drawing-ai-server)
> **关联文档**:
> - 退让距离审查初始设计: `DrawingWebApp/docs/specs/2026-04-26-setback-distance-review-design.md`
> - [[视觉化重构设计]] (Stage A/B/C): `DrawingWebApp/docs/specs/2026-04-30-drawing-memory-vision-init-design.md`
> - 东莞规划管理技术规定: `drawing-ai-server/src/main/resources/standard/东莞规划管理技术规定_2020/`

---

## 1. 背景与问题

### 1.1 审查需求

规划技术审查中，**建筑退线**是最核心的检查项之一。一个地块往往多面不同：

| 方向 | 外围条件 | 适用标准 (东莞) |
|:---:|---------|:---:|
| 北 | 沿 24m 宽道路 | 退道路红线 ≥5m |
| 东 | 相邻二类居住用地 | 退用地红线 ≥5m |
| 西 | 规划道路 15m | 退道路红线 ≥3m |
| 南 | 空地 | 退用地红线 ≥2m |

现有 `CurveMinDist` 命令只能计算**全局最短距离**，无法分方向判定。

### 1.2 制图不规范问题

总平面图中图层名称不规范是普遍现象：

- 道路实体可能在 `0` 层或自定义图层名上
- 相邻用地边界不一定有对应的线型图层
- 外围参考要素（道路红线、河岸线、绿地边界）未必作为独立实体绘制

**因此不能依赖图层名称判断外围条件，必须依赖视觉模型已分析的语义信息。**

### 1.3 已有基础

前序工作已交付以下能力：

| 能力 | 来源 | 状态 |
|------|------|:---:|
| Stage A/B 视觉分析 → `mainAreaDescription` | `2026-04-30-drawing-memory-vision-init-design.md` | ✅ 已上线 |
| 用地红线 + 建筑退让线双线识别 | `RedlinePipeline.js` (Stage C) | ✅ 已实现 |
| `spatialConstraints` 存储 (landBoundary + setbackLine) | `DrawingMemory.java` / `DrawingMemoryStore.java` | ✅ 已实现 |
| C++ `CurveSetbackDist` 面向参考线测距 | `ExPline.cpp` | ✅ 已实现 |
| 东莞规划管理技术规定 RAG 向量库 | `drawing-ai-server` Qdrant | ✅ 已入库 |

---

## 2. 设计目标与范围

### 2.1 目标

1. **一键触发** — 用户在审图 Ribbon 点击"建筑退线"按钮，自动完成测距 + 对照标准 + 出结论
2. **视觉语义驱动** — 各方向外围条件从 `mainAreaDescription`（[[Stage B]] 已分析）中提取，不依赖图层名
3. **有多少信息用多少** — 信息不足的方向标注"需人工确认"，不猜测
4. **方向自治** — 东南西北 4 个方向独立测距、独立判定、独立标注

### 2.2 范围

**In scope:**
- ReviewRibbon "建筑退线"按钮 → AI Chat 预设消息通道
- 方向分组退距测量 JS 代码示例 (`setback_distance_by_direction.js`)
- AI Skill `check_setback_distance.md`
- `layerHints.js` 新增 `river` 图层分类（为后续河流退让做准备）
- `window.__sendAiMessage` 全局桥接（ReviewRibbon → AiAssistant 通用通道）

**Out of scope (后续):**
- 高层建筑附加退距 (第 1.1.6 条：≥0.25H 且 ≥8m) — 需先获取建筑高度
- 河流退让分级表 (第 1.3.4 条) — 需确定河流等级
- 审图清单状态机集成 — 由清单系统统一调度
- 其余智能审图按钮（容积率、绿地率等）的接线 — 复用同一 `handleSendToAi` 通道

### 2.3 非功能要求

- 从按钮点击到审查结论 ≤ 45 秒 (P50)（含 1 次 JS 执行 + 1-2 次 RAG 检索 + LLM 推理）
- 前置条件不满足时（无红线/退让线 handle），LLM 应在 3 秒内提示用户先执行识别

---

## 3. 关键决策记录

| # | 决策 | 选择 | 理由 | 否决方案 |
|---|------|------|------|---------|
| D1 | 方向判定方式 | **质心向量主分量** | 不需要外围参考实体 handle；对矩形/近矩形地块足够准确 | 面向参考线点积法（需要 handleC，但图层名不可靠导致无法自动找到 C） |
| D2 | 外围条件识别 | **读取 mainAreaDescription** | [[Stage B]] 已用视觉模型分析过 2×2 切片，周边描述准确率高 | 图层名正则匹配（制图不规范时频繁误判） |
| D3 | 按钮通信方式 | **window.__sendAiMessage 全局函数** | 与 `window.__odaUi`、`window.__chatDiag` 模式一致；零耦合 | MobX Store 队列（需改 Store）；EventBus（增加一个新模块） |
| D4 | 信息不足处理 | **标注"需人工确认"** | 避免 LLM 幻觉猜测不存在的条件 | 默认取最严格标准（过于保守，可能误报不合规） |
| D5 | 代码示例分层 | **两个示例共存** | `by_direction` 供自动审查（无 handleC）；`facing_ref` 供手动精查（有 handleC） | 合并为一个（参数过多，LLM 调用困难） |

---

## 4. 总体架构 — 端到端流程

```
用户点击 ReviewRibbon "建筑退线" 按钮
  │
  ├── ① handleSendToAi('请审查建筑退线距离是否满足规范要求')
  │     editorStore.setActiveRightPanel('ai')   // 确保 AI 面板打开
  │     window.__sendAiMessage(msg)             // 通过全局桥接发送
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ AiAssistant.handleSend(msg)                                  │
│   → isReviewMessage('...审查...') === true                   │
│   → preCollectForReview(viewer, module)                      │
│   → sendMessage({ text: msg })  →  POST /api/chat           │
└─────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────┐
│ drawing-ai-server: LLM 接收消息                               │
│   → Skill 匹配: check_setback_distance.md                    │
│     keywords: [退让, 退线, 退缩, setback, 审查, 合规]         │
│     intents: [REVIEW_COMPREHENSIVE, REVIEW_SINGLE]           │
│                                                               │
│ LLM 按 Skill 三步流程执行:                                    │
└─────────────────────────────────────────────────────────────┘
  │
  ├── 步骤 ① 读取图纸记忆 + 分方向测距
  │     ├─ 读取 spatialConstraints.landBoundary.handles[0] → handleA
  │     ├─ 读取 spatialConstraints.setbackLine.handles[0]  → handleB
  │     ├─ 读取 mainAreaDescription → 周边描述文本
  │     ├─ search_code_examples("退缩距离 方向 setback direction")
  │     └─ execute_js_code(setback_distance_by_direction.js)
  │          传入 handleA, handleB
  │          返回 { directions: { north, south, east, west } }
  │
  ├── 步骤 ② 比对 mainAreaDescription 确定标准
  │     ├─ 解析 "南侧为南城路，路宽标注24m" → south = road, 24m
  │     ├─ 解析 "西侧为规划道路，路宽15m"   → west = road, 15m
  │     ├─ 解析 "东侧二类居住用地"          → east = adjacent_building_land
  │     ├─ 无信息方向                        → "需人工确认"
  │     └─ search_standards("建筑退缩 道路红线 退让距离")
  │
  └── 步骤 ③ 记录审查结论
        ├─ record_review_finding × N (每个方向)
        └─ generate_review_report (汇总)
```

---

## 5. 核心算法 — 方向分组退距测量

### 5.1 与原设计的差异

原设计 (`2026-04-26-setback-distance-review-design.md`) 采用**面向参考线方向测距**，需要三个 handle：

```
handleA (用地红线) + handleB (退让线) + handleC (外围参考实体)
```

本实现改用**质心向量方向分组**，仅需两个 handle：

```
handleA (用地红线) + handleB (退让线)
```

**改变原因：** 总平面图制图不规范，外围参考实体（道路红线、绿地边界等）的图层名不可靠，自动识别 handleC 的准确率低。而方向信息可以从 `mainAreaDescription`（视觉模型已分析）中直接获取。

### 5.2 算法步骤

```
输入: geA (用地红线几何), geB (建筑退让线几何)
输出: { north, south, east, west } 各方向最短退距 + 标注

Phase 1 — 计算用地红线质心 (64 点采样取平均)
  centroidPts = geA.getSamplePoints(64)
  cx = Σ(pt.x) / N
  cy = Σ(pt.y) / N

Phase 2 — 沿红线采样，按质心向外方向分组
  samplePts = geA.getSamplePoints(400)
  
  for each pA in samplePts:
    dx = pA.x - cx    // 质心→采样点向量
    dy = pA.y - cy
    
    // 按主分量确定方向（不用 atan2，避免角度边界问题）
    if |dx| >= |dy|:
      dir = dx > 0 ? 'east' : 'west'
    else:
      dir = dy > 0 ? 'north' : 'south'
    
    // 计算到退让线的距离
    pB = geB.closestPointTo(pA, tol)
    dist = ||pA - pB||
    
    // 更新该方向的最小距离
    groups[dir].update(dist, pA, pB)

Phase 3 — 交替投影精化 (每方向最多 20 轮)
  for each direction:
    for iter = 0..19:
      newB = geB.closestPointTo(bestA, tol)
      newA = geA.closestPointTo(newB, tol)
      newDist = ||newA - newB||
      if |newDist - minDist| < 1e-6: break
      bestA, bestB, minDist = newA, newB, newDist

Phase 4 — 创建对齐标注 (每方向一个 OdDbAlignedDimension)
```

### 5.3 方向分组示意

```
                    北 (north)
                   dy > 0, |dy| > |dx|
                       ╱ ╲
                      ╱   ╲
                     ╱     ╲
               ┌────╱───────╲────┐
               │   ╱ 用地红线 ╲   │
    西 (west)  │  ╱           ╲  │  东 (east)
   dx < 0      │ ╱    质心 ●   ╲ │   dx > 0
   |dx|>|dy|   │╱               ╲│   |dx|>|dy|
               │╲               ╱│
               │ ╲             ╱ │
               │  ╲           ╱  │
               │   ╲ 退让线  ╱   │
               └────╲───────╱────┘
                     ╲     ╱
                      ╲   ╱
                       ╲ ╱
                    南 (south)
                   dy < 0, |dy| > |dx|
```

### 5.4 交替投影精化

初始采样点间距约为红线周长 / 400。对于周长 800m 的地块，间距为 2m，最短距离可能偏差 ±2m。交替投影通过 A→B→A 反复找最近点，收敛到真实最短距离：

```
      geA ──── bestA₀ ─── bestA₁ ─── bestA₂ ──── (收敛)
                 ↕            ↕           ↕
      geB ──── bestB₀ ─── bestB₁ ─── bestB₂ ──── (收敛)
```

收敛条件：`|newDist - prevDist| < 1e-6` 或达到 20 轮上限。

---

## 6. 数据流与接口

### 6.1 ReviewRibbon → AiAssistant 通信

```
ReviewRibbon                              AiAssistant
     │                                         │
     │  editorStore.setActiveRightPanel('ai')   │
     │─────────────────────────────────────────→│  (面板打开/保持)
     │                                         │
     │  window.__sendAiMessage(msg)             │
     │─────────────────────────────────────────→│  handleSend(msg)
     │                                         │  → sendMessage to LLM
```

`window.__sendAiMessage` 在 AiAssistant 组件挂载时注册，卸载时清除：

```js
useEffect(() => {
  window.__sendAiMessage = handleSend
  return () => { delete window.__sendAiMessage }
}, [handleSend])
```

ReviewRibbon 侧使用 `requestAnimationFrame + retry` 确保 AiAssistant 已挂载：

```js
const handleSendToAi = useCallback((msg) => {
  if (editorStore.activeRightPanel !== 'ai') {
    editorStore.setActiveRightPanel('ai')
  }
  const trySend = (retries = 0) => {
    if (window.__sendAiMessage) {
      window.__sendAiMessage(msg)
    } else if (retries < 15) {
      setTimeout(() => trySend(retries + 1), 100)
    }
  }
  requestAnimationFrame(() => trySend())
}, [editorStore])
```

### 6.2 JS 代码执行结果格式

`setback_distance_by_direction.js` 的 `setResult` 输出：

```json
{
  "handleA": "B8D",
  "handleB": "C3F",
  "centroid": { "x": 250.5, "y": 180.3 },
  "totalSamples": 400,
  "directions": {
    "north": {
      "label": "北",
      "distance": 5.237,
      "ptOnRedline": { "x": 250.1, "y": 310.5 },
      "ptOnSetback": { "x": 250.1, "y": 305.3 },
      "sampleCount": 98,
      "annotated": true
    },
    "south": {
      "label": "南",
      "distance": 8.102,
      "ptOnRedline": { "x": 260.3, "y": 50.2 },
      "ptOnSetback": { "x": 260.3, "y": 58.3 },
      "sampleCount": 102,
      "annotated": true
    },
    "east": {
      "label": "东",
      "distance": 3.015,
      "ptOnRedline": { "x": 420.7, "y": 180.1 },
      "ptOnSetback": { "x": 417.7, "y": 180.1 },
      "sampleCount": 105,
      "annotated": true
    },
    "west": {
      "label": "西",
      "distance": 6.701,
      "ptOnRedline": { "x": 80.2, "y": 175.8 },
      "ptOnSetback": { "x": 86.9, "y": 175.8 },
      "sampleCount": 95,
      "annotated": true
    }
  }
}
```

### 6.3 mainAreaDescription 信息提取

LLM 从 `mainAreaDescription` 中提取各方向外围信息的映射逻辑：

```
mainAreaDescription 原文片段:
"周边道路：南侧为南城路，路宽标注24m；西侧为规划道路，路宽15m；北侧邻市政道路。
相邻地块：东侧为二类居住用地；南城路南侧为空地。"

LLM 解析结果:
┌───────┬───────────────────┬──────┬────────────────┐
│ 方向  │ 外围类型          │ 宽度 │ 适用条文        │
├───────┼───────────────────┼──────┼────────────────┤
│ 北    │ 道路(市政道路)     │ 未知 │ 无法确定标准    │
│ 南    │ 道路(南城路)       │ 24m  │ 第1.3.3条 ≥5m  │
│ 东    │ 居住用地(建筑基地) │  —   │ 第1.3.2条 ≥5m  │
│ 西    │ 道路(规划道路)     │ 15m  │ 第1.3.3条 ≥3m  │
└───────┴───────────────────┴──────┴────────────────┘
```

---

## 7. 适用标准速查

### 7.1 退用地红线 (第 1.3.2 条)

| 相邻用地类型 | 退用地红线 |
|------------|----------|
| 相邻建筑基地（含居住用地） | ≥5m |
| 相邻非建筑基地（绿地/广场/空地） | ≥2m |

### 7.2 退道路红线 (第 1.3.3 条)

| 道路红线宽度 | 退道路红线 |
|:-----------:|:---------:|
| ≥36m | ≥10m |
| ≥24m | ≥5m |
| ≥10m | ≥3m |
| <10m | 按具体情况 |

### 7.3 退河岸线 (第 1.3.4 条)

| 河流等级 | 退河岸线 |
|---------|---------|
| 海岸线 (生活岸线) | 100–125m |
| 一级河道 (东江北干流等) | 100–125m |
| 二级河道 | 50–75m |
| 三级河道 | 30–50m |
| 四级河道 | 20–30m |
| 其他河涌 | 10–20m |

### 7.4 高层建筑附加 (第 1.1.6 条)

| 条件 | 退让要求 |
|------|---------|
| 主体建筑面宽投影 >40m | ≥0.25H 且 ≥8m |
| 主体建筑面宽投影 ≤40m | ≥0.125H 且 ≥8m |

> ⚠️ 高层建筑附加退距当前 **Out of scope**，需先获取建筑高度 H 和立面投影长度。

---

## 8. 审查结论输出格式

LLM 调用 `record_review_finding` 后，`generate_review_report` 汇总输出：

```
═══════════════════════════════════════
  建筑退让距离审查报告
═══════════════════════════════════════

■ 南侧 — 沿南城路（路宽24m）
  测量距离: 8.102m（用地红线→建筑退让线）
  规范要求: ≥5.0m（第1.3.3条：道路宽度≥24m，退道路红线≥5m）
  判定结果: ✓ 合规（余量 3.1m）

■ 西侧 — 沿规划道路（路宽15m）
  测量距离: 6.701m（用地红线→建筑退让线）
  规范要求: ≥3.0m（第1.3.3条：道路宽度≥10m，退道路红线≥3m）
  判定结果: ✓ 合规（余量 3.7m）

■ 东侧 — 相邻二类居住用地
  测量距离: 3.015m（用地红线→建筑退让线）
  规范要求: ≥5.0m（第1.3.2条：相邻建筑基地，退用地红线≥5m）
  判定结果: ✗ 不合规（差 1.985m）

■ 北侧 — 邻市政道路（路宽未知）
  测量距离: 5.237m（用地红线→建筑退让线）
  规范要求: 未知（mainAreaDescription 中无道路宽度信息）
  判定结果: ⚠ 需人工确认

═══════════════════════════════════════
  综合结论: 东侧退让不足(差1.985m)；北侧需补充道路宽度后复核
═══════════════════════════════════════
```

---

## 9. 特殊场景处理

### 9.1 前置条件不满足

| 场景 | LLM 行为 |
|------|---------|
| `spatialConstraints` 中无 `landBoundary` | 提示用户先点击"亮显规划用地红线"完成识别 |
| `spatialConstraints` 中无 `setbackLine` | 提示用户重新运行红线识别（识别流程已含退让线） |
| `mainAreaDescription` 为空 | 提示"[[图纸记忆]]尚未建立"，建议关闭重新打开图纸触发 [[Stage B]] |
| 图纸类型不是总平面图 | 提示"建筑退线审查仅适用于总平面图" |

### 9.2 测距异常

| 场景 | 处理方式 |
|------|---------|
| 某方向无采样点（凹形地块极端情况） | `distance: null`，标注"需人工确认" |
| 退让线与红线重合（distance ≈ 0） | 标注"退让线与红线重合，退距为0" |
| 退让线在红线外侧（不合常理） | 标注"退让线位于红线外侧，请检查实体是否正确" |

### 9.3 异形地块

对于非矩形地块（L 形、三角形等），质心向量方向分组可能出现：
- 某个方向采样点过少（< 20 个）— 距离值可靠性降低
- 质心落在多边形外部（极端凹形）— 方向判断可能反转

**降级策略：** 代码示例在结果中包含 `sampleCount`，LLM 可据此判断可靠性。若 `sampleCount < 20`，建议改用手动精查模式（`setback_distance_facing_ref.js` + 用户指定参考方向）。

### 9.4 两个代码示例的适用场景

| 代码示例 | 输入 | 适用场景 | 触发方式 |
|---------|------|---------|---------|
| `setback_distance_by_direction.js` | handleA + handleB | 自动审查（一键全方向） | "建筑退线"按钮 |
| `setback_distance_facing_ref.js` | handleA + handleB + handleC | 手动精查（指定参考方向） | 对话中用户指定参考实体 |

---

## 10. 文件变更清单

### 已完成

| 文件 | 变更 | 类型 |
|------|------|:---:|
| `DrawingWebApp/src/components/AiAssistant/AiAssistant.jsx` | 暴露 `window.__sendAiMessage = handleSend` | 修改 |
| `DrawingWebApp/src/components/Ribbon/ReviewRibbon.jsx` | 新增 `handleSendToAi` 通用 handler；"建筑退线"按钮接线 | 修改 |
| `DrawingWebApp/src/services/siteAnalyzers/_shared/layerHints.js` | 新增 `river` 图层分类 (河流/水系/河岸/蓝线/河道) | 修改 |
| `drawing-ai-server/.../code_examples/setback_distance_by_direction.js` | 方向分组退距测量（无需参考实体） | 新建 |
| `drawing-ai-server/.../code_examples/setback_distance_facing_ref.js` | 面向参考线退距测量（需 handleC） | 新建 |
| `drawing-ai-server/.../skills/check_setback_distance.md` | AI Skill：三步审查流程 | 新建 |

### 前序已完成（双线识别）

| 文件 | 变更 |
|------|------|
| `drawing-ai-server/.../dto/ObjectLocateResult.java` | 多目标定位结构 `List<LocatedObject>` |
| `drawing-ai-server/.../ObjectLocateService.java` | `LocateRequest` 支持多 target |
| `drawing-ai-server/.../DrawingMemoryController.java` | `/object-locate` 支持多目标；`/spatial-constraints` 支持 setbackLine |
| `drawing-ai-server/.../DrawingMemory.java` | `SpatialConstraints` 新增 `SetbackLine` |
| `DrawingWebApp/src/services/DrawingMemoryApi.js` | `postObjectLocate` 支持多 target |
| `DrawingWebApp/src/services/memory/RedlinePipeline.js` | 双线识别（红线 + 退让线同时识别） |

### 前序已完成（C++）

| 文件 | 变更 |
|------|------|
| `Drawing/Examples/ExCommands/ExPline.cpp` | `computeCurveCentroid`, `findMinDistFacingRef`, `_CurveSetbackDist_func` |
| `Drawing/Examples/ExCommands/DbCmdDef.h` | 注册 `CurveSetbackDist` 命令 |

### 待实现 (P1/P2)

| 文件 | 变更 | 优先级 |
|------|------|:-----:|
| `drawing-ai-server` prompt 组装层 | 规划审查模式下自动注入 `check_setback_distance` skill | P1 |
| `DrawingWebApp/src/components/AiAssistant/constants.js` | `suggestions` 中新增"检查建筑退线"快捷选项 | P2 |
| 其余智能审图按钮 (容积率/绿地率等) | 复用 `handleSendToAi` 通道接线 | P2 |
| 高层建筑附加退距 | 需获取建筑高度 H 和立面投影长度 | P2 |
| 河流退让分级 | 需确定河流等级 | P2 |

---

## 11. 与原设计文档的演进关系

本文档是对 `2026-04-26-setback-distance-review-design.md` 的**实现演进**：

| 维度 | 原设计 (04-26) | 本实现 (05-03) |
|------|---------------|---------------|
| 方向判定 | 需外围参考实体 handleC | 质心向量分组，无需 handleC |
| 外围识别 | 图层名正则 + 文字标注 | `mainAreaDescription` 视觉语义 |
| 触发方式 | 未定义 | ReviewRibbon 按钮 → AI Chat 预设消息 |
| 代码示例 | 1 个 (facing_ref) | 2 个 (by_direction + facing_ref) |
| 审查流程 | 四步 (识别参考→测距→对照→出结论) | 三步 (测距→比对描述→出结论) |
| 信息不足 | 默认 `non_building_land` ≥2m | 标注"需人工确认"，不猜测 |

原设计的 `setback_distance_facing_ref.js` 保留为手动精查场景使用，与新增的 `setback_distance_by_direction.js` 并存。

## 相关笔记

- [[specs]]
- [[首次打开图纸自动归纳 — 视觉化重构设计]]
- [[图例分析功能设计规格]]
- [[ArcGIS Web 服务集成 — C++ 实施架构]]
- [[GIS服务 Ribbon 标签页设计规格]]
- [[GIS服务 Ribbon 标签页 Implementation Plan]]
- [[GIS File Import / Save-Back Design]]
- [[GIS服务 Ribbon 标签页 — 后续实施设计]]
