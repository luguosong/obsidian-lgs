---
title: HKDF 基于 HMAC 的密钥派生函数
description: RFC 5869 - 基于 HMAC 的提取-扩展密钥派生函数 (HKDF)
tags:
  - 密码学
  - HKDF
  - 密钥派生
  - HMAC
  - RFC
---

# HKDF：基于 HMAC 的提取-扩展密钥派生函数 (HMAC-based Extract-and-Expand Key Derivation Function)

> [!info] RFC 信息
> - **RFC 编号**：5869
> - **类别**：Informational
> - **发布日期**：2010 年 5 月
> - **作者**：H. Krawczyk (IBM Research)、P. Eronen (Nokia)

> [!abstract] 摘要
> 本文档指定了一种简单的基于 HMAC 的密钥派生函数 (HKDF)，可作为各种协议和应用中的构建模块。该密钥派生函数 (KDF) 旨在支持广泛的应用和需求，并在密码学哈希函数的使用上保持谨慎。

## 1. 引言

密钥派生函数 (KDF) 是密码系统的基本且必不可少的组件。其目标是接收一些初始密钥材料并从中派生一个或多个密码学强密钥。

本文档指定了一种简单的基于 HMAC 的 KDF，命名为 HKDF，可作为各种协议和应用中的构建模块。它已被多个 IETF 协议使用，包括 [IKEv2]、[PANA] 和 [EAP-AKA]。其目的是以通用方式记录此 KDF，以便在未来的协议和应用中推广使用，并抑制多种 KDF 机制的 proliferation。本文档不作为更改现有协议的号召，也不更改或更新使用此 KDF 的现有规范。

HKDF 遵循"提取-然后-扩展"（extract-then-expand）范式，KDF 在逻辑上由两个模块组成。第一阶段接收输入密钥材料并从中"提取"一个固定长度的伪随机密钥 K。第二阶段将密钥 K"扩展"为多个附加伪随机密钥（即 KDF 的输出）。

在许多应用中，输入密钥材料不一定均匀分布，攻击者可能对其有部分了解（例如[[密钥交换]]协议计算的 Diffie-Hellman 值），甚至有部分控制权（如某些熵收集应用）。因此，"提取"阶段的目标是将输入密材料中可能分散的熵"浓缩"为一个短但密码学强的伪随机密钥。在某些应用中，输入可能已经是一个好的伪随机密钥；在这种情况下，"提取"阶段不是必需的，可以单独使用"扩展"部分。

第二阶段将伪随机密钥"扩展"到所需长度；输出密钥的数量和长度取决于所需密钥的具体密码算法。

> [!note] 与其他 KDF 规范的比较
> 一些现有的 KDF 规范，如 NIST SP [[800-56A]]、NIST SP 800-108 和 IEEE 1363a-2004，要么只考虑第二阶段（扩展伪随机密钥），要么没有明确区分"提取"和"扩展"阶段，通常导致设计缺陷。本规范的目标是在最小化对底层哈希函数假设的同时，适应广泛的 KDF 需求。"提取-扩展"范式很好地支持了这一目标。

## 2. 基于 HMAC 的密钥派生函数 (HKDF)

### 2.1. 记法

HMAC-Hash 表示使用哈希函数 `Hash` 实例化的 HMAC 函数。HMAC 始终有两个参数：第一个是密钥，第二个是输入（或消息）。（注意在提取步骤中，`IKM` 用作 HMAC 输入，而不是 HMAC 密钥。）

当消息由多个元素组成时，使用连接（记为 `|`）作为第二个参数；例如 `HMAC(K, elem1 | elem2 | elem3)`。

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按 [KEYWORDS] 中的描述解释。

### 2.2. 步骤 1：提取 (Extract)

```
HKDF-Extract(salt, IKM) -> PRK
```

**选项：**
- `Hash` — 哈希函数；`HashLen` 表示哈希函数输出的字节长度

**输入：**
- `salt` — 可选的盐值（非秘密随机值）；如果未提供，设为 `HashLen` 个零字节组成的字符串
- `IKM` — 输入密钥材料

