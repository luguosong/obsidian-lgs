# reference-docs — 密码学国家标准 Wiki-First 知识库

## 概述

`reference-docs` 是 Claude Code 的自定义 skill，管理 **130+ 份中国密码学国家标准**（GB/T、GM/T、GB/Z）的结构化知识库。采用 Wiki-First 架构：PDF → MinerU 解析 → LLM 生成 Wiki 页面 → 混合检索（BM25 + 向量 + 图扩展）。

**Skill 路径**：`upda-code/.claude/skills/reference-docs/SKILL.md`
**知识库路径**：`upda-code/references/`

## 何时触发

涉及密码学标准实现时，Claude Code 自动触发此 skill。典型场景：

| 触发场景 | 搜索关键词示例 |
|---------|--------------|
| SM2 签名/验签实现 | `SM2 数字签名算法流程` |
| SM3 哈希实现 | `SM3 填充规则` |
| SM4 加解密实现 | `SM4 工作模式` |
| 证书格式/扩展 | `数字证书 TBSCertificate 结构` |
| OCSP 协议 | `OCSP 请求响应格式` |
| TSA 时间戳 | `时间戳令牌格式` |
| 电子印章 | `SES_Seal 数据结构` |
| 标准间关系 | `SM2 相关标准` |

也可以直接说「查一下 XX 国标」「XX 规范怎么说」「摄入新标准」。

## 架构

```
references/
├── raw/              ← 原始 PDF（按领域分 11 个子目录，130 份标准）
│   ├── sm2/          ← 16 份：SM2 椭圆曲线公钥密码
│   ├── sm3/          ← 3 份：SM3 杂凑算法
│   ├── sm4/          ← 1 份：SM4 分组密码
│   ├── sm9/          ← 11 份：SM9 标识密码
│   ├── zuc/          ← 6 份：祖冲之序列密码
│   ├── pki/          ← 19 份：PKI/证书/CRL/OCSP
│   ├── seal/         ← 10 份：电子签章/印章
│   ├── tls-vpn/      ← 7 份：TLCP/SSL VPN/IPSec
│   ├── device/       ← 14 份：密码机/密码钥匙/签名验签
│   ├── testing/      ← 5 份：检测/审计
│   └── others/       ← 38 份：通用密码应用/法规
├── parsed/           ← MinerU 解析产出（markdown + 注册表）
├── wiki/             ← Wiki 层（LLM 维护的结构化页面）
│   ├── standards/    ← 每个标准一个 .md
│   ├── concepts/     ← 跨标准概念页面
│   ├── comparisons/  ← 对比分析页面
│   ├── relations/    ← 关系页面
│   ├── schema.md     ← 页面结构规则
│   └── purpose.md    ← 知识库方向
├── vectors/          ← FAISS 向量索引 + chunks.json
├── graph/            ← 知识图谱（四信号加权模型）
└── scripts/          ← 12 个 Python 模块 + 45 个单元测试
```

## 四大能力

### 能力 1：混合检索

BM25 关键词 + FAISS 语义向量 + RRF 融合 + 1 跳图扩展。

```bash
cd references/scripts

# 基本查询
python search.py -q "SM2 数字签名流程" -k 5

# JSON 输出（程序调用）
python search.py -q "电子印章 ASN.1 数据结构" --json

# 更多结果
python search.py -q "PKI 证书体系相关标准" -k 10
```

**检索结果标记**：
- `[BM25+Vector]` — 关键词 + 语义同时命中，可信度高
- `[BM25]` — 仅关键词命中
- `[Vector]` — 仅语义匹配
- `[Graph]` — 图扩展发现的相关标准

### 能力 2：查看标准间关系

```bash
# 图谱洞察（枢纽标准、孤立标准、社区划分）
python -c "import json; print(json.dumps(json.load(open('../graph/insights.json')), ensure_ascii=False, indent=2))"

# 查看特定标准的 wiki 页面
cat ../wiki/standards/GMT-0003.1.md
```

### 能力 3：摄入新标准

```bash
cd references/scripts

# 1. 解析 PDF（MinerU）
python mineru_parse.py --file "path/to/new-standard.pdf"

# 2. 增量构建 Wiki 页面（单个标准）
python build_wiki.py --incremental GMT-0003.1

# 3. 重建向量索引（检测变化才重建）
python build_vectors.py --incremental

# 4. 重建知识图谱
python build_graph.py --insights
```

