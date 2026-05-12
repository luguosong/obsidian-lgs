---
title: HOTP 基于 HMAC 的一次性密码
description: RFC 4226 定义的基于 HMAC-SHA-1 的事件驱动型一次性密码（HOTP）算法，用于双因素认证。
tags:
  - 密码学
  - HOTP
  - 一次性密码
  - RFC
---

> [!info] RFC 信息
> **RFC 编号**：4226
> **标题**：HOTP: An HMAC-Based One-Time Password Algorithm
> **类别**：Informational
> **日期**：2005 年 12 月
> **作者**：D. M'Raihi (VeriSign), M. Bellare (UCSD), F. Hoornaert (Vasco), D. Naccache (Gemplus), O. Ranen (Aladdin)

## 备忘录状态

本备忘录为 Internet 社区提供信息，不指定任何形式的 Internet 标准。本备忘录的分发不受限制。

## 版权声明

Copyright (C) The Internet Society (2005).

## 摘要

本文档描述了一种基于 HMAC（Hashed Message Authentication Code，哈希消息认证码）生成一次性密码值的算法，并给出了该算法的安全性分析，以及与该算法安全部署相关的重要参数。所提出的算法可广泛应用于各种网络应用，包括远程 VPN（Virtual Private Network，虚拟专用网络）接入、Wi-Fi 网络登录以及面向事务的 Web 应用。

这项工作是 OATH（Open AuTHentication，开放认证）成员的联合成果，旨在指定一种可自由分发给技术社区的算法。作者认为，一个通用的、共享的算法将通过实现商业和开源实现之间的互操作性，促进双因素认证在 Internet 上的采用。

## 目录

1. 概述
2. 引言
3. 需求术语
4. 算法需求
5. HOTP 算法
   - 5.1 符号与记法
   - 5.2 描述
   - 5.3 生成 HOTP 值
   - 5.4 Digit = 6 的 HOTP 计算示例
6. 安全性考虑
7. 安全需求
   - 7.1 认证协议需求
   - 7.2 HOTP 值的验证
   - 7.3 服务器端节流
   - 7.4 计数器重同步
   - 7.5 共享密钥的管理
8. 复合共享密钥
9. 双向认证
10. 结论
11. 致谢
12. 贡献者
13. 参考文献
   - 13.1 规范性引用
   - 13.2 资料性引用
附录 A - HOTP 算法安全性：详细分析
附录 B - SHA-1 攻击
附录 C - HOTP 算法：参考实现
附录 D - HOTP 算法：测试值
附录 E - 扩展

## 1. 概述

本文档首先介绍了基于 HMAC [BCK1] 生成一次性密码值的算法的背景，因此该算法被命名为 HOTP（HMAC-Based One-Time Password，基于 HMAC 的一次性密码）算法。第 4 节列出了算法需求，第 5 节描述了 HOTP 算法。第 6 节和第 7 节重点关注算法安全性。第 8 节提出了一些扩展和改进，第 10 节总结本文档。在附录 A 中，感兴趣的读者可以找到算法安全性的详细完整分析：首先评估了算法的理想化版本，然后分析了 HOTP 算法的安全性。

## 2. 引言

如今，双因素认证的部署在范围和规模上仍然极其有限。尽管威胁和攻击水平不断升高，大多数 Internet 应用仍然依赖弱认证方案来控制用户访问。硬件和软件技术供应商之间缺乏互操作性一直是采用双因素认证技术的限制因素。特别是，缺乏开放规范导致了硬件和软件组件通过专有技术紧密耦合的解决方案，造成高成本、低采用率和有限的创新。

在过去两年中，网络威胁的快速增加暴露了静态密码作为 Internet 上主要认证手段的不足。同时，要求终端用户携带仅用于网络认证的昂贵单功能设备的做法显然不是正确答案。要使双因素认证在 Internet 上普及，它必须被嵌入到更灵活的设备中，以适应各种应用。

嵌入这项基础技术并确保广泛互操作性的能力，要求该技术对广大的硬件和软件开发者技术社区免费提供。只有开放式系统方法才能确保基本的双因素认证原语能够被构建到下一代消费设备中，如 USB 大容量存储设备、IP 电话和个人数字助理。

一次性密码（One-Time Password）无疑是保护网络访问安全的最简单、最流行的双因素认证形式之一。例如，在大型企业中，VPN 接入通常需要使用一次性密码令牌进行远程[[用户认证]]。一次性密码通常比更强的认证形式（如 PKI（Public-Key Infrastructure，公钥基础设施）或生物识别）更受青睐，因为气隙设备（air-gap device）不需要在用户机器上安装任何客户端桌面软件，因此允许用户在多台机器上漫游，包括家用电脑、自助终端和个人数字助理。

本文档提出了一种简单的一次性密码算法，任何硬件制造商或软件开发者都可以实现该算法来创建可互操作的认证设备和软件代理。该算法基于事件（event-based），因此可以嵌入到大批量设备中，如 Java 智能卡、USB 加密狗和 GSM SIM 卡。所提出的算法根据 IETF 知识产权 [RFC3979] 的条款和条件向开发者社区免费提供。

本文档的作者是 OATH（Open AuTHentication）倡议 [OATH] 的成员。该倡议于 2004 年创建，旨在促进强认证技术提供商之间的协作。

## 3. 需求术语

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按照 [RFC2119] 中的描述进行解释。

## 4. 算法需求

本节列出了驱动本算法设计的主要需求。设计中对终端消费者可用性以及算法在低成本硬件（可能仅提供最少的用户界面功能）上的实现能力给予了大量关注。特别是，将算法嵌入大批量 SIM 卡和 Java 卡的能力是一个基本前提。

**R1** - 算法必须是序列型或计数器型的：目标之一是让 HOTP 算法能嵌入大批量设备，如 Java 智能卡、USB 加密狗和 GSM SIM 卡。

**R2** - 算法在硬件实现时应经济高效，尽量减少对电池、按钮数量、计算能力和 LCD 显示屏尺寸的要求。

**R3** - 算法必须能用于不支持任何数字输入的令牌，但也可以用于更复杂的设备，如安全 PIN 键盘。

**R4** - 令牌上显示的值必须易于用户阅读和输入：这要求 HOTP 值具有合理的长度。HOTP 值必须至少为 6 位数字。同时，HOTP 值最好是"纯数字"，以便在手机等受限设备上轻松输入。

**R5** - 必须有用户友好的机制来重新同步计数器。第 7.4 节和附录 E.4 详细说明了本文档提出的重同步机制。

**R6** - 算法必须使用强共享密钥。共享密钥的长度必须至少为 128 位。本文档推荐共享密钥长度为 160 位。

## 5. HOTP 算法

本节介绍符号记法，并描述 HOTP 算法的基本构建块——计算 HMAC-SHA-1 值的基础函数和提取 HOTP 值的截断方法。

### 5.1 符号与记法

字符串始终指二进制字符串，即由 0 和 1 组成的序列。

如果 s 是字符串，则 |s| 表示其长度。

如果 n 是数字，则 |n| 表示其绝对值。

如果 s 是字符串，则 s[i] 表示其第 i 位。位的编号从 0 开始，因此 s = s[0]s[1]...s[n-1]，其中 n = |s| 是 s 的长度。

StToNum（String to Number，字符串转数字）函数：以字符串 s 为输入，返回其二进制表示所对应的数字。（例如，StToNum(110) = 6。）

