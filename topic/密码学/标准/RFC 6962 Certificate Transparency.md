---
title: RFC 6962 证书透明
description: RFC 6962 定义了 Certificate Transparency 实验性协议，通过公开的仅追加日志记录 TLS 证书的颁发情况，使任何人都能审计 CA 活动并发现可疑证书。
tags:
  - 密码学
  - Certificate Transparency
  - CT
  - 证书透明
  - RFC
---

> [!info] RFC 信息
> - **RFC 编号**：6962
> - **类别**：Experimental
> - **发布日期**：2013 年 6 月
> - **作者**：B. Laurie, A. Langley, E. Kasper (Google)
> - **ISSN**：2070-1721
> - **在线查看**：http://www.rfc-editor.org/info/rfc6962

# Certificate Transparency（证书透明）

## 摘要（Abstract）

本文档描述了一种实验性协议，用于以公开方式记录 Transport Layer Security (TLS) 证书在颁发或被观测到时的存在信息，使任何人都能审计 certificate authority (CA) 的活动、发现可疑证书的颁发，并审计 certificate log（证书日志）本身。最终目标是让客户端拒绝接受未出现在 log 中的 certificate，从而有效迫使 CA 将所有颁发的 certificate 加入 log。

Log 是实现了本文档所定义的提交和查询协议操作的网络服务。

## 备忘录状态（Status of This Memo）

本文档不是 Internet Standards Track 规范；它发布用于审查、实验性实现和评估。

本文档为 Internet 社区定义了一个实验性协议，是 Internet Engineering Task Force (IETF) 的产品，代表 IETF 社区的共识，已通过公开审查并经 Internet Engineering Steering Group (IESG) 批准发布。

## 版权声明（Copyright Notice）

Copyright (c) 2013 IETF Trust and the persons identified as the document authors. All rights reserved.

本文档受 BCP 78 和 IETF Trust's Legal Provisions Relating to IETF Documents (http://trustee.ietf.org/license-info) 约束。从本文档提取的代码组件必须包含 Simplified BSD License 文本，且不提供任何担保。

---

## 1. 概述（Informal Introduction）

Certificate transparency（证书透明）旨在通过提供公开可审计的、仅追加的（append-only）、不可信的 log 来缓解证书误发（misissued certificates）问题。Log 是公开可审计的，因此任何人都可以验证每个 log 的正确性，并监控何时有新 certificate 被添加。Log 本身并不阻止误发，但它们确保利益相关方（特别是证书中命名的主体）可以检测到这种误发行为。注意，这是一种通用机制，但在本文档中，我们仅描述其用于公共 CA 颁发的公共 TLS server certificate 的场景。

每个 log 由 certificate chain（证书链）组成，任何人都可以提交。预期公共 CA 会将其所有新颁发的 certificate 贡献给一个或多个 log；同时预期 certificate holder（证书持有者）也会提交自己的 certificate chain。为避免 log 被垃圾信息淹没至失去效用，要求每个 chain 的根必须是已知的 CA certificate。当 chain 提交到 log 时，会返回一个签名的时间戳（signed timestamp），日后可用来向客户端证明该 chain 已被提交。因此 TLS 客户端可以要求其看到的所有 certificate 都已被记录到 log 中。

关注证书误发的各方可以监控 log，定期请求所有新条目，从而检查其负责的 domain 是否被颁发了意料之外的 certificate。他们如何利用这些信息（特别是发现误发后的处理）超出了本文档的范围，但总体来说，他们可以调用现有的处理误发 certificate 的商业机制。当然，任何愿意的人都可以监控 log，如果认为某个 certificate 被错误颁发，可以采取适当行动。

类似地，那些从特定 log 获得过签名时间戳的各方，之后可以向该 log 要求包含证明（proof of inclusion）。如果 log 无法提供此证明（或者相应的 certificate 在 monitor 的 log 副本中不存在），这就是 log 运行不正确的证据。检查操作是异步的，以允许 TLS 连接不受网络连接问题和防火墙限制的影响而继续进行。

> [!note] Merkle Tree 的作用
> Log 的仅追加属性通过 Merkle Tree（默克尔树）在技术上实现，可用于证明 log 的任何特定版本是任何先前版本的超集。同样，Merkle Tree 避免了对 log 的盲目信任：如果 log 试图向不同的人展示不同内容，可以通过比较 tree root（树根）和 consistency proof（一致性证明）来高效检测。类似地，log 的任何不当行为（例如，为 certificate 签发时间戳后又未将其记入 log）都可以被高效检测并向全世界证明。

### 1.1 需求语言（Requirements Language）

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按 RFC 2119 [RFC2119] 的描述进行解释。

### 1.2 数据结构（Data Structures）

数据结构按照 [RFC[[5246]]] 第 4 节的约定定义。

---

## 2. 密码学组件（Cryptographic Components）

### 2.1 Merkle Hash Tree（默克尔哈希树）

Log 使用二叉 Merkle Hash Tree 进行高效审计。哈希算法为 SHA-256 [FIPS.[[180-4]]]（注意，本实验中此算法是固定的，但预期每个 log 将能够指定自己的哈希算法）。Merkle Tree Hash 的输入是数据条目列表；这些条目将被哈希构成 Merkle Hash Tree 的叶子。输出是单个 32 字节的 Merkle Tree Hash。给定有序的 n 个输入列表 D[n] = {d(0), d(1), ..., d(n-1)}，Merkle Tree Hash (MTH) 定义如下：

