---
title: PKCS#10 证书签名请求
description: RFC 2986 - 证书签名请求语法规范，定义 CSR 的 ASN.1 结构
tags:
  - 密码学
  - PKCS10
  - CSR
  - 证书
  - ASN.1
  - RFC
---

# PKCS#10：证书签名请求语法规范 (Certification Request Syntax Specification) Version 1.7

> [!info] RFC 信息
> - **RFC 编号**：2986
> - **类别**：Informational
> - **发布日期**：2000 年 11 月
> - **作者**：M. Nystrom、B. Kaliski (RSA Security)
> - **替代**：RFC 2314

> [!abstract] 摘要
> 本文档是 RSA Laboratories 公钥密码学标准 (PKCS) 系列中 PKCS #10 v1.7 的再版。本文档描述了证书签名请求的语法。

## 1. 引言

本文档描述证书签名请求的语法。证书签名请求由一个可分辨名称 (DN)、一个公钥和可选的一组属性组成，由请求认证的实体签名。证书签名请求发送给证书颁发机构 (CA)，CA 将请求转换为 X.509 公钥证书。

包含一组属性的目的有两方面：提供关于给定实体的其他信息或一个"质询密码"（通过该密码实体可稍后请求证书吊销）；以及提供要包含在 X.509 证书中的属性。PKCS #9 中给出了属性的非穷尽列表。

> [!note]
> CA 也可能要求非电子形式的请求，也可能返回非电子形式的回复。此类形式的描述不在本文档范围内，可从 CA 处获取。

本文档的初步预期应用是支持 PKCS #7 密码消息，但预计将开发其他应用。

## 2. 定义和记法

### 2.1. 定义

本文档适用以下定义：

- **ALGORITHM** — X.509 中定义的信息对象类，用于描述由算法（唯一对象标识符）及其参数（任意 ASN.1 类型）组成的对象。此类的对象值可由 ASN.1 类型 `AlgorithmIdentifier{}` 表示。
- **AlgorithmIdentifier{}** — 本文档定义的 X.509 类型 AlgorithmIdentifier 的有用参数化版本。此类型将算法对象标识符与其关联的参数类型紧密绑定。
- **ASN.1** — 抽象语法记法一 (Abstract Syntax Notation One)，由 ASN.1 标准 ([X.680]-[X.683]) 定义。
- **ATTRIBUTE** — 此类描述由属性（唯一对象标识符）和关联的一组属性值（任意 ASN.1 类型）组成的对象。
- **Attribute{}** — 本文档定义的 X.501 类型 Attribute 的有用参数化版本。
- **BER** — ASN.1 的基本编码规则 (Basic Encoding Rules)，由 X.690 定义。
- **Certificate** — 将主体实体的可分辨名称绑定到公钥的类型，由数字签名保证。定义在 X.509 中。
- **DER** — ASN.1 的可分辨编码规则 (Distinguished Encoding Rules)，由 X.690 定义。DER 是 BER 的子集。
- **Name** — 唯一标识或"区分" X.500 目录中对象的类型。定义在 X.501 中。

### 2.2. 记法

本文档不使用特殊记法。

## 3. 概述

证书签名请求由三部分组成："证书签名请求信息"、签名算法标识符和对证书签名请求信息的数字签名。证书签名请求信息由实体的可分辨名称、实体的公钥和一组提供该实体其他信息的属性组成。

构建证书签名请求的过程涉及以下步骤：

1. 请求认证的实体构造一个 CertificationRequestInfo 值，包含主体可分辨名称、主体公钥和可选的一组属性。
2. 使用主体实体的私钥对 CertificationRequestInfo 值签名（参见第 4.2 节）。
3. 将 CertificationRequestInfo 值、签名算法标识符和实体签名收集到 CertificationRequest 值中。

CA 通过认证请求实体并验证其签名来处理请求。如果请求有效，CA 从可分辨名称和公钥、颁发者名称以及 CA 选择的序列号、有效期和签名算法构造 X.509 证书。

> [!tip] CA 返回证书的形式
> CA 以何种形式返回新证书不在本文档范围内。一种可能是以 signedData 内容类型的 PKCS #7 密码消息返回。返回消息可以包含从新证书到 CA 的认证路径，也可能包含 CA 认为有帮助的其他证书和 CRL。另一种可能是 CA 将新证书插入中央数据库。

> [!note] 注意事项
> - 实体通常在生成公钥/私钥对后发送证书签名请求，但也可以在实体的可分辨名称变更后发送。
> - 证书签名请求上的签名防止实体请求包含其他方公钥的证书。
> - 本文档与 PEM (RFC 1424) 的证书签名请求语法不兼容，主要区别在于：允许一组属性、不包含颁发者名称/序列号/有效期、不要求签名"无害"消息。

