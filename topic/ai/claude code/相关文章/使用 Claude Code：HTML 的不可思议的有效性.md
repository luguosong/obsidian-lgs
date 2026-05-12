---
title: "Claude Code 实践：HTML 的惊人效力"
source: "https://x.com/trq212/status/2052809885763747935"
description: "Markdown 已成为 Agent 与我们通信的主流文件格式，但随着 Agent 能力不断增强，HTML 正成为更具表达力的替代方案。"
author:
  - "@trq212"
published: 2026-05-09
tags:
  - claude-code
  - html
  - workflow
  - ai-tools
---
字数：2222
![图像](https://pbs.twimg.com/media/HHz_ftzaIAAwkQs?format=jpg&name=large)

Markdown 已成为 Agent 与我们通信的主流文件格式。它简洁、可移植、具备一定的富文本能力，也便于编辑。Claude 甚至已经能够令人惊讶地熟练使用 ASCII 在 Markdown 文件中绘制图表。

但随着 Agent 越来越强大，我开始觉得 Markdown 成了一种限制性的格式。一篇超过一百行的 Markdown 文件我很难读完，我想要更丰富的可视化效果、颜色和图表，并且希望能便于分享。

我越来越少亲自编辑这些文件，而是把它们当作规格说明、参考文件、头脑风暴输出等来使用。真正需要编辑时，我通常也是让 Claude 来做，这就抵消了 Markdown 最大的优势之一。

我已经开始倾向于使用 HTML 作为输出格式，而非 Markdown，而且越来越多地看到 Claude Code 团队的其他成员也在这样做，原因如下。

（如果想先看一些示例，可以在这里看到很多：[https://thariqs.github.io/html-effectiveness](https://thariqs.github.io/html-effectiveness/)，看完记得回来继续阅读）

# 为什么选 HTML？

## 信息密度

![图像](https://pbs.twimg.com/media/HHz_q48aAAAaCfW?format=jpg&name=large)

与 Markdown 相比，HTML 能传达丰富得多的信息。当然，它可以做简单的文档结构，比如标题和格式化，但它还能表示各种其他信息，例如：

- 用表格呈现表格数据
- 用 CSS 呈现设计数据
- 用 SVG 绘制插图
- 用 script 标签展示代码片段
- 用 HTML 元素结合 JavaScript + CSS 实现交互
- 用 SVG 和 HTML 展示工作流
- 用绝对定位和 canvas 呈现空间数据
- 用 image 标签嵌入图片

我甚至可以说，Claude 能够读取的==几乎任何一种信息，你都可以用 HTML 相当高效地表示出来==。这使它成为模型向你传达深度信息、供你审阅的一种高效方式。

我发现，当无法使用 HTML 时，模型可能会在 Markdown 中做一些效率较低的事，比如 ASCII 图表，或者我最喜欢的一个例子——用 Unicode 字符来估算颜色，就像下面这张 Claude Code 截图里显示的那样。

![图像](https://pbs.twimg.com/media/HH0CDc6a8AAy1bv?format=png&name=large)

Claude Code 尝试在 Markdown 中展示颜色

## 视觉清晰度与易读性

![图像](https://pbs.twimg.com/media/HH0AgqJbcAAaEcZ?format=jpg&name=large)

随着 Claude 能够完成越来越复杂的工作，它写的规格说明和计划也越来越长。实际使用中，我发现自己往往不会真正读完超过 100 行的 Markdown 文件，更别说让组织里的其他人去读了。

但 HTML 文档读起来要容易得多，Claude 可以通过标签页、插图、链接等视觉化方式来优化文档结构，便于导航。它甚至可以做到移动端自适应，让你根据设备形态以不同方式阅读。

## 便于分享

Markdown 文件分享起来相当麻烦，因为大多数浏览器无法原生渲染它。你通常需要作为附件通过邮件或消息发送。

而 HTML，只要上传文件（例如到 S3），就可以轻松分享链接。同事可以在任何地方打开，随时引用。

如果是 HTML 格式，你的规格说明、报告或 PR 描述被人实际阅读的概率会高得多。

## 双向交互

![图像](https://pbs.twimg.com/media/HH0Ao0tbYAAOF9e?format=jpg&name=large)

HTML 允许你与文档进行交互，例如，你可能想让它加入滑块或旋钮来调整设计，或者让你调整算法中的不同选项来观察效果。你还可以让它把这些改动复制成一个 prompt，粘贴回 Claude Code 中。关于双向交互的更多示例，可以阅读我关于 playgrounds 的帖子：[https://x.com/trq212/status/2017024445244924382](https://x.com/trq212/status/2017024445244924382)

**数据摄入**

为什么要用 Claude Code 而不是 ClaudeAI 或 Claude Design 来生成 HTML 文件？最重要的原因之一是 Claude Code 能摄入的上下文量。例如，在写这篇文章时，我让 Claude Code 读取我的代码文件夹，找出所有生成过的 HTML 文件，将它们分组分类，然后制作一个包含各类型示例图表的 HTML 文件。你在这篇文章中看到的图表，就是这样生成的。

除了文件系统，Claude Code 还可以通过 MCP（如 Slack、Linear 等）、网络浏览器（Chrome 中的 Claude）、git 历史等来获取额外上下文。

## 充满乐趣

用 Claude 制作 HTML 文档更有趣，让我感觉更有参与感、更投入，这本身就足够了。

## 如何开始

我有点担心大家读完这篇文章后会把它做成一个 `/html` skill 或什么类似的东西。虽然这样做可能有一定价值，但我想强调的是，你不需要做太多就能让 Claude 这样做。

> [!tip] 直接开口就行
> 你可以直接让它"生成一个 HTML 文件"或"生成一个 HTML artifact"。关键在于知道你想让这个 artifact 做什么、以及如何使用它。随着时间推移你可能会制作一个 skill，但现在我建议从头开始 prompt，先摸索一下在不同场景下如何使用它。

# 使用场景

为了让这些更具体，我为不同使用场景制作了很多 HTML 文件。你可以在这里查看全部：[https://thariqs.github.io/html-effectiveness/](https://thariqs.github.io/html-effectiveness/)，以下是概述。

## 规格说明、规划与探索

HTML 是 Claude 深入分析问题的丰富画布。当我开始处理一个问题时，我不会做一个简单的 Markdown 计划，而是期望生成一系列 HTML 文件。例如，我可能先让 Claude Code 进行头脑风暴，探索不同方案；然后让它深入其中一个，也许制作 mockup 或代码片段；最后，当我感觉差不多了，再让它写一份实施计划。计划满意后，我会开启新会话，把这些文件全部传入来进行实施。

验证阶段，我也会让验证 agent 读取这些文件，它能获得更广泛的需求上下文。

![图像](https://pbs.twimg.com/media/HH0BFWLbMAEk_7T?format=jpg&name=large)

**示例 prompt：**

- 我不确定新手引导页面该走哪个方向。生成 6 种截然不同的方案——在布局、风格和信息密度上各有差异——并将它们并排展示在一个 HTML 文件的网格中供我对比。每种方案标注其取舍权衡。
- 用 HTML 文件创建一份详尽的实施计划，确保包含一些 mockup、展示数据流、并附上我可能需要审阅的关键代码片段。让它易于阅读和消化。

**使用场景：**

- 探索代码的不同实现方式
- 探索多种视觉设计方案

## 代码审查与理解

代码在 Markdown 文件中很难阅读。但用 HTML，我们可以渲染 diff、注解、流程图、模块图等。可以用它来理解 agent 写的代码、进行代码审查，或者向审查者解释某个 PR。我发现这通常比 GitHub 默认的 diff 视图效果更好，现在每个 PR 我都会附上一个 HTML 代码说明文档。

![图像](https://pbs.twimg.com/media/HH0BRSQbMAAuuof?format=png&name=large)

**示例 prompt：**

帮我审查这个 PR，制作一个描述它的 HTML artifact。我对其中的 streaming/backpressure 逻辑不太熟悉，重点讲这部分。渲染实际的 diff 并附上行内旁注，按严重程度用颜色标记发现的问题，以及其他任何有助于传达概念的内容。

**使用场景：**

- 创建 PR
- 审查 PR
- 理解某段代码的主题

## 设计与原型

Claude Design 基于 HTML，因为 HTML 在设计表达方面极为强大，即使你的最终界面不是 HTML。Claude 可以用 HTML 绘制设计草图，然后用你选择的语言来实现，无论是 React、Swift 还是其他。

你也可以原型化交互效果，比如动画、操作等。可以让 Claude 添加滑块、旋钮等，精确调出你想要的效果。

![图像](https://pbs.twimg.com/media/HH0BXqjboAAHGsw?format=jpg&name=large)

**示例 prompt：**

我想为一个新的结账按钮做原型，点击时先播放动画然后快速变为紫色。创建一个 HTML 文件，提供若干滑块和选项供我尝试不同的动画参数，并给我一个复制按钮来复制效果好的参数。

**适用于：**

- 创建设计系统 artifact
- 调整组件
- 可视化组件库
- 原型化愉悦的动画效果

## 报告、研究与学习

Claude Code 非常擅长综合多个数据源的信息并将其转化为易读的报告。你可以让 Claude 搜索你的 Slack、代码库、git 历史、互联网等，为你自己、领导层或团队生成极其可读的报告。

你可以将其组织为一份长篇 HTML 文档、一个交互式解释页面，甚至一个幻灯片/演示文稿。让 Claude 用 SVG 绘制图表来帮助可视化。例如，在写关于 prompt caching 的文章时，我让 Claude 读取 git 历史，为我准备了一份深度研究 HTML 文件，内容涵盖我们对 prompt caching 的所有改动。

![图像](https://pbs.twimg.com/media/HH0Bp86bUAAJDyZ?format=jpg&name=large)

**示例 prompt：** 我不了解我们的限流器实际是怎么工作的。读取相关代码，生成一个单页 HTML 解释页面：一个 token-bucket 流程图、3-4 个带注解的关键代码片段，以及底部的"注意事项"部分。为只读一遍的人优化。

**适用于：**

- 总结某个功能的工作原理
- 向我解释一个概念
- 每周向老板汇报的状态报告
- 向领导层提交的事故报告
- SVG 插图、流程图、技术图表等

# 自定义编辑界面

有时候，仅凭文字框很难描述你想要的东西。这种情况下，我会让 Claude 为我正在处理的具体事物构建一个一次性编辑器。不是产品，不是可复用工具，而是一个单一 HTML 文件，专门为这一份数据量身打造。

关键始终在于最后要有一个导出功能：一个"复制为 JSON"或"复制为 prompt"的按钮，把我在 UI 里做的操作转化回可以粘贴到 Claude Code 中的内容。

> [!important] 导出是关键
> ==自定义编辑界面的核心：始终以导出结尾。== 无论是"复制为 JSON"还是"复制为 prompt"按钮，都要确保 UI 操作能转化回可粘贴到 Claude Code 的内容。

![图像](https://pbs.twimg.com/media/HH0FbKebUAAsRPr?format=jpg&name=large)

**示例 prompt：**

- 我需要重新排列这 30 个 Linear 工单的优先级。给我做一个 HTML 文件，将每个工单做成可拖拽的卡片，分布在"现在 / 下一步 / 以后 / 砍掉"四列中。按你的最佳判断预排序。添加一个"复制为 Markdown"按钮，导出最终排序，并在每个分区附一行理由说明。
- 这是我们的功能开关配置。为它构建一个基于表单的编辑器，按区域对开关分组，显示它们之间的依赖关系，当我启用一个前置条件未满足的开关时给我警告。添加一个"复制 diff"按钮，只给我改动的键。
- 我在调这个系统 prompt。做一个左右分栏编辑器：左边是可编辑的 prompt，变量槽高亮显示；右边是三个示例输入，实时渲染填充后的模板。添加字符/token 计数器和复制按钮。

**适用于：**

- 对任何事物进行重排序、分类或分桶（工单、测试用例、反馈）
- 编辑结构化配置（功能开关、环境变量、带约束的 JSON/YAML）
- 带实时预览地调整 prompt、模板或文案
- 整理数据集，审批/拒绝行，标注示例，导出选择结果
- 对文档、记录稿或 diff 进行标注并导出注解
- 选择难以用文字表达的值：颜色、缓动曲线、裁剪区域、cron 表达式、正则表达式

## 常见问题

我向很多人介绍过我切换到 HTML 的事情，也遇到了一些反复被问到的问题。

> [!faq]- 这样不会更消耗 token 吗？
> 虽然 Markdown 通常使用更少的 token，但我发现 HTML 更强的表达力和我更高的实际阅读意愿，综合下来能带来更好的输出。在 Opus 4.7 的百万上下文窗口下，token 用量的增加在上下文窗口里几乎感觉不到。

> [!faq]- 你现在什么时候还会用 Markdown？
> 老实说，几乎所有事情我都已经停止使用 Markdown 了，不过我可能已经处于 HTML 最大化主义者那一端了。

> [!faq]- 怎么查看 HTML 文件？
> 我通常直接在本地浏览器中打开（可以让 Claude 打开），或者上传到 S3 获取可分享的链接。

> [!faq]- 生成 HTML 不是比 Markdown 更慢吗？
> 确实更慢！HTML 可能比 Markdown 慢 2-4 倍，但我觉得结果值得。

> [!faq]- 那版本控制怎么办？
> 这确实是 HTML 最大的缺点之一，HTML diff 嘈杂，比 Markdown 难审查。

> [!faq]- 如何让 Claude 符合我的审美/不做出丑陋的东西？
> 前端设计插件能帮助 Claude 制作出好看的 HTML 文件。但要匹配你们公司的风格，可以让 Claude 扫描你的代码库，生成一个单一的设计系统 HTML 文件。然后用这个设计系统文件作为其他 HTML 文件的参考。

## 保持参与感

以上所有内容都是想说，我使用 HTML 的真正原因是，我感觉与 Claude 更紧密地连接在一起。我曾经开始担心，因为我已经不再深入阅读计划，我将不得不把所有决定都留给 Claude 来做。

但我很高兴地说，使用 HTML 后，我比以往任何时候都更有参与感。希望你也有同样的体验。