---
title: 密码消息语法 (CMS)
description: RFC 5652 定义的密码消息语法标准，用于对任意消息内容进行数字签名、摘要、认证或加密。
tags:
  - 密码学
  - CMS
  - 密码消息语法
  - PKCS7
  - RFC
---

> [!info] RFC 信息
> **RFC 编号**：5652
> **标题**：Cryptographic Message Syntax (CMS)
> **类别**：Standards Track
> **日期**：2009 年 9 月
> **作者**：R. Housley (Vigil Security)
> **替代**：RFC 3852

## 摘要

本文档描述了密码消息语法（Cryptographic Message Syntax，CMS）。该语法用于对任意消息内容进行[[数字签名]]、摘要计算、认证或加密。

## 1. 引言

本文档描述了密码消息语法（Cryptographic Message Syntax，CMS）。该语法用于对任意消息内容进行[[数字签名]]、摘要计算、认证或加密。

CMS 描述了一种用于数据保护的封装语法。它支持[[数字签名]]和加密。该语法允许多层封装——一个封装信封可以嵌套在另一个信封内。同样，一方可以对先前已封装的数据进行[[数字签名]]。它还允许将任意属性（如签名时间）与消息内容一起签名，并支持将其他属性（如副签名，countersignature）与签名关联。

CMS 可以支持多种基于证书的[[密钥管理]]体系结构，例如由 PKIX（Public Key Infrastructure using X.509）工作组定义的体系结构 [PROFILE]。

CMS 值使用 [[ASN.1]] [X.208-88] 生成，采用 BER 编码（Basic Encoding Rules，基本编码规则）[X.209-88]。值通常表示为八位字节字符串。虽然许多系统能够可靠地传输任意八位字节字符串，但众所周知，许多电子邮件系统并不具备这种能力。本文档不涉及在此类环境中为可靠传输而编码八位字节字符串的机制。

### 1.1. CMS 的演进

CMS 源自 PKCS #7 版本 1.5，记录于 RFC 2315 [PKCS#7]。PKCS #7 版本 1.5 是在 IETF 之外开发的；它最初于 1993 年 11 月作为 RSA Laboratories 技术笔记发布。此后，IETF 承担了 CMS 的开发和维护职责。如今，多个重要的 IETF 标准跟踪协议使用了 CMS。

本节描述 IETF 在每个已发布版本中对 CMS 所做的更改。

#### 1.1.1. 自 PKCS #7 版本 1.5 以来的变更

RFC 2630 [CMS1] 是 CMS 在 IETF 标准跟踪上的第一个版本。在可能的情况下，保持了与 PKCS #7 版本 1.5 的向后兼容性；但是，为了适应版本 1 属性证书传输和支持与算法无关的[[密钥管理]]，进行了更改。PKCS #7 版本 1.5 仅支持密钥传输（key transport）。RFC 2630 增加了对密钥协商（key agreement）和预分发的对称密钥加密密钥技术的支持。

#### 1.1.2. 自 RFC 2630 以来的变更

RFC 3369 [CMS2] 废弃了 RFC 2630 [CMS1] 和 RFC 3211 [PWRI]。基于密码的[[密钥管理]]被纳入 CMS 规范，并指定了一种[[扩展机制]]以支持新的[[密钥管理]]方案而无需进一步修改 CMS。保持了与 RFC 2630 和 RFC 3211 的向后兼容性；但是，增加了版本 2 属性证书传输，并弃用了版本 1 属性证书的使用。

[[S/MIME]] v2 签名 [MSG2]（基于 PKCS #7 版本 1.5）与 [[S/MIME]] v3 签名 [MSG3] 和 [[S/MIME]] v3.1 签名 [MSG3.1] 兼容。然而，基于 PKCS #7 版本 1.5 的签名存在一些细微的兼容性问题。这些问题在第 5.2.1 节中讨论。这些问题在当前版本的 CMS 中仍然存在。

本文档不讨论特定的密码算法（它们曾在 RFC 2630 中讨论）。对特定密码算法的讨论已移至单独的文档 [CMSALG]。协议和算法规范的分离允许 IETF 独立更新每个文档。本规范不要求实现任何特定算法。相反，依赖 CMS 的协议应为其环境选择适当的算法。算法可以从 [CMSALG] 或其他来源中选择。

#### 1.1.3. 自 RFC 3369 以来的变更

RFC 3852 [CMS3] 废弃了 RFC 3369 [CMS2]。如前一节所述，RFC 3369 引入了一种[[扩展机制]]以支持新的[[密钥管理]]方案而无需进一步修改 CMS。RFC 3852 引入了类似的[[扩展机制]]以支持额外的证书格式和撤销状态信息格式而无需进一步修改 CMS。这些扩展主要记录在第 10.2.1 节和第 10.2.2 节。保持了与早期版本 CMS 的向后兼容性。

版本号的使用在第 1.3 节中描述。

自 RFC 3369 发布以来，已发现一些勘误。这些勘误发布在 RFC Editor 网站上。本文档已纠正这些错误。

第 11.4 节中描述副签名（countersignature）未签名属性的文本已澄清。希望修订后的文本能更清楚地说明 SignerInfo 签名中被副签名覆盖的部分。

#### 1.1.4. 自 RFC 3852 以来的变更

本文档废弃 RFC 3852 [CMS3]。发布本文档的主要原因是推动 CMS 沿标准成熟度阶梯前进。

本文档包含了最初发布在 RFC 4853 [CMSMSIG] 中的关于当存在多个[[数字签名]]时正确处理 SignedData 受保护内容类型的澄清。

自 RFC 3852 发布以来，已发现一些勘误。这些勘误发布在 RFC Editor 网站上。本文档已纠正这些错误。

### 1.2. 术语

在本文档中，关键术语 MUST、MUST NOT、REQUIRED、SHOULD、SHOULD NOT、RECOMMENDED、MAY 和 OPTIONAL 应按照 [STDWORDS] 中的描述进行解释。

### 1.3. 版本号

每个主要数据结构都以版本号作为数据结构的第一项。版本号旨在避免 [[ASN.1]] 解码错误。一些实现在尝试解码之前不检查版本号，如果发生解码错误，则版本号将作为错误处理例程的一部分进行检查。这是一种合理的方法；它将错误处理置于快速路径之外。当发送方使用不正确的版本号时，这种方法也是宽容的。

大多数初始版本号是在 PKCS #7 版本 1.5 中分配的。其他的是在结构最初创建时分配的。每当结构更新时，都会分配更高的版本号。但是，为确保最大互操作性，仅在使用了新语法特性时才使用更高的版本号。也就是说，使用支持所生成语法的最低版本号。

## 2. 总体概述

CMS 足够通用，可以支持许多不同的内容类型。本文档定义了一种保护内容——ContentInfo。ContentInfo 封装单个已识别的内容类型，该已识别的类型可以提供进一步的封装。本文档定义了六种内容类型：data（数据）、signed-data（签名数据）、enveloped-data（信封数据）、digested-data（摘要数据）、encrypted-data（加密数据）和 authenticated-data（认证数据）。其他内容类型可以在本文档之外定义。

符合本规范的实现 MUST 实现保护内容 ContentInfo，并且 MUST 实现 data、signed-data 和 enveloped-data 内容类型。其他内容类型 MAY 实现。

作为一般设计理念，每种内容类型都允许使用不定长 BER 编码（Basic Encoding Rules）进行单遍处理。当内容很大、存储在磁带上或从另一个进程"管道"传输时，单遍操作特别有用。单遍操作有一个显著缺点：难以在单遍中使用 DER 编码（Distinguished Encoding Rules，辨别编码规则）[X.509-88] 执行编码操作，因为各组件的长度可能事先未知。然而，signed-data 内容类型中的已签名属性和 authenticated-data 内容类型中的已认证属性需要以 DER 形式传输，以确保接收方能够验证包含一个或多个未识别属性的内容。已签名属性和已认证属性是 CMS 中唯一需要 DER 编码的数据类型。

## 3. 通用语法

以下对象标识符标识内容信息类型：

```
id-ct-contentInfo OBJECT IDENTIFIER ::= { iso(1) member-body(2)
   us(840) rsadsi(113549) pkcs(1) pkcs9(9) smime(16) ct(1) 6 }
```

CMS 将内容类型标识符与内容关联。语法 MUST 具有 [[ASN.1]] 类型 ContentInfo：

```
ContentInfo ::= SEQUENCE {
  contentType ContentType,
  content [0] EXPLICIT ANY DEFINED BY contentType }

ContentType ::= OBJECT IDENTIFIER
```

ContentInfo 的字段含义如下：

- **contentType**：指示关联内容的类型。它是一个对象标识符，是由定义内容类型的权威机构分配的唯一整数字符串。
- **content**：关联的内容。内容的类型可以由 contentType 唯一确定。本文档定义了 data、signed-data、enveloped-data、digested-data、encrypted-data 和 authenticated-data 的内容类型。如果在其他文档中定义了额外内容类型，定义的 [[ASN.1]] 类型 SHOULD NOT 为 CHOICE 类型。

## 4. 数据内容类型

以下对象标识符标识数据内容类型：

```
id-data OBJECT IDENTIFIER ::= { iso(1) member-body(2)
   us(840) rsadsi(113549) pkcs(1) pkcs7(7) 1 }
```

数据内容类型旨在引用任意八位字节字符串，如 ASCII 文本文件；其解释留给应用程序。此类字符串不需要具有任何内部结构（尽管它们可以有自己的 [[ASN.1]] 定义或其他结构）。

[[S/MIME]] 使用 id-data 标识 MIME 编码的内容。此内容标识符的使用在 RFC 2311 中为 [[S/MIME]] v2 [MSG2] 指定，在 RFC 2633 中为 [[S/MIME]] v3 [MSG3] 指定，在 RFC 3851 中为 [[S/MIME]] v3.1 [MSG3.1] 指定。

数据内容类型通常封装在 signed-data、enveloped-data、digested-data、encrypted-data 或 authenticated-data 内容类型中。

## 5. 签名数据内容类型 (Signed-data)

签名数据内容类型由任意类型的内容和零个或多个签名值组成。任意数量的签名者可以并行签名任意类型的内容。

签名数据内容类型的典型应用是表示一个签名者对 data 内容类型内容的[[数字签名]]。另一个典型应用是分发证书和证书撤销列表（CRL）。

构造签名数据的过程涉及以下步骤：

1. 对于每个签名者，使用签名者特定的消息摘要算法计算内容的消息摘要（即哈希值）。如果签名者正在签名内容以外的信息，则内容的摘要和其他信息将用签名者的消息摘要算法进行摘要计算（参见第 5.4 节），结果即为"消息摘要"。
2. 对于每个签名者，使用签名者的私钥对消息摘要进行[[数字签名]]。
3. 对于每个签名者，将签名值和其他签名者特定信息收集到 SignerInfo 值中，如第 5.3 节所定义。每个签名者的证书和 CRL，以及不对应任何签名者的证书和 CRL，在此步骤中收集。
4. 所有签名者的消息摘要算法和所有签名者的 SignerInfo 值与内容一起收集到 SignedData 值中，如第 5.1 节所定义。

接收方独立计算消息摘要。此消息摘要和签名者的公钥用于验证签名值。签名者的公钥通过两种方式之一引用：可以通过颁发者可辨别名称和颁发者特定的序列号来唯一标识包含公钥的证书，也可以通过主题密钥标识符引用，后者既适用于已认证也适用于未认证的公钥。虽然不是必须的，签名者的证书可以包含在 SignedData 的 certificates 字段中。