空列表的哈希是空字符串的哈希：

```
MTH({}) = SHA-256().
```

单条目列表的哈希（也称为 leaf hash，叶子哈希）是：

```
MTH({d(0)}) = SHA-256(0x00 || d(0)).
```

> [!tip] 递归定义
> 对于 n > 1，设 k 为小于 n 的最大 2 的幂（即 k < n <= 2k）。则 n 元素列表 D[n] 的 Merkle Tree Hash 递归定义为：
>
> `MTH(D[n]) = SHA-256(0x01 || MTH(D[0:k]) || MTH(D[k:n]))`
>
> 其中 `||` 是字符串拼接，`D[k1:k2]` 表示长度为 (k2 - k1) 的列表 {d(k1), d(k1+1),..., d(k2-1)}。

> [!note] 域分离（Domain Separation）
> 叶子和节点的哈希计算方式不同。这种域分离是实现第二原像抗性（second preimage resistance）所必需的。

注意，我们不要求输入列表的长度为 2 的幂。因此，生成的 Merkle Tree 可能不是平衡的；但其形状由叶子数量唯一确定。（注意：此 Merkle Tree 与 history tree [CrosbyWallach] 提案基本相同，只是我们对非满树的处理方式不同。）

#### 2.1.1 Merkle Audit Path（默克尔审计路径）

Merkle audit path 是 Merkle Hash Tree 中某个叶子对应的、计算该树的 Merkle Tree Hash 所需的最短额外节点列表。树中的每个节点要么是叶子节点，要么由其下方（即朝向叶子方向的）两个节点计算而来。在树的每一步上升（朝向根方向）中，audit path 中的一个节点与当前计算得到的节点进行组合。换句话说，audit path 由从叶子到树根路径上所需的缺失节点列表组成。如果从 audit path 计算出的根与真实根匹配，则 audit path 证明了该叶子存在于树中。

给定有序的 n 个输入列表 D[n] = {d(0), ..., d(n-1)}，第 (m+1) 个输入 d(m)（0 <= m < n）的 Merkle audit path PATH(m, D[n]) 定义如下：

单元素列表 D[1] = {d(0)} 中唯一叶子的路径为空：

```
PATH(0, {d(0)}) = {}
```

对于 n > 1，设 k 为小于 n 的最大 2 的幂。列表中 n > m 个元素的第 (m+1) 个元素 d(m) 的路径递归定义为：

```
PATH(m, D[n]) = PATH(m, D[0:k]) : MTH(D[k:n])    当 m < k 时

PATH(m, D[n]) = PATH(m - k, D[k:n]) : MTH(D[0:k]) 当 m >= k 时
```

其中 `:` 是列表拼接，`D[k1:k2]` 与前面一样表示长度为 (k2 - k1) 的列表。

#### 2.1.2 Merkle Consistency Proof（默克尔一致性证明）

Merkle consistency proof 证明树的仅追加属性。给定 Merkle Tree Hash MTH(D[n]) 和先前发布的 MTH(D[0:m])（m <= n），Merkle consistency proof 是 Merkle Tree 中验证前 m 个输入 D[0:m] 在两棵树中相同所需的节点列表。因此，一致性证明必须包含足以验证 MTH(D[n]) 的中间节点（即对输入的承诺）集合，使得（其中的一个子集）同样的节点也可用于验证 MTH(D[0:m])。我们定义了一个输出（唯一的）最小一致性证明的算法。

给定有序的 n 个输入列表 D[n] = {d(0), ..., d(n-1)}，先前 Merkle Tree Hash MTH(D[0:m])（0 < m < n）的 Merkle consistency proof PROOF(m, D[n]) 定义为：

```
PROOF(m, D[n]) = SUBPROOF(m, D[n], true)
```

当 m = n 且 m 是最初请求 PROOF 时的值时（即子树 Merkle Tree Hash MTH(D[0:m]) 已知），子证明为空：

```
SUBPROOF(m, D[m], true) = {}
```

当 m = n 且 m 不是最初请求的值时，子证明为提交输入 D[0:m] 的 Merkle Tree Hash：

```
SUBPROOF(m, D[m], false) = {MTH(D[m])}
```

对于 m < n，设 k 为小于 n 的最大 2 的幂。子证明递归定义如下：

如果 m <= k，右子树条目 D[k:n] 仅存在于当前树中。我们证明左子树条目 D[0:k] 一致，并添加对 D[k:n] 的承诺：

```
SUBPROOF(m, D[n], b) = SUBPROOF(m, D[0:k], b) : MTH(D[k:n])
```

如果 m > k，左子树条目 D[0:k] 在两棵树中相同。我们证明右子树条目 D[k:n] 一致，并添加对 D[0:k] 的承诺：

```
SUBPROOF(m, D[n], b) = SUBPROOF(m - k, D[k:n], false) : MTH(D[0:k])
```

其中 `:` 是列表拼接。最终证明中的节点数上限为 ceil(log2(n)) + 1。

#### 2.1.3 示例（Example）

包含 7 个叶子的二叉 Merkle Tree：

