---
title: RFC 5751 S/MIME 3.2 消息规范
description: 定义 S/MIME 3.2 版本的消息规范，涵盖数字签名、加密和压缩的 MIME 数据处理方式
tags:
  - 密码学
  - S/MIME
  - 邮件加密
  - CMS
  - RFC
---

> [!info] RFC 信息
> **RFC 编号**：5751
> **标题**：Secure/Multipurpose Internet Mail Extensions (S/MIME) Version 3.2 Message Specification
> **类别**：Standards Track
> **日期**：2010 年 1 月
> **作者**：B. Ramsdell (Brute Squad Labs), S. Turner (IECA)
> **替代**：RFC 3851
> **链接**：http://www.rfc-editor.org/info/rfc5751

## 摘要

本文档定义了 Secure/Multipurpose Internet Mail Extensions (S/MIME) 版本 3.2。S/MIME 提供了一种一致的方式来发送和接收安全的 MIME 数据。数字签名提供了身份认证、消息完整性以及不可抵赖性（non-repudiation）与来源证明。加密提供了数据机密性（data confidentiality）。压缩可用于减少数据大小。本文档替代了 RFC 3851。

## 1. 引言

S/MIME (Secure/Multipurpose Internet Mail Extensions) 提供了一种一致的方式来发送和接收安全的 MIME 数据。基于广泛使用的 Internet MIME 标准，S/MIME 为电子消息应用提供以下密码安全服务：身份认证（authentication）、消息完整性（message integrity）和来源不可抵赖性（non-repudiation of origin）（通过数字签名），以及数据机密性（data confidentiality）（通过加密）。作为补充服务，S/MIME 还提供消息压缩功能。

S/MIME 可被传统邮件用户代理（MUA, Mail User Agent）用于为发送的邮件添加密码安全服务，并解释接收邮件中的密码安全服务。然而，S/MIME 不限于邮件；它可以与任何传输 MIME 数据的传输机制一起使用，例如 HTTP 或 SIP。因此，S/MIME 利用 MIME 基于对象的特性，允许在混合传输系统中交换安全消息。

此外，S/MIME 可用于使用密码安全服务的自动化消息传输代理，这些服务不需要任何人工干预，例如对软件生成的文档进行签名，以及对通过 Internet 发送的 FAX 消息进行加密。

### 1.1 规范概述

本文档描述了一种为 MIME 数据添加密码签名和加密服务的协议。MIME 标准 [MIME-SPEC] 提供了 Internet 消息内容的通用结构，并允许基于新内容类型的应用进行扩展。

本规范定义了如何创建一个按照 Cryptographic Message Syntax (CMS) RFC 5652 [CMS]（源自 PKCS #7 [PKCS-7]）进行密码增强的 MIME body part。本规范还定义了可用于传输这些 body part 的 `application/pkcs7-mime` 媒体类型。

本文档还讨论了如何使用 [MIME-SECURE] 中定义的 `multipart/signed` 媒体类型来传输 S/MIME 签名消息。`multipart/signed` 与 `application/pkcs7-signature` 媒体类型结合使用，后者用于传输分离式 S/MIME 签名（detached signature）。

为了创建 S/MIME 消息，S/MIME 代理必须遵循本文档中的规范，以及 Cryptographic Message Syntax 文档 [CMS]、[CMSALG]、[RSAPSS]、[RSAOAEP] 和 [CMS-SHA2] 中列出的规范。

> [!note] 设计原则
> 在本规范中，对接收代理如何处理传入消息提出了要求和建议，对发送代理如何创建传出消息也有单独的要求和建议。总体策略是"**在接收时宽松，在发送时保守**"。大多数要求针对传入消息的处理，而建议主要针对传出消息的创建。

接收代理和发送代理的要求分离还源于可能存在涉及传统 Internet 邮件客户端以外软件的 S/MIME 系统。S/MIME 可与任何传输 MIME 数据的系统一起使用。例如，发送加密消息的自动化流程可能完全无法接收加密消息。因此，两种类型代理的要求和建议在适当时分别列出。

### 1.2 定义

为本规范之目的，适用以下定义：

**ASN.1**：Abstract Syntax Notation One，如 ITU-T 建议 X.680 [X.680] 所定义。

**BER**：ASN.1 的基本编码规则（Basic Encoding Rules），如 ITU-T 建议 X.690 [X.690] 所定义。

**Certificate（证书）**：一种通过数字签名将实体名称与公钥绑定的类型。

**DER**：ASN.1 的可分辨编码规则（Distinguished Encoding Rules），如 ITU-T 建议 X.690 [X.690] 所定义。

**7 位数据（7-bit data）**：行长小于 998 个字符的文本数据，其中没有任何字符的第 8 位被置位，且没有 NULL 字符。`<CR>` 和 `<LF>` 仅作为 `<CR><LF>` 行尾分隔符的一部分出现。

**8 位数据（8-bit data）**：行长小于 998 个字符的文本数据，且没有 NULL 字符。`<CR>` 和 `<LF>` 仅作为 `<CR><LF>` 行尾分隔符的一部分出现。

**二进制数据（Binary data）**：任意数据。

**传输编码（Transfer encoding）**：对数据进行的可逆转换，使 8 位或二进制数据可通过仅传输 7 位数据的通道发送。

**接收代理（Receiving agent）**：解释和处理 S/MIME CMS 对象、包含 CMS 内容类型的 MIME body part 或两者的软件。

**发送代理（Sending agent）**：创建 S/MIME CMS 内容类型、包含 CMS 内容类型的 MIME body part 或两者的软件。

**S/MIME 代理（S/MIME agent）**：作为接收代理、发送代理或两者的用户软件。

### 1.3 文档约定

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 按 [MUSTSHOULD] 中的描述解释。

此处定义了一些附加术语：

**SHOULD+**：含义与 SHOULD 相同。但作者预期标记为 SHOULD+ 的要求将在未来某个时候升级为 MUST。

**SHOULD-**：含义与 SHOULD 相同。但作者预期标记为 SHOULD- 的要求将在本文档的未来版本中降级为 MAY。

**MUST-**：含义与 MUST 相同。但作者预期此要求在未来的文档中将不再是 MUST。虽然其状态将在稍后确定，但合理预期如果文档的未来修订改变了 MUST- 要求的状态，它将至少保持为 SHOULD 或 SHOULD-。

### 1.4 与先前 S/MIME 实践的兼容性

S/MIME 3.2 版代理应尝试与先前版本的 S/MIME 代理实现最大可能的互操作性。S/MIME 版本 2 在 RFC 2311 至 RFC 2315（含）[SMIMEv2] 中描述，S/MIME 版本 3 在 RFC 2630 至 RFC 2634（含）及 RFC 5035 [SMIMEv3] 中描述，S/MIME 版本 3.1 在 RFC 3850、RFC 3851、RFC 3852、RFC 2634 和 RFC 5035 [SMIMEv3.1] 中描述。RFC 2311 还包含有关 S/MIME 发展的历史信息。

### 1.5 从 S/MIME v3 到 S/MIME v3.1 的变更

- RSA 公钥算法改为 MUST 实现的密钥包装算法，Diffie-Hellman (DH) 算法改为 SHOULD 实现。
- AES 对称加密算法作为 SHOULD 实现被纳入。
- RSA 公钥算法改为 MUST 实现的签名算法。
- 关于使用"空" SignedData 消息传输证书的模糊表述已澄清，以反映也允许传输证书撤销列表（CRL, Certificate Revocation List）。
- 现在明确讨论了对某些 MIME 实体使用二进制编码。
- 添加了通过使用 `message/rfc822` 媒体类型实现头部保护。
- 允许使用 CompressedData CMS 类型，以及必需的媒体类型和文件扩展名添加。

### 1.6 S/MIME v3.1 以来的变更

- 编辑性变更，例如将 "MIME type" 替换为 "media type"，content-type 替换为 Content-Type。
- 将 "Conventions Used in This Document" 移至第 1.3 节。添加了 SHOULD+、SHOULD- 和 MUST- 的定义。
- 第 1.1 节和附录 A：添加了对 RSASSA-PSS、RSAES-OAEP 和 SHA2 CMS 算法 RFC 的引用。添加了 CMS Multiple Signers Clarification 到 CMS 引用。
- 第 1.2 节：将 ASN.1 引用更新为 X.680，BER 和 DER 引用更新为 X.690。
- 第 1.4 节：添加了对 S/MIME MSG 3.1 RFC 的引用。
- 第 2.1 节（摘要算法）：SHA-256 添加为 MUST，SHA-1 和 MD5 改为 SHOULD-。
- 第 2.2 节（签名算法）：RSA with SHA-256 添加为 MUST，DSA with SHA-256 添加为 SHOULD+，RSA with SHA-1、DSA with SHA-1 和 RSA with MD5 改为 SHOULD-，RSASSA-PSS with SHA-256 添加为 SHOULD+。还添加了关于 S/MIME v3.1 客户端支持内容的注释。
- 第 2.3 节（密钥加密）：DH 改为 SHOULD-，RSAES-OAEP 添加为 SHOULD+。详细说明了密钥包装算法的要求。
- 第 2.5.1 节：添加了接收代理必须同时支持 GeneralizedTime 和 UTCTime 的要求。
- 第 2.5.2 节：将引用 "sha1WithRSAEncryption" 替换为 "sha256WithRSAEncryption"，"DES-3EDE-CBC" 替换为 "AES-128 CBC"，删除了 RC5 示例。
- 第 2.5.2.1 节：删除了整个小节（讨论已弃用的 RC2）。
- 第 2.7 节、2.7.1 节、附录 A：移除了 RC2/40 的引用。
- 第 2.7 节（内容加密）：AES-128 CBC 添加为 MUST，AES-192 和 AES-256 CBC 为 SHOULD+，tripleDES 现为 SHOULD-。
- 第 2.7.1 节：将指针从 2.7.2.1 至 2.7.2.4 更新为 2.7.1.1 至 2.7.1.2。
- 第 3.1.1 节：移除了关于 MIME 字符集的文本。
- 第 3.2.2 节和 3.6 节：将 "encrypted" 替换为 "enveloped"。更新 OID 示例为使用 AES-128 CBC OID。
- 第 3.4.3.2 节：将 SHA-1 的 micalg 参数替换为 sha-1。
- 第 4 节：更新了对 CERT v3.2 的引用。
- 第 4.1 节：更新了 RSA 和 DSA 密钥大小讨论。将最后四句移至安全考虑。更新了对安全随机性要求的引用。
- 第 5 节：添加了 IANA 注册模板，将媒体类型注册更新为指向本文档而非 RFC 2311。
- 第 6 节：更新了安全考虑。
- 第 7 节：将引用从附录 B 移至此节。更新了引用。添加了对 SMIMEv2、SMIMEv3 和 SMIMEv3.1 的信息性引用。
- 附录 B：添加了附录 B 以将 S/MIME v2 移至 Historic 状态。