以下是本文档中使用的符号列表：

| 符号 | 含义 |
|------|------|
| **C** | 8 字节计数器值，即移动因子。此计数器必须在 HOTP 生成器（客户端）和 HOTP 验证器（服务器）之间保持同步。 |
| **K** | 客户端和服务器之间的共享密钥；每个 HOTP 生成器都有不同的唯一密钥 K。 |
| **T** | 节流参数：在 T 次不成功的认证尝试后，服务器将拒绝来自该用户的连接。 |
| **s** | 重同步参数：服务器将尝试在 s 个连续计数器值上验证接收到的认证码。 |
| **Digit** | HOTP 值的数字位数；系统参数。 |

### 5.2 描述

HOTP 算法基于一个递增的计数器值和一个仅令牌和验证服务知道的静态对称密钥。为了创建 HOTP 值，我们使用 RFC 2104 [BCK2] 中定义的 HMAC-SHA-1 算法。

由于 HMAC-SHA-1 计算的输出为 160 位，我们必须将其截断为用户可以轻松输入的值。

$$\text{HOTP}(K,C) = \text{Truncate}(\text{HMAC-SHA-1}(K,C))$$

其中：

- Truncate 表示将 HMAC-SHA-1 值转换为 HOTP 值的函数，定义见第 5.3 节。

密钥 (K)、计数器 (C) 和数据值按高字节优先（high-order byte first）进行哈希计算。

HOTP 生成器生成的 HOTP 值按大端序（big endian）处理。

### 5.3 生成 HOTP 值

我们可以将操作分为 3 个不同的步骤：

> [!note] 步骤 1：生成 HMAC-SHA-1 值
> 令 HS = HMAC-SHA-1(K, C) // HS 是一个 20 字节的字符串

> [!note] 步骤 2：生成 4 字节字符串（动态截断）
> 令 Sbits = DT(HS) // DT（定义如下）返回一个 31 位字符串

> [!note] 步骤 3：计算 HOTP 值
> 令 Snum = StToNum(Sbits) // 将 S 转换为 0...2^{31}-1 范围内的数字
> 返回 D = Snum mod 10^Digit // D 是 0...10^{Digit}-1 范围内的数字

Truncate 函数执行步骤 2 和步骤 3，即动态截断，然后取模 10^Digit。动态偏移截断技术的目的是从 160 位（20 字节）的 HMAC-SHA-1 结果中提取 4 字节的动态二进制码。

```
DT(String) // String = String[0]...String[19]
  令 OffsetBits 为 String[19] 的低 4 位
  Offset = StToNum(OffsetBits) // 0 <= Offset <= 15
  令 P = String[Offset]...String[Offset+3]
  返回 P 的最后 31 位
```

> [!tip] 关于屏蔽最高有效位
> 屏蔽 P 的最高有效位的原因是避免有符号和无符号取模运算之间的混淆。不同的处理器执行这些运算的方式不同，屏蔽掉符号位可以消除所有歧义。

实现必须至少提取 6 位数字码，也可以提取 7 位和 8 位数字码。根据安全需求，应考虑使用 Digit = 7 或更多位数以提取更长的 HOTP 值。

下面的段落是使用此技术计算 Digit = 6 的示例，即从 HMAC 值计算 6 位 HOTP 值。

### 5.4 Digit = 6 的 HOTP 计算示例

以下代码示例描述了从 HMAC-SHA-1 结果（hmac_result 字节数组）中提取动态二进制码的过程：

```java
int offset   =  hmac_result[19] & 0xf ;
int bin_code = (hmac_result[offset]  & 0x7f) << 24
   | (hmac_result[offset+1] & 0xff) << 16
   | (hmac_result[offset+2] & 0xff) <<  8
   | (hmac_result[offset+3] & 0xff) ;
```

**SHA-1 HMAC 字节示例**

```
-------------------------------------------------------------
| 字节编号                                                   |
-------------------------------------------------------------
|00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|
-------------------------------------------------------------
| 字节值                                                     |
-------------------------------------------------------------
|1f|86|98|69|0e|02|ca|16|61|85|50|ef|7f|19|da|8e|94|5b|55|5a|
-------------------------------***********----------------++|
```

- 最后一个字节（字节 19）的十六进制值为 0x5a。
- 低 4 位的值为 0xa（偏移值）。
- 偏移值为字节 10（0xa）。
- 从字节 10 开始的 4 个字节的值为 0x50ef7f19，即动态二进制码 DBC1。
- DBC1 的最高有效字节（MSB）为 0x50，因此 DBC2 = DBC1 = 0x50ef7f19。
- HOTP = DBC2 mod 10^6 = 872921。

我们将动态二进制码视为一个 31 位无符号大端整数；第一个字节用 0x7f 屏蔽。

然后我们取该数字对 1,000,000（10^6）取模，生成 6 位 HOTP 值 **872921**（十进制）。

## 6. 安全性考虑

附录中详细的安全性分析的结论是，对于所有实际目的，动态截断（DT）在不同计数器输入上的输出是均匀且独立分布的 31 位字符串。

安全性分析随后详细说明了从字符串到整数的转换以及最终取模 10^Digit（其中 Digit 是 HOTP 值的数字位数）的影响。

分析表明，这些最终步骤引入的偏差可以忽略不计，不会影响 HOTP 算法的安全性，因为对 HOTP 函数的最佳可能攻击是暴力破解攻击。

假设攻击者能够观察大量协议交换并收集成功认证值的序列。该攻击者试图构建函数 F 来基于观察结果生成 HOTP 值，但与随机猜测相比不会有显著优势。

逻辑结论很简单，最佳策略将再次是执行暴力破解攻击，以枚举和尝试所有可能的值。

考虑到本文档附录中的安全性分析，在不失一般性的情况下，我们可以用以下公式紧密近似 HOTP 算法的安全性：

$$Sec = \frac{sv}{10^{Digit}}$$

其中：
- **Sec** 是攻击者的成功概率；
- **s** 是前瞻同步窗口大小；
- **v** 是验证尝试次数；
- **Digit** 是 HOTP 值的数字位数。

显然，我们可以调整 s、T（限制攻击者尝试次数的节流参数）和 Digit 的值，直到达到一定的安全水平，同时保持系统的可用性。

## 7. 安全需求

任何一次性密码算法的安全性仅取决于实现它的应用程序和认证协议。因此，本节讨论算法选择对认证协议和验证软件施加的关键安全需求。

本节讨论的参数 T 和 s 对安全性有显著影响——第 6 节进一步详述了这些参数之间的关系及其对系统安全性的影响。

还需要注意的是，HOTP 算法不能替代加密，也不提供数据传输的隐私保护。应使用其他机制来对抗旨在破坏交易机密性和隐私的攻击。

### 7.1 认证协议需求

本节介绍使用 HOTP 作为证明者（prover）和验证者（verifier）之间认证方法的协议 P 的一些需求。

**RP1** - P 必须支持双因素认证，即通信和验证"你知道什么"（密码，如 Password、Passphrase、PIN 码等）和"你有什么"（令牌）。密钥码仅用户知道，通常与一次性密码值一起输入用于认证目的（双因素认证）。

**RP2** - P 不应易受暴力破解攻击。这意味着建议在验证服务器端实施节流/锁定方案。

**RP3** - P 应在安全通道上实现，以保护用户隐私并防止重放攻击。

### 7.2 HOTP 值的验证