```
           hash
          /    \
         /      \
        /        \
       /          \
      /            \
     k              l
    / \            / \
   /   \          /   \
  /     \        /     \
 g       h      i      j
/ \     / \    / \     |
a b     c d    e f     d6
| |     | |    | |
d0 d1   d2 d3  d4 d5
```

- d0 的 audit path：`[b, h, l]`
- d3 的 audit path：`[c, g, l]`
- d4 的 audit path：`[f, j, k]`
- d6 的 audit path：`[i, k]`

同一棵树，分四步增量构建：

```
    hash0          hash1=k
    / \              /  \
   /   \            /    \
  /     \          /      \
  g      c         g       h
 / \     |        / \     / \
 a b     d2       a b     c d
 | |              | |     | |
d0 d1            d0 d1   d2 d3

         hash2                    hash
         /  \                    /    \
        /    \                  /      \
       /      \                /        \
      /        \              /          \
     /          \            /            \
    k            i          k              l
   / \          / \        / \            / \
  /   \         e f       /   \          /   \
 /     \        | |      /     \        /     \
g       h      d4 d5    g       h      i      j
/ \     / \             / \     / \    / \     |
a b     c d             a b     c d    e f     d6
| |     | |             | |     | |    | |
d0 d1   d2 d3           d0 d1   d2 d3  d4 d5
```

> [!example] 一致性证明示例
> - hash0 和 hash 之间的 consistency proof：`PROOF(3, D[7]) = [c, d, g, l]`。c、g 用于验证 hash0，d、l 额外用于证明 hash 与 hash0 一致。
> - hash1 和 hash 之间的 consistency proof：`PROOF(4, D[7]) = [l]`。可使用 hash1=k 和 l 验证 hash。
> - hash2 和 hash 之间的 consistency proof：`PROOF(6, D[7]) = [i, j, k]`。k、i 用于验证 hash2，j 额外用于证明 hash 与 hash2 一致。

#### 2.1.4 签名（Signatures）

多种数据结构需要签名。Log 必须使用以下两种签名之一：

- 使用 NIST P-256 曲线的椭圆曲线签名（Digital Signature Standard [DSS] 的 D.1.2.3 节），或
- RSA 签名（RSASSA-PKCS1-V1_5 with SHA-256，[RFC3447] 的 8.2 节），密钥长度至少 2048 位。

---

## 3. Log 格式与操作（Log Format and Operation）

任何人都可以向 certificate log 提交 certificate 以进行公开审计；然而，由于未被记录的 certificate 将不被 TLS 客户端接受，预期 certificate 所有者或其 CA 通常会提交它们。Log 是一个单一的、持续增长的、仅追加的 Merkle Tree，包含这些 certificate。

当有效的 certificate 被提交到 log 时，log **必须**立即返回一个 Signed Certificate Timestamp (SCT)。SCT 是 log 的承诺，保证在称为 Maximum Merge Delay (MMD) 的固定时间内将 certificate 纳入 Merkle Tree。如果 log 之前已见过该 certificate，它可以返回与之前相同的 SCT。TLS server **必须**将来自一个或多个 log 的 SCT 与 certificate 一起呈现给 TLS 客户端。TLS 客户端**必须**拒绝没有有效 SCT 的 end-entity certificate（终端实体证书）。

> [!warning] 关键约束
> Log **必须**在 SCT 签发后的 Maximum Merge Delay 期间内将 certificate 纳入其 Merkle Tree。Log 操作员**不得**对检索或共享 log 数据施加任何条件。

### 3.1 Log 条目（Log Entries）

任何人都可以向任何 log 提交 certificate。为了能够将每个被记录的 certificate 归因于其颁发者，log **应当**发布可接受的 root certificate（根证书）列表（此列表可能有用地设为各主要浏览器厂商信任的根证书的并集）。每个提交的 certificate **必须**附带验证证书链直至被接受的 root certificate 所需的所有额外 certificate。Root certificate 本身可以从提交给 log server 的链中省略。

或者，certificate authority（包括根 CA 和中间 CA）可以在颁发前将 certificate 提交到 log。为此，CA 提交一个 Precertificate（预证书），log 可以用它来创建一个对最终颁发的 certificate 有效的条目。Precertificate 是通过向 end-entity TBSCertificate 添加一个特殊的 critical poison extension（关键性毒性扩展，OID 1.3.6.1.4.1.11129.2.4.3，其 extnValue OCTET STRING 包含 [[ASN.1]] NULL 数据 0x05 0x00）来构造的（此扩展确保 Precertificate 无法被标准 X.509v3 客户端验证），然后使用以下方式之一对生成的 TBSCertificate [RFC5280] 进行签名：

- 一个特殊用途的 Precertificate Signing Certificate（CA:true，Extended Key Usage: Certificate Transparency，OID 1.3.6.1.4.1.11129.2.4.4）。该 Precertificate Signing Certificate **必须**由最终将签署 end-entity TBSCertificate 以生成 end-entity certificate 的（根或中间）CA certificate 直接认证。
- 或者，用于签署最终 certificate 的 CA certificate。

如上所述，Precertificate 提交**必须**附带 Precertificate Signing Certificate（如果使用了的话）以及验证链直至被接受的 root certificate 所需的所有额外 certificate。TBSCertificate 上的签名表明 CA 颁发 certificate 的意图。此意图被视为有约束力的（即 Precertificate 的误发等同于最终 certificate 的误发）。每个 log 验证 Precertificate 签名链，并在相应的 TBSCertificate 上签发 Signed Certificate Timestamp。

