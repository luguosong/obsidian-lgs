# drawing-ofd — OFD 查看器 + 签章后端

> OFD（开放版式文档）查看器前端 + Spring Boot 签章后端，已完整接入 UOCS OAuth2 认证。

## 为什么 OFD 需要独立后端？

OFD 是中国国家标准版式文档格式（类似 PDF）。与 PDF 查看器不同，OFD 项目需要一个签章后端来：

1. **验证用户身份** — 通过 UOCS OAuth2 PKCE 流程获取 Token
2. **代理调用印章接口** — 用 Bearer Token 调用 UOCS Gateway 的印章 API
3. **处理签章操作** — 在 OFD 文档上盖章

这构成了一个典型的 "第三方应用接入 UOCS" 的范例。

## 两个组件

```
┌─────────────────────────┐     ┌─────────────────────────┐
│   drawing-ofd-app       │     │   drawing-ofd-server    │
│   React 19 + MUI 7     │     │   Spring Boot 3         │
│   :5201                 │────→│   :5212                 │
│                         │     │                         │
│   - OFD 文件渲染(jszip) │     │   - OAuth2 Resource     │
│   - SM2/SM3 签名验证    │     │     Server (JWKS)       │
│   - PKCE 认证流程       │     │   - 印章 API 代理       │
└─────────────────────────┘     └────────────┬────────────┘
                                             │
                                    Bearer Token
                                             │
                                    ┌────────▼────────────┐
                                    │   UOCS Gateway       │
                                    │   :18010             │
                                    │   - 验证 Token       │
                                    │   - 路由到 Seal 服务 │
                                    └─────────────────────┘
```

## 技术栈

### 前端 (drawing-ofd-app)

| 技术 | 用途 |
|------|------|
| React 19 | UI 框架 |
| MUI 7 | 组件库 |
| MobX 6 | 状态管理 |
| jszip | OFD 文件解析（OFD 本质是 ZIP 包） |

### 后端 (drawing-ofd-server)

| 技术 | 用途 |
|------|------|
| Spring Boot 3 | 后端框架 |
| Spring Security OAuth2 | Resource Server，验证 Bearer Token |
| JWKS | 从 `:18011/oauth2/jwks` 获取公钥验证 Token |

## 核心文档

| 文档 | 说明 |
|------|------|
| [[OAuth2认证体系/OAuth2认证体系设计与实现]] | 完整的 OAuth2 对接指南，含 PKCE、Mode A/B、HMAC 签名 |

## 值得学习的设计

OFD 项目是 UOCS "第三方应用接入" 的参考实现：

- **PKCE 流程** — 前端用 code_verifier / code_challenge 实现 SPA 安全认证
- **Token 代理模式** — 后端验证 Token 后代理调用 Gateway，前端不直接接触 UOCS
- **CORS 配置** — 后端精确允许 `:5201` 来源
