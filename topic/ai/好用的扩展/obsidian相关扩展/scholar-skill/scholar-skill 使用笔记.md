---
title: scholar-skill 使用笔记
source: "https://github.com/EESJGong/scholar-skill"
description: 基于 OpenClaw 框架的学术研究 Skill，通过 L1-L3 分级阅读将论文转化为结构化 Obsidian 知识体系
author: EESJGong
tags:
  - ai
  - 扩展
  - obsidian
  - skill
  - 学术研究
---

# scholar-skill

> [!info] 项目信息
> - **仓库**：[EESJGong/scholar-skill](https://github.com/EESJGong/scholar-skill)
> - **作者**：EESJGong
> - **许可证**：MIT
> - **框架**：OpenClaw
> - **状态**：测试阶段（Testing）
> - **语言**：英文 / 简体中文双语

在 [[Obsidian]] 中构建 **活的科研知识体系**。不只是一次性摘要，而是将论文阅读转化为可持续演进的结构化笔记、核心记忆与知识冲突检测。

## 核心设计理念

| 传统学术助手 | ScholarSkill |
|------------|-------------|
| 搜索、摘要、记录 | 结构化笔记 + 知识网络 + 认知更新 |
| 孤立的聊天记录 | [[Obsidian]] Vault 中持续生长的知识图谱 |
| 不断追加信息 | 新论文可修正旧理解（知识进化） |
| 被动记录 | 比较论点、验证证据、批判性思考 |

## 分级阅读体系

| 级别 | 策略 | 耗时 | 用途 |
|------|------|------|------|
| **L1** | 快速分发 | 分钟级 | 初筛，判断优先级 |
| **L2** | 标准阅读 | 中等 | 结构化笔记 + 知识链接 |
| **L3** | 深度解构 | ~2.5 小时 | 完整知识提取 + 反思报告 |

> [!warning] Token 消耗警告
> L3 深度阅读为长时间异步挂机任务，依赖 OpenClaw 的 `durable-task-runner` 处理多轮 LLM 推演、API 限流等待和崩溃恢复。如果后端挂载商用前沿模型（如 Claude Sonnet、GPT-4o），**单篇深读可能产生高昂 API 账单**。

## 安装

### 快速安装（推荐）

```bash
git clone https://github.com/EESJGong/scholar-skill.git
cd scholar-skill
```

然后让 OpenClaw Agent 完成安装：

```text
请将此仓库安装为 OpenClaw skill，使用中文包，配置 Obsidian vault 路径为 /你的/Obsidian/Vault
```

### 手动安装

```bash
# 选择语言包并配置 vault 路径
python zh-CN/scripts/configure.py auto --vault-path "/你的/Obsidian/Vault"

# 克隆到共享 skills 目录
git clone https://github.com/EESJGong/scholar-skill.git ~/.openclaw/skills/scholar-skill
```

### 安装依赖 Skill

```bash
cd ~/.openclaw
clawhub install obsidian-direct      # 必须：读写本地 .md 文件
clawhub install arxiv-watcher        # 必须：抓取 ArXiv 文献
clawhub install durable-task-runner  # 核心：L3 长任务调度与断点续传
clawhub install academic-research-hub # 可选：学术研究增强
clawhub install tavily               # 可选：联网搜索
clawhub install pdf                  # 可选：PDF 文本解析
```

## 使用示例

```text
获取这篇文献 ArXiv:2407.19354 并进行处理。
先做 L1 快速评估，如果判定为 P0 优先级，则请在后台直接启动 L3 深度阅读。
完成后将知识树更新推送到我的 Obsidian 对应目录。
```

触发条件：意图匹配到"阅读论文"、"L1/L2/L3 阅读"、"知识内化"或"文献笔记"时自动触发。

## 特殊机制

### 知识冲突检测

当新论文推翻旧笔记结论时，不会直接覆写，而是生成确认单放入 `0-Inbox` 文件夹，等待人工审核（Human in the loop）。

### 周期性反思

内置时间触发器，强制在周末或月末对临时存储的知识进行 L2/L3 反思，生成知识体系演进报告。

### 记忆提取

捕获三类记忆：
- **语义记忆**：概念、定义、关系
- **情景记忆**：阅读过程中的发现与联想
- **程序记忆**：可复用的研究方法论

## 仓库结构

```
scholar-skill/
├── SKILL.md          # 仓库入口
├── en/               # 英文完整包
│   ├── SKILL.md
│   ├── scripts/
│   └── templates/
├── zh-CN/            # 简体中文完整包
│   ├── SKILL.md
│   ├── scripts/
│   └── templates/
└── requirements.txt
```

## 风险与注意事项

| 风险 | 说明 |
|------|------|
| **Token 消耗** | L3 循环 + 高频 RAG 检索消耗大量 Token，商用模型账单可观 |
| **数据覆写** | 底层 `obsidian-direct` 为 Python 暴力文件 I/O，多端同步时易引发冲突 |
| **同步冲突** | iCloud/[[Obsidian]] Sync 期间可能出现文件冲突、内容丢失或双链索引错误 |

> [!tip] 建议
> - 在独立测试 Vault 中运行
> - 开启 Git 快照以便回滚
> - L3 深读前预估 Token 成本

## 相关笔记

- [[Superpowers 使用手册与最佳实践 — 实施计划]]
- [[axton-obsidian-visual-skills 套件总览]]
- [[excalidraw-diagram skill]]
- [[Mermaid 语法规则参考]]
- [[mermaid-visualizer skill]]
- [[obsidian-canvas-creator skill]]
- [[defuddle skill]]
- [[json-canvas skill]]
