---
title: GSD 命令参考
tags:
  - ai/工具
  - ai/claude-code
  - 开发工作流
  - 命令参考
aliases:
  - GSD 命令
source: https://github.com/gsd-build/get-shit-done/blob/main/docs/COMMANDS.md
---

# GSD 命令参考

> [!note] 命令语法
> - **[[Claude Code]] / [[Copilot]] / OpenCode / Kilo：** `/gsd-command-name [args]`（连字符形式）
> - **Gemini CLI：** `/gsd:command-name [args]`（冒号形式 — Gemini 在 `gsd:` 命名空间下管理命令）
> - **Codex：** `$gsd-command-name [args]`
>
> 连字符和冒号形式是*同一命令在不同运行时中的拼写方式*。无论你使用哪种运行时，安装程序都会将正确的形式写入该运行时的命令目录。

---

## 命名空间元技能

v1.40 中内置了六个命名空间路由器作为第一阶段入口。它们保持了较低的技能列表 token 开销（6 个路由器约 ~120 tokens，而扁平的 86 项技能列表约 ~2,150 tokens），同时完整功能表面仍可直接调用。模型选择一个命名空间，然后路由到具体的子技能。参见 [#2792](https://github.com/gsd-build/get-shit-done/issues/2792)。

| 命令 | 路由到 |
| --- | --- |
| `/gsd-workflow` | Phase 流水线 — discuss / plan / execute / verify / phase / progress |
| `/gsd-project` | 项目生命周期 — milestones、audits、summary |
| `/gsd-quality` | 质量门控 — code review、debug、audit、security、eval、ui |
| `/gsd-context` | 代码库智能 — map、graphify、docs、learnings |
| `/gsd-manage` | 管理 — config、workspace、workstreams、thread、update、ship、inbox |
| `/gsd-ideate` | 探索与捕获 — explore、sketch、spike、spec、capture |

命名空间技能是**叠加式**的 — 每个现有的具体命令（例如 `/gsd-plan-phase`、`/gsd-code-review --fix`）仍可直接调用。

---

## 核心工作流命令

### /gsd-new-project

通过深度上下文收集初始化新项目。

| Flag | 说明 |
| --- | --- |
| `--auto @file.md` | 从文档自动提取，跳过交互式问答 |

**前置条件：** 不存在 `.planning/PROJECT.md` **产出：** `PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md`、`config.json`、`research/`、`CLAUDE.md`

```
/gsd-new-project                    # Interactive mode
/gsd-new-project --auto @prd.md     # Auto-extract from PRD
```

---

### /gsd-workspace

管理 GSD 工作区 — 创建、列出或移除隔离的工作区环境，包含仓库副本和独立的 `.planning/` 目录。

| Flag | 说明 |
| --- | --- |
| `--new` | 创建新工作区（与 `--name`、`--repos` 等配合使用） |
| `--list` | 列出活跃的 GSD 工作区及其状态 |
| `--remove <name>` | 移除工作区并清理 git worktree |
| `--name <name>` | 工作区名称（与 `--new` 配合使用） |
| `--repos repo1,repo2` | 逗号分隔的仓库路径或名称（与 `--new` 配合使用） |
| `--path /target` | 目标目录（默认：`~/gsd-workspaces/<name>`） |
| `--strategy worktree\|clone` | 复制策略（默认：`worktree`） |
| `--branch <name>` | 检出的分支（默认：`workspace/<name>`） |
| `--auto` | 跳过交互式问答 |

**使用场景：**

- 多仓库：在仓库子集上工作，拥有隔离的 GSD 状态
- 功能隔离：`--repos .` 创建当前仓库的 worktree

**产出：** `WORKSPACE.md`、`.planning/`、仓库副本（worktree 或 clone）

```
/gsd-workspace --new --name feature-b --repos hr-ui,ZeymoAPI
/gsd-workspace --new --name feature-b --repos . --strategy worktree  # Same-repo isolation
/gsd-workspace --list
/gsd-workspace --remove feature-b
```

---

### /gsd-discuss-phase

在规划前通过自适应提问收集 phase 上下文。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号（默认为当前 phase） |

| Flag | 说明 |
| --- | --- |
| `--all` | 跳过区域选择 — 交互式讨论所有灰色地带（不自动推进） |
| `--auto` | 为所有问题自动选择推荐默认值 |
| `--batch` | 批量汇集问题，而非逐个提问 |
| `--analyze` | 在讨论过程中加入权衡分析 |
| `--power` | 通过准备好的答案文件进行批量作答 |
| `--assumptions` | 展示 Claude 关于该 phase 的实现假设，无需交互式会话 |

**前置条件：** `.planning/ROADMAP.md` 存在 **产出：** `{phase}-CONTEXT.md`、`{phase}-DISCUSSION-LOG.md`（审计追踪）

```
/gsd-discuss-phase 1                # Interactive discussion for phase 1
/gsd-discuss-phase 1 --all          # Discuss all gray areas without selection step
/gsd-discuss-phase 3 --auto         # Auto-select defaults for phase 3
/gsd-discuss-phase --batch          # Batch mode for current phase
/gsd-discuss-phase 2 --analyze      # Discussion with trade-off analysis
/gsd-discuss-phase 1 --power        # Bulk answers from file
/gsd-discuss-phase 3 --assumptions  # Surface Claude's assumptions before planning
```

---

### /gsd-ui-phase

为前端 phase 生成 UI 设计契约。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号（默认为当前 phase） |

**前置条件：** `.planning/ROADMAP.md` 存在，phase 包含前端/UI 工作 **产出：** `{phase}-UI-SPEC.md`

```
/gsd-ui-phase 2                     # Design contract for phase 2
```

---

### /gsd-plan-phase

对 phase 进行研究、规划和验证。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号（默认为下一个未规划的 phase） |

| Flag | 说明 |
| --- | --- |
| `--auto` | 跳过交互式确认 |
| `--research` | 即使 RESEARCH.md 已存在也强制重新研究 |
| `--skip-research` | 跳过领域研究步骤 |
| `--research-phase <N>` | 纯研究模式：为 phase `<N>` 启动 researcher，写入 RESEARCH.md，在 planner 前退出。替代已删除的 `gsd-research-phase` 独立命令 (#3042)。 |
| `--view` | 纯研究修饰符：与 `--research-phase` 一起使用时，将现有 RESEARCH.md 输出到 stdout 并退出（不启动子进程）。 |
| `--gaps` | 缺口闭合模式（读取 VERIFICATION.md，跳过研究） |
| `--skip-verify` | 跳过 plan checker 验证循环 |
| `--prd <file>` | 使用 PRD 文件替代 discuss-phase 获取上下文 |
| `--ingest <path-or-glob>` | 使用 ADR 文件替代 discuss-phase 进行上下文综合 |
| `--ingest-format <auto\|nygard\|madr\|narrative>` | `--ingest` 的可选 ADR 解析格式覆盖 |
| `--reviews` | 使用来自 REVIEWS.md 的跨 AI review 反馈重新规划 |
| `--validate` | 在规划开始前运行状态验证 |
| `--bounce` | 规划后运行外部 plan bounce 验证（使用 `workflow.plan_bounce_script`） |
| `--skip-bounce` | 即使配置中启用了 bounce 也跳过 |

**前置条件：** `.planning/ROADMAP.md` 存在 **产出：** `{phase}-RESEARCH.md`、`{phase}-{N}-PLAN.md`、`{phase}-VALIDATION.md`

**纯研究模式（`--research-phase <N>`）：**

- 无修饰符：如果 RESEARCH.md 已存在，提示 `update / view / skip`。
- 使用 `--research`：强制刷新 — 无条件重新启动 researcher，不提示。
- 使用 `--view`：将现有 RESEARCH.md 输出到 stdout，不启动子进程。RESEARCH.md 不存在时报错。

**包合法性门控 (v1.42.1)：** 当 researcher 推荐外部包时，会对每个包运行 `slopcheck install <pkg> --json`，并在 RESEARCH.md 中写入 `## Package Legitimacy Audit` 表格，记录 Registry、Age、Downloads、Source Repo 和 slopcheck 判定结果。判定结果：

- `[SLOP]` — 包被从 RESEARCH.md 中完全移除；永远不会到达 planner
- `[SUS]` — 包被标记；planner 在安装任务前插入 `checkpoint:human-verify`
- `[OK]` — 包通过审批；不添加 checkpoint

通过 WebSearch 获取的包标记为 `[ASSUMED]`（非 `[VERIFIED]`），与 `[SUS]` 同等对待 — 安装前会有一个人工 checkpoint。如果无法安装 `slopcheck`，每个推荐的包都标记为 `[ASSUMED]` 并加门控。

完整的 checkpoint 格式、判定表和故障排除请参阅 [Package Legitimacy Gate in the User Guide](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md#package-legitimacy-gate-v1421)。

```
/gsd-plan-phase 1                              # Research + plan + verify phase 1
/gsd-plan-phase 3 --skip-research              # Plan without research (familiar domain)
/gsd-plan-phase --auto                         # Non-interactive planning
/gsd-plan-phase 2 --validate                   # Validate state before planning
/gsd-plan-phase 1 --bounce                     # Plan + external bounce validation
/gsd-plan-phase 2 --ingest docs/adr/0010.md   # ADR express path for context synthesis
/gsd-plan-phase 2 --ingest 'docs/adr/00*.md' --ingest-format auto
/gsd-plan-phase --research-phase 4             # Research only on phase 4 (prompts if RESEARCH.md exists)
/gsd-plan-phase --research-phase 4 --view      # Print existing RESEARCH.md, no spawn
/gsd-plan-phase --research-phase 4 --research  # Force-refresh research, no prompt
```

---

### /gsd-plan-review-convergence

跨 AI plan 收敛循环 — 使用 review 反馈重新规划，直到没有 HIGH 级别问题。运行 `plan-phase → review → replan → re-review` 循环（默认最多 3 轮）。启动隔离的 agent 进行规划和 review；编排器负责循环控制、HIGH 问题计数、停滞检测和升级。

| 参数 / Flag | 必填 | 说明 |
| --- | --- | --- |
| `N` | **是** | 要规划和 review 的 phase 编号 |
| `--codex` / `--gemini` / `--claude` / `--opencode` | 否 | 单 reviewer 选择 |
| `--all` | 否 | 并行运行所有已配置的 reviewer |
| `--max-cycles N` | 否 | 覆盖循环上限（默认 3） |

**退出行为：** 当 HIGH 计数降为零时循环退出。停滞检测在 HIGH 计数跨轮次未下降时发出警告。升级门控在达到 `--max-cycles` 但仍有未解决的 HIGH 问题时，询问用户是继续还是手动 review。

```
/gsd-plan-review-convergence 3                    # Default reviewers, 3 cycles
/gsd-plan-review-convergence 3 --codex            # Codex-only review
/gsd-plan-review-convergence 3 --all --max-cycles 5
```

---

### /gsd-ultraplan-phase

**\[BETA\]** 将 plan phase 卸载到 Claude Code 的 ultraplan 云端；在浏览器中 review 并导回。plan 在远程起草，终端保持空闲；在浏览器中查看内联评论，然后通过 `/gsd-import` 将最终 plan 导入 `.planning/`。

| Flag | 必填 | 说明 |
| --- | --- | --- |
| `N` | **是** | 要远程规划的 phase 编号 |

**隔离性：** 有意与 `/gsd-plan-phase` 分离，确保上游 ultraplan 变更不会影响核心规划流水线。

```
/gsd-ultraplan-phase 4                  # Offload planning for phase 4
```

---

### /gsd-execute-phase

以 wave 并行方式执行 phase 中的所有 plan，或运行特定 wave。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | **是** | 要执行的 phase 编号 |
| `--wave N` | 否 | 仅执行该 phase 中的 Wave `N` |
| `--validate` | 否 | 执行开始前运行状态验证 |
| `--cross-ai` | 否 | 将执行委托给外部 AI CLI（使用 `workflow.cross_ai_command`） |
| `--no-cross-ai` | 否 | 即使配置中启用了 cross-AI 也强制本地执行 |

**前置条件：** Phase 有 PLAN.md 文件 **产出：** 每个 plan 的 `{phase}-{N}-SUMMARY.md`、git commit，以及 phase 完全完成时的 `{phase}-VERIFICATION.md`

**包安装失败 (v1.42.1)：** 如果 plan 的安装步骤失败，executor 会显示 `checkpoint:human-verify` 并停止。不会自动安装名称类似的替代包。这是有意为之 — 静默替换包名是 slopsquatting 传播的方式。在包的 registry 页面验证后，再回应 checkpoint。

```
/gsd-execute-phase 1                # Execute phase 1
/gsd-execute-phase 1 --wave 2       # Execute only Wave 2
/gsd-execute-phase 1 --validate     # Validate state before execution
/gsd-execute-phase 2 --cross-ai     # Delegate phase 2 to external AI CLI
```

---

### /gsd-verify-work

带自动诊断的用户验收测试。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号（默认为最后执行的 phase） |

**前置条件：** Phase 已执行 **产出：** `{phase}-UAT.md`，发现问题则生成修复 plan

```
/gsd-verify-work 1                  # UAT for phase 1
```

---

### /gsd-ship

从已完成的 phase 工作创建 PR，自动生成 PR 正文。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号或 milestone 版本（例如 `4` 或 `v1.0`） |
| `--draft` | 否 | 创建为 draft PR |

**前置条件：** Phase 已验证（`/gsd-verify-work` 通过），`gh` CLI 已安装并认证 **产出：** 包含规划产物丰富正文的 GitHub PR，STATE.md 已更新

```
/gsd-ship 4                         # Ship phase 4
/gsd-ship 4 --draft                 # Ship as draft PR
```

**PR 正文包含：**

- 来自 ROADMAP.md 的 phase 目标
- 来自 SUMMARY.md 文件的变更摘要
- 已覆盖的需求（REQ-ID）
- 验证状态
- 关键决策
- 通过 `ship.pr_body_sections` 配置的可选 PRD 风格章节

入门指南、示例和验证规则请参阅 [Custom PR Body Sections](https://github.com/gsd-build/get-shit-done/blob/main/docs/ship-pr-body-sections.md)。

---

### /gsd-ui-review

对已实现前端的回顾性六大支柱视觉审计。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号（默认为最后执行的 phase） |

**前置条件：** 项目有前端代码（可独立运行，无需 GSD 项目） **产出：** `{phase}-UI-REVIEW.md`，截图在 `.planning/ui-reviews/`

```
/gsd-ui-review                      # Audit current phase
/gsd-ui-review 3                    # Audit phase 3
```

---

### /gsd-audit-uat

跨 phase 审计所有未完成的 UAT 和验证项。

**前置条件：** 至少有一个 phase 已执行 UAT 或验证 **产出：** 分类审计报告及人工测试计划

```
/gsd-audit-uat
```

---

### /gsd-audit-milestone

验证 milestone 是否满足其完成定义。

**前置条件：** 所有 phase 已执行 **产出：** 包含缺口分析的审计报告

```
/gsd-audit-milestone
```

---

### /gsd-complete-milestone

归档 milestone，打 release tag。

**前置条件：** Milestone 审计已完成（推荐） **产出：** `MILESTONES.md` 条目、git tag

```
/gsd-complete-milestone
```

---

### /gsd-milestone-summary

从 milestone 产物生成综合项目摘要，用于团队 onboarding 和 review。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `version` | 否 | Milestone 版本（默认为当前/最新 milestone） |

**前置条件：** 至少有一个已完成或进行中的 milestone **产出：** `.planning/reports/MILESTONE_SUMMARY-v{version}.md`

**摘要包含：**

- 概览、架构决策、逐 phase 分解
- 关键决策和权衡
- 需求覆盖
- 技术债和延期项
- 新团队成员上手指南
- 生成后提供交互式问答
```
/gsd-milestone-summary                # Summarize current milestone
/gsd-milestone-summary v1.0           # Summarize specific milestone
```

---

### /gsd-new-milestone

启动下一个版本周期。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `name` | 否 | Milestone 名称 |
| `--reset-phase-numbers` | 否 | 将新 milestone 的编号从 Phase 1 重新开始，并在规划前归档旧的 phase 目录 |

**前置条件：** 前一个 milestone 已完成 **产出：** 更新的 `PROJECT.md`、新的 `REQUIREMENTS.md`、新的 `ROADMAP.md`

```
/gsd-new-milestone                  # Interactive
/gsd-new-milestone "v2.0 Mobile"    # Named milestone
/gsd-new-milestone --reset-phase-numbers "v2.0 Mobile"  # Restart milestone numbering at 1
```

---

## Phase 管理命令

### /gsd-phase

ROADMAP.md 中 phase 的增删改查 — 通过单一统一命令添加、插入、移除或编辑 phase。

| Flag | 说明 |
| --- | --- |
| （无） | 在当前 milestone 末尾追加新的整数编号 phase |
| `--insert <N>` | 在 phase N 之后插入紧急工作作为小数编号 phase（例如 3.1） |
| `--remove <N>` | 移除未来的 phase 并重新编号后续 phase |
| `--edit <N>` | 就地编辑现有 phase 的任意字段 |
| `--force` | 允许编辑进行中或已完成的 phase（与 `--edit` 配合使用） |

**前置条件：** `.planning/ROADMAP.md` 存在 **产出：** 更新的 ROADMAP.md

```
/gsd-phase "Add authentication system"          # Append new phase with description
/gsd-phase --insert 3 "Fix auth race condition" # Insert between phase 3 and 4 → creates 3.1
/gsd-phase --remove 7               # Remove phase 7, renumber 8→7, 9→8, etc.
/gsd-phase --edit 5                 # Edit any field of phase 5
/gsd-phase --edit 5 --force         # Edit phase 5 even if in-progress or completed
```

---

### /gsd-validate-phase

回顾性审计并填补 Nyquist 验证缺口。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号 |

```
/gsd-validate-phase 2               # Audit test coverage for phase 2
```

---

## 导航命令

### /gsd-progress

显示状态、下一步操作，并自动推进到下一个逻辑工作流步骤。读取项目状态并确定适当的操作。

| Flag | 说明 |
| --- | --- |
| `--next` | 自动推进到下一个逻辑工作流步骤，无需手动选择路由 |
| `--do "task description"` | 分析自由格式意图并分派到最合适的 GSD 命令 |
| `--forensic` | 在标准报告后附加 6 项完整性审计（STATE 一致性、孤立交接、延期范围漂移、memory 标记的待办、阻塞的 todo、未提交的代码） |

**自动路由行为（`--next`）：**

- 无项目 → 建议 `/gsd-new-project`
- Phase 需要讨论 → 运行 `/gsd-discuss-phase`
- Phase 需要规划 → 运行 `/gsd-plan-phase`
- Phase 需要执行 → 运行 `/gsd-execute-phase`
- Phase 需要验证 → 运行 `/gsd-verify-work`
- 所有 phase 完成 → 建议 `/gsd-complete-milestone`
```
/gsd-progress                       # "Where am I? What's next?" with auto-routing
/gsd-progress --next                # Advance to next step automatically
/gsd-progress --do "fix the auth bug"  # Dispatch freeform intent to best GSD command
/gsd-progress --forensic            # Standard report + integrity audit
```

### /gsd-resume-work

从上次会话恢复完整上下文。

```
/gsd-resume-work                    # After context reset or new session
```

### /gsd-pause-work

在 phase 中途停止时保存上下文交接。

| Flag | 说明 |
| --- | --- |
| `--report` | 在 `.planning/reports/` 中生成会后摘要，记录 commit、文件变更和 phase 进度 |

```
/gsd-pause-work                     # Creates continue-here.md
/gsd-pause-work --report            # Creates continue-here.md + session report
```

### /gsd-manager

交互式命令中心，用于在一个终端中管理多个 phase。

**前置条件：** `.planning/ROADMAP.md` 存在 **行为：**

- 所有 phase 的仪表盘，带可视化状态指示器
- 基于依赖和进度推荐最优下一步操作
- 分派工作：discuss 内联运行，plan/execute 作为后台 agent 运行
- 为高级用户设计，可在一个终端中跨 phase 并行工作
- 支持通过 `manager.flags` 配置逐步骤透传 flag（参见 [Configuration](https://github.com/gsd-build/get-shit-done/blob/main/docs/CONFIGURATION.md#manager-passthrough-flags)）
```
/gsd-manager                        # Open command center dashboard
/gsd-manager --analyze-deps         # Scan ROADMAP phases for dependency relationships before parallel execution
```

**Checkpoint 心跳 (#2410)：**

后台 `execute-phase` 运行在每个 wave 和 plan 边界发出 `[checkpoint]` 标记，使 Claude API SSE 流不会空闲到触发 `Stream idle timeout - partial response received`（在多 plan phase 场景中）。格式为：

```
[checkpoint] phase {N} wave {W}/{M} starting, {count} plan(s), {P}/{Q} plans done
[checkpoint] phase {N} wave {W}/{M} plan {plan_id} starting ({P}/{Q} plans done)
[checkpoint] phase {N} wave {W}/{M} plan {plan_id} complete ({P}/{Q} plans done)
[checkpoint] phase {N} wave {W}/{M} complete, {P}/{Q} plans done ({ok}/{count} ok)
```

如果后台 phase 中途失败，在 transcript 中搜索 `[checkpoint]` 查看最后确认的边界。Manager 的后台完成处理程序使用这些标记在 agent 出错时报告部分进度。

**Manager 透传 Flag：**

在 `.planning/config.json` 的 `manager.flags` 下配置逐步骤 flag。这些 flag 会附加到每个分派的命令：

```
{
  "manager": {
    "flags": {
      "discuss": "--auto",
      "plan": "--skip-research",
      "execute": "--validate"
    }
  }
}
```

---

### /gsd-help

显示所有命令和使用指南。

```
/gsd-help                           # Quick reference
```

---

## 实用工具命令

### /gsd-explore

苏格拉底式构思会话 — 通过探究性问题引导想法，可选启动研究，然后将输出路由到合适的 GSD 产物（笔记、todo、seed、研究问题、需求或新 phase）。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `topic` | 否 | 要探索的主题（例如 `/gsd-explore authentication strategy`） |

```
/gsd-explore                        # Open-ended ideation session
/gsd-explore authentication strategy  # Explore a specific topic
```

---

### /gsd-undo

安全 git 回退 — 使用 phase 清单回退 GSD phase 或 plan commit，带依赖检查和确认门控。

| Flag | 必填 | 说明 |
| --- | --- | --- |
| `--last N` | （三选一必填） | 显示最近的 GSD commit 供交互式选择 |
| `--phase NN` | （三选一必填） | 回退某个 phase 的所有 commit |
| `--plan NN-MM` | （三选一必填） | 回退特定 plan 的所有 commit |

**安全性：** 回退前检查依赖的 phase/plan；始终显示确认门控。

```
/gsd-undo --last 5                  # Pick from the 5 most recent GSD commits
/gsd-undo --phase 03                # Revert all commits for phase 3
/gsd-undo --plan 03-02              # Revert commits for plan 02 of phase 3
```

---

### /gsd-import

将外部 plan 文件导入 GSD 规划系统，在写入前对 `PROJECT.md` 决策进行冲突检测。

| Flag | 必填 | 说明 |
| --- | --- | --- |
| `--from <filepath>` | 是（或 `--from-gsd2`） | 要导入的外部 plan 文件路径 |
| `--from-gsd2` | 是（或 `--from`） | 反向迁移 GSD-2（`.gsd/`）项目回 GSD v1（`.planning/`）格式 |
| `--path <dir>` | 否 | 与 `--from-gsd2` 配合：GSD-2 项目目录路径（默认为当前目录） |

**流程：** 检测冲突 → 提示解决 → 写入为 GSD PLAN.md → 通过 `gsd-plan-checker` 验证

```
/gsd-import --from /tmp/team-plan.md    # Import and validate an external plan
/gsd-import --from-gsd2                # Migrate from GSD-2 back to v1 (current dir)
/gsd-import --from-gsd2 --path ~/old-project  # Migrate from a different path
```

---

### /gsd-ingest-docs

从仓库中已有的 ADR、PRD、SPEC 和文档引导或合并 `.planning/` 配置。运行并行分类（`gsd-doc-classifier`）加综合处理，带优先级规则和循环检测（`gsd-doc-synthesizer`）。生成三分桶冲突报告（`INGEST-CONFLICTS.md`：auto-resolved、competing-variants、unresolved-blockers），并在 LOCKED 对 LOCKED ADR 矛盾时硬阻断。

| 参数 / Flag | 必填 | 说明 |
| --- | --- | --- |
| `path` | 否 | 要扫描的目标目录（默认为仓库根目录） |
| `--mode new\|merge` | 否 | 覆盖自动检测（默认：`.planning/` 不存在时为 `new`，存在时为 `merge`） |
| `--manifest <file>` | 否 | YAML 文件，每项列出 `{path, type, precedence?}`；覆盖启发式分类 |
| `--resolve auto` | 否 | 冲突解决模式（v1：仅支持 `auto`；`interactive` 已保留） |

**限制：** v1 每次调用最多 50 个文档。将共享的冲突检测契约提取到 `references/doc-conflict-engine.md`，`/gsd-import` 也会使用。

```
/gsd-ingest-docs                            # Scan repo root, auto-detect mode
/gsd-ingest-docs docs/                      # Only ingest under docs/
/gsd-ingest-docs --manifest ingest.yaml     # Explicit precedence manifest
```

---

### /gsd-quick

带 GSD 保障执行临时任务。

| Flag | 说明 |
| --- | --- |
| `--full` | 启用完整质量流水线 — discuss + research + plan-checking + verification |
| `--validate` | 仅 plan-checking（最多 2 轮）+ 执行后验证；无 discuss 或 research |
| `--discuss` | 轻量级预规划讨论 |
| `--research` | 在规划前启动针对性 researcher |

细粒度 flag 可组合：`--discuss --research --validate` 等同于 `--full`。

| 子命令 | 说明 |
| --- | --- |
| `list` | 列出所有 quick task 及状态 |
| `status <slug>` | 显示特定 quick task 的状态 |
| `resume <slug>` | 通过 slug 恢复特定 quick task |

```
/gsd-quick                          # Basic quick task
/gsd-quick --discuss --research     # Discussion + research + planning
/gsd-quick --validate               # Plan-checking + verification only
/gsd-quick --full                   # Complete quality pipeline
/gsd-quick list                     # List all quick tasks
/gsd-quick status my-task-slug      # Show status of a quick task
/gsd-quick resume my-task-slug      # Resume a quick task
```

### /gsd-autonomous

自主运行所有剩余 phase。

| Flag | 说明 |
| --- | --- |
| `--from N` | 从特定 phase 编号开始 |
| `--to N` | 完成特定 phase 编号后停止 |
| `--interactive` | 精简上下文并允许用户输入 |

```
/gsd-autonomous                     # Run all remaining phases
/gsd-autonomous --from 3            # Start from phase 3
/gsd-autonomous --to 5              # Run up to and including phase 5
/gsd-autonomous --from 3 --to 5     # Run phases 3 through 5
```

### /gsd-debug

带持久状态的系统性调试。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `description` | 否 | Bug 描述 |

| Flag | 说明 |
| --- | --- |
| `--diagnose` | 纯诊断模式 — 调查但不尝试修复 |

**子命令：**

- `/gsd-debug list` — 列出所有活跃的调试会话及状态、假设和下一步操作
- `/gsd-debug status <slug>` — 打印会话的完整摘要（证据数量、排除数量、解决方案、TDD checkpoint），不启动 agent
- `/gsd-debug continue <slug>` — 通过 slug 恢复特定会话（显示当前焦点后启动续接 agent）
- `/gsd-debug [--diagnose] <description>` — 启动新调试会话（现有行为；`--diagnose` 在根因处停止，不应用修复）

**TDD 模式：** 当 `.planning/config.json` 中 `tdd_mode: true` 时，调试会话要求在应用任何修复前编写并验证一个失败的测试（red → green → done）。

```
/gsd-debug "Login button not responding on mobile Safari"
/gsd-debug --diagnose "Intermittent 500 errors on /api/users"
/gsd-debug list
/gsd-debug status auth-token-null
/gsd-debug continue form-submit-500
```

### /gsd-add-tests

为已完成的 phase 生成测试。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | 否 | Phase 编号 |

```
/gsd-add-tests 2                    # Generate tests for phase 2
```

### /gsd-stats

显示项目统计信息。

```
/gsd-stats                          # Project metrics dashboard
```

### /gsd-profile-user

从 Claude Code 会话分析中生成开发者行为画像，覆盖 8 个维度（沟通风格、决策模式、调试方法、UX 偏好、供应商选择、挫败触发点、学习风格、解释深度）。产出物可个性化 Claude 的响应。

| Flag | 说明 |
| --- | --- |
| `--questionnaire` | 使用交互式问卷替代会话分析 |
| `--refresh` | 重新分析会话并重新生成画像 |

**生成的产物：**

- `USER-PROFILE.md` — 完整行为画像
- `CLAUDE.md` 画像部分 — 被 Claude Code 自动发现
```
/gsd-profile-user                   # Analyze sessions and build profile
/gsd-profile-user --questionnaire   # Interactive questionnaire fallback
/gsd-profile-user --refresh         # Re-generate from fresh analysis
```

### /gsd-health

验证 `.planning/` 目录完整性。使用 `--context` 时，探测上下文窗口利用率守卫的 60% / 70% 阈值（v1.40.0 新增，[#2792](https://github.com/gsd-build/get-shit-done/issues/2792)）。

| Flag | 说明 |
| --- | --- |
| `--repair` | 自动修复可恢复的问题 |
| `--context` | 探测上下文窗口利用率；60% 时警告，70% 时严重 |

```
/gsd-health                         # Check integrity
/gsd-health --repair                # Check and fix
/gsd-health --context               # Context-utilization triage
```

### /gsd-cleanup

归档已完成 milestone 中积累的 phase 目录。

```
/gsd-cleanup
```

---

## Spike 与 Sketch 命令

### /gsd-spike

在确定实现方案前运行 2-5 个聚焦可行性实验。每个实验使用 Given/When/Then 框架，生成可执行代码，并返回 VALIDATED / INVALIDATED / PARTIAL 判定。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `idea` | 否 | 要调查的技术问题或方案 |
| `--quick` | 否 | 跳过 intake 对话；直接使用 `idea` 文本 |
| `--wrap-up` | 否 | 将已完成的 spike 结论打包为可复用的项目本地 skill |

**产出：** `.planning/spikes/NNN-experiment-name/` 包含代码、结果和 README；`.planning/spikes/MANIFEST.md` **`--wrap-up` 产出：** `.claude/skills/spike-findings-[project]/` skill 文件

```
/gsd-spike                              # Interactive intake
/gsd-spike "can we stream LLM tokens through SSE"
/gsd-spike --quick websocket-vs-polling
/gsd-spike --wrap-up                    # Package findings into a reusable skill
```

---

### /gsd-sketch

通过一次性 HTML 原型探索设计方向，在投入实现前进行验证。每个设计问题生成 2-3 个变体，供直接在浏览器中比较。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `idea` | 否 | 要探索的 UI 设计问题或方向 |
| `--quick` | 否 | 跳过 mood intake；直接使用 `idea` 文本 |
| `--text` | 否 | 文本模式回退 — 用编号列表替代交互式提示（适用于非 Claude 运行时） |
| `--wrap-up` | 否 | 将胜出 sketch 的决策打包为可复用的项目本地 skill |

**产出：** `.planning/sketches/NNN-descriptive-name/index.html`（2-3 个交互式变体）、`README.md`、共享的 `themes/default.css`；`.planning/sketches/MANIFEST.md` **`--wrap-up` 产出：** `.claude/skills/sketch-findings-[project]/` skill 文件

```
/gsd-sketch                             # Interactive mood intake
/gsd-sketch "dashboard layout"
/gsd-sketch --quick "sidebar navigation"
/gsd-sketch --text "onboarding flow"    # Non-Claude runtime
/gsd-sketch --wrap-up                   # Package winning sketch into a skill
```

---

## 诊断命令

### /gsd-forensics

失败的 GSD 工作流的事后调查 — 诊断出了什么问题。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `description` | 否 | 问题描述（省略时交互式提示） |

**前置条件：** `.planning/` 目录存在 **产出：** `.planning/forensics/report-{timestamp}.md`

**调查范围：**

- Git 历史分析（近期 commit、卡住的模式、时间间隔）
- 产物完整性（已完成 phase 的预期文件）
- STATE.md 异常和会话历史
- 未提交的工作、冲突、废弃的变更
- 至少检查 4 种异常类型（卡住循环、缺失产物、废弃工作、崩溃/中断）
- 如有可操作的发现，提供创建 GitHub issue 的选项
```
/gsd-forensics                              # Interactive — prompted for problem
/gsd-forensics "Phase 3 execution stalled"  # With problem description
```

---

### /gsd-extract-learnings

从已完成的 phase 工作中提取可复用模式、反模式和架构决策。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | **是** | 要提取经验教训的 phase 编号 |

| Flag | 说明 |
| --- | --- |
| `--all` | 从所有已完成 phase 提取经验教训 |
| `--format` | 输出格式：`markdown`（默认）、`json` |

**前置条件：** Phase 已执行（SUMMARY.md 文件存在） **产出：** `.planning/learnings/{phase}-LEARNINGS.md`

**提取内容：**

- 架构决策及其理由
- 效果良好的模式（可在未来 phase 中复用）
- 遇到的反模式及其解决方式
- 技术栈相关的洞察
- 性能和测试观察
```
/gsd-extract-learnings 3                    # Extract learnings from phase 3
/gsd-extract-learnings --all                # Extract from all completed phases
```

---

## 工作流管理

### /gsd-workstreams

管理并行工作流，用于同时处理 milestone 的不同领域。

**子命令：**

| 子命令 | 说明 |
| --- | --- |
| `list` | 列出所有工作流及状态（无子命令时的默认行为） |
| `create <name>` | 创建新工作流 |
| `status <name>` | 某个工作流的详细状态 |
| `switch <name>` | 设置活跃工作流 |
| `progress` | 跨工作流进度摘要 |
| `complete <name>` | 归档已完成的工作流 |
| `resume <name>` | 恢复工作流中的工作 |

**前置条件：** 活跃的 GSD 项目 **产出：** `.planning/` 下的工作流目录，每个工作流的状态追踪

```
/gsd-workstreams                    # List all workstreams
/gsd-workstreams create backend-api # Create new workstream
/gsd-workstreams switch backend-api # Set active workstream
/gsd-workstreams status backend-api # Detailed status
/gsd-workstreams progress           # Cross-workstream progress overview
/gsd-workstreams complete backend-api  # Archive completed workstream
/gsd-workstreams resume backend-api    # Resume work in workstream
```

---

## 配置命令

### /gsd-settings

交互式配置工作流开关和模型 profile。问题分为六个可视化部分：

- **规划** — Research、Plan Checker、Pattern Mapper、Nyquist、UI Phase、UI Gate、AI Phase
- **执行** — Verifier、TDD Mode、Code Review、Code Review Depth *（条件显示 — 仅在 Code Review 开启时）*、UI Review
- **文档与输出** — Commit Docs、Skip Discuss、Worktrees
- **功能** — Intel、Graphify
- **模型与流水线** — Model Profile、Auto-Advance、Branching
- **其他** — Context Warnings、Research Qs

所有回答通过 `gsd-sdk query config-set` 合并到已解析的项目配置路径（标准安装为 `.planning/config.json`，活跃工作流时为 `.planning/workstreams/<active>/config.json`），保留不相关的键。确认后，用户可将完整设置对象保存到 `~/.gsd/defaults.json`，使未来 `/gsd-new-project` 运行从相同基线开始。

```
/gsd-settings                       # Interactive config
```

### /gsd-config

交互式配置 GSD 设置 — 工作流开关、高级参数、集成和模型 profile — 通过单一统一命令完成。

| Flag | 说明 |
| --- | --- |
| （无） | 常用开关：model、research、plan\_check、verifier、branching |
| `--advanced` | 高级用户参数：规划调优、超时、分支模板、cross-AI 执行、运行时/输出 |
| `--integrations` | 第三方 API key、code-review CLI 路由、agent-skill 注入 |
| `--profile <name>` | 快速 profile 切换：`quality`、`balanced`、`budget` 或 `inherit` |

**`--advanced` 部分：**

| 部分 | 键 |
| --- | --- |
| 规划调优 | `workflow.plan_bounce`、`workflow.plan_bounce_passes`、`workflow.plan_bounce_script`、`workflow.subagent_timeout`、`workflow.inline_plan_threshold` |
| 执行调优 | `workflow.node_repair`、`workflow.node_repair_budget`、`workflow.auto_prune_state` |
| 讨论调优 | `workflow.max_discuss_passes` |
| Cross-AI 执行 | `workflow.cross_ai_execution`、`workflow.cross_ai_command`、`workflow.cross_ai_timeout` |
| Git 自定义 | `git.base_branch`、`git.phase_branch_template`、`git.milestone_branch_template` |
| 运行时/输出 | `response_language`、`context_window`、`search_gitignored`、`graphify.build_timeout` |

所有回答通过 `gsd-sdk query config-set` 合并，保留不相关的键。API key 在所有输出中掩码显示（`****<last-4>`）。

```
/gsd-config                         # Common-case interactive config
/gsd-config --advanced              # Power-user knobs (six-section prompt)
/gsd-config --integrations          # API keys, review CLI routing, agent skills
/gsd-config --profile budget        # Switch to budget profile
/gsd-config --profile quality       # Switch to quality profile
```

完整 schema 和默认值请参阅 [CONFIGURATION.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/CONFIGURATION.md)。

### /gsd-surface

切换显示哪些 skill — 应用 profile、列出或禁用某个集群，无需重新安装。

| 子命令 | 说明 |
| --- | --- |
| `list` | 显示已启用和已禁用的集群及 skill |
| `status` | `list` 的别名，加上 token 开销摘要 |
| `profile <name>` | 写入 `baseProfile` 并重新暂存 skill |
| `disable <cluster>` | 将集群添加到禁用列表并重新暂存 |
| `enable <cluster>` | 从禁用列表中移除集群并重新暂存 |
| `reset` | 删除 surface 增量；恢复到安装时的 profile |

```
/gsd-surface list                   # Show current surface
/gsd-surface profile standard       # Switch to standard profile
/gsd-surface disable utility        # Disable the utility cluster
/gsd-surface reset                  # Restore install-time profile
```

---

## 棕地命令

### /gsd-map-codebase

使用并行 mapper agent 分析现有代码库。使用 `--fast` 进行快速单 agent 扫描，或使用 `--query` 搜索已有智能数据。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `area` | 否 | 将映射范围限定到特定区域 |
| `--fast` | 否 | 快速单焦点评估 — 启动 1 个 mapper agent 而非 4 个并行 agent（轻量替代方案） |
| `--query <term>` | 否 | 搜索 `.planning/intel/` 中可查询的代码库智能文件（需 `intel.enabled: true`） |

| Flag | 说明 |
| --- | --- |
| `--focus tech\|arch\|quality\|concerns\|tech+arch` | `--fast` 模式的聚焦区域（默认：`tech+arch`） |

**产出：** `.planning/codebase/` 分析文档（完整模式）；`.planning/codebase/` 中的针对性文档（`--fast`）；智能查询结果（`--query`）

```
/gsd-map-codebase                   # Full codebase analysis (4 parallel agents)
/gsd-map-codebase auth              # Focus on auth area
/gsd-map-codebase --fast            # Quick tech + arch overview (1 agent)
/gsd-map-codebase --fast --focus quality  # Quality and code health only
/gsd-map-codebase --query authentication  # Search intel for a term
```

### /gsd-graphify

构建、查询和检查存储在 `.planning/graphs/` 中的项目知识图谱。通过 `config.json` 中的 `graphify.enabled: true` 启用（参见 [Configuration Reference](https://github.com/gsd-build/get-shit-done/blob/main/docs/CONFIGURATION.md#graphify-settings)）；禁用时，命令打印激活提示并停止。

| 子命令 | 说明 |
| --- | --- |
| `build` | 构建或重建知识图谱（内联运行 `graphify update .` 并刷新 `.planning/graphs/`） |
| `query <term>` | 在图谱中搜索术语 |
| `status` | 显示图谱新鲜度和统计信息 |
| `diff` | 显示自上次构建以来的变更 |

**产出：** `.planning/graphs/` 图谱产物（节点、边、快照）

```
/gsd-graphify build                 # Build or rebuild the knowledge graph
/gsd-graphify query authentication  # Search the graph for a term
/gsd-graphify status                # Show freshness and statistics
/gsd-graphify diff                  # Show changes since last build
```

**编程访问：** `node gsd-tools.cjs graphify <build|query|status|diff|snapshot>` — 参见 [CLI Tools Reference](https://github.com/gsd-build/get-shit-done/blob/main/docs/CLI-TOOLS.md)。

---

## AI 集成命令

### /gsd-ai-integration-phase

为涉及构建 AI 系统的 phase 生成 AI-SPEC.md 设计契约。展示交互式决策矩阵，呈现领域相关的失败模式和评估标准，产出包含框架推荐、实施指导和评估策略的 `AI-SPEC.md`。

**产出：** phase 目录中的 `{phase}-AI-SPEC.md`

**启动：** 3 个并行专家 agent：domain-researcher、framework-selector、ai-researcher 和 eval-planner

```
/gsd-ai-integration-phase              # Wizard for the current phase
/gsd-ai-integration-phase 3           # Wizard for a specific phase
```

---

### /gsd-eval-review

审计已执行 AI phase 的评估覆盖度，并生成 EVAL-REVIEW.md 修复计划。对照 `/gsd-ai-integration-phase` 生成的 `AI-SPEC.md` 评估计划检查实现。对每个评估维度评分：COVERED/PARTIAL/MISSING。

**前置条件：** Phase 已执行且有 `AI-SPEC.md` **产出：** `{phase}-EVAL-REVIEW.md`，包含发现、缺口和修复指导

```
/gsd-eval-review                       # Audit current phase
/gsd-eval-review 3                     # Audit a specific phase
```

---

## 更新命令

### /gsd-update

更新 GSD，含变更日志预览，可选同步 skill 或重新应用本地补丁。

| Flag | 说明 |
| --- | --- |
| `--sync` | 更新后从 GSD registry 同步 skill |
| `--reapply` | 更新后恢复本地修改（补丁） |

```
/gsd-update                         # Check for updates and install
/gsd-update --sync                  # Update and sync skills
/gsd-update --reapply               # Update and reapply local patches
```

---

## 代码质量命令

### /gsd-code-review

Review phase 期间变更的源文件，检查 bug、安全漏洞和代码质量问题。使用 `--fix` 可在 review 后自动修复发现的问题。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `N` | **是** | 要 review 变更的 phase 编号（例如 `2` 或 `02`） |
| `--depth=quick\|standard\|deep` | 否 | Review 深度级别（覆盖 `workflow.code_review_depth` 配置）。`quick`：仅模式匹配（约 2 分钟）。`standard`：逐文件分析含语言特定检查（约 5-15 分钟，默认）。`deep`：跨文件分析含 import 图和调用链（约 15-30 分钟） |
| `--files file1,file2,...` | 否 | 显式逗号分隔文件列表；完全跳过 SUMMARY/git 范围界定 |
| `--fix` | 否 | review 后自动修复 — 读取 REVIEW.md，启动 fixer agent，原子化提交每个修复 |
| `--fix --all` | 否 | 修复范围包含 Info 级别发现（默认：仅 Critical + Warning） |
| `--fix --auto` | 否 | 修复 + 重新 review 迭代循环，最多 3 轮 |

**前置条件：** Phase 已执行且有 SUMMARY.md 或 git 历史 **产出：** `{phase}-REVIEW.md`，含按严重程度分类的发现；使用 `--fix` 时还有 `{phase}-REVIEW-FIX.md` **启动：** `gsd-code-reviewer` agent；`gsd-code-fixer` agent（使用 `--fix` 时）

**可选结构化预扫描：** 将 `code_quality.fallow.enabled` 设为 `true` 可在 agent review 前运行 fallow。GSD 写入 `{phase}/FALLOW.json` 并在 `REVIEW.md` 中嵌入 `Structural Findings (fallow)` 部分。通过 `code_quality.fallow.scope` 和 `code_quality.fallow.profile` 配置范围和 profile。

```
/gsd-code-review 3                          # Standard review for phase 3
/gsd-code-review 2 --depth=deep             # Deep cross-file review
/gsd-code-review 4 --files src/auth.ts,src/token.ts  # Explicit file list
/gsd-code-review 3 --fix                    # Review then fix Critical + Warning findings
/gsd-code-review 3 --fix --all             # Review then fix all findings including Info
/gsd-code-review 3 --fix --auto            # Review, fix, and re-review until clean (max 3 iterations)
```

---

### /gsd-audit-fix

自主审计到修复流水线 — 运行审计、分类发现、带测试验证自动修复可修复问题，并原子化提交每个修复。

| Flag | 说明 |
| --- | --- |
| `--source <audit>` | 运行哪种审计（默认：`audit-uat`） |
| `--severity high\|medium\|all` | 处理的最低严重程度（默认：`medium`） |
| `--max N` | 最多修复的发现数量（默认：5） |
| `--dry-run` | 分类发现但不修复（显示分类表） |

**前置条件：** 至少有一个 phase 已执行 UAT 或验证 **产出：** 带测试验证的修复 commit；分类报告

```
/gsd-audit-fix                              # Run audit-uat, fix medium+ issues (max 5)
/gsd-audit-fix --severity high             # Only fix high-severity issues
/gsd-audit-fix --dry-run                   # Preview classification without fixing
/gsd-audit-fix --max 10 --severity all     # Fix up to 10 issues of any severity
```

---

## 快速与内联命令

### /gsd-fast

内联执行简单任务 — 无子 agent、无规划开销。适用于拼写修复、配置更改、小重构、遗漏的 commit。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `task description` | 否 | 要做什么（省略时交互式提示） |

**不能替代 `/gsd-quick`** — 需要研究、多步规划或验证的任务请使用 `/gsd-quick`。

```
/gsd-fast "fix typo in README"
/gsd-fast "add .env to gitignore"
```

---

### /gsd-review

来自外部 AI CLI 的跨 AI peer review。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--phase N` | **是** | 要 review 的 phase 编号 |

| Flag | 说明 |
| --- | --- |
| `--gemini` | 包含 Gemini CLI review |
| `--claude` | 包含 Claude CLI review（独立会话） |
| `--codex` | 包含 Codex CLI review |
| `--coderabbit` | 包含 CodeRabbit review |
| `--opencode` | 包含 OpenCode review（通过 GitHub Copilot） |
| `--qwen` | 包含 Qwen Code review（阿里巴巴 Qwen 模型） |
| `--cursor` | 包含 Cursor agent review |
| `--ollama` | 包含 Ollama server review |
| `--lm-studio` | 包含 LM Studio server review |
| `--llama-cpp` | 包含 llama.cpp server review |
| `--all` | 包含所有可用的 reviewer（CLI + 本地模型服务器） |

**默认 reviewer 行为（无 flag 时）：**

- 如果 `review.default_reviewers` **未设置**，`/gsd-review` 运行所有检测到的 reviewer（当前默认行为）。
- 如果 `review.default_reviewers` **已设置**，`/gsd-review` 仅运行该子集（例如 `["gemini","codex"]`）。
- `--all` 始终覆盖配置，运行全部检测到的集合。
- 显式 flag（例如 `--cursor`）覆盖 `--all` 和配置默认值，仅对该次运行生效。

**产出：** `{phase}-REVIEWS.md` — 可被 `/gsd-plan-phase --reviews` 消费

```
# set project default reviewers for no-flag /gsd-review runs
gsd config-set review.default_reviewers '["gemini","codex"]'

/gsd-review --phase 2             # runs gemini+codex from config
/gsd-review --phase 3 --all
/gsd-review --phase 2 --gemini
/gsd-review --phase 2 --cursor    # one-off override
```

---

### /gsd-pr-branch

通过过滤掉 `.planning/` commit 创建干净的 PR 分支。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `target branch` | 否 | 基础分支（默认：`main`） |

**目的：** reviewer 只看到代码变更，而非 GSD 规划产物。

```
/gsd-pr-branch                     # Filter against main
/gsd-pr-branch develop             # Filter against develop
```

---

### /gsd-secure-phase

回顾性验证已完成 phase 的威胁缓解措施。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `phase number` | 否 | 要审计的 phase（默认：最后完成的 phase） |

**前置条件：** Phase 必须已执行。有无 SECURITY.md 均可工作。 **产出：** `{phase}-SECURITY.md` 含威胁验证结果 **启动：** `gsd-security-auditor` agent

三种运行模式：

1. SECURITY.md 存在 — 审计并验证已有的缓解措施
2. 无 SECURITY.md 但 PLAN.md 有威胁模型 — 从产物生成
3. Phase 未执行 — 退出并给出指引
```
/gsd-secure-phase                   # Audit last completed phase
/gsd-secure-phase 5                 # Audit specific phase
```

---

### /gsd-docs-update

基于代码库验证来生成或更新项目文档。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--force` | 否 | 跳过保留提示，重新生成所有文档 |
| `--verify-only` | 否 | 仅检查现有文档的准确性，不生成 |

**产出：** 最多 9 个文档文件（README、architecture、API、getting started、development、testing、configuration、deployment、contributing） **启动：** `gsd-doc-writer` agent（每种文档类型一个），然后 `gsd-doc-verifier` agent 进行事实验证

每个文档编写器直接探索代码库 — 不会产生幻觉路径或过时的签名。文档验证器对照实际文件系统检查声明。

```
/gsd-docs-update                    # Generate/update docs interactively
/gsd-docs-update --force            # Regenerate all docs
/gsd-docs-update --verify-only      # Verify existing docs only
```

---

## 任务捕获与待办命令

### /gsd-capture

捕获想法、任务、笔记和 seed 到合适的目的地。默认模式添加结构化 todo；flag 路由到专门的捕获工作流。

| Flag | 说明 |
| --- | --- |
| （无） | 捕获为结构化 todo 供后续工作 |
| `--note [text]` | 零摩擦笔记 — 追加、列出（`--note list`）或提升（`--note promote N`） |
| `--backlog <description>` | 使用 999.x 编号添加到 backlog 停车场 |
| `--seed [idea summary]` | 捕获前瞻性想法及触发条件 |
| `--list` | 列出待办 todo 并选择一个开始工作 |
| `--global` | 使用全局范围（用于笔记操作） |

**Backlog：** 999.x 编号将条目保持在活跃 phase 序列之外；phase 目录会立即创建，使 `/gsd-discuss-phase` 和 `/gsd-plan-phase` 可以在其上工作。**Seed：** 保留完整的 WHY、何时浮出以及面包屑 — 被 `/gsd-new-milestone` 消费。

**产出：** `.planning/todos/`（默认）、笔记文件（--note）、ROADMAP.md backlog 部分（--backlog）、`.planning/seeds/SEED-NNN-slug.md`（--seed）

```
/gsd-capture "Consider adding dark mode support"   # Add todo
/gsd-capture --note "Caching strategy idea"        # Quick note
/gsd-capture --note list                           # List all notes
/gsd-capture --note promote 3                      # Promote note 3 to todo
/gsd-capture --backlog "GraphQL API layer"         # Add to backlog
/gsd-capture --seed "Add real-time collaboration when WebSocket infra is in place"
/gsd-capture --list                                # Browse and act on todos
```

---

### /gsd-review-backlog

审查 backlog 条目并提升到活跃 milestone。

**每条目操作：** Promote（移到活跃序列）、Keep（保留在 backlog）、Remove（删除）。

```
/gsd-review-backlog
```

---

### /gsd-thread

管理跨会话工作的持久上下文线程。

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| （无）/ `list` | — | 列出所有线程 |
| `list --open` | — | 仅列出状态为 `open` 或 `in_progress` 的线程 |
| `list --resolved` | — | 仅列出状态为 `resolved` 的线程 |
| `status <slug>` | — | 显示特定线程的状态 |
| `close <slug>` | — | 将线程标记为已解决 |
| `name` | — | 按名称恢复已有线程 |
| `description` | — | 创建新线程 |

线程是轻量级的跨会话知识存储，用于跨越多个会话但不属于任何特定 phase 的工作。比 `/gsd-pause-work` 更轻量。

```
/gsd-thread                         # List all threads
/gsd-thread list --open             # List only open/in-progress threads
/gsd-thread list --resolved         # List only resolved threads
/gsd-thread status fix-deploy-key   # Show thread status
/gsd-thread close fix-deploy-key    # Mark thread as resolved
/gsd-thread fix-deploy-key-auth     # Resume thread
/gsd-thread "Investigate TCP timeout in pasta service"  # Create new
```

---

## 状态管理命令

### state validate

检测 STATE.md 与实际文件系统之间的漂移。

**前置条件：** `.planning/STATE.md` 存在 **产出：** 验证报告，显示 STATE.md 字段与文件系统实际情况之间的漂移

```
node gsd-tools.cjs state validate
```

---

### state sync \[--verify\]

从磁盘上的实际项目状态重建 STATE.md。

| Flag | 说明 |
| --- | --- |
| `--verify` | Dry-run 模式 — 显示建议变更但不写入 |

**前置条件：** `.planning/` 目录存在 **产出：** 反映文件系统实际情况的更新 `STATE.md`

```
node gsd-tools.cjs state sync             # Reconstruct STATE.md from disk
node gsd-tools.cjs state sync --verify    # Dry-run: show changes without writing
```

---

### state planned-phase

在 plan-phase 完成后记录状态转换（Planned/Ready to execute）。

| Flag | 说明 |
| --- | --- |
| `--phase N` | 已规划的 phase 编号 |
| `--plans N` | 生成的 plan 数量 |

**前置条件：** Phase 已规划 **产出：** 更新的 `STATE.md` 含规划后状态

```
node gsd-tools.cjs state planned-phase --phase 3 --plans 2
```

---

## 社区命令

### 社区 Hook

可选的 git 和会话 hook，通过 `.planning/config.json` 中的 `hooks.community: true` 启用。除非显式启用，否则全部为空操作。

| Hook | 用途 |
| --- | --- |
| `gsd-validate-commit.sh` | 强制 git commit 消息遵循 Conventional Commits 格式 |
| `gsd-session-state.sh` | 追踪会话状态转换 |
| `gsd-phase-boundary.sh` | 强制 phase 边界检查 |

启用方式：

```
{ "hooks": { "community": true } }
```

---

### 社区邀请

要加入 GSD Discord 社区，请访问 GSD README 中的链接或运行 `/gsd-help` 并按其中显示的 Discord 链接操作。

---

## 贡献：Skill 描述标准

Skill 描述（每个 `commands/gsd/*.md` frontmatter 中的 `description:` 字段）会被注入到每次会话的系统提示中。为保持每次会话的开销较低，描述必须 <= 100 个字符，且不得重复 `argument-hint:` 中已有的 flag 文档。

lint 门控执行预算限制：

```
npm run lint:descriptions
```

该检查也作为 `npm test` 的一部分运行，通过 `tests/enh-2789-description-budget.test.cjs`。

---

## 参考

- [[get-shit-done 概览]]
- [[GSD 实战使用技巧]]
- [COMMANDS.md 原文](https://github.com/gsd-build/get-shit-done/blob/main/docs/COMMANDS.md)

- [[GSD 架构原理]]

## 相关笔记

- [[更新日志]]
- [[配置体系]]
- [[插件]]
- [[Agent 系统]]
- [[Copilot CLI+Claude Code双工具协同实践]]
