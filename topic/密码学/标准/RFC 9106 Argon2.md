---
title: RFC 9106 Argon2 密码哈希与密钥派生
description: RFC 9106 定义了 Argon2 memory-hard function，用于密码哈希和 proof-of-work 场景，包含 Argon2d、Argon2i、Argon2id 三种变体的完整规范、测试向量及安全分析。
tags:
  - 密码学
  - Argon2
  - 密钥派生
  - RFC
---

> [!info] RFC 信息
> **RFC 编号**：9106
> **标题**：Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications
> **类别**：Informational
> **发布日期**：2021 年 9 月
> **作者**：A. Biryukov (University of Luxembourg), D. Dinu (University of Luxembourg / Intel), D. Khovratovich (ABDK Consulting), S. Josefsson (SJD AB)
> **所属组织**：IRTF Crypto Forum Research Group (CFRG)

## 摘要

本文档描述了用于密码哈希和 proof-of-work（工作量证明）应用的 Argon2 memory-hard function（内存困难函数）。我们提供了面向实现者的描述及测试向量，旨在简化 Argon2 在互联网协议中的采用。本文档是 IRTF 中 Crypto Forum Research Group (CFRG) 的成果。

## 备忘录状态

本文档不是互联网标准跟踪规范；仅为信息参考目的而发布。

本文档是 Internet Research Task Force (IRTF) 的成果。IRTF 发布互联网相关研究和开发活动的结果，这些结果可能不适合直接部署。本 RFC 代表了 IRTF Crypto Forum Research Group 的共识。经 IRSG 批准发布的文档不是任何级别互联网标准的候选；参见 RFC 7841 第 2 节。

