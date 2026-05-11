---
title: "gstack：Garry Tan 的 Claude Code 工作流"
source: "https://github.com/garrytan/gstack"
description: "Garry Tan 的 Claude Code 完整配置：23 个专业化工具，覆盖 CEO、设计师、工程经理、发布工程师、文档工程师和 QA 等角色"
author:
tags:
  - ai
  - 扩展

---
字数：5506
## gstack

> "我大概从去年 12 月起就没手动写过一行代码了，这是一个极其巨大的变化。" — [Andrej Karpathy](https://fortune.com/2026/03/21/andrej-karpathy-openai-cofounder-ai-agents-coding-state-of-psychosis-openclaw/)，No Priors 播客，2026 年 3 月

听到 Karpathy 这句话时，我想搞清楚他是怎么做到的。一个人怎么能像二十人的团队一样交付产品？Peter Steinberger 用 AI Agent 几乎独立构建了 [OpenClaw](https://github.com/openclaw/openclaw)——获得了 24.7 万 GitHub Star。变革已经到来。一个拥有正确工具链的独立开发者，可以比传统团队跑得更快。

我是 [Garry Tan](https://x.com/garrytan)，[Y Combinator](https://www.ycombinator.com/) 的 President & CEO。我与数千家初创公司合作过——Coinbase、Instacart、Rippling——都是在它们还只有一两个人的时候。在加入 YC 之前，我是 Palantir 最早的工程师/PM/设计师之一，联合创办了 Posterous（后被 Twitter 收购），并构建了 YC 内部社交网络 Bookface。

**gstack 就是我的答案。** 我构建产品已经 20 年了，而现在的交付速度前所未有。在过去 60 天里：3 个生产环境服务、40+ 个已交付功能——全都是兼职做的，同时还在全职运营 YC。按逻辑代码变更（而非原始 LOC——AI 会膨胀这个数字）计算，我 2026 年的节奏是 **2013 年的约 810 倍**（日均 11,417 对比 14 行逻辑代码）。年初至今（截至 4 月 18 日），2026 年的产出已经达到 **2013 年全年的 240 倍**。统计范围覆盖 40 个公共和私有 `garrytan/*` 仓库（包括 Bookface），已排除一个 demo 仓库。大部分代码由 AI 编写。关键不在于谁敲的键盘，而在于交付了什么。

> 用原始代码行数批评 AI 膨胀产出的人没有错。但他们认为去除通胀因素后我的生产力反而更低，这就不对了。我的生产力大幅提升了。完整的方法论、注意事项和复现脚本：**[关于 LOC 争议](https://github.com/garrytan/gstack/blob/main/docs/ON_THE_LOC_CONTROVERSY.md)**。

**2026 年 — 1,237 次贡献，还在增长：**

[![GitHub 2026 年贡献 — 1,237 次贡献，1-3 月急剧增长](https://github.com/garrytan/gstack/raw/main/docs/images/github-2026.png)](https://github.com/garrytan/gstack/blob/main/docs/images/github-2026.png)

**2013 年 — 在 YC 构建 Bookface 时（772 次贡献）：**

[![GitHub 2013 年贡献 — 在 YC 构建 Bookface 时的 772 次贡献](https://github.com/garrytan/gstack/raw/main/docs/images/github-2013.png)](https://github.com/garrytan/gstack/blob/main/docs/images/github-2013.png)

同一个人。不同的时代。区别在于工具链。

**gstack 就是我的方法。** 它把 Claude Code 变成一个虚拟工程团队——一位重新思考产品的 CEO、一位锁定架构的工程经理、一位捕捉 AI 糟糕产出的设计师、一位发现生产 Bug 的 Reviewer、一位打开真实浏览器的 QA Lead、一位运行 OWASP + STRIDE 审计的安全官，以及一位负责发布 PR 的 Release Engineer。23 个专家角色和 8 个强力工具，全部是斜杠命令，全部 Markdown 驱动，全部免费，MIT 许可证。

这是我的开源软件工厂。我每天都在用它。我把它分享出来，因为这些工具应该人人可用。

Fork 它。改进它。让它成为你自己的。如果你想吐槽免费的开源软件——悉听尊便，但我更建议你先试试。

**适合以下人群：**

- **创始人和 CEO** — 尤其是仍然想亲自写代码交付的技术型创始人
- **Claude Code 新手** — 用结构化的角色替代空白提示
- **Tech Lead 和 Staff Engineer** — 每个 PR 都有严格的 Review、QA 和发布自动化

## 快速开始

1. 安装 gstack（30 秒 — 见下方）
2. 运行 `/office-hours` — 描述你在构建什么
3. 对任何功能想法运行 `/plan-ceo-review`
4. 对任何有改动的分支运行 `/review`
5. 在你的 staging URL 上运行 `/qa`
6. 到此为止。你会知道这是否适合你。

## 安装 — 30 秒

**前提条件：** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) ， [Git](https://git-scm.com/) ， [Bun](https://bun.sh/) v1.0+，[Node.js](https://nodejs.org/)（仅 Windows）

### Step 1: 在你的机器上安装

打开 Claude Code 并粘贴以下内容。Claude 会完成剩余操作。

> Install gstack: 运行 **`git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`**，然后在 CLAUDE.md 中添加一个 "gstack" 部分，说明对所有 Web 浏览使用 gstack 的 /browse skill，永远不要使用 mcp\_\_claude-in-chrome\_\_\* 工具，并列出可用的 skill：/office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /connect-chrome, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /setup-gbrain, /retro, /investigate, /document-release, /codex, /cso, /autoplan, /plan-devex-review, /devex-review, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn。然后询问用户是否还想将 gstack 添加到当前项目，让团队成员也能使用。

在你的仓库内粘贴以下内容。切换到团队模式，引导仓库让团队成员自动获得 gstack，并提交更改：

```
(cd ~/.claude/skills/gstack && ./setup --team) && ~/.claude/skills/gstack/bin/gstack-team-init required && git add .claude/ CLAUDE.md && git commit -m "require gstack for AI-assisted work"
```

不会在你的仓库中放入任何 vendored 文件，没有版本漂移，无需手动升级。每次 Claude Code 会话启动时都会执行快速自动更新检查（限流为每小时一次，网络故障安全，完全静默）。

将 `required` 替换为 `optional`，如果你想引导而非强制团队成员使用。

### OpenClaw

OpenClaw 通过 ACP 生成 Claude Code 会话，因此只要 Claude Code 安装了 gstack，所有 gstack skill 都能直接工作。将以下内容粘贴到你的 OpenClaw Agent：

> Install gstack: 运行 `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup` 来为 Claude Code 安装 gstack。然后在 AGENTS.md 中添加一个 "Coding Tasks" 部分，说明：当为编码工作生成 Claude Code 会话时，告诉会话使用 gstack skill。包括这些示例 — 安全审计："Load gstack. Run /cso"，代码审查："Load gstack. Run /review"，QA 测试 URL："Load gstack. Run /qa https://..."，端到端构建功能："Load gstack. Run /autoplan, implement the plan, then run /ship"，构建前规划："Load gstack. Run /office-hours then /autoplan. Save the plan, don't implement."

**设置完成后，直接自然地与你的 OpenClaw Agent 对话：**

| 你说的 | 会发生什么 |
| --- | --- |
| "修复 README 中的拼写错误" | 简单 — Claude Code 会话，不需要 gstack |
| "对这个仓库运行安全审计" | 生成 Claude Code 并运行 `/cso` |
| "帮我构建一个通知功能" | 生成 Claude Code 并运行 /autoplan → 实现 → /ship |
| "帮我规划 v2 API 重设计" | 生成 Claude Code 并运行 /office-hours → /autoplan，保存计划 |

高级调度路由和 gstack-lite/gstack-full 提示模板见 [docs/OPENCLAW.md](https://github.com/garrytan/gstack/blob/main/docs/OPENCLAW.md)。

### 原生 OpenClaw Skill（通过 ClawHub）

四个方法论文档 skill，直接在你的 OpenClaw Agent 中工作，无需 Claude Code 会话。从 ClawHub 安装：

```
clawhub install gstack-openclaw-office-hours gstack-openclaw-ceo-review gstack-openclaw-investigate gstack-openclaw-retro
```

| Skill | 功能 |
| --- | --- |
| `gstack-openclaw-office-hours` | 6 个追问式产品审视问题 |
| `gstack-openclaw-ceo-review` | 4 种范围模式的战略挑战 |
| `gstack-openclaw-investigate` | 根因调试方法论 |
| `gstack-openclaw-retro` | 每周工程回顾 |

这些是对话式 skill。你的 OpenClaw Agent 直接通过聊天运行它们。

### 其他 AI Agent

gstack 支持 10 种 AI 编码 Agent，不仅限于 Claude。安装脚本会自动检测你已安装的 Agent：

```
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/gstack
cd ~/gstack && ./setup
```

或使用 `./setup --host <name>` 指定特定 Agent：

| Agent | 标志 | Skill 安装到 |
| --- | --- | --- |
| OpenAI Codex CLI | `--host codex` | `~/.codex/skills/gstack-*/` |
| OpenCode | `--host opencode` | `~/.config/opencode/skills/gstack-*/` |
| Cursor | `--host cursor` | `~/.cursor/skills/gstack-*/` |
| Factory Droid | `--host factory` | `~/.factory/skills/gstack-*/` |
| Slate | `--host slate` | `~/.slate/skills/gstack-*/` |
| Kiro | `--host kiro` | `~/.kiro/skills/gstack-*/` |
| Hermes | `--host hermes` | `~/.hermes/skills/gstack-*/` |
| GBrain (mod) | `--host gbrain` | `~/.gbrain/skills/gstack-*/` |

**想添加对其他 Agent 的支持？** 参见 [docs/ADDING\_A\_HOST.md](https://github.com/garrytan/gstack/blob/main/docs/ADDING_A_HOST.md)。只需一个 TypeScript 配置文件，零代码改动。

## 实际效果

```
You:    I want to build a daily briefing app for my calendar.
You:    /office-hours
Claude: [asks about the pain — specific examples, not hypotheticals]

You:    Multiple Google calendars, events with stale info, wrong locations.
        Prep takes forever and the results aren't good enough...

Claude: I'm going to push back on the framing. You said "daily briefing
        app." But what you actually described is a personal chief of
        staff AI.
        [extracts 5 capabilities you didn't realize you were describing]
        [challenges 4 premises — you agree, disagree, or adjust]
        [generates 3 implementation approaches with effort estimates]
        RECOMMENDATION: Ship the narrowest wedge tomorrow, learn from
        real usage. The full vision is a 3-month project — start with
        the daily briefing that actually works.
        [writes design doc → feeds into downstream skills automatically]

You:    /plan-ceo-review
        [reads the design doc, challenges scope, runs 10-section review]

You:    /plan-eng-review
        [ASCII diagrams for data flow, state machines, error paths]
        [test matrix, failure modes, security concerns]

You:    Approve plan. Exit plan mode.
        [writes 2,400 lines across 11 files. ~8 minutes.]

You:    /review
        [AUTO-FIXED] 2 issues. [ASK] Race condition → you approve fix.

You:    /qa https://staging.myapp.com
        [opens real browser, clicks through flows, finds and fixes a bug]

You:    /ship
        Tests: 42 → 51 (+9 new). PR: github.com/you/app/pull/42
```

你说的是"每日简报 App"，Agent 说的是"你在构建一个首席幕僚 AI"——因为它倾听的是你的痛点，而非你的功能需求。八个命令，端到端。那不是一个 Copilot，那是一个团队。

## Sprint 流程

gstack 是一个流程，而非工具集合。Skill 按照 Sprint 的顺序运行：

**Think → Plan → Build → Review → Test → Ship → Reflect**

每个 Skill 的输出都是下一个 Skill 的输入。`/office-hours` 生成设计文档，`/plan-ceo-review` 读取它。`/plan-eng-review` 编写测试计划，`/qa` 使用它。`/review` 发现的 Bug，`/ship` 会验证是否修复。没有遗漏，因为每一步都知道上一步做了什么。

| Skill                    | 你的专家                | 职责                                                                                                                                                                            |
| ------------------------ | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/office-hours`          | **YC Office Hours** | 从这里开始。六个追问式问题，在你写代码之前重新审视产品。反驳你的框架，挑战前提，生成实现方案。设计文档会自动传递给下游所有 Skill。                                                                                                          |
| `/plan-ceo-review`       | **CEO / 创始人**       | 重新思考问题。找到隐藏在需求中的 10 星产品。四种模式：扩展、选择性扩展、保持范围、缩减。                                                                                                                                |
| `/plan-eng-review`       | **工程经理**            | 锁定架构、数据流、图表、边界情况和测试。把隐藏假设暴露出来。                                                                                                                                                |
| `/plan-design-review`    | **高级设计师**           | 对每个设计维度打 0-10 分，解释 10 分长什么样，然后编辑计划达到目标。AI 糟糕产出检测。交互式 — 每个设计选择一个 AskUserQuestion。                                                                                              |
| `/plan-devex-review`     | **开发者体验 Lead**      | 交互式 DX 审查：探索开发者画像，对比竞品 TTHW，设计你的"魔法时刻"，逐步追踪摩擦点。三种模式：DX EXPANSION、DX POLISH、DX TRIAGE。20-45 个追问。                                                                               |
| `/design-consultation`   | **设计合伙人**           | 从零构建完整的设计系统。研究行业现状，提出有创意的风险方案，生成逼真的产品 Mockup。                                                                                                                                 |
| `/review`                | **Staff Engineer**  | 发现能通过 CI 但在生产环境会爆炸的 Bug。自动修复明显的问题。标记完整性缺口。                                                                                                                                    |
| `/investigate`           | **调试器**             | 系统化根因调试。铁律：没有调查就没有修复。追踪数据流，测试假设，3 次修复失败后停止。                                                                                                                                   |
| `/design-review`         | **会写代码的设计师**        | 与 /plan-design-review 相同的审计，然后修复发现的问题。原子提交，前后截图对比。                                                                                                                            |
| `/devex-review`          | **DX 测试员**          | 实时开发者体验审计。实际测试你的上手流程：浏览文档，尝试 Getting Started，计时 TTHW，截图错误。与 `/plan-devex-review` 的评分对比——回旋镖式检验计划是否匹配现实。                                                                       |
| `/design-shotgun`        | **设计探索者**           | "给我看选项。" 生成 4-6 个 AI Mockup 变体，在浏览器中打开对比面板，收集你的反馈并迭代。品味记忆学习你喜欢什么。重复直到你满意，然后交给 `/design-html`。                                                                                 |
| `/design-html`           | **设计工程师**           | 把 Mockup 变成真正可用的生产级 HTML。Pretext 计算布局：文本自动换行，高度随内容调整，布局动态响应。30KB，零依赖。自动检测 React/Svelte/Vue。根据设计类型（Landing Page vs Dashboard vs Form）智能选择 API 路由。输出可以直接发布，不是 demo。             |
| `/qa`                    | **QA Lead**         | 测试你的 App，发现 Bug，用原子提交修复，再验证。为每个修复自动生成回归测试。                                                                                                                                    |
| `/qa-only`               | **QA 报告员**          | 与 /qa 相同的方法论，但仅报告。纯 Bug 报告，不修改代码。                                                                                                                                             |
| `/pair-agent`            | **多 Agent 协调器**     | 与任何 AI Agent 共享浏览器。一条命令，一次粘贴，连接完成。支持 OpenClaw、Hermes、Codex、Cursor 或任何能 curl 的工具。每个 Agent 有自己的标签页。自动以 headed 模式启动，你可以观看一切。自动启动 ngrok 隧道供远程 Agent 使用。范围化 Token、标签页隔离、速率限制、活动归属。 |
| `/cso`                   | **首席安全官**           | OWASP Top 10 + STRIDE 威胁模型。零噪音：17 项误报排除、8/10+ 置信度门槛、独立发现验证。每个发现都包含具体的攻击场景。                                                                                                    |
| `/ship`                  | **发布工程师**           | 同步 main 分支、运行测试、审计覆盖率、推送、创建 PR。如果你没有测试框架，它会自动引导一个。                                                                                                                            |
| `/land-and-deploy`       | **发布工程师**           | 合并 PR，等待 CI 和部署完成，验证生产环境健康状态。从"已批准"到"已在生产环境验证"只需一条命令。                                                                                                                         |
| `/canary`                | **SRE**             | 部署后监控循环。监控控制台错误、性能回退和页面故障。                                                                                                                                                    |
| `/benchmark`             | **性能工程师**           | 基准页面加载时间、Core Web Vitals 和资源大小。每个 PR 的前后对比。                                                                                                                                   |
| `/document-release`      | **技术文档工程师**         | 更新所有项目文档以匹配你刚发布的内容。自动发现过时的 README。                                                                                                                                            |
| `/retro`                 | **工程经理**            | 团队感知的每周回顾。按人分解、交付连续性、测试健康趋势、成长机会。`/retro global` 跨所有项目和 AI 工具运行（Claude Code、Codex、Gemini）。                                                                                    |
| `/browse`                | **QA 工程师**          | 给 Agent 一双眼睛。真实的 Chromium 浏览器，真实的点击，真实的截图。每个命令约 100ms。`/open-gstack-browser` 启动 GStack Browser，带侧边栏、反爬虫隐身和自动模型路由。                                                             |
| `/setup-browser-cookies` | **会话管理器**           | 从你的真实浏览器（Chrome、Arc、Brave、Edge）导入 Cookie 到无头浏览器会话中。测试需要登录的页面。                                                                                                                 |
| `/autoplan`              | **Review Pipeline** | 一条命令，完整审查的计划。自动运行 CEO → 设计 → 工程审查，内嵌决策原则。只把品味决策呈交给你审批。                                                                                                                        |
| `/learn`                 | **记忆**              | 管理 gstack 在跨会话中学到的内容。审查、搜索、精简和导出项目特定的模式、陷阱和偏好。学习成果跨会话积累，让 gstack 在你的代码库上越来越聪明。                                                                                                |

### 我应该用哪个 Review？

| 构建目标 | 计划阶段（编码前） | 线上审计（发布后） |
| --- | --- | --- |
| **终端用户**（UI、Web App、移动端） | `/plan-design-review` | `/design-review` |
| **开发者**（API、CLI、SDK、文档） | `/plan-devex-review` | `/devex-review` |
| **架构**（数据流、性能、测试） | `/plan-eng-review` | `/review` |
| **以上全部** | `/autoplan`（运行 CEO → 设计 → 工程 → DX，自动检测适用哪些） | — |

### 强力工具

| Skill | 功能 |
| --- | --- |
| `/codex` | **第二意见** — 来自 OpenAI Codex CLI 的独立代码审查。三种模式：审查（通过/失败门槛）、对抗性挑战和开放咨询。当 `/review` 和 `/codex` 都运行过时，提供跨模型分析。 |
| `/careful` | **安全护栏** — 在破坏性命令前发出警告（rm -rf、DROP TABLE、force-push）。说"be careful"即可激活。可覆盖任何警告。 |
| `/freeze` | **编辑锁定** — 限制文件编辑到一个目录。调试时防止意外修改范围外的代码。 |
| `/guard` | **完整安全** — `/careful` + `/freeze` 合为一条命令。生产环境工作的最大安全保障。 |
| `/unfreeze` | **解锁** — 移除 `/freeze` 边界。 |
| `/open-gstack-browser` | **GStack Browser** — 启动带侧边栏、反爬虫隐身、自动模型路由（Sonnet 用于操作，Opus 用于分析）的 GStack Browser，一键导入 Cookie，集成 Claude Code。清理页面、智能截图、编辑 CSS、将信息传回终端。 |
| `/setup-deploy` | **部署配置器** — `/land-and-deploy` 的一次性设置。自动检测你的平台、生产环境 URL 和部署命令。 |
| `/setup-gbrain` | **GBrain 引导** — 从零到运行 gbrain 不超过 5 分钟。PGLite 本地、Supabase 现有 URL 或通过 Management API 自动配置新 Supabase 项目。MCP 注册 Claude Code + 每个仓库的信任三级分类（读写/只读/拒绝）。[完整指南](https://github.com/garrytan/gstack/blob/main/USING_GBRAIN_WITH_GSTACK.md)。 |
| `/sync-gbrain` | **保持大脑同步** — 通过 `gbrain sources add` + `gbrain sync --strategy code` 将当前仓库的代码重新索引到 gbrain，刷新 CLAUDE.md 中的 `## GBrain Search Guidance` 块，并在能力检查失败时自动移除引导信息。`--incremental`（默认）、`--full`、`--dry-run`。幂等操作；可安全重复运行。 |
| `/gstack-upgrade` | **自更新器** — 将 gstack 升级到最新版。检测全局 vs vendored 安装，同步两者，显示变更内容。 |

### 新二进制工具（v0.19）

除了斜杠命令 Skill，gstack 还提供独立 CLI 工具，用于不属于会话内部的工作流：

| 命令 | 功能 |
| --- | --- |
| `gstack-model-benchmark` | **跨模型基准测试** — 用同一个 Prompt 分别通过 Claude、GPT（通过 Codex CLI）和 Gemini 运行；对比延迟、Token、成本和（可选的）LLM 评判质量分数。按 Provider 检测认证，不可用的 Provider 自动跳过。输出为表格、JSON 或 Markdown。`--dry-run` 只验证标志和认证，不消耗 API 调用。 |
| `gstack-taste-update` | **设计品味学习** — 将 `/design-shotgun` 的审批和拒绝写入持久化的每项目品味档案。每周衰减 5%。反馈到未来的变体生成中，让系统学习你实际选择什么。 |

### 连续检查点模式（可选，默认本地）

设置 `gstack-config set checkpoint_mode continuous` 后，Skill 会在你工作时自动提交，带有 `WIP:` 前缀和结构化的 `[gstack-context]` 正文（决策、剩余工作、失败方案）。崩溃和上下文切换后可恢复。`/context-restore` 读取这些提交来重建会话状态。`/ship` 在创建 PR 前过滤压缩 WIP 提交（保留非 WIP 提交），确保 bisect 干净。Push 是可选的，通过 `checkpoint_push=true` 开启——默认仅本地，不会在每个 WIP 提交时触发 CI。

### 领域 Skill + 原始 CDP 逃生舱

两个新的浏览器原语让 gstack Agent 随时间不断积累能力：

- **`$B domain-skill save`** — Agent 保存按站点的笔记（例如"LinkedIn 的 Apply 按钮在 iframe 里"），下次访问同一主机名时自动触发。隔离状态 → 成功使用 3 次后激活 → 可通过 `$B domain-skill promote-to-global` 跨项目推广。存储与 `/learn` 的每项目学习文件并列。完整参考：**[docs/domain-skills.md](https://github.com/garrytan/gstack/blob/main/docs/domain-skills.md)**。
- **`$B cdp <Domain.method>`** — 原始 Chrome DevTools Protocol 逃生舱，用于策展命令无法覆盖的罕见场景。默认拒绝：方法必须明确添加到 `browse/src/cdp-allowlist.ts` 并附一行理由。双层互斥锁将浏览器范围的 CDP 调用与每标签页工作串行化。数据导出类方法的输出包裹在 UNTRUSTED 信封中。

> 想要无护栏、无白名单、无守护进程的原始 CDP——仅作为 Agent 到 Chrome 的薄传输层？[browser-use/browser-harness-js](https://github.com/browser-use/browser-harness-js) 是不同的哲学（Agent 编写的辅助函数 vs gstack 的策展命令），如果你不想要 gstack 的安全栈，这是个好选择。两者可以共存：gstack 的 `$B cdp` 和 harness 都可以通过 Playwright 的 `newCDPSession` 连接到同一个 Chrome。

**[每个 Skill 的深度解析、示例和哲学 →](https://github.com/garrytan/gstack/blob/main/docs/skills.md)**

### Karpathy 的四种失败模式？已覆盖。

Andrej Karpathy 的 [AI 编码规则](https://github.com/forrestchang/andrej-karpathy-skills)（17K Star）精准指出了四种失败模式：错误假设、过度复杂、无关编辑、命令式而非声明式。gstack 的工作流 Skill 强制解决了这四个问题。`/office-hours` 在代码编写之前就把假设暴露出来。Confusion Protocol 阻止 Claude 在架构决策上猜测。`/review` 捕获不必要的复杂性和顺手牵羊式的编辑。`/ship` 将任务转化为可验证的目标，以测试优先的方式执行。如果你已经在使用 Karpathy 风格的 CLAUDE.md 规则，gstack 就是让这些规则在整个 Sprint 而非单个 Prompt 中持续生效的工作流执行层。

## 并行 Sprint

gstack 用好一个 Sprint 已经很出色。十个 Sprint 同时跑才真正有趣。

**设计是核心。** `/design-consultation` 从零构建你的设计系统，研究行业现状，提出有创意的风险方案，并编写 `DESIGN.md`。但真正的魔法是 Shotgun-to-HTML 管道。

**`/design-shotgun` 是你的探索工具。** 你描述想要什么。它用 GPT Image 生成 4-6 个 AI Mockup 变体。然后在浏览器中打开对比面板，所有变体并排展示。你选择喜欢的，留下反馈（"更多留白"、"更粗的标题"、"去掉渐变"），它生成新的一轮。重复到你满意为止。品味记忆在几轮后开始生效，偏向你实际喜欢的东西。不再是口头描述愿景然后祈祷 AI 理解——你看到选项，挑好的，视觉化迭代。

**`/design-html` 把它变成现实。** 把批准的 Mockup（来自 `/design-shotgun`、CEO 计划、设计审查或仅仅是描述）转化为生产级 HTML/CSS。不是那种在一个视口宽度看起来不错、其他地方全崩的 AI HTML。它使用 Pretext 进行计算文本布局：文本真正在调整大小时自动换行，高度随内容调整，布局是动态的。30KB 开销，零依赖。它检测你的框架（React、Svelte、Vue）并输出正确的格式。智能 API 路由根据是 Landing Page、Dashboard、Form 还是 Card 布局选择不同的 Pretext 模式。输出是可以直接发布的，不是 demo。

**`/qa` 是一个巨大突破。** 它让我从 6 个并行 Worker 增加到 12 个。Claude Code 说 *"我看到问题了"* 然后真正修复它、生成回归测试、验证修复——这改变了我的工作方式。Agent 现在有眼睛了。

**智能 Review 路由。** 就像运营良好的初创公司：CEO 不需要看基础设施的 Bug 修复，后端变更不需要设计审查。gstack 跟踪已运行了哪些 Review，判断什么合适，自动做正确的事。Review Readiness Dashboard 在你发布前告诉你当前状态。

**测试一切。** `/ship` 如果你的项目没有测试框架，会从零引导一个。每次 `/ship` 运行都会产出覆盖率审计。每个 `/qa` 的 Bug 修复都生成回归测试。100% 测试覆盖率是目标——测试让直觉式编码 (vibe coding) 变成安全编码，而非鲁莽编码 (yolo coding)。

**`/document-release` 是你从未有过的工程师。** 它读取项目中的每个文档文件，交叉引用 diff，更新所有过时的内容。README、ARCHITECTURE、CONTRIBUTING、CLAUDE.md、TODOS — 全部自动保持最新。现在 `/ship` 会自动调用它 — 无需额外命令就能保持文档同步。

**真实浏览器模式。** `/open-gstack-browser` 启动 GStack Browser——一个 AI 控制的 Chromium，带反爬虫隐身、自定义品牌和内置侧边栏扩展。Google 和 NYTimes 等网站可以免验证码访问。菜单栏显示"GStack Browser"而非"Chrome for Testing"。你的常规 Chrome 完全不受影响。所有现有 browse 命令照常工作。`$B disconnect` 返回无头模式。浏览器在窗口打开期间一直存活……没有空闲超时在你工作时杀掉它。

**侧边栏 Agent — 你的 AI 浏览器助手。** 在 Chrome 侧边栏中输入自然语言，一个子 Claude 实例会执行它。"导航到设置页面并截图。""用测试数据填写这个表单。""遍历这个列表中的每一项并提取价格。"侧边栏自动路由到合适的模型：Sonnet 用于快速操作（点击、导航、截图），Opus 用于阅读和分析。每个任务最多 5 分钟。侧边栏 Agent 在隔离会话中运行，不会干扰你的主 Claude Code 窗口。一键从侧边栏底部导入 Cookie。

**个人自动化。** 侧边栏 Agent 不只是开发工作流。例如："浏览我孩子学校的家长门户，把所有其他家长的姓名、电话号码和照片添加到我的 Google Contacts。"两种认证方式：(1) 在 headed 浏览器中登录一次，你的会话会保持；(2) 点击侧边栏底部的"cookies"按钮从你的真实 Chrome 导入 Cookie。认证完成后，Claude 导航目录、提取数据并创建联系人。

**Prompt 注入防御。** 恶意网页会试图劫持你的侧边栏 Agent。gstack 提供多层防御：一个随浏览器打包的 22MB ML 分类器在本地扫描每个页面和工具输出；一个 Claude Haiku 转录检查对完整对话形态进行投票；系统提示中的随机 Canary Token 捕获跨文本、工具参数、URL 和文件写入的会话数据泄露尝试；裁决组合器要求两个分类器达成一致才执行阻止（防止单模型对 Stack Overflow 类指令页面的误报）。侧边栏标题中的盾牌图标显示状态（绿/黄/红）。可通过 `GSTACK_SECURITY_ENSEMBLE=deberta` 选择启用 721MB DeBERTa-v3 集成模型进行 2-of-3 共识。紧急停止开关：`GSTACK_SECURITY_OFF=1`。完整技术栈见 [ARCHITECTURE.md](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md#prompt-injection-defense-sidebar-agent)。

**AI 卡住时的浏览器交接。** 遇到 CAPTCHA、认证墙或 MFA 提示？`$B handoff` 在完全相同的页面打开一个可见的 Chrome，保留所有 Cookie 和标签页。你解决问题后告诉 Claude 完成了，`$B resume` 从中断处继续。Agent 在连续 3 次失败后甚至会自动建议你这样做。

**`/pair-agent` 是跨 Agent 协调。** 你在 Claude Code 中。你还在运行 OpenClaw。或者 Hermes。或者 Codex。你想让它们都看同一个网站。输入 `/pair-agent`，选择你的 Agent，GStack Browser 窗口打开，你可以观看。Skill 打印一段说明。把那段说明粘贴到另一个 Agent 的聊天中。它交换一次性设置密钥获取会话 Token，创建自己的标签页，开始浏览。你可以看到两个 Agent 在同一个浏览器中工作，各自在自己的标签页中，互不干扰。如果安装了 ngrok，隧道会自动启动，另一个 Agent 可以在完全不同的机器上。同一机器上的 Agent 使用零摩擦快捷方式直接写入凭证。这是首次来自不同厂商的 AI Agent 能够通过共享浏览器进行协调，并具备真正的安全性：范围化 Token、标签页隔离、速率限制、域名限制和活动归属。

**多 AI 第二意见。** `/codex` 从 OpenAI 的 Codex CLI 获取独立审查——一个完全不同的 AI 审查同一个 diff。三种模式：带通过/失败门槛的代码审查、主动尝试破坏你代码的对抗性挑战，以及带会话连续性的开放咨询。当 `/review`（Claude）和 `/codex`（OpenAI）都审查了同一分支时，你会得到跨模型分析，展示哪些发现重叠，哪些是各自独有的。

**按需安全护栏。** 说"be careful"，`/careful` 会在任何破坏性命令前发出警告 — rm -rf、DROP TABLE、force-push、git reset --hard。`/freeze` 在调试时将编辑锁定到一个目录，防止 Claude "顺手修复"不相关的代码。`/guard` 同时激活两者。`/investigate` 自动冻结到正在调查的模块。

**主动 Skill 建议。** gstack 会注意到你处于哪个阶段 — 头脑风暴、审查、调试、测试 — 并建议合适的 Skill。不喜欢？说"stop suggesting"，它会跨会话记住。

## 10-15 个并行 Sprint

gstack 配合一个 Sprint 就很强大。十个同时跑则是颠覆性的。

[Conductor](https://conductor.build/) 并行运行多个 Claude Code 会话 — 每个在自己的隔离工作区中。一个会话在新想法上运行 `/office-hours`，另一个对 PR 运行 `/review`，第三个在实现功能，第四个在 staging 上运行 `/qa`，还有六个在其他分支上。全部同时进行。我通常运行 10-15 个并行 Sprint — 这是目前的实际上限。

Sprint 结构是让并行化可行的关键。没有流程，十个 Agent 就是十个混乱源。有了流程 — Think、Plan、Build、Review、Test、Ship — 每个 Agent 都清楚该做什么、何时停止。你像 CEO 管理团队一样管理它们：关注重要的决策，让其余的自动运行。

### 语音输入（AquaVoice、Whisper 等）

gstack Skill 有语音友好的触发短语。自然地说出你想要的 — "run a security check"、"test the website"、"do an engineering review" — 对应的 Skill 就会激活。你不需要记住斜杠命令名或缩写。

## 卸载

### 方式 1：运行卸载脚本

如果 gstack 已安装在你的机器上：

```
~/.claude/skills/gstack/bin/gstack-uninstall
```

它会处理 Skill、符号链接、全局状态（`~/.gstack/`）、项目本地状态、browse 守护进程和临时文件。使用 `--keep-state` 保留配置和分析数据。使用 `--force` 跳过确认。

### 方式 2：手动移除（没有本地仓库）

如果你没有克隆的仓库（例如你通过 Claude Code 粘贴安装，后来删除了克隆）：

```
# 1. 停止 browse 守护进程
pkill -f "gstack.*browse" 2>/dev/null || true

# 2. 移除指向 gstack/ 的每 skill 符号链接
find ~/.claude/skills -maxdepth 1 -type l 2>/dev/null | while read -r link; do
  case "$(readlink "$link" 2>/dev/null)" in gstack/*|*/gstack/*) rm -f "$link" ;; esac
done

# 3. 移除 gstack
rm -rf ~/.claude/skills/gstack

# 4. 移除全局状态
rm -rf ~/.gstack

# 5. 移除集成（跳过你从未安装过的）
rm -rf ~/.codex/skills/gstack* 2>/dev/null
rm -rf ~/.factory/skills/gstack* 2>/dev/null
rm -rf ~/.kiro/skills/gstack* 2>/dev/null
rm -rf ~/.openclaw/skills/gstack* 2>/dev/null

# 6. 移除临时文件
rm -f /tmp/gstack-* 2>/dev/null

# 7. 每项目清理（从每个项目根目录运行）
rm -rf .gstack .gstack-worktrees .claude/skills/gstack 2>/dev/null
rm -rf .agents/skills/gstack* .factory/skills/gstack* 2>/dev/null
```

### 清理 CLAUDE.md

卸载脚本不会编辑 CLAUDE.md。在每个添加了 gstack 的项目中，手动移除 `## gstack` 和 `## Skill routing` 部分。

### Playwright

`~/Library/Caches/ms-playwright/`（macOS）会保留，因为其他工具可能共享它。如果没有其他工具需要它，可以手动删除。

---

免费、MIT 许可、开源。没有高级版、没有候补名单。

我开源了我构建软件的方式。你可以 Fork 它，让它成为你自己的。

> **我们在招人。** 想以 AI 编码速度交付真实产品并帮助完善 gstack？来 YC 工作 — [ycombinator.com/software](https://ycombinator.com/software)。极具竞争力的薪资和股权。旧金山 Dogpatch 区。

## GBrain — 编码 Agent 的持久知识库

[GBrain](https://github.com/garrytan/gbrain) 是一个面向 AI Agent 的持久知识库——把它想象成你的 Agent 在会话之间真正保留的记忆。GStack 提供从零到"运行中，我的 Agent 可以调用它"的一条命令路径。

```
/setup-gbrain
```

三条路径，选一条：

- **Supabase，现有 URL** — 你的云端 Agent 已经配置了一个 Brain；粘贴 Session Pooler URL，这台笔记本电脑就能使用相同的数据。
- **Supabase，自动配置** — 粘贴 Supabase Personal Access Token；Skill 创建新项目，轮询直到健康，获取 Pooler URL，交给 `gbrain init`。端到端约 90 秒。
- **PGLite 本地** — 零账户、零网络、约 30 秒。仅在此 Mac 上的隔离 Brain。适合先试用；之后可用 `/setup-gbrain --switch` 迁移到 Supabase。

初始化后，Skill 会提议将 gbrain 注册为 Claude Code 的 MCP 服务器（`claude mcp add gbrain -- gbrain serve`），这样 `gbrain search`、`gbrain put_page` 等就会作为一等公民的强类型工具出现 — 而非 bash shell 调用。

**保持 Brain 同步。** 在任何仓库中运行 `/sync-gbrain` 将其代码重新索引到 gbrain（默认增量、`--full` 全量重建、`--dry-run` 预览）。Skill 通过 `gbrain sources add` 将当前工作目录注册为联邦来源，运行 `gbrain sync --strategy code`，并在项目的 CLAUDE.md 中写入 `## GBrain Search Guidance` 块，让 Agent 优先使用 `gbrain search` / `code-def` / `code-refs` 而非 Grep。该块在能力检查失败时自动移除 — 没有指向未安装工具的过时引导。

**每远程仓库信任策略。** 你机器上的每个仓库获得以下三级之一：

- `read-write` — Agent 可以搜索 Brain 并从该仓库写回新页面
- `read-only` — Agent 可以搜索但不能写入（适合多客户顾问：搜索共享 Brain，不会在客户 B 的仓库中污染客户 A 的数据）
- `deny` — 完全不与 gbrain 交互

Skill 每个仓库只询问一次。决策在同一远程的 Worktree 和分支间保持一致。

**GStack 记忆同步（不同功能，相同的私有仓库基础设施）。** 可选地将你的 gstack 状态（学习成果、CEO 计划、设计文档、回顾、开发者画像）推送到私有 Git 仓库，让记忆跨机器跟随你，带一次性隐私提示（全部允许 / 仅制品 / 关闭）和纵深防御秘密扫描器，阻止 AWS 密钥、Token、PEM 块和 JWT 在离开你的机器之前。

```
gstack-brain-init
```

**完全指南 — 每个场景、每个标志、每个 bin 辅助工具、每个故障排除步骤：** [USING\_GBRAIN\_WITH\_GSTACK.md](https://github.com/garrytan/gstack/blob/main/USING_GBRAIN_WITH_GSTACK.md)

其他参考：[docs/gbrain-sync.md](https://github.com/garrytan/gstack/blob/main/docs/gbrain-sync.md)（同步专项指南）· [docs/gbrain-sync-errors.md](https://github.com/garrytan/gstack/blob/main/docs/gbrain-sync-errors.md)（错误索引）

## 文档

| 文档 | 覆盖内容 |
| --- | --- |
| [Skill 深度解析](https://github.com/garrytan/gstack/blob/main/docs/skills.md) | 每个 Skill 的哲学、示例和工作流（包括 Greptile 集成） |
| [Builder 精神](https://github.com/garrytan/gstack/blob/main/ETHOS.md) | Builder 哲学：Boil the Lake、Search Before Building、知识三层 |
| [使用 GBrain with GStack](https://github.com/garrytan/gstack/blob/main/USING_GBRAIN_WITH_GSTACK.md) | `/setup-gbrain` 的每条路径、标志、bin 辅助工具和故障排除步骤 |
| [GBrain 同步](https://github.com/garrytan/gstack/blob/main/docs/gbrain-sync.md) | 跨机器记忆设置、隐私模式、故障排除 |
| [架构](https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md) | 设计决策和系统内部 |
| [浏览器参考](https://github.com/garrytan/gstack/blob/main/BROWSER.md) | `/browse` 的完整命令参考 |
| [贡献指南](https://github.com/garrytan/gstack/blob/main/CONTRIBUTING.md) | 开发设置、测试、贡献者模式和开发模式 |
| [更新日志](https://github.com/garrytan/gstack/blob/main/CHANGELOG.md) | 每个版本的更新内容 |

gstack 包含**可选的**使用遥测，用于帮助改进项目。以下是具体说明：

- **默认关闭。** 除非你明确同意，否则不会发送任何数据。
- **首次运行时，** gstack 会询问你是否愿意分享匿名使用数据。你可以拒绝。
- **发送的内容（如果你选择开启）：** Skill 名称、持续时间、成功/失败、gstack 版本、操作系统。仅此而已。
- **永远不会发送：** 代码、文件路径、仓库名、分支名、提示词或任何用户生成的内容。
- **随时可改：** `gstack-config set telemetry off` 立即禁用一切。

数据存储在 [Supabase](https://supabase.com/)（开源 Firebase 替代品）。Schema 在 [`supabase/migrations/`](https://github.com/garrytan/gstack/blob/main/supabase/migrations) 中 — 你可以验证具体收集了什么。仓库中的 Supabase 发布密钥是公钥（类似 Firebase API Key）— 行级安全策略拒绝所有直接访问。遥测通过经过验证的 Edge Functions 流入，强制执行 Schema 检查、事件类型白名单和字段长度限制。

**本地分析始终可用。** 运行 `gstack-analytics` 从本地 JSONL 文件查看个人使用仪表板 — 无需远程数据。

## 故障排除

**Skill 没有出现？** `cd ~/.claude/skills/gstack && ./setup`

**`/browse` 失败？** `cd ~/.claude/skills/gstack && bun install && bun run build`

**安装过时？** 运行 `/gstack-upgrade` — 或在 `~/.gstack/config.yaml` 中设置 `auto_upgrade: true`

**想要更短的命令？** `cd ~/.claude/skills/gstack && ./setup --no-prefix` — 从 `/gstack-qa` 切换到 `/qa`。你的选择在后续升级中会被记住。

**想要带命名空间的命令？** `cd ~/.claude/skills/gstack && ./setup --prefix` — 从 `/qa` 切换到 `/gstack-qa`。如果你同时运行其他 Skill 包，这很有用。

**Codex 提示 "Skipped loading skill(s) due to invalid SKILL.md"？** 你的 Codex Skill 描述已过时。修复方法：`cd ~/.codex/skills/gstack && git pull && ./setup --host codex` — 或对于仓库本地安装：`cd "$(readlink -f .agents/skills/gstack)" && git pull && ./setup --host codex`

**Windows 用户：** gstack 可通过 Git Bash 或 WSL 在 Windows 11 上运行。除 Bun 外还需要 Node.js — Bun 在 Windows 上存在 Playwright pipe transport 的已知 Bug（[bun#4253](https://github.com/oven-sh/bun/issues/4253)）。Browse Server 会自动回退到 Node.js。确保 `bun` 和 `node` 都在你的 PATH 上。

**Claude 说看不到 Skill？** 确保你项目的 `CLAUDE.md` 中有 gstack 部分。添加以下内容：

```
## gstack
Use /browse from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.
Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review,
/design-consultation, /design-shotgun, /design-html, /review, /ship, /land-and-deploy,
/canary, /benchmark, /browse, /open-gstack-browser, /qa, /qa-only, /design-review,
/setup-browser-cookies, /setup-deploy, /setup-gbrain, /sync-gbrain, /retro, /investigate, /document-release,
/codex, /cso, /autoplan, /pair-agent, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn.
```