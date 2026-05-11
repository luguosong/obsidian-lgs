---
title: Spring AI 2.0 Milestone 更新日志
created: 2025-05-11
tags:
  - spring-ai
  - changelog
  - milestone
---

# Spring AI 2.0 Milestone 更新日志

> [!note] 版本线说明
> 2.0.x 为下一大版本的 Milestone 预览版，包含大量 Breaking Changes。
> **不建议用于生产环境**，仅用于评估和迁移准备。
> 详细迁移指南见各版本升级说明。

---

## 2.0.0-M6

**统计**：7 新特性 · 18 Bug 修复 · 5 文档改进 · 30 其他改进

### Breaking Changes

- **移除 `PromptChatMemoryAdvisor`**：Chat Memory Advisors 现在必须提供显式 `conversationId`
- **`OpenAiConnectionProperties` 重命名为 `OpenAiCommonProperties`**
- **OpenAI Properties 类不再继承 `AbstractOpenAiOptions`**：改变了类层次结构
- **全面移除 Setter 方法**：所有 Options 类（OpenAI、Mistral、MiniMax、Google GenAI、ElevenLabs、Bedrock、DeepSeek、Anthropic、Ollama）移除 setter，强制使用 Builder 模式
- **移除 SAP HANA DB 向量存储模块**
- **移除 Infinispan 向量存储模块**
- **移除 `ModelOptionsUtils` 中的多个工具方法**
- **移除 `OpenAiChatOptions` 上不必要的 Jackson 注解**
- **`OpenAiEmbeddingOptions#encodingFormat` 改用枚举类型**替代字符串

### 新特性

- 增强的 Chat Model 可观测性支持
- OpenAI Options 类改进的 Builder 模式
- 工具/函数调用的可观测性增强
- `ChatModel` 接口新增默认 `buildRequestPrompt` 方法，减少各模型提供商重复实现
- `OpenAiEmbeddingOptions#encodingFormat` 改用枚举（类型安全）
- OpenAI embedding encoding format 选项恢复

### Bug 修复重点

- MilvusVectorStore 字符串 ID 删除时未正确转义
- OllamaChatOptions `getOutputSchema()` 异常
- OpenAI 工具选项合并 `ToolCallingChatOptions` 到 `OpenAiChatOptions` 错误
- OpenAI 配置属性未正确解析（Spring Boot 自动配置）
- Qdrant Docker 镜像更新至 1.17.0
- DefaultSemanticCache 字符串拼接替换为 `Filter.Expression`
- 多个模块 null-safety 改进（Google GenAI、MiniMax、Transformers、Vertex AI、ElevenLabs）

### 依赖升级

- OpenAI Java SDK 4.34.0
- Anthropic SDK 2.27.0 → 2.30.0
- Qdrant 1.17

### 构建

- Spring AI starter 模块重组到专用 `starters/` 目录
- JDK 17.0.19

---

## 2.0.0-M5

**统计**：13 新特性 · 36 Bug 修复 · 14 文档改进 · 41 其他改进

### Breaking Changes

- **MCP Java SDK 升级至 2.0.0-M2**：包含 API 层面的破坏性变更，需查阅迁移文档
- **移除 `spring-ai-azure-openai` 模块**：Azure OpenAI 功能合并到 `spring-ai-openai`，需更新依赖和配置
- **`ModelOptionsUtils.merge()` 移除**：非 chat 模型实现（audio、embedding、image）中的此方法已删除
- **ChatClient 选项合并重设计**：新增 `combineWith()` builder 方法，替代原有合并行为
- **移除 Vertex AI 非嵌入模块**：仅保留 `spring-ai-vertex-ai-embedding`
- **移除 ZhipuAI 模型**：从主仓库移除
- **移除 OCI GenAI 支持**：将迁移到独立集成模块
- **移除 `SpringAiTestAutoConfigurations`**：需更新测试配置
- **`spring-ai-openai-sdk` 合并到 `spring-ai-openai`**：功能统一，无需改配置属性

### 新特性

