# GitHub 登录原理

## 概述

upda-cloud 使用 **OAuth2 Authorization Code + PKCE** 双重架构实现 GitHub 登录：

- 前端 SPA 通过 PKCE 与自建 Auth Server 交互（SPA → Auth Server）
- Auth Server 再作为 OAuth2 Client 与 GitHub 交互（Auth Server → GitHub）
- 认证方式为 **GitHub OAuth App**（非 Personal Access Token），授权类型 `AUTHORIZATION_CODE`

```
┌──────────────┐    PKCE Auth Code    ┌──────────────┐    OAuth2 Auth Code    ┌──────────┐
│  前端 SPA    │ ──────────────────→  │  Auth Server │ ──────────────────→   │  GitHub  │
│ (uocs-client)│ ←────────────────── │    (auth)    │ ←──────────────────   │ OAuth App│
└──────────────┘   JWT access_token   └──────────────┘   GitHub access_token  └──────────┘
```

---

## OAuth2 原理入门

> 这一节从零讲清楚 OAuth2 的核心思想。如果你已经熟悉 OAuth2 / OIDC，可以跳到 [[#完整时序图]]。

### OAuth2 解决什么问题？

想象你去酒店入住，前台给你一张**房卡**而不是房间钥匙。房卡有几个特点：

- 它不是万能钥匙，只能开你的房间门、刷电梯、去健身房
- 它有有效期，过期作废
- 你随时可以要求前台注销这张卡

OAuth2 做的就是这件事——**让用户给第三方应用发一张"临时房卡"，而不是把密码交出去**。

没有 OAuth2 的世界里，如果你想用一个第三方 Git 统计工具查看你的 GitHub 数据，你得把 GitHub 密码交给它。这就像把家门钥匙交给酒店前台一样危险。

### 四个核心角色

OAuth2 定义了四个参与者，用一个类比来记：

```
你（用户）              →  Resource Owner       — 拥有数据的人
第三方应用              →  Client               — 想访问你数据的应用
GitHub（身份提供商）    →  Authorization Server — 签发"房卡"的服务器
GitHub API（数据源）    →  Resource Server      — 存储你数据的服务器
```

在本项目中角色对应：

| OAuth2 角色 | 本项目中的对应 |
|---|---|
| Resource Owner | 使用浏览器的最终用户 |
| Client（对外部 IdP） | Auth Server（auth 模块） |
| Client（对前端 SPA） | 前端 SPA（uocs-client） |
| Authorization Server（对外部 IdP） | GitHub OAuth App |
| Authorization Server（对前端 SPA） | Auth Server（auth 模块） |
| Resource Server | GitHub API / UOCS 业务服务 |

注意 Auth Server 身兼两职：它对 GitHub 是 Client，对前端又是 Authorization Server。这就是 [[#概述]] 里说的"双重 OAuth2 角色"。

### Authorization Code 流程（5 步）

OAuth2 有多种授权方式（Grant Type），本项目使用的是最安全的 **Authorization Code**。整个流程分 5 步：

```mermaid
%%{init: {'sequence': {'useMaxWidth': true}}}%%
sequenceDiagram
    actor User as 用户
    participant Client as 第三方应用<br/>(Client)
    participant AuthServer as 授权服务器<br/>(Authorization Server)
    participant Resource as 资源服务器<br/>(Resource Server)

    Note over User,Resource: 第 1 步：用户发起授权请求
    User->>Client: 点击"GitHub 登录"
    Client->>AuthServer: 302 跳转到授权页面<br/>携带 client_id + redirect_uri + scope + state

    Note over User,Resource: 第 2 步：用户同意授权
    AuthServer-->>User: 显示授权页面（"XX 应用想访问你的 GitHub 数据"）
    User->>AuthServer: 点击"同意"

    Note over User,Resource: 第 3 步：授权服务器返回 Authorization Code
    AuthServer->>Client: 302 跳转回 redirect_uri?code=AUTH_CODE&state=xxx

    Note over User,Resource: 第 4 步：Client 用 Code 换取 Token
    Client->>AuthServer: POST /token<br/>code + client_id + client_secret
    AuthServer-->>Client: access_token (+ refresh_token)

    Note over User,Resource: 第 5 步：用 Token 访问资源
    Client->>Resource: GET /api/user<br/>Authorization: Bearer access_token
    Resource-->>Client: 用户数据
```

**为什么要分两步（先拿 Code 再换 Token）？**

这是 Authorization Code 流程的核心安全设计：

1. Authorization Code 通过浏览器 URL 参数传递（302 重定向），浏览器地址栏可见
2. Access Token 在后端服务器之间直接交换（POST 请求），从不经过浏览器
3. 如果攻击者截获了 Code，他没有 `client_secret`，也无法换取 Token

```
浏览器（不安全，URL 可见）    →  只传 Authorization Code
后端服务器（安全，TLS 加密）  →  传 client_secret + Code 换 Token
```

### PKCE — 给 SPA 用的安全加固

传统的 Authorization Code 流程要求 Client 有一个后端服务器来安全保管 `client_secret`。但本项目的前端是纯 SPA（没有后端），`client_secret` 如果放在前端代码里就等于公开了。

**PKCE（Proof Key for Code Exchange，发音 "pixy"）** 就是解决这个问题的：

```mermaid
%%{init: {'sequence': {'useMaxWidth': true}}}%%
sequenceDiagram
    participant Browser as 浏览器（SPA）
    participant Auth as Authorization Server

    Browser->>Browser: 1. 生成随机字符串 code_verifier
    Browser->>Browser: 2. code_challenge = SHA256(code_verifier)

    Browser->>Auth: 3. 授权请求，携带 code_challenge
    Auth->>Auth: 记住 code_challenge
    Auth->>Browser: 4. 返回 Authorization Code

    Browser->>Auth: 5. 用 Code 换 Token，携带 code_verifier
    Auth->>Auth: 6. 验证 SHA256(code_verifier) == 之前存的 code_challenge
    Auth->>Browser: 7. 签发 Token
```

**PKCE 的安全逻辑**：

- 第 3 步：浏览器告诉 Auth Server "我的 challenge 是 X"（X 是 verifier 的哈希）
- 第 5 步：浏览器出示原始 verifier，Auth Server 验证哈希是否匹配
- 攻击者如果截获了 Code，他不知道 verifier（在第 1 步生成后一直藏在浏览器内存里），所以无法完成第 5 步

用一句话总结：**PKCE 让没有 client_secret 的 SPA 也能安全使用 Authorization Code 流程**。

### State 参数 — 防 CSRF

你可能注意到每次授权请求都带一个 `state` 参数。这是为了防止 **CSRF（跨站请求伪造）** 攻击：

```
1. SPA 生成随机 state，存到 sessionStorage
2. 发起授权请求时带上 state
3. Auth Server 回调时原样返回 state
4. SPA 对比返回的 state 和自己存的是否一致
```

如果攻击者构造了一个恶意链接，诱导用户点击后拿到一个别人的 Authorization Code 回调到你的应用——但这个回调里的 `state` 和你之前存储的对不上，请求就会被拒绝。

### Token 的生命周期

OAuth2 令牌有三种，各有用途：

| Token 类型 | 作用 | 有效期 | 本项目存储位置 |
|---|---|---|---|
| **Authorization Code** | 一次性凭证，换取 Token | 极短（通常 10 分钟） | URL 参数，用完即弃 |
| **Access Token** | 访问资源的凭证 | 短（通常 1 小时） | sessionStorage |
| **Refresh Token** | 刷新 Access Token 的凭证 | 长（通常 30 天） | sessionStorage |

```mermaid
%%{init: {'stateDiagram': {'useMaxWidth': true}}}%%
stateDiagram-v2
    [*] --> AuthorizationCode: 用户授权
    AuthorizationCode --> AccessToken: Code + code_verifier 换取
    AccessToken --> Expired: TTL 到期
    Expired --> AccessToken: Refresh Token 刷新
    Expired --> ReLogin: Refresh Token 也过期
    ReLogin --> AuthorizationCode: 重新走授权流程
    AccessToken --> [*]: 登出
```

本项目的前端 `CoreStore.refreshTokenIfNeeded()` 会在 Access Token 过期前 120 秒自动用 Refresh Token 刷新，用户无感知。

### JWT — Access Token 的内部结构

本项目的 Access Token 是 JWT（JSON Web Token）格式。JWT 由三段 Base64URL 编码的字符串组成，用 `.` 分隔：

```
eyJhbGciOiJS256.eyJ1c2VySWQiOiIxMjM0.RSA_SIGNATURE
├─ Header ────────┤├─ Payload ──────┤├─ Signature ──┘
```

**Header**（算法信息）：

```json
{
  "alg": "RS256",    // RSA + SHA-256 签名
  "typ": "JWT"
}
```

**Payload**（业务数据，本项目注入的 claims）：

```json
{
  "iss": "https://auth.uocs.com",   // 签发者（Auth Server）
  "sub": "admin",                    // 主体（UOCS 用户名）
  "aud": "uocs-client",             // 受众（前端 client_id）
  "exp": 1716100000,                 // 过期时间
  "iat": 1716096400,                 // 签发时间
  "userId": "550e8400-e29b-41d4",   // UOCS 业务字段
  "roles": ["USER", "SEAL_USER"],   // UOCS 业务字段
  "scope": "read write"             // OAuth2 权限范围
}
```

**Signature**（防篡改签名）：

用 Auth Server 的 RSA 私钥对 `Header.Payload` 签名。Gateway 用对应的公钥验证，确保 Token 没有被篡改。

> **JWT vs opaque token**：JWT 是自包含的，任何人都可以解码 Payload（只是 Base64），但无法伪造，因为签名需要私钥。所以 **JWT 里不要放密码等敏感信息**，只放用户标识和权限就够了。

### Scope — 权限粒度控制

GitHub OAuth 的 scope 决定了第三方应用能访问你多少数据：

| Scope | 能访问什么 | 本项目是否使用 |
|---|---|---|
| `read:user` | 读取用户公开资料（id、login、avatar） | 是 |
| `user:email` | 读取用户邮箱（即使是私密邮箱） | 是 |
| `repo` | 读写用户的仓库 | 否 |
| `gist` | 读写 Gist | 否 |

本项目只请求了 `read:user` 和 `user:email`，这是最小权限原则——只申请登录所需的最低权限。

### OpenID Connect（OIDC）vs 纯 OAuth2

OAuth2 只解决"授权"（你能访问什么），不解决"认证"（你是谁）。OIDC 在 OAuth2 之上加了一层，提供 `id_token`（一个 JWT，包含用户身份信息）来标准化认证。

本项目的做法介于两者之间：
- 使用标准 OAuth2 Authorization Code 流程获取 GitHub Access Token
- 手动调用 GitHub UserInfo API（`/api/github/user`）获取用户身份
- 在 Auth Server 内部将用户信息映射为 UOCS 用户

这本质上是 **OAuth2 + 自定义认证逻辑**，没有使用完整的 OIDC 协议。

---

## 完整时序图

### GitHub 登录流程

```mermaid
%%{init: {'sequence': {'useMaxWidth': true}}}%%
sequenceDiagram
    actor User as 用户浏览器
    participant SPA as 前端 SPA<br/>(uocs-client)
    participant Auth as Auth Server<br/>(auth)
    participant GH as GitHub
    participant Basic as services-basic<br/>(用户服务)

    User->>SPA: 访问受保护页面
    SPA->>SPA: PrivateRoute 检测无 token
    SPA->>SPA: 生成 PKCE code_verifier + code_challenge + state
    SPA->>SPA: sessionStorage 暂存 PKCE 数据
    SPA->>Auth: 302 → /oauth2/authorize?response_type=code&client_id=uocs-client&code_challenge=xxx&state=xxx
    Auth->>Auth: 用户未登录，302 → /login（Thymeleaf 页面）
    Auth-->>User: 渲染登录页，显示 GitHub 按钮

    User->>Auth: 点击 GitHub 按钮 → /oauth2/authorization/github
    Auth->>GH: 302 → https://github.com/login/oauth/authorize?client_id=xxx&scope=read:user,user:email
    GH-->>User: GitHub 授权页面

    User->>GH: 同意授权
    GH->>Auth: 302 → /login/oauth2/code/github?code=AUTH_CODE
    Auth->>GH: POST /login/oauth/access_token (code + client_secret)
    GH-->>Auth: GitHub access_token

    Auth->>GH: GET https://api.github.com/user (Authorization: Bearer token)
    GH-->>Auth: GitHub 用户信息 (id, login, email, avatar_url)

    Auth->>Auth: FederatedIdentityOAuth2UserService.loadUser()
    Note over Auth: session 中无 bind_user_id → 登录模式

    Auth->>Basic: Feign GET /internal/identity/github/{externalId}
    alt 已关联 UOCS 用户
        Basic-->>Auth: 返回 AuthUserInfoRespDTO
    else 首次登录（JIT Provisioning）
        Auth->>Basic: Feign POST /internal/federated-user
        Note over Basic: 创建 User (username=github_{login}, 随机密码)<br/>分配默认角色 USER + SEAL_USER<br/>创建 UserIdentityProvider 关联
        Basic-->>Auth: 返回 AuthUserInfoRespDTO
    end

    Auth->>Auth: 构建 FederatedOAuth2User (uocsUserId + roles)
    Auth->>Auth: OAuth2TokenCustomizer 注入 userId, roles 到 JWT
    Auth->>SPA: 302 → /oauth2/callback?code=AUTH_CODE&state=xxx

    SPA->>SPA: 验证 state 防 CSRF
    SPA->>Auth: POST /oauth2/token (code + code_verifier)
    Auth-->>SPA: JWT access_token + refresh_token

    SPA->>SPA: sessionStorage 存储 token
    SPA->>Auth: GET /basic/user/permissions (Authorization: Bearer token)
    Auth-->>SPA: 角色、权限、菜单树
    SPA->>SPA: 跳转到登录前页面
```

### GitHub 账号绑定流程

```mermaid
%%{init: {'sequence': {'useMaxWidth': true}}}%%
sequenceDiagram
    actor User as 已登录用户
    participant SPA as 前端 SPA
    participant Auth as Auth Server
    participant GH as GitHub
    participant Basic as services-basic

    User->>SPA: Profile 页点击"绑定 GitHub"
    SPA->>SPA: window.open(authServerUrl + "/bind/start/github?token=ACCESS_TOKEN")
    SPA->>Auth: GET /bind/start/github?token=ACCESS_TOKEN

    Auth->>Auth: JwtDecoder 验证 access_token，提取 userId
    Auth->>Auth: session.setAttribute("bind_user_id", userId)
    Auth->>Auth: 302 → /oauth2/authorization/github

    Auth->>GH: 302 → GitHub 授权页面
    GH-->>User: GitHub 授权页
    User->>GH: 同意授权
    GH->>Auth: 302 → /login/oauth2/code/github?code=AUTH_CODE

    Auth->>GH: 换取 GitHub access_token
    GH-->>Auth: token
    Auth->>GH: GET /api/github/user
    GH-->>Auth: GitHub 用户信息

    Auth->>Auth: FederatedIdentityOAuth2UserService.loadUser()
    Note over Auth: session 中有 bind_user_id → 绑定模式

    Auth->>Basic: Feign POST /internal/bind-idp (userId, provider, externalId, ...)
    Note over Basic: 检查外部账号是否已被其他用户绑定<br/>检查当前用户是否已绑定同一 provider<br/>保存 UserIdentityProvider 记录
    Basic-->>Auth: 绑定成功

    Auth->>Auth: 302 → /bind/success
    Auth-->>SPA: 渲染 bind-success.html → postMessage('idp-bind-success') → 关闭弹窗
    SPA->>SPA: 监听 postMessage，刷新绑定列表
```

---

## 前端实现

### PKCE 发起

**文件**: `upda-cloud-client/src/store/CoreStore.js` `initiateOAuth2Login()`

**文件**: `upda-cloud-client/src/util/oauth2.js`

```javascript
// oauth2.js 关键函数
generateCodeVerifier()   // 64 字符随机字符串，Base64URL 编码
generateCodeChallenge()  // SHA-256(verifyer) → Base64URL，S256 方法
buildAuthorizeUrl()      // ${authServerUrl}/oauth2/authorize?response_type=code&client_id=uocs-client&code_challenge_method=S256&...
exchangeCodeForTokens()  // POST /oauth2/token (code + code_verifier)
refreshAccessToken()     // POST /oauth2/token (grant_type=refresh_token)
isTokenExpiringSoon()    // JWT 解码检查，提前 120 秒判定过期
```

PKCE 临时数据（code_verifier、state）存储在 `sessionStorage`，回调后清除。

### 登录页自动跳转

**文件**: `upda-cloud-client/src/view/Login/Login.jsx`

```javascript
const oauth2Enabled = configStore?.appConfig?.oauth2Enabled === true;
useEffect(() => {
    if (oauth2Enabled && !oauth2Error && configStore?.appConfig) {
        coreStore.initiateOAuth2Login(configStore.appConfig);
    }
}, [oauth2Enabled, oauth2Error, configStore?.appConfig, coreStore]);
```

当 `oauth2Enabled=true` 时，Login 页面**不显示用户名/密码表单**，直接发起 OAuth2 跳转。三种状态：自动跳转中（spinner）、错误回退（重试按钮）、旧模式（表单）。

### OAuth2 回调处理

**文件**: `upda-cloud-client/src/view/OAuth2Callback/OAuth2Callback.jsx`

**路由**: `/oauth2/callback`（`App.jsx` 第 37 行注册）

流程：提取 URL 参数 → 验证 state（与 sessionStorage 比对） → 取出 code_verifier → `exchangeCodeForTokens()` → `coreStore.handleOAuth2Callback(tokens)` → 跳转原始页面（`oauth2_redirect_to`，仅允许相对路径防开放重定向）。

### Token 管理

**文件**: `upda-cloud-client/src/store/CoreStore.js`

- Token 存储在 `sessionStorage`（关闭标签页即清除）
- `refreshTokenIfNeeded()` — token 即将过期时自动刷新
- `logout()` — OAuth2 模式下跳转 Auth Server 的 `/sso-logout` 销毁 session

### 路由守卫

**文件**: `upda-cloud-client/src/component/PrivateRoute.jsx`

OAuth2 模式下，未登录用户不跳前端 `/login`，直接通过 `coreStore.initiateOAuth2Login()` 跳转 Auth Server。

---

## 后端实现

### ClientRegistration 构建

**文件**: `auth/src/main/java/com/upda/auth/config/OAuth2ClientConfig.java`

手动构建 `ClientRegistrationRepository`（不使用 Spring Boot 标准前缀，因 Nacos YAML 展平器对 7 层以上嵌套存在属性丢失问题）。

```java
ClientRegistration.builder()
    .registrationId("github")
    .clientId(federationProperties.getGithubClientId())       // Nacos: federation.providers.github.client-id
    .clientSecret(federationProperties.getGithubClientSecret()) // Nacos: federation.providers.github.client-secret
    .authorizationUri("https://github.com/login/oauth/authorize")
    .tokenUri("https://github.com/login/oauth/access_token")
    .userInfoUri("https://api.github.com/user")
    .userNameAttributeName("id")
    .authorizationGrantType(AUTHORIZATION_CODE)
    .scope("read:user", "user:email")
    .redirectUri("{baseUrl}/login/oauth2/code/{registrationId}")
    .build();
```

未配置时使用 `EmptyClientRegistrationRepository` 优雅降级（联合登录按钮不渲染）。

### Security 过滤链

**文件**: `auth/src/main/java/com/upda/auth/config/AuthorizationServerConfig.java` `defaultSecurityFilterChain`（Order 3）

```java
if (hasOAuth2Clients && federatedUserService != null) {
    http.oauth2Login(oauth2 -> oauth2
        .loginPage("/login")
        .userInfoEndpoint(userInfo -> userInfo.userService(federatedUserService))
        .successHandler(...)   // 区分登录/绑定模式
        .failureHandler(...)   // 区分登录/绑定模式失败
    );
}
```

GitHub 登录按钮在 `login.html` 中动态渲染：遍历 `ClientRegistrationRepository`，每个 `registrationId` 生成一个按钮，href 为 `/oauth2/authorization/{registrationId}`（Spring Security 内置端点）。

### FederatedIdentityOAuth2UserService — 核心逻辑

**文件**: `auth/src/main/java/com/upda/auth/service/FederatedIdentityOAuth2UserService.java`

实现了 `OAuth2UserService<OAuth2UserRequest, OAuth2User>` 接口，处理流程：

1. **获取外部用户信息** — 委托 `DefaultOAuth2UserService` 调用 GitHub API
2. **提取外部用户标识** — 按 provider 提取不同字段：
   - GitHub: `id` (externalId), `login` (username), `email`, `avatar_url`
3. **检查模式** — 从 HTTP Session 读取 `bind_user_id`
   - 有值 → 绑定模式
   - 无值 → 登录模式
4. **登录模式** — Feign 查询关联，未找到则 JIT 创建
5. **绑定模式** — Feign 绑定外部账号
6. **返回** `FederatedOAuth2User`（包装外部 OAuth2User + UOCS 业务属性）

### FederatedOAuth2User — 用户信息包装

**文件**: `auth/src/main/java/com/upda/auth/service/FederatedOAuth2User.java`

同时携带外部 IdP 原始属性和 UOCS 业务属性：

| 字段 | 说明 |
|------|------|
| `delegate` | 原始 OAuth2User（GitHub 返回的属性） |
| `uocsUserId` | UOCS 系统用户 ID |
| `uocsUsername` | UOCS 系统用户名 |
| `roles` | UOCS 角色列表 |

`getName()` 返回 UOCS 用户名。

### JWT Claims 注入

**文件**: `auth/src/main/java/com/upda/auth/config/OAuth2TokenCustomizerConfig.java`

签发 JWT access_token 时，根据 principal 类型注入业务 claims：

- `FederatedOAuth2User`（联合登录）→ 直接从对象获取 userId 和 roles
- 普通用户（formLogin）→ 通过 Feign 查询 services-basic

最终 JWT 包含：`userId`、`roles`、标准 OAuth2 claims（`iss`、`sub`、`aud`、`exp` 等）。

### Gateway JWT 验证

**文件**: `gateway/src/main/java/com/upda/gateway/filter/AuthGlobalFilter.java`

双模式 JWT 验证：通过检查 JWT payload 中的 `iss` claim 区分 OAuth2 JWT 和旧版 JWT。OAuth2 JWT 使用 `ReactiveJwtDecoder`（基于 Auth Server JWK Set）验证。

验证成功后提取 `userId`、`roles`、`scope`，注入 `X-User-Id`、`X-User-Roles`、`X-User-Scopes` header 传递给下游服务。

同时拦截 `/**/internal/**` 路径，防止外部直接访问内部接口。

---

## JIT Provisioning — 首次登录自动创建用户

**文件**: `services-basic/.../service/impl/UOCSUserServiceImpl.java` `createFederatedUser()`

首次 GitHub 登录且未关联 UOCS 用户时，自动创建：

1. **防重检查** — 先查询是否已存在关联
2. **生成用户名** — `github_{login}`，冲突时追加数字后缀
3. **生成密码** — 随机 UUID（联合用户不使用密码认证）
4. **创建 User 实体** — nickname=externalUsername, email, avatar
5. **分配默认角色** — USER + SEAL_USER
6. **创建关联记录** — UserIdentityProvider（provider, externalId, externalUsername, externalEmail, externalAvatar）
7. **并发处理** — 捕获 `DuplicateKeyException`，回退查询已创建的记录

### 解绑保护

`unbindIdp()` 方法有安全检查：若用户为 JIT 创建（创建时间与首个 IdP 绑定时间差 ≤10s）且仅剩最后一个绑定，**禁止解绑**，防止用户无法登录。

---

## 配置速查

### Nacos 配置（Auth Server）

```yaml
federation:
  providers:
    github:
      client-id: <GitHub OAuth App Client ID>
      client-secret: <GitHub OAuth App Client Secret>
      scope: read:user,user:email
      redirect-uri: '{baseUrl}/login/oauth2/code/{registrationId}'
```

配置参考文件：`auth/src/main/resources/nacos-config-reference.yml`（第 70-89 行开发环境，第 125-130 行生产环境）

### 前端 config.json

```json
{
  "authServerUrl": "https://auth.example.com",
  "oauth2ClientId": "uocs-client",
  "oauth2Enabled": true
}
```

### GitHub OAuth App 创建

Settings → Developer settings → OAuth Apps → New OAuth App

关键字段：
- **Authorization callback URL**: `{authServerUrl}/login/oauth2/code/github`
- **Scopes**: `read:user`, `user:email`

---

## 数据映射关系

| GitHub 字段 | UOCS User 字段 | UserIdentityProvider 字段 | 提取位置 |
|---|---|---|---|
| `id` | — | `externalId` | `extractExternalId()` |
| `login` | `nickname` | `externalUsername` | `extractExternalUsername()` |
| `email` | `email` | `externalEmail` | `extractExternalEmail()` |
| `avatar_url` | `avatar` | `externalAvatar` | `extractExternalAvatar()` |
| 自动生成 | `username` = `github_{login}` | — | `createFederatedUser()` |
| 随机 UUID | `password` | — | `createFederatedUser()` |
| 自动分配 | `roles` = USER + SEAL_USER | — | `assignDefaultRoles()` |

---

## 关键文件索引

### 前端（upda-cloud-client）

| 文件 | 说明 |
|------|------|
| `src/util/oauth2.js` | PKCE 工具函数（code_verifier/challenge 生成、token 交换） |
| `src/store/CoreStore.js` | 登录状态管理（发起 OAuth2、回调处理、token 刷新、登出） |
| `src/view/Login/Login.jsx` | 登录页（oauth2Enabled 时自动跳转） |
| `src/view/OAuth2Callback/OAuth2Callback.jsx` | OAuth2 回调处理（state 验证、token 交换、跳转） |
| `src/view/Profile/Profile.jsx` | GitHub 绑定/解绑入口 |
| `src/component/PrivateRoute.jsx` | 路由守卫（OAuth2 模式下跳转 Auth Server） |
| `src/App.jsx` | 路由配置（`/oauth2/callback` 路由注册） |
| `src/services/BasicUserService.js` | API 调用（绑定查询、解绑） |

### 后端 — Auth 模块

| 文件 | 说明 |
|------|------|
| `auth/.../config/OAuth2ClientConfig.java` | GitHub ClientRegistration 手动构建 |
| `auth/.../config/AuthorizationServerConfig.java` | Security 过滤链（联合登录启用） |
| `auth/.../config/OAuth2TokenCustomizerConfig.java` | JWT claims 注入（userId, roles） |
| `auth/.../service/FederatedIdentityOAuth2UserService.java` | 联合登录核心逻辑（登录/绑定模式分发） |
| `auth/.../service/FederatedOAuth2User.java` | 用户信息包装（外部属性 + UOCS 属性） |
| `auth/.../controller/LoginController.java` | 登录页控制器（动态渲染 IdP 按钮） |
| `auth/.../controller/BindController.java` | 绑定控制器（session 标记绑定模式） |
| `auth/.../resources/templates/login.html` | 登录页模板（GitHub 按钮渲染） |

### 后端 — Services-Basic 模块

| 文件 | 说明 |
|------|------|
| `services-basic/.../service/impl/UOCSUserServiceImpl.java` | 联合登录业务（查询关联、JIT 创建、绑定/解绑） |
| `services-basic/.../entity/UserIdentityProvider.java` | 身份关联实体（user_identity_provider 表） |
| `services-basic/.../controller/UserController.java` | 前端 API（绑定查询、解绑） |

### 后端 — API 模块

| 文件 | 说明 |
|------|------|
| `api/api-basic/.../client/UserClient.java` | Feign Client（内部 API 调用） |
| `api/api-basic/.../dto/CreateFederatedUserReqDTO.java` | 创建联合用户请求 DTO |
| `api/api-basic/.../dto/AuthUserInfoRespDTO.java` | 认证用户信息响应 DTO |

### 后端 — Gateway 模块

| 文件 | 说明 |
|------|------|
| `gateway/.../filter/AuthGlobalFilter.java` | JWT 验证 + 内部接口拦截 |

### 配置

| 文件 | 说明 |
|------|------|
| `auth/.../resources/nacos-config-reference.yml` | Nacos 配置参考（含 GitHub OAuth 模板） |
| `upda-cloud-client/public/config.json` | 前端配置（authServerUrl, oauth2ClientId, oauth2Enabled） |
