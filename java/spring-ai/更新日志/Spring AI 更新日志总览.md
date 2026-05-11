---
title: Spring AI 更新日志总览
created: 2025-05-11
tags:
  - spring-ai
  - changelog
  - java
---

# Spring AI 更新日志总览

> 数据来源：[GitHub Releases](https://github.com/spring-projects/spring-ai/releases)
> Spring AI 仓库没有独立的 CHANGELOG.md，所有更新日志通过 GitHub Releases 管理。

## 版本线概览

| 版本线 | 状态 | 说明 |
|--------|------|------|
| **2.0.x** | Milestone（开发中） | 下一大版本，重大 Breaking Changes |
| **1.1.x** | GA（维护中） | 当前稳定版，新特性 + Bug 修复 |
| **1.0.x** | GA（维护中） | 长期支持版，仅 Bug 修复和安全补丁 |

## 版本索引

### 2.0.x Milestone

| 版本 | 新特性 | Bug 修复 | 关键变化 |
|------|--------|---------|----------|
| [[Spring AI 2.0 Milestone#2.0.0-M6\|2.0.0-M6]] | 7 | 18 | 全面移除 Options setter（强制 Builder）；移除 SAP HANA / Infinispan 向量存储；ChatMemory 要求显式 conversationId |
| [[Spring AI 2.0 Milestone#2.0.0-M5\|2.0.0-M5]] | 13 | 36 | MCP SDK 升级至 2.0.0-M2；移除 azure-openai 模块；采用官方 openai-java SDK；移除 Vertex AI / ZhipuAI / OCI GenAI |
| [[Spring AI 2.0 Milestone#2.0.0-M4\|2.0.0-M4]] | 2 | 10 | 标记 Vertex AI / ZhiPu AI / OCI GenAI 为 deprecated |
| [[Spring AI 2.0 Milestone#2.0.0-M3\|2.0.0-M3]] | 23 | 45 | MCP Annotations 迁入核心；Jackson 2→3；Anthropic 官方 SDK；Claude 3 模型移除 |
| [[Spring AI 2.0 Milestone#2.0.0-M2\|2.0.0-M2]] | 20 | 20 | Anthropic Skills API；S3 向量存储；Infinispan 向量存储；Redis 语义缓存 |

### 1.1.x

| 版本 | 新特性 | Bug 修复 | 关键变化 |
|------|--------|---------|----------|
| [[Spring AI 1.1.x#1.1.6\|1.1.6]] | 1 | 5 | ChatMemory 要求显式 conversationId；PromptChatMemoryAdvisor deprecated；MCP SDK 0.18.2 |
| [[Spring AI 1.1.x#1.1.5\|1.1.5]] | 0 | 9 | 安全修复：Transformer 缓存加固、PDF DoS 防护；CosmosDB SQL 注入修复 |
| [[Spring AI 1.1.x#1.1.4\|1.1.4]] | 1 | 11 | 动态禁用 Structured Output Native |
| [[Spring AI 1.1.x#1.1.3\|1.1.3]] | 19 | 31 | Anthropic Skills API；Mistral 结构化输出；ToolCallAdvisor 流式响应 |
| [[Spring AI 1.1.x#1.1.0\|1.1.0]] | 1 | 10 | GA 发布；extraBody 动态反序列化 |
| [[Spring AI 1.1.x#1.1.0-M2\|1.1.0-M2]] | 16 | 12 | VertexAI 结构化输出；Mistral OCR；ZhipuAI GLM-4.5 / GLM-Z1 |
| [[Spring AI 1.1.x#1.1.0-M1\|1.1.0-M1]] | 47 | 106 | MCP 注解支持；GPT-5；Google GenAI；VectorStoreRetriever |

### 1.0.x

| 版本 | 新特性 | Bug 修复 | 关键变化 |
|------|--------|---------|----------|
| [[Spring AI 1.0.x#1.0.7\|1.0.7]] | 0 | 5 | ChatMemory 要求显式 conversationId；MCP SDK 0.10→0.18.2 大版本跳跃 |
| [[Spring AI 1.0.x#1.0.6\|1.0.6]] | 0 | 5 | 安全：Transformer 缓存权限、CosmosDB 参数化查询、PDF DoS |
| [[Spring AI 1.0.x#1.0.5\|1.0.5]] | 0 | 8 | VectorStore 过滤修复、Bedrock 流式修复 |
| [[Spring AI 1.0.x#1.0.4\|1.0.4]] | 1 | 9 | Claude Opus 4.6 / Sonnet 4.6；移除 Claude 3.x 模型 |
| [[Spring AI 1.0.x#1.0.3\|1.0.3]] | 4 | 14 | GraalVM 原生镜像改进；GemFire 元数据过滤 |
| [[Spring AI 1.0.x#1.0.2\|1.0.2]] | 9 | 31 | GPT-5 支持；Kotlin schema；MariaDB 相似度评分 |
| [[Spring AI 1.0.x#1.0.1\|1.0.1]] | 24 | 50 | Claude Opus 4 / Sonnet 4；流式 Tool Call；MySQL 聊天记忆 |

## 重大变更摘要

> [!warning] 2.0.0 升级要点
> - **模块移除**：`spring-ai-azure-openai`（合并到 `spring-ai-openai`）、`spring-ai-vertex-ai-gemini`、ZhipuAI、OCI GenAI、SAP HANA DB、Infinispan
> - **依赖升级**：Jackson 2 → Jackson 3（`tools.jackson`）、MCP SDK 2.0.0-M2
> - **API 变更**：`disableMemory()` → `disableInternalConversationHistory()`、`ModelOptionsUtils.merge()` 移除、**全面移除 Options setter（强制 Builder）**
> - **模型变更**：Claude 3.x 全部移除，需迁移至 Claude 4.x
> - **行为变更**：`PromptChatMemoryAdvisor` 移除，ChatMemory 要求显式 `conversationId`

> [!info] 1.0.x → 1.1.x 升级要点
> - Claude 3.x deprecated → 移除，默认模型改为 `claude-haiku-4-5`
> - `UserMessage.properties` → `UserMessage.metadata`
> - `maxTokens` 与 `maxCompletionTokens` 互斥
> - `VectorStoreRetriever` 接口从 `VectorStore` 中提取
> - 1.0.7 / 1.1.6 起要求显式 `conversationId`

## 相关链接

- [GitHub Releases](https://github.com/spring-projects/spring-ai/releases)
- [官方文档](https://docs.spring.io/spring-ai/reference/)
- [Spring AI BOM](https://docs.spring.io/spring-ai/reference/dependencies.html)
