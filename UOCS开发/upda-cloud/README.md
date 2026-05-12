# upda-cloud — 后端微服务 + 管理前端

> UPDA Cloud 是 UOCS 平台的核心业务系统。

## 这个子项目做什么？

upda-cloud 包含两个独立仓库：

- **后端**（`upda-cloud-server/`）— Spring Cloud 微服务集群，包括 API Gateway、OAuth2 授权服务器、CA 证书引擎、RA 签发代理、电子印章管理、签章服务等 7 个服务
- **前端**（`upda-cloud-client/`）— React + Vite 管理平台，覆盖证书管理、印章管理、用户权限等业务界面

## 核心概念

### 请求怎么流转？

```
浏览器 → Gateway(:18010) → AuthGlobalFilter(JWT验证)
  → 注入 X-User-Id / X-User-Roles / X-User-Scopes 头
  → Nacos 路由到目标微服务
  → Controller → Service → Mapper(DB) / Feign Client
```

### 微服务分工

| 服务 | 职责 | 端口 |
|------|------|------|
| `server-gateway` | API 网关，路由与鉴权 | 18010 |
| `server-auth` | OAuth2 授权服务器 | 18011 |
| `service-basic` | 用户/RBAC/MinIO | 内部 |
| `service-ca` | 证书引擎(签发/吊销/OCSP/TSA) | 内部 |
| `service-ra` | RA 证书签发代理 | 18012 |
| `service-seal` | 印章生命周期与注册编排 | 内部 |
| `service-signer` | 独立签章服务(第三方集成) | 内部 |

## 子目录

| 目录 | 内容 |
|------|------|
| [[后端架构/]] | 后端架构文档，含 Entity 对照表 |
| [[前端架构/]] | 前端架构文档（待补充） |

## 关键设计决策

- **三级 PKI 体系**：CA → RA → 终端实体证书，RA 专注身份核验，CA 专注证书签发
- **注册编排**：已从 RA 迁移到 Seal 服务，调用链是 `Seal → RaClient → RA → CA`
- **CA 内部接口隔离**：`/internal/**` 仅供 Feign 调用，Gateway 拦截外部访问
- **配置管理**：Nacos 3.1 是唯一配置中心，本地 `application.yml` 只保留连接信息
