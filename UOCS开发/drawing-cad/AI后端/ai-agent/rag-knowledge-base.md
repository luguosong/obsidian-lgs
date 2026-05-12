# RAG 知识库 — AutoCAD 帮助文档检索系统

## 架构总览

```
                    用户提问
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Node.js AI Server (port 3001)                       │
│                                                      │
│  LLM 判断是否需要检索知识库                            │
│    ├─ 绘图请求 → 调用 draw_* 工具                      │
│    └─ 知识问题 → 调用 search_cad_knowledge 工具        │
│                       │                              │
│                  HTTP POST                           │
│              /search { query }                       │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│  Python RAG 微服务 (port 3002)                       │
│                                                      │
│  FastAPI (rag_server.py)                             │
│    ├─ 接收 query                                     │
│    ├─ 使用本地 bge-small-zh-v1.5 模型向量化 query     │
│    ├─ 在 ChromaDB 中进行余弦相似度检索                 │
│    └─ 返回 top_k 条最相关文档片段                      │
└───────────────────────┬──────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────┐
│  ChromaDB 向量数据库 (server/rag/chroma_db/)         │
│                                                      │
│  Collection: autocad_help                            │
│    ├─ 文档: 从 HelpHtml 解析的文本块                   │
│    ├─ 向量: 本地 BAAI/bge-small-zh-v1.5 (512维)      │
│    └─ 元数据: title, cmdname, topic_type, source      │
└──────────────────────────────────────────────────────┘
```

### 数据流

1. 用户在 AI 助手中提问（如 "HATCH 命令有哪些选项？"）
2. Node.js 后端将问题发给 LLM
3. LLM 判断这是知识问题，调用 `search_cad_knowledge` 工具
4. Node.js 调用 Python RAG 微服务的 `/search` 接口
5. RAG 微服务将问题向量化，在 ChromaDB 中检索最相关的文档片段
6. 返回 top_k 条结果给 Node.js
7. Node.js 将检索结果作为 tool result 回传给 LLM
8. LLM 基于检索到的官方文档内容生成回答

---

## 文件结构

```
DrawingWebApp/
├── server/
│   ├── rag/                          # RAG 知识库（Python 项目）
│   │   ├── requirements.txt          # Python 依赖
│   │   ├── .env                      # 配置（API Key、路径等）
│   │   ├── .gitignore
│   │   ├── build_index.py            # 索引构建脚本
│   │   ├── rag_server.py             # FastAPI 检索微服务
│   │   └── chroma_db/               # ChromaDB 持久化目录（构建后生成）
│   │       ├── chroma.sqlite3
│   │       └── file_hashes.json      # 增量更新用的文件哈希记录
│   │
│   ├── tools/
│   │   └── cadTools.js               # 新增了 search_cad_knowledge 工具
│   └── .env                          # 新增了 RAG_SERVER_URL 配置
│
├── HelpHtml/                         # AutoCAD 帮助文档源文件
│   ├── filesACD/                     # 主要内容 (7,536 个 HTM 文件)
│   ├── files/
│   └── html/
│
└── docs/
    └── rag-knowledge-base.md         # 本文档
```

---

## 快速启动

### 前置条件

- Python 3.10+
- Node.js 18+（你的 AI Server 已有）
- 无需 API Key — Embedding 使用本地模型 (BAAI/bge-small-zh-v1.5)，完全免费

### 步骤

```bash
# 进入 RAG 目录
cd DrawingWebApp/server/rag

# 创建 Python 虚拟环境
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置 .env（检查 HELP_HTML_DIR 路径是否正确）
# 编辑 .env 确认 HELP_HTML_DIR 指向你的 HelpHtml 目录

# 先做一次 dry-run 统计
python build_index.py --dry-run
# 输出: 扫描到 N 个文件, 生成 N 个文本块

# 构建索引（首次全量，本地模型，约 5-15 分钟，零费用）
#    首次运行会自动从 HuggingFace 下载 bge-small-zh-v1.5 模型（约 93MB）
python build_index.py
# 输出: ✓ 构建完成！ChromaDB 记录总数: XXXX

# 启动 RAG 检索微服务
python rag_server.py
# 输出: 📚 AutoCAD RAG 知识库服务启动中... 端口: 3002

# 验证
# 浏览器打开 http://localhost:3002/docs 查看 API 文档
# 或：
curl -X POST http://localhost:3002/search \
  -H "Content-Type: application/json" \
  -d '{"query": "HATCH 命令", "top_k": 3}'
```

### 启动顺序

启动整个 AI 系统需要 3 个服务：

```bash
# 终端 1: RAG 微服务
cd DrawingWebApp/server/rag
python rag_server.py

# 终端 2: Node.js AI 后端
cd DrawingWebApp/server
npm run dev

# 终端 3: 前端 (可选，开发模式)
cd DrawingWebApp
npm run dev
```

---

## 增量更新

当你有新的帮助文档要添加时：

### 添加新文件

1. 将新的 `.htm` / `.html` 文件放入 `HelpHtml/filesACD/` 目录
2. 运行增量更新：

```bash
cd DrawingWebApp/server/rag
python build_index.py --incremental
```