## 2. CMS 选项

CMS 允许在内容、属性和算法支持方面有多种选项。本节提出了若干支持要求和建议，以实现所有 S/MIME 实现之间的基本互操作性。[CMSALG] 和 [CMS-SHA2] 提供了关于使用密码算法的额外详细信息。[ESS] 提供了关于使用附加属性的额外详细信息。

### 2.1 DigestAlgorithmIdentifier

发送和接收代理必须支持 SHA-256 [CMS-SHA2]，并且应该-支持 SHA-1 [CMSALG]。接收代理应该-支持 MD5 [CMSALG]，以便提供与使用 MD5 摘要的 S/MIME v2 SignedData 对象的向后兼容性。

### 2.2 SignatureAlgorithmIdentifier

**接收代理**：

- 必须支持 RSA with SHA-256
- 应该+支持 DSA with SHA-256
- 应该+支持 RSASSA-PSS with SHA-256
- 应该-支持 RSA with SHA-1
- 应该-支持 DSA with SHA-1
- 应该-支持 RSA with MD5

**发送代理**：

- 必须支持 RSA with SHA-256
- 应该+支持 DSA with SHA-256
- 应该+支持 RSASSA-PSS with SHA-256
- 应该-支持 RSA with SHA-1 或 DSA with SHA-1
- 应该-支持 RSA with MD5

关于密钥大小和算法引用的信息，参见第 4.1 节。

> [!note] 版本兼容性说明
> S/MIME v3.1 客户端支持验证 `id-dsa-with-sha1` 和 `rsaEncryption`，可能不实现 `sha256withRSAEncryption`。S/MIME v3 客户端可能仅实现使用 `id-dsa-with-sha1` 的签名或签名验证，也可能在此字段中使用 `id-dsa` 作为 AlgorithmIdentifier。接收客户端应该将 `id-dsa` 识别为等同于 `id-dsa-with-sha1`，发送客户端在使用该算法时必须使用 `id-dsa-with-sha1`。另外注意，S/MIME v2 客户端仅需验证使用 `rsaEncryption` 算法与 SHA-1 或 MD5 的数字签名，可能完全不实现 `id-dsa-with-sha1` 或 `id-dsa`。

### 2.3 KeyEncryptionAlgorithmIdentifier

**接收和发送代理**：

- 必须支持 RSA Encryption，如 [CMSALG] 所规定
- 应该+支持 RSAES-OAEP，如 [RSAOAEP] 所规定
- 应该-支持 DH 临时-静态模式（ephemeral-static mode），如 [CMSALG] 和 [SP800-57] 所规定

当使用 DH 临时-静态模式时，KeyEncryptionAlgorithmIdentifier [CMS] 中还需指定密钥包装算法。密钥包装和内容加密算法（[CMSALG] 和 [CMSAES]）的底层加密函数以及两种算法的密钥大小必须相同（例如，AES-128 密钥包装算法配合 AES-128 内容加密算法）。由于 AES-128 CBC 是必须实现的内容加密算法，当使用 DH 临时-静态模式时，也必须支持 AES-128 密钥包装算法。

> [!note] 版本兼容性说明
> S/MIME v3.1 客户端可能仅使用 `rsaEncryption` 算法实现密钥加密和解密。S/MIME v3 客户端可能仅使用 Diffie-Hellman 算法实现密钥加密和解密。S/MIME v2 客户端仅能使用 `rsaEncryption` 算法解密内容加密密钥。

### 2.4 通用语法

CMS 有多种内容类型。其中，只有 Data、SignedData、EnvelopedData 和 CompressedData 内容类型目前用于 S/MIME。

#### 2.4.1 Data 内容类型

发送代理必须使用 `id-data` 内容类型标识符来标识"内部" MIME 消息内容。例如，当对 MIME 数据应用数字签名时，CMS SignedData encapContentInfo eContentType 必须包含 `id-data` 对象标识符，并且媒体类型必须存储在 SignedData encapContentInfo eContent OCTET STRING 中（除非发送代理使用 `multipart/signed`，此时 eContent 不存在，见本文档第 3.4.3 节）。又如，当对 MIME 数据应用加密时，CMS EnvelopedData encryptedContentInfo contentType 必须包含 `id-data` 对象标识符，并且加密的 MIME 内容必须存储在 EnvelopedData encryptedContentInfo encryptedContent OCTET STRING 中。

#### 2.4.2 SignedData 内容类型

发送代理必须使用 SignedData 内容类型对消息应用数字签名，或者在退化的情况下（没有签名信息）用于传递证书。对消息应用签名可提供身份认证、消息完整性和来源不可抵赖性。

#### 2.4.3 EnvelopedData 内容类型

此内容类型用于对消息应用数据机密性保护。发送者需要拥有每个预期消息接收者的公钥才能使用此服务。

#### 2.4.4 CompressedData 内容类型

此内容类型用于对消息应用数据压缩。此内容类型不提供身份认证、消息完整性、不可抵赖性或数据机密性，仅用于减小消息大小。

关于此类型与其他 CMS 类型结合使用的更多指导，参见第 3.6 节。

### 2.5 属性与 SignerInfo 类型

SignerInfo 类型允许在签名中包含未签名属性和已签名属性。

接收代理必须能够处理此处列出的每个已签名属性的零个或一个实例。发送代理应该在每条 S/MIME 消息中生成以下每个已签名属性的一个实例：

- 签名时间（Signing Time）（本节第 2.5.1 节）
- SMIME 能力（SMIME Capabilities）（本节第 2.5.2 节）
- 加密密钥偏好（Encryption Key Preference）（本节第 2.5.3 节）
- 消息摘要（Message Digest）（[CMS] 第 11.2 节）
- 内容类型（Content Type）（[CMS] 第 11.1 节）

此外，接收代理应该能够处理 `signingCertificate` 和 `signingCertificatev2` 已签名属性的零个或一个实例，如 RFC 2634 [ESS] 第 5 节和 RFC 5035 [ESS] 第 3 节所定义。

发送代理应该在每条消息的每个 SignerInfo 结构中生成 `signingCertificate` 或 `signingCertificatev2` 已签名属性的一个实例。

将来可能会定义这些属性的附加属性和值。接收代理应该以优雅的方式处理其无法识别的属性或值。

包含此处未列出的已签名属性的交互式发送代理应该向用户显示这些属性，以便用户了解所有正在被签名的数据。

#### 2.5.1 签名时间属性

签名时间属性（signing-time attribute）用于传递消息被签名的时间。签名时间最可能由消息发起者创建，因此其可信度仅与发起者相同。

发送代理必须将 2049 年及之前的签名时间编码为 UTCTime；2050 年及之后的签名时间必须编码为 GeneralizedTime。当使用 UTCTime 选项时，S/MIME 代理必须按如下方式解释年份字段（YY）：

如果 YY 大于或等于 50，年份解释为 19YY；如果 YY 小于 50，年份解释为 20YY。

接收代理必须能够处理以 UTCTime 或 GeneralizedTime 编码的签名时间属性。

#### 2.5.2 SMIME 能力属性

SMIMECapabilities 属性包括签名算法（如 `sha256WithRSAEncryption`）、对称算法（如 `AES-128 CBC`）和密钥加密算法（如 `rsaEncryption`）。还有几个标识符表示对其他可选功能的支持，如二进制编码和压缩。SMIMECapabilities 的设计具有灵活性和可扩展性，以便将来能够以不会破坏现有客户端的方式添加识别其他能力和偏好（如证书）的方法。

如果存在，SMIMECapabilities 属性必须是 SignedAttribute；不得是 UnsignedAttribute。CMS 将 SignedAttributes 定义为 SET OF Attribute。signerInfo 中的 SignedAttributes 不得包含 SMIMECapabilities 属性的多个实例。CMS 定义 Attribute 的 ASN.1 语法包含 attrValues SET OF AttributeValue。SMIMECapabilities 属性必须仅包含 AttributeValue 的单个实例。attrValues SET OF AttributeValue 中不得存在零个或多个 AttributeValue 实例。

