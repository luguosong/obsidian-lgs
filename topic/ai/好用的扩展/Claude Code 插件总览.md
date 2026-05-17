---
title: Claude Code 插件总览
tags:
  - ai
  - 扩展
  - claude-code
created: 2026-05-17
updated: 2026-05-17
---

当前 Claude Code 环境中安装的全局扩展，按类型分类整理。

---

## 一、插件（Plugins）— 15 个

通过 `/install-plugin` 安装，配置在 `~/.claude/settings.json` 的 `enabledPlugins` 中。

### 开发工作流

| 插件 | 版本 | 提供的 Skills / 能力 | 说明 |
|------|------|---------------------|------|
| **superpowers** | 5.1.0 | `brainstorming` `dispatching-parallel-agents` `executing-plans` `verification-before-completion` `subagent-driven-development` `systematic-debugging` `receiving-code-review` `writing-skills` `finishing-a-development-branch` `using-superpowers` `using-git-worktrees` `writing-plans` `requesting-code-review` `test-driven-development` | 14 个 skill 组成完整开发工作流：头脑风暴 → 计划 → TDD → 代码审查 → 收尾分支 |
| **feature-dev** | - | `feature-dev`（含 subagent: `code-architect` `code-explorer` `code-reviewer`） | 功能开发全流程：架构设计 → 代码探索 → 代码审查 |
| **commit-commands** | - | `commit` `commit-push-pr` `clean_gone` | Git 提交快捷命令：单提交、提交+推送+PR、清理已删除远程分支 |
| **code-review** | - | `code-review` | 独立代码审查 skill |
| **code-simplifier** | 1.0.0 | `code-simplifier` subagent | 审查最近修改的代码，简化并提升可维护性 |
| **security-guidance** | - | 安全审查规则注入 | 提供安全编码指导和检查规则 |

### 文档与内容生成

| 插件 | 版本 | 提供的 Skills / 能力 | 说明 |
|------|------|---------------------|------|
| **document-skills** | 98669c11 | `pdf` `docx` `pptx` `xlsx` `canvas-design` `web-artifacts-builder` `brand-guidelines` `algorithmic-art` `theme-factory` `webapp-testing` `mcp-builder` `internal-comms` `doc-coauthoring` `slack-gif-creator` `claude-api` `frontend-design` | Anthropic 官方文档生成套件，支持 PDF、Word、PPT、Excel、Canvas、Web 应用等 16 种输出格式 |
| **frontend-design** | - | `frontend-design` | 前端 UI 设计与实现 |
| **skill-creator** | - | `skillify` | 创建和编辑自定义 skill |

### 开发工具

| 插件 | 版本 | 提供的 Skills / 能力 | 说明 |
|------|------|---------------------|------|
| **context7** | - | MCP 工具：`resolve-library-id` `query-docs` | 实时查询任意库/框架的最新文档和代码示例 |
| **claude-md-management** | 1.0.0 | `revise-claude-md` `claude-md-improver` | 管理和优化 CLAUDE.md 配置文件 |
| **jdtls-lsp** | 1.0.0 | Java LSP（跳转定义、引用查找、类型提示） | Java 语言服务器，提供代码智能 |
| **typescript-lsp** | 1.0.0 | TypeScript LSP（跳转定义、引用查找、类型提示） | TypeScript 语言服务器，提供代码智能 |

### 界面与体验

| 插件 | 版本 | 提供的 Skills / 能力 | 说明 |
|------|------|---------------------|------|
| **claude-hud** | 0.0.12 | `setup` `configure` + 状态栏渲染 | 自定义终端状态栏，显示模型、token 用量等信息 |
| **learning-output-style** | 1.0.0 | 学习模式输出风格 | 结合交互式学习与教育性解释的输出模式 |

---

## 二、全局 Skills — 47 个

安装在 `~/.claude/skills/` 目录，提供 DevOps 全流程覆盖。来源：Gstack 生态。

### 部署与发布

