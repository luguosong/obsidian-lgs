# DrawingWeb (WASM) License Gate C++ 修改报告

> **面向对象**：`drawing-cad/drawingweb` 仓库维护者
> **来源**：`drawing-web-app/docs/superpowers/specs/2026-04-15-wasm-license-gate-design.md`
> **目的**：在 WASM 侧（`DrawingJs.wasm`）内插入 [[License Gate]]，使"打开/新建图纸"操作必须通过签名 Token 校验，配合后端 `drawing-ai-server` 的 `/api/license/*` 接口达成反盗用能力
> **预期产出**：`drawing-cad/drawingweb/` 仓根目录下新增 3 个文件 + 修改 2 处 + `CMakeLists.txt` 1 处 + embind 绑定 1 处，**不改动任何现有业务逻辑**。
>
> **路径说明**：drawingweb 仓的 C++ 源码（`CadCore.cpp` / `CadCoreWebBridge.cpp` / `CMakeLists.txt` 等）直接位于仓库根目录，**不存在 `DrawingWeb/` 子目录**。本文件中所有路径以仓根为基准。
> **后端状态**：Java 原生 [[License Gate]] 已在 `drawing-ai-server` 落地（提交 `92eda17` `d1a287e`）。协议 100% 对齐本文档引用的设计规范，无需 drawingweb 侧配合其它改动

---

## 0. 改动一览（TL;DR）

| # | 文件 | 类型 | 规模 |
|---|------|------|------|
| 1 | `LicenseGate.h` | **新增** | ~60 行 |
| 2 | `LicenseGate.cpp` | **新增** | ~250 行 |
| 3 | `root_pubkey.inc` | **新增（自动生成）** | 1 行常量 |
| 4 | `CadCore.cpp:571`（`OpenFile`） | **插桩 10 行** | 不改现有逻辑 |
| 5 | `CadCore.cpp:587`（`CreateNewFile`） | **插桩 10 行** | 不改现有逻辑 |
| 6 | `CadCoreWebBridge.cpp`（embind） | **新增 2 个导出函数** | ~10 行 |
| 7 | `CMakeLists.txt`（`oda_sources` 宏内） | **新增 1 个源文件、可选 pre-build 生成 inc** | ~3 行 |

**全部新增代码均受"根公钥硬编码 + 不输出私钥到任何工件"约束。** 根公钥以十六进制常量形式通过头文件注入 `.rodata`，私钥永不出现在 WASM 侧。

---

## 1. 上下文与动机

- 后端（`drawing-ai-server`）按设计规范完整实现了三级密钥 + [[License Gate]]：
  - 根密钥对：厂商离线保管；根公钥需烧录进 WASM
  - 客户密钥对：每客户一对，服务端用客户私钥每 3 分钟签一次短 Token（5 分钟 TTL）
  - 硬件指纹：SM3(machineId ∥ MACs ∥ mainboardUuid) 绑定到 License
- 浏览器在 WASM 启动时拉 `/api/license/info`（整个 license.dat），交给 `initLicenseGate()`；WASM 用硬编码根公钥验 license 签名 → 取出客户公钥
- 每次 `OpenFile / CreateNewFile` 前 WASM 用客户公钥验 `window.__currentLicenseToken`，不通过则拒绝并回调 JS 展示错误
- **若 WASM 侧不接入，整条链路无实际防线**（前端可被绕过）

因此本次改动的核心价值落在 WASM 侧。

---

## 2. 文件 1：`LicenseGate.h`（新增于仓根）

> [[设计文档]] §7.2 已给出完整接口定义，此处原样引用。