**输出：**
- `PRK` — 伪随机密钥（`HashLen` 字节）

输出 PRK 计算如下：

```
PRK = HMAC-Hash(salt, IKM)
```

### 2.3. 步骤 2：扩展 (Expand)

```
HKDF-Expand(PRK, info, L) -> OKM
```

**选项：**
- `Hash` — 哈希函数；`HashLen` 表示哈希函数输出的字节长度

**输入：**
- `PRK` — 至少 `HashLen` 字节的伪随机密钥（通常是提取步骤的输出）
- `info` — 可选的上下文和应用特定信息（可以是零长度字符串）
- `L` — 输出密钥材料的字节长度（≤ 255 × HashLen）

**输出：**
- `OKM` — 输出密钥材料（L 字节）

输出 OKM 计算如下：

```
N = ceil(L/HashLen)
T = T(1) | T(2) | T(3) | ... | T(N)
OKM = T 的前 L 个字节
```

其中：

```
T(0) = 空字符串（零长度）
T(1) = HMAC-Hash(PRK, T(0) | info | 0x01)
T(2) = HMAC-Hash(PRK, T(1) | info | 0x02)
T(3) = HMAC-Hash(PRK, T(2) | info | 0x03)
...
```

（其中连接到每个 T(n) 末尾的常量是单个字节。）

> [!tip] HKDF 计算流程
> 1. **提取**：用盐值和输入密钥材料计算 HMAC，得到伪随机密钥 PRK
> 2. **扩展**：用 PRK 和上下文信息迭代计算 HMAC，生成所需长度的输出密钥材料

## 3. HKDF 使用指南

本节包含关于 HKDF 使用的一系列指导原则。更详细的说明和设计原理参见 [HKDF-paper]。

### 3.1. 加盐还是不加盐

HKDF 可以在有随机盐和无随机盐的情况下运行。这是为了适应无法获取盐值的应用。但是，我们强调使用盐显著增强了 HKDF 的安全性——确保哈希函数不同使用之间的独立性、支持"源无关"提取，并加强了支撑 HKDF 设计的分析结果。

随机盐与初始密钥材料在两个根本方面不同：它是非秘密的且可重用。因此，许多应用都能获取盐值。例如，一个持续通过将 HKDF 应用于可更新的熵池（如采样的系统事件）来产生输出的伪随机数生成器 (PRNG)，可以固定一个盐值并在多次 HKDF 应用中使用，无需保护盐值的机密性。在不同的应用领域，密钥协商协议从 Diffie-Hellman 交换派生密码学密钥时，可以从通信双方交换并认证的公开 nonce 派生盐值（这是 [IKEv2] 采用的方法）。

理想情况下，盐值是长度为 HashLen 的随机（或伪随机）字符串。然而，即使质量较低的盐值（较短或熵有限）仍可能对输出密钥材料的安全性做出显著贡献；因此鼓励应用设计者在可以获取盐值时将其提供给 HKDF。

> [!note] 秘密盐值
> 虽然不是典型情况，但某些应用甚至可能有可用于秘密盐值。在这种情况下，HKDF 提供更强的安全保证。例如 IKEv1 的"公钥加密模式"中，提取器的"盐"是从秘密 nonce 计算的；类似地，IKEv1 的预共享密钥模式使用从预共享密钥派生的秘密盐。

### 3.2. HKDF 的 'info' 输入

虽然 `info` 值在 HKDF 定义中是可选的，但在应用中通常非常重要。其主要目标是将派生的密钥材料绑定到应用和上下文特定信息。例如，`info` 可以包含协议编号、算法标识符、用户身份等。特别是，它可以防止在不同上下文中（当相同的输入密钥材料 IKM 在不同上下文中使用时）派生相同的密钥材料。它还可以容纳密钥扩展部分的额外输入（例如，应用可能希望将密钥材料绑定到其长度 L，从而将 L 作为 `info` 字段的一部分）。`info` 有一个技术要求：它应独立于输入密钥材料值 IKM。

### 3.3. 跳过还是不跳过

