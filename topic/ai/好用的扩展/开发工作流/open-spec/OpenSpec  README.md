---
title: "OpenSpec：AI 编程助手的规格驱动开发"
source: "https://github.com/Fission-AI/OpenSpec"
description: "AI 编程助手的规格驱动开发 (SDD) 框架。"
tags:
  - ai
  - spec-driven-development
  - tool
---

[![OpenSpec logo](https://github.com/Fission-AI/OpenSpec/raw/main/assets/openspec_bg.png)](https://github.com/Fission-AI/OpenSpec)

**最受喜爱的 spec 框架。** 我们的理念：

```
→ 灵活而非僵化
→ 迭代而非瀑布
→ 简单而非复杂
→ 为棕地项目而生，不只是绿地项目
→ 从个人项目到企业级，皆可扩展
```

> [!tip] 新功能
> **新工作流已上线！** 我们用全新的 artifact 引导式工作流重建了 OpenSpec。
>
> 运行 `/opsx:propose "你的想法"` 即可开始。→ [了解更多](https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md)

关注 [@0xTab on X](https://x.com/0xTab) 获取更新 · 加入 [OpenSpec Discord](https://discord.gg/YctCnvvshC) 获取帮助和提问。

## 实际效果

```
You: /opsx:propose add-dark-mode
AI:  Created openspec/changes/add-dark-mode/
     ✓ proposal.md — 为什么做，改什么
     ✓ specs/       — 需求和场景
     ✓ design.md    — 技术方案
     ✓ tasks.md     — 实现清单
     准备就绪！

You: /opsx:apply
AI:  正在实现任务...
     ✓ 1.1 添加 theme context provider
     ✓ 1.2 创建切换组件
     ✓ 2.1 添加 CSS 变量
     ✓ 2.2 接入 localStorage
     所有任务完成！

You: /opsx:archive
AI:  已归档至 openspec/changes/archive/2025-01-23-add-dark-mode/
     Spec 已更新。准备下一个功能。
```

**OpenSpec Dashboard**

[![OpenSpec dashboard preview](https://github.com/Fission-AI/OpenSpec/raw/main/assets/openspec_dashboard.png)](https://github.com/Fission-AI/OpenSpec/blob/main/assets/openspec_dashboard.png)

## 快速开始

**需要 Node.js 20.19.0 或更高版本。**

全局安装 OpenSpec：

```bash
npm install -g @fission-ai/openspec@latest
```

然后进入你的项目目录并初始化：

```bash
cd your-project
openspec init
```

现在告诉你的 AI：`/opsx:propose <你想构建的功能>`

如果需要扩展工作流（`/opsx:new`、`/opsx:continue`、`/opsx:ff`、`/opsx:verify`、`/opsx:bulk-archive`、`/opsx:onboard`），通过 `openspec config profile` 选择，然后用 `openspec update` 应用。

> [!note] 兼容性
> 不确定你的工具是否受支持？[查看完整列表](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) — 我们支持 25+ 工具，数量还在增长。
>
> 同时支持 pnpm、yarn、bun 和 nix。[查看安装选项](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md)。

## 文档

→ **[Getting Started](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)**：入门指引
→ **[Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)**：工作流组合与模式
→ **[Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)**：slash commands 与 skills
→ **[CLI](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)**：终端命令参考
→ **[Supported Tools](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)**：工具集成与安装路径
→ **[Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)**：核心概念
→ **[Multi-Language](https://github.com/Fission-AI/OpenSpec/blob/main/docs/multi-language.md)**：多语言支持
→ **[Customization](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md)**：自定义配置

## 社区 Schema

第三方 schema 包通过独立仓库分发——它们提供将 OpenSpec 与其他工具集成的偏好化工作流，类似于 [github/spec-kit 的社区扩展目录](https://github.com/github/spec-kit/tree/main/extensions) 处理工具集成的方式。

→ 在自定义文档中 **[浏览目录](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md#community-schemas)**。

## 为什么选择 OpenSpec？

AI 编程助手很强大，但当需求只存在于聊天记录中时，结果往往不可预测。OpenSpec 添加了一个轻量级的 spec 层，让你在任何代码编写之前就达成共识。

- **先对齐再动手** — 人和 AI 在写代码前先对齐 spec
- **保持条理** — 每个变更都有独立的文件夹，包含 proposal、specs、design 和 tasks
- **灵活工作** — 随时更新任何 artifact，没有僵化的阶段门禁
- **使用你的工具** — 通过 slash commands 支持 20+ AI 助手

### 与同类工具对比

**对比 [Spec Kit](https://github.com/github/spec-kit)**（GitHub）— 全面但偏重。有僵化的阶段门禁，大量 Markdown 文件，需要 Python 环境。OpenSpec 更轻量，允许自由迭代。

**对比 [Kiro](https://kiro.dev/)**（AWS）— 强大但被锁定在他们的 IDE 中，且仅限于 Claude 模型。OpenSpec 与你已有的工具配合使用。

**对比什么也不用** — 没有 spec 的 AI 编程意味着模糊的 prompt 和不可预测的结果。OpenSpec 带来了可预测性，而没有繁琐的流程。

## 更新 OpenSpec

**升级包**

```bash
npm install -g @fission-ai/openspec@latest
```

**刷新 Agent 指令**

在每个项目中运行以下命令，重新生成 AI 指导文件并确保最新的 slash commands 处于激活状态：

```bash
openspec update
```

## 使用注意事项

> [!tip] 模型选择
> OpenSpec 在高推理能力的模型上表现最佳。推荐使用 Opus 4.5 和 GPT 5.2 进行规划和实现。

> [!info] Context 卫生
> OpenSpec 受益于干净的 context window。在开始实现前清空你的 context，并在整个会话中保持良好的 context 卫生。

## 贡献指南

**小修复** — Bug 修复、错别字修正和小的改进可以直接提交 PR。

**大变更** — 对于新功能、重大重构或架构变更，请先提交一份 OpenSpec 变更 proposal，以便在开始实现前对齐意图和目标。

撰写 proposal 时，请记住 OpenSpec 的理念：我们服务于各种 coding agent、模型和用场景的广泛用户群体。变更应该对所有人都适用。

**欢迎 AI 生成的代码** — 前提是已经过测试和验证。包含 AI 生成代码的 PR 应说明使用的 coding agent 和模型（例如"使用 Claude Code 和 claude-opus-4-5-20251101 生成"）。

### 开发

- 安装依赖：`pnpm install`
- 构建：`pnpm run build`
- 测试：`pnpm test`
- 本地开发 CLI：`pnpm run dev` 或 `pnpm run dev:cli`
- 约定式提交（单行）：`type(scope): subject`

## 其他

**遥测**

OpenSpec 收集匿名使用统计数据。

我们仅收集命令名称和版本号，用于了解使用模式。不收集参数、路径、内容或个人身份信息 (PII)。在 CI 环境中自动禁用。

**退出遥测：** `export OPENSPEC_TELEMETRY=0` 或 `export DO_NOT_TRACK=1`
