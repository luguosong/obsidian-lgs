---
title: "GBrain：AI Agent 知识大脑"
source: "https://github.com/garrytan/gbrain"
description: "Garry 打造的 AI Agent 知识大脑，为 OpenClaw/Hermes 等 Agent 提供持久记忆与知识图谱能力。"
author:
tags:
  - ai
  - 扩展

---
字数：6638
## GBrain

你的 AI Agent 很聪明，但容易遗忘。GBrain 为它装上大脑。

由 Y Combinator 总裁兼 CEO 打造，用于驱动他实际运行的 AI Agent。这是他 OpenClaw 和 Hermes 部署的生产级大脑：**17,888 页、4,383 人、723 家公司**，21 个定时任务自主运行，12 天内构建完成。Agent 在你睡觉时摄入会议记录、邮件、推文、语音通话和原创想法，并持续丰富遇到的每个人和公司的信息，夜间自动修复引用、整合记忆。你醒来时，大脑已比你入睡时更聪明。

大脑会自我连线。每次写入页面时，系统会自动提取实体引用并创建类型化链接（`attended`、`works_at`、`invested_in`、`founded`、`advises`），完全无需 LLM 调用。混合搜索、自动连线的知识图谱、结构化时间线、反向链接增权排名——问"谁在 Acme AI 工作？"或"Bob 本季度投资了什么？"，能得到单纯向量搜索无法触达的答案。经过与同类产品的并排基准测试，gbrain 在一个 240 页 Opus 生成的富文本语料库上达到 **P@5 49.1%、R@5 97.9%**，比禁用图谱的自身变体高出 **+31.4 个 P@5 百分点**，也比 ripgrep-BM25 加纯向量 RAG 高出相近幅度。图谱层加上 v0.12 的提取质量共同拉开了这一差距。完整 BrainBench 评分卡和语料库见兄弟仓库 [gbrain-evals](https://github.com/garrytan/gbrain-evals)。

GBrain 将这些模式通用化，包含 34 个 skill，30 分钟内完成安装，让你的 Agent 自动工作。随着 Garry 的私人 Agent 越来越聪明，你的也一样。

> [!info] v0.25.0 新特性 — BrainBench-Real（会话捕获，贡献者可选加入）
> 在 shell 中设置 `GBRAIN_CONTRIBUTOR_MODE=1` 后，所有通过 MCP、CLI 或 subagent 工具桥发起的真实 `query` 和 `search` 调用将被脱敏捕获到 `eval_candidates` 表。用 `gbrain eval export` 导出快照，用 `gbrain eval replay` 在代码变更后回放。系统返回三个指标：已捕获 slug 与当前检索 slug 之间的平均 Jaccard@k、top-1 稳定性和延迟差值 Δ。**生产用户默认关闭**——不会意外积累数据。详见 [docs/eval-bench.md](https://github.com/garrytan/gbrain/blob/master/docs/eval-bench.md)，NDJSON 线格式见 [docs/eval-capture.md](https://github.com/garrytan/gbrain/blob/master/docs/eval-capture.md)。

> [!info] v0.28.8 新特性 — 内置 LongMemEval
> `gbrain eval longmemeval <dataset.jsonl>` 对 gbrain 的混合检索运行公开的 [LongMemEval](https://huggingface.co/datasets/xiaowu0162/longmemeval) 基准测试。每次运行使用一个内存中的 PGLite 实例，在题目之间执行 `TRUNCATE`（运行时枚举表，兼容 schema 迁移），在 Apple Silicon 上每题 p50 耗时 25.9ms。你的 `~/.gbrain` 大脑不会被触碰。检索到的聊天内容使用与保护 take 相同的 `INJECTION_PATTERNS` 进行净化——提示词注入防御的单一事实源。将 JSONL 输出交给 LongMemEval 的 `evaluate_qa.py` 进行评分。

> [!tip] [[快速开始]]
> **约 30 分钟即可获得完整可用的大脑。** 数据库 2 秒内就绪（PGLite，无需服务器）。你只需回答几个关于 API 密钥的问题。

> [!info] 文档说明
> **LLM 用户：** 获取 [`llms.txt`](https://github.com/garrytan/gbrain/blob/master/llms.txt) 查看文档地图，或获取 [`llms-full.txt`](https://github.com/garrytan/gbrain/blob/master/llms-full.txt) 获取内联了核心文档的完整地图（一次请求）。**Agent 用户：** 从 [`AGENTS.md`](https://github.com/garrytan/gbrain/blob/master/AGENTS.md) 开始（若你是 [[Claude Code]]，则看 [`CLAUDE.md`](https://github.com/garrytan/gbrain/blob/master/CLAUDE.md)）。

## 安装

GBrain 被设计为由 AI Agent 安装和操作。如果你还没有运行中的 Agent：

- **[OpenClaw](https://openclaw.ai/)**... 在 Render 上[一键部署 AlphaClaw](https://render.com/deploy?repo=https://github.com/chrysb/alphaclaw)（需 8GB+ 内存）
- **[Hermes Agent](https://github.com/NousResearch/hermes-agent)**... 在 [Railway 上一键部署](https://github.com/praveen-ks-2001/hermes-agent-template)

将以下内容粘贴给你的 Agent：

```
Retrieve and follow the instructions at:
https://raw.githubusercontent.com/garrytan/gbrain/master/INSTALL_FOR_AGENTS.md
```

就这样。Agent 会自动克隆仓库、安装 GBrain、配置大脑、加载 34 个 skill 并设置定时任务。你只需回答几个关于 API 密钥的问题，约 30 分钟完成。

如果你的 Agent 不会自动读取 `AGENTS.md`，请先将其指向该文件：`https://raw.githubusercontent.com/garrytan/gbrain/master/AGENTS.md` 是非 Claude Agent 的操作协议（安装、读取顺序、信任边界、常见任务）。完整文档地图请使用同一 URL 根路径下的 `llms.txt`。

### 独立 CLI（无 Agent）

```
git clone https://github.com/garrytan/gbrain.git && cd gbrain && bun install && bun link
gbrain init                     # 本地大脑，2 秒内就绪
gbrain import ~/notes/          # 索引你的 markdown 笔记
gbrain query "what themes show up across my notes?"
```

> [!warning] 安装注意事项
> **不要使用 `bun install -g github:garrytan/gbrain`。** Bun 会阻止全局安装时的顶层 postinstall hook，导致 schema 迁移从不运行，CLI 在第一次打开 PGLite 时报 `Aborted()`。请使用上方的 `git clone + bun install && bun link`。详见 [#218](https://github.com/garrytan/gbrain/issues/218)。
>
> **不要使用 `bun add -g gbrain` 或 `npm install -g gbrain`。** npm 注册表中有一个不相关的包抢占了该名称（`gbrain@1.3.x`）——你会静默安装到错误的二进制并覆盖正确的那个。v0.28.5+ 会在 `gbrain upgrade` 时检测到这一情况并打印恢复提示，但 `git clone + bun link` 是目前唯一可靠的安装方式，直到我们在 `@garrytan/gbrain` 下正式发布（v0.29 跟踪中）。详见 [#658](https://github.com/garrytan/gbrain/issues/658)。

搜索结果示例：

```
3 results (hybrid search, 0.12s):

1. concepts/do-things-that-dont-scale (score: 0.94)
   PG's argument that unscalable effort teaches you what users want.
   [Source: paulgraham.com, 2013-07-01]

2. originals/founder-mode-observation (score: 0.87)
   Deep involvement isn't micromanagement if it expands the team's thinking.

3. concepts/build-something-people-want (score: 0.81)
   The YC motto. Connected to 12 other brain pages.
```

### MCP Server（Claude Code、Cursor、Windsurf）

GBrain 通过 stdio 暴露 30+ 个 MCP 工具：

```
{
  "mcpServers": {
    "gbrain": { "command": "gbrain", "args": ["serve"] }
  }
}
```

添加到 `~/.claude/server.json`（[[Claude Code]]）、[[Settings]] > [[MCP Server]]s（Cursor）或你的客户端 MCP 配置中。

### 带 OAuth 2.1 的远程 MCP（ChatGPT、Claude Desktop、Cowork、Perplexity）

`gbrain serve --http` 启动一个生产级 OAuth 2.1 服务器，内置管理员面板。无需额外基础设施。所有主流 AI 客户端均可接入，每个请求都有作用域限制，每个操作都有日志记录。

```
# 启动 HTTP 服务器（首次启动时打印管理员 bootstrap token）
gbrain serve --http --port 3131

# 打开管理员面板，粘贴 bootstrap token，注册客户端
open http://localhost:3131/admin

# 公开暴露（设置 --public-url 使 OAuth issuer 一致）
ngrok http 3131 --url your-brain.ngrok.app
gbrain serve --http --port 3131 --public-url https://your-brain.ngrok.app

# ChatGPT 等支持 OAuth 的客户端也可以接入：
claude mcp add gbrain -t http https://your-brain.ngrok.app/mcp -H "Authorization: Bearer TOKEN"
```

在 `/admin` 面板注册 OAuth 客户端——点击 **Register client**，选择作用域，在弹出窗口中保存一次性显示的凭证。也可通过 `oauthProvider.registerClientManual(...)` 或 `gbrain auth register-client` CLI 以编程方式注册。

- **通过 MCP SDK 实现 OAuth 2.1** — 客户端凭证（机器对机器：Perplexity、Claude）、授权码 + PKCE（浏览器：ChatGPT）、refresh token 轮换、撤销、受保护资源元数据。可选的动态客户端注册（DCR）在 `--enable-dcr` 后启用（DCR redirect_uris 须为 `https://` 或回环地址，符合 RFC 6749 §3.1.2.1）。
- **作用域操作** — 30 个操作标记为 `read | write | admin`。`sync_brain` 和 `file_upload` 为 `localOnly`，HTTP 请求时会被拒绝。
- **React 管理员面板** — 7 个页面内嵌于二进制文件（~65KB gzip）。实时 SSE 活动流、Agent 列表、凭证查看、可过滤的请求日志、每客户端配置导出。
- **传统 [[Bearer Token]] 仍然有效** — v0.26 之前通过 `gbrain auth create` 创建的 token 继续以 `read+write+admin` 身份认证。v0.22.7 的简化 `src/mcp/http-transport.ts` 路径保留编译以向后兼容；v0.26+ 部署使用支持 OAuth 的 `serve-http.ts`。

各客户端接入指南：[`docs/mcp/`](https://github.com/garrytan/gbrain/blob/master/docs/mcp/DEPLOY.md)。安全加固默认值、环境变量和威胁模型：[SECURITY.md](https://github.com/garrytan/gbrain/blob/master/SECURITY.md)。

### 与 GStack 配合使用

如果你的工程 Agent 运行在 [GStack](https://github.com/garrytan/gstack) 上，将其指向 gbrain 进行代码查找，而非使用 grep+read。Cathedral II（v0.21.0）提供调用图边和两遍检索——当 Agent 遍历符号图谱而非逐行扫描文件时，`/investigate`、`/review`、`/plan-eng-review` 和 `/office-hours` 都能受益。

五个神奇时刻命令：

```
gbrain code-callers searchKeyword           # 谁调用了这个符号？
gbrain code-callees searchKeyword           # 这个符号调用了什么？
gbrain code-def BrainEngine                 # X 在哪里定义？
gbrain code-refs BrainEngine                # 所有引用位置
gbrain query "how does N+1 handling work" --near-symbol BrainEngine.searchKeyword --walk-depth 2
```

所有五个命令在非 TTY 场景下（gh-CLI 惯例）自动输出 JSON，使得通过 bash 调用的 GStack subagent 能获得干净可解析的响应。运行 `gbrain sources add <repo> --strategy code` 对仓库建立索引，之后 Agent 的大脑优先查找范围就涵盖了代码，而不仅仅是 Markdown。（[Cathedral II 发布说明](https://github.com/garrytan/gbrain/blob/master/CHANGELOG.md#0210---2026-04-25)）

## 34 个 Skill

GBrain 内置 34 个 skill，由 `skills/RESOLVER.md`（或你的 OpenClaw 的 `AGENTS.md`，v0.19 起两个文件名均支持）进行调度。Resolver 告诉 Agent 对于任何任务应该读取哪个 skill。v0.25.1 新增了 9 个研究型 skill（以 `book-mirror` 为旗舰，附带 8 个配对 skill）；详见下方新增的「研究与综合」章节。

[Skill 文件即代码。](https://x.com/garrytan/status/2042925773300908103) 它们是完成知识工作最有力的方式。一个 skill 文件是一个内容丰富的 Markdown 文档，编码了完整的工作流：何时触发、检查什么、如何与其他 skill 协同、质量标准是什么。Agent 读取 skill 并执行它。Skill 还可以调用 GBrain 中打包的确定性 TypeScript 代码（search、import、embed、sync），处理那些不应交由 LLM 判断的部分。[薄壳层、厚 skill](https://github.com/garrytan/gbrain/blob/master/docs/ethos/THIN_HARNESS_FAT_SKILLS.md)：智慧在 skill 中，而非运行时。

### 始终开启

| Skill | 功能说明 |
| --- | --- |
| **signal-detector** | 对每条消息触发。并行启动轻量模型捕获原创想法和实体提及。大脑在自动驾驶中持续成长。 |
| **brain-ops** | 任何外部 API 调用前先查大脑。读取-丰富-写入循环让每次响应都更聪明。 |

### 内容摄入

| Skill | 功能说明 |
| --- | --- |
| **ingest** | 轻量路由器。检测输入类型并分发给合适的摄入 skill。 |
| **idea-ingest** | 链接、文章、推文转化为大脑页面，含分析、作者人员页面和交叉链接。 |
| **media-ingest** | 视频、音频、PDF、书籍、截图、GitHub 仓库。转录、实体提取、反向链接传播。 |
| **meeting-ingestion** | 会议记录转化为大脑页面。每位与会者得到丰富信息。每家公司获得时间线条目。 |
| **voice-note-ingest** | 语音笔记逐字保存——确切措辞被保留，从不意译。根据内容路由到 originals/concepts/people/companies/ideas/personal/voice-notes。 |
| **article-enrichment** | 原始文章转化为结构化页面，含执行摘要、逐字引用、关键洞察和重要性说明。 |

### 研究与综合（v0.25.1）

| Skill | 功能说明 |
| --- | --- |
| **book-mirror** | 旗舰 skill。给 Agent 一本书，获得个性化的逐章双栏分析。左栏保留章节实际内容；右栏用你在大脑中的话语将每个想法映射到你的生活。使用 Opus 处理一本 20 章的书约 $6。搭配 `gbrain book-mirror` CLI 使用可信运行时。 |
| **strategic-reading** | 从某个具体问题视角阅读书籍/文章/案例研究。输出：含做/避/观察以及短/中/长期建议的实用手册。 |
| **concept-synthesis** | 将数千个概念碎片整合为分层知识图谱（T1 Canon 到 T4 Riff）。追溯想法如何跨越多年笔记演化。 |
| **perplexity-research** | 大脑增强的网络研究。将大脑上下文发送给 Perplexity，使搜索聚焦于**新内容**而非已知信息。输出：执行摘要 + 关键新进展 + 确认信号 + 矛盾或更新 + 推荐大脑更新 + 引用来源。 |
| **archive-crawler** | 个人文件归档的通用存档器（Dropbox/Backblaze/Gmail 导出/硬盘转储）。除非在 `gbrain.yml` 中设置了 `archive-crawler.scan_paths:`，否则**拒绝运行**。默认安全围栏。 |
| **academic-verify** | 追溯研究声明的完整链路：发表 → 方法论 → 原始数据 → 独立复现。通过 perplexity-research 路由；产出裁决（已验证/部分验证/不可验证/错误归因/已撤稿）。 |
| **brain-pdf** | 通过 [[gstack]] `make-pdf` 二进制将任何大脑页面渲染为出版级 PDF。剥离 frontmatter，净化 emoji，应用页眉。 |

### 大脑运维

| Skill | 功能说明 |
| --- | --- |
| **enrich** | 分层丰富（Tier 1/2/3）。创建和更新人员/公司页面，含汇编后的事实和时间线。 |
| **query** | 三层搜索加综合与引用。若大脑中没有相关信息，明确说明而非胡编乱造。 |
| **maintain** | 定期健康维护：陈旧页面、孤立页面、死链、引用审计、反向链接强制执行、标签一致性。v0.23 加入 dream cycle 的 synthesize + patterns 阶段……夜间对话记录转化为反思、原创想法和 25 年模式。 |
| **citation-fixer** | 扫描页面中缺失或格式错误的引用，按标准格式修复。 |
| **repo-architecture** | 新大脑文件存放位置的决策协议：主要主题决定目录，而非格式。 |
| **publish** | 将大脑页面分享为密码保护的 HTML。无 LLM 调用。 |
| **data-research** | 使用参数化 YAML 方案的结构化数据研究。从邮件中提取投资人更新、支出、公司指标。 |

### 运营管理

| Skill | 功能说明 |
| --- | --- |
| **daily-task-manager** | 带优先级（P0-P3）的任务生命周期管理。以可搜索的大脑页面存储。 |
| **daily-task-prep** | 晨间准备：含每位与会者大脑上下文的日历预览、未结线索、任务回顾。 |
| **cron-scheduler** | 定时任务错峰调度（5 分钟偏移），安静时段（时区感知，含起床覆盖），幂等性保证。 |
| **reports** | 带时间戳的报告加关键词路由。"最新简报是什么？"立刻找到。 |
| **cross-modal-review** | 通过前一个模型的质量门控。拒绝路由：若一个模型拒绝，静默切换。 |
| **webhook-transforms** | 外部事件（短信、会议、社交提及）转化为含实体提取的大脑页面。 |
| **testing** | 验证每个 skill 是否有带 frontmatter 的 SKILL.md、manifest 覆盖率、resolver 覆盖率。 |
| **skill-creator** | 按合规标准创建新 skill，并对现有 skill 进行 MECE 检查。 |
| **skillify** | "skillify it!" 元 skill。编排 10 步循环，将失败转化为持久 skill：通过 `gbrain skillify scaffold` 创建 stub 骨架，编写真实逻辑，通过 `gbrain skillify check` + `gbrain check-resolvable` 验证。 |
| **skillpack-check** | Agent 可读的 gbrain 健康报告。CI 用退出码；调试用 JSON。适合定时任务。 |
| **smoke-test** | 8 项重启后健康检查，含自动修复（Bun、CLI、DB、worker、Zod CJS、gateway、API key、brain repo）。用户自定义测试放于 `~/.gbrain/smoke-tests.d/*.sh`。 |
| **minion-orchestrator** | 在单个 skill 中处理后台任务。通过 `gbrain jobs submit shell` 提交 shell 任务（operator/CLI，MCP 屏蔽保留名），通过 `gbrain agent run` 启动 LLM subagent。支持父子 DAG、`child_done` 收件箱、跨 worker 重启的持久化。 |

### 身份与配置

| Skill          | 功能说明                                                                                  |
| -------------- | ------------------------------------------------------------------------------------- |
| **soul-audit** | 6 阶段面谈，生成 SOUL.md（Agent 身份）、USER.md（用户画像）、ACCESS_POLICY.md（4 级隐私）、HEARTBEAT.md（运营节奏）。 |
| **setup**      | 自动配置 PGLite 或 Supabase，首次导入，GStack 检测。                                                |
| **migrate**    | 从 [[Obsidian]]、Notion、Logseq、markdown、CSV、JSON、Roam 通用迁移。                                 |
| **briefing**   | 每日简报，含会议上下文、活跃交易和引用跟踪。                                                                |

### 约定规范

`skills/conventions/` 中的跨领域规则：

- **quality.md**... 引用、反向链接、可关注性门控、来源归因
- **brain-first.md**... 任何外部 API 调用前的 5 步查找流程
- **model-routing.md**... 哪个任务用哪个模型
- **test-before-bulk.md**... 任何批量操作前先测试 3-5 个样本
- **cross-modal.yaml**... 审查配对和拒绝路由链

## 工作原理

```
信号到达（会议、邮件、推文、链接）
  -> 信号检测器捕获想法 + 实体（并行，从不阻塞）
  -> brain-ops：先查大脑（gbrain search, gbrain get）
  -> 携带完整上下文响应
  -> 写入：用新信息 + 引用更新大脑页面
  -> 自动链接：每次写入时提取类型化关系（无 LLM 调用）
  -> 同步：gbrain 为下次查询建立索引
```

每个循环都在积累知识。Agent 在会议后丰富人员页面。下次提到这个人时，Agent 已有上下文。差距每天都在复利增长。

系统自我进化。实体丰富度自动升级：只提及一次的人获得 stub 页面（Tier 3）；在三个不同来源出现后，获得网络和社交丰富（Tier 2）；经过会议或 8 次以上提及后，进入完整 pipeline（Tier 1）。大脑无需指令就能学习谁重要。确定性分类器通过失败-改进循环持续优化：记录每次 LLM 回退并从失败中生成更好的正则模式。`gbrain doctor` 展示演进轨迹："意图分类器：87% 确定性，较第 1 周的 40% 提升。"

> [!example] 使用示例
> "30 分钟内帮我准备与 Jordan 的会议"……拉取档案、共同历史、近期动态、未结线索
>
> "我对羞耻感与创始人绩效关系说过什么？"……搜索**你的**思考，而非互联网

## Minions：你的 subagent 不再丢失工作

内置于大脑的持久化 Postgres 原生任务队列。每个长时间运行的 Agent 任务现在都是一个能在 gateway 重启后存活、流式传输进度、可暂停/恢复/中途引导的任务，并显示在 `gbrain jobs list` 中。除现有大脑之外无需任何基础设施。

### 关键生产数字

以下是我的个人 OpenClaw 部署：一个 Render 容器，Supabase Postgres 存储 45,000 页大脑，19 个定时任务按计划触发，承载真实日常工作的 gateway 负载。任务：从外部 API 拉取 1 个月的社交帖子，端到端摄入大脑形成结构化页面。

|  | Minions | `sessions_spawn` |
| --- | --- | --- |
| 耗时 | **753ms** | **>10,000ms**（gateway 超时） |
| Token 成本 | **$0.00** | 每次约 $0.03 |
| 成功率 | **100%** | **0%**（无法启动） |
| 内存/任务 | ~2 MB | ~80 MB |

在 19 个定时任务的负载下，subagent 启动根本无法在 10 秒 gateway 墙前清场。Minions 以零 token 在 1 秒内完成。**规模测试：** 36 个月 19,240 条帖子，单个 bash 循环，总计约 15 分钟，$0.00。Subagent：最优情况约 9 分钟、约 $1.08 token 费用、约 40% 启动失败率。**实验室数据：** 持久性 ∞（SIGKILL 中途中断，10/10 恢复），吞吐量约 10 倍，扇出约 21 倍且无失败墙，内存约 400 倍更少。

完整基准数据见 [gbrain-evals](https://github.com/garrytan/gbrain-evals/tree/main/docs/benchmarks)。

### 路由规则

> **确定性**（相同输入 → 相同步骤 → 相同输出）→ **Minions**
> **需要判断**（输入需要评估或决策）→ **Subagent**

拉取帖子、解析 JSON、写入大脑页面、运行同步——确定性。$0 token，重启后存活，毫秒级运行时间。处理收件箱、评估会议优先级、决定冷邮件是否值得回复——需要判断。这才是 subagent 真正擅长的事。`minion_mode: pain_triggered`（默认值）自动处理路由。

### 解决了哪些问题

六大日常痛点——启动风暴、无响应 Agent、被遗忘的分发、运行中 gateway 崩溃、失控的孙进程、调试灾难——都属于"通过推理模型做确定性工作"的错误。Minions 通过不犯这个错误来修复它们：`max_children` 上限、`timeout_ms` + AbortSignal、`child_done` 收件箱、每个任务完整的 `parent_job_id`/`depth`/记录、带失速检测的 Postgres 持久化、通过递归 CTE 进行级联取消。还有幂等键、附件验证、`removeOnComplete` 和 `gbrain jobs smoke`（半秒内验证安装）。

```
gbrain jobs smoke                        # 验证安装
gbrain jobs submit sync --params '{}'    # 触发后台任务
gbrain jobs stats                        # 健康面板
gbrain jobs supervisor --concurrency 4   # 规范用法：自动重启 worker（仅 Postgres）
gbrain jobs work --concurrency 4         # 裸 worker（无崩溃恢复——建议用 supervisor）
```

`gbrain jobs supervisor` 通过指数退避保持 worker 在崩溃后存活，使用原子 PID 锁，在 `~/.gbrain/audit/supervisor-*.jsonl` 记录结构化审计事件，并提供 `start --detach`/`status --json`/`stop` 子命令供 Agent 调用。在容器中以 PID 1 运行；在 [[systemd]] 主机上作为 `gbrain-worker.service` 的子进程。完整部署指南：[`docs/guides/minions-deployment.md`](https://github.com/garrytan/gbrain/blob/master/docs/guides/minions-deployment.md)。读取 [`skills/minion-orchestrator/SKILL.md`](https://github.com/garrytan/gbrain/blob/master/skills/minion-orchestrator/SKILL.md) 了解父子 DAG、扇入收集、通过收件箱引导。

> [!tip] 核心结论
> **Minions 对后台工作不是比 subagent 好一点点，而是根本上不同的类别。** 753ms vs gateway 超时。$0 vs token 费用。100% vs 无法启动。如果你的 Agent 按计划做确定性工作，现在就用 Minions 运行。

### 健康检查与自愈

Minions 自 v0.11.1 起成为规范——每次 `gbrain upgrade` 都会自动运行迁移（schema → smoke → prefs → host 重写 → 环境感知自动安装）。若要手动验证或在晨间简报中接入定时任务：

```
gbrain doctor                    # 半迁移状态？打印醒目横幅并以非零退出
gbrain skillpack-check --quiet    # 0/1/2 退出码用于 pipeline 门控
gbrain skillpack-check | jq       # 完整 JSON：{healthy, summary, actions[], doctor, migrations}
```

若有异常，`actions[]` 会告诉你确切的修复命令。深度排查：[`docs/guides/minions-fix.md`](https://github.com/garrytan/gbrain/blob/master/docs/guides/minions-fix.md)。

将 gateway 定时任务迁移到 Minions（确定性脚本，每次触发零 LLM token）：[`docs/guides/minions-shell-jobs.md`](https://github.com/garrytan/gbrain/blob/master/docs/guides/minions-shell-jobs.md)。

## 持久化 Agent：gbrain agent（v0.15）

你的 subagent 运行现在能在崩溃后存活。OpenClaw 中途崩溃了？Worker 重启后重新认领任务，并从最后一次提交的轮次开始回放。50 个分片的扇出，一个分片崩溃——聚合器在所有子任务到达终态后仍会认领，并写出混合结果摘要。工具调用以两阶段账本形式持久化（`pending` → `complete | failed`），回放在构造上是安全的，而非靠运气。

```
# 提交单个 subagent 任务
gbrain agent run "summarize my last 10 journal pages"

# 将 N 个 prompt 扇出到 N 个 subagent 子任务 + 1 个聚合器
gbrain agent run "analyze every page" \
  --fanout-manifest manifests/pages.json \
  --subagent-def analyzer

# 跟踪运行中的任务（每轮心跳 + 完成时完整记录）
gbrain agent logs 1247 --follow --since 5m
```

持久化是核心：每次 Anthropic 轮次提交到 `subagent_messages`，每次工具调用提交到 `subagent_tool_executions`。Worker 被杀死、OpenClaw 崩溃、超时——全部可恢复。宿主仓库（你的 OpenClaw 等）通过 `GBRAIN_PLUGIN_PATH` + `gbrain.plugin.json` manifest 提供自己的 subagent 定义：详见 [`docs/guides/plugin-authors.md`](https://github.com/garrytan/gbrain/blob/master/docs/guides/plugin-authors.md)。需要 Worker 上的 `ANTHROPIC_API_KEY`。

## Skillify：说"skillify it！"让 Bug 从结构上无法复现

你的 OpenClaw 遇到了新的失败。你在对话中修复了一次。你说"skillify it！"然后这个修复就永久化了：一个带触发器的 SKILL.md、一个带测试的确定性脚本、一个 Agent 每天重新评估的路由 fixture、一个防止输出漂移的归档审计。十个步骤，全部必需。这个 Bug 不可能再现。

Hermes 和类似 Agent 框架会将创建 skill 作为后台行为自动执行。行得通——直到你不知道 Agent 发布了什么。检查清单会腐化。测试会漂移。Resolver 条目会过时。六个月后变成了一堆没人读过、没人测过、没人确信还在工作的不透明代码。GBrain 提供了相同能力，区别是人始终在控制回路中，每个步骤都是你可以运行的命令。

### 你需要的四个动词（v0.19）

```
# 1. 一次性为新 skill 创建所有 5 个 stub 文件。
gbrain skillify scaffold webhook-verify \
  --description "verify ngrok webhooks" \
  --triggers "verify the webhook,check tunnel" \
  --writes-pages --writes-to people/,companies/

# 2. 用真实逻辑 + 真实测试替换 SKILLIFY_STUB 占位符。
$EDITOR skills/webhook-verify/scripts/webhook-verify.mjs
$EDITOR test/webhook-verify.test.ts

# 3. 运行 10 项审计：SKILL.md 存在、脚本存在、单元 + E2E 测试、
#    LLM 评估、resolver 条目、触发器评估、check-resolvable 门控、大脑归档。
gbrain skillify check skills/webhook-verify/scripts/webhook-verify.mjs

# 4. 验证整棵树：可达性、MECE 重叠、DRY、路由缺口、
#    归档审计、SKILLIFY_STUB 占位符（若有 skill 仍有占位符则失败）。
gbrain check-resolvable              # 警告为建议，错误为阻塞
gbrain check-resolvable --strict     # 警告也阻塞（CI 可选启用）
```

幂等重运行。`--force` 重新生成 stub 文件但**永远不会**重复 resolver 行。Scaffold 在 2 秒内完成。真正的工作（你的规则、你的脚本、你的测试）才是你花时间的地方。其余都是 CLI 帮你写的样板代码。

### gbrain routing-eval — 捕捉用户实际碰到的路由缺口

在任意 skill 旁放置 `routing-eval.jsonl` fixture，每行格式为 `{intent, expected_skill, ambiguous_with?}`。`gbrain check-resolvable` 默认运行结构层；`gbrain routing-eval` 以专用 CI 命令运行相同的结构层。`--llm` 标志作为未来 LLM 决胜层的占位符接受，在此版本中输出 stderr 提示并仅运行结构层。误报（匹配了错误 skill）、漏路由（无 skill 匹配）和同义 fixture（intent 逐字复制了触发词）都以具体的 `file:line` 建议形式浮出。

### 适用于你的 OpenClaw，不只是 gbrain 仓库

v0.19 让 `gbrain check-resolvable` 同时接受 `AGENTS.md` 和 `RESOLVER.md` 作为 resolver 文件，位于 skills 目录或上一级目录（OpenClaw 原生工作区根布局）均可。当 `manifest.json` 缺失时，skill manifest 通过遍历 `skills/*/SKILL.md` 自动推导。设置 `OPENCLAW_WORKSPACE=~/your-openclaw/workspace` 即可直接使用：

```
export OPENCLAW_WORKSPACE=~/your-openclaw/workspace
gbrain check-resolvable --verbose
# 自动检测：工作区根目录的 AGENTS.md，从 SKILL.md 遍历推导出 107 个 skill，
# 发现 15 个不可达错误，108 个重叠和缺口的建议警告。
```

在真实 OpenClaw 部署的首次运行中，从 102 个 skill 中发现了 15 个不可达 skill——约 15% 的树处于暗区。那篇文章中[["Agent]] 永远无法到达的 skill"的陷阱，现在可见了。

### gbrain skillpack install — 将 25 个精选 skill 安装到你的 OpenClaw

gbrain 内置的 skill 是精选包。通过依赖闭包（共享约定一并安装）、逐文件 diff 保护（没有 `--overwrite-local` 时不会覆盖你的本地编辑）、文件锁（序列化并发安装）和原子 managed-block 更新（可清晰看到 gbrain 写入了什么）将其安装到工作区。

```
gbrain skillpack list                          # 25 curated skills
gbrain skillpack install brain-ops             # one skill + its shared conventions
gbrain skillpack install --all                 # the full bundle
gbrain skillpack install brain-ops --dry-run   # preview; no writes
gbrain skillpack diff brain-ops                # compare bundle vs your local copy
```

重复运行是安全的。`AGENTS.md` 中的 managed-block 标记让 `skillpack install` 能在多次单独安装中累积行，而不是互相覆盖。fence 内部的回执注释（`<!-- gbrain:skillpack:manifest cumulative-slugs="..." -->`）跨运行追踪 gbrain 已安装的内容。`install --all` 是唯一会执行修剪的路径；单个 skill 安装永远不会删除它没有安装的内容。如果你手动在 fence 内添加了一行，gbrain 在重装时会保留它，并输出 stderr 通知告知你的 Agent 进行检查。

**Skillify 是让 skill 树在六个月持续积累工作中存活下来的关键。** 阅读 [`skills/skillify/SKILL.md`](https://github.com/garrytan/gbrain/blob/master/skills/skillify/SKILL.md) 获取完整的 10 项检查清单及其捕捉的反模式。

## 存储分层：将批量内容移出 git（v0.22.11）

当你的大脑超过 10 万个文件，机器批量生成的内容（推文、文章、会议记录）成为体积的主要驱动因素时，可以声明哪些目录属于 git，哪些只存在于数据库中。

```
# gbrain.yml at the brain repo root
storage:
  db_tracked:
    - people/
    - companies/
    - deals/
  db_only:
    - media/x/
    - media/articles/
    - meetings/transcripts/
```

`gbrain sync` 自动管理 `db_only` 路径的 `.gitignore`。`gbrain export --restore-only --repo .` 从数据库重新填充缺失文件（容器重启、全新克隆、误删时使用）。`gbrain storage status` 显示分层明细。

完整指南：[docs/storage-tiering.md](https://github.com/garrytan/gbrain/blob/master/docs/storage-tiering.md)。

## 数据接入

GBrain 内置了由 Agent 自动配置的集成方案。每个方案会告知 Agent 需要哪些凭证、如何验证，以及要注册哪些定时任务。

| 方案 | 依赖 | 功能说明 |
| --- | --- | --- |
| [公共隧道](https://github.com/garrytan/gbrain/blob/master/recipes/ngrok-tunnel.md) | — | MCP + 语音的固定 URL（ngrok Hobby $8/月） |
| [凭证网关](https://github.com/garrytan/gbrain/blob/master/recipes/credential-gateway.md) | — | Gmail + 日历访问 |
| [语音转大脑](https://github.com/garrytan/gbrain/blob/master/recipes/twilio-voice-brain.md) | ngrok-tunnel | 电话通话转为大脑页面（Twilio + OpenAI Realtime） |
| [邮件转大脑](https://github.com/garrytan/gbrain/blob/master/recipes/email-to-brain.md) | credential-gateway | Gmail 内容转为实体页面 |
| [X 转大脑](https://github.com/garrytan/gbrain/blob/master/recipes/x-to-brain.md) | — | Twitter 时间线 + 提及 + 删除 |
| [日历转大脑](https://github.com/garrytan/gbrain/blob/master/recipes/calendar-to-brain.md) | credential-gateway | Google 日历转为可搜索的日常页面 |
| [会议同步](https://github.com/garrytan/gbrain/blob/master/recipes/meeting-sync.md) | — | Circleback 会议记录转为含与会者的大脑页面 |
| [重启扫描](https://github.com/garrytan/gbrain/blob/master/recipes/restart-sweep.md) | OpenClaw + Telegram | 检测 OpenClaw 网关重启后丢失的 Telegram 消息 |

**数据研究方案**从邮件中提取结构化数据到追踪的大脑页面。内置方案涵盖投资者更新（MRR、ARR、跑道、员工人数）、费用追踪和公司指标。使用 `gbrain research init` 创建自定义方案。

运行 `gbrain integrations` 查看状态。

## GBrain + GStack

[GStack](https://github.com/garrytan/gstack) 是引擎，GBrain 是扩展模组。

- **[GStack](https://github.com/garrytan/gstack)** = 编码 skill（ship、review、QA、investigate、office-hours、retro）。70,000+ Stars，每天 3 万名开发者使用。当你的 Agent 在自身上编码时，使用的是 GStack。
- **GBrain** = 其他一切 skill（大脑运维、信号检测、数据摄入、信息丰富、定时任务、报告、身份）。当你的 Agent 记忆、思考和运营时，使用的是 GBrain。
- **`hosts/gbrain.ts`** = 桥接层。告知 GStack 的编码 skill 在编码前先检查大脑。

`gbrain init` 会检测 GStack 是否已安装并报告模组状态。如果 GStack 不存在，会告诉你如何获取。

## 架构

```
┌──────────────────┐    ┌───────────────┐    ┌──────────────────┐
│   Brain Repo     │    │    GBrain     │    │    AI Agent      │
│   (git)          │    │  (retrieval)  │    │  (read/write)    │
│                  │    │               │    │                  │
│  markdown files  │───>│  Postgres +   │<──>│  29 skills       │
│  = source of     │    │  pgvector     │    │  define HOW to   │
│    truth         │    │               │    │  use the brain   │
│                  │<───│  hybrid       │    │                  │
│  human can       │    │  search       │    │  RESOLVER.md     │
│  always read     │    │  (vector +    │    │  routes intent   │
│  & edit          │    │   keyword +   │    │  to skill        │
│                  │    │   RRF)        │    │                  │
└──────────────────┘    └───────────────┘    └──────────────────┘
```

仓库是事实记录系统，GBrain 是检索层，Agent 通过两者进行读写。人类永远优先……编辑任意 Markdown 文件后，`gbrain sync` 会自动检测变更。

多机器部署（跨机器精简客户端）和多工作树部署（每个工作树独立代码引擎 + 共享远程构件）参见 [`docs/architecture/topologies.md`](https://github.com/garrytan/gbrain/blob/master/docs/architecture/topologies.md)。

## 知识模型

每个页面都遵循"编译真相 + 时间线"模式：

```
---
type: concept
title: Do Things That Don't Scale
tags: [startups, growth, pg-essay]
---

Paul Graham's argument that startups should do unscalable things early on.
The key insight: the unscalable effort teaches you what users actually
want, which you can't learn any other way.

---

- 2013-07-01: Published on paulgraham.com
- 2024-11-15: Referenced in batch W25 kickoff talk
```

`---` 分隔符**以上**：**编译真相**——当前最优理解，当新证据改变全局时会被重写。分隔符**以下**：**时间线**——只追加的证据轨迹，永不编辑，只会新增。

## 知识图谱

页面不仅仅是文本。每次提及某个人、公司或概念，都会在结构化图谱中生成一个类型化链接。大脑会自我连线。

```
Write a meeting page mentioning Alice and Acme AI
  -> Auto-link extracts entity refs from content (zero LLM calls)
  -> Infers types: meeting page + person ref => \`attended\`
                   "CEO of X" pattern        => \`works_at\`
                   "invested in"             => \`invested_in\`
                   "advises", "advisor"      => \`advises\`
                   "founded", "co-founded"   => \`founded\`
  -> Reconciles stale links: edits remove links no longer in content
  -> Backlinks rank well-connected entities higher in search
```

```
gbrain graph-query people/alice --type attended --depth 2
# returns who Alice met with, transitively
```

图谱能回答向量搜索做不到的问题：“谁在 Acme AI 工作？”、“Bob 投资了什么？”、“找到 Alice 和 Carol 之间的联系”。用一条命令为已有大脑补全连线：

```
gbrain extract links --source db        # wire up the existing 29K pages
gbrain extract timeline --source db     # extract dated events from markdown timelines
```

然后就可以提图谱问题，或者观察搜索排名的提升。与 ripgrep-BM25、仅向量 RAG（同一嵌入器）和禁用图谱的 gbrain 进行并排基准测试：gbrain 在 240 页 Opus 生成的富文本语料库上达到 **P@5 49.1%、R@5 97.9%**，比禁用图谱的混合变体高出 **+31.4 个 P@5 百分点**。单独评估该贡献：v0.11→v0.12 在相同输入下将 gbrain 的 P@5 从 22.1% 提升至 49.1%，可见类型化链接提取质量至关重要。完整评分卡和可复现语料库见 [gbrain-evals](https://github.com/garrytan/gbrain-evals)。

## 搜索

混合搜索：向量 + 关键词 + RRF 融合 + 多查询扩展 + 四层去重。

```
Query
  -> Intent classifier (entity? temporal? event? general?)
  -> Multi-query expansion (Claude Haiku)
  -> Vector search (HNSW cosine) + Keyword search (tsvector)
  -> RRF fusion: score = sum(1/(60 + rank))
  -> Cosine re-scoring + compiled truth boost
  -> 4-layer dedup + compiled truth guarantee
  -> Results
```

单独关键词搜索会遗漏概念性匹配，单独向量搜索会遗漏精确短语，RRF 同时兼顾两者。搜索质量有基准测试且可复现：`gbrain eval --qrels queries.json` 可测量 P@k、Recall@k、MRR 和 nDCG@k。在部署配置变更前进行 A/B 测试。

## 为何有效：多策略协同

大脑不只有一个技巧。每个检索请求都会经过约 20 个确定性技术的叠加处理。没有任何一个是魔法；胜出来自于将它们堆叠在一起，使每一层都能覆盖其他层遗漏的内容。

```
Question
  │
  ├─ INGESTION (every put_page)
  │    ├─ Recursive markdown chunking (or semantic / LLM-guided)
  │    ├─ Embedding cache invalidation on edit
  │    └─ Idempotent imports (content-hash dedup)
  │
  ├─ GRAPH EXTRACTION (auto-link post-hook, zero LLM)
  │    ├─ Entity-ref regex (markdown links + bare slugs)
  │    ├─ Code-fence stripping (no false-positive slugs in code blocks)
  │    ├─ Typed inference cascade (FOUNDED → INVESTED → ADVISES → WORKS_AT)
  │    ├─ Page-role priors (partner-bio language → invested_in)
  │    ├─ Within-page dedup (same target collapses to one link)
  │    ├─ Stale-link reconciliation (edits remove dropped refs)
  │    └─ Multi-type link constraint (same person can works_at AND advises)
  │
  ├─ SEARCH PIPELINE (every query)
  │    ├─ Intent classifier (entity / temporal / event / general — auto-routes)
  │    ├─ Multi-query expansion (Haiku rephrases the question 3 ways)
  │    ├─ Vector search (HNSW cosine over OpenAI embeddings)
  │    ├─ Keyword search (Postgres tsvector + websearch_to_tsquery)
  │    ├─ Source-aware ranking (curated dirs outrank chat/daily swamp at SQL layer)
  │    ├─ Hard-exclude (test/ archive/ attachments/ .raw/ filtered before retrieval)
  │    ├─ Reciprocal Rank Fusion (score = sum 1/(60+rank) across both)
  │    ├─ Cosine re-scoring (re-rank chunks against actual query embedding)
  │    ├─ Compiled-truth boost (assessments outrank timeline noise)
  │    ├─ Backlink boost (well-connected entities rank higher)
  │    └─ Source-aware dedup (one CT chunk per page guaranteed)
  │
  ├─ GRAPH TRAVERSAL (relational queries)
  │    ├─ Recursive CTE with cycle prevention (visited-array check)
  │    ├─ Type-filtered edges (--type works_at, attended, etc.)
  │    ├─ Direction control (in / out / both)
  │    └─ Depth-capped (≤10 for remote MCP; DoS prevention)
  │
  └─ AGENT WORKFLOW (graph-confident hybrid)
       ├─ Graph-query first (high-precision typed answers)
       ├─ Grep fallback when graph returns nothing
       └─ Graph hits ranked first in top-K (better P@K and R@K)
```

BrainBench v1 语料库（240 页富文本，PR #188 前后）的端到端对比：

| 指标 | PR #188 前 | PR #188 后 | Δ |
| --- | --- | --- | --- |
| **Precision@5** | 39.2% | **44.7%** | **+5.4 pts** |
| **Recall@5** | 83.1% | **94.6%** | **+11.5 pts** |
| top-5 命中数 | 217 | 247 | **+30** |
| 仅图谱 F1（消融实验） | 57.8% (grep) | **86.6%** | **+28.8 pts** |

另加 5 项正交能力检查（身份识别、时序查询、1 万页规模下的性能、对格式错误输入的健壮性、MCP 操作契约）。全部通过。完整报告：[gbrain-evals](https://github.com/garrytan/gbrain-evals)。

要点：每种技术处理其他技术遗漏的那类输入。向量搜索遗漏精确 slug 引用，关键词搜索补足；关键词搜索遗漏概念性匹配，向量搜索补足；RRF 兼取两者之长。编译真相加权让评估高于时间线噪音。自动链接提取为图谱连线，让反向链接加权使联系丰富的实体排名更高。图谱遍历能回答单独搜索无法触达的问题。Agent 优先使用图谱以保证精度，回退到关键词搜索以保证召回率。**全部确定性，全部协同，全部可测量。**

## 语音

拨打一个电话号码，你的 AI 会接听。它知道是谁在打电话，从大脑中调取对方的完整上下文，像真正了解你世界的人一样回应。通话结束后，大脑中会出现一个含有会议记录、实体检测和交叉引用的页面。

[![Voice client connected](https://github.com/garrytan/gbrain/raw/master/docs/images/voice-client.png)](https://github.com/garrytan/gbrain/blob/master/docs/images/voice-client.png)

> [观看演示视频](https://x.com/garrytan/status/2043022208512172263)

语音方案随 GBrain 一同提供：[语音转大脑](https://github.com/garrytan/gbrain/blob/master/recipes/twilio-voice-brain.md)。WebRTC 在浏览器标签中即可运行，无需任何设置。真实电话号码是可选的。

## 引擎架构

```
CLI / MCP Server
     (thin wrappers, identical operations)
              |
      BrainEngine interface (pluggable)
              |
     +--------+--------+
     |                  |
PGLiteEngine       PostgresEngine
  (default)          (Supabase)
     |                  |
~/.gbrain/           Supabase Pro ($25/mo)
brain.pglite         Postgres + pgvector
embedded PG 17.5

     gbrain migrate --to supabase|pglite
         (bidirectional migration)
```

PGLite：内嵌式 Postgres，无需服务器，零配置。当你的大脑超出本地容量（1000+ 文件、多设备），`gbrain migrate --to supabase` 可迁移所有数据。

## 文件存储

大脑仓库会积累二进制文件。GBrain 提供三阶段迁移：

```
gbrain files mirror <dir>       # copy to cloud, local untouched
gbrain files redirect <dir>     # replace local with .redirect pointers
gbrain files clean <dir>        # remove pointers, cloud only
gbrain files restore <dir>      # download everything back (undo)
```

存储后端支持：S3 兼容（AWS、R2、MinIO）、Supabase Storage 或本地存储。

## 命令

```
SETUP（初始化）
  gbrain init [--supabase|--url]        创建大脑（默认使用 PGLite）
  gbrain migrate --to supabase|pglite   双向引擎迁移
  gbrain upgrade                        自更新并发现新功能

PAGES（页面）
  gbrain get <slug>                     读取页面（模糊 slug 匹配）
  gbrain put <slug> [< file.md]         写入/更新（自动版本控制）
  gbrain delete <slug>                  删除页面
  gbrain list [--type T] [--tag T]      带过滤条件的列表

SEARCH（搜索）
  gbrain search <query>                 关键词搜索（tsvector）
  gbrain query <question>              混合搜索（向量 + 关键词 + RRF）

IMPORT（导入）
  gbrain import <dir> [--no-embed] [--workers N]
                                        导入 Markdown（幂等）
  gbrain sync [--repo <path>] [--workers N]
                                        Git 到大脑的增量同步
                                        （>100 文件 diff 时 Postgres 自动 4 worker 并行）
  gbrain export [--dir ./out/]          导出为 Markdown

FILES（文件）
  gbrain files list|upload|sync|verify  文件存储操作

EMBEDDINGS（嵌入）
  gbrain embed [<slug>|--all|--stale]   生成/刷新嵌入向量

LINKS + GRAPH（链接与图谱）
  gbrain link|unlink|backlinks          交叉引用管理
  gbrain extract links|timeline|all     从现有页面批量补全
                                        (--source db|fs, --type, --since, --dry-run)
  gbrain graph-query <slug>             类型化遍历（--type T --depth N
                                        --direction in|out|both）

JOBS（Minions 任务）
  gbrain jobs submit <name> [--params JSON] [--follow]  提交后台任务
  gbrain jobs list [--status S] [--queue Q]             按过滤条件列出任务
  gbrain jobs get|cancel|retry|delete <id>              管理任务生命周期
  gbrain jobs prune [--older-than 30d]                  清理已完成/死亡任务
  gbrain jobs stats                                     任务健康仪表盘
  gbrain jobs smoke                                     单命令健康检查
  gbrain jobs work [--queue Q] [--concurrency N]        启动 worker 守护进程

SKILLS（技能，v0.19）
  gbrain skillify scaffold <name>       创建 5 个 stub 文件 + 幂等 resolver 行
  gbrain skillify check [path]          对 skill 执行 10 项审计
  gbrain skillpack list                 列出包中的 25 个精选 skill
  gbrain skillpack install <name>       将一个 skill 及其共享约定复制到目标
  gbrain skillpack install --all        安装完整精选包
  gbrain skillpack diff <name>          逐文件 diff：包 vs 目标工作区
  gbrain check-resolvable [--strict]    Resolver 审计（可达性、MECE、DRY、路由、归档、
                                        SKILLIFY_STUB）。接受 RESOLVER.md 或 AGENTS.md。
  gbrain routing-eval [--llm] [--json]  intent→skill 路由准确率（使用 fixture）

EVAL（评估）
  gbrain eval --qrels <path>            传统 IR 评估（P@k、R@k、MRR、nDCG@k 对照 ground truth）
  gbrain eval export [--since DUR]      以 NDJSON 流式导出捕获的 eval_candidates（BrainBench-Real）
  gbrain eval prune --older-than DUR    eval_candidates 的数据保留清理（需要时间窗口）
  gbrain eval replay --against FILE     对当前构建回放捕获的查询（Jaccard@k、top-1、延迟 Δ）
  gbrain eval longmemeval <dataset>     对 gbrain 混合检索运行公开 LongMemEval（v0.28.8）
                                        [--limit N] [--retrieval-only] [--keyword-only] [--expansion]
                                        [--top-k K] [--model M] [--output FILE]

ADMIN（管理）
  gbrain doctor [--json] [--fast]       健康检查（resolver、skill、DB、嵌入）
  gbrain doctor --fix [--dry-run]       自动修复 DRY 违规（将内联规则委托给约定）
  gbrain doctor --locks                 列出空闲 in-tx 后端（57014 诊断，仅 Postgres）
  gbrain stats                          大脑统计信息
  gbrain serve                          MCP server（stdio）
  gbrain serve --http [--port 3131]     带 OAuth 2.1 + 管理仪表盘的 HTTP MCP server
                                        [--token-ttl 3600] [--enable-dcr]
                                        [--public-url URL] [--log-full-params]
  gbrain auth create|list|revoke|test   传统 Bearer Token 管理
  gbrain auth register-client <name>    注册 OAuth 2.1 客户端
        --grant-types client_credentials,authorization_code
        --scopes "read write admin"
  gbrain auth revoke-client <client_id> 撤销 OAuth 2.1 客户端（级联清除
                                        活动 token + auth code，via FK CASCADE）
  # OAuth 2.1 客户端也可通过 /admin 仪表盘注册，
  # 或通过 oauthProvider.registerClientManual() 以编程方式注册（供 host-repo 包装器使用）。
  gbrain integrations                   集成方案仪表盘
  gbrain sources list|add|remove|...    多源大脑管理（v0.18）
                                        v0.28.2: --url <https://...> 注册联邦远程 git 仓库；
                                        clone 自动管理在 $GBRAIN_HOME/clones/<id>/ 下，
                                        同步时若丢失则自动重新克隆。也通过 MCP 暴露，
                                        供远程 agent 配置（whoami + sources_{add,list,remove,status}）。
  gbrain dream [--dry-run] [--phase N]  9 阶段维护周期（lint→backlinks→sync→synthesize
                                        →extract→patterns→recompute_emotional_weight→embed→orphans）。
                                        v0.23 新增 synthesize + patterns。v0.29 新增 emotional-weight
                                        重算。v0.30.2: synthesize 现可分块处理大型会议记录
                                        （配置: dream.synthesize.max_prompt_tokens, max_chunks_per_transcript）。
  gbrain dream --input <file>           临时会议记录综合（隐含 --phase synthesize）
  gbrain dream --date YYYY-MM-DD        综合单日内容；--from/--to 用于历史回填
  gbrain check-backlinks check|fix      反向链接强制检查
  gbrain lint [--fix]                   LLM 构件检测
  gbrain repair-jsonb [--dry-run]       修复 v0.12.0 双重编码的 JSONB（Postgres）
  gbrain orphans [--json] [--count]     查找零入站 wikilink 的孤立页面
  gbrain transcribe <audio>             转录音频（Groq Whisper）
  gbrain research init <name>           创建数据研究方案脚手架
  gbrain research list                  列出可用方案
```

运行 `gbrain --help` 查看完整参考文档。

## 起源故事

我在配置自己的 [OpenClaw](https://openclaw.ai/) Agent 时，开始建立一个 Markdown 大脑仓库。每人一页、每家公司一页，编译真相在上，时间线在下。不到一周：10,000+ 个文件、3,000+ 位联系人、13 年的日历数据、280+ 份会议记录、300+ 个记录的想法。

Agent 在我睡觉时运行。梦境周期扫描每一段对话，丰富缺失的实体信息，修复损坏的引用，整合记忆。我醒来时，大脑已经比我入睡时更聪明了。

这个仓库中的 skill 就是对这些模式的通用化提炼。原本需要 11 天手工搭建的东西，现在作为一个 30 分钟内即可安装的扩展模组提供给你。

## 文档

**面向 Agent：**

- **[skills/RESOLVER.md](https://github.com/garrytan/gbrain/blob/master/skills/RESOLVER.md)**... 从这里开始。Skill 调度器。
- [单独 Skill 文件](https://github.com/garrytan/gbrain/blob/master/skills)... 28 套独立指令集（25 套包含在精选的 `gbrain skillpack install` 包中）
- [GBRAIN\_SKILLPACK.md](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_SKILLPACK.md)... 历史参考架构
- [数据接入](https://github.com/garrytan/gbrain/blob/master/docs/integrations/README.md)... 集成方案与数据流
- [GBRAIN\_VERIFY.md](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_VERIFY.md)... 安装验证

**面向人类：**

- [GBRAIN\_RECOMMENDED\_SCHEMA.md](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_RECOMMENDED_SCHEMA.md)... 大脑仓库目录结构
- [精简载体，丰富技能](https://github.com/garrytan/gbrain/blob/master/docs/ethos/THIN_HARNESS_FAT_SKILLS.md)... 架构哲学
- [ENGINES.md](https://github.com/garrytan/gbrain/blob/master/docs/ENGINES.md)... 可插拔引擎接口

**参考资料：**

- [GBRAIN\_V0.md](https://github.com/garrytan/gbrain/blob/master/docs/GBRAIN_V0.md)... 完整产品规格
- [CHANGELOG.md](https://github.com/garrytan/gbrain/blob/master/CHANGELOG.md)... 版本历史

**基准测试：**

- [gbrain-evals](https://github.com/garrytan/gbrain-evals)... BrainBench——兄弟仓库，包含评估框架、语料库、评分卡和 4 种适配器的对比。依赖 gbrain，不随 gbrain 一并安装。

## 贡献指南

参见 [CONTRIBUTING.md](https://github.com/garrytan/gbrain/blob/master/CONTRIBUTING.md)。运行 `bun run test` 执行并行单元测试快速循环（Mac 开发机上约 85 秒，3700+ 个测试），或运行 `bun run verify` 执行推送前门控（隐私 + jsonb + 进度 + 测试隔离 + wasm + admin-build + 类型检查）。完整本地 CI 门控（gitleaks + 单元 + Docker 中所有 29 个 E2E 文件，与 GH Actions 运行相同的检查），使用 `bun run ci:local`……或在快速迭代时使用 `bun run ci:local:diff` 执行 diff 感知子集。

如果你在开发检索或任何搜索/嵌入/排名相关功能，请在 shell rc 中设置 `GBRAIN_CONTRIBUTOR_MODE=1`，并使用 `gbrain eval replay` 将你的变更与真实捕获查询的快照进行门控对比——开发循环详见 [`docs/eval-bench.md`](https://github.com/garrytan/gbrain/blob/master/docs/eval-bench.md)。捕获对生产用户**默认关闭**（不会意外积累数据）；环境变量是贡献者的选择加入机制。

欢迎 PR：新的数据丰富 API、性能优化、额外的引擎后端、遵循 `skills/skill-creator/SKILL.md` 合规标准的新 skill。

## 许可证

MIT
## 相关笔记

- [["llm-wiki"]]
- [[更新日志]]
- [[MCP]]
- [[多平台支持]]
- [[企业管理]]
- [[更新日志（1.x 及更早）]]
- [[更新日志（≤2.1.98）]]
- [[工作原理]]