## 4. 证书签名请求语法

### 4.1. CertificationRequestInfo

证书签名请求信息的 ASN.1 类型为 CertificationRequestInfo：

```asn1
CertificationRequestInfo ::= SEQUENCE {
     version       INTEGER { v1(0) } (v1,...),
     subject       Name,
     subjectPKInfo SubjectPublicKeyInfo{{ PKInfoAlgorithms }},
     attributes    [0] Attributes{{ CRIAttributes }}
}

SubjectPublicKeyInfo { ALGORITHM : IOSet} ::= SEQUENCE {
     algorithm        AlgorithmIdentifier {{IOSet}},
     subjectPublicKey BIT STRING
}

PKInfoAlgorithms ALGORITHM ::= {
     ...  -- 在此添加任何本地定义的算法 --
     }

Attributes { ATTRIBUTE:IOSet } ::= SET OF Attribute{{ IOSet }}

CRIAttributes  ATTRIBUTE  ::= {
     ... -- 在此添加任何本地定义的属性 --
     }

Attribute { ATTRIBUTE:IOSet } ::= SEQUENCE {
     type   ATTRIBUTE.&id({IOSet}),
     values SET SIZE(1..MAX) OF ATTRIBUTE.&Type({IOSet}{@type})
}
```

CertificationRequestInfo 各字段的含义：

- **version** — 版本号，用于与本文档的未来修订兼容。此版本应为 0。
- **subject** — 证书主体（公钥待认证的实体）的可分辨名称。
- **subjectPublicKeyInfo** — 包含待认证公钥的信息。信息标识实体的公钥算法（及关联参数）；公钥算法示例包括 PKCS #1 的 rsaEncryption 对象标识符。信息还包括实体公钥的比特串表示。对于上述公钥算法，比特串包含 PKCS #1 类型 RSAPublicKey 的 DER 编码。
- **attributes** — 提供证书主体附加信息的属性集合。PKCS #9 中定义了一些可能有用的属性类型，如 challenge-password 属性（指定实体用于请求证书吊销的密码）和 extensionRequest 属性。

### 4.2. CertificationRequest

证书签名请求的 ASN.1 类型为 CertificationRequest：

```asn1
CertificationRequest ::= SEQUENCE {
     certificationRequestInfo CertificationRequestInfo,
     signatureAlgorithm AlgorithmIdentifier{{ SignatureAlgorithms }},
     signature          BIT STRING
}

AlgorithmIdentifier {ALGORITHM:IOSet } ::= SEQUENCE {
     algorithm          ALGORITHM.&id({IOSet}),
     parameters         ALGORITHM.&Type({IOSet}{@algorithm}) OPTIONAL
}

SignatureAlgorithms ALGORITHM ::= {
     ... -- 在此添加任何本地定义的算法 --
     }
```

CertificationRequest 各字段的含义：

- **certificationRequestInfo** — 证书签名请求信息，即被签名的值。
- **signatureAlgorithm** — 标识签名算法（及关联参数）。例如，规范可以在 SignatureAlgorithms 信息对象集中包含 PKCS #1 的 md5WithRSAEncryption 的 ALGORITHM 对象。
- **signature** — 使用证书签名请求主体的私钥对证书签名请求信息签名的结果。

签名过程包含两个步骤：

1. 将 certificationRequestInfo 组件的值进行 DER 编码，得到字节字符串。
2. 在指定签名算法下用证书签名请求主体的私钥对步骤 1 的结果签名，得到比特串（即签名）。

> [!tip] 等效语法
> CertificationRequest 的等效语法可以写为 `SIGNED{ EncodedCertificationRequestInfo }`，其中 SIGNED 是一个通用签名包装类型。

## 5. 安全考虑

安全问题贯穿本备忘录全文讨论。

## 6. 作者地址

- **Magnus Nystrom** — RSA Security, Box 10704, S-121 29 Stockholm, Sweden. Email: magnus@rsasecurity.com
- **Burt Kaliski** — RSA Security, 20 Crosby Drive, Bedford, MA 01730 USA. Email: bkaliski@rsasecurity.com

## 附录 A. ASN.1 模块

本附录以 ASN.1 模块 PKCS-10 的形式包含本文档中的所有 ASN.1 类型和值定义。

