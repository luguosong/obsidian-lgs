# License Gate — WASM 图纸加载硬件许可

`license/` 包实现端到端的离线许可证校验，在 WASM 加载每张图纸前做握手。纯 Java 实现，**已完全取代早期 Node.js 版本**。

> **⚠️ 授权文件签发非本仓职责**
>
> `license.dat` / `customer_key.pem` / `root_pubkey.pem` 以及厂商持有的
> `root_private.pem` / `root_public.pem`，**均由专职负责人统一签发**。
> 本仓（drawing-ai-server）及 AI 助手**不得**代为执行 `generate-root-key` /
> `sign-license` 等厂商 CLI 命令来生成授权文件，也不得提交任何 `.pem` /
> `license.dat` 到 Git。需要新证书时请联系授权负责人，只负责把下发的文件
> 放入约定目录（`./license/` 或容器 bind mount 路径）。

## 协议角色

| 角色 | 谁持有 | 职责 |
|------|--------|------|
| 根密钥对 | 厂商 | 签发 customer 私钥 + license payload |
| 客户密钥 + license.dat | 每台客户机 | 绑定硬件指纹，签 5 分钟 token 给 WASM |
| 根公钥（烤入 WASM） | WASM C++ 插桩 | 验证 token 未被伪造 |

## 运行时流程

1. 启动：`LicenseStartupRunner` 依次校验根签名 → 指纹 → 过期日 → 客户私钥，失败 `System.exit(1)`
2. WASM 加载图纸前：前端 `LicenseStore` POST `/api/license/session/start`，Java 端返回 5min TTL token（`base64url(payload).base64url(sm2sig)`）
3. 5 分钟续期：`/api/license/token/refresh`
4. 并发超限：429 `MAX_CONCURRENT_REACHED`
5. 关闭标签：`sendBeacon` 到 `/api/license/session/end`（text/plain）

## 厂商离线 CLI（`LicenseToolsMain`）

```bash
# 位于 Spring Boot fat jar，通过 PropertiesLauncher 调用 tools 主类
java -cp target/drawing-ai-server-*.jar \
     -Dloader.main=com.lvjian.drawingai.license.tools.LicenseToolsMain \
     org.springframework.boot.loader.launch.PropertiesLauncher \
     <subcommand> [args...]

# 子命令：
#   generate-root-key <pub.pem> <priv.pem>      — 生成 SM2 根密钥对
#   sign-license <payload.json> <root_priv.pem> <out.dat>  — 用根私钥签发 license
#   verify-license <license.dat> <root_pub.pem> — 验证 license 文件
#   print-fingerprint                           — 输出当前机器 64 hex 指纹（客户机运行）
```

## 关键实现点

- `Sm2Helper`：Bouncy Castle `SM2Signer` + `ParametersWithID("1234567812345678")`，DER 输出**必须手工解析 R/S 填充到 64 字节**（前端 sm-crypto 只接受 R‖S）
- `CanonicalJsonSerializer`：RFC 8785 JCS 子集（键排序 + 整数时间戳避免浮点歧义），与 Node `canonical-json.js` 字节对齐
- `FingerprintService`：OSHI 采集 `/etc/machine-id` + 主板 UUID + MAC → SM3。Linux 容器需 bind mount `/etc/machine-id`、`/sys/class/dmi/id/{product_uuid,board_serial}`，Windows 部署指纹降级
- `SessionStore`：ConcurrentHashMap，TTL 扫描 + `max_concurrent` 限流
- `LicenseController` 对前端暴露 4 个 endpoint，**WASM 端会在 `initLicenseGate()` 里再次用根公钥验签 token**（防止绕过 Java 端）

## 配置清单（`application.yml`）

```yaml
license:
  enabled:             ${LICENSE_ENABLED:true}
  file:                ${LICENSE_FILE:./license/license.dat}
  customer-key:        ${LICENSE_CUSTOMER_KEY:./license/customer_key.pem}
  root-pubkey:         ${LICENSE_ROOT_PUBKEY:./license/root_pubkey.pem}
  token-ttl-sec:       ${LICENSE_TOKEN_TTL_SEC:300}
  session-ttl-sec:     ${LICENSE_SESSION_TTL_SEC:300}
```

容器部署参见 `docker-compose/uocs-app/compose.drawing-cad.yaml` 与
`docker-compose/uocs-app/drawing-cad/license/README.md`。WASM 侧 C++ 插桩
参考 `drawing-cad/drawing-web-app/docs/wasm-license-gate-cpp-patch.md`。
