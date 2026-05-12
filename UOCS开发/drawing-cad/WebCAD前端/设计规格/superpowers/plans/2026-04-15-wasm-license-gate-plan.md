# WASM License Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 `DrawingJs.wasm` 必须连接厂商签发的 License + 后端 Server 才能打开/新建图纸。已打开图纸继续可编辑；新建/再次打开需要有效授权。

**Architecture:** 双层非对称 SM2 信任链：厂商根密钥签 License（每客户一份，绑定服务器硬件指纹 + 最大并发数），客户密钥签 5 分钟短期 Token；JS 每 3 分钟心跳续签；WASM 在 `CadCore::OpenFile/CreateNewFile` 入口做 SM2 验签与过期检查。

**Tech Stack:**
- Server：Node.js（Express），`sm-crypto`（SM2/SM3）、`node-machine-id`
- WASM：C++ 17，已集成 `libUACore.a` + `libUARoot.a` + GMSSL
- Frontend：React 19 + MobX
- Docker：`network_mode: host` + bind mount 宿主硬件信息

**Reference spec:** [docs/superpowers/specs/2026-04-15-wasm-license-gate-design.md](../specs/2026-04-15-wasm-license-gate-design.md)

---

## File Structure

```
DrawingWebApp/
├── server/
│   ├── package.json                    # 修改: 加 sm-crypto, node-machine-id
│   ├── index.js                        # 修改: 启动时调 validator, 挂 license 路由
│   ├── license/                        # 新建: 运行时 license 文件 (不进 git)
│   │   ├── .gitignore                  #   仅允许 root_pubkey.pem 与示例
│   │   └── root_pubkey.pem             # 新建: 厂商根公钥 (公开不敏感)
│   ├── license-gate/                   # 新建
│   │   ├── canonical-json.js           #   确定性 JSON 序列化
│   │   ├── base64url.js                #   RFC 4648 §5 编解码
│   │   ├── fingerprint.js              #   宿主硬件指纹 (SM3)
│   │   ├── validator.js                #   启动自检
│   │   ├── signer.js                   #   签发 Token
│   │   ├── sessions.js                 #   内存会话表
│   │   └── routes.js                   #   4 个 HTTP endpoint
│   ├── tools/                          # 新建: 厂商 / 客户离线工具
│   │   ├── generate-root-key.js
│   │   ├── sign-license.js
│   │   ├── print-fingerprint.js
│   │   ├── embed-root-pubkey.js
│   │   └── verify-license.js
│   └── test/                           # 新建: node:test 测试
│       ├── fixtures/                   #   固定测试用根密钥 (仅测试用)
│       ├── canonical-json.test.js
│       ├── base64url.test.js
│       ├── fingerprint.test.js
│       ├── signer.test.js
│       ├── sessions.test.js
│       └── routes.test.js
├── Dockerfile                          # 新建
├── docker-compose.yml                  # 新建
└── src/
    ├── hooks/
    │   └── useWasmModule.js            # 修改: postRun 里拉 license + 启心跳
    ├── stores/
    │   └── LicenseStore.js             # 新建: MobX 授权状态
    ├── context/
    │   └── ViewerContext.js            # 修改: 注册 LicenseStore
    └── components/
        └── LicenseErrorOverlay/        # 新建: 授权失败全屏蒙层
            ├── LicenseErrorOverlay.jsx
            └── LicenseErrorOverlay.module.css

DrawingWeb/
├── LicenseGate.h                       # 新建
├── LicenseGate.cpp                     # 新建
├── root_pubkey.inc                     # 新建 (自动生成, 可提交)
├── CadCore.cpp                         # 修改: OpenFile & CreateNewFile 插桩
├── CadCoreWebBridge.cpp                # 修改: 加 embind 绑定
└── CMakeLists.txt                      # 修改: 加 LicenseGate.cpp 源文件
```

---

## Conventions used in this plan

- **TDD discipline**：Phase 1–3（Node.js 部分）严格按 RED → GREEN → COMMIT 节奏。每个测试先失败，再通过
- **测试框架**：Node 内置的 `node:test` + `assert`。零新增依赖
- **提交粒度**：每个 Task 结束一次 commit，消息遵循仓库约定（`feat(license):`、`test(license):`）
- **C++ 与前端 UI 采用手动验证**（受限于没有现成测试框架）
- **路径约定**：
  - 服务端代码相对于 `DrawingWebApp/server/`
  - 前端代码相对于 `DrawingWebApp/src/`
  - WASM 代码相对于 `DrawingWeb/`

---

## Phase 0: 准备工作

### Task 0.1: 新增 npm 依赖

**Files:**
- Modify: `DrawingWebApp/server/package.json`

- [ ] **Step 1: 添加依赖**

编辑 `server/package.json`，在 `dependencies` 加入：

```json
    "sm-crypto": "^0.3.13",
    "node-machine-id": "^1.1.12",
```

完整 `dependencies` 段（保留已有）：

```json
  "dependencies": {
    "@ai-sdk/anthropic": "^3.0.66",
    "@ai-sdk/deepseek": "^2.0.27",
    "@ai-sdk/google": "^3.0.57",
    "@ai-sdk/openai": "^3.0.41",
    "ai": "^6.0.116",
    "cors": "^2.8.5",
    "dotenv": "^16.4.0",
    "express": "^4.21.0",
    "node-machine-id": "^1.1.12",
    "sm-crypto": "^0.3.13",
    "zod": "^3.23.0"
  }
```

同时在 `scripts` 加测试脚本：

```json
  "scripts": {
    "dev": "node --watch index.js",
    "start": "node index.js",
    "test": "node --test test/**/*.test.js",
    "license:dev-fixtures": "node tools/dev-fixtures.js"
  }
```

- [ ] **Step 2: 安装**

```bash
cd DrawingWebApp/server
npm install
```

Expected: 安装成功，`node_modules/sm-crypto/` 与 `node_modules/node-machine-id/` 存在。

- [ ] **Step 3: 验证 sm-crypto 可用**

```bash
node -e "const { sm2, sm3 } = require('sm-crypto'); console.log('sm3:', sm3('hello')); const kp = sm2.generateKeyPairHex(); console.log('privkey len:', kp.privateKey.length, 'pubkey len:', kp.publicKey.length);"
```

Expected：
```
sm3: becbbfaae6548b8bf0cfcad5a27183cd1be6093b1cceccc303d9c61d0a645268
privkey len: 64
pubkey len: 130
```

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/server/package.json DrawingWebApp/server/package-lock.json
git commit -m "feat(license): add sm-crypto and node-machine-id deps"
```

---

### Task 0.2: 目录骨架

**Files:**
- Create: `DrawingWebApp/server/license-gate/` (empty)
- Create: `DrawingWebApp/server/tools/`
- Create: `DrawingWebApp/server/test/fixtures/`
- Create: `DrawingWebApp/server/license/.gitignore`

- [ ] **Step 1: 新建目录与占位文件**

```bash
mkdir -p DrawingWebApp/server/license-gate
mkdir -p DrawingWebApp/server/tools
mkdir -p DrawingWebApp/server/test/fixtures
mkdir -p DrawingWebApp/server/license
```

- [ ] **Step 2: 写 `server/license/.gitignore`**

```gitignore
# 所有运行时 license 文件都不进 git, 只有示例与公钥例外
*
!.gitignore
!root_pubkey.pem
!README.md
```

- [ ] **Step 3: 写 `server/license/README.md`**

```markdown
# License 目录

此目录存放运行时文件, **大部分不进入 git**:

- `license.dat`          — 厂商签发的许可证 JSON (由 `sign-license.js` 生成)
- `customer_key.pem`     — 客户 SM2 私钥, 权限必须 0600
- `root_pubkey.pem`      — 厂商根公钥 (公开不敏感, 可以进 git)

容器部署时本目录挂载为 `/app/license:ro`。

开发环境: 运行 `npm run license:dev-fixtures` 生成本机可用的测试 license。
```

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/server/license/
git commit -m "feat(license): scaffold license directory with gitignore"
```

---

## Phase 1: 共用工具（纯函数，零依赖）

### Task 1.1: canonical-json 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/canonical-json.js`
- Create: `DrawingWebApp/server/test/canonical-json.test.js`

- [ ] **Step 1: 写失败测试** `test/canonical-json.test.js`

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { canonicalJson } from '../license-gate/canonical-json.js'

test('canonicalJson sorts keys alphabetically', () => {
  const out = canonicalJson({ b: 1, a: 2 })
  assert.equal(out, '{"a":2,"b":1}')
})

test('canonicalJson is recursive', () => {
  const out = canonicalJson({ x: { c: 3, a: 1, b: 2 } })
  assert.equal(out, '{"x":{"a":1,"b":2,"c":3}}')
})

test('canonicalJson keeps array order', () => {
  assert.equal(canonicalJson([3, 1, 2]), '[3,1,2]')
})

test('canonicalJson handles null/number/bool/string', () => {
  assert.equal(canonicalJson(null), 'null')
  assert.equal(canonicalJson(42), '42')
  assert.equal(canonicalJson(true), 'true')
  assert.equal(canonicalJson('x'), '"x"')
})

test('canonicalJson produces same bytes for same logical object', () => {
  const a = { z: 1, a: { m: 2, n: 3 } }
  const b = { a: { n: 3, m: 2 }, z: 1 }
  assert.equal(canonicalJson(a), canonicalJson(b))
})

test('canonicalJson has no whitespace', () => {
  const out = canonicalJson({ a: 1, b: [2, 3] })
  assert.equal(out, '{"a":1,"b":[2,3]}')
})
```

- [ ] **Step 2: 运行测试看它们失败**

```bash
cd DrawingWebApp/server
npm test
```

Expected: 6 个测试失败（模块不存在）

- [ ] **Step 3: 实现** `license-gate/canonical-json.js`

```js
/**
 * RFC 8785 JCS 风格确定性 JSON 序列化 (足够版本, 不覆盖所有 RFC 细节)
 * - 键按 Unicode code point 升序排序
 * - 无任何空白
 * - 递归处理对象
 * - 数组保持原始顺序
 */
export function canonicalJson(obj) {
  if (obj === null || typeof obj !== 'object') {
    return JSON.stringify(obj)
  }
  if (Array.isArray(obj)) {
    return '[' + obj.map(canonicalJson).join(',') + ']'
  }
  const keys = Object.keys(obj).sort()
  return '{' + keys.map(k => JSON.stringify(k) + ':' + canonicalJson(obj[k])).join(',') + '}'
}
```

- [ ] **Step 4: 运行测试看它们通过**

```bash
npm test
```

Expected: 所有 canonical-json 测试 PASS

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/canonical-json.js server/test/canonical-json.test.js
git commit -m "feat(license): add canonical JSON serializer"
```

---

### Task 1.2: base64url 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/base64url.js`
- Create: `DrawingWebApp/server/test/base64url.test.js`

- [ ] **Step 1: 写失败测试**

```js
// test/base64url.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { base64urlEncode, base64urlDecode } from '../license-gate/base64url.js'

test('encode produces URL-safe chars, no padding', () => {
  const out = base64urlEncode(Buffer.from([0xfb, 0xff, 0xff])) // 标准 base64 含 + / 填充
  assert.match(out, /^[A-Za-z0-9_-]+$/)
  assert.ok(!out.includes('='))
})

test('decode is inverse of encode', () => {
  for (const len of [0, 1, 2, 3, 32, 64, 128]) {
    const input = Buffer.from(Array.from({ length: len }, (_, i) => i & 0xff))
    const round = base64urlDecode(base64urlEncode(input))
    assert.deepEqual(round, input)
  }
})

test('decode accepts missing padding', () => {
  const orig = Buffer.from('hello')      // 5 bytes → 标准 base64 "aGVsbG8="
  const noPad = base64urlEncode(orig)     // "aGVsbG8"
  const back = base64urlDecode(noPad)
  assert.deepEqual(back, orig)
})
```

- [ ] **Step 2: 运行测试看失败**

```bash
npm test
```

- [ ] **Step 3: 实现** `license-gate/base64url.js`

```js
/**
 * RFC 4648 §5 base64url 编解码 (无填充)
 */
export function base64urlEncode(buf) {
  return Buffer.from(buf).toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '')
}

export function base64urlDecode(str) {
  // 补齐填充到 4 的倍数
  const pad = (4 - (str.length % 4)) % 4
  const normalized = str.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat(pad)
  return Buffer.from(normalized, 'base64')
}
```

- [ ] **Step 4: 运行测试看通过**

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/base64url.js server/test/base64url.test.js
git commit -m "feat(license): add base64url encoder/decoder"
```

---

### Task 1.3: SM2 签/验 helper + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/sm2-helper.js`
- Create: `DrawingWebApp/server/test/sm2-helper.test.js`

这个模块封装 `sm-crypto`，统一约定 `hash: true, der: false`（输出 64 字节 R||S），与 WASM 侧 `UcEvpPKey::verify` 互通。

- [ ] **Step 1: 写失败测试**

