# Copilot CLI 扩展手册

> **本文档记录当前电脑（主机：10545）上已配置的 GitHub Copilot CLI 全部扩展。**
> 涵盖 Plugins、MCP Servers、Custom Skills、Custom Agents 四类，后续可按需扩充各章节。
>
> - **电脑**：主机 10545 / 用户 `luguosong`
> - **配置根目录**：`C:\Users\10545\.copilot\`
> - **最后更新**：2026-05-19

---

## 扩展类型速览

| 类型 | 调用方式 | 存储位置 | 管理方式 |
|------|---------|---------|---------|
| **Plugin**（marketplace） | `/<plugin>:<cmd>` 或 `--agent <plugin>:<agent>` | `~/.copilot/installed-plugins/` | `copilot plugin` 子命令 |
| **MCP Server** | AI 自动调用工具 | `~/.copilot/mcp-config.json` | `copilot mcp` 子命令 |
| **Custom Skill**（本地） | Session 中直接引用 | `~/.copilot/global-skills/` 或项目 `.github/skills/` | 手动创建 `.md` 文件 |
| **Custom Agent** | `--agent <name>` | 项目 `.github/agents/` | 手动创建文件 |

---

## Plugins

> **当前已安装：12 个**
>
> | 来源 | 数量 | 安装位置 |
> |------|------|---------|
> | `awesome-copilot`（社区） | 11 个 | `~/.copilot/installed-plugins/awesome-copilot/` |
> | `copilot-plugins`（官方） | 1 个 | `~/.copilot/installed-plugins/copilot-plugins/` |

### Plugin 管理命令

```bash
# 安装插件
copilot plugin install <插件名>@awesome-copilot

# 查看已安装插件
copilot plugin list

# 更新插件（全部 / 指定）
copilot plugin update
copilot plugin update java-development

# 在 Session 中使用 slash command
/<插件名>:<命令名>

# 在 Session 中使用 agent
copilot --agent <插件名>:<agent名>
```

---

### java-development

**定位**：Java 全栈开发最佳实践（Spring Boot、JUnit 5、Javadoc）

#### Slash Commands

| 命令 | 说明 | 使用场景 |
|------|------|---------|
| `/java-development:java-springboot` | Spring Boot 最佳实践指导 | 编写 Controller/Service/配置类时 |
| `/java-development:java-junit` | JUnit 5 单元测试规范 | 编写测试时获取最佳实践 |
| `/java-development:java-docs` | Javadoc 文档规范 | 为 Java 类型添加文档注释 |
| `/java-development:create-spring-boot-java-project` | 创建 Spring Boot 项目骨架 | 新增微服务模块时 |

#### 典型用法

```
# 让 Copilot 按 Spring Boot 规范审查当前 Service 类
/java-development:java-springboot 请审查这个 Service 类是否符合 Spring Boot 最佳实践

# 为当前文件生成 JUnit 5 测试
/java-development:java-junit 为 SealService 生成覆盖主要分支的 JUnit 5 测试

# 为接口方法补充 Javadoc
/java-development:java-docs 为当前文件中缺少 Javadoc 的公开方法补充文档注释
```

---

### testing-automation

**定位**：TDD 工作流 + JUnit 5 + Playwright 测试全栈支持

#### Slash Commands

| 命令 | 说明 |
|------|------|
| `/testing-automation:java-junit` | JUnit 5 测试最佳实践 |
| `/testing-automation:playwright-generate-test` | 基于场景生成 Playwright 测试 |
| `/testing-automation:playwright-explore-website` | 使用 Playwright 探索网站行为 |

#### Agents（TDD 三件套）

| Agent | 阶段 | 说明 |
|-------|------|------|
| `tdd-red` | 红灯 | 先写失败的测试，描述期望行为 |
| `tdd-green` | 绿灯 | 实现最小代码让测试通过 |
| `tdd-refactor` | 重构 | 在绿灯基础上重构，保持测试通过 |
| `playwright-tester` | E2E | Playwright 专项测试模式 |

#### TDD 工作流示例

```
# 第一步：写失败的测试（Red）
copilot --agent testing-automation:tdd-red
> 我需要为 OcspService.checkCertStatus() 方法编写测试，该方法应验证证书状态

# 第二步：实现代码（Green）
copilot --agent testing-automation:tdd-green
> 让 checkCertStatus 测试通过，只实现最小必要代码

