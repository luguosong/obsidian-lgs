---
title: Spring AI 1.1.x 更新日志
created: 2025-05-11
tags:
  - spring-ai
  - changelog
---

# Spring AI 1.1.x 更新日志

> [!tip] 当前稳定版
> 1.1.x 是当前推荐的稳定版本线，适用于生产环境。

---

## 1.1.6

**统计**：1 新特性 · 5 Bug 修复 · 2 文档改进 · 5 其他改进

> [!warning] 行为变更
> Chat Memory Advisors 现在要求显式提供 `conversationId`，不再支持隐式 ID。

### Breaking Changes

- Chat Memory Advisors 必须显式提供 `conversationId`
- `PromptChatMemoryAdvisor` 标记为 deprecated，需迁移到替代实现

### 新特性

- MCP 自动配置添加 `@ConditionalOnMissingBean` 检查，允许用户覆盖默认 bean

### Bug 修复

- MilvusVectorStore `doDelete` 字符串 ID 转义错误
- ChatClientAdvisorTests 更新为显式 `conversationId`
- MistralAI 观测集成测试修复
- MistralAI API 请求中配置选项未正确传递
- Ollama 集成中 `AssistantMessage.ToolCall.id` 回退修复

### 依赖升级

- MCP SDK 0.17.0 → 0.18.2
- MCP annotations 0.8.0 → 0.9.0

### 构建

- JDK 17.0.19
- Starter 模块重组到 `starters/` 目录

---

## 1.1.5

**统计**：9 Bug 修复 · 3 文档改进 · 11 其他改进

### 升级说明

- Pixtral 12B 模型已移除，Pixtral Large 标记为 deprecated

### 安全修复

- Transformer 模型缓存目录权限加固，防止未授权访问
- 修复畸形 PDF 导致的 DoS 漏洞（过度内存分配）

### Bug 修复重点

- CosmosDB 向量存储 `doDelete` 方法参数化查询（防止 SQL 注入）
- VectorStoreChatMemoryAdvisor 的 `conversationId` 未正确应用
- 向量存储过滤表达式转换器键处理
- OpenAI API `extra_body` 参数错误包含

### 依赖升级

- [[Spring Boot]] 3.5.13 → 3.5.14
- Apache Tika 3.3.0、jsoup 1.22.1、Apache PDFBox 3.0.7

---

## 1.1.4

**统计**：1 新特性 · 11 Bug 修复 · 1 其他改进

### 新特性

- 运行时动态禁用 Structured Output Native 功能

### Bug 修复重点

- extraBody 在有 toolDefinitions 时丢失
- Anthropic prompt caching 中多块系统消息缓存
- Redis / Neo4j 向量存储过滤表达式
- Google GenAI 嵌入模型 API 更新
- Bedrock 代理聊天模型媒体获取可靠性

---

## 1.1.3

**统计**：19 新特性 · 31 Bug 修复 · 23 文档改进 · 25 其他改进

### 新特性

- Neo4j 向量存储支持自定义过滤表达式转换器（Builder 模式）
- OpenAiSdkChatModel Builder 模式
- OpenAI 嵌入模型自定义维度支持
- **ToolCallAdvisor 流式响应支持**
- SimpleVectorStore 删除时支持过滤
- **Anthropic Claude [[Skills]] API** 支持
- Ollama 嵌入模型维度参数
- JSON Schema 自定义（结构化输出和函数调用）
- **Mistral AI 结构化输出**（JSON Schema）
- Mistral AI OCR（光学字符识别）
- Mcp*ServerCustomizer 接口，MCP 非 Web 环境修复
- OllamaChatOptions 实现 StructuredOutputChatOptions
- Chat Memory Advisors 支持 ToolResponseMessage
- 运行时动态增强工具 Schema
- ToolCallAdvisor conversationHistoryEnabled 选项
- Azure 向量存储可配置字段名
- TokenTextSplitter 自定义标点支持

### Bug 修复重点

- 过滤表达式转换器全面修复（Redis、Neo4j、OpenSearch、Elasticsearch）
- MongoDB 聊天记忆消息排序
- Anthropic prompt caching 多块系统消息
- ChromaApi [[异常处理]]
- Neo4jVectorStore doAdd 忽略 sessionConfig

---

## 1.1.0

**统计**：1 新特性 · 10 Bug 修复 · 3 文档改进 · 3 其他改进

> [!success] GA 发布
> 1.1.0 是 1.1.x 线的正式发布版。

### 新特性

- ChatCompletionRequest 支持 `@JsonAnySetter` 动态字段反序列化（extraBody）

### Bug 修复重点

- MongoChatMemoryIndexCreator 组件扫描
- MCP 工具定义 inputSchema 验证
- OpenAI API 畸形响应错误处理
- MongoDB 聊天记忆 Maven 依赖
- ElevenLabs 自动配置条件属性
- Anthropic 过度 debug 日志清理

---

## 1.1.0-M2

**统计**：16 新特性 · 12 Bug 修复 · 6 文档改进 · 22 其他改进

### 新特性

- VertexAI Gemini 结构化输出 Schema 验证
- **Mistral AI OCR** 支持
- Ollama 嵌入模型硬件/内存/性能选项
- MCP Gateway Testcontainers 支持
- Google GenAI BOM 条目
- ZhipuAI thinking 和 response_format 参数
- ZhiPu 新模型：GLM-4.5、GLM-Z1
- MCP Gateway [[Docker Compose]] 支持
- Bedrock Cohere chat enable 属性
- EmbeddingOptions Builder 对齐 ChatOptions
- AssistantMessage Builder 支持
- OpenAI API 可作为 Bean 注入
- Anthropic API 缓存管理
- Google GenAI 扩展 token 使用元数据

### 依赖升级

- [[Spring Boot]] 3.5.5 → 3.5.6
- MCP SDK 0.12.1 → 0.13.1

---

## 1.1.0-M1

**统计**：47 新特性 · 106 Bug 修复 · 70 文档改进 · 120 其他改进

> [!info] 1.1 线的首个 [[Milestone]]，变更量最大

### Breaking Changes

- MCP 自动配置类重命名（添加 `Mcp` 前缀）
- `maxTokens` 与 `maxCompletionTokens` 互斥
- `UserMessage.properties` → `UserMessage.metadata`
- 提取 `VectorStoreRetriever` 接口

### 新特性

- **MCP 注解配置**：Client 和 Server 全面注解支持
- **GPT-5 模型支持**：含 verbosity 参数
- **Google GenAI 模块**：使用最新 Google GenAI SDK
- **Google GenAI 嵌入模块**
- VectorStoreRetriever 接口提取
- ChatClient 支持 PromptUserSpec / PromptSystemSpec 元数据
- 音频转录标准化接口
- ZhiPu AI Builder 模式、自定义嵌入维度
- Weaviate 向量存储 meta 字段前缀和 content 字段可配置
- Anthropic streaming thinking events
- Anthropic 动态 API Key
- Neo4j 向量存储自动确定嵌入维度
- MySQL 聊天记忆 SPRING_AI_CHAT_MEMORY 表 schema
- Streamable HTTP transport for MCP client
- ChatClient#mutate 深拷贝 advisors
- 可配置工具执行[[异常处理]]
- Kotlin data class JSON Schema 支持
- MariaDB 相似度搜索评分

## 相关笔记

- [[更新日志]]
- [[Spring AI 1.0.x 更新日志]]
- [[Spring AI 2.0 Milestone 更新日志]]
- [[Spring AI 更新日志总览]]
- [[Harness Engineering 架构详解]]
- [[多平台支持]]
- [[Java 概述]]
- [[依赖管理]]
