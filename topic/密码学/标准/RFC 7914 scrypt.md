---
title: scrypt 基于密码的密钥派生
description: RFC 7914 - scrypt 基于内存困难函数的密码密钥派生算法
tags:
  - 密码学
  - scrypt
  - 密钥派生
  - 内存困难
  - PBKDF
  - RFC
---

# scrypt：基于密码的密钥派生函数 (Password-Based Key Derivation Function)

> [!info] RFC 信息
> - **RFC 编号**：7914
> - **类别**：Informational
> - **发布日期**：2016 年 8 月
> - **作者**：C. Percival (Tarsnap)、S. Josefsson (SJD AB)

> [!abstract] 摘要
> 本文档指定了基于密码[[的密钥派生函数]] scrypt。该函数从一个秘密字符串派生一个或多个密钥。它基于内存困难函数 (Memory-Hard Function)，提供了针对使用定制硬件攻击的额外保护。文档还提供了 [[ASN.1]] 模式。

## 1. 引言

基于密码[[的密钥派生函数]]用于密码学和安全协议中，从一个秘密值派生一个或多个密钥。多年来，使用了几种基于密码[[的密钥派生函数]]，包括原始的基于 DES 的 UNIX Crypt 函数、FreeBSD MD5 crypt、[[PKCS#5 PBKDF2]] [RFC2898]（通常使用 SHA-1）、GNU SHA-256/512 crypt [SHA2CRYPT]、Windows NTLM 哈希和基于 Blowfish 的 bcrypt [BCRYPT]。这些算法都基于一个密码学原语结合加盐和/或迭代。迭代计数用于减慢计算速度，盐值用于增加预计算的成本。

> [!warning] 传统 KDF 的弱点
> 上述所有基于密码[[的密钥派生函数]]面对强大攻击者都有相同的弱点：即使增加迭代次数以保持合法用户的计算时间不变，使用定制硬件并行实现的暴力破解成本每年仍在下降——因为半导体技术发展使电路不仅更快，也更小，允许在相同成本下实现更多并行性。

scrypt 函数旨在减少攻击者通过使用定制设计的并行电路来破解基于密码[[的密钥派生函数]]所能获得的优势。

本文档不是首次引入 scrypt。原始 scrypt 论文 [SCRYPT] 已作为同行评审的科学论文发表。本文档的目的是为使用 scrypt 的文档提供稳定参考。

## 2. scrypt 参数

scrypt 函数接受多个参数：

- **P** — 密码短语 (Passphrase)，通常是用户选择的密码
- **S** — 盐值 (Salt)，通常唯一且随机生成 [RFC4086]
- **r** — 块大小参数 ("blockSize")
- **N** — CPU/内存代价参数 ("costParameter")，必须大于 1，是 2 的幂，且小于 2^(128 × r / 8)
- **p** — 并行化参数 ("parallelizationParameter")，正整数，小于等于 ((2^32-1) × 32) / (128 × r)
- **dkLen** — 派生密钥的字节长度 ("keyLength")，正整数，小于等于 (2^32 - 1) × 32

用户可以根据可用的内存和计算能力、内存子系统的延迟-带宽乘积以及所需的并行度来调整参数 N、r 和 p。当前，r=8 和 p=1 能产生良好结果，但随着内存延迟和 CPU 并行度增加，两者的最优值可能会增大。

> [!tip] 参数调整
> 由于 SMix 的计算是独立的，可以使用较大的 p 值来增加 scrypt 的计算成本而不增加内存使用量。因此，即使 CPU 功率和内存容量的增长率出现分化，scrypt 仍有望保持实用性。

## 3. Salsa20/8 Core 函数

Salsa20/8 Core 是 Salsa20 Core 的减少轮次变体。它是从 64 字节字符串到 64 字节字符串的哈希函数。注意 Salsa20/8 Core **不是**密码学哈希函数，因为它不抗碰撞。

```c
#define R(a,b) (((a) << (b)) | ((a) >> (32 - (b))))
void salsa20_word_specification(uint32 out[16],uint32 in[16])
{
  int i;
  uint32 x[16];
  for (i = 0;i < 16;++i) x[i] = in[i];
  for (i = 8;i > 0;i -= 2) {
    x[ 4] ^= R(x[ 0]+x[12], 7);  x[ 8] ^= R(x[ 4]+x[ 0], 9);
    x[12] ^= R(x[ 8]+x[ 4],13);  x[ 0] ^= R(x[12]+x[ 8],18);
    x[ 9] ^= R(x[ 5]+x[ 1], 7);  x[13] ^= R(x[ 9]+x[ 5], 9);
    x[ 1] ^= R(x[13]+x[ 9],13);  x[ 5] ^= R(x[ 1]+x[13],18);
    x[14] ^= R(x[10]+x[ 6], 7);  x[ 2] ^= R(x[14]+x[10], 9);
    x[ 6] ^= R(x[ 2]+x[14],13);  x[10] ^= R(x[ 6]+x[ 2],18);
    x[ 3] ^= R(x[15]+x[11], 7);  x[ 7] ^= R(x[ 3]+x[15], 9);
    x[11] ^= R(x[ 7]+x[ 3],13);  x[15] ^= R(x[11]+x[ 7],18);
    x[ 1] ^= R(x[ 0]+x[ 3], 7);  x[ 2] ^= R(x[ 1]+x[ 0], 9);
    x[ 3] ^= R(x[ 2]+x[ 1],13);  x[ 0] ^= R(x[ 3]+x[ 2],18);
    x[ 6] ^= R(x[ 5]+x[ 4], 7);  x[ 7] ^= R(x[ 6]+x[ 5], 9);
    x[ 4] ^= R(x[ 7]+x[ 6],13);  x[ 5] ^= R(x[ 4]+x[ 7],18);
    x[11] ^= R(x[10]+x[ 9], 7);  x[ 8] ^= R(x[11]+x[10], 9);
    x[ 9] ^= R(x[ 8]+x[11],13);  x[10] ^= R(x[ 9]+x[ 8],18);
    x[12] ^= R(x[15]+x[14], 7);  x[13] ^= R(x[12]+x[15], 9);
    x[14] ^= R(x[13]+x[12],13);  x[15] ^= R(x[14]+x[13],18);
  }
  for (i = 0;i < 16;++i) out[i] = x[i] + in[i];
}
```

## 4. scryptBlockMix 算法

scryptBlockMix 算法与 [SCRYPT] 中描述的 BlockMix 算法相同，但使用 Salsa20/8 Core 作为哈希函数 H。

```
算法 scryptBlockMix

参数：
         r       块大小参数。

输入：
         B[0] || B[1] || ... || B[2 * r - 1]
                输入字节字符串（128 * r 字节），
                视为 2 * r 个 64 字节块，
                其中 B 的每个元素是 64 字节块。

输出：
         B'[0] || B'[1] || ... || B'[2 * r - 1]
                输出字节字符串。

步骤：

  1. X = B[2 * r - 1]

  2. for i = 0 to 2 * r - 1 do
       T = X xor B[i]
       X = Salsa (T)
       Y[i] = X
     end for

  3. B' = (Y[0], Y[2], ..., Y[2 * r - 2],
           Y[1], Y[3], ..., Y[2 * r - 1])
```

## 5. scryptROMix 算法

scryptROMix 算法与 [SCRYPT] 中描述的 ROMix 算法相同，但使用 scryptBlockMix 作为哈希函数 H。

```
算法 scryptROMix

输入：
         r       块大小参数。
         B       输入字节向量，长度 128 * r 字节。
         N       CPU/内存代价参数，必须大于 1，
                 是 2 的幂，且小于 2^(128 * r / 8)。

输出：
         B'      输出字节向量，长度 128 * r 字节。

步骤：

  1. X = B

  2. for i = 0 to N - 1 do
       V[i] = X
       X = scryptBlockMix (X)
     end for

  3. for i = 0 to N - 1 do
       j = Integerify (X) mod N
              其中 Integerify (B[0] ... B[2 * r - 1]) 定义为
              将 B[2 * r - 1] 解释为小端整数的结果。
       T = X xor V[j]
       X = scryptBlockMix (T)
     end for

  4. B' = X
```

> [!tip] ROMix 的核心思想
> ROMix 分两阶段工作：第一阶段顺序填充内存（N 个块），第二阶段伪随机地从内存中读取并混合。这种"顺序写-随机读"的模式正是 scrypt 抵抗专用硬件攻击的关键——攻击者必须拥有足够的内存才能高效计算。

## 6. scrypt 算法

以下使用的 PBKDF2-HMAC-SHA-256 表示使用 HMAC-SHA-256 [RFC6234] 作为伪随机函数 (PRF) 的 PBKDF2 算法 [RFC2898]。HMAC-SHA-256 函数生成 32 字节输出。

```
算法 scrypt

输入：
         P       密码短语，字节字符串。
         S       盐值，字节字符串。
         N       CPU/内存代价参数。
         r       块大小参数。
         p       并行化参数。
         dkLen   派生密钥的字节长度。

输出：
         DK      派生密钥，长度 dkLen 字节。

步骤：

 1. 初始化由 p 个块组成的数组 B，每块 128 * r 字节：
     B[0] || B[1] || ... || B[p - 1] =
       PBKDF2-HMAC-SHA256 (P, S, 1, p * 128 * r)

 2. for i = 0 to p - 1 do
       B[i] = scryptROMix (r, B[i], N)
     end for

 3. DK = PBKDF2-HMAC-SHA256 (P, B[0] || B[1] || ... || B[p - 1],
                              1, dkLen)
```

> [!tip] scrypt 三层结构
> scrypt 的设计是三层嵌套：外层用 PBKDF2 处理密码和盐值，中间层用 ROMix 进行内存困难的混合，内层用 BlockMix/Salsa20/8 进行块级混淆。这种结构确保了大量的内存访问和顺序依赖性。

## 7. ASN.1 语法

本节定义了 scrypt 密钥派生函数的 [[ASN.1]] 语法，旨在与 PKCS#5 的 PBKDF2 在同一抽象级别上操作。

```asn1
id-scrypt OBJECT IDENTIFIER ::= {1 3 6 1 4 1 11591 4 11}

scrypt-params ::= SEQUENCE {
       salt OCTET STRING,
       costParameter INTEGER (1..MAX),
       blockSize INTEGER (1..MAX),
       parallelizationParameter INTEGER (1..MAX),
       keyLength INTEGER (1..MAX) OPTIONAL }
```

scrypt-params 各字段的含义：

- **salt** — 盐值，字节字符串
- **costParameter** — CPU/内存代价参数 N
- **blockSize** — 块大小参数 r
- **parallelizationParameter** — 并行化参数 p
- **keyLength**（可选）— 派生密钥的字节长度

### 7.1. ASN.1 模块

```asn1
-- scrypt ASN.1 Module

scrypt-0 {1 3 6 1 4 1 11591 4 10}

DEFINITIONS ::= BEGIN

id-scrypt OBJECT IDENTIFIER ::= {1 3 6 1 4 1 11591 4 11}

scrypt-params ::= SEQUENCE {
    salt OCTET STRING,
    costParameter INTEGER (1..MAX),
    blockSize INTEGER (1..MAX),
    parallelizationParameter INTEGER (1..MAX),
    keyLength INTEGER (1..MAX) OPTIONAL
}

PBES2-KDFs ALGORITHM-IDENTIFIER ::=
       { {scrypt-params IDENTIFIED BY id-scrypt}, ... }

END
```

## 8. Salsa20/8 Core 测试向量

```
INPUT:
7e 87 9a 21 4f 3e c9 86 7c a9 40 e6 41 71 8f 26
ba ee 55 5b 8c 61 c1 b5 0d f8 46 11 6d cd 3b 1d
ee 24 f3 19 df 9b 3d 85 14 12 1e 4b 5a c5 aa 32
76 02 1d 29 09 c7 48 29 ed eb c6 8d b8 b8 c2 5e

OUTPUT:
a4 1f 85 9c 66 08 cc 99 3b 81 ca cb 02 0c ef 05
04 4b 21 81 a2 fd 33 7d fd 7b 1c 63 96 68 2f 29
b4 39 31 68 e3 c9 e6 bc fe 6b c5 b7 a0 6d 96 ba
e4 24 cc 10 2c 91 74 5c 24 ad 67 3d c7 61 8f 81
```

## 9. scryptBlockMix 测试向量

```
INPUT
B[0] =  f7 ce 0b 65 3d 2d 72 a4 10 8c f5 ab e9 12 ff dd
        77 76 16 db bb 27 a7 0e 82 04 f3 ae 2d 0f 6f ad
        89 f6 8f 48 11 d1 e8 7b cc 3b d7 40 0a 9f fd 29
        09 4f 01 84 63 95 74 f3 9a e5 a1 31 52 17 bc d7

B[1] =  89 49 91 44 72 13 bb 22 6c 25 b5 4d a8 63 70 fb
        cd 98 43 80 37 46 66 bb 8f fc b5 bf 40 c2 54 b0
        67 d2 7c 51 ce 4a d5 fe d8 29 c9 0b 50 5a 57 1b
        7f 4d 1c ad 6a 52 3c da 77 0e 67 bc ea af 7e 89

OUTPUT
B'[0] = a4 1f 85 9c 66 08 cc 99 3b 81 ca cb 02 0c ef 05
        04 4b 21 81 a2 fd 33 7d fd 7b 1c 63 96 68 2f 29
        b4 39 31 68 e3 c9 e6 bc fe 6b c5 b7 a0 6d 96 ba
        e4 24 cc 10 2c 91 74 5c 24 ad 67 3d c7 61 8f 81

B'[1] = 20 ed c9 75 32 38 81 a8 05 40 f6 4c 16 2d cd 3c
        21 07 7c fe 5f 8d 5f e2 b1 a4 16 8f 95 36 78 b7
        7d 3b 3d 80 3b 60 e4 ab 92 09 96 e5 9b 4d 53 b6
        5d 2a 22 58 77 d5 ed f5 84 2c b9 f1 4e ef e4 25
```

## 10. scryptROMix 测试向量

```
INPUT:
B = f7 ce 0b 65 3d 2d 72 a4 10 8c f5 ab e9 12 ff dd
    77 76 16 db bb 27 a7 0e 82 04 f3 ae 2d 0f 6f ad
    89 f6 8f 48 11 d1 e8 7b cc 3b d7 40 0a 9f fd 29
    09 4f 01 84 63 95 74 f3 9a e5 a1 31 52 17 bc d7
    89 49 91 44 72 13 bb 22 6c 25 b5 4d a8 63 70 fb
    cd 98 43 80 37 46 66 bb 8f fc b5 bf 40 c2 54 b0
    67 d2 7c 51 ce 4a d5 fe d8 29 c9 0b 50 5a 57 1b
    7f 4d 1c ad 6a 52 3c da 77 0e 67 bc ea af 7e 89

OUTPUT:
B = 79 cc c1 93 62 9d eb ca 04 7f 0b 70 60 4b f6 b6
    2c e3 dd 4a 96 26 e3 55 fa fc 61 98 e6 ea 2b 46
    d5 84 13 67 3b 99 b0 29 d6 65 c3 57 60 1f b4 26
    a0 b2 f4 bb a2 00 ee 9f 0a 43 d1 9b 57 1a 9c 71
    ef 11 42 e6 5d 5a 26 6f dd ca 83 2c e5 9f aa 7c
    ac 0b 9c f1 be 2b ff ca 30 0d 01 ee 38 76 19 c4
    ae 12 fd 44 38 f2 03 a0 e4 e1 c4 7e c3 14 86 1f
    4e 90 87 cb 33 39 6a 68 73 e8 f9 d2 53 9a 4b 8e
```

## 11. PBKDF2-HMAC-SHA-256 测试向量

```
PBKDF2-HMAC-SHA-256 (P="passwd", S="salt",
                     c=1, dkLen=64) =
55 ac 04 6e 56 e3 08 9f ec 16 91 c2 25 44 b6 05
f9 41 85 21 6d de 04 65 e6 8b 9d 57 c2 0d ac bc
49 ca 9c cc f1 79 b6 45 99 16 64 b3 9d 77 ef 31
7c 71 b8 45 b1 e3 0b d5 09 11 20 41 d3 a1 97 83

PBKDF2-HMAC-SHA-256 (P="Password", S="NaCl",
                     c=80000, dkLen=64) =
4d dc d8 f6 0b 98 be 21 83 0c ee 5e f2 27 01 f9
64 1a 44 18 d0 4c 04 14 ae ff 08 87 6b 34 ab 56
a1 d4 25 a1 22 58 33 54 9a db 84 1b 51 c9 b3 17
6a 27 2b de bb a1 d0 78 47 8f 62 b3 97 f3 3c 8d
```

## 12. scrypt 测试向量

```
scrypt (P="", S="",
        N=16, r=1, p=1, dklen=64) =
77 d6 57 62 38 65 7b 20 3b 19 ca 42 c1 8a 04 97
f1 6b 48 44 e3 07 4a e8 df df fa 3f ed e2 14 42
fc d0 06 9d ed 09 48 f8 32 6a 75 3a 0f c8 1f 17
e8 d3 e0 fb 2e 0d 36 28 cf 35 e2 0c 38 d1 89 06

scrypt (P="password", S="NaCl",
        N=1024, r=8, p=16, dkLen=64) =
fd ba be 1c 9d 34 72 00 78 56 e7 19 0d 01 e9 fe
7c 6a d7 cb c8 23 78 30 e7 73 76 63 4b 37 31 62
2e af 30 d9 2e 22 a3 88 6f f1 09 27 9d 98 30 da
c7 27 af b9 4a 83 ee 6d 83 60 cb df a2 cc 06 40

scrypt (P="pleaseletmein", S="SodiumChloride",
        N=16384, r=8, p=1, dkLen=64) =
70 23 bd cb 3a fd 73 48 46 1c 06 cd 81 fd 38 eb
fd a8 fb ba 90 4f 8e 3e a9 b5 43 f6 54 5d a1 f2
d5 43 29 55 61 3f 0f cf 62 d4 97 05 24 2a 9a f9
e6 1e 85 dc 0d 65 1e 40 df cf 01 7b 45 57 58 87

scrypt (P="pleaseletmein", S="SodiumChloride",
        N=1048576, r=8, p=1, dkLen=64) =
21 01 cb 9b 6a 51 1a ae ad db be 09 cf 70 f8 81
ec 56 8d 57 4a 2f fd 4d ab e5 ee 98 20 ad aa 47
8e 56 fd 8f 4b a5 d0 9f fa 1c 6d 92 7c 40 f4 c3
37 30 40 49 e8 a9 52 fb cb f4 5c 6f a7 7a 41 a4
```

## 13. PKCS#8 测试向量

使用 PBES2 以 scrypt 作为 KDF，以下展示一个 [[PKCS#8]] 编码的私钥示例。密码为 "Rabbit"，N=1048576，r=8，p=1。盐值为 "Mouse"，加密算法为 aes256-CBC。

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
MIHiME0GCSqGSIb3DQEFDTBAMB8GCSsGAQQB2kcECzASBAVNb3VzZQIDEAAAAgEI
AgEBMB0GCWCGSAFlAwQBKgQQyYmguHMsOwzGMPoyObk/JgSBkJb47EWd5iAqJlyy
+ni5ftd6gZgOPaLQClL7mEZc2KQay0VhjZm/7MbBUNbqOAXNM6OGebXxVp6sHUAL
iBGY/Dls7B1TsWeGObE0sS1MXEpuREuloZjcsNVcNXWPlLdZtkSH6uwWzR0PyG/Z
+ZXfNodZtd/voKlvLOw5B3opGIFaLkbtLZQwMiGtl42AS89lZg==
-----END ENCRYPTED PRIVATE KEY-----
```

## 14. 安全考虑

本文档指定了一种密码学算法，始终存在被发现弱点的风险。通过跟踪密码学研究领域，可以了解与 scrypt 相关的出版物。

ROMix 已在随机预言机模型下被证明是顺序内存困难的。scrypt 的安全性依赖于一个假设：使用 Salsa20/8 Core 的 BlockMix 不存在任何允许比随机预言机更容易迭代的"捷径"。

> [!warning] 安全注意事项
> - 密码和其他敏感数据（如中间值）在实现处理完毕后可能长期存在于内存、核心转储、交换区等中。实现应考虑将敏感数据存储在受保护的内存区域中。
> - scrypt 算法根据参数可能需要大量内存。系统应防止攻击者提供不合理大的参数导致的拒绝服务攻击。
> - 不良的参数选择可能对安全性有害——例如，如果将参数调整到内存使用量减小到很小的量，将影响算法的安全性属性。

## 15. 参考文献

### 15.1. 规范性引用

- \[RFC2898] Kaliski, B., "PKCS #5: Password-Based Cryptography Specification Version 2.0", RFC 2898, September 2000.
- \[RFC6234] Eastlake 3rd, D. and T. Hansen, "US Secure Hash Algorithms (SHA and SHA-based HMAC and HKDF)", RFC 6234, May 2011.

### 15.2. 资料性引用

- \[BCRYPT] Provos, N. and D. Mazieres, "A Future-Adaptable Password Scheme", USENIX 1999.
- \[NTLM] Microsoft, "[MS-NLMP]: NTLM Authentication Protocol", 2015.
- \[RFC20] Cerf, V., "ASCII format for network interchange", STD 80, RFC 20, October 1969.
- \[RFC4086] Eastlake 3rd, D., et al., "Randomness Requirements for Security", BCP 106, RFC 4086, June 2005.
- \[RFC5208] Kaliski, B., "PKCS #8: Private-Key Information Syntax Specification Version 1.2", RFC 5208, May 2008.
- \[RFC5958] Turner, S., "Asymmetric Key Packages", RFC 5958, August 2010.
- \[SALSA20CORE] Bernstein, D., "The Salsa20 Core", March 2005.
- \[SALSA20SPEC] Bernstein, D., "Salsa20 specification", April 2005.
- \[SCRYPT] Percival, C., "STRONGER KEY DERIVATION VIA SEQUENTIAL MEMORY-HARD FUNCTIONS", BSDCan'09, May 2009.
- \[SHA2CRYPT] Drepper, U., "Unix crypt using SHA-256 and SHA-512", April 2008.

## 致谢

本文档的文字借用自 [SCRYPT] 和 [RFC2898]。[[PKCS#8]] 测试向量由 Stephen N. Henson 提供。

## 作者地址

- **Colin Percival** — Tarsnap. Email: cperciva@tarsnap.com
- **Simon Josefsson** — SJD AB. Email: simon@josefsson.org

## 相关笔记

- [[标准]]
- [[PKCS#12 个人信息交换语法 v1.1]]
- [[PKCS#11 v3.0 Cryptoki]]
- [[PKCS#10 证书签名请求]]
- [["OpenPGP 消息格式"]]
- [["X.509 公钥基础设施证书与 CRL"]]
- [[密码消息语法 (CMS)]]
- [[RFC 5751 S/MIME 3.2 消息规范]]
