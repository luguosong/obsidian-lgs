# RAG 知识库管道

## 行业标准文档（standard 类型）

PDF 标准文档 → PDFBox 3.0.4 解析 → 按章节分块 → bge-m3 嵌入（1024 维）→ Qdrant `drawing_knowledge` 集合。

**文档存放位置**：`src/main/resources/standard/`
**当前索引**：东莞市城市规划管理技术规定（2020年文件汇编），241 个向量块

**分块策略**：按章节标题（正则匹配 `第X章`、`X.X` 等）智能分割，保留上下文层级信息。每块包含元数据：`doc_type=standard`、`source=文件名`、`title=章节标题`。

## 去重机制（IndexBuilder）

防止重复导入同一文档，通过 Qdrant REST API 实现（Spring AI VectorStore 不支持过滤删除）：

| 模式 | 参数 | 行为 |
|------|------|------|
| 增量（默认） | `force=false` | Scroll API 获取已索引 `source` 列表，仅处理新文件 |
| 强制重建 | `force=true` | Delete API 按 `doc_type` 清除后全量重建 |

**Qdrant REST 端口**：gRPC 端口 - 1（默认 18140），通过 `@Value` 注入配置。

## ToolProtocol 注册

RAG 工具（`search_code_examples`、`search_help_docs`、`search_standards`）必须在 `ToolRegistry.registerProtocols()` 中注册为 `serverReadOnly`。否则会触发 fail-closed 默认行为（clientSide=true），导致 RAG 查询被推送到前端而非服务端预执行。

## 索引管理命令

```bash
curl -X POST http://localhost:3001/api/index/build-code               # 增量构建代码示例
curl -X POST http://localhost:3001/api/index/build-code?force=true    # 强制重建代码示例
curl -X POST http://localhost:3001/api/index/build-docs               # 增量构建帮助文档
curl -X POST http://localhost:3001/api/index/build-standards          # 增量构建行业标准
curl -X POST http://localhost:3001/api/index/build-standards?force=true # 强制重建行业标准
curl -X POST http://localhost:3001/api/index/rebuild                  # 全量重建（始终 force）
curl -X DELETE http://localhost:3001/api/index/clear/standard         # 清除标准文档向量
curl http://localhost:3001/api/index/stats                            # 统计（含各类型计数）
curl "http://localhost:3001/api/index/search-test?type=standard&query=建筑退让" # 检索测试
```
