---
title: Canvas 规范参考
description: Obsidian Canvas 的 JSON Canvas 文件格式完整规范
created: 2026-05-10
tags:
  - 参考
  - obsidian
  - canvas
  - json
  - 规范
---

# Canvas 规范参考

> [!note] 来源
> 整理自 [axton-obsidian-visual-skills/references/canvas-spec.md](https://github.com/axtonliu/axton-obsidian-visual-skills/blob/master/obsidian-canvas-creator/references/canvas-spec.md)，基于 [JSON Canvas](https://jsoncanvas.org/) 规范 v1.0

## 顶层结构

```json
{
  "nodes": [...],
  "edges": [...]
}
```

两个字段均为可选数组。

## 节点类型

### 公共必填字段

所有节点：`id`、`type`、`x`、`y`、`width`、`height`

可选公共字段：`color`

### 文本节点 (`text`)

存储 Markdown 格式纯文本。

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

引用 Vault 内文件。可选 `subpath` 链接到特定标题/块。

```json
{
  "id": "def456",
  "type": "file",
  "x": 300, "y": 0,
  "width": 400, "height": 300,
  "file": "Images/diagram.png"
}
```

带 subpath：
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

视觉容器，推荐添加 `label`。

可选字段：
- `label` — 分组标题
- `background` — 背景图片路径
- `backgroundStyle` — `cover`（填充）/ `ratio`（等比）/ `repeat`（平铺）

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

## 边（Edges）

连接节点的线条。

**必填**：`id`、`fromNode`、`toNode`

**可选**：

| 字段 | 选项 | 说明 |
|------|------|------|
| `fromSide` | `top`、`right`、`bottom`、`left` | 起始边 |
| `fromEnd` | `none`（默认）、`arrow` | 起点形状 |
| `toSide` | `top`、`right`、`bottom`、`left` | 终止边 |
| `toEnd` | `arrow`（默认）、`none` | 终点形状 |
| `color` | 预设 `"1"`-`"6"` 或 hex | 颜色 |
| `label` | 字符串 | 标签文本 |

```json
{
  "id": "edge1",
  "fromNode": "abc123",
  "fromSide": "bottom",
  "toNode": "def456",
  "toSide": "top",
  "toEnd": "arrow",
  "color": "3",
  "label": "导致"
}
```

## 颜色系统

### 预设颜色

| 值 | 颜色 | 跟随主题 |
|----|------|---------|
| `"1"` | 红色 | 是 |
| `"2"` | 橙色 | 是 |
| `"3"` | 黄色 | 是 |
| `"4"` | 绿色 | 是 |
| `"5"` | 青色 | 是 |
| `"6"` | 紫色 | 是 |

### 自定义 Hex

格式：`"#RRGGBB"`（大写），如 `"#4A90E2"`

> [!tip] 同一 Canvas 内保持格式一致。

## Z-Index 层叠

节点按数组顺序层叠：
1. 先放 group（底层）
2. 再放子分组
3. 最后放内容节点（顶层）

## 中文内容编码

| 原字符 | 替换为 |
|--------|--------|
| 中文双引号 `""` | `『』` |
| 中文单引号 `''` | `「」` |
| 英文双引号 `"` | `\"` |

## 验证要求

1. 所有 `id` 唯一（节点和边之间也不能重复）
2. 边的 `fromNode` / `toNode` 引用有效节点 ID
3. 必填字段完整
4. 坐标和尺寸为整数
5. 颜色格式统一

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Canvas 无法打开 | 检查 JSON 语法、ID 唯一性、边引用有效 |
| 节点重叠 | 增大间距（最小 320px 水平、200px 垂直） |
| 分组不显示 | 确保 group 在数组中先于内容节点，添加 `label` |
| 文本截断 | 增大节点尺寸或拆分为多节点 |
| 颜色不对 | 保持格式一致（全预设或全 hex） |

## 性能建议

- 节点数 < 500 保持流畅
- 使用压缩图片作为背景
- 节点文本保持简洁，长内容用 file 节点
- 减少交叉连线

---

→ 返回 [[obsidian-canvas-creator skill]] | [[axton-obsidian-visual-skills 套装总览]]