```cpp
#pragma once

#include <string>
// SM2 / SM3 原语来自本仓库链接的 **GmSSL**（CMakeLists.txt:130 `libcrypto.a + libssl.a`）
// 推荐引入（按 GmSSL 实际安装头文件路径调整）：
// #include <openssl/sm2.h>
// #include <openssl/sm3.h>
// #include <openssl/evp.h>

class LicenseGate {
public:
    static LicenseGate& instance();

    // WASM 启动时由 JS 调用，传入从 /api/license/info 拉取的 License JSON（整个 license.dat 原文）
    // 返回 false 时，整个 Viewer 不应启动；lastError() 给出原因
    bool initFromLicenseJson(const std::string& licenseJson);

    // 每次 OpenFile / CreateNewFile 前调用
    // 内部：EM_ASM 读 window.__currentLicenseToken → base64url 解码 → SM2 验签
    //      → 检查 license_id 一致 → 检查 expires_at > now
    bool verifyCurrentToken();

    bool isInitialized() const { return m_initialized; }
    const std::string& lastError() const { return m_lastError; }
    const std::string& licenseId() const { return m_licenseId; }

private:
    LicenseGate() = default;

    // 持久状态（进程单例）
    std::string m_rootPubKeyHex;     // 编译时注入，65 字节 uncompressed，130 hex
    std::string m_customerPubKeyHex; // 来自 license.payload.customer_pubkey
    std::string m_licenseId;         // 来自 license.payload.license_id
    long long   m_licenseExpiresSec = 0; // license.payload.expires_at（unix 秒）
    bool        m_initialized = false;
    std::string m_lastError;
};
```

> 如果仓库原本使用 `UcEvpPKey` 等包装类管理密钥对象，将上面两个 hex 字段替换为实际类型即可。本报告采用 `std::string` 十六进制是为了降低适配门槛。

---

## 3. 文件 2：`LicenseGate.cpp`（新增于仓根 · 参考实现）

实现分 4 个职责：
1. 解析 license.dat JSON（只需提取 `payload.license_id`、`payload.customer_pubkey`、`payload.expires_at`、`canonical_payload`、`signature` 五个字段）
2. 用**硬编码根公钥**验证 license 签名
3. Token 解析（base64url 切分）
4. 用 license 中的**客户公钥**验 Token + 检查 license_id/expires_at

**SM2 签名格式**：`base64(R‖S)`，64 字节；**SM2 摘要**：GMT 0009，`e = SM3(Z ∥ m)`，`userId = "1234567812345678"`。

