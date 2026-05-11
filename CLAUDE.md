# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

Obsidian 知识库（Vault），包含技术学习笔记，约 180 篇 Markdown 文档。**不是软件项目，没有构建/测试/lint 命令。**

## 目录结构

```
topic/           # 笔记主体
  ai/            # Claude Code、GitHub Copilot CLI、Agent SDK、扩展推荐
  docker/        # Docker 基础、Compose、Swarm、安全扫描、Harbor、CICD
  git/           # Git 内部原理、分支、变基、钩子、协作、高级工具
  linux/         # 入门、Shell、文件系统、网络、进程管理、编程接口
  oauth/         # OAuth 标准
java/            # Java SE、Spring AI（目录已建，内容待填充）
frontend/        # 前端笔记（目录已建，内容待填充）
attachments/     # 图片等附件
```

每个 topic 下按子主题分目录，每个子主题含 `笔记/` 和/或 `更新日志/` 子目录。

## Obsidian 配置

- **主题**：Minimal（配合 `snippets/headings.css` 自定义标题样式）
- **字体**：Source Code Pro + LXGW WenKai
- **已安装插件**：Excalidraw、Terminal、Obsidian Git、Minimal Settings、Quiet Outline、Notebook Navigator

## 编辑笔记时的规则

- 文件名用中文，除非涉及专有名词（如 "Docker"、"Spring"）
- 使用 Obsidian Flavored Markdown：wikilinks (`[[页面名]]`)、callouts (`> [!type]`)、frontmatter properties
- 图片等附件放 `attachments/` 目录，用 `![[image.png]]` 嵌入
- 代码块标注语言标识符（`java`、`bash`、`yaml` 等）
- 笔记内代码注释用中文

## 已配置的 Claude Skills

| Skill | 用途 |
|-------|------|
| `obsidian-markdown` | Obsidian 风格 Markdown 语法（wikilinks、callouts、properties、embeds） |
| `obsidian-cli` | Obsidian CLI 操作 |
| `obsidian-bases` | Obsidian Bases 数据库功能 |
| `obsidian-canvas-creator` | 生成 `.canvas` 文件（思维导图、自由布局） |
| `excalidraw-diagram` | 生成 Excalidraw 图表（流程图、架构图） |
| `mermaid-visualizer` | 生成 Mermaid 图表 |
| `doc-translate` | 翻译英文 Markdown 为中文，原地覆盖（>30KB 文件自动用 subagent） |

## MCP 服务器

- **qmd**（`@tobilu/qmd`）：Markdown 文档查询与管理

## 常见操作

- **新建笔记**：在对应 `topic/<主题>/笔记/` 下创建 `.md` 文件，带 frontmatter
- **翻译文档**：使用 `/doc-translate` skill，指定文件或目录路径
- **画图**：使用 `/excalidraw-diagram` 或 `/mermaid-visualizer`
