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
> - **[[Claude Code]] / [[Copilot]] / OpenCode / Kilo**：`/gsd-command-name [args]`
> - **Gemini CLI**：`/gsd:command-name [args]`（冒号命名空间）
> - **Codex**：`$gsd-command-name [args]`

---

## 核心工作流命令

### gsd-new-project

初始化新项目，深度收集上下文。

| Flag | 说明 |
|------|------|
| `--auto @file.md` | 从文档自动提取，跳过交互式问答 |

**生成**：`PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md`、`config.json`、`research/`

```bash
/gsd-new-project               # 交互模式
/gsd-new-project --auto @prd.md # 从 PRD 文档自动提取
```

---

### gsd-discuss-phase

规划前通过自适应问答收集阶段上下文。

| 参数/Flag | 说明 |
|-----------|------|
| `N` | 阶段号（默认当前阶段） |
| `--all` | 讨论所有灰色地带，不跳过任何区域 |
| `--auto` | 自动选择所有问题的推荐默认值 |
| `--batch` | 批量模式，分组收集问题而非逐一提问 |
| `--analyze` | 在讨论中加入权衡分析 |
| `--assumptions` | 展示 Claude 对该阶段的实现假设，不启动交互 |
| `--power` | 从预准备的答案文件批量回答 |

**生成**：`{phase}-CONTEXT.md`、`{phase}-DISCUSSION-LOG.md`

```bash
/gsd-discuss-phase 1              # 交互讨论阶段 1
/gsd-discuss-phase 1 --all        # 讨论所有灰区
/gsd-discuss-phase 3 --auto       # 自动选择默认值
/gsd-discuss-phase --batch        # 当前阶段批量模式
/gsd-discuss-phase 2 --analyze    # 附带权衡分析
/gsd-discuss-phase 3 --assumptions # 展示 Claude 的假设
```

---

### gsd-plan-phase

研究 + 规划 + 验证一个阶段。

| 参数/Flag | 说明 |
|-----------|------|
| `N` | 阶段号（默认下一个未规划阶段） |
| `--auto` | 跳过交互确认 |
| `--research` | 强制重新研究（即使 RESEARCH.md 已存在） |
| `--skip-research` | 跳过领域研究步骤 |
| `--research-phase N` | 仅研究模式：仅跑研究代理，不创建计划 |
| `--view` | 与 `--research-phase` 配合，打印现有研究结果到 stdout |
| `--gaps` | 缺口填补模式（读取 VERIFICATION.md，跳过研究） |
| `--skip-verify` | 跳过计划验证循环 |
| `--prd <file>` | 用 PRD 文件替代 discuss-phase 的上下文 |
| `--validate` | 规划前运行状态验证 |

**生成**：`{phase}-RESEARCH.md`、`{phase}-{N}-PLAN.md`、`{phase}-VALIDATION.md`

```bash
/gsd-plan-phase 1                        # 研究 + 规划 + 验证阶段 1
/gsd-plan-phase 3 --skip-research        # 跳过研究（熟悉领域）
/gsd-plan-phase --auto                   # 非交互模式
/gsd-plan-phase 2 --validate             # 规划前验证状态
/gsd-plan-phase --research-phase 4       # 仅研究阶段 4
/gsd-plan-phase --research-phase 4 --view # 打印已有研究结果
/gsd-plan-phase --research-phase 4 --research # 强制刷新研究
```

> [!info] 包合法性审查（v1.51）
> 研究代理推荐外部包时，自动运行 `slopcheck` 检查注册表、年龄、下载量、源码仓库。
> - `[SLOP]`：包被完全移除，永不进入规划
> - `[SUS]`：包被标记，规划在安装任务前插入 `checkpoint:human-verify`
> - `[OK]`：包已批准，无需检查点

---

### gsd-execute-phase

以 wave 并行化方式执行阶段的所有计划。

| 参数/Flag | 说明 |
|-----------|------|
| `N` | **必填** 阶段号 |
| `--wave N` | 仅执行第 N 个 wave |
| `--validate` | 执行前运行状态验证 |
| `--cross-ai` | 委托给外部 AI CLI 执行 |
| `--no-cross-ai` | 强制本地执行（忽略 config 中的跨 AI 配置） |

**生成**：每个计划的 `{phase}-{N}-SUMMARY.md`、git commits、`{phase}-VERIFICATION.md`

```bash
/gsd-execute-phase 1            # 执行阶段 1 所有计划
/gsd-execute-phase 1 --wave 2   # 仅执行 Wave 2
/gsd-execute-phase 1 --validate # 执行前验证状态
/gsd-execute-phase 2 --cross-ai # 委托给外部 AI 执行
```

> [!warning] 包安装失败时
> 如果安装步骤失败，执行器会暂停并显示 `checkpoint:human-verify`，**不会**自动安装同名替代包（这是防止 slopsquatting 的机制）。手动在注册表页面验证包后再继续。

---

### gsd-verify-work

用户验收测试（UAT）+ 自动诊断。

| 参数 | 说明 |
|------|------|
| `N` | 阶段号（默认最后执行的阶段） |

**生成**：`{phase}-UAT.md`，发现问题时生成修复方案

```bash
/gsd-verify-work 1      # 验收阶段 1
```

---

### gsd-ship

从已完成阶段创建 PR，自动生成 PR 描述。

| 参数/Flag | 说明 |
|-----------|------|
| `N` | 阶段号或里程碑版本（如 `4` 或 `v1.0`） |
| `--draft` | 创建为草稿 PR |

**前提**：阶段已通过 `verify-work`，`gh` CLI 已安装并认证

**PR 描述包含**：ROADMAP.md 中的阶段目标、SUMMARY.md 变更摘要、覆盖的需求 ID、验证状态、关键决策

