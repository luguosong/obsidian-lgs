# WASM License Gate 设计（DrawingWebApp）

**日期**：2026-04-15
**状态**：设计已确认，待实现
**作者**：@ZFSWin11 与 Claude 协作
**涉及代码库**：`DrawingWeb/`（C++/WASM）、`DrawingWebApp/`（React 前端）、`DrawingWebApp/server/`（后端，当前 Node.js，计划迁移至 **Java**）

---

## 目标与威胁模型

### 目标

防止客户在**没有厂商授权的情况下**使用 `DrawingJs.wasm` + `DrawingJs.data` + `DrawingJs.js`。即：

- 客户拿到完整的 `dist/` + `server/` 部署包后，仍然必须启动厂商配发的 License + 后端服务，前端才能**打开/新建** DWG 图纸
- 实行**私有化部署 + 离线授权码**模式（每客户一份 License 文件）
- 绑定到**服务器机器硬件 + 最大并发浏览器数**
- 已打开的图纸在 Token 过期或 server 掉线后**仍能继续编辑**，但**新建/再次打开**必须有效授权

### 威胁等级（Level 3）

承认的对手能力：
- 会拆 `server/` 静态资源、改前端 JS、抓网络包
- 会尝试把 `dist/` 搬到另一台机器、另一个容器

接受的极限（诚实披露）：
- 专业逆向工程师若愿意 hex-edit `.wasm` / 补丁 `verify()` 函数总能绕过。我们的目标是**阻止普通逆向者与技术型客户**，不是阻止国家级对手

### 关键设计决策一览

| 维度 | 选择 |
|---|---|
| 部署模型 | 客户私有化部署 + 离线 License 文件 |
| 威胁等级 | Level 3（允许修改 WASM C++ 源码） |
| 离线容忍 | 允许已打开图纸持续编辑；`OpenFile`/`CreateNewFile` 时强制在线校验 |
| 绑定粒度 | 服务器机器硬件指纹 + 最大并发浏览器数 |
| 加密算法 | **SM2 + SM3 + GMT0009**（国密合规） |
| 信任链 | **双层非对称**：厂商根密钥签 License；客户密钥签 Token |
| 校验插桩点 | `CadCore::OpenFile` 与 `CadCore::CreateNewFile`（[CadCore.cpp:571/587](../../DrawingWeb/CadCore.cpp)） |
| Token 刷新 | JS 每 3 分钟心跳；Token 过期时间 5 分钟 |
| 失败行为 | 失败时 WASM 拒绝打开图纸 + JS 前端弹窗；不 crash |
| 后端语言 | **Java（目标实现）**，Node.js 是过渡形态 |
| 部署形式 | **Docker**，需绑定宿主机硬件信息 |

---

## 架构总览

