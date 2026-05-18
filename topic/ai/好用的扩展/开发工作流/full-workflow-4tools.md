---
title: 四工具完整工作流
description: GSD + OpenSpec + Superpowers + GStack 四工具联合工作流程，从想法到上线的完整流水线
tags:
  - ai
  - 扩展
  - 开发工作流
created: 2026-05-13
---

# 四工具完整工作流：GSD + OpenSpec + Superpowers + GStack

## 四者定位一句话

| 工具              | 本质                 | 解决什么问题                                                      |     |
| --------------- | ------------------ | ----------------------------------------------------------- | --- |
| **GSD**         | 上下文工程 + 多 Agent 编排 | 防止 context rot，管理跨会话状态，phase 级并行执行                          |     |
| **OpenSpec**    | Spec 驱动开发 (SDD)    | 每个 feature 有结构化制品（proposal/specs/design/tasks），人与 AI 先对齐再动手 |     |
| **Superpowers** | 工程纪律 skill 库       | TDD、subagent 执行、code review 流程自动触发                          |     |
| **GStack**      | 虚拟角色视角             | CEO/设计师/安全官/QA 各自审视，真实浏览器测试                                 |     |

---

## 协作关系分析

### 重叠与互补

```
阶段              GSD              OpenSpec         Superpowers      GStack
需求澄清          /gsd-new-project  /opsx:propose    brainstorming    /office-hours
Spec 制品         STATE.md等         proposal+specs   —                —  
架构规划          /gsd-discuss-phase design.md        writing-plans    /plan-eng-review
任务拆解          /gsd-plan-phase   tasks.md         writing-plans    —
并行执行          /gsd-execute-phase —               subagent-driven  /careful /freeze
代码审查          /gsd-verify-work  —                requesting-review /review /codex
QA              —                 —                verification     /qa /browse
安全审计          —                 —                —                /cso
发布             /gsd-ship         /opsx:archive    finishing-branch  /ship /land-and-deploy
复盘             /gsd-new-milestone —                —                /retro /learn
```

**真正互补，无冲突的组合：**

- **GSD 的 context 管理 + OpenSpec 的 spec 制品**：GSD 解决跨会话状态丢失，OpenSpec 解决每个 feature 的结构化对齐，两者在 `openspec/changes/` 目录和 `.planning/` 目录共存，互不干扰。
- **OpenSpec spec → Superpowers writing-plans**：`tasks.md` 可以直接作为 `writing-plans` 的输入，OpenSpec 负责"做什么"，Superpowers 负责"怎么做"的任务粒度拆解。
- **GSD 的并行执行 + Superpowers TDD**：`/gsd-execute-phase` 派发的子 Agent 天然可以遵守 `test-driven-development` skill（TDD 规则写在 CLAUDE.md 中自动生效）。
- **GStack /qa + GSD /gsd-verify-work**：两者互补，GSD verify 是计划符合性检查，GStack `/qa` 是真实浏览器行为验证。

**存在重叠，择一即可：**

- 需求澄清：GSD `/gsd-new-project` vs GStack `/office-hours` → **选 GSD**，它生成结构化 ROADMAP/REQUIREMENTS 文件，GStack 的追问是一次性对话
- 任务规划：OpenSpec `tasks.md` vs Superpowers `writing-plans` → **两者串联**，OpenSpec 定义 what，Superpowers 细化 how
- 代码审查：GSD `/gsd-verify-work` vs GStack `/review` → **都保留**，GSD 验计划符合性，GStack 做代码质量审查

---

## 完整工作流（8 阶段）

### 阶段 0：项目初始化（新项目/新 milestone）

**目标**：建立跨会话状态基线，防止 context rot。

| 步骤 | 工具 | 命令 | 产出 |
|------|------|------|------|
| 1 | GSD | `/gsd-new-project` | `PROJECT.md` `REQUIREMENTS.md` `ROADMAP.md` `STATE.md` |
| 2 | GSD | `/gsd-map-codebase`（已有代码时） | 分析现有架构，写入 context |

