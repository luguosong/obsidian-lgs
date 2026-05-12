# Redis + MySQL 优化方案（已落地）

> drawing-ai-server 三层缓存 + 双向兜底架构。**状态：P1–P4 全量实施完成（含质量校验 6 个问题全部修复），80 单元测试全通过，E2E 实测首问→二问 -30% 响应时间。**

## 架构全景

```
┌──────────────────────────────────────────────────────────────┐
│ 请求入口 (ChatService / ReviewCoordinator)                   │
├──────────────────────────────────────────────────────────────┤
│ 🛡️ RateLimiter (Redis 滑动窗口) + Resilience4j 熔断          │
├──────────────────────────────────────────────────────────────┤
│ L0: Caffeine 本地缓存  (~10μs，进程内)                       │
│    ↓ miss                                                     │
│ L1: Redis  (~1-2ms，TTL ±10% 抖动)                            │
│    ↓ miss → 🔒 SingleFlight (防击穿) + 🔍 Bloom (防穿透)     │
│ L2: MySQL / Qdrant / LLM  (事实来源)                          │
├──────────────────────────────────────────────────────────────┤
│ 📊 准确性反哺：ReviewHistory → PromptSection                  │
│    Qdrant 跨会话 QA 语义缓存 + HotQueryTracker 热榜预热      │
└──────────────────────────────────────────────────────────────┘
```

## 阶段落地

### P1 基础设施

| 组件 | 位置 | 作用 |
|------|------|------|
| `TieredCacheTemplate<V>` | `cache/` | L0 Caffeine + L1 Redis 统一读写模板（Cache-Aside） |
| `TtlJitter` | `cache/` | TTL ±10% 抖动工具，防雪崩 |
| `SingleFlightExecutor` | `cache/` | Redis `SET NX` + Lua 原子释放，防击穿 |

### P2 速度优化

| 组件 | 路径 | 收益 |
|------|------|------|
| `CachedEmbeddingModel` | `embedding/` | query→vector Redis 缓存，TTL 7d ±10%；Base64(float[] LE)；批量部分命中；命中省 100-300ms 或 Ollama 10s+ |
| RagService 三层缓存 | `service/RagService` | L0 Caffeine + L1 Redis + SingleFlight；热 query 预热（`HotQueryTracker`） |
| ToolOrchestrator fileId 级缓存 | `engine/tool/ToolOrchestrator` | 只读 DWG 工具跨会话复用；三级缓存 L0 Caffeine → L1 Redis → L2 `cad_dwg_snapshot` MySQL；错误负缓存 2 分钟 ±20% 抖动；256KB 大 key 保护（可配 `app.cache.tool.max-value-bytes`） |
| `DwgSnapshotRepository` | `persistence/` | L2 MySQL 兜底：`find/upsert/deleteByFileId` + `@PostConstruct ensureSchema`，异常 fail-open |
| DrawingMemory 截断归档（轻量方案） | `memory/DrawingMemoryStore` + `persistence/DrawingMemoryArchiveRepository` | `MAX_QA_ENTRIES=150`（原 30），超限时 `addQaEntry` 返回被驱逐条目，单线程 daemon 异步落盘到 `cad_drawing_memory_archive`；`@PreDestroy` 3s 优雅关闭 |

### P3 准确性优化

| 组件 | 功能 |
|------|------|
| `ReviewHistoryPromptSection` | 同 fileId 二次审图时加载 Redis 审图摘要（critical_count / top5_issues）；miss 从 `cad_review_report` 聚合 |
| `CrossSessionQaCacheService` | Qdrant 集合 `ai_qa_cache` + Redis 命中计数 + MySQL `cad_qa_library` 沉淀；相似度阈值 0.92 |
| `DrawingMemoryInitService` 分布式锁 | Redis `SET NX EX 60` + 双重检查，多实例部署不重入 |

### P4 健壮性加固

| 组件 | 说明 |
|------|------|
| Resilience4j 熔断 | `EmbeddingModel` / `VectorStore` / `ChatModel` 三处；阈值 50-60%，开路 20-30s |
| Redis 滑动窗口限流 | 统一实现 `SlidingWindowRateLimiter`（key 前缀 `ai:rl:*`），per-clientId 30/min+200/hour，全局 20 LLM/sec；Lua 原子 `ZADD/ZREMRANGEBYSCORE/ZCARD`；`RateLimitFilter` + `ChatService` 共用同一限流器 |
| `RedisBloomFilter` | 启动从 `cad_chat_session` 加载 clientId+fileId；miss Bloom → 负缓存 60s |
| `HotQueryTracker` | 每 30 min 扫描 top-20 热 query 升级逻辑过期；启动从 `cad_rag_hot_query` 预热 |
| `@PreDestroy` 兜底写回 | SessionMemoryStore L1 强制 persist，5s 超时 |

