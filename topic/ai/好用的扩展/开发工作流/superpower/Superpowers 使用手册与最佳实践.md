---
title: "Superpowers 使用手册与最佳实践"
source: "https://github.com/obra/superpowers"
description: "一套面向编码 Agent 的可组合技能框架的完整使用手册，包含核心工作流教学、进阶技能指南和最佳实践。"
tags:
  - ai
  - 扩展
  - 开发工作流
---

## 引言：为什么需要方法论

你有没有经历过这样的场景：让 AI Agent 帮你写个功能，它二话不说直接开写，写到一半发现理解错了需求，删了重来；或者写完了才想起来没写测试，补测试的时候又改了实现逻辑；又或者在一个分支上同时改三个功能，最后 merge 的时候一团糟。

这些问题不是 Agent 的能力问题——是**方法论**的缺失。

Superpowers 是一套构建在编码 Agent 之上的**软件开发方法论**。它把 Jesse Vincent 多年的 Agent 协作经验提炼成 14 个可自动触发的 skill（技能），让 Agent 从"我说你做"变成一个有纪律的工程搭档。

核心理念用三句话概括：

- **流程优于猜测** — Agent 不会跳过设计直接写代码
- **证据优于断言** — 没有测试通过就不算完成
- **隔离优于混合** — 每个功能在独立工作区开发

> [!tip] 这篇手册适合谁？
> 已经会用 Claude Code（或其他编码 Agent），想通过 Superpowers 提升开发质量和效率的开发者。如果你还没用过编码 Agent，建议先熟悉基本操作再回来。

> 相关笔记：[[Superpowers：我在 2025 年 10 月如何使用编码代理]] — 了解 Superpowers 的诞生背景和设计哲学

## 安装与快速验证

> [!info] 完整安装步骤
> 本文只覆盖 Claude Code 平台。其他平台（Codex、Gemini CLI、Cursor 等）的安装方式请参考 [[Superpowers README]]。

在 Claude Code 中执行：

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

退出并重启 `claude`。

**验证安装成功：** 启动新会话后，你应该看到类似这样的注入提示：

```
<session-start-hook><EXTREMELY_IMPORTANT>
You have Superpowers.
```

也可以通过 `/plugins` 命令查看已安装插件列表，确认 Superpowers 处于启用状态。

> [!warning] 已废弃的用法
> 早期版本需要手动输入 `/superpowers:brainstorm` 等斜杠命令。现在 skill 会根据上下文自动触发，不需要手动调用。

## 场景：给 Todo 应用添加导出功能

接下来的六章，我们会跟随一个完整场景走完 Superpowers 的核心工作流。

**场景设定：** 你有一个 Next.js 写的 Todo 应用，用 Prisma + PostgreSQL 存储数据。你想加一个功能：用户可以把待办事项导出为 Markdown 文件。

为什么选这个场景？

- 简单到你能快速理解需求，不需要懂业务领域
- 涉及前后端（API 路由 + 下载按钮），能展示完整开发链路
- 有设计决策空间（导出全部还是筛选？即时下载还是生成后通知？），正好让 brainstorming skill 发挥作用

准备好了吗？出发。