> [!important] Log 验证要求
> Log **必须**验证提交的 end-entity certificate 或 Precertificate 具有有效的签名链，可追溯到受信任的 root CA certificate。Log **可以**接受已过期、尚未生效、已被吊销或其他不完全符合 X.509 验证规则的 certificate。但是，log **必须**拒绝发布没有到已知 root CA 有效链的 certificate。如果 certificate 被接受并签发了 SCT，接受的 log **必须**存储用于验证的整个链，包括 certificate 或 Precertificate 本身以及用于验证链的 root certificate，并且**必须**在审计请求时出示此链。

每个 log 中的 certificate 条目**必须**包含以下组件：

```
enum { x509_entry(0), precert_entry(1), (65535) } LogEntryType;

struct {
    LogEntryType entry_type;
    select (entry_type) {
        case x509_entry: X509ChainEntry;
        case precert_entry: PrecertChainEntry;
    } entry;
} LogEntry;

opaque ASN.1Cert<1..2^24-1>;

struct {
    ASN.1Cert leaf_certificate;
    ASN.1Cert certificate_chain<0..2^24-1>;
} X509ChainEntry;

struct {
    ASN.1Cert pre_certificate;
    ASN.1Cert precertificate_chain<0..2^24-1>;
} PrecertChainEntry;
```

Log **可以**限制其接受的链长度。

- **entry_type**：此条目的类型。此协议版本的未来修订可能会添加新的 LogEntryType 值。第 4 节解释了客户端应如何处理未知条目类型。
- **leaf_certificate**：提交用于审计的 end-entity certificate。
- **certificate_chain**：验证 end-entity certificate 所需的额外 certificate 链。第一个 certificate **必须**认证 end-entity certificate。后续每个 certificate **必须**直接认证前一个。最后一个 certificate **必须**是 log 接受的 root certificate。
- **pre_certificate**：提交用于审计的 Precertificate。
- **precertificate_chain**：验证 Precertificate 提交所需的额外 certificate 链。第一个 certificate **可以**是有效的 Precertificate Signing Certificate，并且**必须**认证第一个 certificate。后续每个 certificate **必须**直接认证前一个。最后一个 certificate **必须**是 log 接受的 root certificate。

### 3.2 Signed Certificate Timestamp 结构（Structure of the Signed Certificate Timestamp）

```
enum { certificate_timestamp(0), tree_hash(1), (255) }
  SignatureType;

enum { v1(0), (255) }
  Version;

  struct {
      opaque key_id[32];
  } LogID;

  opaque TBSCertificate<1..2^24-1>;

  struct {
      opaque issuer_key_hash[32];
      TBSCertificate tbs_certificate;
  } PreCert;

  opaque CtExtensions<0..2^16-1>;
```

- **key_id**：log 公钥的 SHA-256 哈希，以 SubjectPublicKeyInfo 的 DER 编码计算。
- **issuer_key_hash**：certificate 颁发者公钥的 SHA-256 哈希，以 SubjectPublicKeyInfo 的 DER 编码计算。这用于将颁发者绑定到最终 certificate。
- **tbs_certificate**：Precertificate 的 DER 编码 TBSCertificate（参见 [RFC5280]）——即不含签名和 poison extension 的部分。如果 Precertificate 不是用将颁发最终 certificate 的 CA certificate 签名的，则 TBSCertificate 的 issuer 也需改为将颁发最终 certificate 的 CA 的 issuer。注意，也可以从最终 certificate 中提取 TBSCertificate 并删除 SCT 扩展来重建。还应注意，由于 TBSCertificate 包含必须同时匹配 Precertificate 签名算法和最终 certificate 签名算法的 AlgorithmIdentifier，因此它们必须使用相同的算法和参数进行签名。

```
struct {
    Version sct_version;
    LogID id;
    uint64 timestamp;
    CtExtensions extensions;
    digitally-signed struct {
        Version sct_version;
        SignatureType signature_type = certificate_timestamp;
        uint64 timestamp;
        LogEntryType entry_type;
        select(entry_type) {
            case x509_entry: ASN.1Cert;
            case precert_entry: PreCert;
        } signed_entry;
       CtExtensions extensions;
    };
} SignedCertificateTimestamp;
```

digitally-signed 元素的编码在 [RFC[[5246]]] 中定义。

- **sct_version**：SCT 遵循的协议版本。此版本为 v1。
- **timestamp**：当前 NTP Time [RFC5905]，自 epoch（1970 年 1 月 1 日 00:00）以来的毫秒数，忽略闰秒。
- **entry_type**：可能从 SCT 呈现的上下文中隐含。
- **signed_entry**：X509ChainEntry 情况下为 `leaf_certificate`，PrecertChainEntry 情况下为 PreCert。
- **extensions**：此协议版本（v1）的未来扩展。目前未指定任何扩展。

### 3.3 在 TLS 握手中包含 Signed Certificate Timestamp

来自至少一个 log 的、对应 end-entity certificate 的 SCT 数据必须包含在 TLS 握手中，可通过以下三种方式之一：