HOTP 客户端（硬件或软件令牌）递增其计数器，然后计算下一个 HOTP 值。如果认证服务器接收到的值与客户端计算的值匹配，则 HOTP 值验证通过。在这种情况下，服务器将计数器值加一。

如果服务器接收到的值与客户端计算的值不匹配，服务器启动重同步协议（前瞻窗口），然后才请求再次认证。

如果重同步失败，服务器要求再次执行协议的认证过程，直到达到授权的最大尝试次数。

如果达到授权的最大尝试次数，服务器应锁定账户并启动通知用户的程序。

### 7.3 服务器端节流

将 HMAC-SHA-1 值截断为较短的值使暴力破解攻击成为可能。因此，认证服务器需要检测并阻止暴力破解攻击。

我们建议设置节流参数 T，该参数定义了一次性密码验证的最大可能尝试次数。验证服务器为每个 HOTP 设备管理单独的计数器，以记录任何失败的尝试。我们建议 T 不要设置得太大，特别是如果服务器上使用的重同步方法是基于窗口的，且窗口大小较大。T 应设置得尽可能低，同时确保可用性不受显著影响。

另一种选择是实施延迟方案以避免暴力破解攻击。每次失败尝试 A 后，认证服务器将等待增加的 T*A 秒数，例如，假设 T = 5，则在 1 次尝试后，服务器等待 5 秒，在第二次失败尝试时，它等待 5*2 = 10 秒，依此类推。

延迟或锁定方案必须跨登录会话实施，以防止基于多个并行猜测技术的攻击。

### 7.4 计数器重同步

虽然服务器的计数器值仅在成功进行 HOTP 认证后才递增，但令牌上的计数器在用户每次请求新的 HOTP 时递增。因此，服务器和令牌上的计数器值可能会失去同步。

我们建议在服务器上设置前瞻参数 s，定义前瞻窗口的大小。简而言之，服务器可以重新计算接下来的 s 个 HOTP 服务器值，并将其与接收到的客户端 HOTP 值进行核对。

在这种情况下，计数器的同步只需服务器计算接下来的 HOTP 值并确定是否存在匹配。可选地，系统可以要求用户发送一系列（例如 2 个、3 个）HOTP 值用于重同步目的，因为伪造连续 HOTP 值序列比猜测单个 HOTP 值更困难。

参数 s 设置的上限确保服务器不会无限期地检查 HOTP 值（防止拒绝服务攻击），同时也限制了攻击者尝试制造 HOTP 值的可能解空间。s 应设置得尽可能低，同时确保可用性不受影响。

### 7.5 共享密钥的管理

处理用于生成和验证 OTP 值的共享密钥的操作必须安全执行，以减轻敏感信息泄露的风险。本节描述了不同的操作模式和根据数据安全最新技术水平执行这些操作的技术。

我们可以考虑在验证系统中生成和（安全地）存储共享密钥的两种不同途径：

- **确定性生成**：密钥在供应和验证阶段都从主种子派生，并在需要时即时生成。
- **随机生成**：密钥在供应阶段随机生成，必须立即存储并在其生命周期内保持安全。

#### 确定性生成

一种可能的策略是从主密钥派生共享密钥。主密钥仅存储在服务器上。必须使用防篡改设备来存储主密钥，并从主密钥和一些公共信息派生共享密钥。主要好处是避免在任何时候暴露共享密钥，同时避免对存储的特殊要求，因为共享密钥可以在需要时按需生成。

我们区分两种不同的情况：

- 使用单个主密钥 MK 来派生共享密钥；每个 HOTP 设备有不同的密钥，K_i = SHA-1(MK, i)，其中 i 代表唯一标识 HOTP 设备的一条公共信息，如序列号、令牌 ID 等。显然，这是在应用或服务上下文中的——不同的应用或服务提供商将有不同的密钥和设置。
- 使用多个主密钥 MK_i，每个 HOTP 设备存储一组不同的派生密钥，{K_i,j = SHA-1(MK_i, j)}，其中 j 代表标识设备的公共信息。其想法是在验证服务器的硬件安全模块（HSM，Hardware Security Module）中仅存储活动的主密钥，并使用秘密共享方法（如 [Shamir]）将其他密钥保存在安全的地方。在这种情况下，如果主密钥 MK_i 被泄露，则可以切换到另一个密钥而无需更换所有设备。

> [!warning] 确定性生成的风险
> 确定性情况的缺点是主密钥的泄露显然会使攻击者能够基于正确的公共信息重建任何共享密钥。需要撤销所有密钥，或者在有多个主密钥的情况下切换到新的密钥集。

另一方面，用于存储主密钥和生成共享密钥的设备必须是防篡改的。此外，HSM 不会暴露在验证系统的安全边界之外，因此降低了泄露风险。

#### 随机生成

共享密钥随机生成。我们建议遵循 [RFC4086] 中的建议，选择良好且安全的随机源来生成这些密钥。（真正的）随机生成器需要自然发生的随机性来源。实际上，生成共享密钥有两条可能的途径：

- **硬件生成器**：利用物理现象中出现的随机性。一个良好的实现可以基于振荡器，并以使主动攻击更难执行的方式构建。
- **软件生成器**：设计一个好的软件随机生成器并非易事。一个简单但高效的实现应基于各种源，并对采样序列应用 SHA-1 等单向函数。

我们建议选择经过验证的产品（无论是硬件还是软件生成器）来计算共享密钥。

我们还建议安全地存储共享密钥，更具体地说，在存储时使用防篡改硬件加密对共享密钥进行加密，并仅在需要时暴露：例如，共享密钥在需要验证 HOTP 值时解密，并立即重新加密以限制在 RAM 中的暴露时间。存储共享密钥的数据存储必须位于安全区域，以尽可能避免对验证系统和密钥数据库的直接攻击。

特别是，对共享密钥的访问应仅限于验证系统所需的程序和进程。我们不在此详细阐述不同的安全机制，但显然，保护共享密钥至关重要。

## 8. 复合共享密钥

在共享密钥 K 中包含额外的认证因子可能是可取的。这些额外因子可以由令牌知道但不容易被他人获取的任何数据组成。此类数据的示例包括：

- 在令牌上通过用户输入获取的 PIN 或密码
- 电话号码
- 令牌上可通过编程获取的任何唯一标识符

在这种场景中，复合共享密钥 K 在供应过程中由随机种子值与一个或多个额外认证因子组合构建。服务器可以按需构建或存储复合密钥——无论选择哪种实现方式，令牌仅存储种子值。当令牌执行 HOTP 计算时，它从种子值和本地派生或输入的其他认证因子值计算 K。

使用复合共享密钥可以通过在令牌上包含额外认证因子来增强基于 HOTP 的认证系统。只要令牌是可信设备，这种方法还有一个额外的好处：不需要将认证因子（如用户输入的 PIN）暴露给其他设备。

## 9. 双向认证

有趣的是，HOTP 客户端也可用于认证验证服务器，声称它是一个知道共享密钥的真实实体。

由于 HOTP 客户端和服务器是同步的并且共享相同的密钥（或重新计算它的方法），可以实现一个简单的 3 步协议：

1. 终端用户输入 TokenID 和第一个 OTP 值 OTP1；
2. 服务器检查 OTP1，如果正确，返回 OTP2；
3. 终端用户使用其 HOTP 设备检查 OTP2，如果正确，使用该网站。

> [!note] 安全通道要求
> 如前所述，所有 OTP 通信必须通过安全通道进行，例如 SSL/TLS、IPsec 连接。

