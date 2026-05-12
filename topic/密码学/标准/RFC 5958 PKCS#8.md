---
title: PKCS#8 非对称密钥包
description: RFC 5958 - 非对称密钥包语法规范，定义私钥信息和加密私钥信息的 ASN.1 结构
tags:
  - 密码学
  - PKCS8
  - 私钥
  - ASN.1
  - RFC
---

# PKCS#8：非对称密钥包 (Asymmetric Key Packages)

> [!info] RFC 信息
> - **RFC 编号**：5958
> - **类别**：Standards Track
> - **发布日期**：2010 年 8 月
> - **作者**：S. Turner (IECA)
> - **替代**：RFC 5208

> [!abstract] 摘要
> 本文档定义了私钥信息的语法及其内容类型。私钥信息包括指定公钥算法的私钥和一组属性。[[密码消息语法 (CMS)]]（RFC 5652 定义）可用于对非对称密钥格式内容类型进行[[数字签名]]、摘要、认证或加密。本文档替代 RFC 5208。

## 1. 引言

本文档定义了私钥信息的语法及其[[密码消息语法 (CMS)]] [RFC5652] 内容类型。私钥信息包括指定公钥算法的私钥和一组属性。CMS 可用于对非对称密钥格式内容类型进行[[数字签名]]、摘要、认证或加密。本文档替代 PKCS #8 v1.2 [RFC5208]。

### 1.1. 需求术语

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按 [RFC2119] 中的描述解释。

### 1.2. ASN.1 语法记法

密钥包使用 [[ASN.1]] [X.680]、[X.681]、[X.682] 和 [X.683] 定义。

### 1.3. 相对 RFC 5208 的更新摘要

以下总结了相对 [RFC5208] 的更新：

- 将 "PrivateKeyInfo" 重命名为 "OneAsymmetricKey"。这反映了 publicKey 字段的添加，以允许非对称密钥的两部分分别传递。并非所有算法都会同时使用两个字段；但为完整性添加了 publicKey 字段。
- 定义了非对称密钥包 CMS 内容类型。
- 移除了 attributes 中的冗余 IMPLICIT。
- 向 OneAsymmetricKey 添加了 publicKey 并更新了版本号。
- 添加了 PKCS #9 属性可能被支持。
- 添加了与其他私钥格式兼容性的讨论。
- 添加了编码规则集的要求。
- 将导入从 PKCS #5 更改为 [RFC5912] 和 [RFC5911]。
- 将 ALGORITHM-IDENTIFIER 替换为 [RFC5912] 的 ALGORITHM。
- 注册了 application/pkcs8 媒体类型和 .p8 文件扩展名。

## 2. 非对称密钥包 CMS 内容类型

非对称密钥包 CMS 内容类型用于在双方之间传输一个或多个明文非对称密钥。非对称密钥包可以封装在一个或多个 CMS 保护内容类型中（参见第 4 节）。此规范的早期版本 [RFC5208] 未指定特定的编码规则集，但生成方应使用 DER [X.690]，接收方必须支持 BER [X.690]（其中也包含 DER [X.690]）。

非对称密钥包内容类型的语法如下：

```asn1
ct-asymmetric-key-package CONTENT-TYPE ::=
  { AsymmetricKeyPackage IDENTIFIED BY id-ct-KP-aKeyPackage }

id-ct-KP-aKeyPackage OBJECT IDENTIFIER ::=
  { joint-iso-itu-t(2) country(16) us(840) organization(1)
    gov(101) dod(2) infosec(1) formats(2)
    key-package-content-types(78) 5
  }

AsymmetricKeyPackage ::= SEQUENCE SIZE (1..MAX) OF OneAsymmetricKey

OneAsymmetricKey ::= SEQUENCE {
  version                   Version,
  privateKeyAlgorithm       PrivateKeyAlgorithmIdentifier,
  privateKey                PrivateKey,
  attributes            [0] Attributes OPTIONAL,
  ...,
  [[2: publicKey        [1] PublicKey OPTIONAL ]],
  ...
}

PrivateKeyInfo ::= OneAsymmetricKey

Version ::= INTEGER { v1(0), v2(1) } (v1, ..., v2)

PrivateKeyAlgorithmIdentifier ::= AlgorithmIdentifier
                                   { PUBLIC-KEY,
                                     { PrivateKeyAlgorithms } }

PrivateKey ::= OCTET STRING
                   -- 内容因密钥类型而异。
                   -- 算法标识符决定了密钥的格式。

PublicKey ::= BIT STRING
                   -- 内容因密钥类型而异。
                   -- 算法标识符决定了密钥的格式。

Attributes ::= SET OF Attribute { { OneAsymmetricKeyAttributes } }
```