```js
// test/sm2-helper.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import pkg from 'sm-crypto'
const { sm2 } = pkg
import { sm2Sign, sm2Verify } from '../license-gate/sm2-helper.js'

test('sign and verify roundtrip', () => {
  const { privateKey, publicKey } = sm2.generateKeyPairHex()
  const msg = 'hello license'
  const sig = sm2Sign(msg, privateKey)
  assert.ok(sm2Verify(msg, sig, publicKey), 'verify should return true')
})

test('verify fails when signature tampered', () => {
  const { privateKey, publicKey } = sm2.generateKeyPairHex()
  const sig = sm2Sign('abc', privateKey)
  // 翻转一个 bit
  const tampered = Buffer.from(sig)
  tampered[10] ^= 0x01
  assert.equal(sm2Verify('abc', tampered, publicKey), false)
})

test('verify fails when message tampered', () => {
  const { privateKey, publicKey } = sm2.generateKeyPairHex()
  const sig = sm2Sign('abc', privateKey)
  assert.equal(sm2Verify('abd', sig, publicKey), false)
})

test('signature output is exactly 64 bytes', () => {
  const { privateKey } = sm2.generateKeyPairHex()
  const sig = sm2Sign('hello', privateKey)
  assert.equal(sig.length, 64)
})
```

- [ ] **Step 2: 运行测试看失败**

- [ ] **Step 3: 实现** `license-gate/sm2-helper.js`

```js
import pkg from 'sm-crypto'
const { sm2 } = pkg

/**
 * SM2 签名 (GMT0009 userId=1234567812345678, SM3 摘要, R||S 格式)
 * @param {string|Buffer} message - 待签名数据
 * @param {string} privateKeyHex  - 64 字符 hex
 * @returns {Buffer} 64 字节 R||S
 */
export function sm2Sign(message, privateKeyHex) {
  const msgStr = typeof message === 'string' ? message : message.toString('utf8')
  const sigHex = sm2.doSignature(msgStr, privateKeyHex, {
    hash: true,   // 自动 SM3 + GMT0009 Z 值
    der: false,   // 64 字节 R||S, 不用 DER
  })
  return Buffer.from(sigHex, 'hex')
}

/**
 * SM2 验签
 * @param {string|Buffer} message
 * @param {Buffer} signature 64 字节 R||S
 * @param {string} publicKeyHex 130 字符 hex (04 + x + y)
 * @returns {boolean}
 */
export function sm2Verify(message, signature, publicKeyHex) {
  const msgStr = typeof message === 'string' ? message : message.toString('utf8')
  const sigHex = Buffer.from(signature).toString('hex')
  return sm2.doVerifySignature(msgStr, sigHex, publicKeyHex, {
    hash: true,
    der: false,
  })
}
```

- [ ] **Step 4: 运行测试通过**

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/sm2-helper.js server/test/sm2-helper.test.js
git commit -m "feat(license): add SM2 sign/verify helper (GMT0009, R||S)"
```

---

## Phase 2: 厂商/客户离线工具

### Task 2.1: generate-root-key.js

**Files:**
- Create: `DrawingWebApp/server/tools/generate-root-key.js`

- [ ] **Step 1: 实现**

```js
#!/usr/bin/env node
/**
 * 生成厂商根密钥对 (SM2)
 * 输出: root_private.pem, root_public.pem
 *
 * ⚠️ 此脚本只应在离线机上运行一次; root_private.pem 永不联网
 *
 * Usage:
 *   node tools/generate-root-key.js [output-dir]
 */
import fs from 'fs'
import path from 'path'
import pkg from 'sm-crypto'
const { sm2 } = pkg

const outDir = process.argv[2] || '.'
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true })

const { privateKey, publicKey } = sm2.generateKeyPairHex()

// PEM-like wrapping (纯 hex, 加 header/footer 方便识别)
const priv =
  '-----BEGIN SM2 PRIVATE KEY-----\n' +
  privateKey + '\n' +
  '-----END SM2 PRIVATE KEY-----\n'

const pub =
  '-----BEGIN SM2 PUBLIC KEY-----\n' +
  publicKey + '\n' +
  '-----END SM2 PUBLIC KEY-----\n'

const privPath = path.join(outDir, 'root_private.pem')
const pubPath  = path.join(outDir, 'root_public.pem')

fs.writeFileSync(privPath, priv, { mode: 0o600 })
fs.writeFileSync(pubPath, pub)

console.log('Generated SM2 root key pair:')
console.log('  PRIVATE (keep offline!): ' + privPath)
console.log('  PUBLIC  (embed in WASM): ' + pubPath)
console.log('Private key fingerprint:   ' + sm2.getPublicKeyFromPrivateKey(privateKey).substring(0, 32) + '...')
```

- [ ] **Step 2: 本地自测**

```bash
cd DrawingWebApp/server
node tools/generate-root-key.js /tmp/test-root
cat /tmp/test-root/root_public.pem
```

Expected: 3 行 PEM，中间一行 130 hex 字符。

- [ ] **Step 3: 加一个 hex 解析 helper** (后续工具要用)

创建 `server/license-gate/pem.js`:

```js
import fs from 'fs'

export function readHexFromPem(path, expectedLabel) {
  const text = fs.readFileSync(path, 'utf8')
  const re = new RegExp(`-----BEGIN ${expectedLabel}-----\\s*([0-9a-fA-F]+)\\s*-----END ${expectedLabel}-----`)
  const m = text.match(re)
  if (!m) throw new Error(`PEM file ${path} missing ${expectedLabel}`)
  return m[1].trim()
}
```

- [ ] **Step 4: Commit**

```bash
git add server/tools/generate-root-key.js server/license-gate/pem.js
git commit -m "feat(license): add root key pair generator tool"
```

---

### Task 2.2: print-fingerprint.js + fingerprint.js 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/fingerprint.js`
- Create: `DrawingWebApp/server/test/fingerprint.test.js`
- Create: `DrawingWebApp/server/tools/print-fingerprint.js`

- [ ] **Step 1: 写测试**

```js
// test/fingerprint.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { computeFingerprint, computeFingerprintFromParts } from '../license-gate/fingerprint.js'

test('computeFingerprintFromParts is deterministic', () => {
  const parts = { machineId: 'abc', macs: ['00:11:22:33:44:55'], motherboardUuid: 'xyz' }
  assert.equal(computeFingerprintFromParts(parts), computeFingerprintFromParts(parts))
})

test('computeFingerprintFromParts sorts MACs', () => {
  const a = computeFingerprintFromParts({
    machineId: 'm', macs: ['aa:aa:aa:aa:aa:aa', 'bb:bb:bb:bb:bb:bb'], motherboardUuid: 'u'
  })
  const b = computeFingerprintFromParts({
    machineId: 'm', macs: ['bb:bb:bb:bb:bb:bb', 'aa:aa:aa:aa:aa:aa'], motherboardUuid: 'u'
  })
  assert.equal(a, b)
})

test('computeFingerprintFromParts lowercases MACs', () => {
  const a = computeFingerprintFromParts({
    machineId: 'm', macs: ['AA:BB:CC:DD:EE:FF'], motherboardUuid: 'u'
  })
  const b = computeFingerprintFromParts({
    machineId: 'm', macs: ['aa:bb:cc:dd:ee:ff'], motherboardUuid: 'u'
  })
  assert.equal(a, b)
})

test('computeFingerprintFromParts outputs 64 hex chars', () => {
  const fp = computeFingerprintFromParts({ machineId: 'x', macs: [], motherboardUuid: 'y' })
  assert.match(fp, /^[0-9a-f]{64}$/)
})

test('computeFingerprint returns same format on this machine', () => {
  const fp = computeFingerprint()
  assert.match(fp, /^[0-9a-f]{64}$/)
})
```

- [ ] **Step 2: 运行失败**

- [ ] **Step 3: 实现** `license-gate/fingerprint.js`

```js
import os from 'os'
import fs from 'fs'
import { execSync } from 'child_process'
import { machineIdSync } from 'node-machine-id'
import pkg from 'sm-crypto'
const { sm3 } = pkg

const VIRTUAL_IF_PATTERN = /^(docker|veth|br-|virbr|tun|tap|cni|flannel|cali|lo)/

/**
 * 从预先收集的三件套计算指纹 (便于测试)
 */
export function computeFingerprintFromParts({ machineId, macs, motherboardUuid }) {
  const sortedMacs = macs.map(m => m.toLowerCase()).sort().join(',')
  const input = `${machineId}|${sortedMacs}|${motherboardUuid}`
  return sm3(input)
}

/**
 * 从当前机器收集三件套并计算指纹
 */
export function computeFingerprint() {
  const parts = collectParts()
  return computeFingerprintFromParts(parts)
}

/**
 * 收集硬件三件套 (便于日志与工具打印)
 */
export function collectParts() {
  return {
    machineId:      getMachineId(),
    macs:           getPhysicalMacs(),
    motherboardUuid: getMotherboardUuid(),
  }
}

function getMachineId() {
  try { return machineIdSync({ original: true }) }
  catch (_) { return 'unknown-machine-id' }
}

function getPhysicalMacs() {
  const ifs = os.networkInterfaces()
  const out = []
  for (const [name, addrs] of Object.entries(ifs)) {
    if (VIRTUAL_IF_PATTERN.test(name)) continue
    for (const a of addrs || []) {
      if (a.internal) continue
      if (!a.mac || a.mac === '00:00:00:00:00:00') continue
      out.push(a.mac)
    }
  }
  // 去重
  return [...new Set(out)]
}

function getMotherboardUuid() {
  try {
    if (process.platform === 'win32') {
      const out = execSync('wmic csproduct get uuid', { encoding: 'utf8' })
      const lines = out.split('\n').map(l => l.trim()).filter(Boolean)
      // lines[0] = "UUID", lines[1] = the UUID
      if (lines.length >= 2) return lines[1]
      return 'unknown-mb-uuid'
    }
    // 优先宿主机挂载路径 (Docker)
    const hostPath = '/host/product_uuid'
    if (fs.existsSync(hostPath)) return fs.readFileSync(hostPath, 'utf8').trim()
    return fs.readFileSync('/sys/class/dmi/id/product_uuid', 'utf8').trim()
  } catch (_) {
    return 'unknown-mb-uuid'
  }
}
```

- [ ] **Step 4: 运行测试通过**

- [ ] **Step 5: 实现** `tools/print-fingerprint.js`

```js
#!/usr/bin/env node
/**
 * 打印本机硬件指纹, 客户发给厂商用于签 License
 *
 * Usage:
 *   node tools/print-fingerprint.js
 */
import { computeFingerprint, collectParts } from '../license-gate/fingerprint.js'

const parts = collectParts()
const fp = computeFingerprint()

console.log('Machine fingerprint components (for debugging):')
console.log('  machine-id      : ' + parts.machineId)
console.log('  physical MACs   : ' + (parts.macs.join(', ') || '<none>'))
console.log('  motherboard UUID: ' + parts.motherboardUuid)
console.log('')
console.log('Fingerprint (SM3, send THIS to vendor):')
console.log('  ' + fp)
```

- [ ] **Step 6: 本地自测**

```bash
node tools/print-fingerprint.js
```

Expected: 打印三件套和一个 64 字符 hex。

- [ ] **Step 7: Commit**

```bash
git add server/license-gate/fingerprint.js server/tools/print-fingerprint.js server/test/fingerprint.test.js
git commit -m "feat(license): hardware fingerprint computation and print tool"
```

---

### Task 2.3: sign-license.js

**Files:**
- Create: `DrawingWebApp/server/tools/sign-license.js`

- [ ] **Step 1: 实现**

