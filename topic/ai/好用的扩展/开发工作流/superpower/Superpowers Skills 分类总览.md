---
title: "Superpowers Skills 分类总览"
tags:
  - ai
  - 扩展
  - superpowers
description: Superpowers v5.1.0 全部 14 个 skill，按测试类、协作类、元技能三大维度分类
source: https://github.com/obra/superpowers
---

# Superpowers Skills 分类总览

> 基于 Superpowers v5.1.0（作者 Jesse Vincent），共 14 个 skill，按**测试类、协作类、元技能**三大维度整理。
> Superpowers 是 Claude Code 官方核心技能库，提供完整的软件开发方法论：从头脑风暴到分支完成。

---

## 一、测试类（5 个）

> 覆盖 TDD、调试、代码审查、完成验证——确保代码质量的铁律组。

| Skill | 命令 | 用途 |
|-------|------|------|
| **test-driven-development** | `/superpowers:test-driven-development` | 严格 RED-GREEN-REFACTOR 循环。铁律：没有失败的测试就不写生产代码——写了就删掉重来 |
| **systematic-debugging** | `/superpowers:systematic-debugging` | 四阶段调试法：根因调查 → 模式分析 → 假设验证 → 最小修复。铁律：无根因不修复 |
| **verification-before-completion** | `/superpowers:verification-before-completion` | 完成前强制验证。铁律：没有新鲜证据就不声称完成。禁止"应该能用了"、"我很有信心" |
| **requesting-code-review** | `/superpowers:requesting-code-review` | 调度代码审查子 Agent，按严重度分级处理反馈（Critical/Important/Minor） |
| **receiving-code-review** | `/superpowers:receiving-code-review` | 正确接收审查反馈：读→理解→验证→评估→回应→实施。禁止表演性赞同，鼓励技术反驳 |

### 三条铁律

```
TDD:    没有失败的测试 → 不写生产代码（写了删掉重来）
调试:   没有根因分析 → 不提修复方案
验证:   没有运行证据 → 不声称完成
```

### 测试类典型流程

```
/test-driven-development → /systematic-debugging → /requesting-code-review
         ↓                        ↓                       ↓
    红-绿-重构循环          遇到 bug 时启动          每个 task 完成后触发

/receiving-code-review → /verification-before-completion
         ↓                        ↓
    处理审查反馈              最终验证后才声明完成
```

---

## 二、协作类（7 个）

> 覆盖从需求探索到分支完成的完整协作工作流。Superpowers 的核心是一条标准流水线。

### 需求与设计（2 个）

| Skill | 命令 | 用途 |
|-------|------|------|
| **brainstorming** | `/superpowers:brainstorming` | 苏格拉底式设计细化：逐个提问 → 2-3 方案对比 → 写 spec 到 `docs/superpowers/specs/` → 用户确认后转 writing-plans |
| **writing-plans** | `/superpowers:writing-plans` | 将 spec 拆分为 2-5 分钟的 TDD 小任务，假设工程师零上下文。禁止占位符（TBD、"添加适当错误处理"等） |

### 执行与调度（3 个）

| Skill | 命令 | 用途 |
|-------|------|------|
| **subagent-driven-development** | `/superpowers:subagent-driven-development` | 主力执行方式：每个 task 调度独立子 Agent，含规格审查 + 代码质量审查双重检查 |
| **dispatching-parallel-agents** | `/superpowers:dispatching-parallel-agents` | 面对 2+ 个独立问题时，并行调度多个专用子 Agent 各自解决 |
| **executing-plans** | `/superpowers:executing-plans` | 顺序执行计划（当子 Agent 不可用时的降级方案），逐步验证 |

### 分支完成（1 个）

| Skill | 命令 | 用途 |
|-------|------|------|
| **finishing-a-development-branch** | `/superpowers:finishing-a-development-branch` | 实现完成后引导决策：本地合并 / 创建 PR / 保留现状 / 丢弃。自动检测 worktree 并清理 |

### 工作流集成（1 个）

| Skill | 命令 | 用途 |
|-------|------|------|
| **using-git-worktrees** | `/superpowers:using-git-worktrees` | 在独立 worktree 中开始功能开发，保证工作区隔离。优先用原生工具，降级到手动 `git worktree add` |

### 标准协作流水线

```
brainstorming → using-git-worktrees → writing-plans
     ↓                  ↓                  ↓
  需求探索          工作区隔离          任务拆分
                                          ↓
                               subagent-driven-development
                               （或 executing-plans 降级方案）
                                          ↓
                    ┌─────────────────────┼─────────────────────┐
                    ↓                     ↓                     ↓
            test-driven-          requesting-code-      receiving-code-
            development            review                  review
                    ↓                     ↓                     ↓
              TDD 循环              调度审查              处理反馈
                    └─────────────────────┼─────────────────────┘
                                          ↓
                              verification-before-completion
                                          ↓
                              finishing-a-development-branch
                                          ↓
                                合并 / PR / 保留 / 丢弃
```

---

## 三、元技能（2 个）

> 控制 Superpowers 自身行为的引导技能。

| Skill | 命令 | 用途 |
|-------|------|------|
| **using-superpowers** | `/superpowers:using-superpowers` | 元引导：会话启动时建立 skill 发现与使用规则。核心原则——只要有 1% 可能适用的 skill，就必须先调用。优先级：用户指令 > Superpowers skill > 系统默认 |
| **writing-skills** | `/superpowers:writing-skills` | 用 TDD 方法编写新 skill：先写失败测试场景 → 写最小 skill → 重构完善。覆盖 skill 类型（technique/pattern/reference）、目录结构、frontmatter 格式、CSO 描述优化 |

---

## 总览图

```
                ┌──────────────────────────────────┐
                │   Superpowers v5.1.0  (14 Skills) │
                │   obra/superpowers · MIT License   │
                └───────────────┬──────────────────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
  ┌──────▼──────┐       ┌──────▼──────┐        ┌──────▼──────┐
  │  测试类 (5)  │       │  协作类 (7)  │        │  元技能 (2)  │
  └──────┬──────┘       └──────┬──────┘        └──────┬──────┘
         │                      │                      │
    ┌────┼────┐          ┌─────┼─────┐             ┌──┴──┐
    │    │    │          │     │     │             │     │
   TDD  调试 验证      设计   执行   完成       引导  编写
                审查×2                        自身  新 skill
```

## 相关笔记

- [["Superpowers：编码 Agent 技能框架"]]
- [["Superpowers 使用手册与最佳实践"]]
- [["Superpowers 实战：用 TDD 工作流构建生产功能"]]
- [["Superpowers：我在 2025 年 10 月如何使用编码代理"]]
- [[gstack Skills 分类总览]]