```
┌─────────────────────── 厂商侧 (离线机器) ─────────────────────┐
│                                                               │
│   Kroot_priv (SM2)  ←── 永不联网, 存在加密 U 盘              │
│         │                                                      │
│         │ sign(License payload)                                │
│         ▼                                                      │
│   license.dat  +  customer_key.pem  (发给客户)                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ 物理交付
                              ▼
┌─────────────────────── 客户侧 (部署环境) ──────────────────────┐
│                                                                 │
│   ┌───────── Docker Host ─────────┐                            │
│   │  /etc/machine-id              │ ──bind mount─┐             │
│   │  /sys/class/dmi/id/...        │              │             │
│   │  physical NIC MACs            │              │             │
│   └───────────────────────────────┘              ▼             │
│                                      ┌───────────────────────┐  │
│                                      │  license-server (Java)│  │
│                                      │  + license.dat        │  │
│                                      │  + customer_key.pem   │  │
│                                      │  + root_pubkey.pem    │  │
│                                      │                       │  │
│                                      │  启动自检 → 运行中签 Token│  │
│                                      │  会话表 (ConcurrentMap │  │
│                                      │           或 Redis)    │  │
│                                      └──────────┬────────────┘  │
│                                                 │               │
│                                                 │ HTTP          │
│                                                 ▼               │
│                                   ┌─────────────────────────┐   │
│                                   │  Browser (React + WASM) │   │
│                                   │                         │   │
│                                   │  useWasmModule postRun: │   │
│                                   │   1. fetch /license/info│   │
│                                   │   2. initLicenseGate    │   │
│                                   │   3. session/start      │   │
│                                   │   4. 3min heartbeat     │   │
│                                   │                         │   │
│                                   │  CadCore::OpenFile:     │   │
│                                   │    verifyCurrentToken() │   │
│                                   │    (SM2 验签 + 过期)     │   │
│                                   └─────────────────────────┘   │
│                                                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## 三对密钥

### 根密钥对 `(Kroot_priv, Kroot_pub)`

- **算法**：SM2（EC over sm2p256v1 曲线）
- **`Kroot_priv`**：由厂商**离线保管**，永不联网。推荐加密 U 盘 + 纸质备份
- **`Kroot_pub`**：**硬编码进 `DrawingJs.wasm`**。编译时通过 `DrawingWeb/root_pubkey.inc`（自动生成的头文件）注入 `.rodata` 段
- **轮换策略**：正常情况 2–3 年一次；泄露时必须立即生成新根密钥对 + 全量重发布 WASM + 重签所有客户 License

### 客户密钥对 `(Kcust_priv_i, Kcust_pub_i)`（每客户一对）

- **算法**：SM2
- **`Kcust_priv_i`**：客户 `server/license/customer_key.pem`，运行时仅加载到内存。文件权限 `0600`。不随代码库提交
- **`Kcust_pub_i`**：作为 License payload 的一个字段，**由根私钥背书**
- **轮换策略**：客户续费 / 合同变更时重新签发 License，新生成一对客户密钥

### 硬件指纹（不是密钥，但作为 License 绑定维度）

- **组成**：`SM3(machine-id ∥ ',' ∥ sorted-MACs ∥ '|' ∥ motherboard-uuid)`
- **长度**：64 字符 hex（SM3 输出 32 字节）
- **由客户在安装前运行 `print-fingerprint` 工具得到**，寄给厂商；厂商把它写入 License payload 并签名

---

## License 文件格式

### JSON 结构

```json
{
  "payload": {
    "license_id":         "LIC-20260415-A1B2C3",
    "customer_name":      "ACME CAD Co.",
    "customer_pubkey":    "04<hex, 130 chars, 65-byte SM2 uncompressed public key>",
    "server_fingerprint": "<64-char SM3 hex>",
    "max_concurrent":     10,
    "issued_at":          "2026-04-15T00:00:00Z",
    "expires_at":         "2027-04-15T00:00:00Z",
    "version":            1
  },
  "signature": "<base64 of 64-byte SM2 R||S signature>"
}
```

### Canonical JSON

签名覆盖的是**字节序列**，而非 JSON 对象。因此签发端与验签端必须使用**确定性序列化**：

- 键按 **Unicode code point 升序**排序
- 不含任何空白字符（无 indent、无空格）
- UTF-8 编码，不加 BOM
- 字符串使用最短 `\uXXXX` 转义（参考 RFC 8785 JCS 子集）

JavaScript 参考实现：

```js
function canonicalJson(obj) {
  if (obj === null || typeof obj !== 'object') return JSON.stringify(obj)
  if (Array.isArray(obj)) return '[' + obj.map(canonicalJson).join(',') + ']'
  const keys = Object.keys(obj).sort()
  return '{' + keys.map(k => JSON.stringify(k) + ':' + canonicalJson(obj[k])).join(',') + '}'
}
```

Java 参考实现：`com.fasterxml.jackson.databind.ObjectMapper` 配合 `JsonInclude.Include.NON_NULL` + 自定义 `TreeMap` 键排序；或使用 [jcs-java](https://github.com/cyberphone/json-canonicalization) 等库。

### 签名算法细节

- **算法**：SM2（GMT 0003-2012）
- **摘要**：先按 GMT 0009-2012 计算 SM2 专用摘要 `e = SM3(Z ∥ canonicalPayloadUtf8)`，其中 `Z = SM3(ENTLA ∥ userId ∥ a ∥ b ∥ Gx ∥ Gy ∥ Ax ∥ Ay)`，`userId = "1234567812345678"`（默认 16 字节 ASCII）
- **签名格式**：64 字节 **R‖S**（非 DER）。R 和 S 各 32 字节大端
- **签名字段编码**：`base64(R‖S)` → 放入 JSON 的 `"signature"` 字段

### 签发流程（厂商侧，离线）

```
1. 客户初次部署, 在目标宿主机运行:
     print-fingerprint → 得到 64-char SM3 hex
   客户发给厂商: license_id + fingerprint + 合同 (并发数, 有效期)