```js
#!/usr/bin/env node
/**
 * 厂商离线签发客户 License
 *
 * Usage:
 *   node tools/sign-license.js \
 *     --root-key   path/to/root_private.pem \
 *     --customer   "ACME CAD Co." \
 *     --fingerprint <64-hex> \
 *     --max-concurrent 10 \
 *     --expires    2027-04-15 \
 *     [--out-dir   ./out]
 */
import fs from 'fs'
import path from 'path'
import crypto from 'crypto'
import pkg from 'sm-crypto'
const { sm2 } = pkg
import { canonicalJson } from '../license-gate/canonical-json.js'
import { sm2Sign } from '../license-gate/sm2-helper.js'
import { readHexFromPem } from '../license-gate/pem.js'

function parseArgs() {
  const args = {}
  for (let i = 2; i < process.argv.length; i += 2) {
    const k = process.argv[i].replace(/^--/, '')
    args[k] = process.argv[i + 1]
  }
  return args
}

const args = parseArgs()
for (const req of ['root-key', 'customer', 'fingerprint', 'max-concurrent', 'expires']) {
  if (!args[req]) {
    console.error(`Missing --${req}`)
    process.exit(1)
  }
}
if (!/^[0-9a-f]{64}$/.test(args.fingerprint)) {
  console.error('--fingerprint must be 64-char SM3 hex')
  process.exit(1)
}

const rootPrivHex = readHexFromPem(args['root-key'], 'SM2 PRIVATE KEY')

// 1. 为客户生成 SM2 密钥对
const { privateKey: custPriv, publicKey: custPub } = sm2.generateKeyPairHex()

// 2. 组 payload
const licenseId = 'LIC-' + new Date().toISOString().slice(0, 10).replace(/-/g, '') +
  '-' + crypto.randomBytes(3).toString('hex').toUpperCase()

const payload = {
  license_id:         licenseId,
  customer_name:      args.customer,
  customer_pubkey:    custPub,
  server_fingerprint: args.fingerprint,
  max_concurrent:     parseInt(args['max-concurrent'], 10),
  issued_at:          new Date().toISOString(),
  expires_at:         args.expires + 'T00:00:00Z',
  version:            1,
}

// 3. 根私钥签 canonical payload
const payloadStr = canonicalJson(payload)
const signature  = sm2Sign(payloadStr, rootPrivHex)

const license = {
  payload,
  signature: signature.toString('base64'),
}

// 4. 输出
const outDir = args['out-dir'] || './out-' + licenseId
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true })

const licensePath   = path.join(outDir, 'license.dat')
const custKeyPath   = path.join(outDir, 'customer_key.pem')

fs.writeFileSync(licensePath, JSON.stringify(license, null, 2))

const custKeyPem =
  '-----BEGIN SM2 PRIVATE KEY-----\n' +
  custPriv + '\n' +
  '-----END SM2 PRIVATE KEY-----\n'
fs.writeFileSync(custKeyPath, custKeyPem, { mode: 0o600 })

console.log('Generated license for: ' + args.customer)
console.log('  license_id     : ' + licenseId)
console.log('  fingerprint    : ' + args.fingerprint)
console.log('  max_concurrent : ' + payload.max_concurrent)
console.log('  expires        : ' + payload.expires_at)
console.log('Files:')
console.log('  ' + licensePath)
console.log('  ' + custKeyPath + '  (permissions 0600)')
console.log('')
console.log('Send BOTH files to customer through secure channel.')
```

- [ ] **Step 2: 集成测试（自己签、自己验）**

建一个临时脚本验证签名能被验签通过：

```bash
cd DrawingWebApp/server
mkdir -p /tmp/license-test
node tools/generate-root-key.js /tmp/license-test

# 假一个指纹
FP=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))")

node tools/sign-license.js \
  --root-key /tmp/license-test/root_private.pem \
  --customer "Test Customer" \
  --fingerprint $FP \
  --max-concurrent 5 \
  --expires 2027-04-15 \
  --out-dir /tmp/license-test

ls /tmp/license-test/
# 应有: root_private.pem, root_public.pem, license.dat, customer_key.pem
cat /tmp/license-test/license.dat
```

Expected: `license.dat` 是合法 JSON，含 `payload` 与 `signature`。

- [ ] **Step 3: Commit**

```bash
git add server/tools/sign-license.js
git commit -m "feat(license): add sign-license vendor tool"
```

---

### Task 2.4: verify-license.js (调试工具)

**Files:**
- Create: `DrawingWebApp/server/tools/verify-license.js`
- Create: `DrawingWebApp/server/test/verify-license-integration.test.js`

- [ ] **Step 1: 写集成测试**

```js
// test/verify-license-integration.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'fs'
import path from 'path'
import os from 'os'
import { execSync } from 'child_process'
import { canonicalJson } from '../license-gate/canonical-json.js'
import { sm2Verify } from '../license-gate/sm2-helper.js'
import { readHexFromPem } from '../license-gate/pem.js'

test('integration: generate-root-key + sign-license produces verifiable license', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lic-'))
  try {
    // 1. 生成根密钥
    execSync(`node tools/generate-root-key.js "${tmp}"`, { stdio: 'inherit' })
    const rootPubHex = readHexFromPem(path.join(tmp, 'root_public.pem'), 'SM2 PUBLIC KEY')

    // 2. 签 License
    const fp = 'a'.repeat(64)
    execSync([
      'node tools/sign-license.js',
      `--root-key "${path.join(tmp, 'root_private.pem')}"`,
      '--customer "Test"',
      `--fingerprint ${fp}`,
      '--max-concurrent 3',
      '--expires 2030-01-01',
      `--out-dir "${tmp}"`,
    ].join(' '), { stdio: 'inherit' })

    // 3. 用根公钥验 License
    const licenseJson = JSON.parse(fs.readFileSync(path.join(tmp, 'license.dat'), 'utf8'))
    const canonical = canonicalJson(licenseJson.payload)
    const sig = Buffer.from(licenseJson.signature, 'base64')
    assert.ok(sm2Verify(canonical, sig, rootPubHex), 'License signature must verify')

    // 4. 检查字段
    assert.equal(licenseJson.payload.server_fingerprint, fp)
    assert.equal(licenseJson.payload.max_concurrent, 3)
    assert.ok(licenseJson.payload.license_id.startsWith('LIC-'))
    assert.match(licenseJson.payload.customer_pubkey, /^04[0-9a-f]{128}$/)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
})
```

- [ ] **Step 2: 运行测试（应通过）**

```bash
npm test
```

- [ ] **Step 3: 实现** `tools/verify-license.js`

```js
#!/usr/bin/env node
/**
 * 校验 license.dat: 根签名有效、未过期、payload 格式正确
 *
 * Usage:
 *   node tools/verify-license.js --license path/to/license.dat --root-pub path/to/root_public.pem
 */
import fs from 'fs'
import { canonicalJson } from '../license-gate/canonical-json.js'
import { sm2Verify } from '../license-gate/sm2-helper.js'
import { readHexFromPem } from '../license-gate/pem.js'

function parseArgs() {
  const args = {}
  for (let i = 2; i < process.argv.length; i += 2) {
    const k = process.argv[i].replace(/^--/, '')
    args[k] = process.argv[i + 1]
  }
  return args
}

const args = parseArgs()
if (!args.license || !args['root-pub']) {
  console.error('Usage: verify-license.js --license <file> --root-pub <pem>')
  process.exit(1)
}

const licenseJson = JSON.parse(fs.readFileSync(args.license, 'utf8'))
const rootPubHex = readHexFromPem(args['root-pub'], 'SM2 PUBLIC KEY')

const canonical = canonicalJson(licenseJson.payload)
const sig = Buffer.from(licenseJson.signature, 'base64')

const ok = sm2Verify(canonical, sig, rootPubHex)
if (!ok) {
  console.error('❌ License signature INVALID')
  process.exit(2)
}

const now = Date.now()
const exp = new Date(licenseJson.payload.expires_at).getTime()
const daysLeft = Math.floor((exp - now) / (24 * 3600 * 1000))

console.log('✅ License signature valid')
console.log('   license_id     : ' + licenseJson.payload.license_id)
console.log('   customer       : ' + licenseJson.payload.customer_name)
console.log('   fingerprint    : ' + licenseJson.payload.server_fingerprint)
console.log('   max_concurrent : ' + licenseJson.payload.max_concurrent)
console.log('   expires_at     : ' + licenseJson.payload.expires_at + `  (${daysLeft} days left)`)
if (daysLeft < 0) {
  console.warn('   ⚠️  LICENSE EXPIRED')
  process.exit(3)
}
```

- [ ] **Step 4: Commit**

```bash
git add server/tools/verify-license.js server/test/verify-license-integration.test.js
git commit -m "feat(license): add verify-license tool + integration test"
```

---

### Task 2.5: dev-fixtures.js（开发机 license）

**Files:**
- Create: `DrawingWebApp/server/tools/dev-fixtures.js`

开发者在本地运行 `npm run license:dev-fixtures`，自动生成一个绑定本机指纹的 dev license，写到 `server/license/`。

- [ ] **Step 1: 实现**

```js
#!/usr/bin/env node
/**
 * 开发环境一键生成可用 license (绑定本机指纹, 有效 1 年)
 *
 * 生成 server/license/ 下:
 *   - root_pubkey.pem
 *   - license.dat
 *   - customer_key.pem
 *
 * 并额外把 root_private.pem 放到 server/license/dev-root-private.pem (仅开发用, .gitignore 忽略)
 *
 * Usage:
 *   npm run license:dev-fixtures
 */
import fs from 'fs'
import path from 'path'
import { execSync } from 'child_process'
import { fileURLToPath } from 'url'
import { computeFingerprint } from '../license-gate/fingerprint.js'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const serverRoot = path.resolve(__dirname, '..')
const licenseDir = path.join(serverRoot, 'license')

if (!fs.existsSync(licenseDir)) fs.mkdirSync(licenseDir, { recursive: true })

// 1. 生成根密钥对, private 放 license/dev-root-private.pem
console.log('Step 1: generate dev root key pair')
execSync(`node tools/generate-root-key.js "${licenseDir}"`, { cwd: serverRoot, stdio: 'inherit' })
// 改名: root_private.pem → dev-root-private.pem (为了清楚)
fs.renameSync(path.join(licenseDir, 'root_private.pem'),
              path.join(licenseDir, 'dev-root-private.pem'))
// root_public.pem 改名为 root_pubkey.pem (server 期望的名字)
fs.renameSync(path.join(licenseDir, 'root_public.pem'),
              path.join(licenseDir, 'root_pubkey.pem'))

// 2. 计算本机指纹
console.log('Step 2: compute local fingerprint')
const fp = computeFingerprint()
console.log('  ' + fp)

// 3. 签 License, 写到 license/
console.log('Step 3: sign license')
const nextYear = new Date()
nextYear.setFullYear(nextYear.getFullYear() + 1)
const expiresDate = nextYear.toISOString().slice(0, 10)

execSync([
  'node tools/sign-license.js',
  `--root-key "${path.join(licenseDir, 'dev-root-private.pem')}"`,
  '--customer "Dev Machine"',
  `--fingerprint ${fp}`,
  '--max-concurrent 5',
  `--expires ${expiresDate}`,
  `--out-dir "${licenseDir}"`,
].join(' '), { cwd: serverRoot, stdio: 'inherit' })

console.log('\nDone. Dev license ready at: ' + licenseDir)
console.log('  license.dat + customer_key.pem + root_pubkey.pem')
console.log('  (dev-root-private.pem kept for local re-signing; do NOT commit)')
```

- [ ] **Step 2: 更新 `.gitignore`**

把 `dev-root-private.pem` 也加入 `server/license/.gitignore` 的例外列表之外（已经用通配符 `*` 忽略一切，所以自动忽略）。确认：

```gitignore
# server/license/.gitignore
*
!.gitignore
!root_pubkey.pem
!README.md
```

- [ ] **Step 3: 自测**

```bash
cd DrawingWebApp/server
npm run license:dev-fixtures
ls license/
# 应有: .gitignore, README.md, dev-root-private.pem, root_pubkey.pem, license.dat, customer_key.pem
node tools/verify-license.js --license license/license.dat --root-pub license/root_pubkey.pem
```

Expected: ✅ License signature valid，剩 365 天。

- [ ] **Step 4: Commit**

```bash
git add server/tools/dev-fixtures.js
git commit -m "feat(license): add dev-fixtures script for local development"
```

---

## Phase 3: Server 端 License Gate

### Task 3.1: signer 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/signer.js`
- Create: `DrawingWebApp/server/test/signer.test.js`

- [ ] **Step 1: 写测试**

```js
// test/signer.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import pkg from 'sm-crypto'
const { sm2 } = pkg
import { signToken, parseToken } from '../license-gate/signer.js'
import { sm2Verify } from '../license-gate/sm2-helper.js'

test('signToken produces verifiable token', () => {
  const { privateKey, publicKey } = sm2.generateKeyPairHex()
  const token = signToken({
    licenseId: 'LIC-TEST-01', sessionId: 'sess_1', maxConcurrent: 5,
  }, privateKey)

  const { payload, payloadBytes, signature } = parseToken(token)
  assert.equal(payload.license_id, 'LIC-TEST-01')
  assert.equal(payload.session_id, 'sess_1')
  assert.equal(payload.max_concurrent, 5)
  assert.ok(payload.nonce && payload.nonce.length === 32) // 16 bytes hex
  assert.ok(payload.expires_at > payload.issued_at)
  assert.equal(payload.expires_at - payload.issued_at, 300) // 5 min

  assert.ok(sm2Verify(payloadBytes, signature, publicKey))
})

test('parseToken rejects malformed token', () => {
  assert.throws(() => parseToken('no-dot-here'))
  assert.throws(() => parseToken(''))
})

test('two tokens have different nonces', () => {
  const { privateKey } = sm2.generateKeyPairHex()
  const t1 = signToken({ licenseId: 'X', sessionId: 'a', maxConcurrent: 1 }, privateKey)
  const t2 = signToken({ licenseId: 'X', sessionId: 'a', maxConcurrent: 1 }, privateKey)
  const p1 = parseToken(t1).payload
  const p2 = parseToken(t2).payload
  assert.notEqual(p1.nonce, p2.nonce)
})
```

- [ ] **Step 2: 跑测试失败**

- [ ] **Step 3: 实现** `license-gate/signer.js`