```asn1
PKCS-10 {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
pkcs-10(10) modules(1) pkcs-10(1)}

DEFINITIONS IMPLICIT TAGS ::=

BEGIN

-- EXPORTS All --
-- 此模块中定义的所有类型和值均导出供其他 ASN.1 模块使用。

IMPORTS

informationFramework, authenticationFramework
     FROM UsefulDefinitions {joint-iso-itu-t(2) ds(5) module(1)
     usefulDefinitions(0) 3}

ATTRIBUTE, Name
     FROM InformationFramework informationFramework

ALGORITHM
     FROM AuthenticationFramework authenticationFramework;

-- 证书签名请求
CertificationRequestInfo ::= SEQUENCE {
     version       INTEGER { v1(0) } (v1,...),
     subject       Name,
     subjectPKInfo SubjectPublicKeyInfo{{ PKInfoAlgorithms }},
     attributes    [0] Attributes{{ CRIAttributes }}
}

SubjectPublicKeyInfo {ALGORITHM: IOSet} ::= SEQUENCE {
     algorithm        AlgorithmIdentifier {{IOSet}},
     subjectPublicKey BIT STRING
}

PKInfoAlgorithms ALGORITHM ::= {
     ...  -- 在此添加任何本地定义的算法 --
     }

Attributes { ATTRIBUTE:IOSet } ::= SET OF Attribute{{ IOSet }}

CRIAttributes  ATTRIBUTE  ::= {
     ... -- 在此添加任何本地定义的属性 --
     }

Attribute { ATTRIBUTE:IOSet } ::= SEQUENCE {
     type   ATTRIBUTE.&id({IOSet}),
     values SET SIZE(1..MAX) OF ATTRIBUTE.&Type({IOSet}{@type})
}

CertificationRequest ::= SEQUENCE {
     certificationRequestInfo CertificationRequestInfo,
     signatureAlgorithm AlgorithmIdentifier{{ SignatureAlgorithms }},
     signature          BIT STRING
}

AlgorithmIdentifier {ALGORITHM:IOSet } ::= SEQUENCE {
     algorithm  ALGORITHM.&id({IOSet}),
     parameters ALGORITHM.&Type({IOSet}{@algorithm}) OPTIONAL
}

SignatureAlgorithms ALGORITHM ::= {
     ... -- 在此添加任何本地定义的算法 --
     }

END
```

## 附录 B. 知识产权考虑

RSA Security 对本文档描述的一般构造不提出专利要求，但特定的底层技术可能受专利保护。

## 附录 C. 修订历史

**Version 1.0** — 之前的版本（也以 [6] 中的 "version 1.5" 发布）。

**Version 1.7** — 此版本包含若干编辑性修改，包括参考文献更新和 ASN.1 类型定义的修改。实质性变更如下：

- 引用 X.680-X.690（ASN.1 及其编码规则的当前国际标准），移除所有对 X.208 和 X.209 的引用。
- X.690 标准要求 DER 下 SET OF 组件的编码值按升序排列。但应用不应依赖属性组件的排序。
- 移除所有对 PKCS #6 扩展证书语法标准的引用。随着 X.509 v3 证书扩展的添加，RSA Laboratories 撤回了对 PKCS #6 的支持。

## 附录 D. 参考文献

- \[1] RSA Laboratories. PKCS #1: RSA Encryption Standard. Version 2.0, October 1998.
- \[2] RSA Laboratories. PKCS #7: Cryptographic Message Syntax Standard. Version 1.5, November 1993.
- \[3] RSA Laboratories. PKCS #9: Selected Attribute Types. Version 2.0, February 2000.
- \[4] Adams, C. and S. Farrell, "Internet X.509 PKI - Certificate Management Protocols", RFC 2510, March 1999.
- \[5] Kaliski, B., "PEM: Part IV: Key Certification and Related Services", RFC 1424, February 1993.
- \[6] Kaliski, B., "PKCS #10: Certification Request Syntax Version 1.5", RFC 2314, March 1998.
- \[7] ITU-T X.500 (1997) — The Directory: Overview of concepts, models and services.
- \[8] ITU-T X.501 (1993) — The Directory: Models.
- \[9] ITU-T X.509 (1997) — The Directory: Authentication framework.
- \[10] ITU-T X.680 (1997) — ASN.1: Specification of Basic Notation.
- \[11] ITU-T X.681 (1997) — ASN.1: Information Object Specification.
- \[12] ITU-T X.682 (1997) — ASN.1: Constraint Specification.
- \[13] ITU-T X.683 (1997) — ASN.1: Parameterization of ASN.1 Specifications.
- \[14] ITU-T X.690 (1997) — ASN.1 Encoding Rules: BER, CER and DER.

## 附录 E. 联系信息与关于 PKCS

公钥密码学标准 (PKCS) 是 RSA Laboratories 与全球安全系统开发者合作制定的规范，旨在加速公钥密码学的部署。PKCS 文档于 1991 年首次发布，已成为广泛引用和实现的标准。PKCS 系列的贡献已成为许多正式和事实标准的一部分，包括 ANSI X9 文档、PKIX、SET、S/MIME 和 SSL。