> [!note] 多签名场景
> 当存在多个签名时，成功验证与给定签名者关联的一个签名通常被视为该签名者的成功签名。但是，某些应用环境需要其他规则。采用非"每个签名者一个有效签名"规则的应用程序必须指定这些规则。此外，当简单匹配签名者标识符不足以确定签名是否由同一签名者生成时，应用规范必须描述如何确定哪些签名由同一签名者生成。支持不同接收方群体是签名者选择包含多个签名的主要原因。例如，signed-data 内容类型可能包含使用 RSA 签名算法和 ECDSA（椭圆曲线[[数字签名]]算法）生成的签名，允许接收方验证与其中一种算法关联的签名。

本节分为六个部分。第一部分描述顶层类型 SignedData，第二部分描述 EncapsulatedContentInfo，第三部分描述每个签名者的信息类型 SignerInfo，第四、五、六部分分别描述消息摘要计算、签名生成和签名验证过程。

### 5.1. SignedData 类型

以下对象标识符标识签名数据内容类型：

```
id-signedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
   us(840) rsadsi(113549) pkcs(1) pkcs7(7) 2 }
```

签名数据内容类型应具有 [[ASN.1]] 类型 SignedData：

```
SignedData ::= SEQUENCE {
  version CMSVersion,
  digestAlgorithms DigestAlgorithmIdentifiers,
  encapContentInfo EncapsulatedContentInfo,
  certificates [0] IMPLICIT CertificateSet OPTIONAL,
  crls [1] IMPLICIT RevocationInfoChoices OPTIONAL,
  signerInfos SignerInfos }

DigestAlgorithmIdentifiers ::= SET OF DigestAlgorithmIdentifier

SignerInfos ::= SET OF SignerInfo
```

SignedData 类型的字段含义如下：

- **version**：语法版本号。适当的值取决于 certificates、eContentType 和 SignerInfo。版本 MUST 按如下方式分配：
  - IF（certificates 存在 AND 任何类型为 other 的证书存在）OR（crls 存在 AND 任何类型为 other 的 crl 存在）THEN version MUST 为 5
  - ELSE IF（certificates 存在 AND 任何版本 2 属性证书存在）THEN version MUST 为 4
  - ELSE IF（certificates 存在 AND 任何版本 1 属性证书存在）OR（任何 SignerInfo 结构为版本 3）OR（encapContentInfo eContentType 不是 id-data）THEN version MUST 为 3
  - ELSE version MUST 为 1

- **digestAlgorithms**：消息摘要算法标识符的集合。集合中 MAY 有任意数量的元素，包括零。每个元素标识一个或多个签名者使用的消息摘要算法及任何关联参数。该集合旨在以任意顺序列出所有签名者使用的消息摘要算法，以便于单遍签名验证。实现 MAY 无法验证使用未包含在此集合中的摘要算法的签名。消息摘要过程在第 5.4 节中描述。

- **encapContentInfo**：已签名的内容，由内容类型标识符和内容本身组成。EncapsulatedContentInfo 类型的详细信息在第 5.2 节中讨论。

- **certificates**：证书的集合。该证书集应足以包含从认可的"根"或"顶级认证机构"到 signerInfos 字段中所有签名者的认证路径。证书可能多于必要的数量，也可能足以包含从两个或更多独立顶级认证机构的认证路径。如果预期接收方有其他方式获取必要的证书（例如，从先前的一组证书），证书也可能少于必要的数量。签名者的证书 MAY 被包含。强烈建议不要使用版本 1 属性证书。

- **crls**：撤销状态信息的集合。该集合应包含足够的信息以确定 certificates 字段中的证书是否有效，但不需要完全对应。证书撤销列表（CRL）是撤销状态信息的主要来源。CRL MAY 多于必要的数量，也 MAY 少于必要的数量。

- **signerInfos**：每个签名者信息的集合。集合中 MAY 有任意数量的元素，包括零。当集合代表多个签名时，成功验证给定签名者的一个签名应被视为该签名者的成功签名。但是，某些应用环境需要其他规则。SignerInfo 类型的详细信息在第 5.3 节中讨论。由于每个签名者可以使用不同的[[数字签名]]技术，且未来的规范可能更新语法，所有实现 MUST 优雅地处理未实现的 SignerInfo 版本。此外，由于并非所有实现都支持每种可能的签名算法，所有实现 MUST 在遇到未实现的签名算法时优雅地处理。

### 5.2. EncapsulatedContentInfo 类型

内容以 EncapsulatedContentInfo 类型表示：

```
EncapsulatedContentInfo ::= SEQUENCE {
  eContentType ContentType,
  eContent [0] EXPLICIT OCTET STRING OPTIONAL }

ContentType ::= OBJECT IDENTIFIER
```

EncapsulatedContentInfo 类型的字段含义如下：

- **eContentType**：对象标识符，唯一指定内容类型。
- **eContent**：内容本身，以八位字节字符串形式携带。eContent 不需要 DER 编码。

EncapsulatedContentInfo 字段中 eContent 的可选省略使得构造"外部签名"（external signatures）成为可能。在外部签名的情况下，被签名的内容不包含在 signed-data 内容类型中包含的 EncapsulatedContentInfo 值中。如果 EncapsulatedContentInfo 中的 eContent 值不存在，则 signatureValue 的计算和 eContentType 的赋值仍按照 eContent 值存在的方式进行。

在没有签名者的退化情况下，被"签名"的 EncapsulatedContentInfo 值是无关紧要的。在这种情况下，被"签名"的 EncapsulatedContentInfo 值中的内容类型 MUST 为 id-data（如第 4 节所定义），且 EncapsulatedContentInfo 值的内容字段 MUST 被省略。

#### 5.2.1. 与 PKCS #7 的兼容性

> [!warning] 兼容性注意事项
> 本节包含对希望同时支持 CMS 和 PKCS #7 [PKCS#7] SignedData 内容类型的实现者的警告。

CMS 和 PKCS #7 都使用对象标识符来标识封装内容的类型，但 PKCS #7 SignedData 内容类型中内容本身的 [[ASN.1]] 类型是可变的。

PKCS #7 定义 content 为：

```
content [0] EXPLICIT ANY DEFINED BY contentType OPTIONAL
```

CMS 定义 eContent 为：

```
eContent [0] EXPLICIT OCTET STRING OPTIONAL
```

CMS 定义在大多数应用中更易使用，且与 [[S/MIME]] v2 和 [[S/MIME]] v3 兼容。使用 CMS 和 PKCS #7 的 [[S/MIME]] 签名消息是兼容的，因为 RFC 2311（[[S/MIME]] v2 [MSG2]）、RFC 2633（[[S/MIME]] v3 [MSG3]）和 RFC 3851（[[S/MIME]] v3.1 [MSG3.1]）指定了相同的签名消息格式。[[S/MIME]] v2 将 MIME 内容封装在 Data 类型（即 OCTET STRING）中，携带在 SignedData contentInfo content ANY 字段中，而 [[S/MIME]] v3 将 MIME 内容携带在 SignedData encapContentInfo eContent OCTET STRING 中。因此，在 [[S/MIME]] v2、[[S/MIME]] v3 和 [[S/MIME]] v3.1 中，MIME 内容被放置在 OCTET STRING 中，消息摘要对内容的相同部分进行计算。也就是说，消息摘要是对组成 OCTET STRING 值的八位字节计算的，不包括标签和长度八位字节。

当封装内容不使用 Data 类型格式化时，CMS 和 PKCS #7 SignedData 类型之间存在不兼容性。例如，当 RFC 2634 签名回执 [ESS] 封装在 CMS SignedData 类型中时，Receipt SEQUENCE 被编码在 SignedData encapContentInfo eContent OCTET STRING 中，消息摘要使用整个 Receipt SEQUENCE 编码（包括标签、长度和值八位字节）计算。但是，如果 RFC 2634 签名回执封装在 PKCS #7 SignedData 类型中，则 Receipt SEQUENCE 以 DER 编码 [X.509-88] 放在 SignedData contentInfo content ANY 字段中（是一个 SEQUENCE，而不是 OCTET STRING）。因此，消息摘要仅使用 Receipt SEQUENCE 编码的值八位字节计算。

以下策略可用于在处理 SignedData 内容类型时实现与 PKCS #7 的向后兼容性。如果实现无法使用 CMS SignedData encapContentInfo eContent OCTET STRING 语法对 SignedData 类型进行 [[ASN.1]] 解码，则实现 MAY 尝试使用 PKCS #7 SignedData contentInfo content ANY 语法解码 SignedData 类型，并相应地计算消息摘要。

以下策略可用于在创建封装内容不使用 Data 类型格式的 SignedData 内容类型时实现与 PKCS #7 的向后兼容性。实现 MAY 检查 eContentType 的值，然后根据对象标识符值调整 eContent 的预期 DER 编码。例如，为支持 Microsoft Authenticode [MSAC]，MAY 包含以下信息：

- eContentType 对象标识符设置为 `{ 1 3 6 1 4 1 311 2 1 4 }`
- eContent 包含 DER 编码的 Authenticode 签名信息

### 5.3. SignerInfo 类型

每个签名者的信息以 SignerInfo 类型表示：

```
SignerInfo ::= SEQUENCE {
  version CMSVersion,
  sid SignerIdentifier,
  digestAlgorithm DigestAlgorithmIdentifier,
  signedAttrs [0] IMPLICIT SignedAttributes OPTIONAL,
  signatureAlgorithm SignatureAlgorithmIdentifier,
  signature SignatureValue,
  unsignedAttrs [1] IMPLICIT UnsignedAttributes OPTIONAL }

SignerIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier }

SignedAttributes ::= SET SIZE (1..MAX) OF Attribute

UnsignedAttributes ::= SET SIZE (1..MAX) OF Attribute

Attribute ::= SEQUENCE {
  attrType OBJECT IDENTIFIER,
  attrValues SET OF AttributeValue }

AttributeValue ::= ANY

SignatureValue ::= OCTET STRING
```

SignerInfo 类型的字段含义如下：

- **version**：语法版本号。如果 SignerIdentifier 是 CHOICE issuerAndSerialNumber，则版本 MUST 为 1。如果 SignerIdentifier 是 subjectKeyIdentifier，则版本 MUST 为 3。

- **sid**：指定签名者的证书（从而指定签名者的公钥）。签名者的公钥被接收方用于验证签名。SignerIdentifier 提供了两种指定签名者公钥的替代方式。issuerAndSerialNumber 替代方式通过颁发者的可辨别名称和证书序列号标识签名者的证书；subjectKeyIdentifier 通过密钥标识符标识签名者的证书。当引用 X.509 证书时，密钥标识符与 X.509 subjectKeyIdentifier 扩展值匹配。当引用其他证书格式时，指定证书格式及其在 CMS 中使用的文档必须包含将密钥标识符匹配到适当证书字段的详细信息。实现 MUST 支持接收 SignerIdentifier 的 issuerAndSerialNumber 和 subjectKeyIdentifier 形式。在生成 SignerIdentifier 时，实现 MAY 支持其中一种形式（issuerAndSerialNumber 或 subjectKeyIdentifier）并始终使用它，或实现 MAY 任意混合两种形式。但是，subjectKeyIdentifier MUST 用于引用包含在非 X.509 证书中的公钥。

- **digestAlgorithm**：标识签名者使用的消息摘要算法及任何关联参数。消息摘要对被签名的内容或内容与签名属性一起计算，使用第 5.4 节描述的过程。消息摘要算法 SHOULD 在关联的 SignedData 的 digestAlgorithms 字段中列出。实现 MAY 无法验证使用未包含在 SignedData digestAlgorithms 集合中的摘要算法的签名。

