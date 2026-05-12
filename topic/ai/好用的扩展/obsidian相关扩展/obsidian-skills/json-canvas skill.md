---
title: json-canvas skill
description: 创建和编辑 JSON Canvas 文件，支持节点、边、分组和样式
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - canvas
  - json-canvas
  - 可视化
---

# json-canvas

> [!summary]
> 创建和编辑 **JSON [[Canvas]]**（`.canvas`）文件——[[Obsidian]] 团队发起的开放标准（[jsoncanvas.org](https://jsoncanvas.org/)），支持节点、边、分组和样式，用于无限画布可视化。

**触发词**：`canvas 文件`、`JSON Canvas`、`.canvas`、`思维导图`、`架构图`、`无限画布`

## 文件格式

`.canvas` 文件是 JSON，顶层结构：

```json
{
  "nodes": [...],
  "edges": [...]
}
```

## 节点类型（Nodes）

所有节点共享：`id`、`type`、`x`、`y`、`width`、`height`、`color`（可选）

### 文本节点 (`text`)

```json
{
  "id": "node-1",
  "type": "text",
  "x": 100, "y": 100,
  "width": 300, "height": 200,
  "text": "# 标题\n\n支持 **Markdown**"
}
```

### 文件节点 (`file`)

引用 vault 中的笔记或附件。可选 `subpath` 指向特定标题/块。

```json
{
  "id": "node-2",
  "type": "file",
  "x": 500, "y": 100,
  "width": 400, "height": 300,
  "file": "笔记/项目概述.md",
  "subpath": "#核心目标"
}
```

### 网页节点 (`link`)

```json
{
  "id": "node-4",
  "type": "link",
  "x": 100, "y": 400,
  "width": 600, "height": 400,
  "url": "https://obsidian.md"
}
```

### 分组节点 (`group`)

视觉容器，推荐添加 `label`。

```json
{
  "id": "group-1",
  "type": "group",
  "x": 50, "y": 50,
  "width": 800, "height": 600,
  "label": "项目规划区",
  "background": "path/to/bg.png",
  "backgroundStyle": "cover"
}
```

`backgroundStyle`：`cover`（填充）/ `ratio`（等比）/ `repeat`（平铺）/ `center`（居中）

## 边（Edges）

| 字段 | 选项 | 说明 |
|------|------|------|
| `fromSide` / `toSide` | `top`、`right`、`bottom`、`left` | 连接方向 |
| `fromEnd` | `none`（默认）、`arrow` | 起点形状 |
| `toEnd` | `arrow`（默认）、`none` | 终点形状 |
| `color` | 预设 `"1"`-`"6"` 或 hex | 颜色 |
| `label` | 字符串 | 标签 |

```json
{
  "id": "edge-1",
  "fromNode": "node-1", "fromSide": "right", "fromEnd": "none",
  "toNode": "node-2", "toSide": "left", "toEnd": "arrow",
  "color": "#0288d1",
  "label": "连接说明"
}
```

## 颜色规范

### 预设颜色

| 编号 | 颜色 |
|------|------|
| `"1"` | 红色 |
| `"2"` | 橙色 |
| `"3"` | 黄色 |
| `"4"` | 绿色 |
| `"5"` | 蓝色 |
| `"6"` | 紫色 |

也支持 hex：`"color": "#ff6b6b"`

## 坐标系

- 原点 `(0, 0)` 在画布中央
- X 轴向右为正，Y 轴**向下为正**
- 推荐节点间距 ≥ 50px，最小尺寸 200×80

## 使用示例

```
# 架构图
创建微服务架构 canvas，展示 API 网关、服务、数据库的调用关系

# 思维导图
创建"深度学习"主题思维导图，5 个分支各展开 2-3 子节点

# 学习路线图
创建 Python 学习路线 canvas，用颜色区分阶段，引用 vault 笔记

# 项目看板
创建项目规划 canvas，用分组区分需求/开发/测试/发布阶段
```

## 协作关系

- [[obsidian-markdown skill]]：canvas 中的文件节点引用 markdown 笔记
- [[obsidian-cli skill]]：通过 CLI 将 `.canvas` 写入 vault

## 相关笔记

> [!tip] 增强版 [[Canvas]] Skill
> [[axton-obsidian-visual-skills 套装总览]] 中的 [[obsidian-canvas-creator skill]] 是本 skill 的增强版，额外支持：
> - 思维导图/自由布局两种模式
> - 自动布局算法（放射树、网格分区、力导向）
> - 智能节点尺寸和碰撞检测
>
> 详见 [[Canvas 规范参考]] 和 [[Canvas 布局算法参考]]

## 参考链接

- [JSON Canvas 官方规范](https://jsoncanvas.org/)
- [Obsidian Canvas 使用指南](https://help.obsidian.md/Plugins/Canvas)

---

→ 返回 [[obsidian-skills 套件总览]]
