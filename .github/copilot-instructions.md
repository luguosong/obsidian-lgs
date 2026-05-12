# Copilot Instructions

This is an **Obsidian knowledge vault** (~180 Markdown documents), not a software project. There are no build, test, or lint commands.

## Repository Structure

```
topic/           # 笔记主体（AI · Docker · Git · Linux · OAuth · Obsidian · 设计模式 · 密码学 等）
  <主题>/
    笔记/        # 正文笔记
    更新日志/    # 产品/工具的版本更新记录（可选）
    相关新闻/    # 新闻摘录（可选）
java/            # Java SE、Spring AI（内容待填充）
frontend/        # 前端笔记（内容待填充）
attachments/     # 图片等附件（全库共享）
Excalidraw/      # Excalidraw 图表源文件
UOCS开发/        # 特定项目开发文档（独立模块，勿混入 topic）
```

## Naming & Frontmatter Conventions

- **文件名用中文**，专有名词保留英文（如 `Docker Compose.md`、`Git.md`）
- 新笔记需包含 YAML frontmatter：

```yaml
---
title: 笔记标题
tags:
  - 标签1
  - 标签2
---
```

- 标题不用数字序号（`1.1`、`Step 1` 等），用语义化层级（`#` `##` `###`）

## Obsidian Flavored Markdown

- 内部链接：`[[页面名]]`，带别名：`[[页面名|显示文字]]`
- 图片嵌入：`![[image.png]]`（图片放 `attachments/`）
- Callout：`> [!note]`、`> [!warning]`、`> [!tip]` 等
- 代码块必须标注语言（`java`、`bash`、`yaml`、`typescript` 等）
- 笔记内代码注释用中文

## Available Skills

| Skill | 触发场景 |
|-------|---------|
| `obsidian-markdown` | 编写/校验 Obsidian Flavored Markdown 语法 |
| `obsidian-cli` | 通过 CLI 操作 Vault（读取、搜索、管理笔记） |
| `obsidian-bases` | 创建/编辑 `.base` 数据库视图文件 |
| `obsidian-canvas-creator` | 生成 `.canvas` 思维导图或自由布局文件 |
| `excalidraw-diagram` | 生成 Excalidraw 图表（流程图、架构图） |
| `mermaid-visualizer` | 生成 Mermaid 图表嵌入笔记 |
| `doc-translate` | 翻译英文 Markdown 为中文（>30KB 自动用 subagent） |
| `doc-changelog-updater` | 从 GitHub Releases 抓取新版本，更新 `更新日志/` 目录 |
| `doc-auto-link` | 补全正文中未链接的笔记标题，添加 `[[wikilink]]` |
| `defuddle` | 从网页 URL 提取干净的 Markdown 内容 |

## MCP Server

- **qmd**（`@tobilu/qmd`）：Markdown 文档查询与管理

## Obsidian Plugins (Installed)

`obsidian-excalidraw-plugin` · `terminal` · `obsidian-git` · `obsidian-minimal-settings` · `notebook-navigator` · `obsidian-quiet-outline`