- **signedAttrs**：已签名属性的集合。该字段是可选的，但如果被签名的 EncapsulatedContentInfo 值的内容类型不是 id-data，则该字段 MUST 存在。SignedAttributes MUST 进行 DER 编码，即使结构的其余部分是 BER 编码。有用的属性类型（如签名时间）在第 11 节中定义。如果该字段存在，它 MUST 至少包含以下两个属性：
  - 一个 **content-type 属性**，其值为被签名的 EncapsulatedContentInfo 值的内容类型。第 11.1 节定义了 content-type 属性。但是，content-type 属性 MUST NOT 作为第 11.4 节中定义的副签名未签名属性的一部分使用。
  - 一个 **message-digest 属性**，其值为内容的消息摘要。第 11.2 节定义了 message-digest 属性。

- **signatureAlgorithm**：标识签名者用于生成[[数字签名]]的签名算法及任何关联参数。

- **signature**：[[数字签名]]生成的结果，使用消息摘要和签名者的私钥。签名的详细信息取决于所使用的签名算法。

- **unsignedAttrs**：未签名属性的集合。该字段是可选的。有用的属性类型（如副签名）在第 11 节中定义。

SignedAttribute 和 UnsignedAttribute 类型的字段含义如下：

- **attrType**：指示属性的类型。它是一个对象标识符。
- **attrValues**：构成属性的值集合。集合中每个值的类型可以由 attrType 唯一确定。attrType 可以对集合中的项数施加限制。

### 5.4. 消息摘要计算过程

消息摘要计算过程对被签名的内容或内容与签名属性一起计算消息摘要。无论哪种情况，消息摘要计算过程的初始输入是被签名的封装内容的"值"。具体而言，初始输入是应用签名过程的 encapContentInfo eContent OCTET STRING。只有组成 eContent OCTET STRING 值的八位节被输入到消息摘要算法，不包括标签或长度八位字节。

消息摘要计算过程的结果取决于 signedAttrs 字段是否存在。当该字段不存在时，结果就是上述内容的消息摘要。当该字段存在时，结果是对 signedAttrs 字段中包含的 SignedAttrs 值的完整 DER 编码的消息摘要。由于 SignedAttrs 值（当存在时）必须包含 content-type 和 message-digest 属性，这些值被间接包含在结果中。content-type 属性 MUST NOT 包含在第 11.4 节定义的副签名未签名属性中。为消息摘要计算执行 signedAttrs 字段的单独编码。signedAttrs 中的 IMPLICIT [0] 标签不用于 DER 编码，而是使用 EXPLICIT SET OF 标签。也就是说，EXPLICIT SET OF 标签（而不是 IMPLICIT [0] 标签）的 DER 编码 MUST 包含在消息摘要计算中，连同 SignedAttributes 值的长度和内容八位字节。

当 signedAttrs 字段不存在时，只有组成 SignedData encapContentInfo eContent OCTET STRING 值的八位字节（例如，文件的内容）被输入到消息摘要计算中。这有一个优点：在签名生成过程之前不需要知道被签名内容的长度。

虽然 encapContentInfo eContent OCTET STRING 标签和长度八位字节不包括在消息摘要计算中，但它们通过其他方式受到保护。长度八位字节受消息摘要算法性质的保护，因为在计算上不可能找到任何两个具有相同消息摘要的不同长度的不同消息内容。

### 5.5. 签名生成过程

签名生成过程的输入包括消息摘要计算过程的结果和签名者的私钥。签名生成的详细信息取决于所使用的签名算法。指定签名者使用的签名算法的对象标识符及任何参数携带在 signatureAlgorithm 字段中。签名者生成的签名值 MUST 编码为 OCTET STRING 并携带在 signature 字段中。

### 5.6. 签名验证过程

签名验证过程的输入包括消息摘要计算过程的结果和签名者的公钥。接收方 MAY 通过任何方式获取签名者的正确公钥，但首选方法是从 SignedData certificates 字段获取的证书。签名者公钥的选择和验证 MAY 基于认证路径验证（参见 [PROFILE]）以及其他外部上下文，但超出了本文档的范围。签名验证的详细信息取决于所使用的签名算法。

接收方 MUST NOT 依赖发起方计算的任何消息摘要值。如果 SignedData signerInfo 包含 signedAttributes，则内容消息摘要 MUST 按第 5.4 节所述计算。要使签名有效，接收方计算的消息摘要值 MUST 与 SignedData signerInfo 的 signedAttributes 中包含的 messageDigest 属性值相同。

如果 SignedData signerInfo 包含 signedAttributes，则 content-type 属性值 MUST 与 SignedData encapContentInfo eContentType 值匹配。

## 6. 信封数据内容类型 (Enveloped-data)

信封数据内容类型由任意类型的加密内容和一个或多个接收方的加密内容加密密钥组成。加密内容和一个接收方的加密内容加密密钥的组合是该接收方的"数字信封"（digital envelope）。任意类型的内容都可以使用支持的[[密钥管理]]技术为任意数量的接收方进行信封封装。

信封数据内容类型的典型应用是表示一个或多个接收方对 data 或 signed-data 内容类型内容的数字信封。

信封数据通过以下步骤构造：

1. 为特定的内容加密算法随机生成一个内容加密密钥。
2. 为每个接收方加密内容加密密钥。此加密的详细信息取决于所使用的[[密钥管理]]算法，但支持四种通用技术：
   - **密钥传输（key transport）**：内容加密密钥使用接收方的公钥加密。
   - **密钥协商（key agreement）**：使用接收方的公钥和发送方的私钥生成成对对称密钥，然后使用该成对对称密钥加密内容加密密钥。
   - **对称密钥加密密钥**：内容加密密钥使用先前分发的对称密钥加密密钥加密。
   - **密码（passwords）**：内容加密密钥使用从密码或其他共享秘密值派生的密钥加密密钥加密。
3. 对于每个接收方，将加密的内容加密密钥和其他接收方特定信息收集到 RecipientInfo 值中（在第 6.2 节中定义）。
4. 使用内容加密密钥加密内容。内容加密可能需要将内容填充到某个块大小的倍数；参见第 6.3 节。
5. 所有接收方的 RecipientInfo 值与加密内容一起收集形成 EnvelopedData 值（在第 6.1 节中定义）。

接收方通过解密一个加密的内容加密密钥来打开数字信封，然后使用恢复的内容加密密钥解密加密内容。

本节分为四个部分。第一部分描述顶层类型 EnvelopedData，第二部分描述每个接收方的信息类型 RecipientInfo，第三和第四部分描述内容加密和密钥加密过程。

### 6.1. EnvelopedData 类型

以下对象标识符标识信封数据内容类型：

```
id-envelopedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 3 }
```

信封数据内容类型应具有 [[ASN.1]] 类型 EnvelopedData：

```
EnvelopedData ::= SEQUENCE {
  version CMSVersion,
  originatorInfo [0] IMPLICIT OriginatorInfo OPTIONAL,
  recipientInfos RecipientInfos,
  encryptedContentInfo EncryptedContentInfo,
  unprotectedAttrs [1] IMPLICIT UnprotectedAttributes OPTIONAL }

OriginatorInfo ::= SEQUENCE {
  certs [0] IMPLICIT CertificateSet OPTIONAL,
  crls [1] IMPLICIT RevocationInfoChoices OPTIONAL }

RecipientInfos ::= SET SIZE (1..MAX) OF RecipientInfo

EncryptedContentInfo ::= SEQUENCE {
  contentType ContentType,
  contentEncryptionAlgorithm ContentEncryptionAlgorithmIdentifier,
  encryptedContent [0] IMPLICIT EncryptedContent OPTIONAL }

EncryptedContent ::= OCTET STRING

UnprotectedAttributes ::= SET SIZE (1..MAX) OF Attribute
```

EnvelopedData 类型的字段含义如下：

- **version**：语法版本号。适当的值取决于 originatorInfo、RecipientInfo 和 unprotectedAttrs。版本 MUST 按如下方式分配：
  - IF（originatorInfo 存在）AND（（任何类型为 other 的证书存在）OR（任何类型为 other 的 crl 存在））THEN version 为 4
  - ELSE IF（（originatorInfo 存在 AND 任何版本 2 属性证书存在））OR（任何 RecipientInfo 结构包含 pwri）OR（任何 RecipientInfo 结构包含 ori）THEN version 为 3
  - ELSE IF（originatorInfo 不存在）AND（unprotectedAttrs 不存在）AND（所有 RecipientInfo 结构为版本 0）THEN version 为 0
  - ELSE version 为 2

- **originatorInfo**：可选地提供关于发起方的信息。仅在[[密钥管理]]算法要求时存在。它 MAY 包含证书和 CRL：
  - **certs**：证书的集合。certs MAY 包含与多种不同[[密钥管理]]算法关联的发起方证书。certs MAY 还包含与发起方关联的属性证书。certs 中包含的证书应足以让所有接收方从认可的"根"或"顶级认证机构"构建认证路径。但是，certs MAY 包含多于必要的证书，也 MAY 包含足以从两个或更多独立顶级认证机构构建认证路径的证书。或者，如果预期接收方有其他方式获取必要的证书，certs MAY 包含少于必要的证书。
  - **crls**：CRL 的集合。该集合应包含足够的信息以确定 certs 字段中的证书是否有效，但不需要完全对应。CRL MAY 多于必要的数量，也 MAY 少于必要的数量。

- **recipientInfos**：每个接收方信息的集合。集合中 MUST 至少有一个元素。

- **encryptedContentInfo**：加密内容信息。

- **unprotectedAttrs**：未加密属性的集合。该字段是可选的。有用的属性类型在第 11 节中定义。

EncryptedContentInfo 类型的字段含义如下：

- **contentType**：指示内容类型。
- **contentEncryptionAlgorithm**：标识用于加密内容的内容加密算法及任何关联参数。内容加密过程在第 6.3 节中描述。所有接收方使用相同的内容加密算法和内容加密密钥。
- **encryptedContent**：加密内容的结果。该字段是可选的，如果字段不存在，其预期值必须通过其他方式提供。

recipientInfos 字段位于 encryptedContentInfo 字段之前，以便 EnvelopedData 值可以在单遍中处理。

### 6.2. RecipientInfo 类型

每个接收方的信息以 RecipientInfo 类型表示。RecipientInfo 对每种支持的[[密钥管理]]技术有不同的格式。每种[[密钥管理]]技术都可以用于同一加密内容的每个接收方。在所有情况下，加密的内容加密密钥被传输给一个或多个接收方。

由于并非所有实现都支持每种可能的[[密钥管理]]算法，所有实现 MUST 在遇到未实现的算法时优雅地处理。例如，如果接收方收到使用 RSA-OAEP（Optimal Asymmetric Encryption Padding，最优非[[对称加密]]填充）在 RSA 公钥中加密的内容加密密钥，而实现仅支持 RSA PKCS #1 v1.5，则必须实现优雅的失败。

实现 MUST 支持密钥传输、密钥协商和预分发的对称密钥加密密钥，分别由 ktri、kari 和 kekri 表示。实现 MAY 支持基于密码的[[密钥管理]]（由 pwri 表示）。实现 MAY 支持任何其他[[密钥管理]]技术（由 ori 表示）。由于每个接收方可以使用不同的[[密钥管理]]技术，且未来的规范可能定义额外的[[密钥管理]]技术，所有实现 MUST 优雅地处理 RecipientInfo CHOICE 中未实现的替代方案，所有实现 MUST 优雅地处理 RecipientInfo CHOICE 中其他方面已支持的替代方案的未实现版本，所有实现 MUST 优雅地处理未实现或未知的 ori 替代方案。

```
RecipientInfo ::= CHOICE {
  ktri KeyTransRecipientInfo,
  kari [1] KeyAgreeRecipientInfo,
  kekri [2] KEKRecipientInfo,
  pwri [3] PasswordRecipientinfo,
  ori [4] OtherRecipientInfo }

EncryptedKey ::= OCTET STRING
```

#### 6.2.1. KeyTransRecipientInfo 类型

使用密钥传输的每个接收方信息以 KeyTransRecipientInfo 类型表示。KeyTransRecipientInfo 的每个实例将内容加密密钥传输给一个接收方。