在某些应用中，输入密钥材料 IKM 可能已经是密码学强密钥（例如 TLS RSA 密码套件中的 pre-master secret 是一个伪随机字符串，除了前两个字节）。在这种情况下，可以跳过提取部分，直接将 IKM 用作扩展步骤中 HMAC 的密钥。另一方面，应用仍可以使用提取部分以兼容一般情况。特别是，如果 IKM 是随机的（或伪随机的）但比 HMAC 密钥长，提取步骤可以输出合适的 HMAC 密钥。

> [!warning] Diffie-Hellman 场景
> 如果 IKM 是 Diffie-Hellman 值（如 TLS 使用 Diffie-Hellman 的情况），则提取步骤**不应跳过**。跳过将导致直接使用 Diffie-Hellman 值 g^{xy}（它**不是**均匀随机或伪随机字符串）作为 HMAC 的密钥 PRK。应通过提取步骤处理 g^{xy}（最好使用盐值），并将结果 PRK 用作扩展部分中 HMAC 的密钥。

在所需密钥比特数 L 不超过 HashLen 的情况下，可以直接将 PRK 用作 OKM。但这**不推荐**，特别是因为这会省略 `info` 作为派生过程一部分的使用（将 `info` 作为提取步骤的输入是不可取的——参见 [HKDF-paper]）。

### 3.4. 独立性的作用

密钥派生函数的分析假设输入密钥材料 (IKM) 来自某个源，该源被建模为某个长度的比特流上的概率分布（例如熵池产生的流、从随机选择的 Diffie-Hellman 指数派生的值等）；IKM 的每个实例是该分布的一个样本。密钥派生函数的主要目标是确保将 KDF 应用于从（同一）源分布采样的任意两个值 IKM 和 IKM' 时，结果密钥 OKM 和 OKM' 本质上相互独立（在统计或计算意义上）。为实现此目标，KDF 的输入应从适当的输入分布中选择，且输入应相互独立地选择（技术上，每个样本必须有足够的熵，即使在以其他 KDF 输入为条件时也是如此）。

独立性也是提供给 KDF 的盐值的重要方面。虽然无需保密盐值，且同一盐值可以与多个 IKM 值一起使用，但假设盐值独立于输入密钥材料。特别是，应用需要确保盐值不是由攻击者选择或操纵的。

## 4. HKDF 的应用

HKDF 旨在用于各种 KDF 应用，包括：

- 从不完美的随机源（如物理随机数生成器）构建伪随机生成器
- 从弱随机源（如从系统事件、用户按键收集的熵）生成伪随机性
- 在密钥协商协议中从共享的 Diffie-Hellman 值派生密码学密钥
- 从混合公钥加密方案派生对称密钥
- 密钥包装机制的密钥派生
- 以及更多

> [!warning] 不适用于密码派生
> HKDF 的提取步骤可以浓缩现有熵，但**不能放大熵**。对于从低熵源（如用户密码）派生密码学密钥的场景，密码的主要目标是利用盐值和有意减缓密钥派生计算来减慢字典攻击。HKDF 自然支持使用盐值，但减速机制不属于本规范。对基于密码的 KDF 感兴趣的应用应考虑 [PKCS5] 等是否比 HKDF 更适合。

## 5. 安全考虑

尽管 HKDF 很简单，但在设计和分析中考虑了许多安全因素。所有这些方面的阐述超出了本文档的范围。详细信息和设计原理参见 [HKDF-paper]。

该论文对 HKDF 作为多用途 KDF 进行了大量密码学分析，尤其注重其使用密码学哈希函数的方式。由于我们对当前哈希函数强度的信心有限，这一点尤为重要。然而，此分析并不意味着任何方案的绝对安全性，它在很大程度上取决于底层哈希函数的强度和建模选择。尽管如此，它仍有力地表明了 HKDF 设计的正确结构及其相对于其他常见 KDF 方案的优势。

## 6. 致谢

作者感谢 CFRG（Crypto Forum Research Group）列表成员的有益评论，以及 Dan Harkins 提供的测试向量。

## 7. 参考文献

### 7.1. 规范性引用