增量模式会：
- 计算每个文件的 MD5 哈希
- 与上次构建时的哈希比较
- 只处理新增或内容变更的文件
- 跳过未变更的文件（不会重新向量化）

### 添加自定义文档

你也可以添加非 AutoCAD 的文档（如 ODA SDK 文档、公司内部绘图标准等）：

1. 将 HTML 文件放入 `HelpHtml/` 下的任意子目录
2. 确保 HTML 中包含有意义的 `<title>` 标签和正文内容
3. 运行增量更新

### 完全重建

如果需要从头重建整个索引：

```bash
python build_index.py
# 全量模式会先清空旧数据，然后重新处理所有文件
```

---

## 配置说明

### server/rag/.env

| 变量 | 默认值 | 说明 |
|---|---|---|
| `EMBEDDING_MODEL` | `BAAI/bge-small-zh-v1.5` | 本地 Embedding 模型（HuggingFace 模型名） |
| `HELP_HTML_DIR` | `E:/ODAGitLab/.../HelpHtml` | HTML 源目录 |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB 数据目录 |
| `RAG_PORT` | `3002` | FastAPI 服务端口 |

### server/.env (Node.js 端)

| 变量 | 默认值 | 说明 |
|---|---|---|
| `RAG_SERVER_URL` | `http://localhost:3002` | RAG 微服务地址 |

### build_index.py 内部参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `CHUNK_SIZE` | 800 | 每个文本块的最大字符数 |
| `CHUNK_OVERLAP` | 150 | 相邻块的重叠字符数 |
| `MIN_TEXT_LENGTH` | 100 | 低于此长度的页面会被过滤 |
| `EMBEDDING_BATCH_SIZE` | 256 | 每批次本地向量化的文本数量 |

---

## API 参考

### RAG 微服务 (port 3002)

#### `GET /health`
健康检查，返回知识库状态。

**响应示例：**
```json
{ "status": "ok", "chunks": 12345, "collection": "autocad_help" }
```

#### `GET /stats`
详细统计信息。

#### `POST /search`
语义检索 — 核心接口。

**请求：**
```json
{ "query": "HATCH 命令的选项和参数", "top_k": 5 }
```

**响应：**
```json
{
  "results": [
    {
      "text": "[常用选项（"图案填充和渐变色"对话框）]\n定义由渐变和图案填充共享的边界...",
      "title": "常用选项（"图案填充和渐变色"对话框）",
      "source": "GUID-006BE8D3-0731-47BA-A7CF-1B50282CD108.htm",
      "cmdname": "HATCH",
      "topic_type": "concept",
      "score": 0.8234
    }
  ],
  "query": "HATCH 命令的选项和参数",
  "total": 5
}
```

#### `POST /search_by_command?cmdname=HATCH&top_k=5`
按命令名精确检索。

---

## 费用说明

### 完全免费（本地模型）

Embedding 使用本地模型 `BAAI/bge-small-zh-v1.5`（sentence-transformers），**索引构建和检索均零费用**：

- **索引构建**: 本地 CPU/GPU 计算，无需网络调用
- **检索**: 本地向量化 query + ChromaDB 本地相似度搜索
- **模型下载**: 首次运行自动从 HuggingFace 下载（约 93MB），之后从本地缓存加载

---

## 故障排除

### Q: build_index.py 首次运行很慢
首次运行需要从 HuggingFace 下载 `bge-small-zh-v1.5` 模型（约 93MB）。如果下载慢，可设置 HuggingFace 镜像：`HF_ENDPOINT=https://hf-mirror.com python build_index.py`

### Q: rag_server.py 启动报 "ChromaDB 数据目录不存在"
请先运行 `python build_index.py` 构建索引。

### Q: AI 没有调用知识库检索工具
检查 Node.js 后端的 `.env` 中是否配置了 `RAG_SERVER_URL=http://localhost:3002`，以及 RAG 微服务是否在运行。如果 RAG 服务未启动，该工具会返回"知识库检索失败"但不会影响绘图功能。

### Q: 检索结果不够准确
- 调整 `CHUNK_SIZE`（较小的块更精确，较大的块保留更多上下文）
- 增加 `top_k`（返回更多结果）
- 换用更大的本地模型如 `BAAI/bge-large-zh-v1.5`（更准确，但加载更慢、占用更多内存）

### Q: 想使用 GPU 加速
`sentence-transformers` 支持 CUDA GPU。安装 PyTorch GPU 版本后，模型会自动使用 GPU 加速向量化。

---

## 后续扩展

### 添加 ODA SDK 文档
ODA 的 API 文档 (docs.opendesign.com) 如果你有离线 HTML 版本，可以直接放入 `HelpHtml/` 目录一起索引。

### 添加行业标准文档
将 GB/T、ISO 等绘图标准的 HTML/PDF 转文本后放入 `HelpHtml/` 目录。

### 升级到更强的 Embedding 模型
修改 `.env` 中的 `EMBEDDING_MODEL` 为 `BAAI/bge-large-zh-v1.5`（或其他 sentence-transformers 兼容模型），然后重新运行 `python build_index.py` 全量重建。

### 集成到 Dify / AnythingLLM
如果将来需要更强大的知识库管理 UI，可以将 ChromaDB 数据迁移到 Dify 等平台。