```cpp
#include "LicenseGate.h"
#include "root_pubkey.inc"   // 自动生成：static constexpr const char kRootPubKeyHex[] = "04...";

#include <emscripten.h>
#include <cstring>
#include <cstdio>
#include <chrono>
#include <cstdlib>

// ============================================================
// 0. 依赖的 SM2/SM3/Base64 原语
//    以下 4 个函数需按本仓库已链接的 GmSSL 实际 API 适配（CMakeLists.txt:130 libcrypto.a / libssl.a）：
//      sm2Verify(pubKeyHex, msg, sig64)   -> bool   GMT0009 摘要 + R||S 签名
//      base64Decode(input)                -> bytes
//      base64UrlDecode(input)             -> bytes  RFC 4648 §5, 无填充
//      jsonFind(json, "a.b.c")            -> string 轻量路径查找（或用 nlohmann/json）
// ============================================================

// 伪声明（实际按 GmSSL 头文件为准，候选 API：sm2_do_verify / SM2_do_verify / SM2_verify，
// 参见 asyncify_whitelist.txt:8534-8543 已白名单的 GmSSL SM2 符号）
extern bool        sm2Verify(const std::string& pubKeyHex,
                             const std::string& message,
                             const std::string& signature64Bytes);
extern std::string base64Decode(const std::string& in);
extern std::string base64UrlDecode(const std::string& in);
extern std::string jsonGetString(const std::string& json, const char* path);  // "payload.license_id"
extern long long   jsonGetLong  (const std::string& json, const char* path);

// ============================================================
// LicenseGate 实现
// ============================================================

LicenseGate& LicenseGate::instance() {
    static LicenseGate s;
    return s;
}

bool LicenseGate::initFromLicenseJson(const std::string& licenseJson) {
    m_initialized = false;
    m_lastError.clear();
    m_rootPubKeyHex = kRootPubKeyHex;   // 来自 root_pubkey.inc

    if (licenseJson.empty()) {
        m_lastError = "empty license.dat";
        return false;
    }

    // 1. 取签名 + canonical_payload
    //    设计文档要求服务端把 canonical_payload 一并存档，避免跨语言 JCS 差异
    std::string canonical = jsonGetString(licenseJson, "canonical_payload");
    std::string sigB64    = jsonGetString(licenseJson, "signature");
    if (canonical.empty() || sigB64.empty()) {
        m_lastError = "license missing canonical_payload or signature";
        return false;
    }

    std::string sigBytes = base64Decode(sigB64); // 64 bytes R||S
    if (sigBytes.size() != 64) {
        m_lastError = "license signature length != 64";
        return false;
    }

    // 2. 用硬编码根公钥验 license 签名
    if (!sm2Verify(m_rootPubKeyHex, canonical, sigBytes)) {
        m_lastError = "license root signature INVALID";
        return false;
    }

    // 3. 缓存 payload 字段
    m_licenseId          = jsonGetString(licenseJson, "payload.license_id");
    m_customerPubKeyHex  = jsonGetString(licenseJson, "payload.customer_pubkey");
    // expires_at 在 license 中是 ISO 8601 字符串；这里偷懒，转成 unix 秒
    std::string expIso   = jsonGetString(licenseJson, "payload.expires_at");
    m_licenseExpiresSec  = isoToUnixSec(expIso);  // 由实现者补充 / 或改用 jsonGetLong + epoch

    if (m_licenseId.empty() || m_customerPubKeyHex.size() != 130) {
        m_lastError = "license payload malformed (license_id or customer_pubkey)";
        return false;
    }

    auto nowSec = std::chrono::duration_cast<std::chrono::seconds>(
                      std::chrono::system_clock::now().time_since_epoch()).count();
    if (m_licenseExpiresSec > 0 && nowSec > m_licenseExpiresSec) {
        m_lastError = "license expired";
        return false;
    }

    m_initialized = true;
    std::printf("[License] initialized OK license_id=%s\n", m_licenseId.c_str());
    return true;
}

bool LicenseGate::verifyCurrentToken() {
    m_lastError.clear();
    if (!m_initialized) {
        m_lastError = "license not initialized";
        return false;
    }

    // 1. 从 JS 读 window.__currentLicenseToken（长度不定，MAX 2048）
    char tokenBuf[2048] = {0};
    int n = EM_ASM_INT({
        var t = (window && window.__currentLicenseToken) ? window.__currentLicenseToken : "";
        if (t.length >= $1) return 0;
        stringToUTF8(t, $0, $1);
        return t.length;
    }, tokenBuf, sizeof(tokenBuf));

    if (n <= 0) {
        m_lastError = "no license token on window";
        return false;
    }
    std::string token(tokenBuf, n);

    // 2. 按 "." 切分为 base64url(payload).base64url(sig)
    auto dot = token.find('.');
    if (dot == std::string::npos) {
        m_lastError = "token malformed (no dot)";
        return false;
    }
    std::string payloadB64 = token.substr(0, dot);
    std::string sigB64     = token.substr(dot + 1);

    std::string payloadStr = base64UrlDecode(payloadB64);
    std::string sigBytes   = base64UrlDecode(sigB64);
    if (sigBytes.size() != 64) {
        m_lastError = "token signature length != 64";
        return false;
    }

    // 3. 用客户公钥验签（GMT0009 摘要在 sm2Verify 内部完成）
    if (!sm2Verify(m_customerPubKeyHex, payloadStr, sigBytes)) {
        m_lastError = "token signature INVALID";
        return false;
    }

    // 4. 检查 payload.license_id 与本机一致
    std::string tokenLicId = jsonGetString(payloadStr, "license_id");
    if (tokenLicId != m_licenseId) {
        m_lastError = "token license_id mismatch";
        return false;
    }

    // 5. 检查 token 过期（payload.expires_at 是 unix 秒）
    long long tokenExp = jsonGetLong(payloadStr, "expires_at");
    auto nowSec = std::chrono::duration_cast<std::chrono::seconds>(
                      std::chrono::system_clock::now().time_since_epoch()).count();
    if (nowSec > tokenExp) {
        m_lastError = "token expired";
        return false;
    }

    // 6.（可选）检查 license 本身是否已过期
    if (m_licenseExpiresSec > 0 && nowSec > m_licenseExpiresSec) {
        m_lastError = "license expired";
        return false;
    }

    return true;
}
```