AsymmetricKeyPackage 包含一个或多个 OneAsymmetricKey 元素。

OneAsymmetricKey 的语法容纳版本号、与私钥配合使用的非对称算法标识、私钥、可选的密钥材料属性（如 [X.520] 的 userCertificate）以及可选的公钥。通常，公钥或证书会存在其中之一。公钥和证书同时出现的情况很少见，因为这会包含两份公钥副本。

OneAsymmetricKey 重命名了 [RFC5208] 中定义的 PrivateKeyInfo 语法。新名称更好地反映了同时携带私钥和公钥组件的能力。通过版本号保持与原始 PrivateKeyInfo 的向后兼容性。OneAsymmetricKey 的字段用法如下：

- **version**：标识 OneAsymmetricKey 的版本。如果 publicKey 存在，则 version 设为 v2，否则设为 v1。
- **privateKeyAlgorithm**：标识私钥算法并可选地包含与非对称密钥对关联的参数。算法由对象标识符 (OID) 标识，参数格式取决于 OID，但 PrivateKeyAlgorithms 信息对象集限制了允许的 OID。
- **privateKey**：包含私钥值的 OCTET STRING。内容的解释在私钥算法的注册中定义。例如，DSA 密钥是 INTEGER，RSA 密钥表示为 [RFC3447] 定义的 RSAPrivateKey，ECC 密钥表示为 [RFC5915] 定义的 ECPrivateKey。
- **attributes**（可选）：包含与公钥对应的信息（如证书）。attributes 字段使用 ATTRIBUTE 类，受 OneAsymmetricKeyAttributes 信息对象集限制。[RFC2985] 中的属性可以被支持。
- **publicKey**（可选）：存在时，包含以 BIT STRING 编码的公钥。BIT STRING 内的结构（如果有）取决于 privateKeyAlgorithm。

## 3. 加密私钥信息

本节给出加密私钥信息的语法，被 [P12] 使用。

加密私钥信息的 [[ASN.1]] 类型为 EncryptedPrivateKeyInfo：

```asn1
EncryptedPrivateKeyInfo ::= SEQUENCE {
  encryptionAlgorithm  EncryptionAlgorithmIdentifier,
  encryptedData        EncryptedData }

EncryptionAlgorithmIdentifier ::= AlgorithmIdentifier
                                   { CONTENT-ENCRYPTION,
                                     { KeyEncryptionAlgorithms } }

EncryptedData ::= OCTET STRING
```

EncryptedPrivateKeyInfo 的字段用法如下：

- **encryptionAlgorithm**：标识私钥信息的加密算法。
- **encryptedData**：加密私钥信息（即 PrivateKeyInfo）的结果。

加密过程包含以下两个步骤：

1. 将私钥信息编码为字节字符串。生成方应使用 DER [X.690]，接收方必须支持 BER [X.690]。
2. 用密钥加密步骤 1 的结果，得到加密后的字节字符串。

## 4. 保护 AsymmetricKeyPackage

CMS 保护内容类型 [RFC5652] 和 [RFC5083] 可用于为 AsymmetricKeyPackage 提供安全保护：

- **SignedData**：对 AsymmetricKeyPackage 应用[[数字签名]]。
- **EncryptedData**：使用[[对称加密]]加密 AsymmetricKeyPackage（发送方和接收方已共享加密密钥）。
- **EnvelopedData**：使用[[对称加密]]加密 AsymmetricKeyPackage（发送方和接收方不共享加密密钥）。
- **AuthenticatedData**：使用消息认证码保护 AsymmetricKeyPackage，[[密钥管理]]方式与 EnvelopedData 类似。
- **AuthEnvelopedData**：使用支持认证加密的算法保护 AsymmetricKeyPackage，[[密钥管理]]方式与 EnvelopedData 类似。

## 5. 其他私钥格式考虑

本文档定义了交换非对称私钥的内容类型的语法和语义。还有两种用于传输非对称私钥的格式：

- **PFX (Personal Information Exchange)** [P12]，通常称为 PKCS #12 或 P12，是个人身份信息（包括私钥、证书、其他秘密和扩展）的传输语法。OneAsymmetricKey、PrivateKeyInfo 和 EncryptedPrivateKeyInfo 可以在 P12 消息中携带。私钥信息 OneAsymmetricKey 和 PrivateKeyInfo 在 P12 的 keyBag BAG-TYPE 中携带。EncryptedPrivateKeyInfo 在 P12 的 pkcs8ShroudedKeyBag BAG-TYPE 中携带。当前实现中，文件扩展名 .pfx 和 .p12 可以互换使用。
- **Microsoft 私钥专有传输语法**：使用 .pvk 文件扩展名进行本地存储。