**仅执行一次，后续 milestone 用 `/gsd-new-milestone` 开始。**

---

### 阶段 1：Ideation（需求对齐）

**目标**：在写 spec 前把真正的问题搞清楚。

| 步骤  | 工具          | 命令/Skill           | 作用                  |
| --- | ----------- | ------------------ | ------------------- |
| 1   | GStack      | `/office-hours`    | 6 个逼问问题，挑战需求前提      |
| 2   | GStack      | `/plan-ceo-review` | 产品视角挑战范围（可选，大功能时用）  |
| 3   | Superpowers | `brainstorming`    | Socratic 式追问细化，自动触发 |

**产出**：清晰的 feature 意图，喂给下一阶段。

---

### 阶段 2：Spec 制品生成

**目标**：人与 AI 在动手前对齐，每个 feature 有结构化文档。

| 步骤 | 工具 | 命令 | 产出 |
|------|------|------|------|
| 1 | OpenSpec | `/opsx:propose <feature>` | `openspec/changes/<feature>/proposal.md` `specs/` `design.md` `tasks.md` |
| 2 | GSD | `/gsd-discuss-phase N` | 补充灰色地带决策（API 形状、错误处理、数据结构），写入 `CONTEXT.md` |

**两者不冲突**：OpenSpec 制品放 `openspec/` 目录，GSD 状态放 `.planning/` 目录，可共存。

---

### 阶段 3：架构规划

**目标**：技术方案落地，形成可执行计划。

| 步骤  | 工具          | 命令/Skill              | 作用                            |     |
| --- | ----------- | --------------------- | ----------------------------- | --- |
| 1   | Superpowers | `using-git-worktrees` | 创建隔离 worktree 分支              |     |
| 2   | GSD         | `/gsd-plan-phase N`   | Research + 生成任务计划 + 自验证循环     |     |
| 3   | Superpowers | `writing-plans`       | 将计划细化为 2-5 分钟粒度任务（含文件路径、验证步骤） |     |
| 4   | GStack      | `/plan-eng-review`    | 数据流 ASCII 图、状态机、错误路径、测试矩阵     |     |
| 5   | GStack      | `/plan-design-review` | UI 维度 0-10 评分（仅前端任务）          |     |

**串联关系**：GSD 生成的 `tasks.md` → Superpowers `writing-plans` 进一步细化 → GStack review 补充技术视角。

---

### 阶段 4：实现（并行执行）

**目标**：按计划自主执行，main context 保持低占用。

| 步骤 | 工具 | 命令/Skill | 作用 |
|------|------|-----------|------|
| 1 | GSD | `/gsd-execute-phase N` | 并行波次执行，每个子 Agent 独立 200k context，每任务原子 commit |
| 2 | Superpowers | `subagent-driven-development` | 每任务双阶段 review（spec 符合性 + 代码质量），与 GSD 执行互补 |
| 3 | Superpowers | `test-driven-development` | 通过 CLAUDE.md 全局生效，子 Agent 自动遵守 RED-GREEN-REFACTOR |
| 4 | GStack | `/careful` `/freeze` `/guard` | 破坏性命令防护，限制编辑范围 |

**权限**：`bypassPermissions` 模式，在 worktree 隔离环境中运行。

**GSD 与 Superpowers 执行的选择**：
- 大型 phase（多文件、多模块）→ 优先 `/gsd-execute-phase`（更强的上下文隔离）
- 单个任务 / 需要细粒度 review → 优先 `subagent-driven-development`

---

### 阶段 5：代码审查

**目标**：多视角发现问题，人工批准关键决策。

| 步骤  | 工具          | 命令/Skill                         | 作用                                 |
| --- | ----------- | -------------------------------- | ---------------------------------- |
| 1   | GSD         | `/gsd-verify-work N`             | 计划符合性验证，失败自动生成 fix plan            |
| 2   | Superpowers | `requesting-code-review`         | 按严重程度分类报告                          |
| 3   | Superpowers | `receiving-code-review`          | 标准化处理 review 反馈                    |
| 4   | GStack      | `/review`                        | Staff Engineer 视角，自动修复明显问题         |
| 5   | GStack      | `/codex`                         | OpenAI Codex 独立 review（可选，重要 PR 用） |
| 6   | Superpowers | `verification-before-completion` | 确认实际修复而非仅声称修复                      |
|     |             |                                  |                                    |
|     |             |                                  |                                    |
|     |             |                                  |                                    |
|     |             |                                  |                                    |