```
KeyTransRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 0 or 2
  rid RecipientIdentifier,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }

RecipientIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier }
```

KeyTransRecipientInfo 类型的字段含义如下：

- **version**：语法版本号。如果 RecipientIdentifier 是 CHOICE issuerAndSerialNumber，则版本 MUST 为 0。如果 RecipientIdentifier 是 subjectKeyIdentifier，则版本 MUST 为 2。

- **rid**：指定发送方用于保护内容加密密钥的接收方证书或密钥。内容加密密钥使用接收方的公钥加密。RecipientIdentifier 提供了两种指定接收方证书（从而指定接收方公钥）的替代方式。接收方的证书必须包含密钥传输公钥。因此，包含密钥用途扩展的接收方 X.509 版本 3 证书 MUST 断言 keyEncipherment 位。issuerAndSerialNumber 替代方式通过颁发者的可辨别名称和证书序列号标识接收方的证书；subjectKeyIdentifier 通过密钥标识符标识接收方的证书。当引用 X.509 证书时，密钥标识符与 X.509 subjectKeyIdentifier 扩展值匹配。当引用其他证书格式时，指定证书格式及其在 CMS 中使用的文档必须包含将密钥标识符匹配到适当证书字段的详细信息。对于接收方处理，实现 MUST 支持这两种指定接收方证书的替代方式。对于发送方处理，实现 MUST 支持至少其中一种替代方式。

- **keyEncryptionAlgorithm**：标识用于为接收方加密内容加密密钥的密钥加密算法及任何关联参数。密钥加密过程在第 6.4 节中描述。

- **encryptedKey**：为接收方加密内容加密密钥的结果。

#### 6.2.2. KeyAgreeRecipientInfo 类型

使用密钥协商的接收方信息以 KeyAgreeRecipientInfo 类型表示。KeyAgreeRecipientInfo 的每个实例将内容加密密钥传输给一个或多个使用相同密钥协商算法和该算法域参数的接收方。

```
KeyAgreeRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 3
  originator [0] EXPLICIT OriginatorIdentifierOrKey,
  ukm [1] EXPLICIT UserKeyingMaterial OPTIONAL,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  recipientEncryptedKeys RecipientEncryptedKeys }

OriginatorIdentifierOrKey ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier,
  originatorKey [1] OriginatorPublicKey }

OriginatorPublicKey ::= SEQUENCE {
  algorithm AlgorithmIdentifier,
  publicKey BIT STRING }

RecipientEncryptedKeys ::= SEQUENCE OF RecipientEncryptedKey

RecipientEncryptedKey ::= SEQUENCE {
  rid KeyAgreeRecipientIdentifier,
  encryptedKey EncryptedKey }

KeyAgreeRecipientIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  rKeyId [0] IMPLICIT RecipientKeyIdentifier }

RecipientKeyIdentifier ::= SEQUENCE {
  subjectKeyIdentifier SubjectKeyIdentifier,
  date GeneralizedTime OPTIONAL,
  other OtherKeyAttribute OPTIONAL }

SubjectKeyIdentifier ::= OCTET STRING
```

KeyAgreeRecipientInfo 类型的字段含义如下：

- **version**：语法版本号。MUST 始终为 3。

- **originator**：一个具有三种替代方式的 CHOICE，指定发送方的密钥协商公钥。发送方使用相应的私钥和接收方的公钥生成成对密钥。内容加密密钥使用该成对密钥加密。issuerAndSerialNumber 替代方式通过颁发者的可辨别名称和证书序列号标识发送方的证书（从而标识发送方的公钥）。subjectKeyIdentifier 替代方式通过密钥标识符标识发送方的证书。当引用 X.509 证书时，密钥标识符与 X.509 subjectKeyIdentifier 扩展值匹配。当引用其他证书格式时，指定证书格式及其在 CMS 中使用的文档必须包含将密钥标识符匹配到适当证书字段的详细信息。originatorKey 替代方式包括算法标识符和发送方的密钥协商公钥。此替代方式允许发起方匿名，因为公钥未经过认证。实现 MUST 支持所有三种指定发送方公钥的替代方式。

- **ukm**：可选。对于某些密钥协商算法，发送方提供用户密钥材料（User Keying Material，UKM）以确保每次相同的两方生成成对密钥时生成不同的密钥。实现 MUST 接受包含 ukm 字段的 KeyAgreeRecipientInfo SEQUENCE。不支持使用 UKM 的密钥协商算法的实现 MUST 优雅地处理 UKM 的存在。

- **keyEncryptionAlgorithm**：标识用于使用密钥加密密钥加密内容加密密钥的密钥加密算法及任何关联参数。密钥加密过程在第 6.4 节中描述。

- **recipientEncryptedKeys**：包含一个或多个接收方的接收方标识符和加密密钥。KeyAgreeRecipientIdentifier 是一个具有两种替代方式的 CHOICE，指定发送方用于生成成对密钥加密密钥的接收方证书（从而指定接收方的公钥）。接收方的证书必须包含密钥协商公钥。因此，包含密钥用途扩展的接收方 X.509 版本 3 证书 MUST 断言 keyAgreement 位。内容加密密钥使用成对密钥加密密钥加密。issuerAndSerialNumber 替代方式通过颁发者的可辨别名称和证书序列号标识接收方的证书；RecipientKeyIdentifier 如下所述。encryptedKey 是使用密钥协商算法生成的成对密钥加密密钥加密内容加密密钥的结果。实现 MUST 支持这两种指定接收方证书的替代方式。

RecipientKeyIdentifier 类型的字段含义如下：

- **subjectKeyIdentifier**：通过密钥标识符标识接收方的证书。当引用 X.509 证书时，密钥标识符与 X.509 subjectKeyIdentifier 扩展值匹配。当引用其他证书格式时，指定证书格式及其在 CMS 中使用的文档必须包含将密钥标识符匹配到适当证书字段的详细信息。
- **date**：可选。当存在时，date 指定发送方使用的接收方先前分发的 UKM。
- **other**：可选。当存在时，此字段包含接收方用于定位发送方使用的公钥材料的附加信息。

#### 6.2.3. KEKRecipientInfo 类型

使用预分发对称密钥的接收方信息以 KEKRecipientInfo 类型表示。KEKRecipientInfo 的每个实例将内容加密密钥传输给一个或多个拥有预分发密钥加密密钥的接收方。

```
KEKRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 4
  kekid KEKIdentifier,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }

KEKIdentifier ::= SEQUENCE {
  keyIdentifier OCTET STRING,
  date GeneralizedTime OPTIONAL,
  other OtherKeyAttribute OPTIONAL }
```

KEKRecipientInfo 类型的字段含义如下：

- **version**：语法版本号。MUST 始终为 4。
- **kekid**：指定先前分发给发送方和一个或多个接收方的对称密钥加密密钥。
- **keyEncryptionAlgorithm**：标识用于使用密钥加密密钥加密内容加密密钥的密钥加密算法及任何关联参数。密钥加密过程在第 6.4 节中描述。
- **encryptedKey**：使用密钥加密密钥加密内容加密密钥的结果。

KEKIdentifier 类型的字段含义如下：

- **keyIdentifier**：标识先前分发给发送方和一个或多个接收方的密钥加密密钥。
- **date**：可选。当存在时，date 指定先前分发的密钥集中的一把密钥加密密钥。
- **other**：可选。当存在时，此字段包含接收方用于确定发送方使用的密钥加密密钥的附加信息。

#### 6.2.4. PasswordRecipientInfo 类型

使用密码或共享秘密值的接收方信息以 PasswordRecipientInfo 类型表示。PasswordRecipientInfo 的每个实例将内容加密密钥传输给一个或多个拥有密码或共享秘密值的接收方。

PasswordRecipientInfo 类型在 RFC 3211 [PWRI] 中指定。此处重复 PasswordRecipientInfo 结构以确保完整性。

```
PasswordRecipientInfo ::= SEQUENCE {
  version CMSVersion,   -- Always set to 0
  keyDerivationAlgorithm [0] KeyDerivationAlgorithmIdentifier
                               OPTIONAL,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }
```

PasswordRecipientInfo 类型的字段含义如下：

- **version**：语法版本号。MUST 始终为 0。
- **keyDerivationAlgorithm**：标识用于从密码或共享秘密值派生密钥加密密钥的密钥派生算法及任何关联参数。如果此字段不存在，密钥加密密钥由外部源提供，例如硬件加密令牌（如智能卡）。
- **keyEncryptionAlgorithm**：标识用于使用密钥加密密钥加密内容加密密钥的加密算法及任何关联参数。
- **encryptedKey**：使用密钥加密密钥加密内容加密密钥的结果。

#### 6.2.5. OtherRecipientInfo 类型

用于额外[[密钥管理]]技术的接收方信息以 OtherRecipientInfo 类型表示。OtherRecipientInfo 类型允许在未来的文档中指定超越密钥传输、密钥协商、预分发对称密钥加密密钥和基于密码的[[密钥管理]]的[[密钥管理]]技术。对象标识符唯一标识此类[[密钥管理]]技术。

```
OtherRecipientInfo ::= SEQUENCE {
  oriType OBJECT IDENTIFIER,
  oriValue ANY DEFINED BY oriType }
```

OtherRecipientInfo 类型的字段含义如下：

- **oriType**：标识[[密钥管理]]技术。
- **oriValue**：包含使用已标识[[密钥管理]]技术的接收方所需的协议数据元素。

### 6.3. 内容加密过程

为所需的内容加密算法随机生成内容加密密钥。待保护的数据按如下描述进行填充，然后使用内容加密密钥加密填充后的数据。加密操作在内容加密密钥的控制下将任意八位字节字符串（数据）映射到另一个八位字节字符串（密文）。加密数据包含在 EnvelopedData encryptedContentInfo encryptedContent OCTET STRING 中。

某些内容加密算法假定输入长度是 k 个八位字节的倍数，其中 k 大于 1。对于此类算法，输入应在尾部填充 `k-(lth mod k)` 个值均为 `k-(lth mod k)` 的八位字节，其中 lth 是输入的长度。换句话说，输入在尾部填充以下字符串之一：

```
              01 -- if lth mod k = k-1
           02 02 -- if lth mod k = k-2
               .
               .
               .
     k k ... k k -- if lth mod k = 0
```

填充可以被无歧义地移除，因为所有输入都被填充，包括已经是块大小倍数的输入值，且没有填充字符串是另一个的后缀。此填充方法仅在 k 小于 256 时有良好定义。

### 6.4. 密钥加密过程

密钥加密过程的输入——提供给接收方密钥加密算法的值——就是内容加密密钥的"值"。

上述任何[[密钥管理]]技术都可以用于同一加密内容的每个接收方。

## 7. 摘要数据内容类型 (Digested-data)

摘要数据内容类型由任意类型的内容和内容的消息摘要组成。

通常，摘要数据内容类型用于提供内容完整性，其结果通常成为 enveloped-data 内容类型的输入。

构造摘要数据的步骤如下：

1. 使用消息摘要算法计算内容的消息摘要。
2. 将消息摘要算法和消息摘要与内容一起收集到 DigestedData 值中。

接收方通过将消息摘要与独立计算的消息摘要进行比较来验证消息摘要。

以下对象标识符标识摘要数据内容类型：

```
id-digestedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 5 }
```

摘要数据内容类型应具有 [[ASN.1]] 类型 DigestedData：

```
DigestedData ::= SEQUENCE {
  version CMSVersion,
  digestAlgorithm DigestAlgorithmIdentifier,
  encapContentInfo EncapsulatedContentInfo,
  digest Digest }

Digest ::= OCTET STRING
```

DigestedData 类型的字段含义如下：