## 10. 结论

本文档描述了 HOTP，一种基于 HMAC 的一次性密码算法。它还推荐了部署该算法的首选实现和相关操作模式。

本文档还展示了安全性要素，并论证了 HOTP 算法是实用且健全的，最佳可能攻击是暴力破解攻击，可以通过在验证服务器中仔细实施对策来防止。

最后，提出了若干增强方案，以便在特定应用需要时提高安全性。

## 11. 致谢

作者感谢 Siddharth Bajaj、Alex Deacon、Loren Hart 和 Nico Popp 在本文档构思和编写过程中提供的帮助。

## 12. 贡献者

本文档的作者想强调三位对本文档做出关键贡献的人员：

- Laszlo Elteto，SafeNet, Inc. 系统架构师
- Ernesto Frutos，Authenex, Inc. 工程总监
- Fred McClain，Boojum Mobile, Inc. 创始人兼 CTO

没有他们的建议和宝贵意见，本文档将不会是现在的样子。

## 13. 参考文献

### 13.1 规范性引用

- [BCK1] M. Bellare, R. Canetti and H. Krawczyk, "Keyed Hash Functions and Message Authentication", Proceedings of Crypto'96, LNCS Vol. 1109, pp. 1-15.
- [BCK2] Krawczyk, H., Bellare, M., and R. Canetti, "HMAC: Keyed-Hashing for Message Authentication", RFC 2104, February 1997.
- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC3979] Bradner, S., "Intellectual Property Rights in IETF Technology", BCP 79, RFC 3979, March 2005.
- [RFC4086] Eastlake, D., 3rd, Schiller, J., and S. Crocker, "Randomness Requirements for Security", BCP 106, RFC 4086, June 2005.

### 13.2 资料性引用

- [OATH] Initiative for Open AuTHentication http://www.openauthentication.org
- [PrOo] B. Preneel and P. van Oorschot, "MD-x MAC and building fast MACs from hash functions", Advances in Cryptology CRYPTO '95, Lecture Notes in Computer Science Vol. 963, D. Coppersmith ed., Springer-Verlag, 1995.
- [Crack] Crack in SHA-1 code 'stuns' security gurus http://www.eetimes.com/showArticle.jhtml?articleID=60402150
- [Sha1] Bruce Schneier. SHA-1 broken. February 15, 2005. http://www.schneier.com/blog/archives/2005/02/sha1_broken.html
- [Res] Researchers: Digital encryption standard flawed http://news.com.com/Researchers+Digital+encryption+standard+flawed/2100-1002-5579881.html?part=dht&tag=ntop&tag=nl.e703
- [Shamir] How to Share a Secret, by Adi Shamir. In Communications of the ACM, Vol. 22, No. 11, pp. 612-613, November, 1979.

---

## 附录 A - HOTP 算法安全性：详细分析

本节总结了 HOTP 算法的安全性分析。我们首先详述最佳攻击策略，然后阐述各种假设下的安全性以及截断的影响，并对数字位数提出建议。

我们重点关注 Digit = 6 的情况，即生成 6 位数字值的 HOTP 函数，这是本文档推荐的最低要求。

### A.1 定义与记法

我们用 {0,1}^l 表示所有长度为 l 的字符串集合。

令 Z_{n} = {0,.., n - 1}。

IntDiv(a,b) 表示整数除法算法，接受整数 a、b（其中 a >= b >= 1）作为输入，返回整数 (q,r)——即 a 除以 b 的商和余数。（因此 a = bq + r，0 <= r < b。）

令 H: {0,1}^k x {0,1}^c --> {0,1}^n 为基础函数，接受 k 位密钥 K 和 c 位计数器 C，返回 n 位输出 H(K,C)。（在 HOTP 的情况下，H 是 HMAC-SHA-1；我们使用这个形式化定义来推广我们的安全性证明。）

### A.2 理想化算法：HOTP-IDEAL

我们现在定义 HOTP 算法的一个理想化对应物。在这个算法中，H 的角色由构成密钥的随机函数扮演。

更准确地说，令 Maps(c,n) 表示从 {0,1}^c 映射到 {0,1}^n 的所有函数的集合。理想化算法的密钥空间为 Maps(c,n)，因此该算法的"密钥"是一个从 {0,1}^c 到 {0,1}^n 的函数 h。我们想象这个密钥（函数）是随机抽取的。实现这个理想化算法是不可行的，因为密钥（从 {0,1}^c 到 {0,1}^n 的函数）太大以至于无法存储。那为什么要考虑它？

我们的安全性分析将表明，只要 H 满足某个广为接受的假设，实际算法和理想化算法的安全性在所有实际目的上都是相同的。因此，我们真正面临的任务是评估理想化算法的安全性。

在分析理想化算法时，我们专注于评估算法本身设计的质量，独立于 HMAC-SHA-1。这实际上是关键问题。

### A.3 安全模型

该模型展示了所考虑的威胁或攻击类型，并能够评估 HOTP 和 HOTP-IDEAL 的安全性。我们用 ALG 表示 HOTP 或 HOTP-IDEAL，用于本次安全性分析。

我们考虑的场景是用户和服务器共享 ALG 的密钥 K。双方维护一个计数器 C，初始为零，用户通过向服务器发送 ALG(K,C) 来认证自己。如果该值正确，服务器接受。

为了防止用户计数器的意外递增，服务器在接收到值 z 时，只要 z 等于 ALG(K,i)（其中 i 在范围 C,...,C + s - 1 内），就接受，其中 s 是重同步参数，C 是服务器计数器。如果以某个 i 值接受，则将其计数器递增到 i+1。如果不接受，则不改变计数器值。

我们指定的模型捕获了攻击者可以做什么以及需要实现什么才能"获胜"。首先，假设攻击者能够窃听，即看到用户传输的认证码。其次，如果攻击者能让服务器接受一个相对于用户从未传输过认证码的计数器值的认证码，则攻击者获胜。

形式化的攻击者（我们用 B 表示）一开始就知道正在使用哪个算法 ALG，知道系统设计，知道所有系统参数。唯一不预先给定的是用户和服务器之间共享的密钥 K。

模型给予 B 对事件调度的完全控制。它可以访问代表用户的认证码预言机（oracle）。通过调用此预言机，攻击者可以要求[[用户认证]]自己并获得认证码作为回报。它可以随时随意调用此预言机，使用积累的认证码来可能"学习"如何自己制作认证码。在任何时候，它也可以调用验证预言机，向其提供自己选择的候选认证码。如果服务器接受此认证码，则攻击者获胜。

考虑以下涉及攻击者 B 试图攻破认证算法 ALG: K x {0,1}^c --> R 的安全性的博弈：

**初始化** - 从 K 中随机选择密钥 K，计数器 C 初始化为 0，布尔值 win 设为 false。

**博弈执行** - 攻击者 B 获得以下两个预言机：

```
Oracle AuthO()
--------------
   A = ALG(K,C)
   C = C + 1
   返回 O 给 B

Oracle VerO(A)
--------------
   i = C
   While (i <= C + s - 1 and Win == FALSE) do
      If A == ALG(K,i) then Win = TRUE; C = i + 1
      Else i = i + 1
   返回 Win 给 B
```

AuthO() 是认证码预言机，VerO(A) 是验证预言机。