---

### 阶段 6：QA & 测试

**目标**：真实验证行为，E2E 覆盖，生成回归测试。

| 步骤  | 工具          | 命令/Skill                  | 作用                                   |
| --- | ----------- | ------------------------- | ------------------------------------ |
| 1   | Superpowers | `test-driven-development` | 单元/集成测试覆盖（已在实现阶段完成大部分）               |
| 2   | GStack      | `/qa`                     | 真实 Chromium E2E，找到 bug → 修复 → 生成回归测试 |
| 3   | GStack      | `/qa-only`                | 纯报告模式，不修改代码（用于阶段性评估）                 |
| 4   | GStack      | `/browse`                 | Agent 获取浏览器视觉能力                      |
| 5   | Superpowers | `systematic-debugging`    | 4 阶段根因分析（bug 修复时触发）                  |

**分工**：Superpowers 负责代码层测试，GStack `/qa` 负责浏览器行为层测试。

---

### 阶段 7：安全审计

**目标**：Ship 前发现安全漏洞，适合每 Sprint 末执行。

| 步骤  | 工具     | 命令     | 作用                                                  |
| --- | ------ | ------ | --------------------------------------------------- |
| 1   | GStack | `/cso` | OWASP Top 10 + STRIDE 威胁建模，8/10+ 置信度门控，含 17 个误报排除规则 |
|     |        |        |                                                     |
|     |        |        |                                                     |

**对 WebUACAD 的重点**：OAuth2/BFF 端点、GM/T 签名流程、Qdrant 向量库访问控制。

---

### 阶段 8：发布

**目标**：从验证到生产的全自动化。

| 步骤  | 工具          | 命令/Skill                         | 作用                                              |
| --- | ----------- | -------------------------------- | ----------------------------------------------- |
| 1   | OpenSpec    | `/opsx:archive`                  | 归档 feature spec 制品到 `openspec/changes/archive/` |
| 2   | Superpowers | `finishing-a-development-branch` | 验证测试，提供 merge/PR/keep/discard 选项，清理 worktree    |
| 3   | GStack      | `/ship`                          | 同步 main，跑测试，开 PR，自动触发 `/document-release`       |
| 4   | GSD         | `/gsd-ship N`                    | 从已验证工作创建 PR（GSD 视角的 ship）                       |
| 5   | GStack      | `/land-and-deploy`               | 合并 PR，等待 CI，验证生产健康                              |
| 6   | GStack      | `/canary`                        | 部署后监控，控制台错误/性能回归/页面故障                           |

**GStack `/ship` 与 GSD `/gsd-ship` 选其一**，取决于哪个工具管理了本次 phase 的执行。

---

### 阶段 9：复盘与记忆沉淀

**目标**：积累项目学习，为下一 milestone 提供上下文。

| 步骤 | 工具 | 命令/Skill | 作用 |
|------|------|-----------|------|
| 1 | GSD | `/gsd-complete-milestone` | 归档 milestone，打 tag，清理状态 |
| 2 | GSD | `/gsd-new-milestone` | 开启下一版本，继承现有 context |
| 3 | GStack | `/retro` | 按人统计，发布条纹，测试健康趋势 |
| 4 | GStack | `/learn` | 管理跨会话记忆，项目模式/陷阱/偏好 |
| 5 | GStack | `/benchmark` | Core Web Vitals 基线对比 |

---

### Debug Loop（随时触发）

| 工具 | 命令/Skill | 作用 |
|------|-----------|------|
| Superpowers | `systematic-debugging` | 4 阶段根因，Iron Law：先调查再修复 |
| GStack | `/investigate` | 同样方法论，自动 freeze 到问题模块 |
| GStack | `/freeze` `/guard` | 防止调试时意外改动无关代码 |
| GSD | `/gsd-verify-work` | 修复后重新验证计划符合性 |

