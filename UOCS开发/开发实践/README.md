# 开发实践

> 编码规范与 AI 协作准则。开始写代码之前必读。

## 两份核心文档

| 文档 | 说明 |
|------|------|
| [[AI编码行为准则]] | 如何让 AI（Claude Code、Copilot CLI）写出更好的代码 |
| [[编码规范]] | 后端/前端编码约定、Entity 变更联动规则、全局禁止事项 |

## AI 编码行为准则的核心思想

AI 编码工具容易犯的错误：过度设计、静默选择理解、修改无关代码。这份准则从四个维度约束 AI 行为：

1. **Think Before Coding** — 不假设，不隐藏困惑，主动暴露权衡
2. **Simplicity First** — 最小化代码解决问题，不做推测性设计
3. **Surgical Changes** — 只改必须改的，匹配已有风格
4. **Goal-Driven Execution** — 定义可验证的成功标准

## 编码规范的关键规则

### 后端 (Spring Cloud)

- 构造器注入 (`@RequiredArgsConstructor` + `final`)，禁止 `@Autowired`
- DTO 命名：`{动作}{Entity}ReqDTO` / `RespDTO`
- ORM：MyBatis-Plus + XML Mapper

### 前端

- **upda-cloud-client**：函数式组件 + Hooks + MobX + MUI v7
- **中间件查看器**：各自独立（CAD 用 Ant Design，PDF/OFD 用 MUI）

### Entity 变更 5 步流程

Entity 实体类变更时必须按顺序执行：增量 DDL → `schema.sql` → `Mapper.xml` → `Mapper.java` → 检查 DTO。

### 全局红线

- 禁止 `git init` in `upda-code/`
- 禁止硬编码密码
- 禁止直接修改 `drawingweb/`（生成修改报告）
- 禁止静默执行 DDL
