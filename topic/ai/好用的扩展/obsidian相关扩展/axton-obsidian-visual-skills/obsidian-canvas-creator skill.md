---
title: obsidian-canvas-creator skill
description: 创建 Obsidian Canvas 文件，支持思维导图和自由布局两种模式
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - canvas
  - 可视化
---

# obsidian-canvas-creator

> [!summary]
> 从[[文本内容]]创建交互式 [[Obsidian]] [[Canvas]]（`.canvas`）文件，输出有效的 JSON [[Canvas]] 格式，可直接在 [[Obsidian]] 中打开。

**触发词**：`Canvas`、`思维导图`、`可视化图表`、`mind map`

## 布局模式

| 模式 | 结构 | 适用场景 |
|------|------|---------|
| **思维导图** | 从中心向外的放射状层级 | 头脑风暴、主题探索、层级内容 |
| **自由布局** | 自定义位置、灵活连接 | 复杂网络、非层级内容、自定义排列 |

## 节点类型

所有节点共享的必填字段：`id`、`type`、`x`、`y`、`width`、`height`

### 文本节点 (`text`)

```json
{
  "id": "abc123",
  "type": "text",
  "x": 0, "y": 0,
  "width": 250, "height": 100,
  "text": "# 主题\n\n内容",
  "color": "4"
}
```

### 文件节点 (`file`)

引用 Vault 内其他文件或附件：

```json
{
  "id": "def456",
  "type": "file",
  "x": 300, "y": 0,
  "width": 400, "height": 300,
  "file": "Images/diagram.png"
}
```

可选 `subpath` 字段链接到特定标题/块：

```json
{ "file": "Notes/会议记录.md", "subpath": "#待办事项" }
```

### 链接节点 (`link`)

```json
{
  "id": "jkl012",
  "type": "link",
  "x": 0, "y": -200,
  "width": 250, "height": 100,
  "url": "https://obsidian.md",
  "color": "5"
}
```

### 分组节点 (`group`)

视觉容器，推荐添加 `label`：

```json
{
  "id": "group1",
  "type": "group",
  "x": -50, "y": -50,
  "width": 600, "height": 400,
  "label": "核心概念",
  "color": "4"
}
```

## 边（连接）

```json
{
  "id": "edge1",
  "fromNode": "abc123",
  "toNode": "def456",
  "fromSide": "right",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "3",
  "label": "导致"
}
```

| 字段 | 选项 | 说明 |
|------|------|------|
| `fromSide` / `toSide` | `top`、`right`、`bottom`、`left` | 连接方向 |
| `fromEnd` | `none`（默认）、`arrow` | 起点形状 |
| `toEnd` | `arrow`（默认）、`none` | 终点形状 |
| `color` | 预设 `"1"`-`"6"` 或 hex | 连线颜色 |
| `label` | 字符串 | 连线标签 |

## 配色方案

### 预设颜色

| 值 | 颜色 | 语义建议 |
|----|------|---------|
| `"1"` | 红色 | 警告、重要 |
| `"2"` | 橙色 | 行动项 |
| `"3"` | 黄色 | 问题、笔记 |
| `"4"` | 绿色 | 正面、完成 |
| `"5"` | 青色 | 信息、细节 |
| `"6"` | 紫色 | 概念、抽象 |

也支持自定义 hex：`"#4A90E2"`

> [!tip] 同一 [[Canvas]] 内保持颜色格式一致（全用预设或全用 hex）。

## 节点尺寸指南

| 文本长度 | 推荐尺寸 |
|---------|---------|
| <30 字符 | 220 × 100 px |
| 30-60 字符 | 260 × 120 px |
| 60-100 字符 | 320 × 140 px |
| >100 字符 | 320 × 180 px |

## Z-Index 层叠顺序

nodes 数组中的顺序决定层叠：
1. **先放 group 节点**（底层）
2. 再放子分组
3. 最后放文本/文件/链接节点（顶层）

## 关键规则

### 引号处理

| 原字符 | 替换为 |
|--------|--------|
| 中文双引号 `""` | `『』` |
| 中文单引号 `''` | `「」` |
| 英文双引号 `"` | `\"` |

### 间距要求

- 最小水平间距：**320px**（节点中心间）
- 最小垂直间距：**200px**（节点中心间）
- 计算时需考虑节点尺寸

### ID 生成

- 8-12 位随机 hex 字符串
- 所有节点和边的 ID 必须唯一

## 工作流程

1. **分析内容** → 识别主题、层级关系、关键点
2. **确定布局** → 思维导图（放射状）或自由布局（分区）
3. **规划结构** → 根节点 → 主分支 → 次级分支 → 叶节点
4. **生成 [[Canvas]]** → 节点 + 边 + 可选分组
5. **验证输出** → 唯一 ID、无重叠、有效引用、JSON 格式正确

## 完整示例

```json
{
  "nodes": [
    {
      "id": "g001", "type": "group",
      "x": -50, "y": -50,
      "width": 700, "height": 500,
      "label": "核心概念", "color": "4"
    },
    {
      "id": "c01", "type": "text",
      "x": 0, "y": 0,
      "width": 300, "height": 120,
      "text": "# 中心主题\n\n核心观点", "color": "4"
    },
    {
      "id": "b01", "type": "text",
      "x": 400, "y": -100,
      "width": 220, "height": 100,
      "text": "分支 A", "color": "5"
    },
    {
      "id": "b02", "type": "text",
      "x": 400, "y": 100,
      "width": 220, "height": 100,
      "text": "分支 B", "color": "5"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "fromNode": "c01", "fromSide": "right",
      "toNode": "b01", "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "e2",
      "fromNode": "c01", "fromSide": "right",
      "toNode": "b02", "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

## 更多参考

- [[Canvas 规范参考]] — JSON [[Canvas]] 完整规范
- [[Canvas 布局算法参考]] — MindMap/Freeform 布局算法详解
- [[axton-obsidian-visual-skills 套装总览]] — 返回项目总览