1. 使用 X509v3 certificate extension（如所述）
2. 使用 TLS extension（[RFC[[5246]]] 的 7.4.1.4 节），类型为 `signed_certificate_timestamp`
3. 使用 OCSP Stapling（也称为 "Certificate Status Request" TLS extension；参见 [RFC6066]），其中响应包含 OID 为 1.3.6.1.4.1.11129.2.4.5 的 OCSP extension（参见 [RFC2560]）

**必须**包含至少一个 SCT。Server 操作员**可以**包含多个 SCT。

类似地，CA 可以将 Precertificate 提交到多个 log，所有获得的 SCT 可以直接嵌入最终 certificate 中，方法是将 SignedCertificateTimestampList 结构编码为 [[ASN.1]] OCTET STRING，并作为 X.509v3 certificate extension（OID 1.3.6.1.4.1.11129.2.4.2）插入 TBSCertificate。收到 certificate 后，客户端可以重建原始 TBSCertificate 以验证 SCT 签名。

嵌入 OCSP extension 或 X509v3 certificate extension 中的 [[ASN.1]] OCTET STRING 内容如下：

```
opaque SerializedSCT<1..2^16-1>;

struct {
    SerializedSCT sct_list <1..2^16-1>;
} SignedCertificateTimestampList;
```

这里 `SerializedSCT` 是一个不透明字节字符串，包含序列化的 TLS 结构。此编码确保 TLS 客户端可以单独解码每个 SCT（即如果有版本升级，过时的客户端仍可解析旧 SCT，同时跳过无法理解的新版本 SCT）。

> [!tip] 三种机制的实现要求
> - TLS 客户端**必须**实现所有三种机制。
> - Server **必须**至少实现其中一种。
> - 现有 TLS server 通常无需修改即可使用 certificate extension 机制。

TLS server 应发送来自多个 log 的 SCT，以防一个或多个 log 不被客户端接受（例如 log 因不当行为被撤销或密钥泄露）。

#### 3.3.1 TLS Extension

SCT 可以在 TLS 握手期间使用类型为 `signed_certificate_timestamp` 的 TLS extension 发送。

支持此 extension 的客户端**应当**发送具有适当类型和空 `extension_data` 的 ClientHello extension。

Server **必须**仅向在 ClientHello 中指示支持此 extension 的客户端发送 SCT，此时通过将 `extension_data` 设置为 `SignedCertificateTimestampList` 来发送 SCT。

会话恢复使用原始会话信息：客户端**应当**在 ClientHello 中包含 extension 类型，但如果会话被恢复，server 不需要处理它或在 ServerHello 中包含此 extension。

### 3.4 Merkle Tree

Merkle Tree Hash 的哈希算法为 SHA-256。

Merkle Tree 输入的结构：

```
enum { timestamped_entry(0), (255) }
  MerkleLeafType;

struct {
    uint64 timestamp;
    LogEntryType entry_type;
    select(entry_type) {
        case x509_entry: ASN.1Cert;
        case precert_entry: PreCert;
    } signed_entry;
    CtExtensions extensions;
} TimestampedEntry;

struct {
    Version version;
    MerkleLeafType leaf_type;
    select (leaf_type) {
        case timestamped_entry: TimestampedEntry;
    }
} MerkleTreeLeaf;
```

- **version**：MerkleTreeLeaf 对应的协议版本。此版本为 v1。
- **leaf_type**：叶子输入的类型。当前仅定义了 `timestamped_entry`（对应 SCT）。此协议版本的未来修订可能会添加新的 MerkleLeafType 类型。第 4 节解释了客户端应如何处理未知叶子类型。
- **timestamp**：为此 certificate 签发的对应 SCT 的时间戳。
- **signed_entry**：对应 SCT 的 `signed_entry`。
- **extensions**：对应 SCT 的 `extensions`。

Merkle Tree 的叶子是对应 `MerkleTreeLeaf` 结构的 leaf hash。

### 3.5 Signed Tree Head（签名树头）

每次 log 向树追加新条目时，log **应当**对相应的 tree hash 和树信息进行签名。该数据的签名结构如下：

```
digitally-signed struct {
    Version version;
    SignatureType signature_type = tree_hash;
    uint64 timestamp;
    uint64 tree_size;
    opaque sha256_root_hash[32];
} TreeHeadSignature;
```

- **version**：TreeHeadSignature 遵循的协议版本。此版本为 v1。
- **timestamp**：当前时间。时间戳**必须**至少与树中最新的 SCT 时间戳一样新。每个后续时间戳**必须**比前一次更新的时间戳更新。
- **tree_size**：新树中的条目数。
- **sha256_root_hash**：Merkle Hash Tree 的根。

每个 log **必须**按需生成不早于 Maximum Merge Delay 的 Signed Tree Head。在不太可能发生的、MMD 期间未收到任何新提交的情况下，log **应当**使用新的时间戳签署相同的 Merkle Tree Hash。

---

## 4. Log 客户端消息（Log Client Messages）

消息以 HTTPS GET 或 POST 请求发送。POST 参数和所有响应编码为 JSON 对象 [RFC4627]。GET 参数编码为与顺序无关的键值对 URL 参数，使用 `application/x-www-form-urlencoded` 格式（参见 [HTML401]）。二进制数据按各消息指定的方式进行 base64 编码 [RFC4648]。