- **version**：语法版本号。如果封装内容类型为 id-data，则 version 的值 MUST 为 0；如果封装内容类型不是 id-data，则 version 的值 MUST 为 2。
- **digestAlgorithm**：标识计算内容摘要所使用的消息摘要算法及任何关联参数。当没有签名属性时，消息摘要过程与第 5.4 节中的相同。
- **encapContentInfo**：被摘要的内容，如第 5.2 节所定义。
- **digest**：消息摘要过程的结果。

digestAlgorithm 字段、encapContentInfo 字段和 digest 字段的排序使得可以在单遍中处理 DigestedData 值。

## 8. 加密数据内容类型 (Encrypted-data)

加密数据内容类型由任意类型的加密内容组成。与 enveloped-data 内容类型不同，加密数据内容类型既没有接收方也没有加密的内容加密密钥。密钥必须通过其他方式管理。

加密数据内容类型的典型应用是加密 data 内容类型的内容以进行本地存储，可能加密密钥是从密码派生的。

以下对象标识符标识加密数据内容类型：

```
id-encryptedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 6 }
```

加密数据内容类型应具有 [[ASN.1]] 类型 EncryptedData：

```
EncryptedData ::= SEQUENCE {
  version CMSVersion,
  encryptedContentInfo EncryptedContentInfo,
  unprotectedAttrs [1] IMPLICIT UnprotectedAttributes OPTIONAL }
```

EncryptedData 类型的字段含义如下：

- **version**：语法版本号。如果 unprotectedAttrs 存在，则 version MUST 为 2。如果 unprotectedAttrs 不存在，则 version MUST 为 0。
- **encryptedContentInfo**：加密内容信息，如第 6.1 节所定义。
- **unprotectedAttrs**：未加密属性的集合。该字段是可选的。有用的属性类型在第 11 节中定义。

## 9. 认证数据内容类型 (Authenticated-data)

认证数据内容类型由任意类型的内容、消息认证码（MAC，Message Authentication Code）和一个或多个接收方的加密认证密钥组成。MAC 和一个接收方的加密认证密钥的组合是该接收方验证内容完整性所必需的。任意类型的内容都可以为任意数量的接收方进行完整性保护。

构造认证数据的过程涉及以下步骤：

1. 为特定的消息认证算法随机生成消息认证密钥。
2. 为每个接收方加密消息认证密钥。此加密的详细信息取决于所使用的[[密钥管理]]算法。
3. 对于每个接收方，将加密的消息认证密钥和其他接收方特定信息收集到 RecipientInfo 值中（在第 6.2 节中定义）。
4. 使用消息认证密钥，发起方计算内容的 MAC 值。如果发起方正在认证内容以外的附加信息（参见第 9.2 节），则计算内容的消息摘要，内容的消息摘要和其他信息使用消息认证密钥进行认证，结果即为"MAC 值"。

### 9.1. AuthenticatedData 类型

以下对象标识符标识认证数据内容类型：

```
id-ct-authData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
   us(840) rsadsi(113549) pkcs(1) pkcs-9(9) smime(16)
   ct(1) 2 }
```

认证数据内容类型应具有 [[ASN.1]] 类型 AuthenticatedData：

```
AuthenticatedData ::= SEQUENCE {
  version CMSVersion,
  originatorInfo [0] IMPLICIT OriginatorInfo OPTIONAL,
  recipientInfos RecipientInfos,
  macAlgorithm MessageAuthenticationCodeAlgorithm,
  digestAlgorithm [1] DigestAlgorithmIdentifier OPTIONAL,
  encapContentInfo EncapsulatedContentInfo,
  authAttrs [2] IMPLICIT AuthAttributes OPTIONAL,
  mac MessageAuthenticationCode,
  unauthAttrs [3] IMPLICIT UnauthAttributes OPTIONAL }

AuthAttributes ::= SET SIZE (1..MAX) OF Attribute

UnauthAttributes ::= SET SIZE (1..MAX) OF Attribute

MessageAuthenticationCode ::= OCTET STRING
```

AuthenticatedData 类型的字段含义如下：

- **version**：语法版本号。版本 MUST 按如下方式分配：
  - IF（originatorInfo 存在）AND（（任何类型为 other 的证书存在）OR（任何类型为 other 的 crl 存在））THEN version 为 3
  - ELSE IF（originatorInfo 存在 AND 任何版本 2 属性证书存在）THEN version 为 1
  - ELSE version 为 0

- **originatorInfo**：可选地提供关于发起方的信息。仅在[[密钥管理]]算法要求时存在。它 MAY 包含证书、属性证书和 CRL，如第 6.1 节所定义。

- **recipientInfos**：每个接收方信息的集合，如第 6.1 节所定义。集合中 MUST 至少有一个元素。

- **macAlgorithm**：消息认证码（MAC）算法标识符。它标识发起方使用的 MAC 算法及任何关联参数。macAlgorithm 字段的位置便于接收方进行单遍处理。

- **digestAlgorithm**：标识在存在认证属性时用于计算封装内容消息摘要的消息摘要算法及任何关联参数。消息摘要过程在第 9.2 节中描述。digestAlgorithm 字段的位置便于接收方进行单遍处理。如果 digestAlgorithm 字段存在，则 authAttrs 字段 MUST 也存在。

- **encapContentInfo**：被认证的内容，如第 5.2 节所定义。

- **authAttrs**：认证属性的集合。authAttrs 结构是可选的，但如果被认证的 EncapsulatedContentInfo 值的内容类型不是 id-data，则 MUST 存在。如果 authAttrs 字段存在，则 digestAlgorithm 字段 MUST 也存在。AuthAttributes 结构 MUST 进行 DER 编码，即使结构的其余部分是 BER 编码。有用的属性类型在第 11 节中定义。如果 authAttrs 字段存在，它 MUST 至少包含以下两个属性：
  - 一个 **content-type 属性**，其值为被认证的 EncapsulatedContentInfo 值的内容类型。第 11.1 节定义了 content-type 属性。
  - 一个 **message-digest 属性**，其值为内容的消息摘要。第 11.2 节定义了 message-digest 属性。

- **mac**：消息认证码。

- **unauthAttrs**：未认证属性的集合。该字段是可选的。目前尚未定义用于未认证属性的属性，但其他有用的属性类型在第 11 节中定义。

### 9.2. MAC 生成

MAC 计算过程对被认证的内容或被认证内容的消息摘要与发起方的认证属性一起计算消息认证码（MAC）。

如果 authAttrs 字段不存在，MAC 计算过程的输入是 encapContentInfo eContent OCTET STRING 的值。只有组成 eContent OCTET STRING 值的八位字节被输入到 MAC 算法；标签和长度八位字节被省略。这有一个优点：在 MAC 生成过程之前不需要知道被认证内容的长度。

如果 authAttrs 字段存在，MUST 包含 content-type 属性（如第 11.1 节所述）和 message-digest 属性（如第 11.2 节所述），MAC 计算过程的输入是 authAttrs 的 DER 编码。为消息摘要计算执行 authAttrs 字段的单独编码。authAttrs 字段中的 IMPLICIT [2] 标签不用于 DER 编码，而是使用 EXPLICIT SET OF 标签。也就是说，SET OF 标签（而不是 IMPLICIT [2] 标签）的 DER 编码应包含在消息摘要计算中，连同 authAttrs 值的长度和内容八位字节。

消息摘要计算过程对被认证的内容计算消息摘要。消息摘要计算过程的初始输入是被认证的封装内容的"值"。具体而言，输入是应用认证过程的 encapContentInfo eContent OCTET STRING。只有组成 encapContentInfo eContent OCTET STRING 值的八位字节被输入到消息摘要算法，不包括标签或长度八位字节。这有一个优点：不需要事先知道被认证内容的长度。虽然 encapContentInfo eContent OCTET STRING 标签和长度八位字节不包括在消息摘要计算中，但它们仍通过其他方式受到保护。长度八位字节受消息摘要算法性质的保护，因为在计算上不可能找到任何两个具有相同消息摘要的不同长度的不同内容。

MAC 计算过程的输入包括上述定义的 MAC 输入数据和 recipientInfo 结构中携带的认证密钥。MAC 计算的详细信息取决于所使用的 MAC 算法（例如 HMAC，Hashed Message Authentication Code）。指定发起方使用的 MAC 算法的对象标识符及任何参数携带在 macAlgorithm 字段中。发起方生成的 MAC 值编码为 OCTET STRING 并携带在 mac 字段中。

### 9.3. MAC 验证

MAC 验证过程的输入包括输入数据（基于 authAttrs 字段的存在与否确定，如第 9.2 节所定义）和 recipientInfo 中携带的认证密钥。MAC 验证过程的详细信息取决于所使用的 MAC 算法。

接收方 MUST NOT 依赖发起方计算的任何 MAC 值或消息摘要值。内容按第 9.2 节所述进行认证。如果发起方包含认证属性，则 authAttrs 的内容按第 9.2 节所述进行认证。要使认证成功，接收方计算的 MAC 值 MUST 与 mac 字段的值相同。类似地，当 authAttrs 字段存在时要使认证成功，接收方计算的内容消息摘要值 MUST 与 authAttrs 中 message-digest 属性中包含的消息摘要值相同。

如果 AuthenticatedData 包含 authAttrs，则 content-type 属性值 MUST 与 AuthenticatedData encapContentInfo eContentType 值匹配。

## 10. 有用类型

本节分为两个部分。第一部分定义算法标识符，第二部分定义其他有用类型。

### 10.1. 算法标识符类型

所有算法标识符都具有相同的类型：AlgorithmIdentifier。AlgorithmIdentifier 的定义取自 X.509 [X.509-88]。

每种算法类型都有许多替代方案。

#### 10.1.1. DigestAlgorithmIdentifier

DigestAlgorithmIdentifier 类型标识消息摘要算法。示例包括 SHA-1、MD2 和 MD5。消息摘要算法将八位字节字符串（内容）映射到另一个八位字节字符串（消息摘要）。

```
DigestAlgorithmIdentifier ::= AlgorithmIdentifier
```

#### 10.1.2. SignatureAlgorithmIdentifier

SignatureAlgorithmIdentifier 类型标识签名算法，它也可以标识消息摘要算法。示例包括 RSA、DSA、DSA with SHA-1、ECDSA 和 ECDSA with SHA-256。签名算法支持签名生成和验证操作。签名生成操作使用消息摘要和签名者的私钥生成签名值。签名验证操作使用消息摘要和签名者的公钥确定签名值是否有效。上下文确定预期哪种操作。

```
SignatureAlgorithmIdentifier ::= AlgorithmIdentifier
```

#### 10.1.3. KeyEncryptionAlgorithmIdentifier

KeyEncryptionAlgorithmIdentifier 类型标识用于加密内容加密密钥的密钥加密算法。加密操作在密钥加密密钥的控制下将八位字节字符串（密钥）映射到另一个八位字节字符串（加密密钥）。解密操作是加密操作的逆操作。上下文确定预期哪种操作。

加密和解密的详细信息取决于所使用的[[密钥管理]]算法。支持密钥传输、密钥协商、预分发的对称密钥加密密钥和从密码派生的对称密钥加密密钥。

```
KeyEncryptionAlgorithmIdentifier ::= AlgorithmIdentifier
```

#### 10.1.4. ContentEncryptionAlgorithmIdentifier

ContentEncryptionAlgorithmIdentifier 类型标识内容加密算法。示例包括 Triple-DES 和 RC2。内容加密算法支持加密和解密操作。加密操作在内容加密密钥的控制下将八位字节字符串（明文）映射到另一个八位字节字符串（密文）。解密操作是加密操作的逆操作。上下文确定预期哪种操作。

```
ContentEncryptionAlgorithmIdentifier ::= AlgorithmIdentifier
```

#### 10.1.5. MessageAuthenticationCodeAlgorithm