2. 厂商在离线机器运行:
     sign-license \
       --root-key kroot_private.pem \
       --customer "ACME CAD Co." \
       --fingerprint <hex> \
       --max-concurrent 10 \
       --expires 2027-04-15
   输出: license.dat, customer_key.pem

3. 厂商通过安全渠道 (加密邮件/USB) 送达客户
   客户放到:
     server/license/license.dat        (可读)
     server/license/customer_key.pem   (0600)
     server/license/root_pubkey.pem    (已随 server 代码分发, 公开不敏感)
```

### 吊销策略

不引入在线 CRL。简化策略：

- 正常到期：依赖 `expires_at`
- 紧急吊销：下一版 WASM 烧录 `license_id` 黑名单（常量数组），通过强制升级实现
- 客户私钥泄露：该 `license_id` 进入黑名单，给客户签发新 License

---

## Token 协议

### Token 格式

```
Token 字符串 = base64url(payload_utf8) + "." + base64url(signature_R‖S)
```

**base64url 编码规则**：RFC 4648 §5，字符集 `A-Za-z0-9_-`，**无填充**（`=`）。WASM 侧解码器必须能处理"无填充"输入。

`payload`（紧凑 JSON）：

```json
{
  "license_id":     "LIC-20260415-A1B2C3",
  "session_id":     "sess_<uuid-v4>",
  "issued_at":      1744704000,
  "expires_at":     1744704300,
  "max_concurrent": 10,
  "nonce":          "<16-byte hex random>"
}
```

- `issued_at`、`expires_at`：Unix 秒
- `expires_at = issued_at + 300`（固定 5 分钟）
- `nonce`：16 字节随机，防 Token 做 key 缓存复用
- Token 总长度约 450–500 字节

### 签名

由 server 用 `customer_key.pem` 做 SM2 签名：

```
sig = SM2_Sign(
  digest = SM3_GMT09(canonicalJson(payload)),
  privateKey = customerPrivKey
)  // 输出 64 字节 R‖S
```

### 生命周期

```
t=0      Client    POST /api/license/session/start
         Server    → 分配 sessionId, 初次签 Token(exp=300s), 返回
         JS        保存到 window.__currentLicenseToken
         JS        启动 setInterval(180_000)

t=180    JS        POST /api/license/token/refresh { sessionId }
         Server    → 验 sessionId 存在, 更新 lastSeen, 重签 Token(exp=180+300)
         JS        更新 window.__currentLicenseToken

t=360    JS        继续心跳 ...

t=?      WASM      CadCore::OpenFile
         WASM      EM_ASM 读 window.__currentLicenseToken
         WASM      SM2 验签 + 检查 expires_at > now + 检查 license_id
         WASM      通过 → 执行原逻辑; 不通过 → return + 通知 JS

页面关闭  JS        navigator.sendBeacon /api/license/session/end
         Server    → 立即删除 sessionId, 释放并发名额

Server 被动清理:
         每 60 秒扫一次 sessions 表,
         lastSeen 超过 5 分钟的 session 强制删除