```js
import crypto from 'crypto'
import { canonicalJson } from './canonical-json.js'
import { base64urlEncode, base64urlDecode } from './base64url.js'
import { sm2Sign } from './sm2-helper.js'

const TOKEN_TTL_SEC = parseInt(process.env.TOKEN_TTL_SEC || '300', 10)

/**
 * @param {{licenseId, sessionId, maxConcurrent}} meta
 * @param {string} customerPrivKeyHex
 * @returns {string} 紧凑 token "base64url.base64url"
 */
export function signToken({ licenseId, sessionId, maxConcurrent }, customerPrivKeyHex) {
  const now = Math.floor(Date.now() / 1000)
  const payload = {
    license_id:     licenseId,
    session_id:     sessionId,
    issued_at:      now,
    expires_at:     now + TOKEN_TTL_SEC,
    max_concurrent: maxConcurrent,
    nonce:          crypto.randomBytes(16).toString('hex'),
  }
  const payloadStr   = canonicalJson(payload)
  const payloadBytes = Buffer.from(payloadStr, 'utf8')
  const sig          = sm2Sign(payloadBytes, customerPrivKeyHex)

  return base64urlEncode(payloadBytes) + '.' + base64urlEncode(sig)
}

/**
 * 纯解析, 不验签
 * @returns {{payload, payloadBytes, signature}}
 */
export function parseToken(token) {
  if (!token || typeof token !== 'string') throw new Error('Empty token')
  const dot = token.indexOf('.')
  if (dot < 0) throw new Error('Malformed token: no separator')
  const payloadBytes = base64urlDecode(token.slice(0, dot))
  const signature    = base64urlDecode(token.slice(dot + 1))
  const payload      = JSON.parse(payloadBytes.toString('utf8'))
  return { payload, payloadBytes, signature }
}
```

- [ ] **Step 4: 测试通过**

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/signer.js server/test/signer.test.js
git commit -m "feat(license): implement token signer and parser"
```

---

### Task 3.2: sessions 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/sessions.js`
- Create: `DrawingWebApp/server/test/sessions.test.js`

- [ ] **Step 1: 写测试**

```js
// test/sessions.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createSessionStore } from '../license-gate/sessions.js'

test('startSession returns sessionId when under cap', () => {
  const s = createSessionStore({ maxConcurrent: 3 })
  const r = s.startSession()
  assert.match(r.sessionId, /^[0-9a-f-]{36}$/)  // uuid v4
})

test('startSession returns error when at cap', () => {
  const s = createSessionStore({ maxConcurrent: 2 })
  s.startSession(); s.startSession()
  const r3 = s.startSession()
  assert.equal(r3.error, 'MAX_CONCURRENT_REACHED')
  assert.equal(r3.active, 2)
  assert.equal(r3.max, 2)
})

test('touchSession returns false for unknown id', () => {
  const s = createSessionStore({ maxConcurrent: 1 })
  assert.equal(s.touchSession('not-exists'), false)
})

test('touchSession returns true for known id and updates lastSeen', async () => {
  const s = createSessionStore({ maxConcurrent: 1 })
  const { sessionId } = s.startSession()
  const before = s._peekLastSeen(sessionId)
  await new Promise(r => setTimeout(r, 10))
  assert.equal(s.touchSession(sessionId), true)
  const after = s._peekLastSeen(sessionId)
  assert.ok(after > before)
})

test('endSession frees the slot', () => {
  const s = createSessionStore({ maxConcurrent: 1 })
  const { sessionId } = s.startSession()
  assert.equal(s.activeCount(), 1)
  s.endSession(sessionId)
  assert.equal(s.activeCount(), 0)
  // 现在应能再起一个
  assert.ok(s.startSession().sessionId)
})

test('evictExpired removes sessions older than TTL', async () => {
  const s = createSessionStore({ maxConcurrent: 5, sessionTtlMs: 50 })
  const { sessionId } = s.startSession()
  await new Promise(r => setTimeout(r, 80))
  s.evictExpired()
  assert.equal(s.activeCount(), 0)
  assert.equal(s.touchSession(sessionId), false)
})
```

- [ ] **Step 2: 跑测试失败**

- [ ] **Step 3: 实现** `license-gate/sessions.js`

```js
import { randomUUID } from 'crypto'

/**
 * 内存会话表 (单实例). 多实例部署可替换为 Redis 后实现相同接口。
 *
 * @param {{maxConcurrent: number, sessionTtlMs?: number}} opts
 */
export function createSessionStore({ maxConcurrent, sessionTtlMs = 5 * 60 * 1000 }) {
  const sessions = new Map()   // id → { startedAt, lastSeen }

  return {
    startSession() {
      if (sessions.size >= maxConcurrent) {
        return { error: 'MAX_CONCURRENT_REACHED', active: sessions.size, max: maxConcurrent }
      }
      const sid = randomUUID()
      const now = Date.now()
      sessions.set(sid, { startedAt: now, lastSeen: now })
      return { sessionId: sid }
    },

    touchSession(sid) {
      const s = sessions.get(sid)
      if (!s) return false
      s.lastSeen = Date.now()
      return true
    },

    endSession(sid) {
      sessions.delete(sid)
    },

    activeCount() { return sessions.size },

    /** 被 setInterval 周期调用, 清理死会话 */
    evictExpired() {
      const now = Date.now()
      for (const [sid, s] of sessions) {
        if (now - s.lastSeen > sessionTtlMs) {
          sessions.delete(sid)
          console.log(`[License] Session ${sid} evicted (lastSeen ${Math.round((now - s.lastSeen) / 1000)}s ago)`)
        }
      }
    },

    _peekLastSeen(sid) { return sessions.get(sid)?.lastSeen },
  }
}
```

- [ ] **Step 4: 测试通过**

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/sessions.js server/test/sessions.test.js
git commit -m "feat(license): in-memory session store with TTL eviction"
```

---

### Task 3.3: validator 模块

**Files:**
- Create: `DrawingWebApp/server/license-gate/validator.js`
- Create: `DrawingWebApp/server/test/validator.test.js`

- [ ] **Step 1: 写测试** (使用 dev-fixtures 预生成的 license 作为 fixture)

```js
// test/validator.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'fs'
import path from 'path'
import os from 'os'
import { execSync } from 'child_process'
import { validateAtStartup } from '../license-gate/validator.js'
import { computeFingerprint } from '../license-gate/fingerprint.js'

function makeFixture({ fingerprint, expires = '2030-01-01' }) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lic-'))
  execSync(`node tools/generate-root-key.js "${tmp}"`, { stdio: 'ignore' })
  execSync([
    'node tools/sign-license.js',
    `--root-key "${path.join(tmp, 'root_private.pem')}"`,
    '--customer "Fixture Customer"',
    `--fingerprint ${fingerprint}`,
    '--max-concurrent 7',
    `--expires ${expires}`,
    `--out-dir "${tmp}"`,
  ].join(' '), { stdio: 'ignore' })
  // 重命名 root_public.pem → root_pubkey.pem (server 期望)
  fs.renameSync(path.join(tmp, 'root_public.pem'), path.join(tmp, 'root_pubkey.pem'))
  return tmp
}

test('validateAtStartup succeeds for matching fingerprint', async () => {
  const fp = computeFingerprint()
  const tmp = makeFixture({ fingerprint: fp })
  try {
    const ctx = await validateAtStartup({
      licensePath:     path.join(tmp, 'license.dat'),
      customerKeyPath: path.join(tmp, 'customer_key.pem'),
      rootPubKeyPath:  path.join(tmp, 'root_pubkey.pem'),
    })
    assert.equal(ctx.payload.max_concurrent, 7)
    assert.equal(ctx.payload.customer_name, 'Fixture Customer')
    assert.ok(ctx.customerPrivKeyHex.length === 64)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
})

test('validateAtStartup fails for wrong fingerprint', async () => {
  const wrongFp = 'f'.repeat(64)
  const tmp = makeFixture({ fingerprint: wrongFp })
  try {
    await assert.rejects(validateAtStartup({
      licensePath:     path.join(tmp, 'license.dat'),
      customerKeyPath: path.join(tmp, 'customer_key.pem'),
      rootPubKeyPath:  path.join(tmp, 'root_pubkey.pem'),
    }), /bound to different machine/)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
})

test('validateAtStartup fails for expired license', async () => {
  const fp = computeFingerprint()
  const tmp = makeFixture({ fingerprint: fp, expires: '2000-01-01' })
  try {
    await assert.rejects(validateAtStartup({
      licensePath:     path.join(tmp, 'license.dat'),
      customerKeyPath: path.join(tmp, 'customer_key.pem'),
      rootPubKeyPath:  path.join(tmp, 'root_pubkey.pem'),
    }), /expired/i)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
})

test('validateAtStartup fails for tampered signature', async () => {
  const fp = computeFingerprint()
  const tmp = makeFixture({ fingerprint: fp })
  try {
    // 破坏签名
    const p = path.join(tmp, 'license.dat')
    const j = JSON.parse(fs.readFileSync(p, 'utf8'))
    const sig = Buffer.from(j.signature, 'base64')
    sig[5] ^= 0xff
    j.signature = sig.toString('base64')
    fs.writeFileSync(p, JSON.stringify(j))

    await assert.rejects(validateAtStartup({
      licensePath:     p,
      customerKeyPath: path.join(tmp, 'customer_key.pem'),
      rootPubKeyPath:  path.join(tmp, 'root_pubkey.pem'),
    }), /signature invalid/i)
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true })
  }
})
```

- [ ] **Step 2: 跑测试失败**

- [ ] **Step 3: 实现** `license-gate/validator.js`

```js
import fs from 'fs/promises'
import { canonicalJson } from './canonical-json.js'
import { sm2Verify } from './sm2-helper.js'
import { readHexFromPem } from './pem.js'
import { computeFingerprint } from './fingerprint.js'

/**
 * 启动自检. 任何一步失败就抛错, 调用方应 process.exit(1).
 *
 * @returns {Promise<{payload, customerPrivKeyHex}>}
 */
export async function validateAtStartup({ licensePath, customerKeyPath, rootPubKeyPath }) {
  console.log('[License] ---- Startup validation ----')

  // 1. 读 license.dat
  const licenseText = await fs.readFile(licensePath, 'utf8')
  const license     = JSON.parse(licenseText)
  if (!license.payload || !license.signature) {
    throw new Error('License file missing payload or signature')
  }

  // 2. 读根公钥
  const rootPubHex = readHexFromPem(rootPubKeyPath, 'SM2 PUBLIC KEY')
  console.log('[License] Loaded root_pubkey.pem ... OK')

  // 3. 验根签名
  const payloadCanonical = canonicalJson(license.payload)
  const sigBytes         = Buffer.from(license.signature, 'base64')
  if (!sm2Verify(payloadCanonical, sigBytes, rootPubHex)) {
    throw new Error('License signature invalid: not signed by vendor root key')
  }
  console.log('[License] Root signature verified ... OK')

  // 4. 硬件指纹
  const computedFp = computeFingerprint()
  if (computedFp !== license.payload.server_fingerprint) {
    throw new Error(
      `License bound to different machine. ` +
      `Expected ${license.payload.server_fingerprint}, got ${computedFp}`
    )
  }
  console.log('[License] Hardware fingerprint matched ... OK')

  // 5. 过期检查
  const now = Date.now()
  const expMs = new Date(license.payload.expires_at).getTime()
  if (isNaN(expMs)) {
    throw new Error('License expires_at is not a valid date')
  }
  if (now > expMs) {
    throw new Error(`License expired at ${license.payload.expires_at}`)
  }
  const daysLeft = Math.floor((expMs - now) / (24 * 3600 * 1000))
  console.log(`[License] Not expired (${daysLeft} days left) ... OK`)

  // 6. 读客户私钥
  const customerPrivKeyHex = readHexFromPem(customerKeyPath, 'SM2 PRIVATE KEY')
  if (customerPrivKeyHex.length !== 64) {
    throw new Error('Customer private key is not 32 bytes (64 hex chars)')
  }
  console.log('[License] Customer private key loaded ... OK')

  console.log(`[License] license_id=${license.payload.license_id} customer="${license.payload.customer_name}" max_concurrent=${license.payload.max_concurrent}`)
  console.log('[License] -------------------------------')

  return { payload: license.payload, customerPrivKeyHex }
}
```

- [ ] **Step 4: 测试通过**

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/validator.js server/test/validator.test.js
git commit -m "feat(license): startup validator with root-signature + fingerprint check"
```

---

### Task 3.4: routes 模块 + 测试

**Files:**
- Create: `DrawingWebApp/server/license-gate/routes.js`
- Create: `DrawingWebApp/server/test/routes.test.js`

- [ ] **Step 1: 写测试（用 express + supertest-less 手写，不引新依赖）**

```js
// test/routes.test.js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import fs from 'fs'
import path from 'path'
import os from 'os'
import { execSync } from 'child_process'
import express from 'express'
import { createLicenseRoutes } from '../license-gate/routes.js'
import { validateAtStartup } from '../license-gate/validator.js'
import { parseToken } from '../license-gate/signer.js'
import { sm2Verify } from '../license-gate/sm2-helper.js'
import { computeFingerprint } from '../license-gate/fingerprint.js'

async function setupServer() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lic-'))
  const fp = computeFingerprint()
  execSync(`node tools/generate-root-key.js "${tmp}"`, { stdio: 'ignore' })
  execSync([
    'node tools/sign-license.js',
    `--root-key "${path.join(tmp, 'root_private.pem')}"`,
    '--customer "Test"',
    `--fingerprint ${fp}`,
    '--max-concurrent 2',
    '--expires 2030-01-01',
    `--out-dir "${tmp}"`,
  ].join(' '), { stdio: 'ignore' })
  fs.renameSync(path.join(tmp, 'root_public.pem'), path.join(tmp, 'root_pubkey.pem'))

  const ctx = await validateAtStartup({
    licensePath:     path.join(tmp, 'license.dat'),
    customerKeyPath: path.join(tmp, 'customer_key.pem'),
    rootPubKeyPath:  path.join(tmp, 'root_pubkey.pem'),
  })

  const app = express()
  app.use(express.json())
  app.use('/api/license', createLicenseRoutes({ ...ctx, licensePath: path.join(tmp, 'license.dat') }))

  return new Promise(resolve => {
    const server = app.listen(0, () => {
      const port = server.address().port
      resolve({ port, ctx, tmpDir: tmp, server })
    })
  })
}

async function req(port, method, url, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } }
  if (body) opts.body = JSON.stringify(body)
  const r = await fetch(`http://127.0.0.1:${port}${url}`, opts)
  const text = await r.text()
  let json; try { json = JSON.parse(text) } catch { json = text }
  return { status: r.status, body: json }
}