# 第三步：重构（Refactor）
copilot --agent testing-automation:tdd-refactor
> 重构 checkCertStatus 实现，提高可读性，保持测试绿灯
```

---

### frontend-web-dev

**定位**：React 19 前端开发 + Playwright E2E 测试

#### Slash Commands

| 命令 | 说明 |
|------|------|
| `/frontend-web-dev:playwright-generate-test` | 基于场景生成 Playwright 测试 |
| `/frontend-web-dev:playwright-explore-website` | 探索网站测试行为 |

#### Agents

| Agent | 说明 |
|-------|------|
| `expert-react-frontend-engineer` | React 19 专家：现代 hooks、Server Components、Actions、TypeScript、性能优化 |
| `electron-angular-native` | Electron + Angular 代码审查（本项目不适用） |

#### 典型用法

```
# 使用 React 19 专家 agent 审查组件
copilot --agent frontend-web-dev:expert-react-frontend-engineer
> 审查 SealListPage 组件，指出不符合 React 19 最佳实践的写法

# 生成签章流程的 E2E 测试
/frontend-web-dev:playwright-generate-test
> 场景：用户登录后，进入印章管理页，创建新印章，验证列表中出现新印章
```

---

### context-engineering

**定位**：跨模块/多文件变更前的上下文规划（本项目跨多子仓库必备）

#### Slash Commands

| 命令 | 说明 | 最佳时机 |
|------|------|---------|
| `/context-engineering:context-map` | 生成任务相关文件地图 | 动手前，理清影响范围 |
| `/context-engineering:what-context-needed` | 询问 Copilot 需要哪些文件 | 任务说明后，让 AI 自报所需文件 |
| `/context-engineering:refactor-plan` | 多文件重构计划（含回滚步骤） | 跨模块重构前 |

#### Agents

| Agent | 说明 |
|-------|------|
| `context-architect` | 规划多文件变更：识别依赖、生成执行顺序 |

#### 推荐工作流

```
# 改动前先生成 context map
/context-engineering:context-map
> 我要修改 service-seal 的证书绑定流程，请生成相关文件地图

# 让 Copilot 告诉你需要哪些文件
/context-engineering:what-context-needed
> 我需要在 service-signer 中添加 PDF 签章批量接口，你需要看哪些文件？
```

---

### database-data-management

**定位**：SQL 性能优化 + 代码审查（MySQL + MyBatis-Plus 场景）

#### Slash Commands

| 命令 | 说明 |
|------|------|
| `/database-data-management:sql-optimization` | SQL 性能优化（支持 MySQL/PostgreSQL/SQL Server/Oracle） |
| `/database-data-management:sql-code-review` | SQL 安全 + 可维护性审查（含 SQL 注入防护） |
| `/database-data-management:postgresql-optimization` | PostgreSQL 专项优化（本项目使用 MySQL，参考价值有限） |
| `/database-data-management:postgresql-code-review` | PostgreSQL 专项代码审查 |

#### Agents

| Agent | 说明 |
|-------|------|
| `postgresql-dba` | PostgreSQL DBA 模式（本项目不适用） |
| `ms-sql-dba` | SQL Server DBA 模式（本项目不适用） |

#### 典型用法

```
# 优化 MyBatis Mapper 中的慢查询
/database-data-management:sql-optimization
> 以下 SQL 在数据量大时很慢，请给出优化建议和索引策略：
> SELECT * FROM t_cert WHERE user_id = ? AND status = 1 ORDER BY create_time DESC

# 审查新写的 Mapper XML
/database-data-management:sql-code-review
> 审查以下 Mapper SQL 是否存在安全漏洞或性能问题
```

---

### project-documenter

**定位**：自动生成项目文档（C4 架构图 + Markdown + Word）

#### Agents

| Agent | 说明 |
|-------|------|
| `project-documenter` | 自动扫描代码库，生成 C4 架构图、Markdown 文档、Word 文档 |

#### Skills（内置）

| Skill | 说明 |
|-------|------|
| `drawio` | 生成 `.drawio` 文件并导出 PNG |
| `md-to-docx` | 将 Markdown 转为 Word（`.docx`），嵌入 PNG 图片 |

#### 生成内容结构

```
docs/
├── project-summary.md      # 10 节 Markdown 文档
├── project-summary.docx    # Word 文档（含目录、内嵌图片）
└── diagrams/
    ├── high-level-architecture.drawio     # C4 Context 图
    ├── processing-pipeline.drawio         # C4 Container 图
    └── component-relationships.drawio     # C4 Component 图
