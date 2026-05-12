# gstack 使用手册设计规格

日期：2026-05-12  
状态：已锁定

---

## 目标与受众

**目标**：社区分享级别的教学文档，兼顾入门引导与深度实践。  
**受众**：已了解 Claude Code 基础、想将 gstack Sprint 方法论落地的开发者。  
**对标**：与同目录下 Superpowers 使用手册形成对照组（同一场景，不同工具）。

---

## 核心场景

**产品**：Next.js Todo 应用（与 Superpowers 手册一致）  
**新功能**：为 Todo 列表添加 Markdown 导出功能  
**对照价值**：读者可直接对比 gstack vs Superpowers 两套方法论在同一任务上的差异

---

## 文档结构

### 前言

- gstack 是什么（Garry Tan 设计，YC President，20 年产品构建经验）
- Sprint 方法论核心思想（Think → Plan → Build → Review → Test → Ship → Reflect）
- 与 Superpowers 的定位差异（角色扮演 vs 工作流编排）
- 安装一行命令（wikilink 到 `[[gstack]]` 详细说明）

### 第一站：/office-hours — 产品需求对齐

4 层结构：
1. 为什么：写代码前先做产品论证，避免方向错误
2. 怎么运作：CEO 视角审查需求、用户故事、优先级
3. 场景演示：用 /office-hours 讨论 Markdown 导出功能的必要性
4. 最佳实践：何时跳过、何时必须做

### 第二站：/plan-ceo-review + /plan-eng-review — 双视角规划

4 层结构：
1. 为什么：商业可行性与工程可行性双重验证
2. 怎么运作：两个 skill 的分工与输出物
3. 场景演示：Markdown 导出的 CEO 审查（ROI/风险）+ 工程审查（技术方案）
4. 最佳实践：何时叠加 /plan-design-review，何时用 /autoplan 替代

### 第三站：编码阶段 — /careful 守护实现

4 层结构：
1. 为什么：高风险变更需要额外保护
2. 怎么运作：/careful 模式启动、/freeze + /guard 锁定关键文件
3. 场景演示：实现导出功能时用 /careful，锁定核心 Todo 逻辑
4. 最佳实践：什么情况必须 /freeze，什么情况可以省略

### 第四站：/review — 代码审查

4 层结构：
1. 为什么：多角色视角发现人工盲点
2. 怎么运作：/review 的审查维度（逻辑/安全/性能/可读性）
3. 场景演示：导出功能代码的 /review 输出示例
4. 最佳实践：/codex 作为第二意见的用法

### 第五站：/qa + /design-review — 质量验收

4 层结构：
1. 为什么：功能正确性与设计一致性分开验证
2. 怎么运作：/qa 测试流程、/design-review 视觉检查
3. 场景演示：导出按钮的 QA 场景 + 设计一致性审查
4. 最佳实践：/qa-only 快速回归的场景

### 第六站：/ship + /canary — 安全发布

4 层结构：
1. 为什么：发布是风险最高的节点
2. 怎么运作：/ship 预检、/canary 灰度验证
3. 场景演示：Markdown 导出功能的发布流程
4. 最佳实践：何时需要 /canary，何时直接 /ship

### 第七站：/retro — 复盘闭环

4 层结构：
1. 为什么：学习沉淀，避免重复犯同类错误
2. 怎么运作：/retro 输出结构（What went well / Improvements / Actions）
3. 场景演示：本次 Sprint 复盘示例
4. 最佳实践：与 /document-release 配合记录决策

### 进阶篇

#### 并行 Sprint（Conductor 模式）
- 10-15 个 Claude Code 会话同时推进
- 任务切分原则（互不干扰的子任务）
- Conductor 角色职责

#### 设计流水线
- /design-shotgun → /design-html → /design-review 三段式
- 何时启动完整设计流水线

#### GBrain 持久记忆
- /setup-gbrain 初始化
- /sync-gbrain 会话间知识传递
- 适合存入 GBrain 的内容类型

#### /investigate 深度调查
- 与普通 /review 的区别
- 适合的问题类型（性能瓶颈、神秘 Bug）

#### /cso 安全审查
- 触发时机（auth、支付、用户数据变更）
- 与 common/security 规则的配合

#### /learn 跨会话学习
- 将本次 Sprint 的技术决策写入长期记忆

### 附录

- 完整 Sprint 技能速查表（Mermaid 流程图）
- 与 Superpowers 方法论对照表
- 常见问题 FAQ

---

## 格式约定

- **frontmatter**：tags, created, aliases
- **agent 对话**：`[!agent]` / `[!user]` callout 块
- **流程图**：Mermaid（Sprint 总览、技能分布）
- **提示块**：`[!tip]`、`[!warning]`、`[!best-practice]`
- **wikilink**：`[[gstack]]` 指向现有说明文档，`[[Superpowers 使用手册与最佳实践]]` 用于对照引用
- **行内代码**：skill 名称如 `/office-hours`、`/ship`

---

## 目标规模

约 7000–8000 汉字，单文件 MOC，镜像 Superpowers 手册密度。

---

## 验收标准

- [ ] 7 个 Station 各含 4 层结构（为什么/怎么运作/场景演示/最佳实践）
- [ ] 全程贯穿同一场景（Next.js Todo + Markdown 导出）
- [ ] 包含至少 2 个 Mermaid 图（Sprint 总览 + 技能速查）
- [ ] 进阶篇覆盖并行 Sprint、GBrain、/cso、/investigate
- [ ] wikilink 到现有 `[[gstack]]` 文档
- [ ] 与 Superpowers 手册有明确对照点（前言 + 附录）
- [ ] 无硬编码 URL，所有引用通过 wikilink
