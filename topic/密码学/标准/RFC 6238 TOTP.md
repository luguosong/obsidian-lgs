---
title: TOTP 基于时间的一次性密码算法
description: RFC 6238 定义了基于时间的一次性密码（TOTP）算法，扩展 HOTP 以支持时间因子，广泛用于双因素认证
tags:
  - 密码学
  - TOTP
  - 双因素认证
  - RFC
---

> [!info] RFC 信息
> - **RFC 编号**：6238
> - **标题**：TOTP: Time-Based One-Time Password Algorithm
> - **类别**：Informational
> - **发布日期**：2011 年 5 月
> - **作者**：D. M'Raihi（Verisign）、S. Machani（Diversinet）、M. Pei（Symantec）、J. Rydell（Portwise）

## 摘要

本文档描述了一次性密码（OTP，One-Time Password）算法的一个扩展，即对 [RFC 4226](https://www.rfc-editor.org/rfc/rfc4226) 中定义的基于 HMAC 的一次性密码（HOTP，HMAC-based One-Time Password）算法进行扩展，以支持基于时间的移动因子（moving factor）。HOTP 算法指定了一个基于事件的 OTP 算法，其移动因子是一个事件计数器。本文将移动因子建立在时间值之上。OTP 算法的基于时间变体提供了短期有效的 OTP 值，有利于增强安全性。

所提出的算法可用于广泛的网络应用场景，从远程 VPN（Virtual Private Network）访问和 Wi-Fi 网络登录到面向事务的 Web 应用。作者认为，一个通用且共享的算法将通过实现商业和开源实现之间的互操作性，促进双因素认证在互联网上的采用。

## 备忘录状态

本文档不是互联网标准跟踪规范；仅为信息目的而发布。

本文档是互联网工程任务组（IETF，Internet Engineering Task Force）的产品。它代表了 IETF 社区的共识。它已经过公开审查，并已被互联网工程指导组（IESG）批准发布。并非所有被 IESG 批准的文档都具备成为任何级别互联网标准的资格；参见 [RFC 5741](https://www.rfc-editor.org/rfc/rfc5741) 第 2 节。

有关本文档的当前状态、任何勘误以及如何提供反馈的信息，可在 http://www.rfc-editor.org/info/rfc6238 获取。

## 版权声明

Copyright (c) 2011 IETF Trust and the persons identified as the document authors. All rights reserved.

本文档受 BCP 78 和 IETF Trust 关于 IETF 文档的法律条款（http://trustee.ietf.org/license-info）的约束。请仔细阅读这些文档，因为它们描述了您对本文档的权利和限制。从本文档中提取的代码组件必须包含简化 BSD 许可证的文本，如 Trust 法律条款第 4.e 节所述，并且不提供任何担保。

## 目录

- [[#1. 引言]]
	- [[#1.1 范围]]
	- [[#1.2 背景]]
- [[#2. 符号与术语]]
- [[#3. 算法需求]]
- [[#4. TOTP 算法]]
	- [[#4.1 符号说明]]
	- [[#4.2 算法描述]]
- [[#5. 安全考虑]]
	- [[#5.1 概述]]
	- [[#5.2 验证与时间步长大小]]
- [[#6. 重同步]]
- [[#7. 致谢]]
- [[#8. 参考文献]]
- [[#附录 A. TOTP 算法：参考实现]]
- [[#附录 B. 测试向量]]

## 1. 引言

### 1.1 范围

本文档描述了一次性密码（OTP）算法的一个扩展，即对 [RFC4226](https://www.rfc-editor.org/rfc/rfc4226) 中定义的基于 HMAC 的一次性密码（HOTP）算法进行扩展，以支持基于时间的移动因子。

### 1.2 背景

如 [RFC4226](https://www.rfc-editor.org/rfc/rfc4226) 所定义，HOTP 算法基于 HMAC-SHA-1 算法（如 [RFC2104](https://www.rfc-editor.org/rfc/rfc2104) 所规定），并将其应用于一个递增的计数值，该计数器值在 HMAC 计算中代表消息。

基本原理是，将 HMAC-SHA-1 计算的输出进行截断，以获得用户友好的值：

```
HOTP(K,C) = Truncate(HMAC-SHA-1(K,C))
```

其中 Truncate 表示可以将 HMAC-SHA-1 值转换为 HOTP 值的函数。K 和 C 分别表示共享密钥（shared secret）和计数值；详细定义参见 [RFC4226](https://www.rfc-editor.org/rfc/rfc4226)。

TOTP 是该算法的基于时间变体，其中从时间参考和时间步长推导出的值 T 替换了 HOTP 计算中的计数器 C。

> [!note] HMAC 哈希函数选择
> TOTP 实现可以使用基于 SHA-256 或 SHA-512 [SHA2](http://csrc.nist.gov/publications/fips/fips180-3/fips180-3_final.pdf) 哈希函数的 HMAC-SHA-256 或 HMAC-SHA-512 函数，以替代 [RFC4226](https://www.rfc-editor.org/rfc/rfc4226) 中为 HOTP 计算指定的 HMAC-SHA-1 函数。

## 2. 符号与术语

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按照 [RFC2119](https://www.rfc-editor.org/rfc/rfc2119) 中的描述进行解释。

## 3. 算法需求

本节总结了设计 TOTP 算法时考虑的需求。

- **R1**：证明者（prover，如令牌 token、软令牌 soft token）和验证者（verifier，即认证或验证服务器）必须知道或能够推导出当前的 Unix 时间（即自 1970 年 1 月 1 日 UTC 午夜以来经过的秒数），以用于 OTP 生成。有关常见的"Unix 时间"的更详细定义，参见 [UT](http://en.wikipedia.org/wiki/Unix_time)。证明者使用的时间精度会影响时钟同步的频率；参见第 6 节。

- **R2**：证明者和验证者必须共享相同的密钥，或者掌握密钥变换的知识以生成共享密钥。

- **R3**：算法必须使用 HOTP [RFC4226](https://www.rfc-editor.org/rfc/rfc4226) 作为关键构建块。

- **R4**：证明者和验证者必须使用相同的时间步长值 X。

- **R5**：每个证明者必须有唯一的密钥。

- **R6**：密钥应当随机生成或使用密钥派生算法（key derivation algorithm）生成。

- **R7**：密钥可以存储在防篡改设备（tamper-resistant device）中，且应当受到保护以防止未经授权的访问和使用。

## 4. TOTP 算法

HOTP 算法的这一变体指定了基于将计数器表示为时间因子来计算一次性密码值的方法。

### 4.1 符号说明

- **X** 表示以秒为单位的时间步长（默认值 X = 30 秒），是一个系统参数。

- **T0** 是开始计算时间步长的 Unix 时间（默认值为 0，即 Unix 纪元），也是一个系统参数。

### 4.2 算法描述

基本上，我们将 TOTP 定义为 `TOTP = HOTP(K, T)`，其中 T 是一个整数，表示从初始计数时间 T0 到当前 Unix 时间之间的时间步数。

更具体地说，`T = (Current Unix time - T0) / X`，其中计算使用默认的向下取整函数（floor function）。

> [!example] 示例
> 当 T0 = 0 且时间步长 X = 30 时：
> - 如果当前 Unix 时间为 59 秒，则 T = 1
> - 如果当前 Unix 时间为 60 秒，则 T = 2

当时间值 T 超过 2038 年之后时，此算法的实现必须支持大于 32 位整数的时间值 T。系统参数 X 和 T0 的值在配给过程（provisioning process）中预先确定，并作为配给步骤的一部分在证明者和验证者之间传递。配给流程不在本文档的范围内；有关此类配给容器规范，请参阅 [RFC6030](https://www.rfc-editor.org/rfc/rfc6030)。

## 5. 安全考虑

### 5.1 概述

此算法的安全性和强度取决于底层构建块 HOTP 的属性，HOTP 是一个基于使用 SHA-1 作为哈希函数的 HMAC [RFC2104](https://www.rfc-editor.org/rfc/rfc2104) 的构造。

[RFC4226](https://www.rfc-editor.org/rfc/rfc4226) 中详细的安全分析结论是，在所有实际用途中，动态截断（dynamic truncation）在 不同输入上的输出是均匀且独立分布的字符串。

该分析表明，对 HOTP 函数的最佳可能攻击是暴力破解攻击（brute force attack）。

> [!warning] 密钥生成
> 如算法需求部分所述，密钥应当随机选择或使用经过适当随机值种子的密码学强伪随机生成器（cryptographically strong pseudorandom generator）生成。密钥长度应当与 HMAC 输出长度一致，以促进互操作性。

我们建议遵循 [RFC4086](https://www.rfc-editor.org/rfc/rfc4086) 中的建议进行所有伪随机和随机数生成。用于生成密钥的伪随机数应当成功通过 [CN](http://www.gemplus.com/smart/rd/publications/pdf/CN99maur.pdf) 中指定的随机性测试，或类似的公认测试。

所有通信应当通过安全通道进行，例如 SSL/TLS（Secure Socket Layer/Transport Layer Security）[RFC5246](https://www.rfc-editor.org/rfc/rfc5246) 或 IPsec 连接 [RFC4301](https://www.rfc-editor.org/rfc/rfc4301)。

我们还建议在验证系统中安全地存储密钥，更具体地说，使用防篡改硬件加密对密钥进行加密，仅在需要时暴露：例如，在需要验证 OTP 值时解密密钥，并立即重新加密，以将密钥在 RAM 中的暴露时间限制在很短的时间段内。

密钥存储必须位于安全区域，以尽可能避免对验证系统和密钥数据库的直接攻击。特别是，对密钥材料的访问应仅限于验证系统所需的程序和进程。

### 5.2 验证与时间步长大小

在同一时间步内生成的 OTP 将是相同的。当验证系统收到 OTP 时，它不知道客户端生成 OTP 时的精确时间戳。验证系统通常使用收到 OTP 时的时间戳进行 OTP 比较。由于网络延迟，OTP 生成时间和 OTP 到达接收系统的时间之间的间隔（以 T 来衡量，即自 T0 以来的时间步数）可能很大。验证系统处的接收时间和实际的 OTP 生成可能不在产生相同 OTP 的同一时间步窗口内。当 OTP 在时间步窗口末尾生成时，接收时间最有可能落入下一个时间步窗口。

> [!tip] 验证策略建议
> 验证系统通常应设置一个可接受的 OTP 传输延迟窗口策略进行验证。验证系统不仅应将 OTP 与接收时间戳进行比较，还应与传输延迟范围内的过去时间戳进行比较。较大的可接受延迟窗口会暴露更大的攻击窗口。我们建议最多允许一个时间步作为网络延迟。

时间步长大小对安全性和可用性都有影响。较大的时间步长意味着 OTP 被验证系统接受的 有效窗口更大。使用较大时间步长的含义如下：

**第一，较大的时间步长暴露更大的攻击窗口。** 当 OTP 在被消费之前生成并暴露给第三方时，第三方可以在该时间步窗口内消费该 OTP。

我们建议默认时间步长为 **30 秒**。这个 30 秒的默认值是在安全性和可用性之间取得平衡而选择的。

**第二，下一个不同的 OTP 必须在下一个时间步窗口中生成。** 用户必须等到时钟从上次提交移动到下一个时间步窗口。等待时间可能不完全是时间步的长度，这取决于上一个 OTP 的生成时间。例如，如果上一个 OTP 是在时间步窗口的中间点生成的，则下一个 OTP 的等待时间是时间步长度的一半。通常，较大的时间步窗口意味着用户在上一次成功的 OTP 验证后需要等待更长时间才能获得下一个有效的 OTP。过大的窗口（例如 10 分钟）很可能不适合典型的互联网登录场景；用户可能无法在 10 分钟内获得下一个 OTP，因此不得不在 10 分钟后重新登录同一网站。

> [!warning] OTP 重放防护
> 注意，证明者可能在给定的时间步窗口内多次向验证者发送相同的 OTP。验证者在第一次 OTP 成功验证后**不得**接受该 OTP 的第二次尝试，以确保 OTP 的一次性使用。

## 6. 重同步

由于客户端和验证服务器之间可能存在时钟漂移（clock drift），我们建议验证器设置一个特定限制，规定证明者在被拒绝之前可以"失同步"的时间步数。

此限制可以设置为从收到 OTP 值时计算的当前时间步向前和向后。如果时间步为推荐的 30 秒，且验证器设置为仅向后接受两个时间步，则最大经过时间漂移约为 89 秒，即计算的时间步中的 29 秒加上两个向后时间步的 60 秒。

这意味着验证器可以针对当前时间执行一次验证，然后对每个向后步再执行两次验证（总共 3 次验证）。成功验证后，验证服务器可以以时间步数为单位记录令牌检测到的时钟漂移。当在此步骤之后收到新的 OTP 时，验证器可以使用已调整的当前时间戳（根据令牌记录的时间步时钟漂移数进行调整）来验证 OTP。

此外，需要注意的是，证明者未向验证系统发送 OTP 的时间越长，证明者和验证者之间积累的时钟漂移就（可能）越长。在这种情况下，如果漂移超过允许的阈值，上述自动重同步可能无法工作。应使用额外的认证措施来安全地认证证明者，并显式重同步证明者和验证器之间的时钟漂移。

## 7. 致谢

本文档的作者感谢以下人员对本规范的贡献和支持：Hannes Tschofenig、Jonathan Tuliani、David Dix、Siddharth Bajaj、Stu Veath、Shuh Chang、Oanh Hoang、John Huang 和 Siddhartha Mohapatra。

## 8. 参考文献

### 8.1 规范性引用

- [RFC2104] Krawczyk, H., Bellare, M., and R. Canetti, "HMAC: Keyed-Hashing for Message Authentication", RFC 2104, February 1997.
- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC4086] Eastlake 3rd, D., Schiller, J., and S. Crocker, "Randomness Recommendations for Security", BCP 106, RFC 4086, June 2005.
- [RFC4226] M'Raihi, D., Bellare, M., Hoornaert, F., Naccache, D., and O. Ranen, "HOTP: An HMAC-Based One-Time Password Algorithm", RFC 4226, December 2005.
- [SHA2] NIST, "FIPS PUB 180-3: Secure Hash Standard (SHS)", October 2008, <http://csrc.nist.gov/publications/fips/fips180-3/fips180-3_final.pdf>.

### 8.2 信息性引用

- [CN] Coron, J. and D. Naccache, "An Accurate Evaluation of Maurer's Universal Test", LNCS 1556, February 1999, <http://www.gemplus.com/smart/rd/publications/pdf/CN99maur.pdf>.
- [RFC4301] Kent, S. and K. Seo, "Security Architecture for the Internet Protocol", RFC 4301, December 2005.
- [RFC5246] Dierks, T. and E. Rescorla, "The Transport Layer Security (TLS) Protocol Version 1.2", RFC 5246, August 2008.
- [RFC6030] Hoyer, P., Pei, M., and S. Machani, "Portable Symmetric Key Container (PSKC)", RFC 6030, October 2010.
- [UT] Wikipedia, "Unix time", February 2011, <http://en.wikipedia.org/wiki/Unix_time>.

## 附录 A. TOTP 算法：参考实现

```java
/**
Copyright (c) 2011 IETF Trust and the persons identified as
authors of the code. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, is permitted pursuant to, and subject to the license
terms contained in, the Simplified BSD License set forth in Section
4.c of the IETF Trust's Legal Provisions Relating to IETF Documents
(http://trustee.ietf.org/license-info).
*/

import java.lang.reflect.UndeclaredThrowableException;
import java.security.GeneralSecurityException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.math.BigInteger;
import java.util.TimeZone;

/**
 * OATH TOTP 算法的示例实现。
 * 访问 www.openauthentication.org 了解更多信息。
 *
 * @author Johan Rydell, PortWise, Inc.
 */

public class TOTP {

    private TOTP() {}

    /**
     * 此方法使用 JCE 提供加密算法。
     * HMAC 使用加密哈希算法作为参数计算哈希消息认证码。
     *
     * @param crypto: 加密算法（HmacSHA1、HmacSHA256、HmacSHA512）
     * @param keyBytes: 用于 HMAC 密钥的字节
     * @param text: 要认证的消息或文本
     */

    private static byte[] hmac_sha(String crypto, byte[] keyBytes,
            byte[] text){
        try {
            Mac hmac;
            hmac = Mac.getInstance(crypto);
            SecretKeySpec macKey =
                new SecretKeySpec(keyBytes, "RAW");
            hmac.init(macKey);
            return hmac.doFinal(text);
        } catch (GeneralSecurityException gse) {
            throw new UndeclaredThrowableException(gse);
        }
    }

    /**
     * 此方法将 HEX 字符串转换为 Byte[]
     *
     * @param hex: HEX 字符串
     *
     * @return: 字节数组
     */

    private static byte[] hexStr2Bytes(String hex){
        // 添加一个字节以获得正确的转换
        // 以 "0" 开头的值可以被转换
        byte[] bArray = new BigInteger("10" + hex,16).toByteArray();

        // 复制所有真实字节，不包括"第一个"
        byte[] ret = new byte[bArray.length - 1];
        for (int i = 0; i < ret.length; i++)
            ret[i] = bArray[i+1];
        return ret;
    }

    private static final int[] DIGITS_POWER
    // 0 1  2   3    4     5      6       7        8
    = {1,10,100,1000,10000,100000,1000000,10000000,100000000 };

    /**
     * 此方法为给定参数集生成 TOTP 值。
     *
     * @param key: 共享密钥，HEX 编码
     * @param time: 反映时间的值
     * @param returnDigits: 要返回的位数
     *
     * @return: 包含 {@link truncationDigits} 位数字的十进制数字字符串
     */

    public static String generateTOTP(String key,
            String time,
            String returnDigits){
        return generateTOTP(key, time, returnDigits, "HmacSHA1");
    }

    /**
     * 此方法为给定参数集生成 TOTP 值。
     *
     * @param key: 共享密钥，HEX 编码
     * @param time: 反映时间的值
     * @param returnDigits: 要返回的位数
     *
     * @return: 包含 {@link truncationDigits} 位数字的十进制数字字符串
     */

    public static String generateTOTP256(String key,
            String time,
            String returnDigits){
        return generateTOTP(key, time, returnDigits, "HmacSHA256");
    }

    /**
     * 此方法为给定参数集生成 TOTP 值。
     *
     * @param key: 共享密钥，HEX 编码
     * @param time: 反映时间的值
     * @param returnDigits: 要返回的位数
     *
     * @return: 包含 {@link truncationDigits} 位数字的十进制数字字符串
     */

    public static String generateTOTP512(String key,
            String time,
            String returnDigits){
        return generateTOTP(key, time, returnDigits, "HmacSHA512");
    }

    /**
     * 此方法为给定参数集生成 TOTP 值。
     *
     * @param key: 共享密钥，HEX 编码
     * @param time: 反映时间的值
     * @param returnDigits: 要返回的位数
     * @param crypto: 要使用的加密函数
     *
     * @return: 包含 {@link truncationDigits} 位数字的十进制数字字符串
     */

    public static String generateTOTP(String key,
            String time,
            String returnDigits,
            String crypto){
        int codeDigits = Integer.decode(returnDigits).intValue();
        String result = null;

        // 使用计数器
        // 前 8 个字节用于移动因子
        // 符合基础 RFC 4226 (HOTP)
        while (time.length() < 16 )
            time = "0" + time;

        // 将 HEX 转换为 Byte[]
        byte[] msg = hexStr2Bytes(time);
        byte[] k = hexStr2Bytes(key);

        byte[] hash = hmac_sha(crypto, k, msg);

        // 将选定的字节放入结果 int 中
        int offset = hash[hash.length - 1] & 0xf;

        int binary =
            ((hash[offset] & 0x7f) << 24) |
            ((hash[offset + 1] & 0xff) << 16) |
            ((hash[offset + 2] & 0xff) << 8) |
            (hash[offset + 3] & 0xff);

        int otp = binary % DIGITS_POWER[codeDigits];

        result = Integer.toString(otp);
        while (result.length() < codeDigits) {
            result = "0" + result;
        }
        return result;
    }

    public static void main(String[] args) {
        // HMAC-SHA1 的种子 - 20 字节
        String seed = "3132333435363738393031323334353637383930";
        // HMAC-SHA256 的种子 - 32 字节
        String seed32 = "3132333435363738393031323334353637383930" +
        "313233343536373839303132";
        // HMAC-SHA512 的种子 - 64 字节
        String seed64 = "3132333435363738393031323334353637383930" +
        "3132333435363738393031323334353637383930" +
        "3132333435363738393031323334353637383930" +
        "31323334";
        long T0 = 0;
        long X = 30;
        long testTime[] = {59L, 1111111109L, 1111111111L,
                1234567890L, 2000000000L, 20000000000L};

        String steps = "0";
        DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        df.setTimeZone(TimeZone.getTimeZone("UTC"));

        try {
            System.out.println(
                    "+---------------+-----------------------+" +
            "------------------+--------+--------+");
            System.out.println(
                    "|  Time(sec)    |   Time (UTC format)   " +
            "| Value of T(Hex)  |  TOTP  | Mode   |");
            System.out.println(
                    "+---------------+-----------------------+" +
            "------------------+--------+--------+");

            for (int i=0; i<testTime.length; i++) {
                long T = (testTime[i] - T0)/X;
                steps = Long.toHexString(T).toUpperCase();
                while (steps.length() < 16) steps = "0" + steps;
                String fmtTime = String.format("%1$-11s", testTime[i]);
                String utcTime = df.format(new Date(testTime[i]*1000));
                System.out.print("|  " + fmtTime + "  |  " + utcTime +
                        "  | " + steps + " |");
                System.out.println(generateTOTP(seed, steps, "8",
                "HmacSHA1") + "| SHA1   |");
                System.out.print("|  " + fmtTime + "  |  " + utcTime +
                        "  | " + steps + " |");
                System.out.println(generateTOTP(seed32, steps, "8",
                "HmacSHA256") + "| SHA256 |");
                System.out.print("|  " + fmtTime + "  |  " + utcTime +
                        "  | " + steps + " |");
                System.out.println(generateTOTP(seed64, steps, "8",
                "HmacSHA512") + "| SHA512 |");

                System.out.println(
                        "+---------------+-----------------------+" +
                "------------------+--------+--------+");
            }
        }catch (final Exception e){
            System.out.println("Error : " + e);
        }
    }
}
```

## 附录 B. 测试向量

本节提供了可用于 HOTP 基于时间变体算法互操作性测试的测试值。

测试令牌的共享密钥使用 ASCII 字符串值 `"12345678901234567890"`。当时间步长 X = 30，Unix 纪元作为计算时间步长的初始值（T0 = 0）时，TOTP 算法对于指定的模式和 时间戳将显示以下值。

| 时间（秒） | UTC 时间 | T 值（十六进制） | TOTP | 模式 |
|:---:|:---:|:---:|:---:|:---:|
| 59 | 1970-01-01 00:00:59 | 0000000000000001 | 94287082 | SHA1 |
| 59 | 1970-01-01 00:00:59 | 0000000000000001 | 46119246 | SHA256 |
| 59 | 1970-01-01 00:00:59 | 0000000000000001 | 90693936 | SHA512 |
| 1111111109 | 2005-03-18 01:58:29 | 00000000023523EC | 07081804 | SHA1 |
| 1111111109 | 2005-03-18 01:58:29 | 00000000023523EC | 68084774 | SHA256 |
| 1111111109 | 2005-03-18 01:58:29 | 00000000023523EC | 25091201 | SHA512 |
| 1111111111 | 2005-03-18 01:58:31 | 00000000023523ED | 14050471 | SHA1 |
| 1111111111 | 2005-03-18 01:58:31 | 00000000023523ED | 67062674 | SHA256 |
| 1111111111 | 2005-03-18 01:58:31 | 00000000023523ED | 99943326 | SHA512 |
| 1234567890 | 2009-02-13 23:31:30 | 000000000273EF07 | 89005924 | SHA1 |
| 1234567890 | 2009-02-13 23:31:30 | 000000000273EF07 | 91819424 | SHA256 |
| 1234567890 | 2009-02-13 23:31:30 | 000000000273EF07 | 93441116 | SHA512 |
| 2000000000 | 2033-05-18 03:33:20 | 0000000003F940AA | 69279037 | SHA1 |
| 2000000000 | 2033-05-18 03:33:20 | 0000000003F940AA | 90698825 | SHA256 |
| 2000000000 | 2033-05-18 03:33:20 | 0000000003F940AA | 38618901 | SHA512 |
| 20000000000 | 2603-10-11 11:33:20 | 0000000027BC86AA | 65353130 | SHA1 |
| 20000000000 | 2603-10-11 11:33:20 | 0000000027BC86AA | 77737706 | SHA256 |
| 20000000000 | 2603-10-11 11:33:20 | 0000000027BC86AA | 47863826 | SHA512 |

> 表 1：TOTP 测试向量表