MessageAuthenticationCodeAlgorithm 类型标识消息认证码（MAC）算法。示例包括 DES-MAC 和 HMAC-SHA-1。MAC 算法支持生成和验证操作。MAC 生成和验证操作使用相同的对称密钥。上下文确定预期哪种操作。

```
MessageAuthenticationCodeAlgorithm ::= AlgorithmIdentifier
```

#### 10.1.6. KeyDerivationAlgorithmIdentifier

KeyDerivationAlgorithmIdentifier 类型在 RFC 3211 [PWRI] 中指定。此处重复 KeyDerivationAlgorithmIdentifier 定义以确保完整性。

密钥派生算法将密码或共享秘密值转换为密钥加密密钥。

```
KeyDerivationAlgorithmIdentifier ::= AlgorithmIdentifier
```

### 10.2. 其他有用类型

本节定义文档其他地方使用的类型。类型不按任何特定顺序列出。

#### 10.2.1. RevocationInfoChoices

RevocationInfoChoices 类型提供一组撤销状态信息替代方案。该集合应包含足够的信息以确定与之关联的证书和属性证书是否被撤销。但是，撤销状态信息 MAY 多于必要的数量，也 MAY 少于必要的数量。X.509 证书撤销列表（CRL）[X.509-97] 是撤销状态信息的主要来源，但可以支持任何其他撤销信息格式。提供 OtherRevocationInfoFormat 替代方案以支持任何其他撤销信息格式而无需进一步修改 CMS。例如，[[在线证书状态协议]]（OCSP，Online Certificate Status Protocol）响应 [OCSP] 可以使用 OtherRevocationInfoFormat 支持。

CertificateList 可以包含 CRL、机构撤销列表（ARL，Authority Revocation List）、增量 CRL（Delta CRL）或属性证书撤销列表。所有这些列表共享通用语法。

CertificateList 类型提供证书撤销列表（CRL）。CRL 在 X.509 [X.509-97] 中指定，并在 RFC 5280 [PROFILE] 中为互联网使用进行了配置。

CertificateList 的定义取自 X.509。

```
RevocationInfoChoices ::= SET OF RevocationInfoChoice

RevocationInfoChoice ::= CHOICE {
  crl CertificateList,
  other [1] IMPLICIT OtherRevocationInfoFormat }

OtherRevocationInfoFormat ::= SEQUENCE {
  otherRevInfoFormat OBJECT IDENTIFIER,
  otherRevInfo ANY DEFINED BY otherRevInfoFormat }
```

#### 10.2.2. CertificateChoices

CertificateChoices 类型提供 PKCS #6 扩展证书 [PKCS#6]、X.509 证书、版本 1 X.509 属性证书（ACv1）[X.509-97]、版本 2 X.509 属性证书（ACv2）[X.509-00] 或任何其他证书格式。PKCS #6 扩展证书已过时。包含 PKCS #6 证书是为了向后兼容，PKCS #6 证书 SHOULD NOT 被使用。ACv1 也已过时。包含 ACv1 是为了向后兼容，ACv1 SHOULD NOT 被使用。X.509 证书的互联网配置在"Internet X.509 Public Key Infrastructure: Certificate and CRL [[Profile]]"[PROFILE] 中指定。ACv2 的互联网配置在"An Internet Attribute Certificate [[Profile]] for Authorization"[ACPROFILE] 中指定。提供 OtherCertificateFormat 替代方案以支持任何其他证书格式而无需进一步修改 CMS。

Certificate 的定义取自 X.509。

AttributeCertificate 的定义取自 X.509-1997 和 X.509-2000。X.509-1997 的定义分配给 AttributeCertificateV1（参见第 12.2 节），X.509-2000 的定义分配给 AttributeCertificateV2。

```
CertificateChoices ::= CHOICE {
 certificate Certificate,
 extendedCertificate [0] IMPLICIT ExtendedCertificate, -- Obsolete
 v1AttrCert [1] IMPLICIT AttributeCertificateV1,       -- Obsolete
 v2AttrCert [2] IMPLICIT AttributeCertificateV2,
 other [3] IMPLICIT OtherCertificateFormat }

OtherCertificateFormat ::= SEQUENCE {
  otherCertFormat OBJECT IDENTIFIER,
  otherCert ANY DEFINED BY otherCertFormat }
```

#### 10.2.3. CertificateSet

CertificateSet 类型提供一组证书。该集合应足以包含从认可的"根"或"顶级认证机构"到与之关联的所有发送方证书的认证路径。但是，证书可能多于必要的数量，也 MAY 少于必要的数量。

"认证路径"的精确含义超出了本文档的范围。但是，[PROFILE] 为 X.509 证书提供了定义。某些应用可能对认证路径的长度施加上限；其他应用可能强制认证路径内证书的主题和颁发者之间的某些关系。

```
CertificateSet ::= SET OF CertificateChoices
```

#### 10.2.4. IssuerAndSerialNumber

IssuerAndSerialNumber 类型通过证书颁发者的可辨别名称和颁发者特定的证书序列号标识证书，从而标识实体和公钥。

Name 的定义取自 X.501 [X.501-88]，CertificateSerialNumber 的定义取自 X.509 [X.509-97]。

```
IssuerAndSerialNumber ::= SEQUENCE {
  issuer Name,
  serialNumber CertificateSerialNumber }

CertificateSerialNumber ::= INTEGER
```

#### 10.2.5. CMSVersion

CMSVersion 类型提供语法版本号，用于与本规范的未来修订版兼容。

```
CMSVersion ::= INTEGER
               { v0(0), v1(1), v2(2), v3(3), v4(4), v5(5) }
```

#### 10.2.6. UserKeyingMaterial

UserKeyingMaterial 类型提供用户密钥材料（UKM）的语法。某些密钥协商算法需要 UKM 以确保每次相同的两方生成成对密钥时生成不同的密钥。发送方提供用于特定密钥协商算法的 UKM。

```
UserKeyingMaterial ::= OCTET STRING
```

#### 10.2.7. OtherKeyAttribute

OtherKeyAttribute 类型提供包含其他密钥属性的语法，允许接收方选择发送方使用的密钥。属性对象标识符必须与属性本身的语法一起注册。应避免使用此结构，因为它可能妨碍互操作性。

```
OtherKeyAttribute ::= SEQUENCE {
  keyAttrId OBJECT IDENTIFIER,
  keyAttr ANY DEFINED BY keyAttrId OPTIONAL }
```

## 11. 有用属性

本节定义可与 signed-data、enveloped-data、encrypted-data 或 authenticated-data 一起使用的属性。Attribute 的语法与 X.501 [X.501-88] 和 RFC 5280 [PROFILE] 兼容。本节中定义的一些属性最初在 PKCS #9 [PKCS#9] 中定义；其他最初在本规范的先前版本 [CMS1] 中定义。属性不按任何特定顺序列出。

额外的属性在许多地方定义，尤其是 [[S/MIME]] 版本 3.1 [[消息规范]] [MSG3.1] 和 [[S/MIME]] 增强安全服务 [ESS]，它们还包含关于这些属性放置位置的建议。

### 11.1. 内容类型 (Content Type)

content-type 属性类型指定 signed-data 或 authenticated-data 中 ContentInfo 的内容类型。当 signed-data 中存在已签名属性或 authenticated-data 中存在认证属性时，content-type 属性类型 MUST 存在。content-type 属性值 MUST 与 signed-data 或 authenticated-data 中的 encapContentInfo eContentType 值匹配。

content-type 属性 MUST 是已签名属性或认证属性；MUST NOT 是未签名属性、未认证属性或未保护属性。

以下对象标识符标识 content-type 属性：

```
id-contentType OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 3 }
```

Content-type 属性值具有 [[ASN.1]] 类型 ContentType：

```
ContentType ::= OBJECT IDENTIFIER
```

即使语法定义为 SET OF AttributeValue，content-type 属性 MUST 具有单个属性值；不允许零个或多个 AttributeValue 实例。

SignedAttributes 和 AuthAttributes 语法定义各为 SET OF Attributes。signerInfo 中的 SignedAttributes MUST NOT 包含多个 content-type 属性实例。类似地，AuthenticatedData 中的 AuthAttributes MUST NOT 包含多个 content-type 属性实例。

### 11.2. 消息摘要 (Message Digest)

message-digest 属性类型指定在 signed-data 中签名的 encapContentInfo eContent OCTET STRING 的消息摘要（参见第 5.4 节）或在 authenticated-data 中认证的消息摘要（参见第 9.2 节）。对于 signed-data，消息摘要使用签名者的消息摘要算法计算。对于 authenticated-data，消息摘要使用发起方的消息摘要算法计算。

在 signed-data 中，当存在任何已签名属性时，message-digest 已签名属性类型 MUST 存在。在 authenticated-data 中，当存在任何认证属性时，message-digest 认证属性类型 MUST 存在。

message-digest 属性 MUST 是已签名属性或认证属性；MUST NOT 是未签名属性、未认证属性或未保护属性。

以下对象标识符标识 message-digest 属性：

```
id-messageDigest OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 4 }
```

Message-digest 属性值具有 [[ASN.1]] 类型 MessageDigest：

```
MessageDigest ::= OCTET STRING
```

message-digest 属性 MUST 具有单个属性值，即使语法定义为 SET OF AttributeValue。MUST NOT 存在零个或多个 AttributeValue 实例。

SignedAttributes 语法和 AuthAttributes 语法各定义为 SET OF Attributes。signerInfo 中的 SignedAttributes MUST 仅包含一个 message-digest 属性实例。类似地，AuthenticatedData 中的 AuthAttributes MUST 仅包含一个 message-digest 属性实例。

### 11.3. 签名时间 (Signing Time)

signing-time 属性类型指定签名者（据称）执行签名过程的时间。signing-time 属性类型旨在用于 signed-data。

signing-time 属性 MUST 是已签名属性或认证属性；MUST NOT 是未签名属性、未认证属性或未保护属性。

以下对象标识符标识 signing-time 属性：

```
id-signingTime OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 5 }
```

Signing-time 属性值具有 [[ASN.1]] 类型 SigningTime：

```
SigningTime ::= Time

Time ::= CHOICE {
  utcTime UTCTime,
  generalizedTime GeneralizedTime }
```

> [!note] Time 定义
> Time 的定义与 1997 版 X.509 [X.509-97] 中指定的定义匹配。

1950 年 1 月 1 日至 2049 年 12 月 31 日（含）之间的日期 MUST 编码为 UTCTime。年份值在 1950 年之前或 2049 年之后的任何日期 MUST 编码为 GeneralizedTime。

UTCTime 值 MUST 以协调世界时（Coordinated Universal Time，即前称格林威治标准时间 GMT 和祖鲁时钟时间）表示，并且 MUST 包含秒（即时间为 YYMMDDHHMMSSZ），即使秒数为零。午夜 MUST 表示为 "YYMMDD000000Z"。世纪信息是隐含的，世纪 MUST 按如下方式确定：

- 当 YY 大于或等于 50 时，年份 MUST 解释为 19YY。
- 当 YY 小于 50 时，年份 MUST 解释为 20YY。

GeneralizedTime 值 MUST 以协调世界时表示，并且 MUST 包含秒（即时间为 YYYYMMDDHHMMSSZ），即使秒数为零。GeneralizedTime 值 MUST NOT 包含小数秒。

signing-time 属性 MUST 具有单个属性值，即使语法定义为 SET OF AttributeValue。MUST NOT 存在零个或多个 AttributeValue 实例。

SignedAttributes 语法和 AuthAttributes 语法各定义为 SET OF Attributes。signerInfo 中的 SignedAttributes MUST NOT 包含多个 signing-time 属性实例。类似地，AuthenticatedData 中的 AuthAttributes MUST NOT 包含多个 signing-time 属性实例。