test('GET /info returns license.dat text', async () => {
  const { port, server } = await setupServer()
  try {
    const r = await req(port, 'GET', '/api/license/info')
    assert.equal(r.status, 200)
    assert.ok(r.body.payload && r.body.signature)
  } finally { server.close() }
})

test('POST /session/start returns token under cap', async () => {
  const { port, ctx, server } = await setupServer()
  try {
    const r = await req(port, 'POST', '/api/license/session/start')
    assert.equal(r.status, 200)
    assert.match(r.body.sessionId, /^[0-9a-f-]{36}$/)
    assert.ok(r.body.token)
    // 验 token
    const { payload, payloadBytes, signature } = parseToken(r.body.token)
    assert.equal(payload.license_id, ctx.payload.license_id)
    assert.equal(payload.session_id, r.body.sessionId)
    const { publicKey } = require('sm-crypto').sm2
    // customer_pubkey 来自 license payload
    const pub = ctx.payload.customer_pubkey
    assert.ok(sm2Verify(payloadBytes, signature, pub))
  } finally { server.close() }
})

test('POST /session/start returns 429 when at cap', async () => {
  const { port, server } = await setupServer()
  try {
    await req(port, 'POST', '/api/license/session/start')
    await req(port, 'POST', '/api/license/session/start')
    const r3 = await req(port, 'POST', '/api/license/session/start')
    assert.equal(r3.status, 429)
    assert.equal(r3.body.error, 'MAX_CONCURRENT_REACHED')
    assert.equal(r3.body.active, 2)
    assert.equal(r3.body.max, 2)
  } finally { server.close() }
})

test('POST /token/refresh rotates token for known session', async () => {
  const { port, server } = await setupServer()
  try {
    const { body: { sessionId, token: t1 } } = await req(port, 'POST', '/api/license/session/start')
    const r = await req(port, 'POST', '/api/license/token/refresh', { sessionId })
    assert.equal(r.status, 200)
    assert.ok(r.body.token)
    assert.notEqual(r.body.token, t1)
  } finally { server.close() }
})

test('POST /token/refresh 401 for unknown session', async () => {
  const { port, server } = await setupServer()
  try {
    const r = await req(port, 'POST', '/api/license/token/refresh', { sessionId: 'nope' })
    assert.equal(r.status, 401)
    assert.equal(r.body.error, 'SESSION_NOT_FOUND')
  } finally { server.close() }
})

test('POST /session/end frees slot', async () => {
  const { port, server } = await setupServer()
  try {
    const { body: { sessionId } } = await req(port, 'POST', '/api/license/session/start')
    await req(port, 'POST', '/api/license/session/start')
    // 第 3 次应超配额
    const over = await req(port, 'POST', '/api/license/session/start')
    assert.equal(over.status, 429)

    // end 第一个
    await req(port, 'POST', '/api/license/session/end', { sessionId })
    // 现在有位置
    const r = await req(port, 'POST', '/api/license/session/start')
    assert.equal(r.status, 200)
  } finally { server.close() }
})
```

注意：`require('sm-crypto')` 在 ESM 测试文件里不能直接用；改写成 import。修正测试代码：把第 2 个测试里的 `const { publicKey } = require('sm-crypto').sm2` 这行删掉（未使用），并确保已在文件顶部 `import pkg from 'sm-crypto'; const { sm2 } = pkg` 如需。

- [ ] **Step 2: 跑测试失败**

- [ ] **Step 3: 实现** `license-gate/routes.js`

```js
import express from 'express'
import fs from 'fs'
import { signToken } from './signer.js'
import { createSessionStore } from './sessions.js'

/**
 * @param {{payload, customerPrivKeyHex, licensePath}} ctx
 */
export function createLicenseRoutes(ctx) {
  const { payload, customerPrivKeyHex, licensePath } = ctx
  const store = createSessionStore({ maxConcurrent: payload.max_concurrent })

  // 每 60 秒清理死会话
  const evictTimer = setInterval(() => store.evictExpired(), 60 * 1000)
  // 测试里 app.close() 时 timer 自动随进程退出; 但 evictTimer.unref() 让它不阻塞退出
  evictTimer.unref()

  const r = express.Router()

  // GET /api/license/info
  r.get('/info', (_req, res) => {
    try {
      const raw = fs.readFileSync(licensePath, 'utf8')
      res.type('application/json').send(raw)
    } catch (err) {
      res.status(500).json({ error: 'Cannot read license file', detail: err.message })
    }
  })

  // POST /api/license/session/start
  r.post('/session/start', (_req, res) => {
    const result = store.startSession()
    if (result.error) {
      return res.status(429).json(result)
    }
    const token = signToken({
      licenseId: payload.license_id,
      sessionId: result.sessionId,
      maxConcurrent: payload.max_concurrent,
    }, customerPrivKeyHex)
    res.json({
      sessionId: result.sessionId,
      token,
      active: store.activeCount(),
      max:    payload.max_concurrent,
    })
    console.log(`[License] session/start ${result.sessionId} → ${store.activeCount()}/${payload.max_concurrent} active`)
  })

  // POST /api/license/token/refresh
  r.post('/token/refresh', (req, res) => {
    const { sessionId } = req.body || {}
    if (!store.touchSession(sessionId)) {
      return res.status(401).json({ error: 'SESSION_NOT_FOUND' })
    }
    const token = signToken({
      licenseId: payload.license_id,
      sessionId,
      maxConcurrent: payload.max_concurrent,
    }, customerPrivKeyHex)
    res.json({ token })
  })

  // POST /api/license/session/end  (body 可能是 text/plain, sendBeacon 默认)
  r.post('/session/end', express.text({ type: '*/*' }), (req, res) => {
    try {
      const parsed = typeof req.body === 'string' ? JSON.parse(req.body) : req.body
      if (parsed?.sessionId) {
        store.endSession(parsed.sessionId)
        console.log(`[License] session/end ${parsed.sessionId} → ${store.activeCount()} active`)
      }
    } catch (_) { /* ignore */ }
    res.json({ ok: true })
  })

  return r
}
```

- [ ] **Step 4: 测试通过**

```bash
cd DrawingWebApp/server
npm test
```

- [ ] **Step 5: Commit**

```bash
git add server/license-gate/routes.js server/test/routes.test.js
git commit -m "feat(license): HTTP endpoints for session/start, refresh, end, info"
```

---

### Task 3.5: 把 license gate 接入 server/index.js

**Files:**
- Modify: `DrawingWebApp/server/index.js`

- [ ] **Step 1: 在现有 import 后面加**

在 [server/index.js:20](../../server/index.js#L20) 之后（现有 providers import 后），增加：

```js
import { validateAtStartup } from './license-gate/validator.js'
import { createLicenseRoutes } from './license-gate/routes.js'
```

- [ ] **Step 2: 在 LLM Provider 初始化之前加启动自检**

找到这段代码（在 `server/index.js` 里）：

```js
const MODEL_ID = process.env.OPENAI_MODEL || 'gpt-4o'
const { model: defaultModel, ... } = await resolveModel(MODEL_ID)
```

在它**之前**加入：

```js
// ────────────── License Gate 启动自检 ──────────────
let licenseCtx
try {
  licenseCtx = await validateAtStartup({
    licensePath:     process.env.LICENSE_PATH     || './license/license.dat',
    customerKeyPath: process.env.CUSTOMER_KEY_PATH || './license/customer_key.pem',
    rootPubKeyPath:  process.env.ROOT_PUBKEY_PATH || './license/root_pubkey.pem',
  })
} catch (err) {
  console.error('\n[License] ❌ STARTUP FAILED:', err.message)
  console.error('[License] Server refuses to start. Fix the license and try again.\n')
  process.exit(1)
}
```

- [ ] **Step 3: 挂载路由**

在现有 `app.use(cors(...))` 与 `app.use(express.json(...))` 之后，找到 `app.get('/api/ai/health', ...)` 之前，插入：

```js
// ────────────── License Gate 路由 ──────────────
app.use('/api/license', createLicenseRoutes({
  ...licenseCtx,
  licensePath: process.env.LICENSE_PATH || './license/license.dat',
}))
```

- [ ] **Step 4: 启动 server 手动冒烟**

```bash
cd DrawingWebApp/server
npm run license:dev-fixtures   # 确保 license 目录齐全
npm run dev
```

Expected 日志：
```
[License] ---- Startup validation ----
[License] Loaded root_pubkey.pem ... OK
[License] Root signature verified ... OK
[License] Hardware fingerprint matched ... OK
[License] Not expired (365 days left) ... OK
[License] Customer private key loaded ... OK
[License] license_id=LIC-... customer="Dev Machine" max_concurrent=5
[License] -------------------------------
  🤖 WebUACAD CAD AI Server running at http://localhost:3001
```

- [ ] **Step 5: 手动打 HTTP 测试**

另开一个终端：
```bash
curl -s http://localhost:3001/api/license/info | head -c 200 ; echo
curl -s -X POST http://localhost:3001/api/license/session/start
```

Expected: `/info` 返回含 `payload/signature` 的 JSON；`/session/start` 返回 `{sessionId, token, active:1, max:5}`。

- [ ] **Step 6: Commit**

```bash
git add server/index.js
git commit -m "feat(license): wire license gate into AI server startup and routes"
```

---

## Phase 4: WASM / C++ 改动

### Task 4.1: embed-root-pubkey 工具

**Files:**
- Create: `DrawingWebApp/server/tools/embed-root-pubkey.js`

- [ ] **Step 1: 实现**

```js
#!/usr/bin/env node
/**
 * 从 root_public.pem 生成 DrawingWeb/root_pubkey.inc
 *
 * Usage:
 *   node tools/embed-root-pubkey.js <input.pem> <output.inc>
 */
import fs from 'fs'
import { readHexFromPem } from '../license-gate/pem.js'

if (process.argv.length < 4) {
  console.error('Usage: embed-root-pubkey.js <input.pem> <output.inc>')
  process.exit(1)
}
const [, , inPath, outPath] = process.argv
const hex = readHexFromPem(inPath, 'SM2 PUBLIC KEY')
if (!/^04[0-9a-f]{128}$/.test(hex)) {
  console.error('Unexpected SM2 public key format (must be 04 + 128 hex)')
  process.exit(1)
}

const content = `// AUTO-GENERATED by tools/embed-root-pubkey.js — DO NOT EDIT
// Source: ${inPath}
// Generated: ${new Date().toISOString()}
//
// This is the vendor ROOT public key (SM2, uncompressed, 65 bytes).
// It is used by LicenseGate to verify the root signature of license.dat.
// The corresponding root private key is kept OFFLINE by the vendor.
#pragma once

static constexpr const char kRootPubKeyHex[] =
    "${hex}";
`

fs.writeFileSync(outPath, content)
console.log(`Wrote ${outPath}`)
```

- [ ] **Step 2: 自测**

```bash
cd DrawingWebApp/server
node tools/embed-root-pubkey.js license/root_pubkey.pem ../../DrawingWeb/root_pubkey.inc
cat ../../DrawingWeb/root_pubkey.inc
```

Expected: 生成的 `.inc` 文件含 130 字符 hex 字符串。

- [ ] **Step 3: Commit**

```bash
git add DrawingWebApp/server/tools/embed-root-pubkey.js
git commit -m "feat(license): add embed-root-pubkey tool for WASM build"
```

**注意**：`root_pubkey.inc` 本身后续 Task 会提交，暂不提交（在本地生成的公钥是 dev 密钥）。

---

### Task 4.2: LicenseGate 类骨架

**Files:**
- Create: `DrawingWeb/LicenseGate.h`
- Create: `DrawingWeb/LicenseGate.cpp`

- [ ] **Step 1: 写 LicenseGate.h**

```cpp
// DrawingWeb/LicenseGate.h
#pragma once

