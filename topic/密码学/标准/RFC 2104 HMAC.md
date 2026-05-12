---
title: HMAC 基于哈希的消息认证
description: RFC 2104 - 描述使用密码学哈希函数进行消息认证的 HMAC 机制
tags:
  - 密码学
  - HMAC
  - 消息认证
  - RFC
---

# HMAC：基于哈希的消息认证 (Keyed-Hashing for Message Authentication)

> [!info] RFC 信息
> - **RFC 编号**：2104
> - **类别**：Informational
> - **发布日期**：1997 年 2 月
> - **作者**：H. Krawczyk (IBM)、M. Bellare (UCSD)、R. Canetti (IBM)

> [!abstract] 摘要
> 本文档描述 HMAC——一种使用密码学哈希函数进行消息认证的机制。HMAC 可与任何迭代式密码学哈希函数（如 MD5、SHA-1）配合使用，结合一个共享密钥。HMAC 的密码学强度取决于底层哈希函数的特性。

## 1. 引言

在开放计算和通信环境中，提供一种验证通过不可靠介质传输或存储的信息完整性的手段是首要需求。基于密钥提供此类完整性校验的机制通常称为"消息认证码"（MAC）。消息认证码通常用于共享密钥的两方之间，以验证双方之间传输的信息。

本文档提出一种基于密码学哈希函数的 MAC 机制。该机制称为 HMAC，基于作者在 [BCK1] 中的工作。关于 HMAC 的设计原理、安全性分析及其与其他 keyed-hash 方法的比较，请参阅该文献。

HMAC 可与任何迭代式密码学哈希函数结合使用。MD5 和 SHA-1 即为此类哈希函数的示例。HMAC 还使用一个密钥来计算和验证消息认证值。该构造的主要目标如下：

- **无需修改即可使用**现有哈希函数。尤其是那些在软件中性能良好、代码可自由获取且广泛使用的哈希函数。
- **保持哈希函数原有的性能**，不产生显著退化。
- **以简单的方式使用和处理密钥**。
- **在合理假设底层哈希函数的前提下**，对认证机制的密码学强度有清晰的分析。
- **允许轻松替换底层哈希函数**，以应对更快或更安全的哈希函数的出现。

本文档使用通用密码学哈希函数（记为 H）来定义 HMAC。HMAC 的具体实例化需要指定特定的哈希函数。当前候选哈希函数包括 SHA-1 [SHA]、MD5 [MD5]、RIPEMD-128/160 [RIPEMD]。这些不同的 HMAC 实现分别记为 HMAC-SHA1、HMAC-MD5、HMAC-RIPEMD 等。

> [!note] 关于 MD5 的说明
> 截至本文撰写时，MD5 和 SHA-1 是最广泛使用的密码学哈希函数。MD5 最近被发现易受碰撞搜索攻击 [Dobb]。此攻击及 MD5 的其他已知弱点并不影响 HMAC 中 MD5 的使用（参见 [Dobb]）；然而，SHA-1 似乎是密码学上更强的函数。迄今为止，对于 MD5 性能至关重要的应用，可以考虑在 HMAC 中使用 MD5。无论如何，实现者和使用者都需要关注这些密码学哈希函数可能的密码分析进展，以及最终替换底层哈希函数的需求（参见第 6 节）。

## 2. HMAC 定义

HMAC 的定义需要一个密码学哈希函数（记为 H）和一个密钥 K。假设 H 是一个通过迭代基本压缩函数处理数据块的密码学哈希函数。记 B 为此类数据块的字节长度（上述所有哈希函数示例中 B=64），L 为哈希输出的字节长度（MD5 为 L=16，SHA-1 为 L=20）。认证密钥 K 的长度可以是任意值，最大为 B（哈希函数的块长度）。使用超过 B 字节密钥的应用会先用 H 对密钥进行哈希，然后使用得到的 L 字节字符串作为 HMAC 的实际密钥。无论哪种情况，K 的最小推荐长度为 L 字节（即哈希输出长度）。关于密钥的更多信息参见第 3 节。

定义两个固定且不同的字符串 ipad 和 opad（'i' 和 'o' 分别代表 inner 和 outer）：

```
ipad = 字节 0x36 重复 B 次
opad = 字节 0x5C 重复 B 次
```

对数据 `text` 计算 HMAC 的过程如下：

```
H(K XOR opad, H(K XOR ipad, text))
```

具体步骤：