- 自定义 `StructuredOutputConverter` 可参与原生结构化输出管道
- `ToolCallAdvisor.Builder` 暴露 `conversationHistoryEnabled` getter
- 统一缓存使用指标到 `Usage` 接口
- **采用官方 openai-java SDK**：替代内部实现，支持所有 OpenAI 模型
- OpenAI 音频转录模型支持
- MCP Server 工具暴露过滤：`spring.ai.mcp.server.expose-mcp-client-tools`
- OpenAI 内容审核模型支持
- OpenAI SDK 模型支持 extra body 参数

---

## 2.0.0-M4

**统计**：2 新特性 · 10 Bug 修复 · 13 其他改进

### 升级说明

- Vertex AI / OCI GenAI / ZhiPu AI 标记为 deprecated，后续版本将移除，需规划迁移

### 新特性

- Gemini 3.x 模型支持 Google Search + 自定义工具
- 支持动态禁用原生结构化输出

### Bug 修复重点

- extraBody 在有 toolDefinitions 时丢失的问题
- AzureOpenAiChatOptions stop 字段初始化回退
- Redis / Neo4j 向量存储过滤表达式转换问题
- OpenAI SDK + Azure OpenAI 部署的 API Key header 配置

### 依赖升级

- Google Generative AI SDK 1.44.0
- OpenAI SDK 4.28.0
- Anthropic SDK 2.17.0

---

## 2.0.0-M3

**统计**：23 新特性 · 45 Bug 修复 · 16 文档改进 · 67 其他改进

> [!danger] 大量破坏性变更
> 包括 MCP 注解包重命名、MCP transport artifact 迁移、Jackson 2→3、`ToolContext` 中移除会话历史。

### Breaking Changes

- **MCP Annotations 包迁移**：`org.springaicommunity.mcp` → `org.springframework.ai.mcp.annotation`
- **MCP transport artifact 迁移**：`io.modelcontextprotocol.sdk` → `org.springframework.ai.mcp`
- **Jackson 2 → Jackson 3**：`com.fasterxml.jackson` → `tools.jackson`（Spring Boot 4 默认）
- **`McpAsyncClientCustomizer` / `McpSyncClientCustomizer` 移除**：合并为 `McpClientCustomizer<B>`
- **Anthropic 集成改用官方 Java SDK**：内部实现从 RestClient 改为官方 SDK
- **`disableMemory()` → `disableInternalConversationHistory()`**
- **Claude 3 Opus / Sonnet / Haiku 移除**：必须迁移到 Claude 4.x
- **Huggingface 模型移出主仓库**
- 多个 ChatOptions 类改用 Builder 模式：`DeepSeek`、`Bedrock`、`MistralAi`、`AzureOpenAi`、`Anthropic`
- `ModelRequest#getOptions` 改为非 null 返回

### 新特性

- MCP 客户端自定义抽象
- 过滤表达式转换器改进
- Builder 简化（移除不必要泛型）
- Anthropic 官方 SDK 集成
- `disableMemory()` 重命名为 `disableInternalConversationHistory()`

---

## 2.0.0-M2

**统计**：20 新特性 · 20 Bug 修复 · 16 文档改进 · 38 其他改进

### Breaking Changes

- **Anthropic Skills API 统一**：helper 类重命名
- **SemanticCache 接口搬迁**：从 Redis 包移到通用包
- **Couchbase 向量存储类搬迁**：需更新 import

### 新特性

- Ollama 嵌入模型维度参数支持
- JSON Schema 自定义
- OpenAI 内容审核 / 音频默认端点配置
- **Amazon S3 向量存储**支持
- **Infinispan 向量存储**支持
- **Amazon Bedrock Knowledge Base 向量存储**
- Redis 语义缓存改进
- QdrantVectorStore content 字段名可配置
- Mistral AI 结构化输出（JSON Schema）
- Redis 语义缓存 Advisor
- JSpecify null-safety 注解
- MCP Server Customizer 接口
- 动态工具 Schema 增强
- ToolCallAdvisor conversationHistoryEnabled 选项