SMIMECapabilities 属性的语义指定了宣布 SMIMECapabilities 的客户端能够支持的功能的部分列表。客户端不必列出其支持的每一项能力，也不必列出所有能力以免能力列表过长。在 SMIMECapabilities 属性中，对象标识符（OID）按偏好顺序排列，但应该按其类别（签名算法、对称算法、密钥加密算法等）进行逻辑分组。

SMIMECapabilities 属性的结构旨在便于简单的表查找和二进制比较以确定匹配。例如，AES-128 CBC 的 SMIMECapability 的 DER 编码必须无论实现如何都完全相同编码。由于需要相同编码的要求，记录用于 SMIMECapabilities 属性的算法的作者应该明确记录常见情况的正确字节序列。

对于任何能力，与 OID 关联的参数必须指定区分同一算法两个实例所需的所有参数。

对应算法的 OID 应该使用与实际算法相同的 OID，除非从 OID 无法明确算法用途的情况。例如，在早期规范中，`rsaEncryption` 是模糊的，因为它可以指签名算法或密钥加密算法。如果 OID 存在歧义，需要由注册 SMIMECapabilities 列表的维护者裁决哪种算法类型将使用该 OID，并且必须在 `smimeCapabilities` OID 下分配新 OID 以满足该 OID 的其他用途。

注册的 SMIMECapabilities 列表指定了需要参数的 OID 的参数，最值得注意的是可变长度对称密码的密钥长度。如果特定 OID 没有区分参数，则必须省略参数，并且不得编码为 NULL。将来可能会为 SMIMECapabilities 属性定义附加值。接收代理必须以优雅的方式处理具有其无法识别的值的 SMIMECapabilities 对象。

第 2.7.1 节解释了缓存能力的策略。

#### 2.5.3 加密密钥偏好属性

加密密钥偏好属性（encryption key preference attribute）允许签名者明确描述签名者哪个证书包含签名者偏好的加密密钥。此属性旨在增强与使用独立加密密钥和签名密钥的客户端的互操作行为。此属性用于向查看该属性的任何人传达列出的证书中哪个适合用于加密会话密钥，以用于未来的加密消息。

如果存在，SMIMEEncryptionKeyPreference 属性必须是 SignedAttribute；不得是 UnsignedAttribute。CMS 将 SignedAttributes 定义为 SET OF Attribute。signerInfo 中的 SignedAttributes 不得包含 SMIMEEncryptionKeyPreference 属性的多个实例。CMS 定义 Attribute 的 ASN.1 语法包含 attrValues SET OF AttributeValue。SMIMEEncryptionKeyPreference 属性必须仅包含 AttributeValue 的单个实例。attrValues SET OF AttributeValue 中不得存在零个或多个 AttributeValue 实例。

如果使用此属性，发送代理应该在签名消息中包含的证书集合中包含所引用的证书。如果证书先前已提供给接收代理，则可以省略。如果常用或偏好的加密证书与用于签名消息的证书不同，发送代理应该使用此属性。

如果消息上的签名有效且签名时间大于当前存储的值，接收代理应该存储偏好数据。（与 SMIMECapabilities 一样，应该检查时钟偏移，如果偏移过大则不使用数据。）接收代理应该尽可能尊重发送者的加密密钥偏好属性。然而，这仅代表偏好，接收代理可以使用任何有效证书回复发送者。

第 2.7.1 节解释了缓存偏好数据的策略。

##### 2.5.3.1 接收者密钥管理证书的选择

为了确定在为特定接收者发送未来的 CMS EnvelopedData 消息时要使用的密钥管理证书，应该遵循以下步骤：

- 如果在从目标接收者接收的 SignedData 对象中找到 SMIMEEncryptionKeyPreference 属性，则它标识了应该用作该接收者 X.509 密钥管理证书的 X.509 证书。
- 如果在从目标接收者接收的 SignedData 对象中未找到 SMIMEEncryptionKeyPreference 属性，则应该在 X.509 证书集合中搜索与签名者具有相同主题名称且可用于密钥管理的 X.509 证书。
- 或者使用其他方法确定用户的密钥管理密钥。如果未找到 X.509 密钥管理证书，则无法对消息签名者进行加密。如果找到多个 X.509 密钥管理证书，S/MIME 代理可以在其中任意选择。

### 2.6 SignerIdentifier SignerInfo 类型

S/MIME v3.2 实现必须同时支持 `issuerAndSerialNumber` 和 `subjectKeyIdentifier`。使用 `subjectKeyIdentifier` 选项的消息无法被 S/MIME v2 客户端读取。

> [!warning] 注意
> 某些证书使用的 `subjectKeyIdentifier` 值不适合唯一标识证书。实现必须准备好可能不同实体的多个证书具有相同的 `subjectKeyIdentifier` 值，并且必须准备好在签名验证期间尝试每个匹配的证书，然后再指示错误条件。

### 2.7 ContentEncryptionAlgorithmIdentifier

**发送和接收代理**：

- 必须支持使用 AES-128 CBC [CMSAES] 进行加密和解密
- 应该+支持使用 AES-192 CBC 和 AES-256 CBC [CMSAES] 进行加密和解密
- 应该-支持使用 DES EDE3 CBC（下文简称 "tripleDES"）[CMSALG] 进行加密和解密

#### 2.7.1 决定使用哪种加密方法

当发送代理创建加密消息时，必须决定使用哪种类型的加密。决策过程涉及使用从接收者消息中包含的能力列表获取的信息，以及带外信息，如私人协议、用户偏好、法律限制等。

第 2.5.2 节定义了一种方法，发送代理可以通过该方法可选地宣布其解密能力及其偏好顺序。以下方法应用于处理和记住传入签名消息中的加密能力属性：

- 如果接收代理尚未为发送者的公钥创建能力列表，则在验证传入消息上的签名并检查时间戳后，接收代理应该创建一个新列表，至少包含签名时间和对称加密能力。
- 如果此类列表已存在，接收代理应该验证传入消息中的签名时间大于列表中存储的签名时间，且签名有效。如果是，接收代理应该更新列表中的签名时间和能力。远在未来（即大于任何合理时钟偏移的差异）的签名时间值，或签名无法验证的消息中的能力列表，不得被接受。

能力列表应该被存储以便将来在创建消息时使用。

在发送消息之前，发送代理必须决定是否愿意对消息中的特定数据使用弱加密。如果发送代理决定弱加密对此数据不可接受，则发送代理不得使用弱算法。使用或不使用弱加密的决定覆盖本节中关于使用哪种加密算法的任何其他决定。

第 2.7.1.1 节至第 2.7.1.2 节描述了发送代理在决定对消息应用哪种类型的加密时应该使用的决策。这些规则是有序的，因此发送代理应该按给定顺序做出决定。

##### 2.7.1.1 规则 1：已知能力

如果发送代理已从接收者处收到其即将加密的消息对应的一组能力，则发送代理应该通过选择列表中发送代理知道如何加密的第一个能力（即预期接收者最偏好的能力）来使用该信息。如果发送代理合理预期接收者能够解密消息，则发送代理应该使用列表中的某个能力。

##### 2.7.1.2 规则 2：未知能力，未知 S/MIME 版本

如果满足以下两个条件：

- 发送代理不了解接收者的加密能力，且
- 发送代理不了解接收者的 S/MIME 版本

则发送代理应该使用 AES-128，因为它是更强的算法且 S/MIME v3.2 所要求的。如果发送代理在此步骤中选择不使用 AES-128，则应该使用 tripleDES。

#### 2.7.2 选择弱加密

所有使用 40 位密钥的算法被许多人认为是弱加密。由人工控制的发送代理应该允许人工发送者在发送数据之前确定使用弱加密算法发送数据的风险，并可能允许人工发送者使用更强的加密方法，如 tripleDES 或 AES。

#### 2.7.3 多个接收者

如果发送代理正在为接收者组编写加密消息，其中某些接收者的加密能力不重叠，发送代理被迫发送多条消息。

> [!warning] 安全警告
> 如果发送代理选择发送一条用强算法加密的消息，然后发送同一消息用弱算法加密，监视通信信道的人可以通过解密弱加密消息来获取强加密消息的内容。

## 3. 创建 S/MIME 消息

本节描述 S/MIME 消息格式及其创建方式。S/MIME 消息是 MIME body 和 CMS 内容类型的组合。使用多种媒体类型以及多种 CMS 内容类型。要保护的数据始终是规范化的 MIME 实体。MIME 实体和其他数据（如证书和算法标识符）被传递给 CMS 处理设施，生成 CMS 对象。最后，CMS 对象被包装在 MIME 中。S/MIME 的增强安全服务 [ESS] 文档描述了嵌套安全 S/MIME 消息的格式。ESS 描述了如何使用 `multipart/signed` 和 `application/pkcs7-mime` 格式化三重包装的 S/MIME 消息的签名。

S/MIME 提供一种仅加密数据格式、多种仅签名数据格式以及多种签名加加密数据格式。需要多种格式以适应多种环境，特别是签名消息。选择这些格式的标准也有描述。

本节的读者应了解 [MIME-SPEC] 和 [MIME-SECURE] 中描述的 MIME。

### 3.1 准备用于签名、加密或压缩的 MIME 实体

S/MIME 用于保护 MIME 实体。MIME 实体可以是子部分、消息的多个子部分，或包含所有子部分的整条消息。作为整条消息的 MIME 实体仅包括 MIME 消息头和 MIME body，不包括 RFC-822 头部。注意，S/MIME 也可用于保护 Internet 邮件以外应用中使用的 MIME 实体。如果需要保护 RFC-822 头部，本节后面将解释 `message/rfc822` 媒体类型的使用。

