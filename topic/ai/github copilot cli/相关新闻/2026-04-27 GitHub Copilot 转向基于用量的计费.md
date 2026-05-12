---
title: "GitHub Copilot 转向基于用量的计费"
source: "https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/"
description: "从 6 月 1 日起，你的 Copilot 使用量将消耗 GitHub AI Credits。"
author:
  - "Mario Rodriguez"
---

> [!abstract] 摘要
> 今天我们宣布，所有 GitHub [[Copilot]] 计划将于 **2026 年 6 月 1 日** 转向基于用量的计费方式。

今后不再计算 premium request 数量，每个 [[Copilot]] 计划都将包含每月的 **GitHub AI Credits** 额度，付费计划可额外购买用量。用量将基于 token 消耗计算，包括输入、输出和缓存 token，按各模型的公开 API 费率计费。

此次变更使 [[Copilot]] 定价与实际用量对齐，是构建可持续、可靠的 [[Copilot]] 业务和用户体验的重要一步。

为帮助客户做好准备，我们还将在 5 月初推出**预览账单**功能，让用户和管理员在 6 月 1 日过渡前了解预估费用。用户登录 github.com 后可在 Billing Overview 页面查看。

## 变更原因

[[Copilot]] 已不再是一年前的产品。

它已从编辑器内的助手演进为一个 agentic 平台，能够运行长时间、多步骤的编码会话，使用最新模型，并在整个仓库中迭代。Agentic 使用正在成为默认模式，带来了显著更高的计算和推理需求。

如今，一个简短的聊天提问和一次长达数小时的自主编码会话对用户来说花费相同。GitHub 承担了用量背后不断攀升的推理成本，但当前的 premium request 模型已不可持续。

基于用量的计费解决了这个问题。它使定价与实际用量更好地对齐，帮助我们维持长期的服务可靠性，并减少对重度用户的限制。

## 具体变更

从 **6 月 1 日** 起，premium request 单位 (PRU) 将被 **GitHub AI Credits** 取代。

Credits 将基于 token 用量消耗，包括输入、输出和缓存 token，按各模型的公开 API 费率计算。

几个重要细节：

- **基础计划价格不变。** [[Copilot]] Pro 仍为 $10/月，Pro+ 仍为 $39/月，Business 仍为 $19/用户/月，Enterprise 仍为 $39/用户/月。
- **代码补全和 Next Edit 建议仍包含在所有计划中**，不消耗 AI Credits。
- **不再提供降级体验。** 当前，耗尽 PRU 的用户可能会降级到较低成本模型继续工作。新模式下，用量将由可用 credits 和管理员预算控制来管理。
- **[[Copilot]] 代码审查除了消耗 GitHub AI Credits 外，还将消耗 [[GitHub Actions]] 分钟数。** 这些分钟数按与其他 [[GitHub Actions]] 工作流相同的每分钟费率计费。

上周，我们还对 [[Copilot]] 个人计划（包括 Free、Pro、Pro+ 和 Student）[推出了临时变更](https://github.blog/news-insights/company-news/changes-to-github-copilot-individual-plans/)，并暂停了自助购买 [[Copilot]] Business 计划。这些是出于可靠性和性能方面的措施，为更广泛地向基于用量的计费过渡做准备。基于用量的计费生效后，我们将放宽使用限制。

## 对个人用户的影响

[[Copilot]] Pro 和 Pro+ 月度订阅将包含与当前订阅价格对应的每月 AI Credits：

- **[[Copilot]] Pro：** $10/月，包含 $10 的每月 AI Credits
- **[[Copilot]] Pro+：** $39/月，包含 $39 的每月 AI Credits

月度 Pro 或 Pro+ 计划的用户将在 2026 年 6 月 1 日自动迁移到基于用量的计费。

年度 Pro 或 Pro+ 计划的用户将继续使用现有计划，采用基于 premium request 的定价，直到计划到期。[年度计划订阅者的模型倍数将在 6 月 1 日增加（见表格）](https://docs.github.com/copilot/reference/copilot-billing/models-and-pricing#model-multipliers-for-annual-copilot-pro-and-copilot-pro-subscribers)。到期后，他们将过渡到 [[Copilot]] Free，可选择升级到付费月度计划。或者，他们可以在年度计划到期前转换为付费月度计划，我们将按比例返还年度计划剩余价值的 credits。

## 对企业和商业用户的影响

[[Copilot]] Business 和 [[Copilot]] Enterprise 的月度席位价格保持不变：

- **[[Copilot]] Business：** $19/用户/月，包含 $19 的每月 AI Credits
- **[[Copilot]] Enterprise：** $39/用户/月，包含 $39 的每月 AI Credits

为支持过渡，现有 [[Copilot]] Business 和 [[Copilot]] Enterprise 客户将在 6 月、7 月和 8 月自动获得促销赠送额度：

- **[[Copilot]] Business：** $30 的每月 AI Credits
- **[[Copilot]] Enterprise：** $70 的每月 AI Credits

我们还推出了跨企业的共享额度池，有助于消除闲置容量。每个用户未使用的额度不再孤立，credits 可以在整个组织内共享。

管理员还将获得新的预算控制功能，可以在企业、成本中心和用户级别设置预算。当共享额度池耗尽时，组织可以选择是否允许按公开费率继续使用或限制支出。

## 总结

计划价格不变。你将完全掌控自己的支出，拥有追踪用量的工具，并可以在需要时选择购买更多 AI Credits。

## 相关笔记

- [["GitHub Copilot 个人计划变更"]]
- [[Claude Code]]
- [[社区市场 awesome-copilot]]
- [[自动化与脚本集成]]
- [[更新日志]]
- [[Agent 系统]]
- [[官方市场 copilot-plugins]]
- [[Copilot CLI+Claude Code双工具协同实践]]