---

## 快速参考：阶段 → 主工具

```
0. 项目初始化    → GSD /gsd-new-project
1. Ideation      → GStack /office-hours + Superpowers brainstorming
2. Spec 制品     → OpenSpec /opsx:propose + GSD /gsd-discuss-phase
3. 架构规划      → GSD /gsd-plan-phase + Superpowers writing-plans + GStack /plan-eng-review
4. 实现          → GSD /gsd-execute-phase + Superpowers subagent-driven + TDD
5. 代码审查      → GSD /gsd-verify-work + Superpowers review + GStack /review
6. QA            → GStack /qa + Superpowers TDD
7. 安全审计      → GStack /cso
8. 发布          → OpenSpec /opsx:archive + Superpowers finishing + GStack /ship + /canary
9. 复盘          → GSD /gsd-complete-milestone + GStack /retro + /learn
```

---

## 场景演示：从想法到上线

> [!tip] 前置阅读
> 本文假设你已分别安装并了解各工具的基本操作。如果还没有，先读 [[Superpowers 使用手册与最佳实践]] 和 [[gstack 使用手册与最佳实践]]。

以下演示 [[Superpowers]] + [[gstack]] 两工具的核心流程。对于大型项目，在此基础前叠加 GSD 的上下文管理和 OpenSpec 的 spec 制品即可。

**场景设定：** 你有一个 Next.js 的 Todo 应用（Prisma + PostgreSQL），想加一个功能——用户可以把待办事项导出为 Markdown 文件。

### 第 1 站：产品挑战（GStack）

先用 [[gstack]] 的 `/office-hours` 从产品角度审视这个想法：

```
你: /office-hours
你: 我想给 Todo 应用加一个 Markdown 导出功能

Claude: 让我先理解痛点。你目前是怎么把待办事项分享给别人的？
        有没有具体的场景——不是假设的，是你自己遇到过的？
```

> [!important] 为什么从 [[gstack]] 开始而不是 [[Superpowers]]？
> `/brainstorming` 擅长打磨**技术设计**，但不会挑战你的**产品前提**。先让 `/office-hours` 验证"这个功能值不值得做"，再让 `/brainstorming` 决定"怎么做"——避免精心设计了一个没人要的功能。

### 第 2 站：多角色审查（GStack）

想法通过产品验证后，用 `/autoplan` 一键跑完 CEO → 设计 → 工程三轮审查：

```
你: /autoplan

Claude: [自动运行 CEO 审查 → 发现"导出"可以扩展为"多格式分享"]
        [自动运行设计审查 → 确认 Markdown 格式优先]
        [自动运行工程审查 → ASCII 架构图、数据流、测试矩阵]
        需要你确认的品味决策：
        1. 是否支持 PDF 导出（当前 Sprint 还是后续）？
        2. 导出按钮放在列表页还是详情页？
```

> [!tip] autoplan 的"自动决策"原则
> `/autoplan` 内置 6 条决策原则，对明确的方向自动推进，只把"品味"层面的选择呈交给你。这比逐一运行三个审查命令节省大量时间。

### 第 3 站：设计打磨（Superpowers）

审查产出的设计文档自动传递给 [[Superpowers]] 的 `brainstorming`，做**技术层面的精细打磨**：

```
Claude: 我读了工程审查的输出。有几个技术决策需要确认：
        1. 导出是实时生成还是异步任务？
           - 实时生成：简单，但列表超 1000 条时可能超时
           - 异步任务：需要引入队列，但支持大规模导出
```

**产出：** 最终设计文档，包含所有技术决策和约束。

### 第 4 站：隔离工作区（Superpowers）

确认设计后，[[Superpowers]] 自动触发 `using-git-worktrees`：

```
Claude: 创建隔离工作区 feature/markdown-export
        分支基于 main，测试基线验证通过：42 tests, 0 failures
```