被保护并在此节中描述的 MIME 实体可以被认为是"内部" MIME 实体。也就是说，它可能是更大的 MIME 消息中"最内层"的对象。将"外部" MIME 实体处理为 CMS 内容类型在第 3.2 节、第 3.4 节和其他地方描述。

准备 MIME 实体的过程在 [MIME-SPEC] 中给出。此处使用相同的过程，但在签名时有一些附加限制。[MIME-SPEC] 中过程的描述在此重复，但建议读者参考该文档获取确切过程。本节还描述了附加要求。

使用单一过程创建将要应用签名、加密和压缩任意组合的 MIME 实体。建议执行一些附加步骤以防御在邮件传输期间可能发生的已知损坏，这对于使用 `multipart/signed` 格式的明文签名（clear-signing）尤为重要。建议对加密消息或签名加加密消息也执行这些附加步骤，以便消息可以不经修改地转发到任何环境。

这些步骤是描述性的而非规定性的。实现者可以使用任何过程，只要结果相同即可。

**步骤 1**。按照本地约定准备 MIME 实体。

**步骤 2**。将 MIME 实体的叶节点部分转换为规范形式（canonical form）。

**步骤 3**。对 MIME 实体的叶节点应用适当的传输编码。

当收到 S/MIME 消息时，处理消息上的安全服务，结果是 MIME 实体。该 MIME 实体通常被传递给支持 MIME 的用户代理，在那里被进一步解码并呈现给用户或接收应用。

为了保护外部的、非内容相关的消息头字段（例如 "Subject"、"To"、"From" 和 "Cc" 字段），发送客户端可以将完整的 MIME 消息包装在 `message/rfc822` 包装器中，以便对这些头字段应用 S/MIME 安全服务。由接收客户端决定如何呈现此"内部"头部以及未受保护的"外部"头部。

当收到 S/MIME 消息时，如果顶层受保护的 MIME 实体的 Content-Type 为 `message/rfc822`，可以假定其意图是提供头部保护。此实体应该作为顶层消息呈现，同时考虑前面讨论的头部合并问题。

#### 3.1.1 规范化

每个 MIME 实体必须转换为一种规范形式，该形式在创建签名的环境和验证签名的环境中都能唯一且无歧义地表示。MIME 实体不仅用于签名，也必须为加密和压缩进行规范化。

规范化的确切细节取决于实体的实际媒体类型和子类型，此处不描述。相反，应该参考特定媒体类型的标准。例如，`text/plain` 类型的规范化与 `audio/basic` 的规范化不同。除文本类型外，大多数类型无论计算平台或环境如何都只有一种表示形式，可以被视为其规范表示。通常，规范化由发送代理的非安全部分执行，而不是由 S/MIME 实现执行。

最常见和最重要的规范化是文本规范化，因为文本在不同环境中通常有不同的表示形式。主类型为 "text" 的 MIME 实体必须同时规范化其行尾和字符集。行尾必须是 `<CR><LF>` 字符对，字符集应该是已注册的字符集 [CHARSETS]。规范化的详细信息在 [MIME-SPEC] 中指定。

注意，某些字符集（如 ISO-2022）对相同字符有多种表示形式。在准备此类文本进行签名时，必须使用为该字符集指定的规范表示形式。

#### 3.1.2 传输编码

当生成以下任何受保护的 MIME 实体（使用 `multipart/signed` 格式的签名除外）时，完全不需要传输编码。S/MIME 实现必须能够处理二进制 MIME 对象。如果不存在 Content-Transfer-Encoding 头字段，则假定传输编码为 7BIT。

然而，S/MIME 实现应该对它们保护的所有 MIME 实体使用第 3.1.3 节中描述的传输编码。仅保护 7 位 MIME 实体的原因（即使对于未暴露于传输的加密数据也是如此）是它允许 MIME 实体在任何环境中不经修改地处理。例如，受信任的网关可能会移除消息的信封但保留签名，然后将签名的消息转发给最终接收者，以便他们可以直接验证签名。如果站点内部的传输不是 8 位干净的（例如在具有单个邮件网关的广域网上），除非原始 MIME 实体仅是 7 位数据，否则验证签名将不可能。

"知道"所有预期接收者都能处理内部（除最外层外的所有层）二进制 MIME 对象的 S/MIME 实现应该对内部实体使用二进制编码，而不是 7 位安全的传输编码。使用 7 位安全编码（如 base64）会不必要地扩大消息大小。实现可以通过解释 `id-cap-preferBinaryInside` SMIMECapabilities 属性、通过事先约定或通过其他方式"知道"接收者实现能够处理内部二进制 MIME 实体。

如果一个或多个预期接收者无法处理内部二进制 MIME 对象，或者对于任何预期接收者此能力未知，S/MIME 实现应该对它们保护的所有 MIME 实体使用第 3.1.3 节中描述的传输编码。

#### 3.1.3 使用 multipart/signed 的签名的传输编码

如果 `multipart/signed` 实体要通过标准 Internet SMTP 基础设施或其他仅限于 7 位文本的传输进行传输，则必须应用传输编码以使其表示为 7 位文本。已经是 7 位数据的 MIME 实体不需要传输编码。8 位文本和二进制数据等实体可使用 quoted-printable 或 base64 传输编码。

> [!info] 为什么要求 7 位
> 7 位要求的主要原因是 Internet 邮件传输基础设施无法保证传输 8 位或二进制数据。即使传输基础设施的许多段现在能处理 8 位甚至二进制数据，有时无法知道传输路径是否 8 位干净。如果包含 8 位数据的邮件遇到无法传输 8 位或二进制数据的消息传输代理，该代理有三个选择，没有一个是明文签名消息可接受的：
>
> - 代理可以更改传输编码；这会使签名无效。
> - 代理可以不管怎样传输数据，这很可能会导致第 8 位被损坏；这也会使签名无效。
> - 代理可以将消息退回给发送者。

[MIME-SECURE] 禁止代理更改 `multipart/signed` 消息第一部分的传输编码。如果无法传输 8 位或二进制数据的合规代理遇到第一部分包含 8 位或二进制数据的 `multipart/signed` 消息，则必须将消息作为无法投递退回给发送者。

#### 3.1.4 示例规范化 MIME 实体

以下示例展示了一个具有完整传输编码的 `multipart/mixed` 消息。此消息包含一个文本部分和一个附件。示例消息文本包含非 US-ASCII 字符，因此需要传输编码。虽然此处未显示，每行末尾为 `<CR><LF>`。MIME 头部、文本和传输编码部分的行尾都必须是 `<CR><LF>`。

注意，此示例不是 S/MIME 消息。

```
Content-Type: multipart/mixed; boundary=bar

--bar
Content-Type: text/plain; charset=iso-8859-1
Content-Transfer-Encoding: quoted-printable

=A1Hola Michael!

How do you like the new S/MIME specification?

It's generally a good idea to encode lines that begin with
From=20because some mail transport agents will insert a greater-
than (>) sign, thus invalidating the signature.

Also, in some cases it might be desirable to encode any =20
trailing whitespace that occurs on lines in order to ensure =20
that the message signature is not invalidated when passing =20
a gateway that modifies such whitespace (like BITNET). =20

--bar
Content-Type: image/jpeg
Content-Transfer-Encoding: base64

iQCVAwUBMJrRF2N9oWBghPDJAQE9UQQAtl7LuRVndBjrk4EqYBIb3h5QXIX/LC//
jJV5bNvkZIGPIcEmI5iFd9boEgvpirHtIREEqLQRkYNoBActFBZmh9GC3C041WGq
uMbrbxc+nIs1TIKlA08rVi9ig/2Yh7LFrK5Ein57U/W72vgSxLhe/zhdfolT9Brn
HOxEa44b+EI=

--bar--
```

### 3.2 application/pkcs7-mime 媒体类型

`application/pkcs7-mime` 媒体类型用于承载 CMS 内容类型，包括 EnvelopedData、SignedData 和 CompressedData。构建这些实体的详细信息在后续各节中描述。本节描述 `application/pkcs7-mime` 媒体类型的通用特征。

承载的 CMS 对象始终包含按第 3.1 节描述准备的 MIME 实体（如果 eContentType 为 `id-data`）。当 eContentType 包含不同值时，可以承载其他内容。有关签名回执的示例，参见 [ESS]。

由于 CMS 内容类型是二进制数据，在大多数情况下 base64 传输编码是合适的，特别是与 SMTP 传输一起使用时。使用的传输编码取决于发送对象通过的传输，而不是媒体类型的特征。

注意，此讨论指的是 CMS 对象或"外部" MIME 实体的传输编码。它与 CMS 对象所保护的 MIME 实体（"内部"对象）的传输编码完全不同且无关，后者在第 3.1 节中描述。

由于存在多种类型的 `application/pkcs7-mime` 对象，发送代理应该尽可能帮助接收代理了解对象的内容，而无需强制接收代理解码对象的 ASN.1。所有 `application/pkcs7-mime` 对象的 Content-Type 头字段应该包含可选的 "smime-type" 参数，如下列各节所述。

#### 3.2.1 name 和 filename 参数

对于 `application/pkcs7-mime`，发送代理应该在 Content-Type 字段中发出可选的 "name" 参数以与旧系统兼容。发送代理还应该发出带有 "filename" 参数的可选 Content-Disposition 字段 [CONTDISP]。如果发送代理发出上述参数，参数值应该是具有适当扩展名的文件名：