**适配清单**（给 drawingweb 维护者）：
1. `sm2Verify(pubKeyHex, msg, sig64)` —— 映射到本仓库链接的 **GmSSL SM2 验签 API**（候选：`sm2_do_verify` / `SM2_do_verify` / `SM2_verify`，`asyncify_whitelist.txt:8534-8543` 已白名单）。输入为 GMT0009 摘要和 R‖S 64 字节格式。**GmSSL 的 `SM2_do_verify` 接受 `ECDSA_SIG*`**（含 BIGNUM r/s），需先用 `BN_bin2bn` 把 R‖S 拆成两个 32B BIGNUM 包装进 `ECDSA_SIG`；若选用 DER API（`SM2_verify`），则在 R‖S 外层套 [[ASN.1]] SEQUENCE
2. `base64Decode` / `base64UrlDecode` —— 推荐直接在 C++ 实现（~30 行），或通过 `<emscripten/val.h>` 委托 JS 的 `atob`
3. `jsonGetString/jsonGetLong` —— 若仓库已集成 `rapidjson` / `nlohmann::json`，替换为对应调用；否则可临时用 `EM_ASM_*` 委托 `JSON.parse`
4. `isoToUnixSec(string)` —— 可用 `std::get_time` + `timegm`；或直接让后端返回 unix 秒

---

## 4. 文件 3：`root_pubkey.inc`（自动生成，位于仓根）

**生成方法**（建议在 drawing-ai-server 侧执行，避免厂商在 drawingweb 仓库误存私钥）：

```bash
# 1. 厂商一次性生成根密钥对（ai-server CLI，结果已在本次 commit d1a287e 验证可用）
cd drawing-cad/drawing-ai-server
mvn dependency:build-classpath -Dmdep.outputFile=target/cp.txt -q
java -cp "$(cat target/cp.txt);target/classes" \
  com.lvjian.drawingai.license.tools.LicenseToolsMain generate-root-key \
  --out ./keys

# → ./keys/root_private.pem（加密保管，绝不提交）
# → ./keys/root_public.pem（公钥 hex，可提交或直接嵌入）
```

**从 root_public.pem 生成 `root_pubkey.inc`**（一行 shell 或等价 js）：

```bash
HEX=$(grep -v "-----" keys/root_public.pem | tr -d '\n')
cat > root_pubkey.inc <<EOF
// AUTO-GENERATED - DO NOT EDIT
// 根公钥（SM2 uncompressed, 65 bytes / 130 hex chars, 前缀 0x04）
static constexpr const char kRootPubKeyHex[] =
    "$HEX";
EOF
```

建议：
- `root_pubkey.inc` **可以提交**（公钥公开无害，且便于 CI 重建 WASM）
- `root_public.pem` / `root_private.pem` **绝不提交** drawingweb 仓

---

## 5. 文件 4：`CadCore.cpp` 插桩（仓根）

> **只改 2 处，每处插入约 10 行**；**不修改原有任何语句**。

### 5.1 `OpenFile`（设计文档引用行号 571，按实际代码行号就近插入即可）

```cpp
#include "LicenseGate.h"   // 在文件头部 include 区追加

// ...

void CadCore::OpenFile(std::wstring name)
{
    // ===== License Gate (INSERTED) =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        std::string err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('OpenFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] OpenFile denied: %s\n", err.c_str());
        return;   // 直接返回，不调用后续任何原有语句
    }
    // ===== End License Gate =====

    releaseDeviceAndContext();  // ← 原有第 1 行逻辑起点
    // ...（原逻辑不改）
}
```

### 5.2 `CreateNewFile`（设计文档引用行号 587）

