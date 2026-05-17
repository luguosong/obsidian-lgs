---
title: Copilot CLI 插件总览
tags:
  - ai
  - 扩展
  - copilot-cli
created: 2026-05-17
updated: 2026-05-17
---

当前 GitHub Copilot CLI 环境中安装的全局扩展，按类型分类整理。配置目录：`~/.copilot/`。

> 对照参考：[[Claude Code 插件总览]]

---

## 配置目录结构

```
~/.copilot/
├── config.json              # 登录信息、已安装插件清单
├── settings.json            # 用户设置（model、enabledPlugins、footer 等）
├── mcp-config.json          # MCP 服务器配置
├── copilot-instructions.md  # 全局指令（角色、规范、行为）
├── user-hooks/              # 用户自定义 hook（当前为空）
├── global-skills/           # 本地全局 skill 包
├── installed-plugins/       # 从 marketplace 安装的插件缓存
│   ├── awesome-copilot/         # github/awesome-copilot
│   ├── superpowers-marketplace/ # obra/superpowers-marketplace
│   ├── copilot-plugins/         # 官方插件源
│   └── local/                   # 本地链接
├── agents/                  # 自定义 agent
├── skills/                  # 自定义 skill
└── session-state/           # 会话状态持久化
```

---

## 全局 Hooks

| Hook | 状态 | 说明 |
|------|------|------|
| user-hooks | 已注册但**目录为空** | 通过 `local` marketplace 注册为插件（`enabled: true`），但 `~/.copilot/user-hooks/` 下无自定义 hook 脚本 |

> 暂未配置任何执行时回调脚本。如需添加，可在 `~/.copilot/user-hooks/` 下放置 hook 文件。

---

## MCP 服务器

配置文件：`~/.copilot/mcp-config.json`

| MCP | 类型 | 用途 |
|-----|------|------|
| **context7** | HTTP (`https://mcp.context7.com/mcp`) | 第三方库文档查询，工具：`query-docs`、`resolve-library-id` |

> 仅注册一个全局 MCP。其余 MCP（如 `qmd`、IDEA MCP）由项目级或 IDE 侧管理。

---

## 全局 Skills

来源：本地插件 `global-skills@local`，路径 `~/.copilot/global-skills/skills/`。

| Skill | 触发场景 |
|-------|---------|
| **fix-bug** | 标准化 Bug 修复 TDD 流程：先写复现测试 → 修复 → 验证无回归 → 提交 |
| **code-review** | 分层代码审查（功能→安全→性能→可维护性），生成结构化 PR 描述 |
| **git-workflow** | Git 工作流：分支策略、commit message 规范、合并策略、冲突解决 |
| **e2e-tool-selection** | 端到端测试工具自动决策：`playwright-cli` vs `chrome-devtools-mcp` |
| **perf-profile** | 性能分析：前端 Core Web Vitals、后端慢查询、API 响应瓶颈 |
| **refactor** | 安全重构：先测试绑定，小步重构，持续验证绿色 |

---

## 已安装插件（Plugins）

配置在 `~/.copilot/settings.json` 的 `enabledPlugins` 中，共 **16 个**（含 `user-hooks` 与 `global-skills` 两个本地插件）。

### 开发工作流

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **superpowers** v5.1.0 | superpowers-marketplace | 14 个 skill 组成完整开发工作流：`brainstorming` `writing-plans` `executing-plans` `test-driven-development` `systematic-debugging` `dispatching-parallel-agents` `subagent-driven-development` `verification-before-completion` `requesting-code-review` `receiving-code-review` `finishing-a-development-branch` `using-git-worktrees` `using-superpowers` `writing-skills` |
| **rug-agentic-workflow** | awesome-copilot | 三 agent 协作：`rug-orchestrator`（编排）+ `swe-subagent`（实现）+ `qa-subagent`（QA） |
| **context-engineering** | awesome-copilot | 多文件改动的上下文规划：`context-architect` agent |
| **doublecheck** | awesome-copilot | AI 输出三层验证管道（自审 → 源验证 → 对抗审查） |

### 测试与质量

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **testing-automation** | awesome-copilot | TDD 三段式 agent：`tdd-red` `tdd-green` `tdd-refactor`，外加 `playwright-tester` |
| **polyglot-test-agent** | awesome-copilot | 多语言测试生成流水线：researcher / planner / implementer / builder / tester / fixer / linter / generator |

### 规划与文档

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **project-planning** | awesome-copilot | `plan` `planner` `prd` `implementation-plan` `task-planner` `task-researcher` `research-technical-spike` |
| **technical-spike** | awesome-copilot | 技术调研脚本：`research-technical-spike` agent |

### 语言与栈专属

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **java-development** | awesome-copilot | Java/Spring Boot/Quarkus 开发规范、测试、文档最佳实践 |
| **openapi-to-application-java-spring-boot** | awesome-copilot | 从 OpenAPI spec 生成 Spring Boot 应用骨架 |
| **frontend-web-dev** | awesome-copilot | 前端开发 agent：`electron-angular-native`、`expert-react-frontend-engineer` |
| **database-data-management** | awesome-copilot | 数据库 DBA agent：`ms-sql-dba`、`postgresql-dba` |

### 团队角色 Agent

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **software-engineering-team** | awesome-copilot | 7 个专家 agent：`se-system-architecture-reviewer`、`se-security-reviewer`、`se-ux-ui-designer`、`se-product-manager-advisor`、`se-technical-writer`、`se-gitops-ci-specialist`、`se-responsible-ai-code` |

### 其他

| 插件 | 来源 | 提供的能力 |
|------|------|-----------|
| **spark** | copilot-plugins | Spark 应用模板（`spark-app-template`） |
| **user-hooks** | local | 用户 hook 容器（目录为空） |
| **global-skills** | local | 全局 skill 容器（见上节 6 个 skill） |

---

## Marketplace 源

`~/.copilot/settings.json` 中 `extraKnownMarketplaces`：

| 名称 | 来源 |
|------|------|
| **awesome-copilot** | github/awesome-copilot |
| **superpowers-marketplace** | obra/superpowers-marketplace |
| **copilot-plugins** | 官方内置 |
| **local** | 本地链接 |

---

## 当前生效模型

`~/.copilot/settings.json` → `model: "claude-opus-4.7"`，`experimental: true`。

---

## 维护建议

- **新增 hook**：在 `~/.copilot/user-hooks/` 下添加脚本（当前为空，可作起点）
- **新增 MCP**：编辑 `~/.copilot/mcp-config.json` 的 `mcpServers`
- **新增全局 skill**：放入 `~/.copilot/global-skills/skills/<skill-name>/SKILL.md`
- **安装插件**：`copilot /plugin install <name>@<marketplace>`
- **查看清单**：直接读取 `settings.json` 的 `installedPlugins` / `enabledPlugins`

## 相关笔记

- [[Claude Code 插件总览]]
- [[推荐skill]]
- [[full-workflow-4tools]]
- [[00-superpower]]
