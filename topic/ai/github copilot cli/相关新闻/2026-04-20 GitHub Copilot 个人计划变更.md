---
title: "GitHub Copilot 个人计划变更"
source: "https://github.blog/news-insights/company-news/changes-to-github-copilot-individual-plans/"
description: "我们做出这些变更以确保现有客户获得可靠、可预期的体验。"
author:
  - "Joe Binder"
---

今天我们对 GitHub Copilot 个人计划做出以下变更，以保护现有客户的体验：暂停新用户注册、收紧使用限制、调整模型可用性。我们理解这些变更会带来不便，希望清楚地说明原因和对你的影响。

Agentic 工作流从根本上改变了 Copilot 的计算需求。长时间运行的并行会话现在消耗的资源远超原始计划结构所设计的承载能力。随着 Copilot agentic 能力的快速扩展，agent 执行了更多工作，更多用户触及了为维护服务可靠性而设定的使用限制。如果不进一步采取措施，所有人的服务质量都会下降。

我们听到了你对使用限制和模型可用性的不满，我们需要在添加这些限制措施方面做得更好——以下是具体变更和原因。

1. **暂停 GitHub Copilot Pro、Pro+ 和 Student 计划的新用户注册。** 暂停注册使我们能更有效地服务现有客户。
2. **收紧个人计划的使用限制。** Pro+ 计划提供的限额是 Pro 的 5 倍以上。需要更高限额的 Pro 用户可以升级到 Pro+。使用限制现在会在 VS Code 和 Copilot CLI 中显示，方便你避免触及限制。
3. **Opus 模型不再在 Pro 计划中提供。** Opus 4.7 仍在 Pro+ 计划中可用。正如我们在 [changelog](https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/) 中公布的，Opus 4.5 和 Opus 4.6 将从 Pro+ 中移除。

> [!warning] 退款截止日期
> 如果你遇到了意外的限制，或者这些变更不适合你，可以在 **5 月 20 日** 前访问 [Billing settings](https://github.com/settings/billing/licensing) 取消 Pro 或 Pro+ 订阅并获得当前订阅剩余时间的退款。

## GitHub Copilot 的使用限制机制

GitHub Copilot 目前有两种使用限制：会话限制和每周（7 天）限制。两种限制取决于两个不同因素——token 消耗量和模型倍数。

会话限制主要用于确保在高峰使用期间服务不会过载。其设定使大多数用户不受影响。随着时间推移，这些限制将在可靠性和需求之间取得平衡。如果确实遇到了会话限制，必须等到使用窗口重置后才能继续使用 Copilot。

每周限制是对用户在一周内可消耗的 token 总量设定的上限。我们最近引入了每周限制，以应对并行化、长时间运行的请求，这类请求通常会持续较长时间并产生极高的成本。

各计划的每周限额设定使大多数用户不受影响。如果你触及了每周限制但仍有 premium requests 剩余，可以继续使用 Auto 模型选择的 Copilot。当每周周期重置时，模型选择将重新启用。如果你是 Pro 用户，可以升级到 Pro+ 来提高每周限额。Pro+ 的限额是 Pro 的 5 倍以上。

> [!info] 使用限制 ≠ Premium Requests
> 使用限制与 premium request 权益是分开的。Premium requests 决定你可以访问哪些模型以及可以发出多少请求。相比之下，使用限制是基于 token 的防护措施，限制你在给定时间窗口内可以消耗多少 token。你可能仍有 premium requests 剩余，但同时触及使用限制。

## 避免意外限制和提升透明度

从今天起，VS Code 和 Copilot CLI 都会在你接近限制时显示剩余用量。这些变更是为了帮助你避免意外触及限制。

![在 VS Code 中触及使用限制的截图。消息显示「你已使用超过 75% 的每周使用限额。你的限额将在 4 月 27 日晚上 8:00 重置。」](https://github.blog/wp-content/uploads/2026/04/Screenshot-2026-04-20-at-2.05.12-PM.png?w=1394)

VS Code 中的使用限制

![在 GitHub Copilot CLI 中触及使用限制的截图。消息显示「！你已使用超过 75% 的每周使用限额。你的限额将在 4 月 24 日下午 3 点重置。」](https://github.blog/wp-content/uploads/2026/04/image-20.png?w=2976)

Copilot CLI 中的使用限制

> [!tip] 接近限制时的应对措施
> - 在简单任务中使用**倍数较小的模型**。倍数越大，越快触及限制。
> - 如果你是 Pro 计划用户，考虑**升级到 Pro+**，可将限额提高 5 倍以上。
> - 使用 **plan mode**（[VS Code](https://code.visualstudio.com/docs/copilot/concepts/agents#_planning)、[Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices#2-plan-before-you-code)）来提高任务效率。Plan mode 也能提升任务成功率。
> - **减少并行工作流。** `/fleet` 等工具会导致更高的 token 消耗，如果接近限制应谨慎使用。

## 为什么这样做

我们看到所有用户的用量都在加剧，因为他们认识到了 agent 和 subagent 在解决复杂编码问题上的价值。这些长时间运行的并行工作流能产生很大价值，但也对我们的基础设施和定价结构构成了挑战：现在少数几个请求的成本超过计划价格已是常态！这是我们需要解决的问题。我们今天采取的措施使我们能够在开发更可持续的解决方案的同时，为现有用户提供最佳体验。
