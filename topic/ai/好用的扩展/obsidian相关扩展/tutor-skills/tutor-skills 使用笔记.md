---
title: tutor-skills 使用笔记
source: "https://github.com/RoundTable02/tutor-skills"
description: 将文档或代码库转化为结构化 Obsidian StudyVault，再通过交互式测验追踪知识盲区的闭环学习 Skill
author: Choi Wontak (RoundTable02)
tags:
  - ai
  - 扩展
  - obsidian
  - skill
  - 学习
---

# tutor-skills

> [!info] 项目信息
> - **仓库**：[RoundTable02/tutor-skills](https://github.com/RoundTable02/tutor-skills)
> - **作者**：Choi Wontak
> - **许可证**：MIT
> - **兼容**：[[Claude Code]]、Cursor、Windsurf 等 Agent [[Skills]] 规范工具

两个 Skill 构成 **"输入 → 内化 → 检测"** 完整闭环：将文档或代码库一键转化为结构化的 [[Obsidian]] 知识库（StudyVault），之后通过无提示的交互式测验不断暴露知识盲区并记录学习轨迹。

## 工作流概览

```
Documents / Code                Obsidian                Quiz Session
┌──────────────┐           ┌──────────────┐         ┌──────────────┐
│ PDF, MD,     │ /tutor    │ StudyVault/  │ /tutor  │ 4 题/轮，     │
│ HTML, EPUB,  │──setup──▶ │ 结构化笔记   │────────▶│ 概念级追踪    │
│ 源码项目     │           │ + MOC + 练习 │         │ + 进度更新    │
└──────────────┘           └──────────────┘         └──────┬───────┘
                                     ▲                       │
                                     └─── 进度回写 ──────────┘
```

## 两个 Skill

| Skill | 命令 | 功能 | 输入 | 输出 |
|-------|------|------|------|------|
| **tutor-setup** | `/tutor-setup` | 生成 StudyVault | 文档或源码 | [[Obsidian]] 笔记 + 仪表盘 + 练习题 |
| **tutor** | `/tutor` | 交互测验 | 已有 StudyVault | 测验会话 + 概念级进度追踪 |

## 安装

```bash
# 一行安装（推荐，需 npx skills）
npx skills add RoundTable02/tutor-skills

# 手动安装
git clone https://github.com/RoundTable02/tutor-skills.git
cd tutor-skills && ./install.sh
```

> [!tip] 前置要求
> - [[Claude Code]] CLI
> - [Obsidian](https://obsidian.md/)（用于查看和复习生成的 StudyVault）

## tutor-setup 详解

### 模式自动侦测

| 检测到文件 | 模式 |
|-----------|------|
| `package.json`、`pom.xml`、`Cargo.toml`、`go.mod` 等项目文件 | **代码库模式** |
| 无项目标记 | **文档模式** |

### 文档模式（9 阶段）

将 PDF、文本、网页等转化为学习笔记。

| 阶段 | 名称 | 关键动作 |
|------|------|---------|
| D1 | 源发现 | 扫描文件，提取内容，验证映射 |
| D2 | 内容分析 | 构建主题层级和依赖图 |
| D3 | 标签规范 | 定义英文 kebab-case 标签体系 |
| D4 | Vault 结构 | 按主题创建编号文件夹 |
| D5 | 仪表盘 | MOC + Quick Reference + 考试陷阱 |
| D6 | 概念笔记 | 结构化笔记，含表格、图示、callout |
| D7 | 练习题 | 每主题 8+ 题，可折叠答案（主动回忆） |
| D8 | 互链 | wiki-links 全文交叉引用 |
| D9 | 自检 | 对照质量清单验证 |

生成结构：

```
StudyVault/
  00-Dashboard/          # MOC + Quick Reference + Exam Traps
  01-<Topic1>/           # 概念笔记 + 练习题
  02-<Topic2>/
  ...
```

### 代码库模式（9 阶段）

将源码项目转化为新开发者上手指南。

| 阶段 | 名称 | 关键动作 |
|------|------|---------|
| C1 | 项目探索 | 扫描文件、检测技术栈、映射目录 |
| C2 | 架构分析 | 识别模式、追踪请求流、映射模块边界 |
| C3 | 标签规范 | 定义 `#arch-*`、`#module-*`、`#pattern-*` |
| C4 | Vault 结构 | 仪表盘 + 按模块分文件夹 |
| C5 | 仪表盘 | MOC + 模块图 + API 接口 + Getting Started |
| C6 | 模块笔记 | 用途、关键文件、接口、流程、依赖 |
| C7 | 上手练习 | 代码阅读、配置、调试、扩展任务 |
| C8 | 互链 | 模块与练习交叉链接 |
| C9 | 自检 | 对照质量清单验证 |

## tutor 详解

基于概念级的交互式测验，追踪"你知道什么 / 不知道什么"。

### 会话类型

| 类型 | 触发条件 | 重点 |
|------|---------|------|
| 诊断性测评 | 存在未测量区域（⬜） | 新领域广泛评估 |
| 针对弱项 | 存在弱项（🟥/🟨） | 薄弱环节定向练习 |
| 自选章节 | 始终可用 | 按需复习任意区域 |
| 高难度回顾 | 全部区域 🟩/🟦 | 挑战已掌握内容 |

### 测验流程

1. 检测 StudyVault 并读取学习仪表盘
2. 根据当前掌握度呈现会话选项
3. 每轮 4 道题（4 选 1，零提示）
4. 评分并解释错题
5. 自动更新概念文件和仪表盘

### 进度追踪

| 标记 | 等级 | 正确率 |
|------|------|--------|
| 🟥 | 薄弱 | 0–39% |
| 🟨 | 一般 | 40–69% |
| 🟩 | 良好 | 70–89% |
| 🟦 | 精通 | 90–100% |
| ⬜ | 未测 | 无数据 |

概念级追踪记录：尝试次数、正确次数、最后测试日期、错题笔记。后续练习会在新语境中复述错题概念（而非重复原题）。

## 学习循环

```
  /tutor-setup → 在 Obsidian 中阅读笔记 → /tutor 诊断测验
                                              ↓
         ← 在 Obsidian 中复习弱项 ← ← ← 查看结果，针对弱项 /tutor 再测
```

## 卸载

```bash
./uninstall.sh
# 或手动
rm -rf ~/.claude/skills/tutor-setup ~/.claude/skills/tutor
```