| 媒体类型 | 文件扩展名 |
|---------|----------|
| `application/pkcs7-mime`（SignedData, EnvelopedData） | `.p7m` |
| `application/pkcs7-mime`（退化 SignedData 证书管理消息） | `.p7c` |
| `application/pkcs7-mime`（CompressedData） | `.p7z` |
| `application/pkcs7-signature`（SignedData） | `.p7s` |

此外，文件名应该限制为八个字符后跟三字母扩展名。八字符文件名基数可以是任何不同的名称；应该使用文件名基数 "smime" 来指示 MIME 实体与 S/MIME 相关联。

包含文件名有两个目的。它便于将 S/MIME 对象作为磁盘文件使用。它还可以跨网关传达类型信息。当 `application/pkcs7-mime` 类型的 MIME 实体（例如）到达没有 S/MIME 特殊知识的网关时，它将把实体的媒体类型默认为 `application/octet-stream` 并将其作为通用附件处理，从而丢失类型信息。然而，附件的建议文件名通常会跨网关传递。这通常允许接收系统确定适当的应用程序来交接附件，在此情况下是独立的 S/MIME 处理应用程序。

> [!note]
> 此机制是为某些环境中的实现提供便利。正确的 S/MIME 实现必须使用媒体类型，不得依赖文件扩展名。

#### 3.2.2 smime-type 参数

`application/pkcs7-mime` 内容类型定义了可选的 "smime-type" 参数。此参数的意图是传达关于应用的安全（签名或加密）以及所含内容的详细信息。本规范定义以下 smime-types。

| 名称 | CMS 类型 | 内部内容 |
|------|---------|---------|
| `enveloped-data` | EnvelopedData | id-data |
| `signed-data` | SignedData | id-data |
| `certs-only` | SignedData | none |
| `compressed-data` | CompressedData | id-data |

为了与未来规范保持一致性，分配新的 smime-type 参数时应该遵循以下指导原则：

1. 如果签名和加密都可以应用于内容，则应该分配两个 smime-type 值："signed-*" 和 "enveloped-*"。如果只能分配一种操作，则可以省略。因此，由于 "certs-only" 只能被签名，所以 "signed-" 被省略。
2. 应该为内容 OID 分配一个公共字符串。当 MIME 是内部内容时，我们对 `id-data` 内容 OID 使用 "data"。
3. 如果未分配公共字符串，则推荐使用 "OID.\<oid\>" 的公共字符串（例如，"OID.2.16.840.1.101.3.4.1.2" 将是 AES-128 CBC）。

此字段明确意图作为邮件客户端应用的合适提示，以指示消息是"签名的"还是"加密的"，而无需深入 CMS 载荷。

### 3.3 创建仅加密消息

本节描述在不签名的情况下加密 MIME 实体的格式。

> [!warning] 重要提示
> 发送加密但未签名的消息不提供数据完整性。可以以某种方式替换密文，使得处理后的消息仍然有效，但含义可能被改变。

**步骤 1**。按照第 3.1 节准备要加密的 MIME 实体。

**步骤 2**。将 MIME 实体和其他所需数据处理为 EnvelopedData 类型的 CMS 对象。除了为每个接收者加密内容加密密钥的副本外，应该为发起者加密内容加密密钥的副本并将其包含在 EnvelopedData 中（见 [CMS] 第 6 节）。

**步骤 3**。将 EnvelopedData 对象包装在 CMS ContentInfo 对象中。

**步骤 4**。将 ContentInfo 对象插入 `application/pkcs7-mime` MIME 实体中。

仅加密消息的 smime-type 参数为 "enveloped-data"。此类消息的文件扩展名为 ".p7m"。

示例消息：

```
Content-Type: application/pkcs7-mime; smime-type=enveloped-data;
     name=smime.p7m
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=smime.p7m

rfvbnj756tbBghyHhHUujhJhjH77n8HHGT9HG4VQpfyF467GhIGfHfYT6
7n8HHGghyHhHUujhJh4VQpfyF467GhIGfHfYGTrfvbnjT6jH7756tbB9H
f8HHGTrfvhJhjH776tbB9HG4VQbnj7567GhIGfHfYT6ghyHhHUujpfyF4
0GhIGfHfQbnj756YT64V
```

### 3.4 创建仅签名消息

S/MIME 定义了两种签名消息格式：

- `application/pkcs7-mime` 配合 SignedData
- `multipart/signed`

通常，发送时首选 `multipart/signed` 形式，接收代理必须能够处理两种格式。

#### 3.4.1 为仅签名消息选择格式

关于何时选择特定仅签名格式并没有硬性规则。这取决于所有接收者的能力，以及拥有 S/MIME 设施的接收者能够验证签名的相对重要性，与没有 S/MIME 软件的接收者能够查看消息的相对重要性。

使用 `multipart/signed` 格式签名的消息无论接收者是否拥有 S/MIME 软件都可以查看。无论他们是使用原生 MIME 用户代理还是通过网关翻译消息，也都可以查看。在此上下文中，"可查看"意味着能够基本上像处理未签名消息一样处理消息，包括消息可能具有的任何其他 MIME 结构。

使用 SignedData 格式签名的消息除非接收者拥有 S/MIME 设施，否则无法查看。然而，SignedData 格式保护消息内容不被善意中间代理更改。此类代理可能执行换行或内容传输编码更改，这些会破坏签名。

#### 3.4.2 使用 application/pkcs7-mime 配合 SignedData 签名

此签名格式使用 `application/pkcs7-mime` 媒体类型。创建此格式的步骤如下：

**步骤 1**。按照第 3.1 节准备 MIME 实体。

**步骤 2**。将 MIME 实体和其他所需数据处理为 SignedData 类型的 CMS 对象。

**步骤 3**。将 SignedData 对象包装在 CMS ContentInfo 对象中。

**步骤 4**。将 ContentInfo 对象插入 `application/pkcs7-mime` MIME 实体中。

使用 `application/pkcs7-mime` 配合 SignedData 的消息的 smime-type 参数为 "signed-data"。此类消息的文件扩展名为 ".p7m"。

示例消息：

```
Content-Type: application/pkcs7-mime; smime-type=signed-data;
     name=smime.p7m
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=smime.p7m

567GhIGfHfYT6ghyHhHUujpfyF4f8HHGTrfvhJhjH776tbB9HG4VQbnj7
77n8HHGT9HG4VQpfyF467GhIGfHfYT6rfvbnj756tbBghyHhHUujhJhjH
HUujhJh4VQpfyF467GhIGfHfYGTrfvbnjT6jH7756tbB9H7n8HHGghyHh
6YT64V0GhIGfHfQbnj75
```

#### 3.4.3 使用 multipart/signed 格式签名

此格式是明文签名（clear-signing）格式。没有任何 S/MIME 或 CMS 处理设施的接收者也能查看消息。它使用 [MIME-SECURE] 中描述的 `multipart/signed` 媒体类型。`multipart/signed` 媒体类型有两个部分。第一部分包含被签名的 MIME 实体；第二部分包含"分离式签名" CMS SignedData 对象，其中 encapContentInfo eContent 字段不存在。

##### 3.4.3.1 application/pkcs7-signature 媒体类型

此媒体类型始终包含一个 CMS ContentInfo，其中包含一个 SignedData 类型的 CMS 对象。SignedData encapContentInfo eContent 字段必须不存在。signerInfos 字段包含 MIME 实体的签名。

使用 `application/pkcs7-signature` 的仅签名消息的文件扩展名为 ".p7s"。

##### 3.4.3.2 创建 multipart/signed 消息

**步骤 1**。按照第 3.1 节准备要签名的 MIME 实体，特别注意明文签名的特殊要求。

**步骤 2**。将 MIME 实体提交给 CMS 处理，以获取 encapContentInfo eContent 字段不存在的 SignedData 类型对象。

**步骤 3**。将 MIME 实体插入 `multipart/signed` 消息的第一部分，除了第 3.1 节中描述的处理外不进行其他处理。

**步骤 4**。对"分离式签名" CMS SignedData 对象应用传输编码，并将其插入 `application/pkcs7-signature` 类型的 MIME 实体中。

**步骤 5**。将 `application/pkcs7-signature` 的 MIME 实体插入 `multipart/signed` 实体的第二部分。

`multipart/signed` 的 Content-Type 有两个必需参数：protocol 参数和 micalg 参数。

protocol 参数必须为 "application/pkcs7-signature"。注意，protocol 参数值周围需要引号，因为 MIME 要求参数值中的 "/" 字符必须被引用。

micalg 参数允许在验证签名时进行一遍处理。micalg 参数的值取决于计算消息完整性检查（Message Integrity Check）时使用的消息摘要算法。如果使用多个消息摘要算法，必须按 [MIME-SECURE] 用逗号分隔。micalg 参数中放置的值应该来自以下列表：

| 算法 | 使用的值 |
|------|---------|
| MD5 | `md5` |
| SHA-1 | `sha-1` |
| SHA-224 | `sha-224` |
| SHA-256 | `sha-256` |
| SHA-384 | `sha-384` |
| SHA-512 | `sha-512` |
| 其他 | （在算法配置文件中单独定义，或 "unknown"） |

> [!note] 历史说明
> 一些早期 S/MIME 实现为 micalg 参数发出并期望 "rsa-md5"、"rsa-sha1" 和 "sha1"。接收代理应该能够从其无法识别的 micalg 参数值中优雅恢复。此参数的未来名称将与 IANA "Hash Function Textual Names" 注册表保持一致。

##### 3.4.3.3 示例 multipart/signed 消息