```bash
/gsd-ship 4             # 发布阶段 4
/gsd-ship 4 --draft     # 创建草稿 PR
```

---

### gsd-complete-milestone / gsd-new-milestone

```bash
/gsd-complete-milestone                     # 归档里程碑，打 git tag
/gsd-new-milestone                          # 开始下一个版本（交互）
/gsd-new-milestone "v2.0 Mobile"            # 指定里程碑名称
/gsd-new-milestone --reset-phase-numbers "v2.0" # 重新从 Phase 1 开始编号
```

---

## 导航与进度命令

### gsd-progress

查看状态并自动跳转到下一个工作流步骤。

| Flag | 说明 |
|------|------|
| `--next` | 自动执行下一个逻辑步骤（无需手动选择） |
| `--do "task"` | 解析自由描述，调度到最合适的 GSD 命令 |
| `--forensic` | 附加 6 项完整性审计（STATE 一致性、孤儿交接、漂移等） |

**`--next` 自动路由逻辑**：
```
无项目         → 建议 /gsd-new-project
阶段需讨论     → 运行 /gsd-discuss-phase
阶段需规划     → 运行 /gsd-plan-phase
阶段需执行     → 运行 /gsd-execute-phase
阶段需验证     → 运行 /gsd-verify-work
所有阶段完成   → 建议 /gsd-complete-milestone
```

```bash
/gsd-progress              # 查看状态和下一步建议
/gsd-progress --next       # 自动执行下一步
/gsd-progress --do "fix the auth bug" # 分发意图
/gsd-progress --forensic   # 标准报告 + 完整性审计
```

---

### gsd-resume-work / gsd-pause-work

```bash
/gsd-resume-work            # 恢复上次会话的上下文

/gsd-pause-work             # 保存当前进度（创建 continue-here.md）
/gsd-pause-work --report    # 保存 + 生成会话报告（commits、变更、进度）
```

---

### gsd-manager

多阶段交互式命令中心，适合同时并行处理多个阶段的高级用户。

```bash
/gsd-manager                    # 打开命令中心仪表板
/gsd-manager --analyze-deps     # 分析 ROADMAP 中的阶段依赖关系
```

---

## 调研与探索命令

### gsd-map-codebase

分析现有代码库的技术栈、架构、约定、风险点。

| Flag | 说明 |
|------|------|
| `--fast` | 快速分析（跳过深度研究） |
| `--query` | 查询已有的代码库分析结果 |

```bash
/gsd-map-codebase
/gsd-map-codebase --fast
/gsd-map-codebase --query
```

---

### gsd-spike

验证技术方案可行性。每次 spike 运行 2-5 个实验，每个实验有 Given/When/Then 假设 + 真实代码 + 裁决。

```bash
/gsd-spike                                    # 交互式
/gsd-spike "can we stream LLM tokens via SSE"
/gsd-spike --quick "websocket vs SSE latency"
/gsd-spike --wrap-up                          # 打包为项目技能，后续会话自动加载
```

---

### gsd-sketch

在写真实组件前，视觉探索布局/交互方案。

```bash
/gsd-sketch "dashboard layout"
/gsd-sketch --quick "sidebar navigation"
/gsd-sketch --wrap-up   # 打包为项目技能
```

---

### gsd-explore

在项目结构内深度研究（代码库、需求、规划制品），给出分析报告。

```bash
/gsd-explore "how does the auth flow work"
```

---

## Backlog 与 Thread 命令

### gsd-capture

```bash
/gsd-capture --backlog "GraphQL API layer"    # 存入 backlog（999.x 编号）
/gsd-capture --seed "Add collab when WS infra is ready"  # 存为带触发条件的 seed
```

### gsd-review-backlog

批量审核 backlog 条目（升级/保留/删除）：

```bash
/gsd-review-backlog
```

### gsd-thread

轻量级跨会话知识记录（不属于特定阶段）：

```bash
/gsd-thread                          # 列出所有 thread
/gsd-thread "Investigate TCP timeout" # 新建 thread
/gsd-thread fix-deploy-key-auth       # 继续已有 thread
```

---

## Workstreams 命令

并行处理多个功能线，各自独立的 `.planning/` 状态：

```bash
/gsd-workstreams create backend-api
/gsd-workstreams switch backend-api
/gsd-workstreams list
/gsd-workstreams complete backend-api
```

---

## 代码质量命令

```bash
/gsd-code-review            # 代码审查
/gsd-code-review --fix      # 审查并自动修复
/gsd-add-tests              # 为现有代码补充测试
/gsd-secure-phase           # 安全审查当前阶段
/gsd-docs-update            # 更新文档
```

---

## 其他实用命令

| 命令 | 说明 |
|------|------|
| `/gsd-quick "fix login bug"` | 快速执行小任务，不走完整工作流 |
| `/gsd-autonomous "add dark mode"` | 完全自主模式，GSD 自行规划并执行 |
| `/gsd-debug` | 诊断和修复当前问题 |
| `/gsd-stats` | 展示项目统计和进度 |
| `/gsd-health` | 检查项目结构完整性 |
| `/gsd-cleanup` | 清理过期的制品文件 |
| `/gsd-forensics` | 完整项目诊断（用于调试问题） |
| `/gsd-undo` | 撤销上一个 GSD 操作 |
| `/gsd-settings` | 修改配置（`.planning/config.json`） |
| `/gsd-update` | 更新 GSD 到最新版本 |

---

## 参考

- [[get-shit-done 概览]]
- [[GSD 实战使用技巧]]
- [COMMANDS.md 原文](https://github.com/gsd-build/get-shit-done/blob/main/docs/COMMANDS.md)