执行时，B 随意查询两个预言机。令 Adv(B) 为上述博弈中 win 被设为 true 的概率。这是攻击者成功冒充用户的概率。

我们的目标是评估这个值作为 B 的验证查询数 v、认证码预言机查询数 a 和 B 的运行时间 t 的函数可以有多大。这将告诉我们如何设置节流参数，以有效限制 v 的上界。

### A.4 理想认证算法的安全性

本节总结了 HOTP-IDEAL 的安全性分析，首先讨论取模 10^Digit 转换的影响，然后重点关注不同可能的攻击。

#### A.4.1 从位到数字

随机 n 位字符串的动态偏移截断产生随机 31 位字符串。当它取模 m = 10^Digit 时（如 HOTP 中所做），分布会发生什么变化？

以下引理估计了这种情况下的输出偏差。

**引理 1**

令 N >= m >= 1 为整数，令 (q,r) = IntDiv(N,m)。对于 Z_{m} 中的 z：

$$P_{N,m}(z) = Pr[x \bmod m = z : x \text{ 随机选自 } Z_{N}]$$

则对于 Z_{m} 中的任意 z：

$$P_{N,m}(z) = \begin{cases} (q + 1) / N & \text{如果 } 0 \le z < r \\ q / N & \text{如果 } r \le z < m \end{cases}$$

**引理 1 的证明**

令随机变量 X 在 Z_{N} 上均匀分布。则：

$$P_{N,m}(z) = Pr[X \bmod m = z]$$

$$= Pr[X < mq] \cdot Pr[X \bmod m = z | X < mq] + Pr[mq \le X < N] \cdot Pr[X \bmod m = z | mq \le X < N]$$

$$= \frac{mq}{N} \cdot \frac{1}{m} + \begin{cases} \frac{N - mq}{N} \cdot \frac{1}{N - mq} & \text{如果 } 0 \le z < N - mq \\ 0 & \text{如果 } N - mq \le z \le m \end{cases}$$

$$= \frac{q}{N} + \begin{cases} \frac{r}{N} \cdot \frac{1}{r} & \text{如果 } 0 \le z < N - mq \\ 0 & \text{如果 } r \le z \le m \end{cases}$$

化简即得所证等式。

令 N = 2^31，d = 6，m = 10^d。如果 x 从 Z_{N} 中随机选择（即随机 31 位字符串），则通过取 x mod m 将其缩减为 6 位数字并不会产生随机 6 位数字。

相反，x mod m 的分布如下表所示：

| 值 | 每个值作为输出的概率 |
|------|------|
| 0, 1, ..., 483647 | 2148/2^31，约等于 1.00024045/10^6 |
| 483648, ..., 999999 | 2147/2^31，约等于 0.99977478/10^6 |

如果 X 在 Z_{2^31} 上均匀分布（即随机 31 位字符串），则上表显示了 X mod 10^6 不同输出的概率。第一组值出现的概率略大于 10^-6，其余的概率略小于 10^-6，意味着分布略有非均匀性。

> [!tip] 偏差可忽略
> 如上表所示，偏差很小，正如我们稍后将看到的，可以忽略不计：概率非常接近 10^-6。

#### A.4.2 暴力破解攻击

如果认证码由 d 个随机数字组成，则使用 v 次验证尝试的暴力破解攻击将以 sv/10^Digit 的概率成功。

然而，攻击者可以利用引理 1 预测的 HOTP-IDEAL 输出中的偏差来发动稍好的攻击。

即，它使用最可能值范围内的认证码进行认证尝试，即 0,...,r - 1 范围内的值，其中 (q,r) = IntDiv(2^31, 10^Digit)。

以下在我们安全模型中指定了一个发动此攻击的攻击者，并将成功概率估计为验证查询数的函数。

为简单起见，我们假设验证查询数最多为 r。当 N = 2^31 且 m = 10^6 时，r = 483,648，而节流值肯定小于此值，因此此假设并无太大限制。

**命题 1**

假设 m = 10^Digit < 2^31，令 (q,r) = IntDiv(2^31,m)。假设 s <= m。暴力破解攻击者 B-bf 使用 v <= r 个验证预言机查询攻击 HOTP。该攻击者不进行认证码预言机查询，成功概率为：

$$Adv(B\text{-}bf) = 1 - (1 - v(q+1)/2^{31})^s$$

约等于：

$$sv \cdot (q+1)/2^{31}$$

当 m = 10^6 时，q = 2,147。在这种情况下，使用 v 次验证尝试的暴力破解攻击成功概率为：

$$Adv(B\text{-}bf) \approx sv \cdot 2148/2^{31} = sv \cdot 1.00024045/10^6$$

如该等式所示，重同步参数 s 具有显著影响，因为攻击者的成功概率与 s 成正比。这意味着 s 不能设置得太大，否则会损害安全性。

#### A.4.3 暴力破解攻击是最佳可能攻击

一个核心问题是是否存在比暴力破解更好的攻击。特别是，暴力破解攻击没有尝试收集用户发送的认证码并试图对其进行密码分析以学习如何更好地构建认证码。这样做有帮助吗？是否有某种方法可以"学习"如何构建认证码，使成功率高于暴力破解攻击？

> [!info] 核心结论
> 以下说明这些问题的答案是否定的。无论攻击者使用什么策略，即使它看到并试图利用[[用户认证]]尝试的认证码，其成功概率不会超过暴力破解攻击——只要它观察到的认证次数不是极其巨大。这是关于该方案安全性的宝贵信息。

**命题 2**

假设 m = 10^Digit < 2^31，令 (q,r) = IntDiv(2^31,m)。令 B 为任何使用 v 个验证预言机查询和 a <= 2^c - s 个认证码预言机查询攻击 HOTP-IDEAL 的攻击者。则：

$$Adv(B) \le sv \cdot (q+1)/2^{31}$$

> [!note] 注
> 此结果的条件是攻击者看到的[[用户认证]]次数不超过 2^c - s，只要 c 足够大，这几乎不构成限制。

当 m = 10^6 时，q = 2,147。在这种情况下，命题 2 说明任何攻击 HOTP-IDEAL 并进行 v 次验证尝试的攻击者 B 的成功概率最多为：

**等式 1**

$$sv \cdot 2148/2^{31} \approx sv \cdot 1.00024045/10^6$$

即 B 的成功率不超过暴力破解攻击所达到的率。

### A.5 HOTP 的安全性分析

在前面的章节中，我们分析了实际认证算法 HOTP 的理想化对应物 HOTP-IDEAL 的安全性。我们现在证明，在对 H 的适当且广为接受的假设下，实际算法的安全性与理想化对应物基本相同。

所讨论的假设是 H 是一个安全的伪随机函数（PRF，Pseudorandom Function），即其输入-输出值在实践中与随机函数的值不可区分。

考虑一个攻击者 A，它被给定一个函数 f: {0,1}^c --> {0,1}^n 的预言机，最终输出一个比特。我们将 Adv(A) 表示为 A 的 prf-优势，代表攻击者区分其预言机是 H(K,.) 还是 {0,1}^c 到 {0,1}^n 的随机函数的能力。

一种可能的攻击基于对密钥 K 的穷举搜索。如果 A 运行 t 步，T 表示执行一次 H 计算的时间，则这种攻击的 prf-优势为 (t/T)2^{-k}。另一种可能的攻击是生日攻击 [PrOo]，其中 A 可以在 p 次预言机查询和大约 pT 的运行时间内获得 p^2/2^n 的优势。