```
Content-Type: multipart/signed;
   protocol="application/pkcs7-signature";
   micalg=sha1; boundary=boundary42

--boundary42
Content-Type: text/plain

This is a clear-signed message.

--boundary42
Content-Type: application/pkcs7-signature; name=smime.p7s
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=smime.p7s

ghyHhHUujhJhjH77n8HHGTrfvbnj756tbB9HG4VQpfyF467GhIGfHfYT6
4VQpfyF467GhIGfHfYT6jH77n8HHGghyHhHUujhJh756tbB9HGTrfvbnj
n8HHGTrfvhJhjH776tbB9HG4VQbnj7567GhIGfHfYT6ghyHhHUujpfyF4
7GhIGfHfYT64VQbnj756

--boundary42--
```

被摘要的内容（`multipart/signed` 的第一部分）由以下字节组成：

```
43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74 65 78 74 2f 70 6c 61 69
6e 0d 0a 0d 0a 54 68 69 73 20 69 73 20 61 20 63 6c 65 61 72 2d 73 69
67 6e 65 64 20 6d 65 73 73 61 67 65 2e 0d 0a
```

### 3.5 创建仅压缩消息

本节描述压缩 MIME 实体的格式。请注意，3.1 版之前的 S/MIME 版本未指定 CompressedData 的任何用途，将无法识别它。[CMSCOMPR] 中描述了使用能力指示接收 CompressedData 能力的方法，这是兼容性的首选方法。

**步骤 1**。按照第 3.1 节准备要压缩的 MIME 实体。

**步骤 2**。将 MIME 实体和其他所需数据处理为 CompressedData 类型的 CMS 对象。

**步骤 3**。将 CompressedData 对象包装在 CMS ContentInfo 对象中。

**步骤 4**。将 ContentInfo 对象插入 `application/pkcs7-mime` MIME 实体中。

仅压缩消息的 smime-type 参数为 "compressed-data"。此类消息的文件扩展名为 ".p7z"。

示例消息：

```
Content-Type: application/pkcs7-mime; smime-type=compressed-data;
   name=smime.p7z
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=smime.p7z

rfvbnj756tbBghyHhHUujhJhjH77n8HHGT9HG4VQpfyF467GhIGfHfYT6
7n8HHGghyHhHUujhJh4VQpfyF467GhIGfHfYGTrfvbnjT6jH7756tbB9H
f8HHGTrfvhJhjH776tbB9HG4VQbnj7567GhIGfHfYT6ghyHhHUujpfyF4
0GhIGfHfQbnj756YT64V
```

### 3.6 多重操作

仅签名、仅加密和仅压缩的 MIME 格式可以嵌套。这是因为这些格式都是封装其他 MIME 实体的 MIME 实体。

S/MIME 实现必须能够在接收者计算机的合理资源限制内接收和处理任意嵌套的 S/MIME。

可以按任何顺序应用签名、加密和压缩操作。这由实现者和用户选择。当先签名时，签名者随后被加密安全地遮蔽。当先加密时，签名者被暴露，但可以在不移除加密的情况下验证签名。这在需要自动签名验证的环境中很有用，因为验证签名不需要私钥材料。

> [!tip] 操作顺序的安全影响
> 选择先签名还是先加密有安全影响。先加密后签名的消息的接收者可以验证加密块未被更改，但无法确定签名者与消息未加密内容之间的任何关系。先签名后加密的消息的接收者可以假定签名消息本身未被更改，但细心的攻击者可能更改了加密消息中未经验证的部分。

使用压缩时，请记住以下指导原则：

- 不鼓励对二进制编码的加密数据进行压缩，因为这不会产生显著的压缩效果。然而，base64 编码的加密数据可能会受益匪浅。
- 如果有损压缩算法与签名一起使用，则需要先压缩，再签名。

### 3.7 创建证书管理消息

证书管理消息或 MIME 实体用于传输证书和/或证书撤销列表（CRL），例如响应注册请求。

**步骤 1**。将证书和/或 CRL 提供给生成 CMS 的流程，该流程创建 SignedData 类型的 CMS 对象。SignedData encapContentInfo eContent 字段必须不存在，signerInfos 字段必须为空。

**步骤 2**。将 SignedData 对象包装在 CMS ContentInfo 对象中。

**步骤 3**。将 ContentInfo 对象封装在 `application/pkcs7-mime` MIME 实体中。

证书管理消息的 smime-type 参数为 "certs-only"。此类消息的文件扩展名为 ".p7c"。

### 3.8 注册请求

签名消息的发送代理必须拥有签名证书，以便接收代理可以验证签名。获取证书的方式有很多，例如通过与证书颁发机构（CA, Certification Authority）交换、通过硬件令牌或磁盘等。

S/MIME v2 [SMIMEv2] 规定了一种使用 `application/pkcs10` body part 向证书颁发机构"注册"公钥的方法。此后，IETF PKIX 工作组开发了其他请求证书的方法。然而，S/MIME v3.2 不要求特定的证书请求机制。

### 3.9 识别 S/MIME 消息

由于 S/MIME 考虑到在非 MIME 环境中的互操作，使用了多种不同的机制来携带类型信息，因此识别 S/MIME 消息变得有些困难。下表列出了确定消息是否为 S/MIME 消息的标准。如果消息匹配以下任何标准，则被视为 S/MIME 消息。

下表中的文件后缀来自 Content-Type 头字段中的 "name" 参数，或 Content-Disposition 头字段中的 "filename" 参数。给出文件后缀的这些参数未在下面的参数部分列出。

| 媒体类型 | 参数 | 文件后缀 |
|---------|------|---------|
| `application/pkcs7-mime` | 任意 | 任意 |
| `multipart/signed` | `protocol="application/pkcs7-signature"` | 任意 |
| `application/octet-stream` | 任意 | p7m, p7s, p7c, p7z |

## 4. 证书处理

接收代理必须提供某种证书获取机制，以便访问数字信封接收者的证书。本规范不涵盖 S/MIME 代理如何处理证书，仅涵盖证书被验证或拒绝后的操作。S/MIME 证书问题在 [CERT32] 中涵盖。

至少，对于初始 S/MIME 部署，用户代理可以自动生成消息给预期接收者，在签名的回信中请求该接收者的证书。接收和发送代理还应该提供一种机制，允许用户以某种方式为通信者"存储和保护"证书，以保证其后续检索。

### 4.1 密钥对生成

所有生成的密钥对必须从良好的非确定性随机输入源 [RANDOM] 生成，并且私钥必须以安全方式保护。

S/MIME 用户代理不得生成小于 512 位的非对称密钥用于 RSA 或 DSA 签名算法。

- 512 位 RSA with SHA-1 参见 [CMSALG] 和 [FIPS186-2]（不带 Change Notice 1）
- 512 位 RSA with SHA-256 参见 [CMS-SHA2] 和 [FIPS186-2]（不带 Change Notice 1）
- 1024 位至 2048 位 RSA with SHA-256 参见 [CMS-SHA2] 和 [FIPS186-2]（带 Change Notice 1）

第一个引用提供签名算法的对象标识符，第二个提供签名算法的定义。

- 512 位 DSA with SHA-1 参见 [CMSALG] 和 [FIPS186-2]（不带 Change Notice 1）
- 512 位 DSA with SHA-256 参见 [CMS-SHA2] 和 [FIPS186-2]（不带 Change Notice 1）
- 1024 位 DSA with SHA-1 参见 [CMSALG] 和 [FIPS186-2]（带 Change Notice 1）
- 1024 位及以上 DSA with SHA-256 参见 [CMS-SHA2] 和 [FIPS186-3]

第一个引用提供签名算法的对象标识符，第二个提供签名算法的定义。

RSASSA-PSS with SHA-256 参见 [RSAPSS]。1024 位 DH 参见 [CMSALG]。1024 位及以上 DH 参见 [SP800-56A]；无论哪种情况，都使用 [CMSALG] 中规定的来自 X9.42 的 KDF。RSAES-OAEP 参见 [RSAOAEP]。

### 4.2 签名生成

以下是 S/MIME 代理生成 RSA、RSASSA-PSS 和 DSA 签名的要求：

| 密钥大小 | 要求 |
|---------|------|
| <= 1023 位 | 不应该（SHOULD NOT）（见安全考虑） |
| 1024 - 2048 位 | 应该（SHOULD）（见安全考虑） |
| > 2048 位 | 可以（MAY）（见安全考虑） |

### 4.3 签名验证

以下是 S/MIME 接收代理在验证 RSA、RSASSA-PSS 和 DSA 签名时的要求：

| 密钥大小 | 要求 |
|---------|------|
| <= 1023 位 | 可以（MAY）（见安全考虑） |
| 1024 - 2048 位 | 必须（MUST）（见安全考虑） |
| > 2048 位 | 可以（MAY）（见安全考虑） |

### 4.4 加密

以下是 S/MIME 代理在使用 RSA、RSA-OAEP 和 DH 算法建立内容加密密钥时的要求：

| 密钥大小 | 要求 |
|---------|------|
| <= 1023 位 | 不应该（SHOULD NOT）（见安全考虑） |
| 1024 - 2048 位 | 应该（SHOULD）（见安全考虑） |
| > 2048 位 | 可以（MAY）（见安全考虑） |

### 4.5 解密

以下是 S/MIME 代理在使用 RSA、RSAES-OAEP 和 DH 算法建立内容解密密钥时的要求：