> [!note] 格式转换
> .pvk 和 .p12/.pfx 格式不可互换；但存在转换工具可以在格式之间转换。

要从 AsymmetricKeyPackage 中提取私钥信息，需要移除封装层。至少需要移除外层 ContentInfo [RFC5652]。如果 AsymmetricKeyPackage 封装在 SignedData [RFC5652] 中，还需要移除 SignedData 和 EncapsulatedContentInfo 层。对 EnvelopedData、EncryptedData、AuthenticatedData 和 AuthEnvelopedData 也是如此。移除所有外层后，每个 OneAsymmetricKey 结构对应一组私钥信息。OneAsymmetricKey 和 PrivateKeyInfo 是同一结构，因此可以保存为 .p8 文件或复制到 P12 KeyBag BAG-TYPE 中。

> [!warning] 安全提醒
> 移除封装安全层将使签名失效，并可能将密钥暴露给未经授权的方。

.p8 文件有时使用 PEM 编码。PEM 编码时使用 .pem 文件扩展名。PEM 编码为 DER 编码的 EncryptedPrivateKeyInfo 或 PrivateKeyInfo 的 Base64 编码 [RFC4648]，分别包含在以下标记之间：

```
-----BEGIN ENCRYPTED PRIVATE KEY-----
-----END ENCRYPTED PRIVATE KEY-----
```

或

```
-----BEGIN PRIVATE KEY-----
-----END PRIVATE KEY-----
```

## 6. 安全考虑

私钥信息的保护对公钥密码学至关重要。私钥材料泄露给其他实体可能导致冒充。加密过程中使用的加密算法必须与所保护密钥的强度相当。

非对称密钥包内容本身未受保护。此内容类型可以与安全协议结合以保护包的内容。

## 7. IANA 考虑

本文档使用对象标识符来标识 CMS 内容类型和附录 A 中的 [[ASN.1]] 模块。CMS 内容类型 OID 注册在 DoD arc 中。[[ASN.1]] 模块 OID 注册在 RSADSI 委派给 SMIME 工作组的 arc 中。IANA 无需对此文档或任何预期更新采取进一步行动。

### 7.1. 媒体子类型 application/pkcs8 注册

| 字段 | 值 |
|------|-----|
| Type name | application |
| Subtype name | pkcs8 |
| Required parameters | 无 |
| Optional parameters | 无 |
| Encoding considerations | binary |
| Security considerations | 携带密码学私钥，参见第 6 节 |
| Interoperability considerations | 此媒体类型中的 PKCS #8 对象必须为 DER 编码的 PrivateKeyInfo |
| Published specification | RFC 5958 |
| File extension(s) | .p8 |
| Intended usage | COMMON |

## 8. 参考文献

### 8.1. 规范性引用