我们的假设是这些是最佳可能的攻击。这转化为以下内容。

**假设 1**

令 T 表示执行一次 H 计算的时间。则如果 A 是任何运行时间最多为 t 且最多进行 p 次预言机查询的攻击者：

$$Adv(A) \le (t/T)/2^k + p^2/2^n$$

> [!tip] 实际意义
> 在实践中，此假设意味着 H 作为 PRF 非常安全。例如，给定 k = n = 160，运行时间为 2^60 且进行 2^40 次预言机查询的攻击者的优势最多约为 2^{-80}。

**定理 1**

假设 m = 10^Digit < 2^31，令 (q,r) = IntDiv(2^31,m)。令 B 为任何使用 v 个验证预言机查询、a <= 2^c - s 个认证码预言机查询且运行时间为 t 的攻击 HOTP 的攻击者。令 T 表示执行一次 H 计算的时间。如果假设 1 成立，则：

$$Adv(B) \le sv \cdot (q + 1)/2^{31} + (t/T)/2^k + (sv + a)^2/2^n$$

在实践中，(t/T)2^{-k} + (sv + a)^2 2^{-n} 项远小于 sv(q + 1)/2^n 项，因此上述说明在所有实际目的中，攻击 HOTP 的攻击者的成功率就是 sv(q + 1)/2^n，与 HOTP-IDEAL 相同，意味着 HOTP 算法在实践中基本上与其理想化对应物一样好。

在 m = 10^6 的 6 位数字输出情况下，这意味着进行 v 次认证尝试的攻击者的成功率最多为等式 1 给出的值。

例如，考虑运行时间最多为 2^60 且最多看到 2^40 次[[用户认证]]尝试的攻击者。这两个选择对攻击者来说都非常慷慨——攻击者通常不会有这些资源——但我们要说的是，即使如此强大的攻击者也不会比等式 1 所指示的更成功。

由于节流和对 s 的限制，我们可以安全地假设 sv <= 2^40。因此：

$$(t/T)/2^k + (sv + a)^2/2^n \le 2^{60}/2^{160} + (2^{41})^2/2^{160} \approx 2^{-78}$$

这远小于等式 1 的成功概率，与其相比可以忽略不计。

---

## 附录 B - SHA-1 攻击

本节讨论近期对 SHA-1 的攻击对基于 HMAC-SHA-1 的 HOTP 安全性的影响。我们首先讨论 SHA-1 的情况，然后讨论与 HMAC-SHA-1 和 HOTP 的关联。引用的参考文献在第 13 节中。

### B.1 SHA-1 状态

哈希函数 h 的碰撞是指两个不同的输入 x、y 使得 h(x) = h(y)。由于 SHA-1 输出 160 位，生日攻击在 2^{80} 次试验中可以找到碰撞。（一次试验即一次函数计算。）这曾被认为是最优的，直到 Wang、Yin 和 Yu 于 2005 年 2 月 15 日宣布他们找到了在 2^{69} 次试验中找到碰撞的攻击方法。

SHA-1 破解了吗？对于大多数实际用途，我们可能会说可能没有，因为发动攻击所需的资源是巨大的。我们可以这样来理解：估计所需时间与分解 760 位 RSA 模数的时间大致相同，这目前被认为是不可能完成的。

NIST 的 Burr 在 [Crack] 中被引述说"大型国家情报机构可以用几百万美元的计算机时间在合理的时间内完成此操作"。然而，这种计算可能除了此类资金充足的机构外都无法完成。

还应问的是，找到 SHA-1 碰撞对签名等实际应用的安全性有什么实际影响。要利用碰撞 x、y 来伪造签名，需要以某种方式获得 x 的签名，然后就可以伪造 y 的签名。这种损害程度取决于 y 的内容：攻击创建的 y 在应用上下文中可能没有意义。此外，需要选择消息攻击来获得 x 的签名。这在某些上下文中似乎是可能的，但在其他上下文中则不然。总的来说，对签名安全性的影响是否显著尚不清楚。

确实，人们可以在媒体上读到 SHA-1 已经"被破解"[Sha1]，加密和 SSL 已经"被破解"[Res]。媒体有放大事件的倾向：在新闻中宣布一组密码分析学家在攻击 SHA-1 方面做了非常有趣的理论工作几乎不会引起关注。

密码学家也很兴奋。但这主要是因为这是一个重要的理论突破。攻击只会随时间推移而改进：因此，重要的是监控哈希函数密码分析的任何进展，并为未来可能的实际破解做好准备，制定健全的迁移计划。

### B.2 HMAC-SHA-1 状态

对 SHA-1 的新攻击对 HMAC-SHA-1 的安全性没有影响。对后者的最佳攻击仍然需要发送者认证 2^{80} 条消息，攻击者才能创建伪造。为什么？

HMAC 不是哈希函数。它是一个使用哈希函数内部的消息认证码（MAC，Message Authentication Code）。MAC 依赖于密钥，而哈希函数不依赖。对于 MAC，需要担心的是伪造，而不是碰撞。HMAC 的设计使得哈希函数（这里是 SHA-1）中的碰撞不会导致 HMAC 的伪造。

回顾 HMAC-SHA-1(K,x) = SHA-1(K_o, SHA-1(K_i, x))，其中密钥 K_o、K_i 从 K 派生。假设攻击者找到了一对 x、y 使得 SHA-1(K_i, x) = SHA-1(K_i, y)。（称之为隐藏密钥碰撞。）那么如果能获得 x 的 MAC（这本身就是一项艰巨的任务），就可以伪造 y 的 MAC。（这些值是相同的。）但找到隐藏密钥碰撞比找到碰撞更难，因为攻击者不知道隐藏密钥 K_i。它可能只有 HMAC-SHA-1 使用密钥 K 的一些输出。迄今为止，没有任何声明或证据表明最近对 SHA-1 的攻击可以扩展到寻找隐藏密钥碰撞。

> [!info] 历史佐证
> 从历史上看，HMAC 的设计在这方面已经证明了自身。MD5 被认为已被破解，因为可以相对容易地找到该哈希函数的碰撞。但目前仍然没有比平凡的 2^{64} 时间生日攻击更好的针对 HMAC-MD5 的攻击。（MD5 输出 128 位，不是 160 位。）我们正在看到 HMAC 的这种强度在 SHA-1 上下文中再次发挥作用。

### B.3 HOTP 状态

由于 HMAC-SHA-1 没有出现新的弱点，因此对 HOTP 没有影响。对 HOTP 的最佳攻击仍然是本文档中描述的那些，即尝试猜测输出值。

HOTP 的安全性证明要求 HMAC-SHA-1 表现为伪随机函数。HMAC-SHA-1 作为伪随机函数的质量不受对 SHA-1 的新攻击的影响，因此这个已证明的保证也不受影响。

---

## 附录 C - HOTP 算法：参考实现

