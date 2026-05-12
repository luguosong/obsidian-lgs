---
title: Excalidraw JSON Schema 参考
description: Excalidraw 元素类型、配色方案和完整 JSON 结构参考
created: 2026-05-10
tags:
  - 参考
  - excalidraw
  - json
  - schema
---

# Excalidraw JSON Schema 参考

> [!note] 来源
> 整理自 [axton-obsidian-visual-skills/references/excalidraw-schema.md](https://github.com/axtonliu/axton-obsidian-visual-skills/blob/master/excalidraw-diagram/references/excalidraw-schema.md)

## 顶层结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## 配色方案

### 主色

| 用途 | 颜色 | Hex |
|------|------|-----|
| 标题 | 深蓝 | `#1e40af` |
| 副标题 | 中蓝 | `#3b82f6` |
| 正文 | 深灰 | `#374151` |
| 强调 | 橙色 | `#f59e0b` |
| 成功 | 绿色 | `#10b981` |
| 警告 | 红色 | `#ef4444` |

### 背景色

| 用途 | Hex |
|------|-----|
| 浅蓝背景 | `#dbeafe` |
| 浅灰中性 | `#f3f4f6` |
| 浅橙高亮 | `#fef3c7` |
| 浅绿成功 | `#d1fae5` |
| 浅紫强调 | `#ede9fe` |

## 元素类型

### 矩形 (`rectangle`)

```json
{
  "type": "rectangle",
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "roundness": {"type": 3}
}
```

### 文本 (`text`)

```json
{
  "type": "text",
  "text": "内容",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent"
}
```

### 箭头 (`arrow`)

```json
{
  "type": "arrow",
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#374151",
  "strokeWidth": 2,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

### 椭圆 (`ellipse`)

```json
{
  "type": "ellipse",
  "strokeColor": "#10b981",
  "backgroundColor": "#d1fae5",
  "fillStyle": "solid"
}
```

### 菱形 (`diamond`)

```json
{
  "type": "diamond",
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid"
}
```

### 线条 (`line`)

```json
{
  "type": "line",
  "points": [[0, 0], [200, 100]],
  "strokeColor": "#374151",
  "strokeWidth": 2
}
```

## 字体值

| 值 | 字体名 |
|----|--------|
| 1 | Virgil（手绘） |
| 2 | Helvetica |
| 3 | Cascadia |
| 4 | Assistant |
| **5** | **Excalifont（推荐）** |

## 填充样式

| 值 | 效果 |
|----|------|
| `solid` | 实心 |
| `hachure` | 斜线填充 |
| `cross-hatch` | 交叉线填充 |
| `dots` | 点状填充 |

## 圆角类型

| 值 | 效果 |
|----|------|
| `{"type": 1}` | 直角 |
| `{"type": 2}` | 微圆角 |
| `{"type": 3}` | **全圆角（推荐）** |

## 元素绑定

文本绑定到容器时，容器需声明 `boundElements`，文本需设置 `containerId`。

---

→ 返回 [[excalidraw-diagram skill]] | [[axton-obsidian-visual-skills 套装总览]]

## 相关笔记

- [[axton-obsidian-visual-skills 套件总览]]
- [[Canvas 布局算法参考]]
- [[Canvas 规范参考]]
- [[Mermaid 语法规则参考]]
- [[mermaid-visualizer skill]]
- [[obsidian-canvas-creator skill]]
- [[json-canvas skill]]