```

#### 典型用法

```
# 为某个子模块生成文档
copilot --agent project-documenter:project-documenter
> 为 upda-cloud/upda-cloud-server/service-ca 生成项目文档，包含架构图和 Word 文档

# 为整个微服务体系生成架构文档
> 扫描 upda-cloud/upda-cloud-server 的服务拓扑，生成 C4 Context 架构图
```

---

### doublecheck

**定位**：AI 输出验证（三层检验：自检 → 来源核实 → 对抗审查）

#### 使用模式

**持续模式**（整个会话生效，推荐）：

```
use doublecheck
```

开启后，每个含事实声明的回答都会附带可信度评级：

| 评级 | 含义 |
|------|------|
| VERIFIED | 找到支撑来源 |
| PLAUSIBLE | 符合常识，未找到具体来源 |
| UNVERIFIED | 无法确认 |
| DISPUTED | 找到矛盾证据 |
| FABRICATION RISK | 符合幻觉模式（高风险） |

**单次验证**：

```
use doublecheck to verify: <粘贴需要验证的 AI 输出>
```

**关闭**：

```
turn off doublecheck
```

#### 适用场景

- 查询国密标准（GM/T）规范细节时
- 涉及 OCSP/TSA/CRL 协议实现细节时
- 参考第三方库版本兼容性声明时

---

### security-best-practices

**定位**：AI Prompt 安全审查与改进

#### Slash Commands

| 命令 | 说明 |
|------|------|
| `/security-best-practices:ai-prompt-engineering-safety-review` | 全面分析 Prompt 的安全性、偏见、漏洞，给出改进建议 |

#### 典型用法

```
/security-best-practices:ai-prompt-engineering-safety-review
> 审查以下用于 drawing-ai-server 的 RAG 系统 prompt，检查是否存在注入风险：
> [粘贴 system prompt]
```

---

### advanced-security

> 📌 **来源**：`github/copilot-plugins`（GitHub 官方插件市场）

**定位**：代码提交前的安全守门员——扫描密钥泄露 + 依赖漏洞（对接 GitHub Advisory Database）

```bash
copilot plugin install advanced-security@copilot-plugins
```

#### Skills（对话中自动激活）

| Skill | 触发场景 | 说明 |
|-------|---------|------|
| `secret-scanning` | 询问"检查代码有没有密钥/凭据泄露" | 扫描代码、文件或 git 变更中的 Secret，支持 GitHub Secret 检测模式 |
| `dependency-scanning` | 询问"检查依赖有没有已知漏洞" | 对接 GitHub Advisory Database，审查 `pom.xml` / `package.json` 等锁文件中的 CVE |

#### 典型用法

```
# 提交前检查有无硬编码密钥
> 检查这个文件中是否有硬编码的密钥或凭据

# 检查 Maven 依赖 CVE
> 检查 upda-cloud-server 的 pom.xml 中有没有已知安全漏洞的依赖
```

#### 真实案例（2026-05-19 发现并修复）

在 `nacos-config-reference.yml` 中发现 Base64 编码的 AES-128 密钥硬编码为 Spring 环境变量的默认值：

```yaml
# ⚠️ 修复前（危险：开发者忘设环境变量时会使用此已知密钥加密数据）
master-key: ${CRYPTO_MASTER_KEY:MgELHT/KBZVgzLCHEy3jxQ==}