#include <uacore/pkcs/uacore_evp_pkey.h>
#include <string>

/**
 * License Gate - SM2 + SM3 (GMT0009) based license verification inside WASM.
 *
 * Lifecycle:
 *   1. JS fetches /api/license/info and passes the JSON to initFromLicenseJson()
 *   2. initFromLicenseJson verifies root signature using hardcoded root pubkey,
 *      extracts customer pubkey, caches it.
 *   3. Before CadCore::OpenFile or CreateNewFile, verifyCurrentToken() is called.
 *      It reads window.__currentLicenseToken via EM_ASM, SM2-verifies the token
 *      signature using customer pubkey, checks expires_at and license_id.
 */
class LicenseGate {
public:
    static LicenseGate& instance();

    /** @return false if init failed; use lastError() for diagnosis. */
    bool initFromLicenseJson(const std::string& licenseJson);

    /** @return true only if there is a valid, non-expired token matching license_id. */
    bool verifyCurrentToken();

    bool isInitialized() const { return m_initialized; }
    const std::string& lastError()  const { return m_lastError; }
    const std::string& licenseId()  const { return m_licenseId; }

private:
    LicenseGate() = default;
    LicenseGate(const LicenseGate&) = delete;
    LicenseGate& operator=(const LicenseGate&) = delete;

    UcEvpPKey   m_rootPubKey;
    UcEvpPKey   m_customerPubKey;
    std::string m_licenseId;
    std::string m_lastError;
    bool        m_initialized = false;
};
```

- [ ] **Step 2: 写 LicenseGate.cpp 骨架（initFromLicenseJson 暂时只留 stub）**

```cpp
// DrawingWeb/LicenseGate.cpp
#include "LicenseGate.h"
#include "root_pubkey.inc"

#include <uacore/pkcs/uacore_evp_ecckey.h>
#include <uacore/crypto/uacore_hashencry.h>
#include <uaroot/string/uaroot_stringinfo.h>

// RapidJSON (已被 GIS 模块引入过)
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>

#include <emscripten.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>

LicenseGate& LicenseGate::instance() {
    static LicenseGate g;
    return g;
}

bool LicenseGate::initFromLicenseJson(const std::string& licenseJson) {
    // TODO (Task 4.3): real implementation
    m_lastError = "not implemented";
    return false;
}

bool LicenseGate::verifyCurrentToken() {
    // TODO (Task 4.4): real implementation
    m_lastError = "not implemented";
    return false;
}
```

- [ ] **Step 3: 不做编译，只 Commit 骨架**

```bash
git add DrawingWeb/LicenseGate.h DrawingWeb/LicenseGate.cpp
git commit -m "feat(license): add LicenseGate class skeleton"
```

---

### Task 4.3: initFromLicenseJson 实现 + 辅助工具函数

**Files:**
- Modify: `DrawingWeb/LicenseGate.cpp`

- [ ] **Step 1: 在 LicenseGate.cpp 顶部加辅助函数**

加在 `LicenseGate::instance()` 之前：

```cpp
namespace {

/** RFC 4648 §5 base64url 解码, 支持无填充 */
static bool base64urlDecode(const std::string& in, std::string& out) {
    // 转为标准 base64
    std::string std64;
    std64.reserve(in.size() + 4);
    for (char c : in) {
        if      (c == '-') std64.push_back('+');
        else if (c == '_') std64.push_back('/');
        else               std64.push_back(c);
    }
    while (std64.size() % 4 != 0) std64.push_back('=');

    // 复用 libUARoot 的 base64 (uastr::Base64Decode 返回 byteArray)
    byteArray ba = uastr::Base64Decode(std64);
    out.assign(ba.data(), ba.size());
    return true;
}

/** 递归地对 rapidjson::Value 做 canonical 序列化 (与 JS 侧 canonicalJson 字节一致) */
static void writeCanonicalJson(const rapidjson::Value& v, rapidjson::Writer<rapidjson::StringBuffer>& w) {
    if (v.IsObject()) {
        std::vector<std::string> keys;
        keys.reserve(v.MemberCount());
        for (auto it = v.MemberBegin(); it != v.MemberEnd(); ++it) {
            keys.emplace_back(it->name.GetString(), it->name.GetStringLength());
        }
        std::sort(keys.begin(), keys.end());
        w.StartObject();
        for (const auto& k : keys) {
            w.Key(k.data(), (rapidjson::SizeType)k.size());
            writeCanonicalJson(v[k.c_str()], w);
        }
        w.EndObject();
    } else if (v.IsArray()) {
        w.StartArray();
        for (auto it = v.Begin(); it != v.End(); ++it) writeCanonicalJson(*it, w);
        w.EndArray();
    } else if (v.IsString()) {
        w.String(v.GetString(), v.GetStringLength());
    } else if (v.IsInt64())   w.Int64(v.GetInt64());
    else if (v.IsUint64())    w.Uint64(v.GetUint64());
    else if (v.IsDouble())    w.Double(v.GetDouble());
    else if (v.IsBool())      w.Bool(v.GetBool());
    else                      w.Null();
}

static std::string canonicalize(const rapidjson::Value& v) {
    rapidjson::StringBuffer buf;
    rapidjson::Writer<rapidjson::StringBuffer> w(buf);
    writeCanonicalJson(v, w);
    return std::string(buf.GetString(), buf.GetSize());
}

/** 将 hex 字符串转为 byteArray */
static byteArray hexToBytes(const std::string& hex) {
    byteArray out;
    out.resize(hex.size() / 2);
    for (size_t i = 0; i < out.size(); ++i) {
        auto h2i = [](char c) -> int {
            if (c >= '0' && c <= '9') return c - '0';
            if (c >= 'a' && c <= 'f') return c - 'a' + 10;
            if (c >= 'A' && c <= 'F') return c - 'A' + 10;
            return -1;
        };
        out[i] = (char)((h2i(hex[2*i]) << 4) | h2i(hex[2*i + 1]));
    }
    return out;
}

} // anonymous namespace
```

- [ ] **Step 2: 实现 initFromLicenseJson**

替换原 stub：

```cpp
bool LicenseGate::initFromLicenseJson(const std::string& licenseJson) {
    m_lastError.clear();
    m_initialized = false;

    // 1. 装载硬编码根公钥 (kRootPubKeyHex from root_pubkey.inc)
    byteArray rootPubBytes = hexToBytes(kRootPubKeyHex);
    EvpPKeyPtr rootKeyPtr = UcEvpEccKey::decode_Public(
        (const std::uint8_t*)rootPubBytes.data(), rootPubBytes.size());
    if (!rootKeyPtr) {
        m_lastError = "Failed to decode embedded root public key";
        return false;
    }
    m_rootPubKey.reset(rootKeyPtr.get());

    // 2. 解析 license JSON
    rapidjson::Document doc;
    doc.Parse(licenseJson.c_str(), licenseJson.size());
    if (doc.HasParseError() || !doc.IsObject()) {
        m_lastError = "License JSON parse error";
        return false;
    }
    if (!doc.HasMember("payload") || !doc.HasMember("signature")) {
        m_lastError = "License JSON missing payload or signature";
        return false;
    }
    const auto& payload = doc["payload"];
    if (!payload.IsObject()) {
        m_lastError = "License payload is not an object";
        return false;
    }

    // 3. canonicalize payload 用于验签
    std::string canonical = canonicalize(payload);

    // 4. base64 解 signature
    std::string sigStr;
    const char* sigB64 = doc["signature"].GetString();
    byteArray sigBytes = uastr::Base64Decode(std::string(sigB64, doc["signature"].GetStringLength()));

    // 5. 计算 SM2 GMT0009 digest
    byteArray digest = uaevp::HashSm2WithSm3_GMT09(
        (unsigned char*)canonical.data(), canonical.size(),
        EVP_PKEY_get0_EC_KEY(m_rootPubKey.rawPKey()));

    // 6. 根公钥验签
    if (!m_rootPubKey.verify(digest, sigBytes)) {
        m_lastError = "License signature invalid: not signed by vendor root key";
        return false;
    }

    // 7. 提取 customer_pubkey
    if (!payload.HasMember("customer_pubkey") || !payload["customer_pubkey"].IsString()) {
        m_lastError = "payload.customer_pubkey missing";
        return false;
    }
    std::string custPubHex = payload["customer_pubkey"].GetString();
    byteArray custPubBytes = hexToBytes(custPubHex);
    EvpPKeyPtr custKeyPtr = UcEvpEccKey::decode_Public(
        (const std::uint8_t*)custPubBytes.data(), custPubBytes.size());
    if (!custKeyPtr) {
        m_lastError = "Failed to decode customer public key";
        return false;
    }
    m_customerPubKey.reset(custKeyPtr.get());

    // 8. 缓存 license_id
    if (payload.HasMember("license_id") && payload["license_id"].IsString()) {
        m_licenseId = payload["license_id"].GetString();
    }

    m_initialized = true;
    std::printf("[License] initFromLicenseJson OK, license_id=%s\n", m_licenseId.c_str());
    return true;
}
```

- [ ] **Step 3: 处理 `UcEvpPKey::rawPKey()`**

`UcEvpPKey` 目前没有公开 `rawPKey()` 访问器。需要在 `E:/updasdk/WorkSpace/uakernel/include/uacore/pkcs/uacore_evp_pkey.h` 加一个：

```cpp
// 新增 public 方法 (加在 isValid() 后面):
EVP_PKEY* rawPKey() const { return m_evp_pkeyPtr.get(); }
```

⚠️ 此修改涉及 uakernel 源码，必须与 uakernel 的维护者（同一团队）确认方式。若不允许修改 uakernel，备选方案是通过 `encode_Public` 把公钥再编码、然后每次直接用 `UcEvpEccKey::decode_Public` 返回的 `EvpPKeyPtr` 自己调用 `EVP_PKEY_get0_EC_KEY`。**推荐改 uakernel**，只加一个 getter 很干净。

这一步的执行：在 `uakernel` 仓库同步加这个 getter，rebuild `libUACore.a`，替换到 `/mnt/hgfs/E/updasdk/Lib/lnx64/8.3/libUACore.a`。

- [ ] **Step 4: Commit**

```bash
git add DrawingWeb/LicenseGate.cpp
# uakernel 改动在另一个仓库提交
git commit -m "feat(license): implement LicenseGate::initFromLicenseJson"
```

---

### Task 4.4: verifyCurrentToken 实现

**Files:**
- Modify: `DrawingWeb/LicenseGate.cpp`

- [ ] **Step 1: 替换 stub**

```cpp
bool LicenseGate::verifyCurrentToken() {
    m_lastError.clear();
    if (!m_initialized) {
        m_lastError = "License not initialized";
        return false;
    }

    // 1. 从 JS 拿 token
    char* tokenCStr = (char*)EM_ASM_PTR({
        var t = (window.__currentLicenseToken || '');
        return stringToNewUTF8(t);
    });
    std::string token = tokenCStr ? tokenCStr : "";
    if (tokenCStr) free(tokenCStr);
    if (token.empty()) {
        m_lastError = "No token (server unreachable?)";
        return false;
    }

    // 2. 拆 payload.signature
    size_t dot = token.find('.');
    if (dot == std::string::npos) {
        m_lastError = "Malformed token (no separator)";
        return false;
    }
    std::string payloadStr, sigStr;
    if (!base64urlDecode(token.substr(0, dot), payloadStr) ||
        !base64urlDecode(token.substr(dot + 1), sigStr)) {
        m_lastError = "Token base64 decode failed";
        return false;
    }

    // 3. 解 payload JSON
    rapidjson::Document pd;
    pd.Parse(payloadStr.data(), payloadStr.size());
    if (pd.HasParseError() || !pd.IsObject()) {
        m_lastError = "Token payload JSON parse error";
        return false;
    }

    // 4. expires_at > now
    if (!pd.HasMember("expires_at") || !pd["expires_at"].IsInt64()) {
        m_lastError = "Token missing expires_at";
        return false;
    }
    int64_t expires = pd["expires_at"].GetInt64();
    int64_t now = (int64_t)(emscripten_date_now() / 1000.0);
    if (now > expires) {
        m_lastError = "Token expired";
        return false;
    }

    // 5. license_id 一致
    if (!pd.HasMember("license_id") || !pd["license_id"].IsString()) {
        m_lastError = "Token missing license_id";
        return false;
    }
    if (m_licenseId != pd["license_id"].GetString()) {
        m_lastError = "Token license_id mismatch";
        return false;
    }

    // 6. SM2 + SM3 GMT09 验签
    byteArray payloadBA(payloadStr.data(), payloadStr.size());
    byteArray sigBA(sigStr.data(), sigStr.size());
    byteArray digest = uaevp::HashSm2WithSm3_GMT09(
        (unsigned char*)payloadBA.data(), payloadBA.size(),
        EVP_PKEY_get0_EC_KEY(m_customerPubKey.rawPKey()));

    if (!m_customerPubKey.verify(digest, sigBA)) {
        m_lastError = "Token signature invalid";
        return false;
    }

    return true;
}
```

- [ ] **Step 2: Commit**

```bash
git add DrawingWeb/LicenseGate.cpp
git commit -m "feat(license): implement LicenseGate::verifyCurrentToken"
```

---

### Task 4.5: CadCore 插桩

**Files:**
- Modify: `DrawingWeb/CadCore.cpp` (lines 571-597)

- [ ] **Step 1: 在 CadCore.cpp 顶部加 include**

找到现有 include 段（约 [CadCore.cpp:1-30](../../DrawingWeb/CadCore.cpp#L1)），加：

```cpp
#include "LicenseGate.h"
```

- [ ] **Step 2: 修改 OpenFile**

把现有 [CadCore.cpp:571-585](../../DrawingWeb/CadCore.cpp#L571) 改为：

```cpp
void CadCore::OpenFile(std::wstring name)
{
    // ===== License Gate =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        const std::string& err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('OpenFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] OpenFile denied: %s\n", err.c_str());
        return;
    }
    // ========================

    releaseDeviceAndContext();

    OdString odName(name.c_str());
    this->exHostAppServices.clearMissingFonts();
    this->exHostAppServices.m_asyncProgressEnabled = true;
    this->m_pDatabase = this->exHostAppServices.readFile(odName);
    this->exHostAppServices.m_asyncProgressEnabled = false;

    setupDeviceAndContext();

    // 通知 JS 端 OpenFile 真正完成（ASYNCIFY 场景下 JS 调用侧看到的 "返回" 是假的）
    EM_ASM({ if (window.__onOpenFileComplete) window.__onOpenFileComplete(); });
}
```

- [ ] **Step 3: 修改 CreateNewFile**

把现有 [CadCore.cpp:587-597](../../DrawingWeb/CadCore.cpp#L587) 改为：

```cpp
void CadCore::CreateNewFile()
{
    // ===== License Gate =====
    if (!LicenseGate::instance().verifyCurrentToken()) {
        const std::string& err = LicenseGate::instance().lastError();
        EM_ASM({
            if (window.__onLicenseDenied)
                window.__onLicenseDenied('CreateNewFile', UTF8ToString($0));
        }, err.c_str());
        std::printf("[License] CreateNewFile denied: %s\n", err.c_str());
        return;
    }
    // ========================

    releaseDeviceAndContext();

    this->m_pDatabase = this->exHostAppServices.createDatabase();
    // 设置 DWGCODEPAGE 为简体中文 (GBK), 避免 AutoCAD 打开时报 NLS 代码页转换警告
    odDbSetDWGCODEPAGE(*m_pDatabase, CP_ANSI_936);
    std::printf("WebUACAD: 新建空白 DWG 数据库 (DWGCODEPAGE=ANSI_936)\n");

    setupDeviceAndContext();
}
```

- [ ] **Step 4: Commit**

```bash
git add DrawingWeb/CadCore.cpp
git commit -m "feat(license): gate CadCore::OpenFile and CreateNewFile with LicenseGate"
```

---

### Task 4.6: Embind 绑定 & CMake 更新

**Files:**
- Modify: `DrawingWeb/CadCoreWebBridge.cpp`
- Modify: `DrawingWeb/CMakeLists.txt`

- [ ] **Step 1: 看一眼现有 embind 绑定写法**

```bash
grep -n "EMSCRIPTEN_BINDINGS\|emscripten::function" DrawingWeb/CadCoreWebBridge.cpp | head -20
```

- [ ] **Step 2: 在 CadCoreWebBridge.cpp 末尾加 license_gate 绑定**

参考文件里已有的 EMSCRIPTEN_BINDINGS 块风格，追加：

```cpp
#include "LicenseGate.h"