```java
/*
 * OneTimePasswordAlgorithm.java
 * OATH Initiative,
 * HOTP 一次性密码算法
 *
 */

/* 版权所有 (C) 2004, OATH. 保留所有权利.
 *
 * 复制和使用本软件的许可被授予，前提是
 * 在所有提及或引用本软件或此函数的材料中
 * 将其标识为"OATH HOTP Algorithm".
 *
 * 制作和使用衍生作品的许可也被授予，前提是
 * 此类作品在所有提及或引用衍生作品的材料中
 * 被标识为"derived from OATH HOTP algorithm".
 *
 * OATH (Open AuTHentication) 及其成员对本软件的
 * 商业适销性或针对任何特定目的的适用性不作
 * 任何声明.
 *
 * 本软件按"原样"提供，不附带任何明示或暗示的保证，
 * OATH 及其成员明确拒绝与本软件相关的任何保证或责任.
 *
 * 这些声明必须保留在本文档和/或软件的任何部分
 * 的任何副本中.
 */

package org.openauthentication.otp;

import java.io.IOException;
import java.io.File;
import java.io.DataInputStream;
import java.io.FileInputStream ;
import java.lang.reflect.UndeclaredThrowableException;

import java.security.GeneralSecurityException;
import java.security.NoSuchAlgorithmException;
import java.security.InvalidKeyException;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 * 此类包含用于计算一次性密码 (OTP) 的静态方法,
 * 使用 JCE 提供 HMAC-SHA-1.
 *
 * @author Loren Hart
 * @version 1.0
 */
public class OneTimePasswordAlgorithm {
    private OneTimePasswordAlgorithm() {}

    // 用于计算校验和数字
    //                                0  1  2  3  4  5  6  7  8  9
    private static final int[] doubleDigits =
                    { 0, 2, 4, 6, 8, 1, 3, 5, 7, 9 };

    /**
     * 使用信用卡算法计算校验和.
     * 此算法的优点是可以检测任何单个
     * 输入错误的数字以及任何相邻数字
     * 的单个交换.
     *
     * @param num 要计算校验和的数字
     * @param digits 数字的有效位数
     *
     * @return num 的校验和
     */
    public static int calcChecksum(long num, int digits) {
        boolean doubleDigit = true;
        int     total = 0;
        while (0 < digits--) {
            int digit = (int) (num % 10);
            num /= 10;
            if (doubleDigit) {
                digit = doubleDigits[digit];
            }
            total += digit;
            doubleDigit = !doubleDigit;
        }
        int result = total % 10;
        if (result > 0) {
            result = 10 - result;
        }
        return result;
    }

    /**
     * 此方法使用 JCE 提供 HMAC-SHA-1 算法.
     * HMAC 计算哈希消息认证码,
     * 在此情况下使用的哈希算法是 SHA1.
     *
     * @param keyBytes   用于 HMAC-SHA-1 密钥的字节
     * @param text       要认证的消息或文本.
     *
     * @throws NoSuchAlgorithmException 如果没有提供者使
     *       HmacSHA1 或 HMAC-SHA-1 摘要算法可用.
     * @throws InvalidKeyException
     *       提供的密钥不是有效的 HMAC-SHA-1 密钥.
     *
     */

    public static byte[] hmac_sha1(byte[] keyBytes, byte[] text)
        throws NoSuchAlgorithmException, InvalidKeyException
    {
//        try {
            Mac hmacSha1;
            try {
                hmacSha1 = Mac.getInstance("HmacSHA1");
            } catch (NoSuchAlgorithmException nsae) {
                hmacSha1 = Mac.getInstance("HMAC-SHA-1");
            }
            SecretKeySpec macKey =
        new SecretKeySpec(keyBytes, "RAW");
            hmacSha1.init(macKey);
            return hmacSha1.doFinal(text);
//        } catch (GeneralSecurityException gse) {
//            throw new UndeclaredThrowableException(gse);
//        }
    }

    private static final int[] DIGITS_POWER
  // 0 1  2   3    4     5      6       7        8
  = {1,10,100,1000,10000,100000,1000000,10000000,100000000};

    /**
     * 此方法为给定的一组参数生成 OTP 值.
     *
     * @param secret       共享密钥
     * @param movingFactor 计数器、时间或其他每次使用时
     *                     变化的值.
     * @param codeDigits   OTP 的数字位数, 不包括
     *                     校验和（如果有）.
     * @param addChecksum  指示是否应在校验和数字后
     *                     附加到 OTP 的标志.
     * @param truncationOffset MAC 结果中开始截断的
     *                     偏移量. 如果此值超出
     *                     0 ... 15 的范围, 则使用动态
     *                     截断.
     *                     动态截断是使用 MAC 最后一个
     *                     字节的最后 4 位来确定起始偏移量.
     * @throws NoSuchAlgorithmException 如果没有提供者使
     *                     HmacSHA1 或 HMAC-SHA-1
     *                     摘要算法可用.
     * @throws InvalidKeyException
     *                     提供的密钥不是
     *                     有效的 HMAC-SHA-1 密钥.
     *
     * @return 十进制数字字符串, 包含
     * {@link codeDigits} 位数字加上可选的校验和
     * 数字（如果请求）.
     */
    static public String generateOTP(byte[] secret,
               long movingFactor,
          int codeDigits,
               boolean addChecksum,
          int truncationOffset)
        throws NoSuchAlgorithmException, InvalidKeyException
    {
        // 将 movingFactor 值放入 text 字节数组
  String result = null;
  int digits = addChecksum ? (codeDigits + 1) : codeDigits;
        byte[] text = new byte[8];
        for (int i = text.length - 1; i >= 0; i--) {
            text[i] = (byte) (movingFactor & 0xff);
            movingFactor >>= 8;
        }

        // 计算 HMAC 哈希
        byte[] hash = hmac_sha1(secret, text);

        // 将选定字节放入结果 int
        int offset = hash[hash.length - 1] & 0xf;
  if ( (0<=truncationOffset) &&
         (truncationOffset<(hash.length-4)) ) {
      offset = truncationOffset;
  }
        int binary =
            ((hash[offset] & 0x7f) << 24)
            | ((hash[offset + 1] & 0xff) << 16)
            | ((hash[offset + 2] & 0xff) << 8)
            | (hash[offset + 3] & 0xff);

        int otp = binary % DIGITS_POWER[codeDigits];
  if (addChecksum) {
      otp =  (otp * 10) + calcChecksum(otp, codeDigits);
  }
  result = Integer.toString(otp);
  while (result.length() < digits) {
      result = "0" + result;
  }
  return result;
    }
}
```

---

## 附录 D - HOTP 算法：测试值

以下测试数据使用 ASCII 字符串 "12345678901234567890" 作为密钥：

Secret = 0x3132333435363738393031323334353637383930

**表 1** 详细列出了每个计数对应的中间 HMAC 值。

| Count | Hexadecimal HMAC-SHA-1(secret, count) |
|-------|---------------------------------------|
| 0 | cc93cf18508d94934c64b65d8ba7667fb7cde4b0 |
| 1 | 75a48a19d4cbe100644e8ac1397eea747a2d33ab |
| 2 | 0bacb7fa082fef30782211938bc1c5e70416ff44 |
| 3 | 66c28227d03a2d5529262ff016a1e6ef76557ece |
| 4 | a904c900a64b35909874b33e61c5938a8e15ed1c |
| 5 | a37e783d7b7233c083d4f62926c7a25f238d0316 |
| 6 | bc9cd28561042c83f219324d3c607256c03272ae |
| 7 | a4fb960c0bc06e1eabb804e5b397cdc4b45596fa |
| 8 | 1b3c89f65e6c9e883012052823443f048b4332db |
| 9 | 1637409809a679dc698207310c8c7fc07290d9e5 |

**表 2** 详细列出了每个计数对应的截断值（十六进制和十进制）以及 HOTP 值。