```

### HTTP Endpoints

#### `GET /api/license/info`

返回 `license.dat` 原文。WASM 启动时用硬编码根公钥再验一次签。

**响应**：`200 text/plain` 或 `application/json`，body 为 `license.dat` 全文。

#### `POST /api/license/session/start`

建立新会话，立即签发第一个 Token。

- **请求**：空 body
- **响应 200**：`{ "sessionId": "sess_...", "token": "base64.base64", "active": 3 }`
- **响应 429**：`{ "error": "MAX_CONCURRENT_REACHED", "active": 10, "max": 10 }`

#### `POST /api/license/token/refresh`

心跳 + 续签。

- **请求**：`application/json` `{ "sessionId": "sess_..." }`
- **响应 200**：`{ "token": "base64.base64" }`
- **响应 401**：`{ "error": "SESSION_NOT_FOUND" }`（session 被清理或从未建立）

#### `POST /api/license/session/end`

会话结束（用 `navigator.sendBeacon`）。

- **请求**：`text/plain` body 为 JSON `{ "sessionId": "sess_..." }`
- **响应 200**：`{ "ok": true }`
- 实现必须接受 `Content-Type: text/plain`（sendBeacon 默认），尝试 JSON.parse

---

## Server 实现规范（语言中立）

本节描述服务端必须满足的行为，**不绑定 Node.js 或 Java**。下文的"参考实现"块分别给出 Node.js（过渡）和 Java（目标）的具体库选型。

### 启动自检

顺序执行以下步骤，任何一步失败**必须以非 0 退出码终止进程**，并向 stderr 输出具体失败原因。

1. **读取根公钥**  
   路径：`${ROOT_PUBKEY_PATH}`（默认 `./license/root_pubkey.pem`）

2. **读取 License 文件**  
   路径：`${LICENSE_PATH}`（默认 `./license/license.dat`）

3. **验证 License 签名**  
   `SM2_Verify(payload, signature, rootPubKey)`；失败消息：  
   `License signature invalid: not signed by vendor root key`

4. **计算本机硬件指纹并比较**  
   失败消息：`License bound to different machine. Expected <abc...>, got <xyz...>`

5. **检查 License 有效期**  
   `now < payload.expires_at`；失败消息：`License expired at <iso8601>`

6. **读取客户私钥**  
   路径：`${CUSTOMER_KEY_PATH}`（默认 `./license/customer_key.pem`）  
   加载到内存，之后不再访问磁盘

7. **启动会话清理定时器**  
   每 60 秒一次，剔除 `now - lastSeen > 5min` 的 session

8. **启动 HTTP Server**  
   日志输出成功信息：
   ```
   [License] OK. license_id=LIC-... customer=ACME CAD Co.
                max_concurrent=10 expires_at=2027-04-15
   ```

### 硬件指纹计算

```
fingerprint_input = <machine-id> + "|" + <sorted-lowercase-MACs-csv> + "|" + <motherboard-uuid>
fingerprint_hex   = hex(SM3(fingerprint_input.utf8))
```

三个输入组件：

| 组件 | Linux | Windows |
|---|---|---|
| `machine-id` | `/etc/machine-id` | `HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid` |
| `MACs` | `ip link` 物理接口，排除 `lo`、`docker*`、`veth*`、`br-*` 等虚拟接口 | `Get-NetAdapter` 物理接口 |
| `motherboard-uuid` | `/sys/class/dmi/id/product_uuid`（需 root 读）| `wmic csproduct get uuid` |

**MAC 过滤规则**：保留 `!internal && mac != 00:00:00:00:00:00 && !(name matches /^(docker|veth|br-|virbr|tun|tap)/)`。小写化后按字符串排序，以英文逗号连接。

**参考实现**：

- **Node.js**：`node-machine-id`（machine-id）+ `os.networkInterfaces()`（MAC）+ `child_process.execSync('wmic ...' | 'cat /sys/.../product_uuid')`（UUID）
- **Java**：
  - `machine-id`：读 `/etc/machine-id` 或注册表（JNA / `System.getProperty("os.name")` 分支）
  - `MAC`：`java.net.NetworkInterface.getNetworkInterfaces()` + 手工过滤
  - `product_uuid`：`Files.readString(Path.of("/sys/class/dmi/id/product_uuid"))` 或 `Runtime.exec("wmic csproduct get uuid")`
  - 或直接用 **[OSHI](https://github.com/oshi/oshi)**：`new SystemInfo().getHardware().getComputerSystem().getHardwareUUID()` + `getNetworkIFs()`。推荐 OSHI

### 会话管理

**数据结构**：

```
sessions: Map<sessionId: UUID, Session>
Session = { startedAt: epochMs, lastSeen: epochMs }
```

**实现选型**：

- **单实例 server**：内存 `Map` / `ConcurrentHashMap<String, Session>`。`beforeunload` 通过 `sendBeacon` 立即释放
- **多实例 server（水平扩展）**：Redis String 或 Hash，带 TTL = 300 秒。每次 `refresh` 刷 TTL。session 计数用 Redis `SCARD` 或 `DBSIZE`（按前缀）
- **推荐**：默认单实例 `ConcurrentHashMap`，通过配置切换 Redis

### Token 签发

```
payload = {
  license_id, session_id, issued_at, expires_at, max_concurrent, nonce
}
payloadStr = canonicalJson(payload)
payloadB64 = base64url(payloadStr.utf8)
digest     = SM2_GMT09_Digest(payloadStr, customerPubKey)   // 需要公钥算 Z 值
sig        = SM2_Sign(digest, customerPrivKey)              // 64-byte R‖S
sigB64     = base64url(sig)
token      = payloadB64 + "." + sigB64
```

**参考实现**：

- **Node.js**：[`sm-crypto`](https://www.npmjs.com/package/sm-crypto)
  ```js
  const sm2 = require('sm-crypto').sm2
  // hash=true 内部自动做 SM3+GMT0009 Z 值; der=false 输出 R||S
  const sigHex = sm2.doSignature(payloadStr, customerPrivKeyHex, { hash: true, der: false })
  ```

- **Java**：**Bouncy Castle** (`org.bouncycastle:bcprov-jdk18on:1.78+`)
  ```java
  Security.addProvider(new BouncyCastleProvider());
  SM2Signer signer = new SM2Signer();
  ECPrivateKeyParameters priv = /* 从 customer_key.pem 加载 */;
  signer.init(true, new ParametersWithID(
      priv,
      "1234567812345678".getBytes(StandardCharsets.US_ASCII)));
  signer.update(payloadBytes, 0, payloadBytes.length);
  byte[] derSig = signer.generateSignature();
  byte[] rs = derToRawRS(derSig);  // 自己写转换, 或用 BC 内部 util
  ```

### 并发管制

- 每次 `POST /session/start`，先比较 `sessions.size() < license.max_concurrent`
- 超限返回 `429 { "error": "MAX_CONCURRENT_REACHED", active, max }`

### 环境变量与配置

| 变量 | 默认值 | 含义 |
|---|---|---|
| `LICENSE_PATH` | `./license/license.dat` | License 文件路径 |
| `CUSTOMER_KEY_PATH` | `./license/customer_key.pem` | 客户私钥路径 |
| `ROOT_PUBKEY_PATH` | `./license/root_pubkey.pem` | 根公钥路径 |
| `SESSION_STORE` | `memory` | `memory` 或 `redis://host:port` |
| `TOKEN_TTL_SEC` | `300` | Token 过期时间（秒） |
| `SESSION_TTL_SEC` | `300` | Session lastSeen 宽限期（秒） |
| `PORT` | `3001` | HTTP 端口 |

