---
title: GSD 实战使用技巧
tags:
  - ai/工具
  - ai/claude-code
  - 开发工作流
  - 实战
aliases:
  - GSD 技巧
source: https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md
---

# GSD 实战使用技巧

> [!tip] 前置阅读
> 先看 [[get-shit-done 概览]] 了解基础工作流。

## 典型项目端到端流程

以"Express webhook 签名验证中间件"为例：

```
/gsd-new-project
```

GSD 会提问：
```
> What are you building?
  A webhook signature validator middleware for Express apps.
> Who's the user?
  Backend developers integrating third-party webhooks (Stripe, GitHub, Shopify).
```

↓ 并行研究代理运行 → 提取需求 → 生成路线图 → **你审核批准**

↓

```
/gsd-discuss-phase 1    # 明确灰区决策，进入规划
/gsd-plan-phase 1       # 生成原子化任务计划
/gsd-execute-phase 1    # 并行执行，每个任务独立 commit
/gsd-verify-work 1      # 验收，失败则生成修复方案
/gsd-ship 1             # 创建 PR
```

## 接手现有代码库

> [!warning] 必须先分析代码库，再初始化项目
> 直接运行 `/gsd-new-project` 会导致 GSD 不了解现有代码的架构约定。

正确顺序：

```bash
/gsd-map-codebase          # 并行分析技术栈、架构、约定、风险点
/gsd-new-project           # 此时会加载代码库上下文，提问更精准
```

`/gsd-map-codebase` 的选项：
- `--fast`：快速分析（跳过深度研究）
- `--query`：查询已有的代码库分析

## 回到进行中的项目

> [!important]
> 每次新会话回到项目时，先重建上下文：

```bash
/gsd-map-codebase       # 重新索引代码库
/gsd-new-project        # 重建 GSD 规划上下文（代码不会被改动）
```

或者直接：
```bash
/gsd-progress --next    # 自动检测上次停在哪，继续执行
```

## 在规划前做技术调研（Spike）

不确定技术方案可行性时，先 spike 再规划：

```bash
/gsd-spike "can we stream LLM tokens through SSE"
/gsd-spike --quick "websocket vs SSE latency"
```

每次 spike 会：
1. 写出 Given/When/Then 假设
2. 跑真实代码（非伪代码）
3. 给出 `VALIDATED / INVALIDATED / PARTIAL` 裁决

结果存入 `.planning/spikes/NNN-name/README.md`。

完成后打包为项目技能，后续会话自动加载：
```bash
/gsd-spike --wrap-up
```

## 视觉探索（Sketch）

在写真正的组件代码前，先比较布局方案：

```bash
/gsd-sketch "dashboard layout"
/gsd-sketch --quick "sidebar navigation"
```

## 管理 Backlog

不成熟的想法放进 backlog，用 `999.x` 编号隔离在活跃阶段之外：

```bash
/gsd-capture --backlog "GraphQL API layer"     # 创建 999.1-graphql-api-layer/
/gsd-capture --backlog "Mobile responsive"     # 创建 999.2-mobile-responsive/
```

当 backlog 的想法成熟时：
```bash
/gsd-discuss-phase 999.1   # 进一步探索
/gsd-plan-phase 999.1      # 开始规划
```

批量审核 backlog：
```bash
/gsd-review-backlog        # 显示所有 backlog，可升级/保留/删除
```

## Seeds：带触发条件的未来想法

Seeds 在特定里程碑到达时自动浮现（不同于 backlog 需要手动管理）：

```bash
/gsd-capture --seed "Add real-time collab when WebSocket infra is in place"
```

运行 `/gsd-new-milestone` 时，GSD 会扫描所有 seeds 并展示匹配项。

## 跨会话上下文 Thread

轻量级跨会话知识记录，不属于任何特定阶段：

```bash
/gsd-thread                          # 列出所有 thread
/gsd-thread "Investigate TCP timeout" # 新建 thread
/gsd-thread fix-deploy-key-auth       # 继续已有 thread
```

## 并行工作流（Workstreams）

同时处理多个不相关功能线，各自有独立的 `.planning/` 状态，互不干扰：

```bash
/gsd-workstreams create backend-api
/gsd-workstreams create frontend-dashboard
/gsd-workstreams switch backend-api   # 切换到 backend 上下文
/gsd-workstreams list                 # 查看所有工作流
/gsd-workstreams complete backend-api # 完成并归档
```

## 配置技巧

### yolo 模式（全自动）

适合对流程有信心、想减少中断时：

```json
// .planning/config.json
{
  "mode": "yolo"
}
```

### 降低 token 消耗

```json
{
  "workflow": {
    "research": false,
    "plan_check": false,
    "verifier": false
  }
}
```

> [!warning]
> 关闭这三个选项会降低输出质量，仅在本地小模型或预算紧张时使用。

### 模型档位

| 档位 | 适用场景 |
|------|---------|
| `quality` | 重要项目，预算充足 |
| `balanced` | 日常开发（推荐默认） |
| `budget` | 原型验证、本地模型 |

## 常见问题排查

### 命令不显示

安装后重启运行时。GSD 安装位置：
- [[Claude Code]]：`~/.claude/skills/gsd-*/`
- Codex：`~/.codex/skills/gsd-*/`
- [[Copilot]]：`~/.github/`

### STATE.md 状态不同步

```bash
node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs" state validate  # 检测漂移
node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs" state sync      # 修复同步
```

### 重新安装（幂等，不会破坏现有状态）

```bash
npx get-shit-done-cc@latest
```

### Docker / 容器环境

```bash
CLAUDE_CONFIG_DIR=/home/youruser/.claude npx get-shit-done-cc --global
```

## 参考

- [[get-shit-done 概览]]
- [[GSD 架构原理]]
- [USER-GUIDE.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/USER-GUIDE.md)
- [COMMANDS.md](https://github.com/gsd-build/get-shit-done/blob/main/docs/COMMANDS.md)

## 相关笔记

- [[GSD 命令参考]]
- [[更新日志]]
- [[配置体系]]
- [[插件]]
- [[Agent 系统]]
- [[Copilot CLI+Claude Code双工具协同实践]]