1. 在 K 末尾追加零，创建 B 字节字符串（例如，K 长度为 20 字节且 B=64，则追加 44 个零字节 0x00）
2. 将步骤 1 得到的 B 字节字符串与 ipad 进行 XOR（按位异或）运算
3. 将数据流 `text` 追加到步骤 2 得到的 B 字节字符串后
4. 对步骤 3 生成的流应用 H
5. 将步骤 1 得到的 B 字节字符串与 opad 进行 XOR 运算
6. 将步骤 4 的 H 结果追加到步骤 5 得到的 B 字节字符串后
7. 对步骤 6 生成的流应用 H，输出结果

> [!tip] 计算过程示意
> HMAC 本质上是两层哈希：先用密钥与内层 padding 异或后与消息一起哈希，再将结果与密钥和外层 padding 异或后再次哈希。

## 3. 密钥

HMAC 的密钥可以是任意长度（超过 B 字节的密钥会先用 H 哈希）。但是，强烈不建议使用少于 L 字节的密钥，因为这会降低函数的安全强度。超过 L 字节的密钥是可接受的，但额外长度不会显著增强函数强度（如果密钥的随机性被认为较弱，则建议使用更长的密钥）。

密钥应随机选择（或使用以随机种子初始化的密码学强伪随机数生成器），并定期刷新。（当前的攻击并未指明密钥更换的具体频率，因为这些攻击实际上是不可行的。然而，定期更换密钥是一项基本安全措施，有助于应对函数和密钥的潜在弱点，并限制密钥泄露的损害范围。）

## 4. 实现说明

HMAC 的定义方式使得底层哈希函数 H 无需修改代码即可使用。具体来说，它使用具有预定义初始值 IV 的函数 H（每个迭代哈希函数指定的固定值，用于初始化其压缩函数）。但是，如果需要，可以以（可能）修改 H 代码支持可变 IV 为代价来提升性能。

其思路是：在生成密钥 K 时或首次使用前，可以一次性预计算压缩函数对 B 字节块 (K XOR ipad) 和 (K XOR opad) 的中间结果。存储这些中间结果，然后在每次需要对消息进行认证时用它们来初始化 H 的 IV。此方法为每个认证消息节省了对两个 B 字节块应用 H 的压缩函数的开销（即 (K XOR ipad) 和 (K XOR opad)）。在认证短数据流时，这种节省可能非常可观。需要强调的是，存储的中间值必须像密钥一样受到同等保护和处理。

> [!warning] 安全提醒
> 存储的中间值需要与密钥同等对待和保护。

选择以上述方式实现 HMAC 是本地实现的决定，不影响互操作性。

## 5. 截断输出

消息认证码的一个常见做法是截断 MAC 的输出，仅输出部分比特（例如 [MM, ANSI]）。Preneel 和 van Oorschot [PV] 展示了截断基于哈希的 MAC 函数输出的一些分析优势。该领域的研究结果并非绝对肯定截断的整体安全优势。它有优点（攻击者可获得的哈希结果信息更少）也有缺点（攻击者需要预测的比特更少）。

HMAC 的应用可以选择通过输出 HMAC 计算结果的左 t 个比特来截断输出（即按第 2 节的正常方式计算，但最终结果截断为 t 比特）。建议输出长度 t 不小于哈希输出长度的一半（以匹配生日攻击界），且不小于 80 比特（攻击者需要预测的比特数的合理下界）。

使用哈希函数 H 输出 t 比特的 HMAC 实现记为 HMAC-H-t。例如，HMAC-SHA1-80 表示使用 SHA-1 函数且输出截断为 80 比特的 HMAC。（如果未指定参数 t，如 HMAC-MD5，则假定输出哈希的所有比特。）

## 6. 安全性

本文提出的消息认证机制的安全性取决于哈希函数 H 的密码学特性：抗碰撞能力（限于初始值保密且随机、函数输出不直接暴露给攻击者的情形），以及 H 的压缩函数应用于单块时的消息认证特性（在 HMAC 中这些块对攻击者而言是部分未知的，因为它们包含内层 H 计算的结果，攻击者无法完全选择）。

这些特性（实际上是更强的特性）通常被假设为 HMAC 所用哈希函数具有的性质。具体来说，如果不具备上述性质的哈希函数将不适合大多数（可能全部）密码学应用，包括基于此类函数的替代消息认证方案。（关于 HMAC 函数的完整分析和原理，请参阅 [BCK1]。）