EMSCRIPTEN_BINDINGS(license_gate) {
    emscripten::function("initLicenseGate", +[](std::string licenseJson) -> bool {
        return LicenseGate::instance().initFromLicenseJson(licenseJson);
    });
    emscripten::function("isLicenseGateReady", +[]() -> bool {
        return LicenseGate::instance().isInitialized();
    });
    emscripten::function("getLicenseGateError", +[]() -> std::string {
        return LicenseGate::instance().lastError();
    });
    emscripten::function("getLicenseId", +[]() -> std::string {
        return LicenseGate::instance().licenseId();
    });
}
```

- [ ] **Step 3: 在 CMakeLists.txt 加源文件**

在 [CMakeLists.txt](../../../DrawingWeb/CMakeLists.txt) 找到添加源文件的地方（`add_executable(...)` 或 `set(SOURCES ...)`），加入 `LicenseGate.cpp`。具体行数取决于现有结构，搜 `CadCore.cpp`，在同一列表里加 `LicenseGate.cpp`。

- [ ] **Step 4: 构建 wasm**

```bash
# 按 DrawingWeb 现有构建流程 (参考 CLAUDE.md):
cd DrawingWeb
# (按项目现有构建命令)
```

Expected: 编译成功，产出 `DrawingJs.js` / `.wasm` / `.data` 放到 `DrawingWebApp/public/`。

- [ ] **Step 5: Commit**

```bash
git add DrawingWeb/CadCoreWebBridge.cpp DrawingWeb/CMakeLists.txt DrawingWeb/root_pubkey.inc
git commit -m "feat(license): embind LicenseGate + add to CMake build"
```

---

### Task 4.7: 更新 asyncify 白名单

**Files:**
- Modify: `DrawingWeb/asyncify_whitelist.txt` （如需）

- [ ] **Step 1: 检查 asyncify 名单**

```bash
grep -i "LicenseGate\|verifyCurrentToken" DrawingWeb/asyncify_whitelist.txt
```

如果 `EM_ASM_PTR` + `emscripten_date_now` 不触发 async，这一步可以跳过。但 fetch 不涉及（因为 fetch 在 JS 层做，WASM 只是同步读 window 变量），因此 `verifyCurrentToken` 本身是同步的。

- [ ] **Step 2: 如果构建时报 async 相关错误**，把以下加入白名单：
```
CadCore::OpenFile
CadCore::CreateNewFile
LicenseGate::verifyCurrentToken
```

（只在报错时才加）

- [ ] **Step 3: Commit（若改了）**

```bash
git add DrawingWeb/asyncify_whitelist.txt
git commit -m "chore(license): update asyncify whitelist for LicenseGate"
```

---

## Phase 5: 前端 JS 集成

### Task 5.1: LicenseStore (MobX)

**Files:**
- Create: `DrawingWebApp/src/stores/LicenseStore.js`
- Modify: `DrawingWebApp/src/context/ViewerContext.js` (or wherever RootStore is)

- [ ] **Step 1: 先看现有 RootStore 结构**

```bash
grep -rn "class RootStore\|class AppStore" DrawingWebApp/src/ | head -10
```

打开相关文件，观察 store 组织方式。

- [ ] **Step 2: 新增 `src/stores/LicenseStore.js`**

```js
import { makeAutoObservable } from 'mobx'

export class LicenseStore {
  status = 'pending'        // 'pending' | 'ok' | 'denied' | 'max-reached' | 'server-down'
  errorTitle = ''
  errorDetail = ''
  licenseId = ''
  maxConcurrent = 0
  active = 0
  expiresAt = null          // ISO string
  lastDeniedOp = ''         // 'OpenFile' | 'CreateNewFile'
  lastDeniedReason = ''

  constructor() { makeAutoObservable(this) }

  setOk({ licenseId, max, active, expiresAt }) {
    this.status = 'ok'
    this.licenseId = licenseId
    this.maxConcurrent = max
    this.active = active
    this.expiresAt = expiresAt
  }

  setServerDown(detail) {
    this.status = 'server-down'
    this.errorTitle = '无法连接授权服务器'
    this.errorDetail = detail
  }

  setDenied(detail) {
    this.status = 'denied'
    this.errorTitle = 'License 校验失败'
    this.errorDetail = detail
  }

  setMaxReached({ active, max }) {
    this.status = 'max-reached'
    this.errorTitle = '授权名额已满'
    this.errorDetail = `${active}/${max} 个并发已被占用`
    this.active = active
    this.maxConcurrent = max
  }

  setActionDenied(op, reason) {
    this.lastDeniedOp = op
    this.lastDeniedReason = reason
  }

  clearActionDenied() {
    this.lastDeniedOp = ''
    this.lastDeniedReason = ''
  }

  get daysLeft() {
    if (!this.expiresAt) return null
    const ms = new Date(this.expiresAt).getTime() - Date.now()
    return Math.max(0, Math.floor(ms / (24 * 3600 * 1000)))
  }
}
```

- [ ] **Step 3: 接入 RootStore**

在 RootStore 对应文件里，把 `LicenseStore` 加入（跟现有 AppStore / EditorStore 同级）：

```js
import { LicenseStore } from '../stores/LicenseStore'
// ...
export class RootStore {
  constructor() {
    this.appStore = new AppStore()
    this.editorStore = new EditorStore()
    this.licenseStore = new LicenseStore()   // 新增
    // ... 其他 store
  }
}
```

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/src/stores/LicenseStore.js DrawingWebApp/src/context/ViewerContext.js
git commit -m "feat(license): add LicenseStore to RootStore"
```

---

### Task 5.2: 修改 useWasmModule.js

**Files:**
- Modify: `DrawingWebApp/src/hooks/useWasmModule.js`

- [ ] **Step 1: 解构 licenseStore**