---

## WASM / C++ 实现规范

### 新增文件

```
DrawingWeb/
├── LicenseGate.h               (新增)
├── LicenseGate.cpp             (新增)
├── root_pubkey.inc             (新增, 自动生成)
└── tools/                      (厂商一次性使用)
    ├── generate-root-key.js
    └── embed-root-pubkey.js
```

### `LicenseGate` 类接口

```cpp
#pragma once
#include <uacore/pkcs/uacore_evp_pkey.h>
#include <string>

class LicenseGate {
public:
    static LicenseGate& instance();

    // WASM 启动时由 JS 调用, 传入从 /api/license/info 拉取的 License JSON
    // 返回 false 时, 整个 Viewer 不应启动, lastError() 描述原因
    bool initFromLicenseJson(const std::string& licenseJson);

    // 每次 OpenFile / CreateNewFile 前调用
    // 内部: EM_ASM 读 window.__currentLicenseToken → SM2 验签 → 过期/id 检查
    bool verifyCurrentToken();

    bool isInitialized() const { return m_initialized; }
    const std::string& lastError() const { return m_lastError; }
    const std::string& licenseId() const { return m_licenseId; }

private:
    LicenseGate() = default;
    UcEvpPKey m_rootPubKey;
    UcEvpPKey m_customerPubKey;
    std::string m_licenseId;
    std::string m_lastError;
    bool m_initialized = false;
};
```

### 根公钥注入

构建流程：

```
1. 厂商一次性生成:
     node tools/generate-root-key.js
     → 输出 root_private.pem, root_public.pem

2. 构建 WASM 前:
     node tools/embed-root-pubkey.js root_public.pem > DrawingWeb/root_pubkey.inc
     生成:
       // AUTO-GENERATED
       static constexpr const char kRootPubKeyHex[] =
           "04<130-char hex>";

3. LicenseGate.cpp 包含 #include "root_pubkey.inc"
```

根私钥**绝不**提交到代码库。推荐将 `root_pubkey.inc` 提交（公钥公开无害），`root_private.pem` 单独加密保管。

### CadCore 插桩

仅改两处，参见 [CadCore.cpp:571](../../DrawingWeb/CadCore.cpp) 与 [:587](../../DrawingWeb/CadCore.cpp)：

