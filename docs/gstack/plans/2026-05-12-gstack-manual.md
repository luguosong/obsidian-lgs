# gstack 使用手册实施计划

日期：2026-05-12  
规格：`docs/gstack/specs/2026-05-12-gstack-manual-design.md`  
输出：`topic/ai/好用的扩展/开发工作流/gstack/gstack 使用手册与最佳实践.md`

---

## 执行顺序

### Phase 1 — 骨架与前言（subagent A）

**任务**：生成文件骨架 + 前言部分

输出物：
- frontmatter（tags, created, aliases）
- 前言（gstack 简介、Sprint 方法论、与 Superpowers 对比定位、安装命令 wikilink）
- Sprint 总览 Mermaid 流程图

验证：前言 ~500 字，Mermaid 可渲染，wikilink 格式正确

---

### Phase 2 — 核心旅程 Station 1–4（subagent B）

**任务**：写第一至四站正文

内容：
- 第一站：/office-hours（产品需求对齐）
- 第二站：/plan-ceo-review + /plan-eng-review（双视角规划）
- 第三站：编码阶段 + /careful + /freeze + /guard
- 第四站：/review + /codex 第二意见

格式要求：每站 4 层（为什么/怎么运作/场景演示/最佳实践），含 [!agent]/[!user] callout 对话

验证：4 站各含完整 4 层，场景贯穿 Next.js Todo Markdown 导出

---

### Phase 3 — 核心旅程 Station 5–7（subagent C）

**任务**：写第五至七站正文

内容：
- 第五站：/qa + /design-review（质量验收）
- 第六站：/ship + /canary（安全发布）
- 第七站：/retro + /document-release（复盘闭环）

格式要求：同 Phase 2

验证：3 站各含完整 4 层，场景连贯

---

### Phase 4 — 进阶篇（subagent D）

**任务**：写进阶篇 6 个主题

内容：
- 并行 Sprint（Conductor 模式）
- 设计流水线（/design-shotgun → /design-html → /design-review）
- GBrain 持久记忆（/setup-gbrain + /sync-gbrain）
- /investigate 深度调查
- /cso 安全审查
- /learn 跨会话学习

验证：6 个主题各含场景说明 + 最佳实践

---

### Phase 5 — 附录与合并（subagent E）

**任务**：生成附录并合并全文

内容：
- 技能速查 Mermaid 流程图（按 Sprint 阶段分组）
- 与 Superpowers 对照表（Markdown 表格）
- FAQ（3–5 条常见问题）
- 将 Phase 1–4 内容合并为单文件

验证：
- 总字数 7000–8000 汉字
- 所有 wikilink 格式正确
- 无重复章节标题

---

### Phase 6 — 质量审查

**任务**：code-reviewer subagent 审查最终文档

检查项：
- 验收标准全部通过
- 格式一致（callout 类型、Mermaid 语法、frontmatter）
- 场景连贯性（同一个 Todo 应用贯穿始终）
- 与 Superpowers 手册风格对齐

---

## 并行策略

Phase 2、3、4 可并行执行（内容互不依赖）。  
Phase 1 必须先完成（提供文件骨架和 frontmatter）。  
Phase 5 在 Phase 1–4 全部完成后执行。  
Phase 6 在 Phase 5 完成后执行。
