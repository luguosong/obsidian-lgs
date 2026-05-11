---
title: excalidraw-diagram skill
description: 用 Excalidraw 格式生成手绘风格图表，输出 Obsidian 原生 .md 文件
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - excalidraw
  - 可视化
---

# excalidraw-diagram

> [!summary]
> 从文本内容生成 Excalidraw 图表，输出 Obsidian-ready 的 `.md` 文件，包含内嵌的 Excalidraw JSON，可被 Obsidian Excalidraw 插件原生打开。

**触发词**：`Excalidraw`、`画图`、`流程图`、`思维导图`、`可视化`、`diagram`

## 支持的图表类型

| 类型 | 适用场景 | 做法 |
|------|---------|------|
| **流程图** | 步骤说明、工作流程、任务执行顺序 | 箭头连接各步骤 |
| **思维导图** | 概念发散、主题分类、灵感捕捉 | 中心向外发散 |
| **层级图** | 组织结构、内容分级、系统拆解 | 自上而下层级节点 |
| **关系图** | 要素间影响、依赖、互动 | 连线表示关联 |
| **对比图** | 方案/观点对照分析 | 左右两栏或表格 |
| **时间线图** | 事件发展、项目进度、模型演化 | 时间轴 + 关键节点 |
| **矩阵图** | 双维度分类、任务优先级 | XY 坐标平面 |
| **自由布局** | 零散灵感、初步信息收集 | 无结构限制 |

## 工作流程

1. 分析内容 → 识别概念、关系、层级
2. 选择图表类型（参考上表）
3. 生成 Excalidraw JSON
4. 生成 Obsidian `.md` 文件（含 frontmatter）
5. 自动保存到当前目录
6. 通知用户文件路径

## 输出文件格式

文件必须严格按照以下结构：

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==
You can decompress Drawing data with the command palette:
'Decompress current Excalidraw file'.
For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
`​``json
{完整 JSON 数据}
`​``
%%
```

> [!warning] 关键要点
> - Frontmatter 必须有 `tags: [excalidraw]`
> - 警告信息必须完整保留
> - JSON 必须被 `%%` 标记包围
> - 只能用 `excalidraw-plugin: parsed`，不能用其他值

## 设计规则

### 文本处理

- **字体**：所有文本必须用 `fontFamily: 5`（Excalifont 手写字体）
- **双引号**：`"` → `『』`
- **圆括号**：`()` → `「」`
- **字号**：标题 24-28px / 副标题 18-20px / 正文 14-16px
- **行高**：`lineHeight: 1.25`

### 配色方案

| 用途 | 颜色 | Hex |
|------|------|-----|
| 标题 | 深蓝 | `#1e40af` |
| 副标题/连接线 | 亮蓝 | `#3b82f6` |
| 正文 | 灰色 | `#374151` |
| 强调 | 金色 | `#f59e0b` |

### 布局

- 画布范围：0-1200 × 0-800 像素
- 坐标原点：左上角 (0,0)
- 元素 ID：唯一字符串（如 `title`、`box1`）
- Index 字段：`a1`、`a2`、`a3`...

## JSON 元素模板

所有元素的公共字段：

```json
{
  "id": "unique-id",
  "type": "rectangle",
  "x": 100, "y": 100,
  "width": 200, "height": 50,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "index": "a1",
  "roundness": {"type": 3},
  "seed": 123456789,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1751928342106,
  "link": null,
  "locked": false
}
```

文本元素额外字段：

```json
{
  "text": "显示文本",
  "rawText": "显示文本",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": null,
  "originalText": "显示文本",
  "autoResize": true,
  "lineHeight": 1.25
}
```

## 元素绑定

### 文本绑定到容器

```json
// 容器
{ "id": "container-id", "boundElements": [{"id": "text-id", "type": "text"}] }
// 文本
{ "id": "text-id", "containerId": "container-id" }
```

### 箭头绑定到形状

```json
{
  "type": "arrow",
  "startBinding": {"elementId": "source-id", "focus": 0, "gap": 5},
  "endBinding": {"elementId": "target-id", "focus": 0, "gap": 5}
}
```

## 更多参考

- [[Excalidraw JSON Schema 参考]] — 元素类型、配色、完整 JSON 结构
- [[axton-obsidian-visual-skills 套装总览]] — 返回项目总览
