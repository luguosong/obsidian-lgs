---
title: Spring AI 1.0.x 更新日志
created: 2025-05-11
tags:
  - spring-ai
  - changelog
---

# Spring AI 1.0.x 更新日志

> [!tip] 长期支持版
> 1.0.x 是首个 GA 版本线，以 Bug 修复和安全补丁为主。

---

## 1.0.7

**统计**：5 Bug 修复 · 6 其他改进

> [!warning] 行为变更
> Chat Memory Advisors 现在要求显式提供 `conversationId`。`PromptChatMemoryAdvisor` 需迁移。

### Breaking Changes

- Chat Memory Advisors 必须显式提供 `conversationId`

### Bug 修复

- Milvus 向量存储 `doDelete` ID 列表字符串转义修复
- [[MCP Server]] `ObjectMapper` 配置错误
- [[MCP Server]] 和 Spring WebMvc 自动配置问题（修复了之前错误的修复）
- ChatClientAdvisor 集成测试更新为显式 `conversationId`
- Anthropic 聊天客户端函数回调集成测试修复

### 依赖升级

- MCP SDK 0.10.0 → 0.18.2（大版本跳跃）

### 构建

- JDK 17.0.19
- Starter 模块重组到 `starters/` 目录

---

## 1.0.6

**统计**：5 Bug 修复

### 安全修复

- Transformer 模型缓存目录创建时设置受限权限
- 修复畸形 PDF 导致的 DoS 漏洞（限制字符缓冲区分配）
- CosmosDB 向量存储 delete 方法参数化查询

### Bug 修复

- VectorStoreChatMemoryAdvisor `conversationId` 过滤
- 向量存储过滤表达式转换器键处理

### 依赖升级

- [[Spring Boot]] → 3.5.14

---

## 1.0.5

**统计**：8 Bug 修复 · 1 其他改进

### Bug 修复

- AWS Bedrock Converse API 流式 `finishReason` 未传播
- Oracle / PostgreSQL 向量存储集成测试
- Ollama 模型提供商集成测试
- Redis 向量存储 TAG/TEXT 过滤
- Neo4j 向量存储过滤表达式键处理
- Bedrock 代理聊天模型媒体获取
- SimpleVectorStore 过滤评估逻辑

---

## 1.0.4

**统计**：1 新特性 · 9 Bug 修复 · 1 文档改进 · 11 其他改进

### 新特性

- **Claude Opus 4.6 和 Sonnet 4.6** 模型加入 `AnthropicApi.ChatModel` 枚举

### Breaking Changes

- **移除 Claude 3.x / 3.7 模型变体**：默认模型改为 `claude-haiku-4-5`
- 需迁移至 Claude 4.x 模型（`claude-haiku-4-5`、`claude-opus-4-6`、`claude-sonnet-4-6`）

### Bug 修复重点

- 过滤表达式转换器修复
- Azure OpenAI 聊天模型流式响应
- MySQL/MariaDB JDBC 聊天记忆消息排序
- Vertex AI Gemini 文本 + 工具调用混合响应
- PDF 文档阅读器 `pagesPerDocument` 配置

### 依赖升级

- [[Spring Boot]] → 3.5.11

---

## 1.0.3

**统计**：4 新特性 · 14 Bug 修复 · 6 文档改进 · 3 其他改进

### 新特性

- GemFireVectorStore 元数据过滤查询
- BedrockChatOptions 增强
- GraalVM 原生镜像编译改进
- OpenAiApi 可作为 Spring Bean 注入

### Bug 修复重点

- Mistral 集成 JSON Schema 生成
- 工具执行错误为空时的回退消息
- Anthropic streaming `thinkingBlock.signature()` 处理
- PromptTemplate.render 变量处理
- Jackson 模块类加载（避免 Thread Context ClassLoader）
- OpenAI 工具调用合并越界异常
- Bedrock Nova 集成测试

---

## 1.0.2

**统计**：9 新特性 · 31 Bug 修复 · 13 文档改进 · 4 依赖升级 · 4 性能改进 · 15 构建更新

### 新特性

- Bedrock Cohere chat enable 属性
- Unicode 属性联合（中文字符处理改进）
- `maxTokens` 与 `maxCompletionTokens` 互斥验证
- **GPT-5 模型支持**
- Kotlin data class JSON Schema（BeanOutputConverter）
- MariaDB 向量存储相似度搜索评分
- 维护分支 cherry-pick 快速 CI 构建

### Bug 修复重点

- Tokenizer 二进制数据 Base64 编码
- VertexAI Gemini 流式测试
- ToolCallback#call(String, ToolContext) 默认实现
- 流式操作空工具调用参数处理
- Bedrock converse chat options 合并
- Azure OpenAI 消息排序
- Anthropic 函数调用集成测试
- SimpleDateFormat → DateTimeFormatter（线程安全）
- MilvusVectorStore metadata null NPE
- Azure 向量存储 metadata mutation
- OpenAI 流式 finish_reason 空字符串
- ResourceAccessException 重试机制
- null safety（Optional 改进）

---

## 1.0.1

**统计**：24 新特性 · 50 Bug 修复 · 45 文档改进 · 32 其他改进

### 新特性

- KeywordMetadataEnricher 自定义模板
- 向量存储添加文档时验证 text/media 内容
- @tool 注解功能增强
- Anthropic 流式无参数工具调用
- Mistral 聊天模型配置更新
- 工具执行异常选择性重抛
- MessageAggregator 工具调用支持
- ChatClient#mutate 深拷贝 advisors
- MiniMaxChatOptions equals/hashCode/deep copy
- 新 Mistral AI 聊天模型
- OllamaChatModel 重试模板
- Anthropic streaming thinking events
- OpenAI 新语音枚举
- Anthropic 动态 API Key（per-request）
- Neo4j 自动确定嵌入维度
- **Claude Opus 4 / Sonnet 4** 模型支持
- OpenAI PDF 文件媒体输入
- MySQL 聊天记忆表 schema
- Chroma 复杂 metadata 处理
- 向量存储 metadata 类型支持
- 可配置工具执行[[异常处理]]
- SQL Server 聊天记忆集成测试

### Bug 修复重点

- 同名方法工具调用错误
- Anthropic API streaming NPE
- SystemPromptTemplate.builder() 返回类型错误
- Anthropic 注解打包
- OpenAI 音频文件名丢失
- Milvus schema 初始化
- ZhiPu AI 无用配置清理
- ZhiPu AI 嵌入模型自定义维度
- Bedrock 流式无参数工具调用
- DeepSeek 空工具调用合并
- Chroma 集合创建日志
- OpenAiAudioTranscriptionResponseMetadata.toString 异常
- getMimeType 无限递归
- McpToolCallback 根[[异常处理]]
