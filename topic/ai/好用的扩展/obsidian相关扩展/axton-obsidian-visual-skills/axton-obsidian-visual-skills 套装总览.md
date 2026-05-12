---
title: axton-obsidian-visual-skills 套件总览
description: Claude Code 的 Obsidian 可视化 Skills 套件，支持 Canvas、Excalidraw、Mermaid 三种格式
created: 2026-05-10
tags:
  - ai
  - claude-code
  - obsidian
  - skill
  - 可视化
---

# axton-obsidian-visual-skills

> [!info] 项目信息
> - **仓库**：[axtonliu/axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills)
> - **作者**：Axton Liu（[axtonliu.ai](https://www.axtonliu.ai)）
> - **许可证**：MIT
> - **状态**：实验性（Experimental）

让 [[Claude Code]] 在 [[Obsidian]] 中生成 **[[Canvas]] / Excalidraw / [[Mermaid]]** 三种可视化格式。

## 什么是 Skills？

[[Skills]] 是 [[Claude Code]] 的提示词[[扩展机制]]，本质是 **Markdown 文件**，Claude 按需加载。相比 [[MCP 服务器]]不需要复杂配置。

## 包含的三个 Skill

| Skill | 输出格式 | 核心能力 | 详见 |
|-------|---------|---------|------|
| [[excalidraw-diagram skill]] | `.md`（内嵌 Excalidraw JSON） | 手绘风格图表，8 种图表类型 | 手绘美学，[[Obsidian]] 原生打开 |
| [[mermaid-visualizer skill]] | ````mermaid` 代码块 | 专业图表，内置语法错误预防 | 6 种图表，跨平台兼容 |
| [[obsidian-canvas-creator skill]] | `.canvas`（JSON Canvas） | 交互式画布，思维导图/自由布局 | 节点分组，颜色编码 |

## 安装

```bash
# 克隆仓库
git clone https://github.com/axtonliu/axton-obsidian-visual-skills.git

# 复制到 Claude Code skills 目录
cp -r axton-obsidian-visual-skills/excalidraw-diagram ~/.claude/skills/
cp -r axton-obsidian-visual-skills/mermaid-visualizer ~/.claude/skills/
cp -r axton-obsidian-visual-skills/obsidian-canvas-creator ~/.claude/skills/
```

也可按需只复制单个 skill。

> [!tip] 前置要求
> - 已安装 [[Claude Code]] CLI
> - [Obsidian](https://obsidian.md/)
> - Excalidraw 插件（仅 excalidraw-diagram 需要）

## 使用示例

```
# Excalidraw
"创建一个展示 [[CI/CD]] 流程的 Excalidraw 流程图"
"画一个关于机器学习概念的思维导图"

# Mermaid
"用 [[Mermaid]] 图表可视化这个流程"
"为 API 认证流程创建时序图"

# Canvas
"把这篇文章转换成 [[Obsidian]] [[Canvas]]"
"创建一个项目规划的思维导图 [[Canvas]]"
```

## 技术参考

| 参考 | 说明 |
|------|------|
| [[Excalidraw JSON Schema 参考]] | Excalidraw 元素类型、配色、JSON 结构 |
| [[Mermaid 语法规则参考]] | 语法错误预防、节点/子图/箭头规范 |
| [[Canvas 规范参考]] | JSON [[Canvas]] 文件格式规范 |
| [[Canvas 布局算法参考]] | MindMap/Freeform 布局算法详解 |

## 致谢

- [Excalidraw](https://excalidraw.com/) — 手绘风格白板
- [Mermaid](https://mermaid.js.org/) — 图表生成工具
- [JSON Canvas](https://jsoncanvas.org/) — 开放的无限画布格式

## 相关笔记

- [[更新日志]]
- [[插件]]
- [[obsidian-skills 套件总览]]