| 密钥大小 | 要求 |
|---------|------|
| <= 1023 位 | 可以（MAY）（见安全考虑） |
| 1024 - 2048 位 | 必须（MUST）（见安全考虑） |
| > 2048 位 | 可以（MAY）（见安全考虑） |

## 5. IANA 考虑

以下信息更新了 `application/pkcs7-mime` 和 `application/pkcs7-signature` 的媒体类型注册，使其引用本文档而非 RFC 2311。

注意，其他文档可以为 S/MIME 定义额外的 MIME 媒体类型。

### 5.1 application/pkcs7-mime 的媒体类型

- **类型名称**：application
- **子类型名称**：pkcs7-mime
- **必需参数**：无
- **可选参数**：smime-type/signed-data、smime-type/enveloped-data、smime-type/compressed-data、smime-type/certs-only、name
- **编码考虑**：见本文档第 3 节
- **安全考虑**：见本文档第 6 节
- **互操作性考虑**：见本文档第 1-6 节
- **已发布规范**：RFC 2311、RFC 2633 和本文档
- **使用此媒体类型的应用**：安全应用
- **附加信息**：无
- **联系人和邮箱**：S/MIME 工作组主席 smime-chairs@tools.ietf.org
- **预期用途**：COMMON
- **使用限制**：无
- **作者**：Sean Turner
- **变更控制器**：IESG 委派的 S/MIME 工作组

### 5.2 application/pkcs7-signature 的媒体类型

- **类型名称**：application
- **子类型名称**：pkcs7-signature
- **必需参数**：无
- **可选参数**：无
- **编码考虑**：见本文档第 3 节
- **安全考虑**：见本文档第 6 节
- **互操作性考虑**：见本文档第 1-6 节
- **已发布规范**：RFC 2311、RFC 2633 和本文档
- **使用此媒体类型的应用**：安全应用
- **附加信息**：无
- **联系人和邮箱**：S/MIME 工作组主席 smime-chairs@tools.ietf.org
- **预期用途**：COMMON
- **使用限制**：无
- **作者**：Sean Turner
- **变更控制器**：IESG 委派的 S/MIME 工作组

## 6. 安全考虑

密码算法将随着时间被破解或削弱。实现者和用户需要检查本文档中列出的密码算法是否继续提供预期的安全级别。IETF 可能不时发布涉及当前技术水平的文档。例如：

- RFC 3218 [MMA] 中描述的百万消息攻击（Million Message Attack）。
- RFC 2785 [DHSUB] 中描述的 Diffie-Hellman "小子群"攻击。
- RFC 4270 [HASH-ATTACK] 中描述的针对哈希算法的攻击。

本规范使用公钥密码技术。假定私钥受到保护以确保不被未授权方访问或篡改。

大多数人或软件无法估计消息内容的价值。此外，大多数人或软件无法估计恢复使用特定大小密钥加密的消息内容的实际成本。此外，如果接收者无法处理消息内容，确定解密失败的成本也非常困难。因此，在不同密钥大小之间选择（或选择是否仅使用明文）对大多数人或软件来说也是不可能的。然而，基于这些标准的决策一直在做出，因此本规范提供了使用这些估计来选择算法的框架。

> [!tip] RSA 密钥大小选择
> 本规范中选择 2048 位作为 RSA 非对称密钥大小是基于提供至少 100 位安全性的愿望。为符合本规范而必须支持的密钥大小似乎适用于 Internet（基于 [STRENGTH]）。当然，有些环境（如金融和医疗系统）可能选择不同的密钥大小。因此，实现可以支持超出本规范推荐范围的密钥大小。

验证签名的接收代理和加密消息的发送代理在使用大于本规范规定的密钥验证签名和加密消息时，需要谨慎处理密码处理的使用。攻击者可能发送包含会导致过度密码处理的密钥的证书，例如大于本规范规定的密钥，这可能会使处理单元不堪重负。使用此类密钥但未首先将证书验证到信任锚的代理应建立某种密码资源管理系统以防止此类攻击。

在 S/MIME 中使用弱密码提供的实际安全性几乎没有超过发送明文。然而，S/MIME 的其他特性（如 AES 规范和向通信方宣布更强密码能力的能力）允许发送者创建使用强加密的消息。除非唯一替代方案是不使用密码，否则永远不建议使用弱密码。

> [!warning] 密钥大小警告
> 小于 1024 位的 RSA 和 DSA 密钥现在被许多专家认为在密码学上不安全（由于计算能力的进步），不应再用于保护消息。此类密钥以前被认为是安全的，因此处理以前接收的已签名和已加密邮件通常会导致使用弱密钥。希望支持先前 S/MIME 版本或处理旧消息的实现需要考虑较小密钥大小带来的安全风险（例如伪造消息）与拒绝服务成本的权衡。如果实现支持验证使用小于 1024 位的 RSA 和 DSA 密钥生成的数字签名，则必须警告用户。实现者应考虑对新接收的消息和先前存储的消息提供不同的警告。不适合用户警告的服务器实现（例如安全邮件列表服务器）应该拒绝具有弱签名的消息。

实现者应该注意，单个个体可能关联多个活动密钥对。例如，一个密钥对可用于支持机密性，而不同的密钥对可用于数字签名。

如果发送代理使用不同强度的密码发送相同消息，监视通信信道的攻击者可能能够通过解密弱加密版本来确定强加密消息的内容。换言之，发送者不应该使用比原始消息更弱的密码发送消息副本。

如果不同时使用认证，密文的修改可能不会被检测到，这就是在发送 EnvelopedData 而不将其包装在 SignedData 中或在其中包含 SignedData 时的情况。

如果实现关注是否符合 NIST 密钥大小建议，参见 [SP800-57]。

> [!warning] 签名状态验证
> 如果消息环境利用消息被签名这一事实来改变消息处理行为（例如运行规则或 UI 显示提示），而不首先验证消息实际上已被签名并了解签名的状态，这可能导致对消息的错误处理。消息上的视觉指示器可能需要定期检查签名验证代码，如果指示器应该提供消息当前状态的信息。

## 7. 参考文献

### 7.1 引用约定

- [CMS] 指代 [RFC5652]。
- [ESS] 指代 [RFC2634] 和 [RFC5035]。
- [MIME] 指代 [RFC2045]、[RFC2046]、[RFC2047]、[RFC2049]、[RFC4288] 和 [RFC4289]。
- [SMIMEv2] 指代 [RFC2311]、[RFC2312]、[RFC2313]、[RFC2314] 和 [RFC2315]。
- [SMIMEv3] 指代 [RFC2630]、[RFC2631]、[RFC2632]、[RFC2633]、[RFC2634] 和 [RFC5035]。
- [SMIMv3.1] 指代 [RFC2634]、[RFC3850]、[RFC3851]、[RFC3852] 和 [RFC5035]。

### 7.2 规范性引用

[CERT32]      Ramsdell, B. and S. Turner, "Secure/Multipurpose
              Internet Mail Extensions (S/MIME) Version 3.2
              Certificate Handling", RFC 5750, January 2010.

[CHARSETS]    Character sets assigned by IANA.  See
              http://www.iana.org/assignments/character-sets.

[CMSAES]      Schaad, J., "Use of the Advanced Encryption Standard
              (AES) Encryption Algorithm in Cryptographic Message
              Syntax (CMS)", RFC 3565, July 2003.

[CMSALG]      Housley, R., "Cryptographic Message Syntax (CMS)
              Algorithms", RFC 3370, August 2002.

[CMSCOMPR]    Gutmann, P., "Compressed Data Content Type for
              Cryptographic Message Syntax (CMS)", RFC 3274, June
              2002.

[CMS-SHA2]    Turner, S., "Using SHA2 Algorithms with Cryptographic
              Message Syntax", RFC 5754, January 2010.

[CONTDISP]    Troost, R., Dorner, S., and K. Moore, Ed.,
              "Communicating Presentation Information in Internet
              Messages: The Content-Disposition Header Field", RFC
              2183, August 1997.

[FIPS186-2]   National Institute of Standards and Technology (NIST),
              "Digital Signature Standard (DSS)", FIPS Publication
              186-2, January 2000. [With Change Notice 1].

[FIPS186-3]   National Institute of Standards and Technology (NIST),
              FIPS Publication 186-3: Digital Signature Standard,
              June 2009.

[MIME-SECURE] Galvin, J., Murphy, S., Crocker, S., and N. Freed,
              "Security Multiparts for MIME: Multipart/Signed and
              Multipart/Encrypted", RFC 1847, October 1995.

[MUSTSHOULD]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

[RANDOM]      Eastlake, D., 3rd, Schiller, J., and S. Crocker,
              "Randomness Requirements for Security", BCP 106, RFC
              4086, June 2005.

[RFC2045]     Freed, N. and N. Borenstein, "Multipurpose Internet
              Mail Extensions (MIME) Part One: Format of Internet
              Message Bodies", RFC 2045, November 1996.

[RFC2046]     Freed, N. and N. Borenstein, "Multipurpose Internet
              Mail Extensions (MIME) Part Two: Media Types", RFC
              2046, November 1996.

[RFC2047]     Moore, K., "MIME (Multipurpose Internet Mail
              Extensions) Part Three: Message Header Extensions for
              Non-ASCII Text", RFC 2047, November 1996.

[RFC2049]     Freed, N. and N. Borenstein, "Multipurpose Internet
              Mail Extensions (MIME) Part Five: Conformance Criteria
              and Examples", RFC 2049, November 1996.

[RFC2634]     Hoffman, P. Ed., "Enhanced Security Services for
              S/MIME", RFC 2634, June 1999.