- \[HMAC] Krawczyk, H., Bellare, M., and R. Canetti, "HMAC: Keyed-Hashing for Message Authentication", RFC 2104, February 1997.
- \[KEYWORDS] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- \[SHS] National Institute of Standards and Technology, "Secure Hash Standard", FIPS PUB 180-3, October 2008.

### 7.2. 资料性引用

- \[1363a] IEEE, "Standard Specifications for Public-Key Cryptography - Amendment 1: Additional Techniques", IEEE Std 1363a-2004, 2004.
- \[800-108] NIST, "Recommendation for Key Derivation Using Pseudorandom Functions", SP 800-108, November 2008.
- \[[[800-56A]]] NIST, "Recommendation for Pair-Wise Key Establishment Schemes Using Discrete Logarithm Cryptography (Revised)", SP [[800-56A]], March 2007.
- \[EAP-AKA] Arkko, J., et al., "Improved Extensible Authentication Protocol Method for 3rd Generation Authentication and Key Agreement (EAP-AKA')", RFC 5448, May 2009.
- \[HKDF-paper] Krawczyk, H., "Cryptographic Extraction and Key Derivation: The HKDF Scheme", Proceedings of CRYPTO 2010.
- \[IKEv2] Kaufman, C., Ed., "Internet Key Exchange (IKEv2) Protocol", RFC 4306, December 2005.
- \[PANA] Forsberg, D., et al., "Protocol for Carrying Authentication for Network Access (PANA)", RFC 5191, May 2008.
- \[PKCS5] Kaliski, B., "PKCS #5: Password-Based Cryptography Specification Version 2.0", RFC 2898, September 2000.

## 附录 A. 测试向量

本附录提供 SHA-256 和 SHA-1 哈希函数 [SHS] 的测试向量。

### A.1. 测试用例 1

基本测试用例（SHA-256）

```
Hash = SHA-256
IKM  = 0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b (22 octets)
salt = 0x000102030405060708090a0b0c (13 octets)
info = 0xf0f1f2f3f4f5f6f7f8f9 (10 octets)
L    = 42

PRK  = 0x077709362c2e32df0ddc3f0dc47bba63
       90b6c73bb50f9c3122ec844ad7c2b3e5 (32 octets)
OKM  = 0x3cb25f25faacd57a90434f64d0362f2a
       2d2d0a90cf1a5a4c5db02d56ecc4c5bf
       34007208d5b887185865 (42 octets)
```

### A.2. 测试用例 2

较长输入/输出测试（SHA-256）

```
Hash = SHA-256
IKM  = 0x000102030405060708090a0b0c0d0e0f
       101112131415161718191a1b1c1d1e1f
       202122232425262728292a2b2c2d2e2f
       303132333435363738393a3b3c3d3e3f
       404142434445464748494a4b4c4d4e4f (80 octets)
salt = 0x606162636465666768696a6b6c6d6e6f
       707172737475767778797a7b7c7d7e7f
       808182838485868788898a8b8c8d8e8f
       909192939495969798999a9b9c9d9e9f
       a0a1a2a3a4a5a6a7a8a9aaabacadaeaf (80 octets)
info = 0xb0b1b2b3b4b5b6b7b8b9babbbcbdbebf
       c0c1c2c3c4c5c6c7c8c9cacbcccdcecf
       d0d1d2d3d4d5d6d7d8d9dadbdcdddedf
       e0e1e2e3e4e5e6e7e8e9eaebecedeeef
       f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff (80 octets)
L    = 82

PRK  = 0x06a6b88c5853361a06104c9ceb35b45c
       ef760014904671014a193f40c15fc244 (32 octets)
OKM  = 0xb11e398dc80327a1c8e7f78c596a4934
       4f012eda2d4efad8a050cc4c19afa97c
       59045a99cac7827271cb41c65e590e09
       da3275600c2f09b8367793a9aca3db71
       cc30c58179ec3e87c14c01d5c1f3434f
       1d87 (82 octets)
```

### A.3. 测试用例 3

零长度盐值/info 测试（SHA-256）

