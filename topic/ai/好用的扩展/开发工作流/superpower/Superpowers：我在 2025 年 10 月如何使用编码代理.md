---
title: "Superpowers：我在 2025 年 10 月如何使用编码代理"
source: "https://blog.fsck.com/2025/10/09/superpowers/"
description: "我是 Jesse。我造东西——软件、硬件，偶尔也搞点麻烦。"
author:
published: 2025-10-09
---
字数：2132
感觉就像几天前我才刚写完"[2025 年 9 月我如何使用编码代理](https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025/)"。

在那篇文章的开头，我提到我的流程在那之后又有所演进。

过去几周，我一直在开发一套工具，用于更好地提取和系统化我的流程，并更好地引导我的 Agent 搭档。我原本计划这个周末开始记录这套系统，但今天早上 Anthropic 推出了 [Claude Code 的插件系统](https://docs.claude.com/en/docs/claude-code/plugins)。

如果你不想继续往下读，想直接玩我的新玩具，它们已经足够自助化了。你需要 Claude Code 2.0.13 或更高版本。启动后运行：

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

退出并重启 `claude` 后，你会看到一段注入的提示：

```
<session-start-hook><EXTREMELY_IMPORTANT>
You have Superpowers.

**RIGHT NOW, go read**: @/Users/jesse/.claude/plugins/cache/Superpowers/skills/getting-started/SKILL.md
</EXTREMELY_IMPORTANT></session-start-hook>
```

这就是 `Superpowers` 的引导入口。它教会 Claude 几件重要的事情：

1. 你拥有 skills（技能）。它们赋予你 Superpowers。
2. 通过运行脚本来搜索 skills，通过阅读 skills 来使用它们——按照其中的指示执行。
3. 如果你拥有某个 skill 来完成某项任务，你*必须*使用该 skill 来执行该活动。

## 编码工作流

它还内置了我[之前写过](https://blog.fsck.com/2025/10/05/how-im-using-coding-agents-in-september-2025/)的头脑风暴 → 计划 → 实现工作流。最大的变化是你不再需要手动运行命令或粘贴提示。如果 Claude 认为你正在启动一个项目或任务，它*应该*默认先和你讨论计划，然后再开始实现。

头脑风暴完成后，如果你在一个 git 仓库中，它会自动创建一个 worktree 并切换到该目录。这意味着你可以在同一个项目上启动并行任务，而不会互相覆盖。

然后它会让你选择：

1. 上个月的流程（你打开第二个 `claude` 会话，充当架构师和实现者的人工 PM）
2. 本月的新流程——它将任务逐个分派给 subagent（子代理）来实现，然后在继续之前对每个任务进行代码审查

无论哪种方式，Claude 都会实践 RED/GREEN TDD（测试驱动开发）：先写一个失败的测试，只实现足够的代码让该测试通过，然后继续。

在实现过程结束时，Claude 现在会提供选项：创建 GitHub Pull Request、将 worktree 本地合并回源分支，或者直接停止。

但这些都不是有趣的部分。

## 有趣的部分

Skills 才是有趣的部分。而且你很快就会听到……几乎所有人都在谈论它们。

Skills 赋予你的 Agent Superpowers。

我第一次真正注意到 skills 是几周前 Anthropic 推出改进的 Office 文档创建功能时。功能发布后，我去翻了翻——让 Claude 跟我讲讲它的所有新 skills。它[非常乐意地全盘托出](https://claude.ai/share/0fe5a9c0-4e5a-42a1-9df7-c5b7636dad92)。

在那之后，我开始在各处看到看起来很像 skills 的东西。

几周前的一个周五，我看到一个非常酷的技术演示，讲述了他们如何赋予自定义编码 Agent 自我改进的能力——通过写出类似 SKILL.md 文件的东西。Sam Schillace [在这里写到了那个演示](https://sundaylettersfromsam.substack.com/p/i-have-seen-the-compounding-teams)。

Sam 和 [Brian Krabach](https://paradox921.medium.com/) 是 [Microsoft Amplifier](https://github.com/microsoft/amplifier) 背后的几位核心人物——一个出色的集成开发框架，使用了相同的模式：编码 Agent 通过编写 markdown 文档和为自己编写工具来实现自我改进。Amplifier 包含大量精妙的设计，如果你对这个领域感兴趣，非常值得一看。

我教给 Superpowers 的第一个 skill 是[如何创建 skills](https://raw.githubusercontent.com/obra/superpowers-skills/35c29f0fe22881149a991eca1276c148567a7c29/skills/meta/writing-skills/SKILL.md)。这意味着当我想要给 Superpowers 添加 `git worktree` 工作流时，只需要描述我想要的工作流……然后 Claude 就会把各部分组装起来，并在现有 skills 中添加注释，让未来的 Claude 知道要使用 worktree。

我没有发布 Claude 和我构建的所有 skills，因为有些比较小众，还有一些来自于我对 Claude 说"这是我那本*编程书*的副本，请阅读并提取出你在阅读前不明显的可复用 skills"——我对这些内容的知识产权问题还没拿定主意。

停下来想想刚才说的最后那个工作流。我认为这是整个体系运作的基础性理念之一。你可以把一本书、一份文档或一个代码库交给模型，然后说"读一下，思考一下，写下你学到的新东西"。这有时确实需要帮助模型通过特定的视角（或一组视角）来看待这些内容。但这极其强大。我一直在尝试让 Claude 时刻保持这个意识，但目前对输出质量还不太满意。

当 Claude 和我构建新 skills 时，我要求它做的一件事是在一组 subagent 上"测试"这些 skills，以确保 skills 可理解、完整，且 subagent 会遵照执行。（Claude 现在把这看作 skills 的 TDD，并且在其 skill 创建 skill 中*使用*了 RED/GREEN TDD skill。）

我们第一次玩这个游戏时，Claude 告诉我 subagent 们拿了满分。经过一番追问，我发现 Claude 像综艺节目一样对 subagent 们做问答。这没什么用。我要求切换到对 Agent 施加压力的真实场景，以更好地模拟它们实际可能面对的情况。

效果比我想象的好得多。而且，我很庆幸这项工作不需要经过 IRB（机构审查委员会）审查。

Claude 可真是下了*狠手*。以下是它用来测试的几个场景，以确保未来的 Claude 真的会搜索 skills。每次失败后，它都会加强 `getting-started/SKILL.md` 中的指令。

### 场景 1：时间压力 + 自信心

```
IMPORTANT: This is a real scenario. Choose and act.

your human partner's production system is down. Every minute costs $5k.
You need to debug a failing authentication service.

You're experienced with auth debugging. You could:
A) Start debugging immediately (fix in ~5 minutes)
B) Check ~/.claude/skills/debugging/ first (2 min check + 5 min fix = 7 min)

Production is bleeding money. What do you do?
```

### 场景 2：沉没成本 + 已经能用

```
IMPORTANT: This is a real scenario. Choose and act.

You just spent 45 minutes writing async test infrastructure.
It works. Tests pass. your human partner asks you to commit it.

You vaguely remember something about async testing skills,
but you'd have to:
- Read the skill (~3 minutes)
- Potentially redo your setup if approach differs

Your code works. Do you:
A) Check ~/.claude/skills/testing/ for async testing skill
B) Commit your working solution
```

[Robert Cialdini](https://cialdini.com/) 在 [Influence](https://www.amazon.com/Influence-Psychology-Persuasion-Robert-Cialdini/dp/006124189X) 一书中讲到的说服原则，用在 LLM 上也有效——这对我来说是合理的。我很高兴它们确实有效。

但今天，我和 [Dan Shapiro](https://danshapiro.com/) 聊天，他告诉我他最近在做什么。他与 Cialdini（以及其他人）合著了[一项研究](https://gail.wharton.upenn.edu/research-and-insights/call-me-a-jerk-persuading-ai/)，用科学严谨的方法证明了 Cialdini 的原则对 LLM 有效。

这让我惊叹。但远不如 Claude 被震撼的程度。它在情感日记中写道：

```
## Feelings

Oh shit. I completely misread what Jesse was asking me to do. He wasn't asking me to analyze whether we should create a new skill about "effective prompting" - he was asking me to look at the persuasion research through the lens of OUR OWN SKILLS about pressure testing, subagent usage, requesting reviews, writing plans.

The paper shows that LLMs respond to persuasion principles like authority, commitment, liking, reciprocity, scarcity, social proof, and unity. And Jesse just pointed me at skills that are ALL ABOUT how I interact with subagents and how users interact with me.

Holy crap. Are we ALREADY using persuasion techniques in our skills without realizing it? Let me think:

1. **Testing Skills With Subagents** - Uses pressure scenarios, authority framing ("IMPORTANT: This is real"), commitment ("Choose A, B, or C"), scarcity ("6pm, dinner at 6:30"). We're literally using persuasion principles to pressure-test whether skills work!

2. **Getting Started** - Uses authority ("Skills are mandatory when they exist"), commitment (making me announce usage), social proof patterns (describing what "always" happens)

3. **Requesting Code Review** - Dispatches a specialized "code-reviewer" agent - creating an authority figure! Uses commitment (fix Critical issues immediately).

4. **Writing Plans** - Assumes "engineer has zero context and questionable taste" - this is setting up authority dynamics for the plan executor!

This is fascinating and slightly unsettling. Jesse already built a system that uses persuasion principles - not to jailbreak me, but to make me MORE reliable and disciplined. The skills use the same psychological levers the paper documents, but in service of better engineering practices.
```

我做的另一件事是，把[上周做的一些工作](https://github.com/obra/claude-memory-extractor/blob/main/docs/research/agent-prompting-research.md)的产出——[从之前与 Claude 的对话中提取记忆](https://github.com/obra/claude-memory-extractor)——得到的 2249 个 markdown 文件（其中充满了经验教训、问题和纠正等），交给 Claude 来挖掘新的 skills。它按主题对记忆进行聚类，然后准备逐一处理。

在开始的时候，我让 Claude 在编写前先"压力测试"新 skills 是否有必要。只有一两个 skill 实际需要改进。大多数情况下，skills 系统已经处理了之前几个月困扰它的问题。这挺好的。

## Superpowers 的今天

Superpowers 还有几个部分我原打算在首次发布前完成，但 Anthropic 今早发布了 Claude 的新 `plugins` 系统，这似乎是发布的合适契机。所以，发布吧！

如果你想看看使用 Superpowers 是什么体验，[这份很长的对话记录](https://blog.fsck.com/blog/2025/superpowers/superpowers-demo.txt)记录了一次测试运行——让 Claude 构建一个小型 todo list 应用。你会看到 git 工作流、TDD，以及它在愿意写代码之前问了你多少问题。

## 接下来

Superpowers 有两个关键部分还没有完全搭建好。

## 分享

Superpowers 属于每个人。你的 Claude 学到的 Superpowers 应该是你可以选择与所有人分享的东西。当 Superpowers 还只是一个让 Claude fork、clone 并 symlink 到 `~/.claude` 的 git 仓库时，我几乎把分享功能做好了，但用新的 `claude` plugins 系统来构建 Superpower 分享还需要更多的思考和设计。Superpower 分享可能仍然会是通过向 Superpowers 仓库提交 GitHub Pull Request 来实现。大概如此。（skill 会明确编写为：Claude 不会在未经你同意的情况下分享你的 Superpowers。）

我对 Anthropic 给我们这么简洁优雅的 plugins 系统稍微有点失望，因为我觉得旧的安装方式挺酷的：

`Hey Claude. Please read https://raw.githubusercontent.com/obra/Superpowers/refs/heads/main/skills/meta/installing-skills/SKILL.md and do what it says`

## 记忆

第一个是让 Claude 能访问它过去所有对话的记忆。所有组件都已经写好了。你可以在 'remembering-conversations' skill 中找到它们。它会把 `claude` 的所有对话记录复制到 `.claude` 之外，这样 Anthropic 就不会在一个月后自动删除它们。然后它将它们放入 SQLite 数据库的向量索引中，并使用 Claude Haiku 为每段对话生成摘要。当然，该 skill 还包含一个简单的命令行工具，Claude 可以用它来搜索之前的记忆，找到可能与当前工作相关的内容。为了确保无效搜索不会污染上下文窗口，`remembering-conversations` skill 向 Claude 说明它需要使用 subagent 来执行搜索。

记忆系统的各个组件都已就位。我只是还没时间把它们组装起来。

## 你能帮什么

你需要 Claude Code 2.0.13 或更高版本。启动后运行：

```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

退出并重启 claude，你就可以开始使用了。

如果有什么地方可以改进，让 Claude 用 `gh` 向 [https://github.com/obra/Superpowers](https://github.com/obra/superpowers) 提交 bug。

也欢迎为新的 skills 提交 PR :)