[RFC4288]     Freed, N. and J. Klensin, "Media Type Specifications
              and Registration Procedures", BCP 13, RFC 4288,
              December 2005.

[RFC4289]     Freed, N. and J. Klensin, "Multipurpose Internet Mail
              Extensions (MIME) Part Four: Registration Procedures",
              BCP 13, RFC 4289, December 2005.

[RFC5035]     Schaad, J., "Enhanced Security Services (ESS) Update:
              Adding CertID Algorithm Agility", RFC 5035, August
              2007.

[RFC5652]     Housley, R., "Cryptographic Message Syntax (CMS)", RFC
              5652, September 2009.

[RSAOAEP]     Housley, R. "Use of the RSAES-OAEP Key Transport
              Algorithm in the Cryptographic Message Syntax (CMS)",
              RFC 3560, July 2003.

[RSAPSS]      Schaad, J., "Use of the RSASSA-PSS Signature Algorithm
              in Cryptographic Message Syntax (CMS)", RFC 4056, June
              2005.

[SP800-56A]   National Institute of Standards and Technology (NIST),
              Special Publication 800-56A: Recommendation Pair-Wise
              Key Establishment Schemes Using Discrete Logarithm
              Cryptography (Revised), March 2007.

[X.680]       ITU-T Recommendation X.680 (2002) | ISO/IEC
              8824-1:2002. Information Technology - Abstract Syntax
              Notation One (ASN.1):  Specification of basic notation.

[X.690]       ITU-T Recommendation X.690 (2002) | ISO/IEC
              8825-1:2002.  Information Technology - ASN.1 encoding
              rules: Specification of Basic Encoding Rules (BER),
              Canonical Encoding Rules (CER) and Distinguished
              Encoding Rules (DER).

### 7.3 信息性引用

[DHSUB]       Zuccherato, R., "Methods for Avoiding the "Small-
              Subgroup" Attacks on the Diffie-Hellman Key Agreement
              Method for S/MIME", RFC 2785, March 2000.

[HASH-ATTACK] Hoffman, P. and B. Schneier, "Attacks on Cryptographic
              Hashes in Internet Protocols", RFC 4270, November 2005.

[MMA]         Rescorla, E., "Preventing the Million Message Attack on
              Cryptographic Message Syntax", RFC 3218, January 2002.

[PKCS-7]      Kaliski, B., "PKCS #7: Cryptographic Message Syntax
              Version 1.5", RFC 2315, March 1998.

[RFC2311]     Dusse, S., Hoffman, P., Ramsdell, B., Lundblade, L.,
              and L. Repka, "S/MIME Version 2 Message Specification",
              RFC 2311, March 1998.

[RFC2312]     Dusse, S., Hoffman, P., Ramsdell, B., and J.
              Weinstein, "S/MIME Version 2 Certificate Handling", RFC
              2312, March 1998.

[RFC2313]     Kaliski, B., "PKCS #1: RSA Encryption Version 1.5", RFC
              2313, March 1998.

[RFC2314]     Kaliski, B., "PKCS #10: Certification Request Syntax
              Version 1.5", RFC 2314, March 1998.

[RFC2315]     Kaliski, B., "PKCS #7: Certification Message Syntax
              Version 1.5", RFC 2315, March 1998.

[RFC2630]     Housley, R., "Cryptographic Message Syntax", RFC 2630,
              June 1999.

[RFC2631]     Rescorla, E., "Diffie-Hellman Key Agreement Method",
              RFC 2631, June 1999.

[RFC2632]     Ramsdell, B., Ed., "S/MIME Version 3 Certificate
              Handling", RFC 2632, June 1999.

[RFC2633]     Ramsdell, B., Ed., "S/MIME Version 3 Message
              Specification", RFC 2633, June 1999.

[RFC3850]     Ramsdell, B., Ed., "Secure/Multipurpose Internet Mail
              Extensions (S/MIME) Version 3.1 Certificate Handling",
              RFC 3850, July 2004.

[RFC3851]     Ramsdell, B., Ed., "Secure/Multipurpose Internet Mail
              Extensions (S/MIME) Version 3.1 Message Specification",
              RFC 3851, July 2004.

[RFC3852]     Housley, R., "Cryptographic Message Syntax (CMS)", RFC
              3852, July 2004.

[SP800-57]    National Institute of Standards and Technology (NIST),
              Special Publication 800-57: Recommendation for Key
              Management, August 2005.

[STRENGTH]    Orman, H., and P. Hoffman, "Determining Strengths For
              Public Keys Used For Exchanging Symmetric Keys", BCP
              86, RFC 3766, April 2004.

## 附录 A. ASN.1 模块

> [!note]
> 此处包含的 ASN.1 模块与 RFC 3851 [SMIMEv3.1] 相比未作更改，除了 `prefersBinaryInside` ASN.1 注释的更改。此模块使用 1988 版本的 ASN.1。

```
SecureMimeMessageV3dot1

  { iso(1) member-body(2) us(840) rsadsi(113549)
         pkcs(1) pkcs-9(9) smime(16) modules(0) msg-v3dot1(21) }

DEFINITIONS IMPLICIT TAGS ::=

BEGIN

IMPORTS

-- Cryptographic Message Syntax [CMS]
   SubjectKeyIdentifier, IssuerAndSerialNumber,
   RecipientKeyIdentifier
       FROM  CryptographicMessageSyntax
             { iso(1) member-body(2) us(840) rsadsi(113549)
               pkcs(1) pkcs-9(9) smime(16) modules(0) cms-2001(14) };

--  id-aa is the arc with all new authenticated and unauthenticated
--  attributes produced by the S/MIME Working Group

id-aa OBJECT IDENTIFIER ::= {iso(1) member-body(2) usa(840)
        rsadsi(113549) pkcs(1) pkcs-9(9) smime(16) attributes(2)}

-- S/MIME Capabilities provides a method of broadcasting the
-- symmetric capabilities understood.  Algorithms SHOULD be ordered
-- by preference and grouped by type

smimeCapabilities OBJECT IDENTIFIER ::= {iso(1) member-body(2)
        us(840) rsadsi(113549) pkcs(1) pkcs-9(9) 15}

SMIMECapability ::= SEQUENCE {
   capabilityID OBJECT IDENTIFIER,
   parameters ANY DEFINED BY capabilityID OPTIONAL }

SMIMECapabilities ::= SEQUENCE OF SMIMECapability

-- Encryption Key Preference provides a method of broadcasting the
-- preferred encryption certificate.

id-aa-encrypKeyPref OBJECT IDENTIFIER ::= {id-aa 11}

SMIMEEncryptionKeyPreference ::= CHOICE {
   issuerAndSerialNumber   [0] IssuerAndSerialNumber,
   receipentKeyId          [1] RecipientKeyIdentifier,
   subjectAltKeyIdentifier [2] SubjectKeyIdentifier
}

-- receipentKeyId is spelt incorrectly, but kept for historical
-- reasons.

id-smime OBJECT IDENTIFIER ::= { iso(1) member-body(2) us(840)
        rsadsi(113549) pkcs(1) pkcs9(9) 16 }

id-cap  OBJECT IDENTIFIER ::= { id-smime 11 }

-- The preferBinaryInside OID indicates an ability to receive
-- messages with binary encoding inside the CMS wrapper.
-- The preferBinaryInside attribute's value field is ABSENT.

id-cap-preferBinaryInside  OBJECT IDENTIFIER ::= { id-cap 1 }

--  The following list OIDs to be used with S/MIME V3

-- Signature Algorithms Not Found in [CMSALG], [CMS-SHA2], [RSAPSS],
-- and [RSAOAEP]

--
-- md2WithRSAEncryption OBJECT IDENTIFIER ::=
--    {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-1(1)
--     2}

--
-- Other Signed Attributes
--
-- signingTime OBJECT IDENTIFIER ::=
--    {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-9(9)
--     5}
--    See [CMS] for a description of how to encode the attribute
--    value.

SMIMECapabilitiesParametersForRC2CBC ::= INTEGER
--        (RC2 Key Length (number of bits))

END
```

## 附录 B. 将 S/MIME v2 消息规范移至 Historic 状态

S/MIME v3 [SMIMEv3]、v3.1 [SMIMEv3.1] 和 v3.2（本文档）与 S/MIME v2 消息规范 [SMIMEv2] 向后兼容，但算法方面除外（删除了 RC2/40 要求，添加了 DSA 和 RSASSA-PSS 要求）。因此，建议将 RFC 2311 [SMIMEv2] 移至 Historic 状态。

## 附录 C. 致谢

非常感谢 S/MIME 版本 2 消息规范 RFC 的其他作者：Steve Dusse、Paul Hoffman、Laurence Lundblade 和 Lisa Repka。没有 v2，就不会有 v3、v3.1 或 v3.2。

S/MIME 工作组的许多成员也非常努力地工作并为本文件做出了贡献。任何人员名单都注定会有遗漏，对此我深表歉意。按字母顺序排列，以下人员在我心中格外突出，因为他们直接对本文件做出了贡献：

Tony Capel、Piers Chivers、Dave Crocker、Bill Flanigan、Peter Gutmann、Alfred Hoenes、Paul Hoffman、Russ Housley、William Ottaway、John Pawling 和 Jim Schaad。

## 作者地址

Blake Ramsdell
Brute Squad Labs, Inc.

Email: blaker@gmail.com

Sean Turner
IECA, Inc.
3057 Nutley Street, Suite 106
Fairfax, VA 22031
USA

Email: turners@ieca.com