- \[RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- \[RFC4648] Josefsson, S., "The Base16, Base32, and Base64 Data Encodings", RFC 4648, October 2006.
- \[RFC5652] Housley, R., "Cryptographic Message Syntax [[(CMS)]]", STD 70, RFC 5652, September 2009.
- \[RFC5911] Hoffman, P. and J. Schaad, "New [[ASN.1]] Modules for CMS and [[S/MIME]]", RFC 5911, June 2010.
- \[RFC5912] Hoffman, P. and J. Schaad, "New [[ASN.1]] Modules for PKIX", RFC 5912, June 2010.
- \[X.680] ITU-T X.680 (2002) — [[ASN.1]]: Specification of Basic Notation.
- \[X.681] ITU-T X.681 (2002) — [[ASN.1]]: Information Object Specification.
- \[X.682] ITU-T X.682 (2002) — [[ASN.1]]: Constraint Specification.
- \[X.683] ITU-T X.683 (2002) — [[ASN.1]]: Parameterization of [[ASN.1]] Specifications.
- \[X.690] ITU-T X.690 (2002) — [[ASN.1]] Encoding Rules: BER, CER and DER.

### 8.2. 资料性引用

- \[P12] RSA Laboratories, "PKCS #12 v1.0: Personal Information Exchange Syntax", June 1999.
- \[RFC2985] Nystrom, M. and B. Kaliski, "PKCS #9: Selected Object Classes and Attribute Types Version 2.0", RFC 2985, November 2000.
- \[RFC3447] Jonsson, J. and B. Kaliski, "PKCS #1: RSA Cryptography Specifications Version 2.1", RFC 3447, February 2003.
- \[RFC5083] Housley, R., "CMS Authenticated-Enveloped-Data Content Type", RFC 5083, November 2007.
- \[RFC5208] Kaliski, B., "PKCS #8: Private-Key Information Syntax Specification Version 1.2", RFC 5208, May 2008.
- \[X.520] ITU-T X.520 (2005) — The Directory: Selected attribute types.
- \[RFC5915] Turner, S. and D. Brown, "Elliptic Curve Private Key Structure", RFC 5915, June 2010.

## 附录 A. ASN.1 模块

本附录提供了本规范中描述的结构的规范性 [[ASN.1]] 定义。

```asn1
AsymmetricKeyPackageModuleV1
  { iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-9(9)
    smime(16) modules(0) id-mod-asymmetricKeyPkgV1(50) }

DEFINITIONS IMPLICIT TAGS ::=

BEGIN

-- EXPORTS ALL

IMPORTS

-- FROM New SMIME ASN.1 [RFC5911]
Attribute{}, CONTENT-TYPE
 FROM CryptographicMessageSyntax-2009
   { iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-9(9)
     smime(16) modules(0) id-mod-cms-2004-02(41) }

-- From New PKIX ASN.1 [RFC5912]
ATTRIBUTE
 FROM PKIX-CommonTypes-2009
   { iso(1) identified-organization(3) dod(6) internet(1)
     security(5) mechanisms(5) pkix(7) id-mod(0)
     id-mod-pkixCommon-02(57) }

-- From New PKIX ASN.1 [RFC5912]
AlgorithmIdentifier{}, ALGORITHM, PUBLIC-KEY, CONTENT-ENCRYPTION
  FROM AlgorithmInformation-2009
    { iso(1) identified-organization(3) dod(6) internet(1)
      security(5) mechanisms(5) pkix(7) id-mod(0)
      id-mod-algorithmInformation-02(58) }

;

ContentSet CONTENT-TYPE ::= {
 ct-asymmetric-key-package,
 ... -- 预期更多内容类型 --
}

ct-asymmetric-key-package CONTENT-TYPE ::=
 { AsymmetricKeyPackage IDENTIFIED BY id-ct-KP-aKeyPackage }

id-ct-KP-aKeyPackage OBJECT IDENTIFIER ::=
  { joint-iso-itu-t(2) country(16) us(840) organization(1)
      gov(101) dod(2) infosec(1) formats(2)
      key-package-content-types(78) 5
  }

AsymmetricKeyPackage ::= SEQUENCE SIZE (1..MAX) OF OneAsymmetricKey

OneAsymmetricKey ::= SEQUENCE {
  version                   Version,
  privateKeyAlgorithm       PrivateKeyAlgorithmIdentifier,
  privateKey                PrivateKey,
  attributes            [0] Attributes OPTIONAL,
  ...,
  [[2: publicKey        [1] PublicKey OPTIONAL ]],
  ...
}

PrivateKeyInfo ::= OneAsymmetricKey

-- PrivateKeyInfo 被 [P12] 使用。如果使用了标记为 version 2 的项，
-- 版本必须为 v2，否则应为 v1。当为 v1 时，PrivateKeyInfo 与
-- [RFC5208] 中的相同。

Version ::= INTEGER { v1(0), v2(1) } (v1, ..., v2)

PrivateKeyAlgorithmIdentifier ::= AlgorithmIdentifier
                                     { PUBLIC-KEY,
                                       { PrivateKeyAlgorithms } }

PrivateKey ::= OCTET STRING
                   -- 内容因密钥类型而异。
                   -- 算法标识符决定了密钥的格式。

PublicKey ::= BIT STRING
                   -- 内容因密钥类型而异。
                   -- 算法标识符决定了密钥的格式。

Attributes ::= SET OF Attribute { { OneAsymmetricKeyAttributes } }

OneAsymmetricKeyAttributes ATTRIBUTE ::= {
  ... -- 用于本地配置文件
}

EncryptedPrivateKeyInfo ::= SEQUENCE {
  encryptionAlgorithm  EncryptionAlgorithmIdentifier,
  encryptedData        EncryptedData }

EncryptionAlgorithmIdentifier ::= AlgorithmIdentifier
                                     { CONTENT-ENCRYPTION,
                                       { KeyEncryptionAlgorithms } }

EncryptedData ::= OCTET STRING -- 加密的 PrivateKeyInfo

PrivateKeyAlgorithms ALGORITHM ::= {
  ... -- 可扩展
}

KeyEncryptionAlgorithms ALGORITHM ::= {
  ... -- 可扩展
}

END
```

## 致谢

非常感谢 RSA 的 Burt Kaliski 和 Jim Randall。没有之前版本的文档，就不会有本文档。

还要感谢 Pasi Eronen、Roni Even、Alfred Hoenes、Russ Housley、Jim Schaad 和 Carl Wallace。

## 作者地址

**Sean Turner** — IECA, Inc., 3057 Nutley Street, Suite 106, Fairfax, VA 22031, USA. Email: turners@ieca.com