对签名时间的正确性没有施加要求，接受据称的签名时间由接收方自行决定。但是，预期某些签名者（如时间戳服务器）将被隐式信任。

### 11.4. 副签名 (Countersignature)

countersignature 属性类型指定对 signed-data 中 SignerInfo 值的签名 OCTET STRING 的内容八位字节的一个或多个签名。也就是说，消息摘要是对组成 OCTET STRING 值的八位字节计算的，不包括标签和长度八位字节。因此，countersignature 属性类型对另一个签名进行副签名（串行签名）。

countersignature 属性 MUST 是未签名属性；MUST NOT 是已签名属性、认证属性、未认证属性或未保护属性。

以下对象标识符标识 countersignature 属性：

```
id-countersignature OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 6 }
```

Countersignature 属性值具有 [[ASN.1]] 类型 Countersignature：

```
Countersignature ::= SignerInfo
```

Countersignature 值与普通签名的 SignerInfo 值具有相同含义，除了：

1. signedAttributes 字段 MUST NOT 包含 content-type 属性；副签名没有内容类型。
2. signedAttributes 字段如果包含任何其他属性，MUST 包含 message-digest 属性。
3. 消息摘要过程的输入是与之关联的 SignerInfo 值的 signatureValue 字段的 DER 编码的内容八位字节。

countersignature 属性可以具有多个属性值。语法定义为 SET OF AttributeValue，MUST 存在一个或多个 AttributeValue 实例。

UnsignedAttributes 语法定义为 SET OF Attributes。signerInfo 中的 UnsignedAttributes 可以包含多个 countersignature 属性实例。

副签名由于具有 SignerInfo 类型，其本身可以包含 countersignature 属性。因此，可以构造任意长的副签名链。

## 12. ASN.1 模块

第 12.1 节包含 CMS 的 [[ASN.1]] 模块，第 12.2 节包含版本 1 属性证书的 [[ASN.1]] 模块。

### 12.1. CMS ASN.1 模块

```asn1
CryptographicMessageSyntax2004
  { iso(1) member-body(2) us(840) rsadsi(113549)
    pkcs(1) pkcs-9(9) smime(16) modules(0) cms-2004(24) }

DEFINITIONS IMPLICIT TAGS ::=
BEGIN

-- EXPORTS All
-- The types and values defined in this module are exported for use
-- in the other ASN.1 modules.  Other applications may use them for
-- their own purposes.

IMPORTS

  -- Imports from RFC 5280 [PROFILE], Appendix A.1
        AlgorithmIdentifier, Certificate, CertificateList,
        CertificateSerialNumber, Name
           FROM PKIX1Explicit88
                { iso(1) identified-organization(3) dod(6)
                  internet(1) security(5) mechanisms(5) pkix(7)
                  mod(0) pkix1-explicit(18) }

  -- Imports from RFC 3281 [ACPROFILE], Appendix B
        AttributeCertificate
           FROM PKIXAttributeCertificate
                { iso(1) identified-organization(3) dod(6)
                  internet(1) security(5) mechanisms(5) pkix(7)
                  mod(0) attribute-cert(12) }

  -- Imports from Appendix B of this document
        AttributeCertificateV1
           FROM AttributeCertificateVersion1
                { iso(1) member-body(2) us(840) rsadsi(113549)
                  pkcs(1) pkcs-9(9) smime(16) modules(0)
                  v1AttrCert(15) } ;

-- Cryptographic Message Syntax

ContentInfo ::= SEQUENCE {
  contentType ContentType,
  content [0] EXPLICIT ANY DEFINED BY contentType }

ContentType ::= OBJECT IDENTIFIER

SignedData ::= SEQUENCE {
  version CMSVersion,
  digestAlgorithms DigestAlgorithmIdentifiers,
  encapContentInfo EncapsulatedContentInfo,
  certificates [0] IMPLICIT CertificateSet OPTIONAL,
  crls [1] IMPLICIT RevocationInfoChoices OPTIONAL,
  signerInfos SignerInfos }

DigestAlgorithmIdentifiers ::= SET OF DigestAlgorithmIdentifier

SignerInfos ::= SET OF SignerInfo

EncapsulatedContentInfo ::= SEQUENCE {
  eContentType ContentType,
  eContent [0] EXPLICIT OCTET STRING OPTIONAL }

SignerInfo ::= SEQUENCE {
  version CMSVersion,
  sid SignerIdentifier,
  digestAlgorithm DigestAlgorithmIdentifier,
  signedAttrs [0] IMPLICIT SignedAttributes OPTIONAL,
  signatureAlgorithm SignatureAlgorithmIdentifier,
  signature SignatureValue,
  unsignedAttrs [1] IMPLICIT UnsignedAttributes OPTIONAL }

SignerIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier }

SignedAttributes ::= SET SIZE (1..MAX) OF Attribute

UnsignedAttributes ::= SET SIZE (1..MAX) OF Attribute

Attribute ::= SEQUENCE {
  attrType OBJECT IDENTIFIER,
  attrValues SET OF AttributeValue }

AttributeValue ::= ANY

SignatureValue ::= OCTET STRING

EnvelopedData ::= SEQUENCE {
  version CMSVersion,
  originatorInfo [0] IMPLICIT OriginatorInfo OPTIONAL,
  recipientInfos RecipientInfos,
  encryptedContentInfo EncryptedContentInfo,
  unprotectedAttrs [1] IMPLICIT UnprotectedAttributes OPTIONAL }

OriginatorInfo ::= SEQUENCE {
  certs [0] IMPLICIT CertificateSet OPTIONAL,
  crls [1] IMPLICIT RevocationInfoChoices OPTIONAL }

RecipientInfos ::= SET SIZE (1..MAX) OF RecipientInfo

EncryptedContentInfo ::= SEQUENCE {
  contentType ContentType,
  contentEncryptionAlgorithm ContentEncryptionAlgorithmIdentifier,
  encryptedContent [0] IMPLICIT EncryptedContent OPTIONAL }

EncryptedContent ::= OCTET STRING

UnprotectedAttributes ::= SET SIZE (1..MAX) OF Attribute

RecipientInfo ::= CHOICE {
  ktri KeyTransRecipientInfo,
  kari [1] KeyAgreeRecipientInfo,
  kekri [2] KEKRecipientInfo,
  pwri [3] PasswordRecipientInfo,
  ori [4] OtherRecipientInfo }

EncryptedKey ::= OCTET STRING

KeyTransRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 0 or 2
  rid RecipientIdentifier,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }

RecipientIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier }

KeyAgreeRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 3
  originator [0] EXPLICIT OriginatorIdentifierOrKey,
  ukm [1] EXPLICIT UserKeyingMaterial OPTIONAL,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  recipientEncryptedKeys RecipientEncryptedKeys }

OriginatorIdentifierOrKey ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  subjectKeyIdentifier [0] SubjectKeyIdentifier,
  originatorKey [1] OriginatorPublicKey }

OriginatorPublicKey ::= SEQUENCE {
  algorithm AlgorithmIdentifier,
  publicKey BIT STRING }

RecipientEncryptedKeys ::= SEQUENCE OF RecipientEncryptedKey

RecipientEncryptedKey ::= SEQUENCE {
  rid KeyAgreeRecipientIdentifier,
  encryptedKey EncryptedKey }

KeyAgreeRecipientIdentifier ::= CHOICE {
  issuerAndSerialNumber IssuerAndSerialNumber,
  rKeyId [0] IMPLICIT RecipientKeyIdentifier }

RecipientKeyIdentifier ::= SEQUENCE {
  subjectKeyIdentifier SubjectKeyIdentifier,
  date GeneralizedTime OPTIONAL,
  other OtherKeyAttribute OPTIONAL }

SubjectKeyIdentifier ::= OCTET STRING

KEKRecipientInfo ::= SEQUENCE {
  version CMSVersion,  -- always set to 4
  kekid KEKIdentifier,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }

KEKIdentifier ::= SEQUENCE {
  keyIdentifier OCTET STRING,
  date GeneralizedTime OPTIONAL,
  other OtherKeyAttribute OPTIONAL }

PasswordRecipientInfo ::= SEQUENCE {
  version CMSVersion,   -- always set to 0
  keyDerivationAlgorithm [0] KeyDerivationAlgorithmIdentifier
                             OPTIONAL,
  keyEncryptionAlgorithm KeyEncryptionAlgorithmIdentifier,
  encryptedKey EncryptedKey }

OtherRecipientInfo ::= SEQUENCE {
  oriType OBJECT IDENTIFIER,
  oriValue ANY DEFINED BY oriType }

DigestedData ::= SEQUENCE {
  version CMSVersion,
  digestAlgorithm DigestAlgorithmIdentifier,
  encapContentInfo EncapsulatedContentInfo,
  digest Digest }

Digest ::= OCTET STRING

EncryptedData ::= SEQUENCE {
  version CMSVersion,
  encryptedContentInfo EncryptedContentInfo,
  unprotectedAttrs [1] IMPLICIT UnprotectedAttributes OPTIONAL }

AuthenticatedData ::= SEQUENCE {
  version CMSVersion,
  originatorInfo [0] IMPLICIT OriginatorInfo OPTIONAL,
  recipientInfos RecipientInfos,
  macAlgorithm MessageAuthenticationCodeAlgorithm,
  digestAlgorithm [1] DigestAlgorithmIdentifier OPTIONAL,
  encapContentInfo EncapsulatedContentInfo,
  authAttrs [2] IMPLICIT AuthAttributes OPTIONAL,
  mac MessageAuthenticationCode,
  unauthAttrs [3] IMPLICIT UnauthAttributes OPTIONAL }

AuthAttributes ::= SET SIZE (1..MAX) OF Attribute

UnauthAttributes ::= SET SIZE (1..MAX) OF Attribute

MessageAuthenticationCode ::= OCTET STRING

DigestAlgorithmIdentifier ::= AlgorithmIdentifier

SignatureAlgorithmIdentifier ::= AlgorithmIdentifier

KeyEncryptionAlgorithmIdentifier ::= AlgorithmIdentifier

ContentEncryptionAlgorithmIdentifier ::= AlgorithmIdentifier

MessageAuthenticationCodeAlgorithm ::= AlgorithmIdentifier

KeyDerivationAlgorithmIdentifier ::= AlgorithmIdentifier

RevocationInfoChoices ::= SET OF RevocationInfoChoice

RevocationInfoChoice ::= CHOICE {
  crl CertificateList,
  other [1] IMPLICIT OtherRevocationInfoFormat }

OtherRevocationInfoFormat ::= SEQUENCE {
  otherRevInfoFormat OBJECT IDENTIFIER,
  otherRevInfo ANY DEFINED BY otherRevInfoFormat }

CertificateChoices ::= CHOICE {
  certificate Certificate,
  extendedCertificate [0] IMPLICIT ExtendedCertificate,  -- Obsolete
  v1AttrCert [1] IMPLICIT AttributeCertificateV1,        -- Obsolete
  v2AttrCert [2] IMPLICIT AttributeCertificateV2,
  other [3] IMPLICIT OtherCertificateFormat }

AttributeCertificateV2 ::= AttributeCertificate

OtherCertificateFormat ::= SEQUENCE {
  otherCertFormat OBJECT IDENTIFIER,
  otherCert ANY DEFINED BY otherCertFormat }

CertificateSet ::= SET OF CertificateChoices

IssuerAndSerialNumber ::= SEQUENCE {
  issuer Name,
  serialNumber CertificateSerialNumber }

CMSVersion ::= INTEGER  { v0(0), v1(1), v2(2), v3(3), v4(4), v5(5) }

UserKeyingMaterial ::= OCTET STRING

OtherKeyAttribute ::= SEQUENCE {
  keyAttrId OBJECT IDENTIFIER,
  keyAttr ANY DEFINED BY keyAttrId OPTIONAL }

-- Content Type Object Identifiers

id-ct-contentInfo OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) smime(16) ct(1) 6 }

id-data OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 1 }

id-signedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 2 }

id-envelopedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 3 }

id-digestedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 5 }

id-encryptedData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs7(7) 6 }

id-ct-authData OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs-9(9) smime(16) ct(1) 2 }

-- The CMS Attributes

MessageDigest ::= OCTET STRING

SigningTime  ::= Time

Time ::= CHOICE {
  utcTime UTCTime,
  generalTime GeneralizedTime }

Countersignature ::= SignerInfo

-- Attribute Object Identifiers

id-contentType OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 3 }

id-messageDigest OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 4 }

id-signingTime OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 5 }

id-countersignature OBJECT IDENTIFIER ::= { iso(1) member-body(2)
    us(840) rsadsi(113549) pkcs(1) pkcs9(9) 6 }

-- Obsolete Extended Certificate syntax from PKCS #6

ExtendedCertificateOrCertificate ::= CHOICE {
  certificate Certificate,
  extendedCertificate [0] IMPLICIT ExtendedCertificate }

ExtendedCertificate ::= SEQUENCE {
  extendedCertificateInfo ExtendedCertificateInfo,
  signatureAlgorithm SignatureAlgorithmIdentifier,
  signature Signature }

ExtendedCertificateInfo ::= SEQUENCE {
  version CMSVersion,
  certificate Certificate,
  attributes UnauthAttributes }

Signature ::= BIT STRING

END -- of CryptographicMessageSyntax2004
```