```cpp
void CadCore::OpenFile(std::wstring name)
{
    // ===== License Gate =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        std::string err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('OpenFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] OpenFile denied: %s\n", err.c_str());
        return;
    }
    // ========================

    releaseDeviceAndContext();
    // ... 原逻辑不变 ...
}

void CadCore::CreateNewFile()
{
    // ===== License Gate =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        std::string err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('CreateNewFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] CreateNewFile denied: %s\n", err.c_str());
        return;
    }
    // ========================

    releaseDeviceAndContext();
    // ... 原逻辑不变 ...
}
```

### JS 侧 embind 暴露

```cpp
// CadCoreWebBridge.cpp (或新增 LicenseGateBindings.cpp)
#include <emscripten/bind.h>
#include "LicenseGate.h"
using namespace emscripten;

EMSCRIPTEN_BINDINGS(license_gate) {
    function("initLicenseGate", +[](std::string json) {
        return LicenseGate::instance().initFromLicenseJson(json);
    });
    function("isLicenseReady", +[]() {
        return LicenseGate::instance().isInitialized();
    });
}
```

---

## 前端 JS 实现规范

### `useWasmModule` postRun 钩子

在创建 `Viewer` 之前**必须**完成 License 初始化与心跳启动。改动集中在 [useWasmModule.js:169-503](../../src/hooks/useWasmModule.js)。

```js
Module.postRun.push(async function () {
    // 0. 先完成目录/补丁/FS shim 等原有逻辑

    // 1. 拉取 License JSON
    let licenseJson
    try {
        const resp = await fetch('/api/license/info')
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        licenseJson = await resp.text()
    } catch (e) {
        showLicenseError('无法连接授权服务器', e.message)
        return  // 不初始化 Viewer
    }

    // 2. WASM 内验 License 签名 + 装载客户公钥
    if (!Module.initLicenseGate(licenseJson)) {
        showLicenseError('License 校验失败', 'WASM 拒绝此 License')
        return
    }

    // 3. 建立会话
    try {
        const resp = await fetch('/api/license/session/start', { method: 'POST' })
        if (resp.status === 429) {
            const err = await resp.json()
            showLicenseError('授权名额已满', `${err.active}/${err.max}`)
            return
        }
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
        const { sessionId, token } = await resp.json()
        window.__licenseSessionId = sessionId
        window.__currentLicenseToken = token
    } catch (e) {
        showLicenseError('无法建立授权会话', e.message)
        return
    }

    // 4. 启动心跳 (3 分钟)
    setInterval(async () => {
        try {
            const resp = await fetch('/api/license/token/refresh', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sessionId: window.__licenseSessionId }),
            })
            if (!resp.ok) return  // 保留旧 Token, 5 分钟后自动过期
            const { token } = await resp.json()
            window.__currentLicenseToken = token
        } catch (_) { /* 网络暂抖动, 下次再试 */ }
    }, 180 * 1000)

    // 5. 页面关闭立即通知 (释放并发名额)
    window.addEventListener('beforeunload', () => {
        navigator.sendBeacon('/api/license/session/end',
            JSON.stringify({ sessionId: window.__licenseSessionId }))
    })

    // 6. WASM 拒绝时的 UI 回调
    window.__onLicenseDenied = (op, reason) => {
        showActionDenied(op, reason)
    }

    // 7. 继续原有 Viewer 创建流程
    const ViewerClass = createViewerClass(Module)
    // ...
})
```

### UI 组件要求

- `showLicenseError(title, detail)`：全屏模态，禁止关闭，展示联系方式
- `showActionDenied(op, reason)`：Toast / Modal，允许关闭，用户可继续使用已打开图纸
- `MobX` 侧建议新增 `licenseStore`：`{ status: 'ok' | 'denied' | 'max-reached', active, max, expiresAt }`，TopBar 徽章展示剩余天数

### `fetch` 超时与重试

- 所有 license endpoints 超时 10 秒
- `session/start` 与 `/info` 失败**不自动重试**（由用户手动刷新页面）
- `token/refresh` 失败**静默**（下一次心跳自然重试）

---

## Docker 部署

### 关键约束：硬件指纹必须基于宿主机

容器内的 `/etc/machine-id`、虚拟 MAC、`/sys/class/dmi` 都**不是宿主机的**。三条解决策略：

| 策略 | 优点 | 缺点 |
|---|---|---|
| **① Bind mount 宿主机信息 + `network_mode: host`** | 指纹真实反映宿主 | 端口冲突风险（必须 host network） |
| ② Bind mount 宿主机信息 + bridge 网络 + 主机 MAC 映射 | 保留网络隔离 | 需要额外机制暴露 host MAC |
| ③ 让客户在宿主机跑工具、把结果写入文件挂进容器 | 简单 | **不安全**：客户可复制文件到另一台宿主 |