```
Hash = SHA-256
IKM  = 0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b (22 octets)
salt = (0 octets)
info = (0 octets)
L    = 42

PRK  = 0x19ef24a32c717b167f33a91d6f648bdf
       96596776afdb6377ac434c1c293ccb04 (32 octets)
OKM  = 0x8da4e775a563c18f715f802a063c5a31
       b8a11f5c5ee1879ec3454e5f3c738d2d
       9d201395faa4b61a96c8 (42 octets)
```

### A.4. 测试用例 4

基本测试用例（SHA-1）

```
Hash = SHA-1
IKM  = 0x0b0b0b0b0b0b0b0b0b0b0b (11 octets)
salt = 0x000102030405060708090a0b0c (13 octets)
info = 0xf0f1f2f3f4f5f6f7f8f9 (10 octets)
L    = 42

PRK  = 0x9b6c18c432a7bf8f0e71c8eb88f4b30baa2ba243 (20 octets)
OKM  = 0x085a01ea1b10f36933068b56efa5ad81
       a4f14b822f5b091568a9cdd4f155fda2
       c22e422478d305f3f896 (42 octets)
```

### A.5. 测试用例 5

较长输入/输出测试（SHA-1）

```
Hash = SHA-1
IKM  = 0x000102030405060708090a0b0c0d0e0f
       101112131415161718191a1b1c1d1e1f
       202122232425262728292a2b2c2d2e2f
       303132333435363738393a3b3c3d3e3f
       404142434445464748494a4b4c4d4e4f (80 octets)
salt = 0x606162636465666768696a6b6c6d6e6f
       707172737475767778797a7b7c7d7e7f
       808182838485868788898a8b8c8d8e8f
       909192939495969798999a9b9c9d9e9f
       a0a1a2a3a4a5a6a7a8a9aaabacadaeaf (80 octets)
info = 0xb0b1b2b3b4b5b6b7b8b9babbbcbdbebf
       c0c1c2c3c4c5c6c7c8c9cacbcccdcecf
       d0d1d2d3d4d5d6d7d8d9dadbdcdddedf
       e0e1e2e3e4e5e6e7e8e9eaebecedeeef
       f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff (80 octets)
L    = 82

PRK  = 0x8adae09a2a307059478d309b26c4115a224cfaf6 (20 octets)
OKM  = 0x0bd770a74d1160f7c9f12cd5912a06eb
       ff6adcae899d92191fe4305673ba2ffe
       8fa3f1a4e5ad79f3f334b3b202b2173c
       486ea37ce3d397ed034c7f9dfeb15c5e
       927336d0441f4c4300e2cff0d0900b52
       d3b4 (82 octets)
```

### A.6. 测试用例 6

零长度盐值/info 测试（SHA-1）

```
Hash = SHA-1
IKM  = 0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b (22 octets)
salt = (0 octets)
info = (0 octets)
L    = 42

PRK  = 0xda8c8a73c7fa77288ec6f5e7c297786aa0d32d01 (20 octets)
OKM  = 0x0ac1af7002b3d761d1e55298da9d0506
       b9ae52057220a306e07b6b87e8df21d0
       ea00033de03984d34918 (42 octets)
```

### A.7. 测试用例 7

SHA-1，未提供盐值（默认为 HashLen 个零字节），零长度 info

```
Hash = SHA-1
IKM  = 0x0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c (22 octets)
salt = 未提供（默认为 HashLen 个零字节）
info = (0 octets)
L    = 42

PRK  = 0x2adccada18779e7c2077ad2eb19d3f3e731385dd (20 octets)
OKM  = 0x2c91117204d745f3500d636a62f64f0a
       b3bae548aa53d423b0d1f27ebba6f5e5
       673a081d70cce7acfc48 (42 octets)
```

## 作者地址

- **Hugo Krawczyk** — IBM Research, 19 Skyline Drive, Hawthorne, NY 10532, USA. Email: hugokraw@us.ibm.com
- **Pasi Eronen** — Nokia Research Center, P.O. Box 407, FI-00045 Nokia Group, Finland. Email: pasi.eronen@nokia.com