> [!note] JSON 对象和 URL 参数可能包含此处未指定的字段。这些额外字段应被忽略。
> `<log server>` 前缀可以包含路径以及服务器名和端口。
> 通常，`version` 为 v1，`id` 为所查询 log server 的 log id。
> 任何错误将以 HTTP 4xx 或 5xx 响应返回，并附带人类可读的错误消息。

### 4.1 Add Chain to Log（向 Log 添加证书链）

```
POST https://<log server>/ct/v1/add-chain
```

**输入**：

- **chain**：base64 编码的 certificate 数组。第一个元素是 end-entity certificate；第二个链接到第一个，依此类推，最后一个是 root certificate 或链接到已知 root certificate 的 certificate。

**输出**：

- **sct_version**：SignedCertificateTimestamp 结构的版本，十进制。兼容的 v1 实现**不得**期望此值为 0（即 v1）。
- **id**：Log ID，base64 编码。由于请求 SCT 以包含在 TLS 握手中的 log 客户端不需要验证它，我们不假设他们知道 log 的 ID。
- **timestamp**：SCT 时间戳，十进制。
- **extensions**：用于未来扩展的不透明类型。Log 应将其设为空字符串。客户端应解码 base64 编码的数据并将其包含在 SCT 中。
- **signature**：SCT 签名，base64 编码。

如果 `sct_version` 不是 v1，则 v1 客户端可能无法验证签名。它**不得**将其视为错误。

### 4.2 Add PreCertChain to Log（向 Log 添加预证书链）

```
POST https://<log server>/ct/v1/add-pre-chain
```

**输入**：

- **chain**：base64 编码的 Precertificate 数组。第一个元素是 end-entity certificate；第二个链接到第一个，依此类推，最后一个是 root certificate 或链接到已知 root certificate 的 certificate。

**输出**与第 4.1 节相同。

### 4.3 Retrieve Latest Signed Tree Head（获取最新签名树头）

```
GET https://<log server>/ct/v1/get-sth
```

无输入。

**输出**：

- **tree_size**：树的大小（条目数），十进制。
- **timestamp**：时间戳，十进制。
- **sha256_root_hash**：树的 Merkle Tree Hash，base64 编码。
- **tree_head_signature**：上述数据的 TreeHeadSignature。

### 4.4 Retrieve Merkle Consistency Proof between Two Signed Tree Heads（获取两个签名树头之间的默克尔一致性证明）

```
GET https://<log server>/ct/v1/get-sth-consistency
```

**输入**：

- **first**：第一棵树的 tree_size，十进制。
- **second**：第二棵树的 tree_size，十进制。

两个 tree size 必须来自现有的 v1 STH。

**输出**：

- **consistency**：Merkle Tree 节点数组，base64 编码。

注意，此数据不需要签名，因为它用于验证已签名的 STH。

### 4.5 Retrieve Merkle Audit Proof from Log by Leaf Hash（通过叶子哈希获取默克尔审计证明）

```
GET https://<log server>/ct/v1/get-proof-by-hash
```

**输入**：

- **hash**：base64 编码的 v1 leaf hash。
- **tree_size**：证明所基于的树的 tree_size，十进制。

`hash` 必须按第 3.4 节的定义计算。`tree_size` 必须指定一个现有的 v1 STH。

**输出**：

- **leaf_index**：与 `hash` 参数对应的 end entity 的从 0 开始的索引。
- **audit_path**：base64 编码的 Merkle Tree 节点数组，证明所选 certificate 的包含性。

### 4.6 Retrieve Entries from Log（从 Log 获取条目）

```
GET https://<log server>/ct/v1/get-entries
```

**输入**：

- **start**：要获取的第一个条目的从 0 开始的索引，十进制。
- **end**：要获取的最后一个条目的从 0 开始的索引，十进制。

**输出**：

- **entries**：对象数组，每个包含：
  - **leaf_input**：base64 编码的 MerkleTreeLeaf 结构。
  - **extra_data**：base64 编码的与 log 条目相关的无符号数据。对于 X509ChainEntry，这是 `certificate_chain`；对于 PrecertChainEntry，这是整个 `PrecertChainEntry`。

> [!note] 数据验证
> 此消息未签名——获取的数据可以通过构建与获取的 STH 对应的 Merkle Tree Hash 来验证。所有叶子**必须**为 v1。但是，兼容的 v1 客户端**不得**将无法识别的 MerkleLeafType 或 LogEntryType 值视为错误。这意味着它可能无法解析某些条目，但每个客户端可以检查它识别的条目，并通过将未识别的叶子视为树的不透明输入来验证数据完整性。

`start` 和 `end` 参数**应当**在 `0 <= x < tree_size`（如第 4.3 节 get-sth 返回的）范围内。

Log **可以**接受 `0 <= start < tree_size` 且 `end >= tree_size` 的请求，通过返回仅覆盖指定范围内有效条目的部分响应。

Log **可以**限制每次 `get-entries` 请求可以获取的条目数。如果客户端请求超过允许的条目数，log **应当**返回最大允许数量的条目。这些条目**应当**从 `start` 指定的条目开始连续排列。

### 4.7 Retrieve Accepted Root Certificates（获取接受的根证书）

```
GET https://<log server>/ct/v1/get-roots
```

无输入。

**输出**：

- **certificates**：log 可接受的 base64 编码 root certificate 数组。

### 4.8 Retrieve Entry+Merkle Audit Proof from Log（从 Log 获取条目+默克尔审计证明）