鉴于目前对候选哈希函数密码学强度的信心有限，重要的是观察 HMAC 构造及其安全用于消息认证的以下两个特性：

1. **构造独立于特定哈希函数**——H 的细节可以替换为任何其他安全的（迭代式）密码学哈希函数。
2. **消息认证与加密不同，具有"暂时性"效果**。消息认证方案的破解被公布后将导致该方案的替换，但不会对过去已认证的信息产生不利影响。这与加密形成鲜明对比——今天加密的信息在未来加密算法被破解时可能面临暴露风险。

> [!tip] 关键安全特性
> HMAC 的一个重要安全属性是：即使底层哈希函数被攻破，过去使用该函数认证的消息仍然安全。这与加密形成对比——加密数据的机密性可能在算法被破解后受到威胁。

已知针对 HMAC 的最强攻击基于哈希函数 H 的碰撞频率（"生日攻击"）[PV,BCK2]，对于最低限度合理的哈希函数来说完全不可行。

举例来说，考虑输出长度为 L=16 字节（128 比特）的哈希函数如 MD5，攻击者需要获取约 2^64 个已知明文上计算的（使用**同一密钥** K！）正确消息认证标签。这需要处理至少 2^64 个 H 的块，在任何现实场景中都是不可能的（对于 64 字节的块长度，在 1Gbps 链路上持续传输需要 250,000 年，且在此期间不更换密钥 K）。此攻击只有在发现函数 H 碰撞行为的严重缺陷（如在 2^30 条消息后找到碰撞）时才可能变得现实。这种发现将意味着需要立即替换函数 H（这种失败对 H 在[[数字签名]]、公钥证书等传统用途中的影响将更为严重）。

> [!warning] 生日攻击 vs. 碰撞攻击
> 此攻击需要与不涉及密钥的密码学哈希函数的常规碰撞攻击严格区分。后者仅需 2^64 次可并行离线操作即可找到碰撞，正逐渐变得可行 [VW]，而 HMAC 上的生日攻击是完全不现实的。（在上例中，如果使用输出为 160 比特的哈希函数，2^64 应替换为 2^80。）

上述构造的正确实现、随机（或密码学伪随机）密钥的选择、安全的[[密钥交换]]机制、频繁的密钥刷新以及良好的密钥保密保护，都是 HMAC 提供的完整性验证机制安全性的必要条件。

## 附录——示例代码

以下提供 HMAC-MD5 的实现示例代码及相应的测试向量（代码基于 [MD5] 中描述的 MD5 代码）。

```c
/*
** 函数：hmac_md5
*/

void
hmac_md5(text, text_len, key, key_len, digest)
unsigned char*  text;                /* 指向数据流的指针 */
int             text_len;            /* 数据流长度 */
unsigned char*  key;                 /* 指向认证密钥的指针 */
int             key_len;             /* 认证密钥长度 */
caddr_t         digest;              /* 调用者的摘要缓冲区 */

{
        MD5_CTX context;
        unsigned char k_ipad[65];    /* 内层填充 -
                                      * 密钥与 ipad 异或
                                      */
        unsigned char k_opad[65];    /* 外层填充 -
                                      * 密钥与 opad 异或
                                      */
        unsigned char tk[16];
        int i;
        /* 如果密钥超过 64 字节，将其重置为 key=MD5(key) */
        if (key_len > 64) {

                MD5_CTX      tctx;

                MD5Init(&tctx);
                MD5Update(&tctx, key, key_len);
                MD5Final(tk, &tctx);

                key = tk;
                key_len = 16;
        }

        /*
         * HMAC_MD5 变换如下：
         *
         * MD5(K XOR opad, MD5(K XOR ipad, text))
         *
         * 其中 K 是 n 字节密钥
         * ipad 是字节 0x36 重复 64 次
         * opad 是字节 0x5c 重复 64 次
         * text 是受保护的数据
         */

        /* 将密钥存入填充数组 */
        bzero( k_ipad, sizeof k_ipad);
        bzero( k_opad, sizeof k_opad);
        bcopy( key, k_ipad, key_len);
        bcopy( key, k_opad, key_len);

        /* 密钥与 ipad 和 opad 异或 */
        for (i=0; i<64; i++) {
                k_ipad[i] ^= 0x36;
                k_opad[i] ^= 0x5c;
        }
        /*
         * 执行内层 MD5
         */
        MD5Init(&context);                   /* 初始化第一次遍历的上下文 */
        MD5Update(&context, k_ipad, 64)      /* 从内层填充开始 */
        MD5Update(&context, text, text_len); /* 然后处理数据 */
        MD5Final(digest, &context);          /* 完成第一次遍历 */
        /*
         * 执行外层 MD5
         */
        MD5Init(&context);                   /* 初始化第二次遍历的上下文 */
        MD5Update(&context, k_opad, 64);     /* 从外层填充开始 */
        MD5Update(&context, digest, 16);     /* 然后处理第一次哈希结果 */
        MD5Final(digest, &context);          /* 完成第二次遍历 */
}
```