# ✅ 修复后（错误密钥会触发异常，强制开发者显式设置）
master-key: ${CRYPTO_MASTER_KEY:please-set-CRYPTO_MASTER_KEY-in-env}
```

涉及文件：
- `service-ca/src/main/resources/nacos-config-reference.yml`（2 处）
- `service-seal/src/main/resources/nacos-config-reference.yml`（1 处）

> 💡 **本项目重点场景**：PKI/证书服务代码中存在大量私钥、Token、密码配置，提交前使用 secret-scanning 可防止敏感信息意外入库。

### react19-upgrade

**定位**：React 19 迁移工具包（本项目多个前端已在 React 19，用于新功能开发规范）

#### Skills（可直接调用）

| Skill | 说明 |
|-------|------|
| `react19-concurrent-patterns` | Suspense、`use()` Hook、Server Components、并发批量更新 |
| `react19-source-patterns` | DOM/root API、ref、context 迁移模式 |
| `react19-test-patterns` | `act()` 语义、错误边界测试、StrictMode 行为变更 |

#### Agents（迁移流水线）

| Agent | 阶段 | 说明 |
|-------|------|------|
| `react19-commander` | 总指挥 | 协调整个迁移/审查流水线 |
| `react19-auditor` | 审查 | 扫描 Breaking Changes 和废弃模式 |
| `react19-dep-surgeon` | 依赖 | 升级 react@19 及兼容依赖 |
| `react19-migrator` | 迁移 | 重写废弃 API |
| `react19-test-guardian` | 测试 | 修复测试套件 |

#### 典型用法

```
# 审查前端组件是否符合 React 19 规范
copilot --agent react19-upgrade:react19-auditor
> 扫描 upda-cloud/upda-cloud-client/src 中是否存在 React 19 废弃模式

# 咨询 React 19 并发特性最佳实践
> 在 drawing-web-app 中使用 Suspense 加载 WASM 模块，有哪些 React 19 最佳实践？
# （会自动激活 react19-concurrent-patterns skill）
```

---

### structured-autonomy

**定位**：结构化自治规划（Plan → Generate → Implement 三步执行法）

#### Slash Commands

| 命令 | 说明 | 使用阶段 |
|------|------|---------|
| `/structured-autonomy:structured-autonomy-plan` | 生成结构化执行计划（任务拆解、依赖分析） | 任务开始前 |
| `/structured-autonomy:structured-autonomy-generate` | 基于计划生成代码框架/骨架 | 计划确认后 |
| `/structured-autonomy:structured-autonomy-implement` | 按计划逐步实现，保持最小化变更 | 实现阶段 |

#### 推荐工作流

```
# 第一步：规划
/structured-autonomy:structured-autonomy-plan
> 需求：在 service-seal 中添加印章批量注销接口，需要通知 service-signer 并更新证书状态

# 第二步：生成骨架（确认计划后执行）
/structured-autonomy:structured-autonomy-generate
> 按上述计划生成接口骨架、DTO 和测试桩

# 第三步：逐步实现
/structured-autonomy:structured-autonomy-implement
> 实现步骤 1：SealBatchRevokeRequest DTO 和参数校验
```

---

### software-engineering-team

**定位**：7 个专业角色 Agents，覆盖软件开发全生命周期

#### Agents

| Agent | 职责 | 本项目适用场景 |
|-------|------|--------------|
| `se-security-reviewer` | 安全审查：OWASP Top 10、Zero Trust、LLM 安全 | 审查 OAuth2/JWT/证书接口安全性 |
| `se-system-architecture-reviewer` | 架构审查：Well-Architected Framework、可扩展性 | 审查微服务间依赖、Feign 调用链 |
| `se-gitops-ci-specialist` | DevOps：CI/CD、部署调试、GitOps 工作流 | Docker Compose 部署优化 |
| `se-technical-writer` | 技术写作：开发文档、技术博客、教程 | 生成 API 文档、接口说明 |
| `se-ux-ui-designer` | UX 设计：用户旅程、Jobs-to-be-Done | 前端页面交互设计 |
| `se-product-manager-advisor` | 产品管理：GitHub Issues、业务价值对齐 | 功能拆解为 Issues |
| `se-responsible-ai-code` | 负责任 AI：偏见预防、无障碍合规 | drawing-ai-server RAG 系统审查 |

#### 典型用法

```
# 安全审查 OAuth2 授权流程
copilot --agent software-engineering-team:se-security-reviewer
> 审查 auth 服务的 Token Exchange (RFC 8693) 实现，重点检查 OWASP 相关风险

# 架构审查微服务依赖
copilot --agent software-engineering-team:se-system-architecture-reviewer
> 审查 service-seal → service-ra → service-ca 调用链，评估耦合度和可扩展性