> [!note] 为什么不用 [[gstack]] 的 freeze？
> `/freeze` 是调试时的应急手段——临时限制编辑范围。`worktree` 是正式开发的结构化隔离——独立分支、独立目录、独立测试基线。**开发用 worktree，调试用 freeze。**

### 第 5 站：任务拆解（Superpowers）

`/writing-plans` 将设计文档拆成 2-5 分钟的小任务：

```
Claude: 实施计划已生成（8 个任务）：

        Task 1: 添加 ExportFormat 枚举到 schema.prisma
        验证: npx prisma validate 通过

        Task 2: 编写 exportService.test.ts（RED 阶段）
        验证: 测试按预期失败

        Task 3: 实现 exportService.ts（GREEN 阶段）
        验证: 所有测试通过
        ...
```

每个任务都有精确的文件路径、完整代码和验证步骤——"清晰到连初级工程师都能跟着做"。

### 第 6 站：TDD 循环（Superpowers）

这是 [[Superpowers]] 的核心纪律。以 Task 2 为例：

```
Claude: [RED] 编写 exportService.test.ts
        测试用例：空列表、单条、多条、特殊字符、超长列表
        运行测试 → 5 failed, 0 passed ✓ (预期失败)

        [GREEN] 实现 exportService.ts
        运行测试 → 0 failed, 5 passed ✓

        [REFACTOR] 提取格式化逻辑为独立函数
        运行测试 → 0 failed, 5 passed ✓ (行为不变)
```

> [!warning] Superpowers 的强制规则
> 如果 Agent 发现在测试之前写了代码，它**会删除代码**。这不是建议，是纪律。

### 第 7 站：代码审查（Superpowers + GStack）

[[Superpowers]] 的 `/requesting-code-review` 在每个任务之间自动运行：

```
Claude: [审查 Task 3]
        ✅ exportService.ts 符合设计规格
        ⚠️ HIGH: 文件流未关闭，大文件可能内存泄漏
        → 已自动修复
```

**全部任务完成后**，再用 [[gstack]] 的 `/review` 做一轮 Staff Engineer 级别的全局审查，并可选 `/codex` 获取 OpenAI 模型的第二意见：

```
你: /review
Claude: [AUTO-FIXED] 3 个问题
        [ASK] Task 5 的竞态条件 → 你确认修复方案

你: /codex
Claude: OpenAI Codex 审查完成
        与 Claude 审查重叠: 2/5 发现一致
        Codex 独有发现: 未处理并发导出限制
```

> [!tip] 双模型审查的价值
> `/review`（Claude）和 `/codex`（OpenAI）各自有不同的盲区。两者都跑一遍，重叠的发现更可信，独有的发现值得特别关注。

### 第 8 站：浏览器 QA（GStack）

代码审查通过后，切换回 [[gstack]] 做真实环境验证：

```
你: /qa https://staging.myapp.com
Claude: [打开真实 Chromium 浏览器]
        [点击"导出"按钮] → 下载了 export.md
        [打开导出文件] → 发现 checkbox 状态未保留
        [修复 bug] → [编写回归测试] → [验证修复]
        Bug 已修复并验证 ✓
```

> [!important] 为什么 QA 用 [[gstack]] 而不是 [[Superpowers]]？
> [[Superpowers]] 的审查基于**代码静态分析**——读代码找问题。[[gstack]] 的 `/qa` 基于**真实浏览器操作**——点击、截图、看实际效果。两者互补，不能互相替代。

### 第 9 站：发布上线（GStack）

最后三个命令完成发布闭环：

```
你: /cso
Claude: OWASP Top 10 + STRIDE 威胁模型审查完成
        0 个 Critical, 1 个 Medium (建议添加导出频率限制)

你: /ship
Claude: 同步 main → 运行测试 (42 → 51, +9 新测试)
        覆盖率审计: 87% → 92%
        PR 已创建: github.com/you/app/pull/42

你: /land-and-deploy
Claude: PR 已合并 → CI 通过 → 部署完成 → 生产环境健康 ✓
```

---

## 选修路线：什么时候可以跳过