**推荐策略 ①**（host network + bind mount）。策略 ③ 明确禁止。

### docker-compose 示例

```yaml
version: '3.8'
services:
  drawingwebapp:
    image: drawingwebapp-server:1.0
    restart: unless-stopped
    network_mode: host  # 必须, 为了硬件指纹 MAC 真实
    volumes:
      # —— 硬件指纹三件套(只读) ——
      - /etc/machine-id:/etc/machine-id:ro
      - /sys/class/dmi/id/product_uuid:/host/product_uuid:ro
      # —— License 文件(只读) ——
      - ./license:/app/license:ro
    environment:
      LICENSE_PATH:      /app/license/license.dat
      CUSTOMER_KEY_PATH: /app/license/customer_key.pem
      ROOT_PUBKEY_PATH:  /app/license/root_pubkey.pem
      PORT:              '3001'
      # 如果用 Redis 集群做多实例:
      # SESSION_STORE:  redis://redis:6379/0
```

### Java 实现需要特殊处理的点

Java 读 `/sys/class/dmi/id/product_uuid` 常因权限失败（需要 root 或 setcap）。两种应对：

- **方案 A**：容器以 root 启动（生产环境可接受，镜像中 UID 0）
- **方案 B**：宿主侧在启动容器前把 `product_uuid` 的内容写入一个 `product_uuid.txt` 文件，以 0644 权限挂进容器。但这**降低了安全性**（文件可被修改），不推荐

对于 Windows 宿主（`wmic csproduct get uuid`），Docker 部署本来就复杂，建议 Windows 场景使用**裸机部署 Java JAR**而非容器。

### 镜像大小与启动

- Java Server 基础镜像：`eclipse-temurin:17-jre-alpine` 约 180 MB，加上 Bouncy Castle + OSHI + 业务代码后约 220 MB
- 启动期望：≤ 3 秒完成 License 自检 + HTTP listen

---

## 安全分析

### 攻击面与防御

| 攻击路径 | 防御 | 绕过成本 |
|---|---|---|
| 抓网络包 Token，离线用 | Token 5 分钟过期 | 低成本只能复用 5 分钟 |
| 改 JS 代码返回伪 Token | WASM 用客户公钥验签，签名对不上 | 需伪造 SM2 签名（计算上不可行） |
| 删掉 JS 心跳 | 缓存 Token 5 分钟后过期，再 OpenFile 被拒 | 无法绕过 |
| 复制 `server/` 到另一台机器 | License 绑定硬件指纹，启动自检失败 | 低 |
| 猜测硬件指纹 | SM3 256-bit，穷举不可行 | 极高 |
| 改 WASM 代码让 `verifyCurrentToken` 返回 true | 确实可行（需 hex-edit + 重打包 `.wasm`） | **中等**（此为 Level 3 已知限制） |
| 替换 License 里的 `customer_pubkey` | License payload 被根签名覆盖，验签失败 | 无法绕过 |
| 偷客户私钥 `customer_key.pem` | 该客户 License 进黑名单，重发 | 限制影响范围 |
| 偷根私钥 `kroot_private.pem` | **系统性灾难**，必须全量重发布 WASM + 轮换 | 厂商运维责任 |

### 已知限制

1. **WASM 补丁攻击**：专业对手用 wabt / wasm-tools 编辑 `.wasm` 二进制，将 `verifyCurrentToken` 改为始终 `return true`，然后搭个 nginx 托管。缓解措施：emscripten 的 `--closure 1`、`-O3`、strip debug symbols，且在多处交叉校验（不仅 OpenFile，未来可在核心几何计算前再校验一次）
2. **并发计数不够精确**：`beforeunload` sendBeacon 是 best-effort，浏览器崩溃时名额不会即时释放，需等 5 分钟清理。若要精确，需要 WebSocket 心跳替代 `setInterval`（设计复杂度显著提高，暂不采纳）
3. **时钟攻击**：WASM 用 `emscripten_date_now()` 取时间，若宿主机时间被调回，Token 可能被"复活"。缓解：服务器签 Token 时把 `issued_at` 写入，客户端记录"已见到的最大 issued_at"，若当前时间小于该值则拒绝（防时钟回滚）。未在 MVP 实现，列为 P2