### 能力 4：健康检查

```bash
python lint_wiki.py          # 控制台报告
python lint_wiki.py --json   # JSON 输出
```

检查项：孤儿页面、断链、缺失 frontmatter、空页面。

## 核心模块说明

| 模块 | 职责 |
|------|------|
| `mineru_parse.py` | PDF → markdown 解析，SHA-256 去重，领域自动分类 |
| `build_wiki.py` | LLM 生成 wiki 页面（阶段 1 标准页 + 阶段 2 概念页），断点续传 |
| `build_vectors.py` | Wiki 页面 → FAISS 索引，增量更新检测 |
| `build_graph.py` | 四信号加权知识图谱 + Louvain 社区检测 |
| `search.py` | BM25 + FAISS + RRF 融合 + 图扩展混合检索 |
| `lint_wiki.py` | Wiki 结构健康检查 |
| `llm_client.py` | Claude API 封装，断点续传，JSON 鲁棒提取 |
| `param_validator.py` | 参数交叉验证（hex/OID/长度从原文精确比对） |
| `cjk_tokenizer.py` | CJK bigram 分词 + OID 保护 + 停用词过滤 |
| `context_budget.py` | 检索结果 token 预算裁剪 |
| `markdown_utils.py` | 标准编号提取 + 按章节分块 |

## 技术要点

### 检索流程

```
用户查询 → CJK 分词 → BM25 检索 ──┐
                     → 语义向量检索 ─┤→ RRF 融合 → 图扩展 → 预算裁剪 → 返回
```

- **RRF 公式**：`score(p) = 1/(k + bm25_rank) + 1/(k + vector_rank)`，k=60
- **向量模型**：`paraphrase-multilingual-MiniLM-L12-v2`（多语言，384 维）
- **BM25 缓存**：pickle 序列化到 `vectors/bm25_cache.pkl`，文件集变化时自动重建

### 知识图谱四信号

| 信号 | 权重 | 说明 |
|------|------|------|
| 直接链接 | 3.0 | `[[wikilink]]` 引用 |
| 共享基础标准 | 4.0 | 多个标准引用同一基础标准 |
| Adamic-Adar | 1.5 | 共同邻居相似度 |
| 类型亲和度 | 1.0 | standard-standard 最强，concept-concept 较弱 |

### 断点续传

`build_wiki.py` 使用 `CheckpointState`（`wiki/.build_state.json`）记录每个 LLM 调用的结果。中断后重新运行会自动跳过已完成的标准，避免重复 API 调用。

### 参数验证

`param_validator.py` 从原始 markdown 和 wiki 页面分别提取数值参数（hex、OID、长度、变量赋值），交叉比对确保 LLM 未篡改精确值。不匹配时写入 wiki 页面的「参数验证警告」章节。

## 全量构建流程

从零开始构建整个知识库：

```bash
cd references/scripts

# 前置：安装依赖
pip install anthropic rank-bm25 faiss-cpu sentence-transformers pytest

# 前置：设置 API Key
set ANTHROPIC_API_KEY=sk-ant-...

# 1. 解析所有 PDF（需 MinerU）
python mineru_parse.py --rebuild-all

# 2. 构建 Wiki 页面（阶段 1 + 2，约 400 次 LLM 调用）
python build_wiki.py

# 3. 构建向量索引
python build_vectors.py --force

# 4. 构建知识图谱
python build_graph.py --insights

# 5. 健康检查
python lint_wiki.py

# 6. 运行测试
python -m pytest tests/ -v
```

## 在代码中引用标准

当实现密码学相关功能时，代码注释必须标注来源标准：

```java
// 依据 GB/T 38540-2020 第 6.1 条：SES_Seal 数据结构定义
// 参见 wiki: [[GB-T-38540]]

// 依据 GM/T 0003.1-2012 第 5 节：SM2 系统参数
// 素数 p = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF
```

## 相关笔记

- [[UOCS开发/架构总览/架构总览|架构总览]]
- [[UOCS开发/drawing-cad/AI后端/RAG知识库|RAG知识库（CAD 行业标准）]]
- [[UOCS开发/drawing-ofd/OAuth2认证体系/OAuth2认证体系设计与实现|OAuth2 认证体系]]