上面的完整流程适合**重要功能**。实际工作中，不是每个改动都需要走全流程：

| 改动类型 | 推荐流程 | 跳过什么 |
|---------|---------|---------|
| **拼写修复 / 配置调整** | 直接改 → `/ship` | 跳过全部 |
| **小 bug 修复** | `/investigate` → 修复 → `/review` → `/ship` | 跳过设计阶段 |
| **新功能（小）** | `/brainstorming` → worktree → TDD → `/review` → `/ship` | 跳过 `/office-hours` 和 `/autoplan` |
| **新功能（大）** | 完整 9 站流程 | 不跳过 |
| **重构** | `/brainstorming` → worktree → TDD → `/review` → `/ship` | 跳过产品阶段和 QA |

> [!note] 一条经验法则
> 如果你的改动**改变了用户能看到的东西**，跑 `/qa`；如果**只改变了内部实现**，`/review` 通常够用。

---

## 常见误区

### 误区 1："我先想好再告诉 Agent 怎么做"

❌ 你一个人想方案，Agent 只管执行 → 浪费了 `/office-hours` 和 `/brainstorming` 的质疑能力

✅ 给 Agent 一个粗略方向，让它通过提问帮你发现盲点

### 误区 2："两个工具的审查是重复的"

❌ `/requesting-code-review`（[[Superpowers]]）和 `/review`（[[gstack]]）做的是同一件事

✅ [[Superpowers]] 审查关注**任务粒度**（每个小任务是否正确），[[gstack]] 审查关注**全局质量**（跨任务的一致性、生产环境风险）。先细后粗，不重复。

### 误区 3："TDD 太慢了，先写完代码再补测试"

❌ 跳过 TDD 直接写代码，事后补测试

✅ [[Superpowers]] 会**删除先于测试编写的代码**。这不是惩罚，是因为先写测试能帮你在写代码前想清楚接口设计。

### 误区 4："我用 GStack 的 brainstorm 替代 Superpowers 的"

❌ [[gstack]] 没有独立的 brainstorming skill，它的 `/office-hours` 做的是**产品验证**而非**技术设计**

✅ 两者互补：`/office-hours` 问"要不要做"，`/brainstorming` 问"怎么做"

---

## 相关笔记

- [[Superpowers 使用手册与最佳实践]] — [[Superpowers]] 完整教学
- [[gstack 使用手册与最佳实践]] — [[gstack]] 完整教学
- [[Superpowers 实战：用 TDD 工作流构建生产功能]] — TDD 深度实战

---

## 针对 WebUACAD 的 CLAUDE.md 配置

```markdown
## Workflow tools
- GSD: context management, phase execution (bypassPermissions in worktree)
- OpenSpec: feature spec artifacts in openspec/changes/
- Superpowers: TDD enforcement, code review discipline (auto-triggered)
- GStack: /qa for React E2E, /cso for security audits, /review for code quality

## Testing
- Unit/integration: mvn test (Spring Boot)
- Frontend unit: npm test
- E2E: npx playwright test (run after UI changes, trigger /qa)

## Security checkpoints
- Run /cso before each Sprint release
- Focus: OAuth2/BFF endpoints, GM/T signing flows, Qdrant access control

## Context management
- Always run /gsd-map-codebase when returning after >1 week
- OpenSpec artifacts: openspec/changes/ (per-feature)
- GSD state: .planning/ (phase-level)

## Permissions
- Use bypassPermissions in git worktree isolation
- Use /guard for production-adjacent work
```

---

## 工具冲突处理原则

1. **GSD vs Superpowers 执行**：大 phase 用 GSD（context 隔离更强），单任务精细控制用 Superpowers subagent。
2. **GSD /gsd-ship vs GStack /ship**：谁执行了这个 phase 谁负责 ship，不要同时跑。
3. **OpenSpec tasks.md vs Superpowers writing-plans**：OpenSpec 定义 what（业务任务），Superpowers 细化 how（实现步骤），串联不替代。
4. **GStack /investigate vs Superpowers systematic-debugging**：两者方法论相似，选一个即可，不需要叠加。