```cpp
void CadCore::CreateNewFile()
{
    // ===== License Gate (INSERTED) =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        std::string err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('CreateNewFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] CreateNewFile denied: %s\n", err.c_str());
        return;
    }
    // ===== End License Gate =====

    releaseDeviceAndContext();
    // ...（原逻辑不改）
}
```

**注意**：`window.__onLicenseDenied` 由前端 `src/hooks/useWasmModule.js` 注册，展示全屏 `LicenseErrorOverlay` 并阻止后续交互。前端已在本轮合并中落地（drawing-web-app commit `897d438`）。

---

## 6. 文件 5：`CadCoreWebBridge.cpp`（embind 追加，仓根）

```cpp
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
    function("licenseId", +[]() {
        return LicenseGate::instance().licenseId();
    });
    function("licenseLastError", +[]() {
        return LicenseGate::instance().lastError();
    });
}
```

前端会在 WASM `postRun` 里首先 `fetch('/api/license/info')` → `Module.initLicenseGate(text)`，失败则直接阻止 Viewer 初始化（已实装）。

---

## 7. 文件 6：`CMakeLists.txt`（仓根 · `buildTeighaClient` macro 内）

### 7.1 新增源文件

本仓库不用标准 `add_executable`，而是通过 `oda_sources(${name} ...)` 宏统一收集源文件（定义于 ODA/Teigha 构建框架，`CMakeLists.txt:259` 起 `buildTeighaClient` macro 内）。

**修改点**：在 `CadCoreWebBridge.cpp` 之后追加一行 `LicenseGate.cpp`。参考现状：

```cmake
# CMakeLists.txt:262-274（buildTeighaClient macro 内 oda_sources 调用）
oda_sources(${name}
    App.cpp
    CadCore.cpp
    CadCoreLisp.cpp
    CadCoreScript.cpp
    CadCoreServices.cpp
    CadCoreWebBridge.cpp
    LicenseGate.cpp        # ← NEW（新增此行）
    CadCoreEdBaseIO.cpp
    CadCoreCompare.cpp
    CadCoreView.cpp
    Commands.cpp
    GisCommands.cpp
    ${WRAPPERS_CPP}
    ...
)
```

`LicenseGate.h` 为头文件，与 `CadCore.cpp` 同目录，不需要额外 `target_include_directories`。

### 7.2 前置生成 `root_pubkey.inc`

在构建开始前调用（或作为 CMake `add_custom_command` 的 pre-build step）：

```bash
# 假定 root_public.pem 已由 CI secret 提供到 $ROOT_PUBKEY_PATH
hex=$(grep -v '-----' "$ROOT_PUBKEY_PATH" | tr -d '\n')
printf '// AUTO-GENERATED\nstatic constexpr const char kRootPubKeyHex[] = "%s";\n' "$hex" \
  > root_pubkey.inc
```

如果允许 `root_pubkey.inc` 入库，则跳过此步；首次由维护者手工生成一次即可。

### 7.3 GmSSL 链接现状

无需额外改动链接配置。`CMakeLists.txt:130` 已有 `libcrypto.a + libssl.a`（GmSSL），`CMakeLists.txt:173` 已链接 `${UACORE_LIB}`。`LicenseGate.cpp` 只需 `#include <openssl/sm2.h>` 等 GmSSL 头文件（或仓库已有的 `TKERNEL_ROOT/Extensions/win/Crypt` 包装），即可使用 SM2/SM3 API。

### 7.4 其余编译选项

- 需开启 `-s MODULARIZE=1 -s EXPORT_NAME=createDrawingJsModule`（当前已是）
- 不需要新的链接参数（`EM_ASM` 默认可用）

---

## 8. 协议对齐点（已由后端实现，无须 drawingweb 配合改动）