### 变更与轮换

| 事件 | 处理方式 |
|---|---|
| 客户续费 | 离线运行 `sign-license` 生成新 `license.dat` + `customer_key.pem`，客户替换并重启 server |
| 客户增并发 | 同上 |
| 客户更换硬件（升级主板 / 换网卡） | 客户重新运行 `print-fingerprint`，厂商重签 License |
| 客户私钥泄露 | 作废原 License，生成新 License + 新客户密钥 |
| 根私钥泄露 | 1. 生成新根密钥对  2. 发布新 WASM（含新 `root_pubkey.inc`）  3. 重签所有在用客户的 License  4. 通知所有客户同步升级 |

---

## 运维与厂商工具

### 工具清单（放在仓库外或离线机）

```
tools/
├── generate-root-key.js      # 一次性: 创建厂商根密钥对
├── embed-root-pubkey.js      # 构建 WASM 前: 生成 root_pubkey.inc
├── sign-license.js           # 每客户一次: 为客户签 license.dat + customer_key.pem
├── print-fingerprint.js/sh   # 客户侧: 打印硬件指纹
└── verify-license.js         # 任选: 校验一个 license.dat 是否有效(调试用)
```

`generate-root-key.js` 和 `sign-license.js` **只运行在离线机**，`root_private.pem` 永不离开该机。

### 标准操作流程

**A. 初次构建 WASM**
1. 在离线机 `node generate-root-key.js` → `root_private.pem` + `root_public.pem`
2. `node embed-root-pubkey.js root_public.pem > DrawingWeb/root_pubkey.inc`
3. 提交 `root_pubkey.inc`（公钥可公开）
4. 编译 `DrawingJs.wasm`，发布到 `DrawingWebApp/public/`

**B. 签发一个客户 License**
1. 客户运行 `print-fingerprint`，把 64 字符 hex 发给厂商
2. 厂商在离线机运行 `sign-license --fingerprint <hex> --max-concurrent 10 --expires 2027-04-15 --customer "ACME"` → 生成 `license.dat` + `customer_key.pem`
3. 通过加密邮件 / GPG 发送给客户
4. 客户放入 `server/license/` 启动

**C. 客户续费**
1. 客户提供当前 `license_id` + 新过期时间 + 是否更换硬件
2. 厂商运行 `sign-license` 生成新文件
3. 客户热替换 `license.dat` + `customer_key.pem`，重启 Docker 容器

### 日志要求

Server 启动：
```
[License] Loading license.dat ... OK
[License] Verifying root signature ... OK
[License] Computing hardware fingerprint ... 5d9f4a...a3b1
[License] Comparing with expected 5d9f4a...a3b1 ... OK
[License] Loading customer_key.pem ... OK
[License] license_id=LIC-20260415-A1B2C3 customer="ACME CAD Co."
          max_concurrent=10 expires=2027-04-15 (365 days left)
[License] Session cleanup timer started (60s interval)
```

Session 事件（INFO 级别）：
```
[License] session/start sess_abc → 3/10 active
[License] session/end   sess_abc → 2/10 active
[License] session evicted sess_xyz (lastSeen 6m ago)
[License] session/start DENIED (10/10 full)
```

---

## 开放问题 / 未决

- Token `nonce` 是否要加入 server 侧去重（防长重放）？当前设计只靠过期时间，中等强度已够，若需要可后续加
- 是否为"Viewer 只读模式"（仅查看已打开图纸，不允许 OpenFile/CreateNewFile）提供降级路径？当前设计是"已打开的可继续编辑"，未显式切"只读"。UI 层可根据 `licenseStore.status` 自行收敛
- 多租户场景（一个 server 服务多个 License）是否需要？当前设计假设一个 server → 一个 License。若需要，需要显著扩展

---

## 术语表

- **根密钥对（Kroot）**：厂商全局密钥对，离线保管
- **客户密钥对（Kcust_i）**：每个客户独立的密钥对，私钥放在客户 server 上
- **License 文件**：JSON 结构，含绑定信息，由根私钥签名
- **Token**：5 分钟短期令牌，由客户私钥签名，WASM 在关键操作时校验
- **硬件指纹**：`SM3(machine-id|MACs|mb-uuid)` 的 64-char hex
- **GMT 0009**：国密 SM2 数字签名 Z 值计算标准，默认 userId = "1234567812345678"