```
GET https://<log server>/ct/v1/get-entry-and-proof
```

**输入**：

- **leaf_index**：所需条目的索引。
- **tree_size**：证明所需的树的 tree_size。

tree size 必须指定一个现有的 STH。

**输出**：

- **leaf_input**：base64 编码的 MerkleTreeLeaf 结构。
- **extra_data**：base64 编码的无符号数据，与第 4.6 节相同。
- **audit_path**：base64 编码的 Merkle Tree 节点数组，证明所选 certificate 的包含性。

此 API 可能仅对调试有用。

---

## 5. 客户端（Clients）

Log 的客户端可能执行各种不同的功能。这里描述一些典型客户端及其功能。任何不一致都可以用作 log 未正确行为的证据，数据结构上的签名防止 log 否认其不当行为。

> [!important] Gossip（八卦协议）
> 所有客户端应当彼此 gossip，至少交换 STH；这是确保它们都具有一致视图所需的全部。Gossip 的确切机制将在单独的文档中描述，但预期会有多种机制。

### 5.1 Submitter（提交者）

Submitter 将 certificate 或 Precertificate 提交到 log（如上所述）。它们可以继续使用返回的 SCT 来构建 certificate 或直接在 TLS 握手中使用。

### 5.2 TLS Client（TLS 客户端）

TLS 客户端不是 log 的直接客户端，但它们在 server certificate 旁边接收 SCT。除了对 certificate 及其链进行正常验证外，它们还应通过从 SCT 数据以及 certificate 计算签名输入并使用相应 log 的公钥验证签名来验证 SCT。注意，本文档不描述客户端如何获取 log 的公钥。

TLS 客户端**必须**拒绝时间戳在未来时间的 SCT。

### 5.3 Monitor（监控者）

Monitor 监控 log 并检查它们是否正确运行。它们还监控感兴趣的 certificate。

Monitor 至少需要检查其监控的每个 log 中的每个新条目。它可能还想保留整个 log 的副本。为此，它应对每个 log 遵循以下步骤：

1. 获取当前 STH（第 4.3 节）。
2. 验证 STH 签名。
3. 获取对应 STH 的树中的所有条目（第 4.6 节）。
4. 确认从获取的条目构建的树产生与 STH 中相同的哈希。
5. 获取当前 STH（第 4.3 节）。重复直到 STH 变化。
6. 验证 STH 签名。
7. 获取对应新 STH 的树中的所有新条目（第 4.6 节）。如果它们在较长时间内不可用，则应将其视为 log 的不当行为。
8. 以下两种方式之一：
   - 如果保留所有 log 条目：验证更新的完整条目列表生成的树与新 STH 的哈希相同。
   - 如果不保留所有 log 条目：
     1. 获取新 STH 与前一个 STH 之间的 consistency proof（第 4.4 节）。
     2. 验证 consistency proof。
     3. 验证新条目生成 consistency proof 中的对应元素。
9. 返回步骤 5。

### 5.4 Auditor（审计者）

Auditor 以关于 log 的部分信息作为输入，并验证此信息与其持有的其他部分信息是否一致。Auditor 可以是 TLS 客户端的组成部分；可以是独立服务；也可以是 monitor 的辅助功能。

来自同一 log 的任意一对 STH 可以通过请求 consistency proof（第 4.4 节）来验证。

附有 SCT 的 certificate 可以通过请求 Merkle audit proof（第 4.5 节）对任何日期在 SCT 时间戳 + Maximum Merge Delay 之后的 STH 进行验证。

Auditor 当然可以不时地自行获取 STH（第 4.3 节）。

---

## 6. IANA 考量（IANA Considerations）

IANA 已为 SCT TLS extension 分配了 RFC [[5246]] ExtensionType 值 (18)。extension 名称为 `signed_certificate_timestamp`。

---

## 7. 安全考量（Security Considerations）

通过 CA、log 和 server 执行此处描述的操作，TLS 客户端可以使用 log 和签名时间戳来降低接受误发 certificate 的可能性。如果 server 为 certificate 呈现了有效的签名时间戳，则客户端知道该 certificate 已在 log 中发布。由此，客户端知道 certificate 的主体有一定时间来注意到误发并采取行动（例如要求 CA 吊销误发的 certificate）。签名时间戳并不保证 certificate 未被误发，因为 certificate 的主体可能没有检查 log，或者 CA 可能拒绝了吊销请求。

> [!note] 激励机制
> 此外，如果 TLS 客户端不接受未被记录的 certificate，则站点所有者将有更大的动力将 certificate 提交到 log（可能在 CA 的协助下），从而提高系统的整体透明度。

### 7.1 误发证书（Misissued Certificates）

未被公开记录、因此没有有效 SCT 的误发 certificate 将被 TLS 客户端拒绝。拥有来自 log 的 SCT 的误发 certificate 将在 Maximum Merge Delay 内出现在该公开 log 中（假设 log 正常运行）。因此，误发 certificate 可被使用而不被审计的最大时间是 MMD。

### 7.2 误发检测（Detection of Misissue）

Log 本身不检测误发的 certificate；它们依赖利益相关方（如 domain 所有者）来监控并采取纠正行动。

### 7.3 不当行为的 Log（Misbehaving Logs）

Log 可能以两种方式行为不当：

