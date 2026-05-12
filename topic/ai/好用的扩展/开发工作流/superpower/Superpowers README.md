---
title: "Superpowers：编码 Agent 技能框架"
source: "https://github.com/obra/superpowers"
description: "一套面向编码 Agent 的可组合技能框架与软件开发方法论。"
author:
tags:
  - ai
  - 扩展

---
字数：988

## Superpowers

[[Superpowers]] 是一套完整的编码 Agent 软件开发方法论，构建在一组可组合的 skill (技能) 之上，配合初始指令确保 Agent 正确使用它们。

## 快速开始

为你的 Agent 赋予 [[Superpowers]]：[Claude Code](#claude-code)、[Codex CLI](#codex-cli)、[Codex App](#codex-app)、[Factory Droid](#factory-droid)、[Gemini CLI](#gemini-cli)、[OpenCode](#opencode)、[Cursor](#cursor)、[GitHub Copilot CLI](#github-copilot-cli)。

## 工作原理

从你启动编码 Agent 的那一刻就开始了。当它发现你在构建东西时，*不会*立刻跳去写代码，而是退后一步，问你到底想做什么。

一旦通过对话理清了需求，它会分段展示给你，每段都短到足以让你真正阅读和消化。

在你确认设计方案后，Agent 会制定一份[[实施计划]]——清晰到连一个热情有余、判断力不足、缺乏项目上下文、不爱写测试的初级工程师都能跟着做。它强调真正的红绿 TDD (Red/Green TDD)、YAGNI (You Aren't Gonna Need It) 和 DRY (Don't Repeat Yourself)。

接下来，你说"go"，它就会启动 *subagent-driven-development*（子 Agent 驱动开发）流程——让各个 Agent 逐一完成工程任务，检查和审查它们的工作，然后继续推进。Claude 按照你制定的计划自主工作两三个小时不跑偏是常有的事。

还有很多其他功能，但以上是这套系统的核心。而且由于 skill 会自动触发，你不需要做任何特殊操作——你的编码 Agent 天生就有 [[Superpowers]]。

## 赞助

如果 [[Superpowers]] 帮你赚到了钱，并且你愿意的话，非常欢迎[赞助我的开源工作](https://github.com/sponsors/obra)。

谢谢！

— Jesse

## 安装

安装方式因 harness (运行环境) 而异。如果你使用多个环境，需要分别安装。

### Claude Code

[[Superpowers]] 可通过[官方 Claude 插件市场](https://claude.com/plugins/superpowers)获取。

#### 官方市场

- 从 Anthropic [[官方市场]]安装插件：
	```
	/plugin install superpowers@claude-plugins-official
	```

#### Superpowers 市场

[[Superpowers]] 市场提供 [[Superpowers]] 及其他相关 [[Claude Code]] 插件。

- 注册市场：
	```
	/plugin marketplace add obra/superpowers-marketplace
	```
- 从该市场安装插件：
	```
	/plugin install superpowers@superpowers-marketplace
	```

### Codex CLI

[[Superpowers]] 可通过[官方 Codex 插件市场](https://github.com/openai/plugins)获取。

- 打开插件搜索界面：
	```
	/plugins
	```
- 搜索 [[Superpowers]]：
	```
	superpowers
	```
- 选择 `Install Plugin`。

### Codex App

[[Superpowers]] 可通过[官方 Codex 插件市场](https://github.com/openai/plugins)获取。

- 在 Codex App 中，点击侧边栏的 Plugins。
- 你应该能在 Coding 分区看到 `Superpowers`。
- 点击 [[Superpowers]] 旁边的 `+`，按提示操作。

### Factory Droid

- 注册市场：
	```
	droid plugin marketplace add https://github.com/obra/superpowers
	```
- 安装插件：
	```
	droid plugin install superpowers@superpowers
	```

### Gemini CLI

- 安装扩展：
	```
	gemini extensions install https://github.com/obra/superpowers
	```
- 后续更新：
	```
	gemini extensions update superpowers
	```

### OpenCode

OpenCode 使用自己的插件安装机制；即使你已经在其他环境中安装过，也需要单独为 OpenCode 安装。

- 告诉 OpenCode：
	```
	Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
	```
- 详细文档：[docs/README.opencode.md](https://github.com/obra/superpowers/blob/main/docs/README.opencode.md)

### Cursor

- 在 Cursor Agent 聊天中，从市场安装：
	```
	/add-plugin superpowers
	```
- 或在插件市场中搜索 "superpowers"。

### GitHub Copilot CLI

- 注册市场：
	```
	copilot plugin marketplace add obra/superpowers-marketplace
	```
- 安装插件：
	```
	copilot plugin install superpowers@superpowers-marketplace
	```

## 基本工作流

1. **brainstorming**（头脑风暴）——在写代码前激活。通过提问打磨粗略想法，探索替代方案，分段展示设计以供验证。保存[[设计文档]]。
2. **using-git-worktrees**——在设计确认后激活。在新分支上创建隔离工作区，运行项目设置，验证干净的测试基线。
3. **writing-plans**（编写计划）——在设计确认后激活。将工作拆分为小任务（每个 2-5 分钟）。每个任务包含精确的文件路径、完整代码和验证步骤。
4. **subagent-driven-development** 或 **executing-plans**——在计划就绪后激活。为每个任务分派独立的子 Agent，执行两阶段审查（先检查是否符合规格，再检查代码质量）；或分批执行并在关键节点暂停等待人工确认。
5. **test-driven-development**——在实现过程中激活。强制执行 RED-GREEN-REFACTOR 循环：写失败测试、看着它失败、写最少的代码、看着它通过、提交。会删除先于测试编写的代码。
6. **requesting-code-review**——在任务之间激活。对照计划审查，按严重程度报告问题。Critical 级别的问题会阻塞进度。
7. **finishing-a-development-branch**——在所有任务完成后激活。验证测试，提供选项（merge/PR/保留/丢弃），清理 worktree。

> [!important] Agent 在执行任何任务前会检查是否有相关的 skill。这些是强制工作流，不是建议。

## 内容概览

### 技能库

**测试**

- **test-driven-development**——RED-GREEN-REFACTOR 循环（包含测试反模式参考）

**调试**

- **systematic-debugging**——4 阶段根因分析流程（包含根因追踪、纵深防御、条件等待等技术）
- **verification-before-completion**——确保问题真正被修复

**协作**

- **brainstorming**——苏格拉底式设计打磨
- **writing-plans**——详细的[[实施计划]]
- **executing-plans**——带检查点的分批执行
- **dispatching-parallel-agents**——并发的子 Agent 工作流
- **requesting-code-review**——预审查清单
- **receiving-code-review**——响应审查反馈
- **using-git-worktrees**——并行开发分支
- **finishing-a-development-branch**——合并/PR 决策工作流
- **subagent-driven-development**——带两阶段审查的快速迭代（先检查规格符合度，再检查代码质量）

**元技能**

- **writing-skills**——按照最佳实践创建新 skill（包含测试方法论）
- **using-superpowers**——[[技能系统]]入门介绍

## 设计哲学

- **测试驱动开发**——始终先写测试
- **系统化优于临时应对**——流程优于猜测
- **降低复杂度**——简洁是首要目标
- **证据优于断言**——验证之后才算完成

阅读[原始发布公告](https://blog.fsck.com/2025/10/09/superpowers/)。

## 贡献指南

[[Superpowers]] 的一般贡献流程如下。请注意，我们通常不接受新 skill 的贡献，对现有 skill 的任何更新都必须在我们支持的所有编码 Agent 上正常运行。

1. Fork 仓库
2. 切换到 `dev` 分支
3. 为你的工作创建分支
4. 按照 `writing-skills` skill 创建和测试新的或修改过的 skill
5. 提交 PR，确保填写 PR 模板

完整指南见 `skills/writing-skills/SKILL.md`。

## 更新

[[Superpowers]] 的更新方式因编码 Agent 而异，但通常是自动的。

## 许可证

MIT License——详见 LICENSE 文件。

## 社区

[[Superpowers]] 由 [Jesse Vincent](https://blog.fsck.com/) 和 [Prime Radiant](https://primeradiant.com/) 的伙伴们共同打造。

- **Discord**：[加入我们](https://discord.gg/35wsABTejz)，获取社区支持、提问，分享你用 [[Superpowers]] 构建的东西
- **Issues**：[https://github.com/obra/superpowers/issues](https://github.com/obra/superpowers/issues)
- **版本公告**：[注册](https://primeradiant.com/superpowers/) 以获取新版本通知