有关本文档当前状态、勘误及反馈方式的信息，可在 [https://www.rfc-editor.org/info/rfc9106](https://www.rfc-editor.org/info/rfc9106) 获取。

## 1. 引言

本文档描述了 Argon2 memory-hard function，用于密码哈希和 proof-of-work 应用。我们提供了面向实现者的描述及测试向量，旨在简化 Argon2 在互联网协议中的采用。本文档对应 Argon2 hash function 的 1.3 版本。

Argon2 是一个 memory-hard function（内存困难函数）。它采用精简设计，以最高的内存填充率和多计算单元的有效利用为目标，同时仍能防御 trade-off 攻击（权衡攻击）。Argon2 针对 x86 架构进行了优化，充分利用了最新 Intel 和 AMD 处理器的 cache（缓存）和内存组织方式。

Argon2 有一个主要变体 Argon2id，以及两个补充变体 Argon2d 和 Argon2i：

- **Argon2d** 使用 data-dependent memory access（数据依赖的内存访问），适用于不存在 side-channel timing attack（侧信道计时攻击）威胁的加密货币和 proof-of-work 应用
- **Argon2i** 使用 data-independent memory access（数据无关的内存访问），适合密码哈希和基于密码的密钥派生
- **Argon2id** 在第一次遍历内存的前半部分以 Argon2i 方式工作，后半部分以 Argon2d 方式工作，从而同时提供侧信道攻击保护和由 time-memory trade-off 带来的暴力破解成本提升。Argon2i 会进行更多次内存遍历以防御 trade-off 攻击

> [!warning] 实现要求
> 任何本文档的实现**必须**支持 Argon2id，而 Argon2d 和 Argon2i **可以**选择性支持。

Argon2 也是对固定输入长度压缩函数 G 和可变输入长度 hash function H 的一种操作模式。虽然 Argon2 理论上可以使用任何输出不超过 64 字节的函数 H，但本文档中使用 BLAKE2b ([RFC 7693](https://www.rfc-editor.org/info/rfc7693))。

有关更多背景和讨论，请参阅 [ARGON2]。

本文档代表了 Crypto Forum Research Group (CFRG) 的共识。

### 1.1. 约定术语

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"NOT RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按照 BCP 14 [RFC2119] [RFC8174] 的描述进行解释，且仅当它们以全部大写形式出现时适用。

## 2. 符号与约定

| 符号 | 含义 |
|------|------|
| `x^y` | 整数 x 的 y 次幂（x 自乘 y 次） |
| `a*b` | 整数 a 与整数 b 的乘积 |
| `c-d` | 整数 c 减去整数 d |
| `E_f` | 带下标索引 f 的变量 E |
| `g / h` | 整数 g 除以整数 h，结果为有理数 |
| `I(j)` | 函数 I 在 j 处的取值 |
| `K \|\| L` | 字符串 K 与字符串 L 的拼接 |
| `a XOR b` | 比特串 a 与 b 的按位异或 |
| `a mod b` | 整数 a 模整数 b 的余数，范围始终为 [0, b-1] |
| `a >>> n` | 64 位比特串 a 右旋转移 n 位 |
| `trunc(a)` | 64 位值截断为最低 32 位 |
| `floor(a)` | 不大于 a 的最大整数 |
| `ceil(a)` | 不小于 a 的最小整数 |
| `extract(a, i)` | 从比特串 a 中提取第 i 组 32 位（从第 0 组开始） |
| `\|A\|` | 集合 A 中元素的数量 |
| `LE32(a)` | 32 位整数 a 转换为 little-endian 字节串（例：123456 → `40 E2 01 00`） |
| `LE64(a)` | 64 位整数 a 转换为 little-endian 字节串（例：123456 → `40 E2 01 00 00 00 00 00`） |
| `int32(s)` | 32 位字符串 s 按 little-endian 转换为非负整数 |
| `int64(s)` | 64 位字符串 s 按 little-endian 转换为非负整数 |
| `length(P)` | 字符串 P 的字节长度，表示为 32 位整数 |
| `ZERO(P)` | P 字节的零字符串 |

## 3. Argon2 算法规范

### 3.1. 输入参数

Argon2 具有以下输入参数：

| 参数 | 类型 | 说明 |
|------|------|------|
| P | 字符串 | 密码（password） |
| S | 字符串 | Salt（盐值） |
| K | 字符串 | 密钥（secret key），可选 |
| X | 字符串 | 关联数据（associated data），可选 |
| L | 字符串 | Argon2 类型标识 |
| I | 整数 | 内存大小（以 KiB 为单位） |
| p | 整数 | 并行度（lane 数量） |
| T | 整数 | 输出 tag 长度（字节数） |
| v | 整数 | 版本号 |
| y | 整数 | Argon2 类型（0=d, 1=i, 2=id） |

Argon2 的输出称为 "tag"（标签），是一个 T 字节长的字符串。

### 3.2. Argon2 操作流程

Argon2 使用内部压缩函数 G（两个 1024 字节输入，一个 1024 字节输出）和内部 hash function `H^x()`（x 为输出字节数）。此处，`H^x()` 对字符串 A 的计算即为 BLAKE2b ([RFC 7693](https://www.rfc-editor.org/info/rfc7693), [Section 3.3](https://www.rfc-editor.org/rfc/rfc7693#section-3.3)) 函数，参数为 `(d, ll, kk=0, nn=x)`，其中 d 是 A 填充到 128 字节倍数后的值，ll 是 d 的字节长度。压缩函数 G 基于其内部置换。还使用了基于 H 构建的可变长度 hash function H'。G 在第 3.5 节中描述，H' 在第 3.3 节中描述。

Argon2 操作步骤如下：

**步骤 1**：建立 H_0 为以下 64 字节值。如果 K、X 或 S 长度为零，则省略其内容，但长度字段保留。

```
H_0 = H^(64)(LE32(p) || LE32(T) || LE32(m) ||
        LE32(t) || LE32(v) || LE32(y) || LE32(length(P)) || P ||
        LE32(length(S)) || S ||  LE32(length(K)) || K ||
        LE32(length(X)) || X)
```

**步骤 2**：分配 m' 个 1024 字节的内存块，m' 计算方式如下：

```
m' = 4 * p * floor (m / 4p)
```

对于 p 个 lane，内存组织为一个包含 p 行（lane）和 q = m' / p 列的块矩阵 B[i][j]。

**步骤 3**：对所有从 0（含）到 p（不含）的 i 计算 B[i][0]：

```
B[i][0] = H'^(1024)(H_0 || LE32(0) || LE32(i))
```

**步骤 4**：对所有从 0（含）到 p（不含）的 i 计算 B[i][1]：

```
B[i][1] = H'^(1024)(H_0 || LE32(1) || LE32(i))
```

**步骤 5**：对所有从 0（含）到 p（不含）的 i，以及所有从 2（含）到 q（不含）的 j，计算 B[i][j]。计算**必须**按 slice 顺序进行（参见第 3.4 节）：首先计算 slice 0 中所有 lane 的块（lane 顺序任意），然后计算 slice 1，依此类推。对每种 Argon2 变体（Argon2d、Argon2i、Argon2id），块索引 l 和 z 的确定方式不同。

```
B[i][j] = G(B[i][j-1], B[l][z])
```

**步骤 6**：如果遍历次数 t 大于 1，则重复。对所有从 0（含）到 p（不含）的 i，以及所有从 1（含）到 q（不含）的 j，计算 B[i][0] 和 B[i][j]。但此时块的计算方式不同——旧值与新值进行 XOR：

```
B[i][0] = G(B[i][q-1], B[l][z]) XOR B[i][0];
B[i][j] = G(B[i][j-1], B[l][z]) XOR B[i][j].
```

**步骤 7**：经过 t 次迭代后，最终块 C 计算为最后一列的 XOR：

```
C = B[0][q-1] XOR B[1][q-1] XOR ... XOR B[p-1][q-1]
```

**步骤 8**：输出 tag 计算为 `H'^T(C)`。

### 3.3. 变长哈希函数 H'

设 V_i 为 64 字节的块，W_i 为其前 32 字节。则函数 H' 定义如下：

```
if T <= 64
    H'^T(A) = H^T(LE32(T)||A)
else
    r = ceil(T/32)-2
    V_1 = H^(64)(LE32(T)||A)
    V_2 = H^(64)(V_1)
    ...
    V_r = H^(64)(V_{r-1})
    V_{r+1} = H^(T-32*r)(V_{r})
    H'^T(X) = W_1 || W_2 || ... || W_r || V_{r+1}
```

### 3.4. 内存组织与并行计算

为了支持并行块计算，我们将内存矩阵进一步划分为 SL = 4 个垂直 slice。一个 slice 与一个 lane 的交集称为 segment（段），长度为 q/SL。同一 slice 的 segment 可以并行计算，且不会互相引用。可以引用所有其他块。

```
slice 0    slice 1    slice 2    slice 3
  ___/\___   ___/\___   ___/\___   ___/\___
 /        \ /        \ /        \ /        \
+----------+----------+----------+----------+
|          |          |          |          | > lane 0
+----------+----------+----------+----------+
|          |          |          |          | > lane 1
+----------+----------+----------+----------+
|          |          |          |          | > lane 2
+----------+----------+----------+----------+
|         ...        ...        ...         | ...
+----------+----------+----------+----------+
|          |          |          |          | > lane p - 1
+----------+----------+----------+----------+
```

#### 3.4.1. 索引生成

##### 3.4.1.1. Argon2d 的索引生成

J_1 由块 B[i][j-1] 的前 32 位给出，J_2 由接下来的 32 位给出：

```
J_1 = int32(extract(B[i][j-1], 0))
J_2 = int32(extract(B[i][j-1], 1))
```

##### 3.4.1.2. Argon2i 的索引生成

对于每个 segment，我们执行以下操作。首先计算值 Z：

```
Z= ( LE64(r) || LE64(l) || LE64(sl) || LE64(m') ||
     LE64(t) || LE64(y) )
```

其中：

| 变量 | 含义 |
|------|------|
| r | 当前遍历编号（pass number） |
| l | lane 编号 |
| sl | slice 编号 |
| m' | 内存块总数 |
| t | 总遍历次数 |
| y | Argon2 类型（0=Argon2d, 1=Argon2i, 2=Argon2id） |

然后计算：

```
q/(128*SL) 1024-byte values
G(ZERO(1024),G(ZERO(1024),
Z || LE64(1) || ZERO(968) )),
G(ZERO(1024),G(ZERO(1024),
Z || LE64(2) || ZERO(968) )),... ,
G(ZERO(1024),G(ZERO(1024),
Z || LE64(q/(128*SL)) || ZERO(968) )),
```

这些值被划分为 q/(SL) 个 8 字节的值 X，视作 X1\|\|X2 并转换为 J_1=int32(X1) 和 J_2=int32(X2)。

值 r、l、sl、m'、t、y 和 i 以 8 字节 little-endian 表示。

##### 3.4.1.3. Argon2id 的索引生成

如果当前遍历编号为 0 且 slice 编号为 0 或 1，则按 Argon2i 方式计算 J_1 和 J_2；否则按 Argon2d 方式计算 J_1 和 J_2。

#### 3.4.2. 引用块索引映射

`l = J_2 mod p` 给出所取块的 lane 索引。对于第一次遍历（r=0）和第一个 slice（sl=0），块取自当前 lane。

集合 W 包含根据以下规则可引用的索引：

1. 如果 l 是当前 lane，则 W 包含最后 SL - 1 = 3 个已完成 segment 中所有块的索引，以及当前遍历中当前 segment 内已计算的块（排除 B[i][j-1]）。
2. 如果 l 不是当前 lane，则 W 包含 lane l 中最后 SL - 1 = 3 个已完成 segment 中所有块的索引。如果 B[i][j] 是某个 segment 的第一个块，则排除 W 中最后一个索引。

然后使用以下映射从 W 中按非均匀分布 [0, |W|) 选取一个块：

```
J_1 -> |W|(1 - J_1^2 / 2^(64))
```

> [!tip] 避免浮点计算
> 为避免浮点运算，使用以下近似：

```
x = J_1^2 / 2^(32)
y = (|W| * x) / 2^(32)
zz = |W| - 1 - y
```

然后取 W 中第 zz 个索引，即为引用块索引 [l][z] 的 z 值。

### 3.5. 压缩函数 G

压缩函数 G 基于以 BLAKE2b 为基础的变换 P 构建。P 对 128 字节的输入进行操作，可视为八个 16 字节寄存器：

```
P(A_0, A_1, ... ,A_7) = (B_0, B_1, ... ,B_7)
```

压缩函数 G(X, Y) 对两个 1024 字节的块 X 和 Y 进行操作。首先计算 R = X XOR Y。然后将 R 视为 16 字节寄存器 R_0, R_1, ..., R_63 的 8x8 矩阵。先对每行应用 P，再对每列应用 P，得到 Z：

```
( Q_0,  Q_1,  Q_2, ... ,  Q_7) <- P( R_0,  R_1,  R_2, ... ,  R_7)
( Q_8,  Q_9, Q_10, ... , Q_15) <- P( R_8,  R_9, R_10, ... , R_15)
                              ...
(Q_56, Q_57, Q_58, ... , Q_63) <- P(R_56, R_57, R_58, ... , R_63)
( Z_0,  Z_8, Z_16, ... , Z_56) <- P( Q_0,  Q_8, Q_16, ... , Q_56)
( Z_1,  Z_9, Z_17, ... , Z_57) <- P( Q_1,  Q_9, Q_17, ... , Q_57)
                              ...
( Z_7, Z_15, Z 23, ... , Z_63) <- P( Q_7, Q_15, Q_23, ... , Q_63)
```

最终，G 输出 Z XOR R：

```
G: (X, Y) -> R -> Q -> Z -> Z XOR R
```

```
+---+       +---+
| X |       | Y |
+---+       +---+
  |           |
  ---->XOR<----
--------|
|      \ /
|     +---+
|     | R |
|     +---+
|       |
|      \ /
|   P rowwise
|       |
|      \ /
|     +---+
|     | Q |
|     +---+
|       |
|      \ /
|  P columnwise
|       |
|      \ /
|     +---+
|     | Z |
|     +---+
|       |
|      \ /
------>XOR
        |
       \ /
```

### 3.6. 置换函数 P

置换 P 基于 BLAKE2b 的轮函数。八个 16 字节输入 S_0, S_1, ..., S_7 被视为 64 位字的 4x4 矩阵，其中 S_i = (v_{2*i+1} \|\| v_{2*i})：

```
v_0  v_1  v_2  v_3
 v_4  v_5  v_6  v_7
 v_8  v_9 v_10 v_11
v_12 v_13 v_14 v_15
```

操作流程如下：

```
GB(v_0, v_4,  v_8, v_12)
GB(v_1, v_5,  v_9, v_13)
GB(v_2, v_6, v_10, v_14)
GB(v_3, v_7, v_11, v_15)

GB(v_0, v_5, v_10, v_15)
GB(v_1, v_6, v_11, v_12)
GB(v_2, v_7,  v_8, v_13)
GB(v_3, v_4,  v_9, v_14)
```

GB(a, b, c, d) 定义如下：

```
a = (a + b + 2 * trunc(a) * trunc(b)) mod 2^(64)
d = (d XOR a) >>> 32
c = (c + d + 2 * trunc(c) * trunc(d)) mod 2^(64)
b = (b XOR c) >>> 24

a = (a + b + 2 * trunc(a) * trunc(b)) mod 2^(64)
d = (d XOR a) >>> 16
c = (c + d + 2 * trunc(c) * trunc(d)) mod 2^(64)
b = (b XOR c) >>> 63
```

> [!note] 与 BLAKE2b 的区别
> GB 中的模加法结合了 64 位乘法。乘法是唯一与原始 BLAKE2b 设计不同的部分。这一选择是为了增加电路深度，从而增加 ASIC 实现的运行时间，同时由于 CPU 的并行性和流水线特性，对 CPU 上的运行时间影响不大。

## 4. 参数选择建议

Argon2d 适用于攻击者无法常规访问系统内存或 CPU 的场景，即他们无法基于计时信息进行侧信道攻击，也无法通过垃圾回收更快地恢复密码。这些场景更典型地出现在后端服务器和加密货币挖矿中。对于实际应用，我们建议以下设置：

- **加密货币挖矿**（在 2 GHz CPU 上使用 1 核心耗时 0.1 秒）—— Argon2d，2 个 lane，250 MB RAM

Argon2id 适用于更现实的场景，即攻击者可能访问同一台机器、使用其 CPU 或发动冷启动攻击。我们建议以下设置：

- **后端服务器认证**（在 2 GHz CPU 上使用 4 核心耗时 0.5 秒）—— Argon2id，8 个 lane，4 GiB RAM
- **硬盘加密的密钥派生**（在 2 GHz CPU 上使用 2 核心耗时 3 秒）—— Argon2id，4 个 lane，6 GiB RAM
- **前端服务器认证**（在 2 GHz CPU 上使用 2 核心耗时 0.5 秒）—— Argon2id，4 个 lane，1 GiB RAM

> [!tip] 推荐参数选择流程
> 我们推荐以下流程来选择 Argon2 的类型和参数：

1. **如果可以接受一个通用安全选项**（不针对特定应用或硬件调优），选择 Argon2id，t=1 次迭代，p=4 个 lane，m=2^21（2 GiB RAM），128 位 salt，256 位 tag 大小。这是**首选推荐方案**。
2. **如果可用内存较少**，通用安全选项为 Argon2id，t=3 次迭代，p=4 个 lane，m=2^16（64 MiB RAM），128 位 salt，256 位 tag 大小。这是**次选推荐方案**。
3. 否则，首先选择类型 y。如果不了解各类型之间的区别，或认为侧信道攻击是可行的威胁，选择 Argon2id。
4. 选择 p=4 个 lane。
5. 确定每次调用可承受的最大内存量，并将其转换为参数 m。
6. 确定每次调用可承受的最大时间（秒）。
7. 选择 salt 长度。128 位对所有应用都足够，但在空间受限时可减少到 64 位。
8. 选择 tag 长度。128 位对大多数应用（包括密钥派生）足够。如需更长的密钥，选择更长的 tag。
9. 如果侧信道攻击是可行威胁或不确定，在库调用中启用内存擦除选项。
10. 使用类型 y、内存 m 和 p 个 lane，以不同的遍历次数 t 运行方案。找出使运行时间不超过可承受时间的最大 t。如果即使 t=1 也超过可承受时间，则相应减少 m。
11. 使用确定的 m、p 和 t 值运行 Argon2。

## 5. 测试向量

本节包含 Argon2 的测试向量。

### 5.1. Argon2d 测试向量

我们提供了包含完整输出（tag）的测试向量。为方便开发者，我们还提供了一些中间变量——具体为每次遍历的第一个和最后一个内存块。

```
=======================================
Argon2d version number 19
=======================================
Memory: 32 KiB
Passes: 3
Parallelism: 4 lanes
Tag length: 32 bytes
Password[32]: 01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
Salt[16]: 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02
Secret[8]: 03 03 03 03 03 03 03 03
Associated data[12]: 04 04 04 04 04 04 04 04 04 04 04 04
Pre-hashing digest: b8 81 97 91 a0 35 96 60
                    bb 77 09 c8 5f a4 8f 04
                    d5 d8 2c 05 c5 f2 15 cc
                    db 88 54 91 71 7c f7 57
                    08 2c 28 b9 51 be 38 14
                    10 b5 fc 2e b7 27 40 33
                    b9 fd c7 ae 67 2b ca ac
                    5d 17 90 97 a4 af 31 09

 After pass 0:
Block 0000 [  0]: db2fea6b2c6f5c8a
Block 0000 [  1]: 719413be00f82634
Block 0000 [  2]: a1e3f6dd42aa25cc
Block 0000 [  3]: 3ea8efd4d55ac0d1
...
Block 0031 [124]: 28d17914aea9734c
Block 0031 [125]: 6a4622176522e398
Block 0031 [126]: 951aa08aeecb2c05
Block 0031 [127]: 6a6c49d2cb75d5b6

 After pass 1:
Block 0000 [  0]: d3801200410f8c0d
Block 0000 [  1]: 0bf9e8a6e442ba6d
Block 0000 [  2]: e2ca92fe9c541fcc
Block 0000 [  3]: 6269fe6db177a388
...
Block 0031 [124]: 9eacfcfbdb3ce0fc
Block 0031 [125]: 07dedaeb0aee71ac
Block 0031 [126]: 074435fad91548f4
Block 0031 [127]: 2dbfff23f31b5883

 After pass 2:
Block 0000 [  0]: 5f047b575c5ff4d2
Block 0000 [  1]: f06985dbf11c91a8
Block 0000 [  2]: 89efb2759f9a8964
Block 0000 [  3]: 7486a73f62f9b142
...
Block 0031 [124]: 57cfb9d20479da49
Block 0031 [125]: 4099654bc6607f69
Block 0031 [126]: f142a1126075a5c8
Block 0031 [127]: c341b3ca45c10da5
Tag: 51 2b 39 1b 6f 11 62 97
     53 71 d3 09 19 73 42 94
     f8 68 e3 be 39 84 f3 c1
     a1 3a 4d b9 fa be 4a cb
```

### 5.2. Argon2i 测试向量

```
=======================================
Argon2i version number 19
=======================================
Memory: 32 KiB
Passes: 3
Parallelism: 4 lanes
Tag length: 32 bytes
Password[32]: 01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
              01 01 01 01 01 01 01 01
Salt[16]: 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02
Secret[8]: 03 03 03 03 03 03 03 03
Associated data[12]: 04 04 04 04 04 04 04 04 04 04 04 04
Pre-hashing digest: c4 60 65 81 52 76 a0 b3
                    e7 31 73 1c 90 2f 1f d8
                    0c f7 76 90 7f bb 7b 6a
                    5c a7 2e 7b 56 01 1f ee
                    ca 44 6c 86 dd 75 b9 46
                    9a 5e 68 79 de c4 b7 2d
                    08 63 fb 93 9b 98 2e 5f
                    39 7c c7 d1 64 fd da a9

 After pass 0:
Block 0000 [  0]: f8f9e84545db08f6
Block 0000 [  1]: 9b073a5c87aa2d97
Block 0000 [  2]: d1e868d75ca8d8e4
Block 0000 [  3]: 349634174e1aebcc
...
Block 0031 [124]: 975f596583745e30
Block 0031 [125]: e349bdd7edeb3092
Block 0031 [126]: b751a689b7a83659
Block 0031 [127]: c570f2ab2a86cf00

 After pass 1:
Block 0000 [  0]: b2e4ddfcf76dc85a
Block 0000 [  1]: 4ffd0626c89a2327
Block 0000 [  2]: 4af1440fff212980
Block 0000 [  3]: 1e77299c7408505b
...
Block 0031 [124]: e4274fd675d1e1d6
Block 0031 [125]: 903fffb7c4a14c98
Block 0031 [126]: 7e5db55def471966
Block 0031 [127]: 421b3c6e9555b79d

 After pass 2:
Block 0000 [  0]: af2a8bd8482c2f11
Block 0000 [  1]: 785442294fa55e6d
Block 0000 [  2]: 9256a768529a7f96
Block 0000 [  3]: 25a1c1f5bb953766
...
Block 0031 [124]: 68cf72fccc7112b9
Block 0031 [125]: 91e8c6f8bb0ad70d
Block 0031 [126]: 4f59c8bd65cbb765
Block 0031 [127]: 71e436f035f30ed0
Tag: c8 14 d9 d1 dc 7f 37 aa
     13 f0 d7 7f 24 94 bd a1
     c8 de 6b 01 6d d3 88 d2
     99 52 a4 c4 67 2b 6c e8
```

### 5.3. Argon2id 测试向量

```
=======================================
Argon2id version number 19
=======================================
Memory: 32 KiB, Passes: 3,
Parallelism: 4 lanes, Tag length: 32 bytes
Password[32]: 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01
01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01
Salt[16]: 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02 02
Secret[8]: 03 03 03 03 03 03 03 03
Associated data[12]: 04 04 04 04 04 04 04 04 04 04 04 04
Pre-hashing digest: 28 89 de 48 7e b4 2a e5 00 c0 00 7e d9 25 2f
 10 69 ea de c4 0d 57 65 b4 85 de 6d c2 43 7a 67 b8 54 6a 2f 0a
 cc 1a 08 82 db 8f cf 74 71 4b 47 2e 94 df 42 1a 5d a1 11 2f fa
 11 43 43 70 a1 e9 97

 After pass 0:
Block 0000 [  0]: 6b2e09f10671bd43
Block 0000 [  1]: f69f5c27918a21be
Block 0000 [  2]: dea7810ea41290e1
Block 0000 [  3]: 6787f7171870f893
...
Block 0031 [124]: 377fa81666dc7f2b
Block 0031 [125]: 50e586398a9c39c8
Block 0031 [126]: 6f732732a550924a
Block 0031 [127]: 81f88b28683ea8e5

 After pass 1:
Block 0000 [  0]: 3653ec9d01583df9
Block 0000 [  1]: 69ef53a72d1e1fd3
Block 0000 [  2]: 35635631744ab54f
Block 0000 [  3]: 599512e96a37ab6e
...
Block 0031 [124]: 4d4b435cea35caa6
Block 0031 [125]: c582210d99ad1359
Block 0031 [126]: d087971b36fd6d77
Block 0031 [127]: a55222a93754c692

 After pass 2:
Block 0000 [  0]: 942363968ce597a4
Block 0000 [  1]: a22448c0bdad5760
Block 0000 [  2]: a5f80662b6fa8748
Block 0000 [  3]: a0f9b9ce392f719f
...
Block 0031 [124]: d723359b485f509b
Block 0031 [125]: cb78824f42375111
Block 0031 [126]: 35bc8cc6e83b1875
Block 0031 [127]: 0b012846a40f346a
Tag: 0d 64 0d f5 8d 78 76 6c 08 c0 37 a3 4a 8b 53 c9 d0
 1e f0 45 2d 75 b6 5e b5 25 20 e9 6b 01 e6 59
```

## 6. IANA 考量

本文档没有 IANA 操作。

## 7. 安全考量

### 7.1. 密码学安全性

Argon2 的碰撞抗性和原像抗性水平与底层 BLAKE2b hash function 等价。产生碰撞需要 2^256 个输入。寻找原像需要尝试 2^512 个输入。

KDF 安全性由密钥长度和 hash function H' 内部状态的大小决定。要将带密钥的 Argon2 输出与随机值区分开，最少需要对 BLAKE2b 调用 2^128 或 2^length(K) 次。

### 7.2. 时空权衡攻击

时空权衡攻击（Time-space trade-off attack）允许以更多内部压缩函数调用为代价，存储更少的内存块来计算 memory-hard function。权衡攻击的优势通过 time-area product（时间-面积乘积）的降低因子来衡量，其中内存和额外的压缩函数核心贡献面积，时间则因需要重新计算缺失的块而增加。较高的降低因子可能加速原像搜索。

> [!note] 已知最佳攻击
> 对 1 次遍历和 2 次遍历的 Argon2i 的最佳攻击是 [AB16] 中描述的低存储攻击，它将 time-area product（使用峰值内存）降低了 5 倍。对 3 次及以上遍历的 Argon2i 的最佳攻击在 [BZ17] 中描述，降低因子是内存大小和遍历次数的函数（例如，对于 1 GiB 内存，3 次遍历降低 3 倍，4 次遍历降低 2.5 倍，6 次遍历降低 2 倍）。降低因子随内存大小每翻倍增加约 0.5。为完全防止 [CBS16] 中的时空权衡攻击，遍历次数必须超过内存的二进制对数减 26。渐近地，对 1 次遍历 Argon2i 的最佳攻击在 [AB16] 中给出，攻击者最大优势的上界为 O(m^0.233)，其中 m 是块数。此攻击也是渐近最优的，因为 [HARD] 也证明了任何攻击的上界为 O(m^0.25)。

对 t 次遍历 Argon2d 的最佳权衡攻击是 ranking trade-off attack（排序权衡攻击），将 time-area product 降低了 1.33 倍。

对 Argon2id 的最佳攻击可以通过将对 1 次遍历 Argon2i 的最佳攻击与对多次遍历 Argon2d 的最佳攻击组合来获得。因此，对 1 次遍历 Argon2id 的最佳权衡攻击是组合的低存储攻击（针对前半内存）和 ranking 攻击（针对后半内存），产生的因子约为 2.1。对 t 次遍历 Argon2id 的最佳权衡攻击是 ranking trade-off attack，将 time-area product 降低了 1.33 倍。

### 7.3. 推荐参数

在使用密码哈希函数的系统中，瓶颈通常是函数延迟而非内存成本。理性的防御者会在自己的机器上以固定计算时间最大化攻击者（拥有 hash、salt 和计时信息列表）的暴力破解成本。[ARGON2ESP] 中的攻击成本估计表明：对于 Argon2i，3 次遍历对大多数合理的内存大小几乎是最佳的；对于 Argon2d 和 Argon2id，1 次遍历在恒定防御者时间下最大化攻击成本。

## 8. 参考文献

### 8.1. 规范性引用

[BLAKE2]
: Saarinen, M-J., Ed. and J-P. Aumasson, "The BLAKE2 Cryptographic Hash and Message Authentication Code (MAC)", RFC 7693, DOI 10.17487/RFC7693, November 2015, <[https://www.rfc-editor.org/info/rfc7693](https://www.rfc-editor.org/info/rfc7693)>.

[RFC2119]
: Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, <[https://www.rfc-editor.org/info/rfc2119](https://www.rfc-editor.org/info/rfc2119)>.

[RFC8174]
: Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, <[https://www.rfc-editor.org/info/rfc8174](https://www.rfc-editor.org/info/rfc8174)>.

### 8.2. 资料性引用

[AB15]
: Biryukov, A. and D. Khovratovich, "Tradeoff Cryptanalysis of Memory-Hard Functions", ASIACRYPT 2015, DOI 10.1007/978-3-662-48800-3_26, December 2015, <[https://eprint.iacr.org/2015/227.pdf](https://eprint.iacr.org/2015/227.pdf)>.

[AB16]
: Alwen, J. and J. Blocki, "Efficiently Computing Data-Independent Memory-Hard Functions", CRYPTO 2016, DOI 10.1007/978-3-662-53008-5_9, March 2016, <[https://eprint.iacr.org/2016/115.pdf](https://eprint.iacr.org/2016/115.pdf)>.

[ARGON2]
: Biryukov, A., Dinu, D., and D. Khovratovich, "Argon2: the memory-hard function for password hashing and other applications", March 2017, <[https://www.cryptolux.org/images/0/0d/Argon2.pdf](https://www.cryptolux.org/images/0/0d/Argon2.pdf)>.

[ARGON2ESP]
: Biryukov, A., Dinu, D., and D. Khovratovich, "Argon2: New Generation of Memory-Hard Functions for Password Hashing and Other Applications", Euro SnP 2016, DOI 10.1109/EuroSP.2016.31, March 2016, <[https://www.cryptolux.org/images/d/d0/Argon2ESP.pdf](https://www.cryptolux.org/images/d/d0/Argon2ESP.pdf)>.

[BZ17]
: Blocki, J. and S. Zhou, "On the Depth-Robustness and Cumulative Pebbling Cost of Argon2i", TCC 2017, DOI 10.1007/978-3-319-70500-2_15, May 2017, <[https://eprint.iacr.org/2017/442.pdf](https://eprint.iacr.org/2017/442.pdf)>.

[CBS16]
: Boneh, D., Corrigan-Gibbs, H., and S. Schechter, "Balloon Hashing: A Memory-Hard Function Providing Provable Protection Against Sequential Attacks", ASIACRYPT 2016, DOI 10.1007/978-3-662-53887-6_8, May 2017, <[https://eprint.iacr.org/2016/027.pdf](https://eprint.iacr.org/2016/027.pdf)>.

[HARD]
: Alwen, J. and V. Serbinenko, "High Parallel Complexity Graphs and Memory-Hard Functions", STOC '15, DOI 10.1145/2746539.2746622, June 2015, <[https://eprint.iacr.org/2014/238.pdf](https://eprint.iacr.org/2014/238.pdf)>.

## 致谢

我们衷心感谢以下在准备和审阅本文档过程中提供帮助的人士：Jean-Philippe Aumasson、Samuel Neves、Joel Alwen、Jeremiah Blocki、Bill Cox、Bjrn Jacke、Tanja Lange、Thomas Pornin、Tim Taubert 和 Mathy Vanhoef。

本文档中描述的工作是在 Daniel Dinu 加入 Intel 之前完成的，当时他在卢森堡大学工作。

## 作者地址

**Alex Biryukov**
University of Luxembourg
Email: [alex.biryukov@uni.lu](mailto:alex.biryukov@uni.lu)

**Daniel Dinu**
University of Luxembourg
Email: [daniel.dinu@intel.com](mailto:daniel.dinu@intel.com)

**Dmitry Khovratovich**
ABDK Consulting
Email: [khovratovich@gmail.com](mailto:khovratovich@gmail.com)

**Simon Josefsson**
SJD AB
Email: [simon@josefsson.org](mailto:simon@josefsson.org)
URI: [http://josefsson.org/](http://josefsson.org/)