### 12.2. 版本 1 属性证书 ASN.1 模块

```asn1
AttributeCertificateVersion1
    { iso(1) member-body(2) us(840) rsadsi(113549)
      pkcs(1) pkcs-9(9) smime(16) modules(0) v1AttrCert(15) }

DEFINITIONS EXPLICIT TAGS ::=
BEGIN

-- EXPORTS All

IMPORTS

  -- Imports from RFC 5280 [PROFILE], Appendix A.1
        AlgorithmIdentifier, Attribute, CertificateSerialNumber,
        Extensions, UniqueIdentifier
           FROM PKIX1Explicit88
                { iso(1) identified-organization(3) dod(6)
                  internet(1) security(5) mechanisms(5) pkix(7)
                  mod(0) pkix1-explicit(18) }

  -- Imports from RFC 5280 [PROFILE], Appendix A.2
        GeneralNames
           FROM PKIX1Implicit88
                { iso(1) identified-organization(3) dod(6)
                  internet(1) security(5) mechanisms(5) pkix(7)
                  mod(0) pkix1-implicit(19) }

  -- Imports from RFC 3281 [ACPROFILE], Appendix B
        AttCertValidityPeriod, IssuerSerial
           FROM PKIXAttributeCertificate
                { iso(1) identified-organization(3) dod(6)
                  internet(1) security(5) mechanisms(5) pkix(7)
                  mod(0) attribute-cert(12) } ;

-- Definition extracted from X.509-1997 [X.509-97], but
-- different type names are used to avoid collisions.

AttributeCertificateV1 ::= SEQUENCE {
  acInfo AttributeCertificateInfoV1,
  signatureAlgorithm AlgorithmIdentifier,
  signature BIT STRING }

AttributeCertificateInfoV1 ::= SEQUENCE {
  version AttCertVersionV1 DEFAULT v1,
  subject CHOICE {
    baseCertificateID [0] IssuerSerial,
      -- associated with a Public Key Certificate
    subjectName [1] GeneralNames },
      -- associated with a name
  issuer GeneralNames,
  signature AlgorithmIdentifier,
  serialNumber CertificateSerialNumber,
  attCertValidityPeriod AttCertValidityPeriod,
  attributes SEQUENCE OF Attribute,
  issuerUniqueID UniqueIdentifier OPTIONAL,
  extensions Extensions OPTIONAL }

AttCertVersionV1 ::= INTEGER { v1(0) }

END -- of AttributeCertificateVersion1
```

## 13. 参考文献

### 13.1. 规范性引用 (Normative References)

- [ACPROFILE] Farrell, S. and R. Housley, "An Internet Attribute Certificate [[Profile]] for Authorization", RFC 3281, April 2002.
- [PROFILE] Cooper, D., Santesson, S., Farrell, S., Boeyen, S., Housley, R., and W. Polk, "Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) [[Profile]]", RFC 5280, May 2008.
- [STDWORDS] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [X.208-88] CCITT. Recommendation X.208: Specification of Abstract Syntax Notation One ([[ASN.1]]), 1988.
- [X.209-88] CCITT. Recommendation X.209: Specification of Basic Encoding Rules for Abstract Syntax Notation One ([[ASN.1]]), 1988.
- [X.501-88] CCITT. Recommendation X.501: The Directory - Models, 1988.
- [X.509-88] CCITT. Recommendation X.509: The Directory - Authentication Framework, 1988.
- [X.509-97] ITU-T. Recommendation X.509: The Directory - Authentication Framework, 1997.
- [X.509-00] ITU-T. Recommendation X.509: The Directory - Authentication Framework, 2000.

### 13.2. 信息性引用 (Informative References)

- [CMS1] Housley, R., "Cryptographic Message Syntax", RFC 2630, June 1999.
- [CMS2] Housley, R., "Cryptographic Message Syntax (CMS)", RFC 3369, August 2002.
- [CMS3] Housley, R., "Cryptographic Message Syntax (CMS)", RFC 3852, July 2004.
- [CMSALG] Housley, R., "Cryptographic Message Syntax (CMS) Algorithms", RFC 3370, August 2002.
- [CMSMSIG] Housley, R., "Cryptographic Message Syntax (CMS) Multiple Signer Clarification", RFC 4853, April 2007.
- [DH-X9.42] Rescorla, E., "Diffie-Hellman Key Agreement Method", RFC 2631, June 1999.
- [ESS] Hoffman, P., Ed., "Enhanced Security Services for [[S/MIME]]", RFC 2634, June 1999.
- [MSAC] Microsoft Development Network (MSDN) Library, "Authenticode", April 2004 Release.
- [MSG2] Dusse, S., Hoffman, P., Ramsdell, B., Lundblade, L., and L. Repka, "[[S/MIME]] Version 2 Message Specification", RFC 2311, March 1998.
- [MSG3] Ramsdell, B., Ed., "[[S/MIME]] Version 3 Message Specification", RFC 2633, June 1999.
- [MSG3.1] Ramsdell, B., Ed., "Secure/Multipurpose Internet Mail Extensions ([[S/MIME]]) Version 3.1 Message Specification", RFC 3851, July 2004.
- [NEWPKCS#1] Kaliski, B. and J. Staddon, "PKCS #1: RSA Cryptography Specifications Version 2.0", RFC 2437, October 1998.
- [OCSP] Myers, M., Ankney, R., Malpani, A., Galperin, S., and C. Adams, [["X.509]] Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP", RFC 2560, June 1999.
- [PKCS#1] Kaliski, B., "PKCS #1: RSA Encryption Version 1.5", RFC 2313, March 1998.
- [PKCS#6] RSA Laboratories. PKCS #6: Extended-Certificate Syntax Standard, Version 1.5. November 1993.
- [PKCS#7] Kaliski, B., "PKCS #7: Cryptographic Message Syntax Version 1.5", RFC 2315, March 1998.
- [PKCS#9] RSA Laboratories. PKCS #9: Selected Attribute Types, Version 1.1. November 1993.
- [PWRI] Gutmann, P., "Password-based Encryption for CMS", RFC 3211, December 2001.
- [RANDOM] Eastlake, D., 3rd, Schiller, J., and S. Crocker, "Randomness Requirements for Security", BCP 106, RFC 4086, June 2005.

## 14. 安全考虑

密码消息语法提供了[[数字签名]]数据、摘要数据、加密数据和认证数据的方法。

> [!warning] 密钥保护
> 实现必须保护签名者的私钥。签名者私钥的泄露允许冒充。

实现必须保护[[密钥管理]]私钥、密钥加密密钥和内容加密密钥。[[密钥管理]]私钥或密钥加密密钥的泄露可能导致使用该密钥保护的所有内容被披露。类似地，内容加密密钥的泄露可能导致关联的加密内容被披露。

实现必须保护[[密钥管理]]私钥和消息认证密钥。[[密钥管理]]私钥的泄露允许冒充认证数据。类似地，消息认证密钥的泄露可能导致认证内容的不可检测修改。

用于分发消息认证密钥的[[密钥管理]]技术本身必须提供数据源认证；否则，内容将从未知来源完整地交付。RSA [PKCS#1] [NEWPKCS#1] 和临时-静态 Diffie-Hellman [DH-X9.42] 都不提供必要的数据源认证。当发起方和接收方的公钥都绑定到 X.509 证书中的适当身份时，静态-静态 Diffie-Hellman [DH-X9.42] 确实提供必要的数据源认证。

当超过两方共享相同的消息认证密钥时，不提供数据源认证。任何知道消息认证密钥的一方都可以计算有效的 MAC；因此，内容可能源自任何一方。

实现必须随机生成内容加密密钥、消息认证密钥、初始化向量（IV）和填充。此外，公/私钥对的生成依赖于随机数。使用不充分的伪随机数生成器（PRNG）生成密码密钥可能导致几乎没有安全性。攻击者可能发现重现生成密钥的 PRNG 环境比暴力搜索整个密钥空间容易得多——搜索由此产生的较小可能性集合。高质量随机数的生成是困难的。RFC 4086 [RANDOM] 在此领域提供了重要指导。

> [!tip] 算法强度匹配
> 使用密钥协商算法或预分发的对称密钥加密密钥时，密钥加密密钥用于加密内容加密密钥。如果密钥加密算法和内容加密算法不同，有效安全性由两者中较弱的算法决定。例如，如果内容使用 168 位 Triple-DES 内容加密密钥加密，而内容加密密钥使用 40 位 RC2 密钥加密密钥包装，则最多提供 40 位保护。通过对 40 位 RC2 密钥的简单搜索可以恢复 Triple-DES 密钥，然后使用 Triple-DES 密钥解密内容。因此，实现者必须确保密钥加密算法与内容加密算法一样强或更强。

实现者应注意密码算法会随时间变弱。随着新的密码分析技术的开发和计算性能的提高，破解特定密码算法的工作量将减少。因此，密码算法实现应该是模块化的，允许随时插入新算法。也就是说，实现者应为必须支持的算法集随时间变化做好准备。

副签名未签名属性包含对内容签名值计算的[[数字签名]]；因此，副签名过程不需要知道原始的已签名内容。这种结构允许实现效率优势；然而，这种结构也可能允许对不适当的签名值进行副签名。因此，执行副签名的实现应该在副签名之前验证原始签名值（此验证需要处理原始内容），或者实现应在确保只对适当签名值进行副签名的上下文中执行副签名。

## 15. 致谢

本文档是许多专业人士贡献的结果。感谢 IETF [[S/MIME]] 工作组所有成员的辛勤工作。特别感谢 Rich Ankney、Simon Blake-Wilson、Tim Dean、Steve Dusse、Carl Ellison、Peter Gutmann、Bob Jueneman、Stephen Henson、Paul Hoffman、Scott Hollenbeck、Don Johnson、Burt Kaliski、John Linn、John Pawling、Blake Ramsdell、Francois Rousseau、Jim Schaad、Dave Solo、Paul Timmel 和 Sean Turner 的努力和支持。

感谢 Tim Polk 鼓励推动本规范沿标准成熟度阶梯前进。此外，感谢 Jan Vilhuber 的仔细阅读，这促成了 RFC 勘误 1744。

## 作者地址

Russell Housley
Vigil Security, LLC
918 Spring Knoll Drive
Herndon, VA 20170
USA
EMail: housley@vigilsec.com