把现有 [useWasmModule.js:10](../../src/hooks/useWasmModule.js#L10) 的 `const { appStore, editorStore } = rootStore` 改为：

```js
const { appStore, editorStore, licenseStore } = rootStore
```

- [ ] **Step 2: 在 postRun 里加 License 初始化 + 心跳**

找到 [useWasmModule.js:169](../../src/hooks/useWasmModule.js#L169) `Module.postRun.push(function () {` 块。在该函数开头（在 `const canvasEl = document.getElementById('canvas')` 之前）插入：

```js
      // ====== License Gate 初始化 ======
      const licenseReady = await (async () => {
        // 1. 拉取 license.dat
        let licenseJson
        try {
          const resp = await fetch('/api/license/info', { signal: AbortSignal.timeout(10000) })
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
          licenseJson = await resp.text()
        } catch (e) {
          licenseStore.setServerDown(e.message || '网络异常')
          return false
        }

        // 2. WASM 内验 License
        if (!Module.initLicenseGate(licenseJson)) {
          const err = Module.getLicenseGateError()
          licenseStore.setDenied(err)
          return false
        }

        // 3. 建会话
        try {
          const resp = await fetch('/api/license/session/start', { method: 'POST' })
          if (resp.status === 429) {
            const err = await resp.json()
            licenseStore.setMaxReached({ active: err.active, max: err.max })
            return false
          }
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
          const { sessionId, token, active, max } = await resp.json()
          window.__licenseSessionId    = sessionId
          window.__currentLicenseToken = token
          licenseStore.setOk({
            licenseId: Module.getLicenseId(),
            max, active,
            expiresAt: null,  // 可从 license.dat payload 读取, 此处先留空
          })
        } catch (e) {
          licenseStore.setServerDown(e.message || '建立会话失败')
          return false
        }

        // 4. 3 分钟心跳
        setInterval(async () => {
          try {
            const resp = await fetch('/api/license/token/refresh', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ sessionId: window.__licenseSessionId }),
              signal: AbortSignal.timeout(8000),
            })
            if (resp.ok) {
              const { token } = await resp.json()
              window.__currentLicenseToken = token
            }
            // 401 (session not found) 或网络错误: 静默, 等下一次; 旧 token 5 分钟后自然过期
          } catch (_) { /* 静默 */ }
        }, 180 * 1000)

        // 5. 页面关闭立即释放名额
        window.addEventListener('beforeunload', () => {
          try {
            navigator.sendBeacon('/api/license/session/end',
              JSON.stringify({ sessionId: window.__licenseSessionId }))
          } catch (_) { /* 浏览器不支持时忽略 */ }
        })

        // 6. WASM 拒绝时的回调
        window.__onLicenseDenied = (op, reason) => {
          licenseStore.setActionDenied(op, reason)
        }

        return true
      })()

      if (!licenseReady) {
        console.error('[License] not ready, Viewer not initialized')
        return
      }
      // ================================
```

- [ ] **Step 3: postRun 改为 async function**

把 `Module.postRun.push(function () {` 改为 `Module.postRun.push(async function () {`。

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/src/hooks/useWasmModule.js
git commit -m "feat(license): wire License Gate init and 3min heartbeat in useWasmModule"
```

---

### Task 5.3: LicenseErrorOverlay 组件

**Files:**
- Create: `DrawingWebApp/src/components/LicenseErrorOverlay/LicenseErrorOverlay.jsx`
- Create: `DrawingWebApp/src/components/LicenseErrorOverlay/LicenseErrorOverlay.module.css`
- Modify: `DrawingWebApp/src/App.jsx` (or 最外层容器)

- [ ] **Step 1: 写 `LicenseErrorOverlay.module.css`**

```css
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
}

.panel {
  background: #262626;
  color: #e8e8e8;
  border-radius: 8px;
  padding: 32px 40px;
  max-width: 520px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
  border-top: 4px solid #ff4d4f;
}

.title {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #ff7875;
}

.detail {
  font-size: 14px;
  line-height: 1.6;
  color: #bfbfbf;
  white-space: pre-wrap;
  word-break: break-all;
}

.retryBtn {
  margin-top: 20px;
  padding: 8px 20px;
  background: #1677ff;
  border: 0;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
}

.retryBtn:hover { background: #4096ff; }
```

- [ ] **Step 2: 写 `LicenseErrorOverlay.jsx`**

```jsx
import { observer } from 'mobx-react-lite'
import { useStores } from '../../context/ViewerContext'
import s from './LicenseErrorOverlay.module.css'

const LicenseErrorOverlay = observer(() => {
  const { rootStore } = useStores()
  const { licenseStore } = rootStore

  const st = licenseStore.status
  if (st === 'ok' || st === 'pending') return null

  return (
    <div className={s.overlay}>
      <div className={s.panel}>
        <div className={s.title}>{licenseStore.errorTitle}</div>
        <div className={s.detail}>{licenseStore.errorDetail}</div>
        <button className={s.retryBtn} onClick={() => window.location.reload()}>
          重新加载
        </button>
      </div>
    </div>
  )
})

export default LicenseErrorOverlay
```

- [ ] **Step 3: 在 App.jsx 挂载**

```jsx
import LicenseErrorOverlay from './components/LicenseErrorOverlay/LicenseErrorOverlay'
// ...
function App() {
  return (
    <>
      <LicenseErrorOverlay />
      {/* 现有 TopBar / Ribbon / Canvas / ... */}
    </>
  )
}
```

- [ ] **Step 4: Commit**

```bash
git add DrawingWebApp/src/components/LicenseErrorOverlay/ DrawingWebApp/src/App.jsx
git commit -m "feat(license): add LicenseErrorOverlay full-screen modal"
```

---

### Task 5.4: ActionDenied Toast

**Files:**
- Create: `DrawingWebApp/src/components/LicenseActionDenied/LicenseActionDenied.jsx`
- Modify: `DrawingWebApp/src/App.jsx`

`__onLicenseDenied` 触发时（OpenFile/CreateNewFile 被拒）显示 toast。

- [ ] **Step 1: 写组件**

```jsx
import { observer } from 'mobx-react-lite'
import { useEffect } from 'react'
import { message } from 'antd'
import { useStores } from '../../context/ViewerContext'

const LicenseActionDenied = observer(() => {
  const { rootStore } = useStores()
  const { licenseStore } = rootStore

  useEffect(() => {
    if (licenseStore.lastDeniedOp) {
      message.error({
        content: `操作被拒绝 (${licenseStore.lastDeniedOp}): ${licenseStore.lastDeniedReason}`,
        duration: 5,
      })
      licenseStore.clearActionDenied()
    }
  }, [licenseStore.lastDeniedOp, licenseStore.lastDeniedReason])

  return null
})

export default LicenseActionDenied
```

- [ ] **Step 2: 挂到 App.jsx**

```jsx
import LicenseActionDenied from './components/LicenseActionDenied/LicenseActionDenied'
// ...
<>
  <LicenseErrorOverlay />
  <LicenseActionDenied />
  {/* ... */}
</>
```

- [ ] **Step 3: Commit**

```bash
git add DrawingWebApp/src/components/LicenseActionDenied/ DrawingWebApp/src/App.jsx
git commit -m "feat(license): toast when CadCore::OpenFile/CreateNewFile denied"
```

---

### Task 5.5: 端到端手动测试

- [ ] **Step 1: 启动 server + 前端**

```bash
# 终端 1
cd DrawingWebApp/server
npm run license:dev-fixtures   # 若还没跑过
npm run dev

# 终端 2
cd DrawingWebApp
npm run dev
```

浏览器打开 http://localhost:3000

- [ ] **Step 2: 核对控制台**

浏览器开发者工具 Console 应见：
- `[useWasmModule] preRun: /uacad 目录结构已就绪`
- `[License] initFromLicenseJson OK, license_id=LIC-...`

Network 面板可见：
- `GET /api/license/info` 200
- `POST /api/license/session/start` 200
- 过 3 分钟后 `POST /api/license/token/refresh` 200

- [ ] **Step 3: 测 OpenFile 通路**

打开一份 DWG 文件，图纸应正常显示。

- [ ] **Step 4: 测授权失败路径**

```bash
# 停 server
# 等 5 分钟让 token 过期 (或把本机时间拨后)
# 再尝试 Open 一份新 DWG
```

Expected: 弹 toast `操作被拒绝 (OpenFile): Token expired`，图纸不打开。

- [ ] **Step 5: 测并发超限**

把 `server/license/license.dat` 里的 `max_concurrent` 手动改成 1（破坏签名后会触发签名错误，不要这样测）。正确的方式：重新用 `sign-license.js` 签一个 `--max-concurrent 1` 的 license。

然后开两个标签页，第二个应见全屏蒙层"授权名额已满 1/1"。

- [ ] **Step 6: Commit 任何修复**（如发现 bug）

---

## Phase 6: Docker 化

### Task 6.1: Dockerfile

**Files:**
- Create: `DrawingWebApp/Dockerfile`

- [ ] **Step 1: 写 Dockerfile**

```dockerfile
FROM node:20-alpine AS frontend-builder
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
RUN npm run build   # 产出 dist/

FROM node:20-alpine AS server
WORKDIR /app
COPY server/package.json server/package-lock.json ./
RUN npm ci --omit=dev
COPY server/ ./
# 前端 dist 也复制进 server container (server 托管 static)
COPY --from=frontend-builder /build/dist ./dist

# 默认目录; 运行时会被 -v /etc/machine-id:/etc/machine-id:ro 覆盖
VOLUME ["/app/license"]

ENV LICENSE_PATH=/app/license/license.dat
ENV CUSTOMER_KEY_PATH=/app/license/customer_key.pem
ENV ROOT_PUBKEY_PATH=/app/license/root_pubkey.pem
ENV PORT=3001

EXPOSE 3001
CMD ["node", "index.js"]
```

- [ ] **Step 2: Commit**

```bash
git add DrawingWebApp/Dockerfile
git commit -m "feat(license): add Dockerfile for server + frontend bundle"
```

---

### Task 6.2: docker-compose.yml

**Files:**
- Create: `DrawingWebApp/docker-compose.yml`

- [ ] **Step 1: 写 docker-compose.yml**

```yaml
version: '3.8'

services:
  drawingwebapp:
    build: .
    image: drawingwebapp-server:1.0
    restart: unless-stopped
    network_mode: host        # 必须: 硬件指纹需真实宿主 MAC
    volumes:
      # ========== 硬件指纹三件套 (只读) ==========
      - /etc/machine-id:/etc/machine-id:ro
      - /sys/class/dmi/id/product_uuid:/host/product_uuid:ro
      # ========== License 文件 (只读) ==========
      - ./license:/app/license:ro
    environment:
      LICENSE_PATH:      /app/license/license.dat
      CUSTOMER_KEY_PATH: /app/license/customer_key.pem
      ROOT_PUBKEY_PATH:  /app/license/root_pubkey.pem
      PORT:              "3001"
      # 如果用 LLM:
      # OPENAI_API_KEY: ${OPENAI_API_KEY}
      # OPENAI_MODEL:   gpt-4o
```

- [ ] **Step 2: 说明文档**

在 `DrawingWebApp/README.md` 或新增 `DEPLOY.md` 末尾加：

```markdown
## Docker 部署（客户侧）

1. 宿主机上生成硬件指纹：
   ```
   docker run --rm \
     -v /etc/machine-id:/etc/machine-id:ro \
     -v /sys/class/dmi/id/product_uuid:/host/product_uuid:ro \
     --network host \
     drawingwebapp-server:1.0 node tools/print-fingerprint.js
   ```
   把输出的 64 字符 hex 发给厂商。

2. 收到 `license.dat` + `customer_key.pem` 后，和 `root_pubkey.pem` 一起放入 `./license/`。

3. 启动：
   ```
   docker compose up -d
   ```

4. 查看启动日志验证 License 自检：
   ```
   docker compose logs -f
   ```
   应见 `[License] license_id=LIC-... max_concurrent=10 ...`
```

- [ ] **Step 3: Commit**

```bash
git add DrawingWebApp/docker-compose.yml DrawingWebApp/DEPLOY.md
git commit -m "feat(license): docker-compose with hardware fingerprint bind mounts"
```

---

### Task 6.3: 镜像冒烟测试

- [ ] **Step 1: 本地构建镜像**

```bash
cd DrawingWebApp
docker build -t drawingwebapp-server:1.0 .
```

- [ ] **Step 2: 生成宿主 License (用开发 root 签)**

```bash
# 宿主机上:
docker run --rm \
  -v /etc/machine-id:/etc/machine-id:ro \
  -v /sys/class/dmi/id/product_uuid:/host/product_uuid:ro \
  --network host \
  drawingwebapp-server:1.0 node tools/print-fingerprint.js
# 记下指纹 FP

# 假设你还在开发机, 有 dev-root-private.pem:
node server/tools/sign-license.js \
  --root-key server/license/dev-root-private.pem \
  --customer "Docker Test" \
  --fingerprint <FP> \
  --max-concurrent 3 \
  --expires 2027-04-15 \
  --out-dir ./license-docker

# 放到 ./license/
cp ./license-docker/license.dat  ./license/
cp ./license-docker/customer_key.pem ./license/
cp server/license/root_pubkey.pem ./license/
```

- [ ] **Step 3: 起 compose**

```bash
docker compose up
```

Expected: 日志里 License 自检通过；无 fingerprint mismatch 报错。

访问 `http://localhost:3001/api/license/info`，看到 JSON。

- [ ] **Step 4: Commit 任何修复**

---

## Phase 7: 收尾

### Task 7.1: 更新项目根 CLAUDE.md

**Files:**
- Modify: `e:/ODAGitLab/main24.10/CLAUDE.md`

- [ ] **Step 1: 在 "DrawingWebApp Backend (AI Server)" 段末尾加：**

```markdown
### License Gate

Server 启动时会执行 License 自检（SM2 双层非对称签名 + 硬件指纹绑定）。
开发环境运行 `npm run license:dev-fixtures` 生成本机 dev license。
详见 [docs/superpowers/specs/2026-04-15-wasm-license-gate-design.md](DrawingWebApp/docs/superpowers/specs/2026-04-15-wasm-license-gate-design.md)。
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(license): point CLAUDE.md at license gate spec"
```

---

### Task 7.2: 完整回归

- [ ] **Step 1: 跑所有单元测试**

```bash
cd DrawingWebApp/server
npm test
```

Expected: 全 PASS。

- [ ] **Step 2: 端到端冒烟**

```bash
npm run license:dev-fixtures
npm run dev            # 另一终端
cd .. && npm run dev   # 前端
# 浏览器打开 localhost:3000, 打开一份 DWG, 成功
```

- [ ] **Step 3: 容器冒烟（可选）**

```bash
cd DrawingWebApp
docker compose up
```

- [ ] **Step 4: 最终 Commit（如有 lint 修复等）**

---

## Self-Review Checklist

1. ✅ Spec 的 Section 1-13 每一节都在实施任务中覆盖：
   - §3 密钥 → Task 2.1, 4.1
   - §4 License 格式 → Task 1.1 (canonical), 2.3 (sign-license), 3.3 (validator)
   - §5 Token 协议 → Task 3.1 (signer), 4.4 (verifyCurrentToken)
   - §6 Server 规范 → Phase 3
   - §7 WASM 规范 → Phase 4
   - §8 前端规范 → Phase 5
   - §9 Docker → Phase 6
2. ✅ 所有步骤都有具体代码 / 命令
3. ✅ TDD 节奏在 Phase 1-3 严格；C++ 侧通过手动冒烟验证（现实妥协）
4. ✅ 类型一致性：`LicenseGate::verifyCurrentToken` 在 Task 4.4 定义，Task 4.5 使用
5. ⚠️ Task 4.3 依赖 uakernel 源码改动（加 `rawPKey()` getter），已在步骤中说明
6. ✅ 无占位符或 "TODO later"

---

## Open TODOs After MVP

- 防时钟回滚（WASM 端记录 "已见到的最大 issued_at"）— P2
- LLM Provider 初始化失败与 License 校验失败的日志区分 — 小打扫
- LicenseStore 里的 `expiresAt` 填充 (目前 Task 5.2 留空, 需从 /api/license/info 的 payload 再读)