# 生成接口文档
copilot --agent software-engineering-team:se-technical-writer
> 为 service-signer 的 /sign/pdf 接口生成开发者接口文档，包含请求示例和错误码说明
```

---

## 快速参考

### 按场景选择

| 场景 | 推荐命令 / Agent |
|------|----------------|
| 编写 Spring Boot 代码前查规范 | `/java-development:java-springboot` |
| TDD 开发新功能 | `testing-automation:tdd-red` → `tdd-green` → `tdd-refactor` |
| 修改前了解影响范围 | `/context-engineering:context-map` |
| 规划复杂多文件任务 | `/structured-autonomy:structured-autonomy-plan` |
| 审查 SQL 性能 | `/database-data-management:sql-optimization` |
| 审查接口安全性 | `software-engineering-team:se-security-reviewer` |
| 架构层面评审 | `software-engineering-team:se-system-architecture-reviewer` |
| 验证 AI 密码学声明 | `use doublecheck` |
| React 19 组件规范审查 | `react19-upgrade:react19-auditor` |
| 生成项目架构文档 | `project-documenter:project-documenter` |
| 提交前检查密钥泄露 | `检查这段代码有无硬编码密钥`（自动激活 secret-scanning） |
| 检查 Maven 依赖 CVE | `检查 pom.xml 依赖漏洞`（自动激活 dependency-scanning） |

---

## MCP Servers

> MCP（Model Context Protocol）服务器为 Copilot 提供额外工具能力（文件操作、数据库查询、API 调用等）。
>
> **配置文件**：`C:\Users\10545\.copilot\mcp-config.json`（当前不存在，按需创建）

### 管理命令

```bash
copilot mcp list    # 查看已配置的 MCP server
copilot mcp add     # 添加新 MCP server
```

### 配置格式

```json
{
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["path/to/server.js"],
      "env": { "KEY": "value" }
    }
  }
}
```

### 内置 MCP（无需配置）

| 服务 | 说明 | 默认状态 |
|------|------|---------|
| `github-mcp-server` | GitHub API 工具集（issues、PR、仓库操作） | 默认启用 |

### 自定义 MCP（待扩充）

> 在此记录后续添加的自定义 MCP server，格式：
>
> **名称**：`xxx`
> **用途**：
> **安装方式**：
> **配置片段**：

---

## Custom Skills

> Custom Skills 是本地 Markdown 文件，作为 Copilot 的专项知识注入。
>
> **全局 Skills 目录**：`C:\Users\10545\.copilot\global-skills\`（按需创建）
> **项目 Skills 目录**：项目 `.github/skills/` 或 `.claude/skills/`

### Skills 文件格式

```markdown
# Skill 名称

## 描述
一句话说明这个 skill 的用途

## 指令
具体的行为指令、规范、知识...
```

### 当前项目 Skills（upda-code）

> 位于 `E:\OpenCloud24.10\upda-code\.claude\skills\`

| Skill | 用途 |
|-------|------|
| `fix-bug` | TDD 标准化 Bug 修复工作流 |
| `deploy-to-228` | 部署到测试服务器（192.168.3.228） |
| `reference-docs` | 密码学/PKI/国家标准知识库查询 |
| `update-context` | 更新项目上下文文档 |
| `backend-test` | Maven 测试运行（指定服务模块） |
| `frontend-dev` | 启动前端开发服务器 |

### 全局 Skills（待扩充）

> 在此记录后续添加到 `~/.copilot/global-skills/` 的全局 skill：

---

## Custom Agents

> Custom Agents 是具有专属指令和工具集的 AI 角色，通过 `--agent` 参数或对话中引用来调用。
>
> **项目 Agents 目录**：项目 `.github/agents/` 或 `.claude/agents/`

### 当前项目 Agents（upda-code）

| Agent | 说明 |
|-------|------|
| `java-reviewer` | Java 后端代码审查（构造器注入、DTO 命名、MyBatis-Plus） |
| `frontend-reviewer` | React 前端代码审查（MobX、MUI v7、函数式组件） |
| `crypto-consultant` | 密码学与国家标准领域专家（自动查阅 reference-docs） |
| `Universal PR Comment Addresser` | 地址化处理 PR 评论 |
| `API Architect` | API 架构指导与工作代码 |
| `Debug Mode Instructions` | 调试应用程序查找并修复 bug |
| `DevOps Expert` | DevOps 专家（infinity loop 原则） |

### 全局 Agents（待扩充）

> 在此记录后续添加的全局自定义 agents：