| Skill | 说明 |
|-------|------|
| `ship` | 一键发布流程 |
| `land-and-deploy` | 合并分支并部署 |
| `canary` | 金丝雀发布 |
| `setup-deploy` | 配置部署环境 |
| `benchmark` / `benchmark-models` | 性能基准测试 |
| `cso` | 客户成功运营 |
| `document-release` | 生成发布文档 |

### 浏览器与测试

| Skill | 说明 |
|-------|------|
| `browse` | Web 浏览操作（使用 Chrome DevTools） |
| `connect-chrome` | 连接 Chrome 浏览器 |
| `chrome-devtools-cli` | Chrome DevTools CLI 操作 |
| `playwright-cli` | Playwright E2E 测试 |
| `setup-browser-cookies` | 配置浏览器 Cookies |
| `qa` / `qa-only` | 自动化 QA 测试 |

### 计划与审查

| Skill | 说明 |
|-------|------|
| `autoplan` | 自动生成实施计划 |
| `plan-ceo-review` / `plan-eng-review` / `plan-design-review` / `plan-devex-review` | 多角色计划审查（CEO、工程、设计、开发体验） |
| `plan-tune` | 计划调优 |
| `design-consultation` / `design-review` / `design-shotgun` / `design-html` | 设计咨询与审查 |
| `devex-review` | 开发体验审查 |
| `review` | PR 预合入审查 |
| `investigate` | 深度调查分析 |

### 工作流控制

| Skill | 说明 |
|-------|------|
| `careful` | 谨慎模式，降低变更风险 |
| `freeze` / `unfreeze` | 冻结/解冻代码变更 |
| `guard` | 代码守护 |
| `gstack` / `gstack-upgrade` | Gstack 主入口与升级 |
| `retro` | 回顾会议 |
| `codex` | Codex 集成 |

### 知识与辅助

| Skill | 说明 |
|-------|------|
| `setup-gbrain` / `sync-gbrain` | GBrain 知识库配置与同步 |
| `learn` / `context-save` / `context-restore` | 学习与上下文保存/恢复 |
| `scrape` | 网页抓取 |
| `make-pdf` | PDF 生成 |
| `office-hours` | 办公时间调度 |
| `find-skills` | 发现可用 skills |
| `health` | 健康检查 |
| `pair-agent` | 配对编程 agent |
| `landing-report` | 着陆报告 |
| `open-gstack-browser` | 打开 Gstack 浏览器 |

---

## 三、全局 MCP 服务器 — 4 个

配置在 `~/.claude.json` 的 `mcpServers` 中，所有项目共享。

| MCP 服务器 | 通信方式 | 提供的工具 | 说明 |
|-----------|---------|-----------|------|
| **zai-mcp-server** | stdio (`npx @z_ai/mcp-server`) | `analyze_image` `analyze_video` `analyze_data_visualization` `extract_text_from_screenshot` `diagnose_error_screenshot` `ui_to_artifact` `ui_diff_check` `understand_technical_diagram` | 多模态 AI 分析：图片/视频理解、OCR、错误诊断、UI 对比、技术图表解读 |
| **zread** | HTTP | `get_repo_structure` `read_file` `search_doc` | 读取 GitHub 仓库的目录结构、文件内容和文档搜索 |
| **web-search-prime** | HTTP | `web_search_prime` | 网页搜索，返回标题、URL、摘要 |
| **web-reader** | HTTP | `webReader` | 抓取网页并转为大模型友好的 Markdown 格式 |

> [!info] 插件附带的 MCP
> **context7** 插件同时提供 MCP 工具 `resolve-library-id` 和 `query-docs`，见上方插件表格。

---

## 四、全局 Hooks

配置在 `~/.claude/settings.json` 的 `hooks` 字段中。

> [!note] 当前状态
> 全局 `settings.json` 中未配置任何 hooks（`hooks` 字段为空）。`~/.claude/hooks/` 目录下仅有 GSD (get-shit-done) 的后台更新检查 worker (`gsd-check-update-worker.js`)，由 GSD skill 在 SessionStart 时自动调用，用于检测新版本和过期 hooks。