## 新增 MySQL 表

所有表 `IF NOT EXISTS`，存放于 `schema-v2.sql`：

| 表 | 用途 |
|----|------|
| `cad_dwg_snapshot` | 跨会话 DWG 解析快照（配合 fileId 级缓存），`DwgSnapshotRepository` |
| `cad_qa_library` | 跨会话 QA 沉淀（Qdrant payload 回写） |
| `cad_rag_hot_query` | RAG 热 query 启动预热来源 |
| `cad_drawing_memory_archive` | DrawingMemory 截断条目归档，`DrawingMemoryArchiveRepository`，payload JSON 数组 |

## Micrometer 指标清单（30+）

全部以 `ai.*` 命名空间，tag `service=xxx` 区分：

| 指标组 | service tag | 指标样例 |
|--------|-------------|---------|
| 三层缓存 | `tiered-cache` | `ai.cache.l0.hit` / `ai.cache.l1.hit` / `ai.cache.miss` |
| RAG | `rag` | `cache.gets{cache=rag,result=hit/miss}` |
| 会话记忆 | `session-memory` | `ai.session.memory.l1.hit` / `l2.hit` / `created` / `read.errors` / `write.errors` / `l1.size` 等 7 |
| [[图纸记忆]] | `drawing-memory` | 同 session-memory 的 7 |
| Embedding 缓存 | `embedding-cache` | `ai.embedding.cache.hit` / `miss` / `redis.read.errors` / `redis.write.errors` |
| QA 跨会话 | `qa-cache` | `ai.qa-cache.read.hit` / `write.count` / `circuit.open` |
| Bloom 过滤器 | `bloom-filter` | `ai.bloom.reject` / `ai.bloom.pass` |

## E2E 实测数据（单实例 localhost）

| 场景 | 数值 |
|------|------|
| 首问冷启动（"CAD总平面图的图层命名应该遵循什么规范？"） | 89s（4 次 RAG miss） |
| 二问相同问题 | 62s（**-30%**，SessionMemory 直答绕过 RAG） |
| Redis embedding key 写入验证 | `ai:embedding:v1:ollama:text-embedding-v4:*` 可见 |
| 80 单元测试（49 基础 + 31 本轮补充：C1 路径 18 + H1 路径 13） | BUILD SUCCESS / 0 failures |

## 配置开关（application.yml）

```yaml
app:
  embedding.cache.enabled: true                # CachedEmbeddingModel 开关
  cache:
    l0:
      rag-max-size: 1000                       # RAG L0 容量
      rag-ttl-minutes: 18                      # L1 60min × 30%
      tool-max-size: 500                       # 工具 L0 容量
      tool-ttl-minutes: 9                      # L1 30min × 30%
    single-flight:
      wait-ms: 3000                            # SingleFlight 等待超时
    tool:
      max-value-bytes: 262144                  # 工具结果 256KB 大 key 阈值
  rate-limit:
    enabled: true
    per-client: { chat-per-minute: 30, chat-per-hour: 200 }
    global: { llm-per-second: 20 }
  bloom-filter:
    enabled: true
    expected-insertions: 1000000
    false-positive-probability: 0.01
```

## 回归与验证

- **单测**：`mvn test` — 49 tests，覆盖 TieredCache / SingleFlight / TtlJitter / HotQueryTracker / RedisBloomFilter / CachedEmbeddingModel / QaCache / RateLimit
- **实测**：Actuator `GET /actuator/metrics/ai.embedding.cache.*` 指标值递增；`docker exec uocs-redis redis-cli --scan --pattern "ai:embedding:v1:*"` 可见 key
- **回滚**：所有新增组件可通过 `app.*.enabled=false` 单独关闭；新 MySQL 表独立 `schema-v2.sql`，不影响主 schema

## 不做的事（明确边界）

- ❌ 不引入 Canal / Debezium（Cache-Aside 已足够）
- ❌ 不引入 Redisson（Spring Data Redis + Lua 够用）
- ❌ 不改 SSE / Harness 核心流程（只在缓存层/Prompt Section 增强）
- ❌ 不改前端（对 drawing-web-app 透明）