### 测试向量

测试字符串的尾部 '\0' 不包含在测试中：

```
key =         0x0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b
key_len =     16 bytes
data =        "Hi There"
data_len =    8  bytes
digest =      0x9294727a3638bb1c13f48ef8158bfc9d

key =         "Jefe"
data =        "what do ya want for nothing?"
data_len =    28 bytes
digest =      0x750c783e6ab0b503eaa86e310a5db738

key =         0xAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
key_len       16 bytes
data =        0xDDDDDDDDDDDDDDDDDDDD...
              ..DDDDDDDDDDDDDDDDDDDD...
              ..DDDDDDDDDDDDDDDDDDDD...
              ..DDDDDDDDDDDDDDDDDDDD...
              ..DDDDDDDDDDDDDDDDDDDD
data_len =    50 bytes
digest =      0x56be34521d144c88dbb8c733f0e8b3f6
```

## 致谢

Pau-Chen Cheng、Jeff Kraemer 和 Michael Oehler 对早期草案提供了有益的评论，并进行了该规范的首次互操作性测试。Jeff 和 Pau-Chen 友好地提供了附录中的示例代码和测试向量。Burt Kaliski、Bart Preneel、Matt Robshaw、Adi Shamir 和 Paul van Oorschot 在 HMAC 构造的研究过程中提供了有益的评论和建议。

## 参考文献

- \[ANSI] ANSI X9.9, "American National Standard for Financial Institution Message Authentication (Wholesale)," American Bankers Association, 1981. Revised 1986.
- \[Atk] Atkinson, R., "IP Authentication Header", RFC 1826, August 1995.
- \[BCK1] M. Bellare, R. Canetti, and H. Krawczyk, "Keyed Hash Functions and Message Authentication", Proceedings of Crypto'96, LNCS 1109, pp. 1-15.
- \[BCK2] M. Bellare, R. Canetti, and H. Krawczyk, "Pseudorandom Functions Revisited: The Cascade Construction", Proceedings of FOCS'96.
- \[Dobb] H. Dobbertin, "The Status of MD5 After a Recent Attack", RSA Labs' CryptoBytes, Vol. 2 No. 2, Summer 1996.
- \[PV] B. Preneel and P. van Oorschot, "Building fast MACs from hash functions", Advances in Cryptology — CRYPTO'95 Proceedings, Lecture Notes in Computer Science, Springer-Verlag Vol.963, 1995, pp. 1-14.
- \[MD5] Rivest, R., "The MD5 Message-Digest Algorithm", RFC 1321, April 1992.
- \[MM] Meyer, S. and Matyas, S.M., Cryptography, New York Wiley, 1982.
- \[RIPEMD] H. Dobbertin, A. Bosselaers, and B. Preneel, "RIPEMD-160: A strengthened version of RIPEMD", Fast Software Encryption, LNCS Vol 1039, pp. 71-82.
- \[SHA] NIST, FIPS PUB 180-1: Secure Hash Standard, April 1995.
- \[Tsu] G. Tsudik, "Message authentication with one-way hash functions", In Proceedings of Infocom'92, May 1992.
- \[VW] P. van Oorschot and M. Wiener, "Parallel Collision Search with Applications to Hash Functions and Discrete Logarithms", Proceedings of the 2nd ACM Conf. Computer and Communications Security, Fairfax, VA, November 1994.

## 作者地址

- **Hugo Krawczyk** — IBM T.J. Watson Research Center, P.O.Box 704, Yorktown Heights, NY 10598. Email: hugo@watson.ibm.com
- **Mihir Bellare** — Dept of Computer Science and Engineering, Mail Code 0114, University of California at San Diego, 9500 Gilman Drive, La Jolla, CA 92093. Email: mihir@cs.ucsd.edu
- **Ran Canetti** — IBM T.J. Watson Research Center, P.O.Box 704, Yorktown Heights, NY 10598. Email: canetti@watson.ibm.com