| 点位 | 后端实现 | 影响 WASM 侧 |
|------|---------|--------------|
| canonical JSON（JCS 子集） | `CanonicalJsonSerializer.java` | **已把 canonical_payload 存入 license.dat**，WASM 无需再做规范化 |
| SM2 签名格式 | `Sm2Helper.sign()` 统一 64B R‖S；内部 ParametersWithID="1234567812345678" | WASM 若用原生 DER API 需转换一次 |
| Token 编码 | `TokenSigner.java` base64url 无填充 | WASM 必须用**无填充** base64url 解码器 |
| `license.dat` 体积 | 约 1–2 KB | WASM 启动 fetch 一次，无性能影响 |
| 启动自检 | `LicenseStartupRunner` 失败则 `System.exit(1)` | 后端启动失败时前端 fetch `/api/license/info` 会得到连接错误，不进 WASM 阶段 |

---

## 9. 本地验收方案

1. **后端启动**：`cd drawing-cad/drawing-ai-server && mvn spring-boot:run`，观察启动日志 `License self-check OK license_id=LIC-...`
2. **前端启动**：`cd drawing-cad/drawing-web-app && pnpm dev`
3. **浏览器访问**：首页 F12 控制台预期依次看到：
   - `fetch('/api/license/info') → 200`
   - `Module.initLicenseGate(...) → true`
   - 心跳 `setInterval 180s` 建立
   - 打开图纸时 `[License] OpenFile OK`
4. **反例 1（根签名篡改）**：手工修改 `license.dat` 的某一字符 → `initLicenseGate` 返回 false，前端 overlay 显示错误
5. **反例 2（Token 篡改）**：在控制台 `window.__currentLicenseToken = 'bad.bad'` → 打开图纸被拒，`LicenseErrorOverlay` 弹出 `token signature INVALID`
6. **反例 3（并发超限）**：开 11 个标签页，第 11 个 `/api/license/session/start` 返回 429（后端 `SessionStore.maxConcurrent` 控制）
7. **反例 4（license 过期）**：把系统时钟调到 `expires_at + 1 day` 后刷新 → 启动自检失败

---

## 10. 联系与交付

- **代码基线**：参考 design.md 第 7 章；前后端改动已合并到：
  - `drawing-cad/drawing-web-app` feat-lgs `897d438`（前端 LicenseStore + Overlay + useWasmModule bootstrap）
  - `drawing-cad/drawing-ai-server` master `92eda17 + d1a287e`（后端 + 厂商 CLI）
- **私钥流转**：推荐由厂商运维保管 `root_private.pem`，**只把 `root_pubkey.inc` 或公钥 hex 文本**传给 drawingweb 维护者
- **验收反馈**：将构建出的 `DrawingJs.{js,wasm,data}` 发布到 OSS 替换现有版本；前端 `public/` 目录无需改动
- **回滚策略**：若 [[License Gate]] 发现重大阻塞问题，临时将 `verifyCurrentToken()` 的实现体改为 `return true;` 即可旁路（**仅紧急情况使用**，且必须在新版本中恢复）

---

## 附录 A：设计规范原文对照

本报告的所有条目均可在以下文档中找到原文依据：

- `drawing-web-app/docs/superpowers/specs/2026-04-15-wasm-license-gate-design.md`
  - §3 三对密钥（根 / 客户 / 指纹）
  - §4 License 文件格式（JSON + Canonical + SM2 R‖S）
  - §5 Token 协议（base64url + 5min TTL + 心跳 180s）
  - §7 WASM / C++ 实现规范（本报告主体）
  - §11 运维工具

- 后端落地参考：
  - `drawing-ai-server/src/main/java/com/lvjian/drawingai/license/` 全部类
  - `drawing-ai-server/src/main/java/com/lvjian/drawingai/license/tools/LicenseToolsMain.java`（4 子命令 CLI）

## 相关笔记

- [[DrawingWeb (WASM) License Gate C++ 修改报告]]
- [[WASM引擎]]
- [[ODA demo cases integration and code optimization]]
- [[WASM API 覆盖报告（p17-wasm-report-1）]]
- [[WASM Emscripten 绑定规律手册]]
- [[WASM License Gate 实施报告（p17-wasm-report-3）]]
- [[WASM 性能优化：批量实体快照 API（Plan A）]]
- [[WASM 结构提取性能分析报告（p17-wasm-report-2）]]