| Count | Truncated Hexadecimal | Truncated Decimal | HOTP |
|-------|-----------------------|-------------------|------|
| 0 | 4c93cf18 | 1284755224 | 755224 |
| 1 | 41397eea | 1094287082 | 287082 |
| 2 | 82fef30 | 137359152 | 359152 |
| 3 | 66ef7655 | 1726969429 | 969429 |
| 4 | 61c5938a | 1640338314 | 338314 |
| 5 | 33c083d4 | 868254676 | 254676 |
| 6 | 7256c032 | 1918287922 | 287922 |
| 7 | 4e5b397 | 82162583 | 162583 |
| 8 | 2823443f | 673399871 | 399871 |
| 9 | 2679dc69 | 645520489 | 520489 |

---

## 附录 E - 扩展

本节介绍了 HOTP 算法的若干增强方案。这些不是推荐扩展或标准算法的一部分，而是可用于定制实现的变体。

### E.1 数字位数

在安全性方面的一个简单增强是从 HMAC-SHA-1 值中提取更多数字。

例如，计算 HOTP 值对 10^8 取模以构建 8 位 HOTP 值，会将攻击者的成功概率从 sv/10^6 降低到 sv/10^8。

这可以提供改善可用性的机会，例如通过增加 T 和/或 s，同时仍然获得更好的整体安全性。例如，s = 10 且 10v/10^8 = v/10^7 < v/10^6，这是 s = 1 时 6 位码的理论最优值。

### E.2 字母数字值

另一种选择是使用 A-Z 和 0-9 值；或者使用从字母数字字母表中取出的 32 个符号的子集，以避免字符之间的任何混淆：0、O 和 Q 以及 l、1 和 I 非常相似，在小显示屏上可能看起来相同。

直接后果是，6 位 HOTP 值的安全性约为 sv/32^6，8 位 HOTP 值约为 sv/32^8。

32^6 > 10^9，因此 6 位字母数字 HOTP 码的安全性略优于 9 位 HOTP 值，这是所提出算法支持的 HOTP 码的最大长度。

32^8 > 10^12，因此 8 位字母数字 HOTP 码的安全性显著优于 9 位 HOTP 值。

根据用于显示和输入 HOTP 值的应用程序和令牌/接口，选择字母数字值可能是在降低成本和对用户影响的同时提高安全性的简单有效方式。

### E.3 HOTP 值序列

正如我们建议在重同步时输入短序列（例如 2 或 3 个）的 HOTP 值，我们可以将此概念推广到协议中，添加一个参数 L 来定义要输入的 HOTP 序列长度。

默认情况下，L 值应设为 1，但如果需要提高安全性，可以要求用户（可能是在短时间内或特定操作期间）输入 L 个 HOTP 值。

这是在不增加 HOTP 长度或使用字母数字值的情况下加强安全性的另一种方式。

> [!note] 定期同步
> 系统也可以被编程为定期（例如每晚、每周两次等）请求同步，为此目的要求输入 L 个 HOTP 值序列。

### E.4 基于计数器的重同步方法

在这种情况下，我们假设客户端不仅可以访问和发送 HOTP 值，还可以发送其他信息，更具体地说是计数器值。

在这种情况下，一种更高效和安全的重同步方法是可能的。客户端应用程序将不仅发送 HOTP 客户端值，而是发送 HOTP 客户端值和相关的 C-client 计数器值，HOTP 值充当计数器的消息认证码。

**重同步基于计数器协议 (RCP)**

服务器接受以下条件全部为真时（其中 C-server 是其当前计数器值）：

1. C-client >= C-server
2. C-client - C-server <= s
3. 检查 HOTP 客户端是否为有效的 HOTP(K, C-Client)
4. 如果为真，服务器将 C 设置为 C-client + 1，客户端认证通过

> [!tip] RCP 的优势
> 在这种情况下，不再需要管理前瞻窗口。攻击者的成功概率仅为 v/10^6，即大约百万分之一。一个附带好处是显然可以将 s "无限"增大，从而在不影响安全性的情况下改善系统可用性。

此重同步协议应在客户端和服务器应用程序的相关影响被认为可接受时使用。

### E.5 数据字段

另一个有趣的选项是引入 Data（数据）字段，用于生成一次性密码值：HOTP(K, C, [Data])，其中 Data 是可选字段，可以是各种身份相关信息的拼接，例如 Data = Address | PIN。

我们也可以使用定时器，作为唯一的移动因子或与计数器结合使用——在这种情况下，例如 Data = Timer，其中 Timer 可以是 UNIX 时间（自 1970/1/1 起的 GMT 秒数）除以某个因子（8、16、32 等），以给出特定的时间步长。一次性密码的时间窗口等于时间步长乘以之前定义的重同步参数。例如，如果取 64 秒作为时间步长，7 作为重同步参数，我们获得 +/- 3 分钟的接受窗口。

使用 Data 字段为算法实现提供了更多灵活性，前提是 Data 字段被明确定义。

---

## 作者地址

David M'Raihi（发送评论和问题的主要联系人）
VeriSign, Inc.
685 E. Middlefield Road
Mountain View, CA 94043 USA

Phone: 1-650-426-3832
EMail: dmraihi@verisign.com

Mihir Bellare
Dept of Computer Science and Engineering, Mail Code 0114
University of California at San Diego
9500 Gilman Drive
La Jolla, CA 92093, USA

EMail: mihir@cs.ucsd.edu

Frank Hoornaert
VASCO Data Security, Inc.
Koningin Astridlaan 164
1780 Wemmel, Belgium

EMail: frh@vasco.com

David Naccache
Gemplus Innovation
34 rue Guynemer, 92447,
Issy les Moulineaux, France
and
Information Security Group,
Royal Holloway,
University of London, Egham,
Surrey TW20 0EX, UK

EMail: david.naccache@gemplus.com, david.naccache@rhul.ac.uk

Ohad Ranen
Aladdin Knowledge Systems Ltd.
15 Beit Oved Street
Tel Aviv, Israel 61110

EMail: Ohad.Ranen@ealaddin.com

## 完整版权声明

Copyright (C) The Internet Society (2005).

> [!note] 法律声明
> 本文档受 BCP 78 中包含的权利、许可和限制的约束，除其中规定外，作者保留所有权利。
>
> 本文档及其中包含的信息按"原样"提供，贡献者、其所代表或受其赞助的组织（如有）、Internet Society 和 Internet Engineering Task Force 不承担任何明示或暗示的保证，包括但不限于对使用本文信息不侵犯任何权利的保证，或对适销性或特定用途适用性的任何暗示保证。

## 知识产权

> [!note] IETF 知识产权声明
> IETF 对任何知识产权或其他权利的有效性或范围不持立场，这些权利可能被声称与本文档中描述的技术的实现或使用有关，或任何此类权利下的许可是否可能或可能不可获得的程度；IETF 也不表示已做出任何独立努力来识别此类权利。有关 RFC 文档中权利程序的信息可在 BCP 78 和 BCP 79 中找到。
>
> 提交给 IETF 秘书处的 IPR 披露副本以及任何许可保证，或试图获得此类专有权利的通用许可或许可的结果，可从 IETF 在线 IPR 存储库获取：http://www.ietf.org/ipr。
>
> IETF 邀请任何相关方提请其注意任何可能涵盖实现本标准所需技术的版权、专利或专利申请或其他专有权利。请将信息发送至 IETF：ietf-ipr@ietf.org。

## 致谢

RFC Editor 功能的资金目前由 Internet Society 提供。