1. 未能在 MMD 内将具有 SCT 的 certificate 纳入 Merkle Tree
2. 通过在不同时间和/或向不同方呈现两个不同的、冲突的 Merkle Tree 视图来违反其仅追加属性

两种违规形式都将被迅速且公开地检测到。

> [!warning] 检测机制
> - **MMD 违规检测**：log 客户端为每个观测到的 SCT 请求 Merkle audit proof 来检测。这些检查可以是异步的，每个 certificate 只需做一次。为保护客户端隐私，这些检查不需要向 log 透露确切的 certificate。客户端可以改为向受信任的 auditor 请求证明，或请求 SCT 时间戳附近一批 certificate 的 Merkle proof。
> - **仅追加属性违规检测**：通过全局 gossip 检测——所有人审计 log 并比较其最新 Signed Tree Head 版本。一旦检测到同一 log 的两个冲突的 Signed Tree Head，这就是该 log 不当行为的密码学证明。

---

## 8. 效率考量（Efficiency Considerations）

Merkle Tree 设计的目的是保持低通信开销。

审计 log 的完整性不需要第三方维护每个完整 log 的副本。Signed Tree Head 可以在新条目可用时更新，而无需重新计算整个树。第三方 auditor 只需获取与 log 现有 STH 的 Merkle consistency proof，即可高效验证其 Merkle Tree 更新的仅追加属性，而无需审计整个树。

---

## 9. 未来变更（Future Changes）

本节列出了我们可能在本文档的 Standards Track 版本中解决的问题：

- 可能允许某种密钥轮换机制，而非迫使 log 操作员创建新 log 以更改 log 签名密钥。
- 可能添加哈希和签名算法灵活性。
- 可能描述某些 gossip 协议。

---

## 10. 致谢（Acknowledgements）

作者感谢 Erwann Abelea, Robin Alden, Al Cutter, Francis Dupont, Stephen Farrell, Brad Hill, Jeff Hodges, Paul Hoffman, Jeffrey Hutzelman, SM, Alexey Melnikov, Chris Palmer, Trevor Perrin, Ryan Sleevi, Rob Stradling 和 Carl Wallace 的宝贵贡献。

---

## 11. 参考文献（References）

### 11.1 规范性引用（Normative Reference）

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.

### 11.2 资料性引用（Informative References）

- [CrosbyWallach] Crosby, S. and D. Wallach, "Efficient Data Structures for Tamper-Evident Logging", Proceedings of the 18th USENIX Security Symposium, Montreal, August 2009, <http://static.usenix.org/event/sec09/tech/full_papers/crosby.pdf>.
- [DSS] National Institute of Standards and Technology, "Digital Signature Standard (DSS)", FIPS 186-3, June 2009, <http://csrc.nist.gov/publications/fips/fips186-3/fips_186-3.pdf>.
- [FIPS.[[180-4]]] National Institute of Standards and Technology, "Secure Hash Standard", FIPS PUB [[180-4]], March 2012, <http://csrc.nist.gov/publications/fips/fips180-4/fips-180-4.pdf>.
- [HTML401] Raggett, D., Le Hors, A., and I. Jacobs, "HTML 4.01 Specification", World Wide Web Consortium Recommendation REC-html401-19991224, December 1999, <http://www.w3.org/TR/1999/REC-html401-19991224>.
- [RFC2560] Myers, M., Ankney, R., Malpani, A., Galperin, S., and C. Adams, [["X.509]] Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP", RFC 2560, June 1999.
- [RFC3447] Jonsson, J. and B. Kaliski, "Public-Key Cryptography Standards (PKCS) #1: RSA Cryptography Specifications Version 2.1", RFC 3447, February 2003.
- [RFC4627] Crockford, D., "The application/json Media Type for JavaScript Object Notation (JSON)", RFC 4627, July 2006.
- [RFC4648] Josefsson, S., "The Base16, Base32, and Base64 Data Encodings", RFC 4648, October 2006.
- [RFC[[5246]]] Dierks, T. and E. Rescorla, "The Transport Layer Security (TLS) Protocol Version 1.2", RFC [[5246]], August 2008.
- [RFC5280] Cooper, D., Santesson, S., Farrell, S., Boeyen, S., Housley, R., and W. Polk, "Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) [[Profile]]", RFC 5280, May 2008.
- [RFC5905] Mills, D., Martin, J., Burbank, J., and W. Kasch, "Network Time Protocol Version 4: Protocol and Algorithms Specification", RFC 5905, June 2010.
- [RFC6066] Eastlake, D., "Transport Layer Security (TLS) Extensions: Extension Definitions", RFC 6066, January 2011.

---

## 作者地址（Authors' Addresses）

**Ben Laurie**
Google UK Ltd.
EMail: benl@google.com

**Adam Langley**
Google Inc.
EMail: agl@google.com

**Emilia Kasper**
Google Switzerland GmbH
EMail: ekasper@google.com

## 相关笔记

- [[PKCS#11 v3.0 Cryptoki]]
- [[密码消息语法 (CMS)]]
- [[RFC 6960 在线证书状态协议 OCSP]]
- [[标准]]
- [["X.509 公钥基础设施证书与 CRL"]]
- [[RFC 9580 OpenPGP 新版]]
- [[FIPS 202 SHA-3]]
- [[PKCS#10 证书签名请求]]
