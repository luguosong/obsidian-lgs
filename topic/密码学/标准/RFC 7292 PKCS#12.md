---
title: PKCS#12 个人信息交换语法 v1.1
description: RFC 7292 定义了个人信息交换语法（PKCS#12），描述了一种用于传输个人身份信息的格式，包括私钥、证书、杂项秘密和扩展，支持多种隐私与完整性模式。
tags:
  - 密码学
  - PKCS12
  - PFX
  - 证书存储
  - RFC
---

> [!info] RFC 信息
> - **RFC 编号**：7292
> - **标题**：PKCS #12: Personal Information Exchange Syntax v1.1
> - **类别**：Informational
> - **发布日期**：[[2014]] 年 7 月
> - **作者**：K. Moriarty (EMC, 编辑), M. Nystrom (Microsoft), S. Parkinson, A. Rusch, M. Scott (RSA)

> [!abstract] 摘要
> PKCS #12 v1.1 描述了一种用于个人身份信息的传输语法，包括私钥、证书、杂项秘密和扩展。支持此标准的机器、应用程序、浏览器、Internet kiosk 等将允许用户导入、导出和使用一组统一的个人身份信息。本标准支持在多种隐私和完整性模式下直接传输个人信息。
>
> 本文档是 RSA Laboratories 公钥密码标准（PKCS）系列中 PKCS #12 v1.1 的再版。通过发布此 RFC，变更控制权已移交至 IETF。

> [!note] IESG 说明
> IESG 感谢 RSA Laboratories 将变更控制权移交给 IETF。保持向后兼容性的增强功能预计将在后续的 IETF Standards Track 文档中出现。

## 1. 引言

本文档是 RSA Laboratories 公钥密码标准（PKCS）系列中 PKCS #12 v1.1 的再版。通过发布此 RFC，变更控制权已移交至 IETF。RSA 及其母公司 EMC 保留继续发布和分发 PKCS #12 v1.1 及其先前版本的权利。

本文档正文（安全考虑部分除外）直接取自 PKCS #12 v1.1 规范。引用列表和内联引用已更新或添加，以引用最新文档以及 PKCS #12 v1.1 最初发布时的现行文档。

本标准描述了一种用于个人身份信息的传输语法，包括私钥、证书、杂项秘密和扩展。支持此标准的机器、应用程序、浏览器、Internet kiosk 等将允许用户导入、导出和使用一组统一的个人身份信息。

本标准支持在多种隐私和完整性模式下直接传输个人信息。其中最安全的隐私和完整性模式要求源平台和目标平台分别拥有可用于[[数字签名]]和加密的受信公钥/私钥对。本标准还支持较低安全性的基于密码的隐私和完整性模式，适用于没有受信公钥/私钥对的情况。

本标准适用于软件和硬件实现。硬件实现通过防篡改令牌（如智能卡和 PCMCIA 设备）提供物理安全性。

本标准可视为在 PKCS #8 [15] [24] 基础上的扩展，通过包含基本但辅助的身份信息以及私钥，并通过公钥隐私和完整性模式提高安全性。

### 1.1 与 PKCS #12 版本 1 的变更

本文档将 PKCS #12 [16] 移入 IETF，并包含作者为本提交所做的一些小改动：

- 增加了哈希算法
- 纳入了技术勘误 #1，对 [[ASN.1]] 语法进行了一些小修正
- 从 [[ASN.1]] 语法中移除了 1024 作为迭代次数的示例值
- 增加了建议：附录 B 中的方法不再用于特定模式（password privacy mode，密码隐私模式），而应使用 PKCS#5 v2.1 中的技术
- 对附录 C 中的 [[ASN.1]] 模块增加了注释和轻微修正
- 移除了原附录 D 中的出口管制讨论
- 在"知识产权考虑"中将 RSA 替换为 EMC
- 对引用进行了大量更改和补充
- 增加了对 NIST SP [[800-132]] 的引用，涉及密码完整性迭代次数值选择的建议（抗字典攻击的一部分）
- 增加了 PFX 缩写展开的注释：该缩写有时展开为 Personal Information Exchange
- 在附录 B 中，将 "no longer recommended"（不再推荐）改为 "not recommended"（不推荐），以明确该方法不被推荐

## 2. 定义与符号

- **AlgorithmIdentifier**：一种 [[ASN.1]] 类型，通过对象标识符标识算法及其关联参数。定义见 [8]。
- **[[ASN.1]]**：Abstract Syntax Notation One（抽象语法记法一），定义见 [2]、[3]、[4] 和 [5]。
- **Attribute**：一种 [[ASN.1]] 类型，通过对象标识符标识属性类型及其关联属性值。[[ASN.1]] 类型 Attribute 定义见 [7]。
- **Certificate（证书）**：经[[数字签名]]的数据单元，将公钥绑定到身份信息。身份证书的特定格式定义见 [8]，另一种格式描述见 [17]。
- **Certificate Revocation List (CRL，证书撤销列表)**：经[[数字签名]]的不再应被认可的证书列表，已由颁发者或更高级别机构撤销。CRL 的一种格式定义见 [8]。
- **ContentInfo**：一种 [[ASN.1]] 类型，用于保存可能已受密码学保护的数据。定义见 [21] 和 [14]。
- **DER**：Distinguished Encoding Rules（可分辨编码规则），定义见 [6]。
- **Destination platform（目标平台）**：来自源平台的个人信息的最终目标平台。
- **DigestInfo**：一种 [[ASN.1]] 类型，用于保存消息摘要。定义见 [21] 和 [14]。
- **Encryption Key Pair (DestEncK，加密密钥对)**：用于本标准公钥隐私模式的公钥/私钥对。公钥半部称为 PDestEncK（强调公钥"受信任"时为 TPDestEncK），私钥半部称为 VDestEncK。
- **Export time（导出时间）**：用户从源平台读取个人信息并将其转换为可互操作的安全 PDU 的时间。
- **Import time（导入时间）**：用户将个人信息从 Safe PDU 写入目标平台的时间。
- **Message Authentication Code (MAC，消息认证码)**：一种抗碰撞、"不可预测"的消息与密钥的函数类型。MAC 用于数据认证，在许多方面类似于秘密密钥[[数字签名]]。
- **Object Identifier（对象标识符）**：一个整数序列，在由命名机构层级管理的全局命名空间中唯一标识关联的数据对象。这是 [[ASN.1]] 中的一种原始数据类型。
- **PFX**：本标准定义的顶层交换 PDU（Protocol Data Unit，协议数据单元）。该缩写有时展开为 Personal Information Exchange。
- **Platform（平台）**：机器、操作系统和应用软件的组合，用户在其中使用个人身份信息。此上下文中的应用是使用个人信息的软件。如果机器类型不同或应用软件不同，则两个平台不同。在多用户系统中，每个用户至少有一个平台。
- **PDU（Protocol Data Unit，协议数据单元）**：以机器无关格式构成的协议消息的位序列。
- **Shrouding（遮蔽）**：对私钥应用的加密，可能与阻止密钥明文在特定明确定义的接口之外可见的策略配合使用。
- **Signature Key Pair (SrcSigK，签名密钥对)**：用于本标准公钥完整性模式的平台特定签名密钥对。公钥半部称为 PSrcSigK（强调公钥"受信任"时为 TPSrcSigK），私钥半部称为 VSrcSigK。
- **Source platform（源平台）**：最终用于目标平台的个人信息的原始平台。

## 3. 概述

### 3.1 交换模式

隐私模式和完整性模式共有四种组合。隐私模式使用加密来保护个人信息不被泄露，完整性模式保护个人信息不被篡改。如果没有防篡改保护，攻击者可能在用户不知情的情况下用无效信息替换用户的个人信息。

> [!note] 隐私模式
> - **公钥隐私模式（Public-key privacy mode）**：个人信息在源平台上使用已知目标平台的受信加密公钥进行封装（enveloped）。信封使用对应的私钥打开。
> - **密码隐私模式（Password privacy mode）**：个人信息使用从用户名和隐私密码派生的对称密钥进行加密，如 [22] 和 [13] 所述。如果同时使用密码完整性模式，隐私密码和完整性密码可以相同也可以不同。

> [!note] 完整性模式
> - **公钥完整性模式（Public-key integrity mode）**：通过对 PFX PDU 内容进行[[数字签名]]来保证完整性，签名使用源平台的私钥签名密钥产生。签名在目标平台上使用对应的公钥验证。
> - **密码完整性模式（Password integrity mode）**：通过从秘密完整性密码派生的 MAC 来保证完整性。如果同时使用密码隐私模式，隐私密码和完整性密码可以相同也可以不同。

### 3.2 模式选择策略

本标准允许隐私和完整性模式的所有组合。当然，良好的安全策略建议避免某些做法，例如在使用密码隐私模式或使用弱[[对称加密]]的公钥隐私模式时，在没有物理保护的情况下传输私钥可能是不明智的。

一般来说，从安全角度来看，公钥模式（包括隐私和完整性）优于密码模式。然而，并非总是能使用公钥模式。例如，在导出时可能不知道目标平台是什么；如果是这种情况，则无法使用公钥隐私模式。

### 3.3 受信公钥

非对称密钥对在本标准中有两种用途：公钥隐私模式和公钥完整性模式。公钥隐私模式需要加密密钥对；公钥完整性模式需要签名密钥对。

本节讨论的密钥可以是平台特定的、专用于传输用户个人信息的密钥。无论如何，此处讨论的密钥不应与用户希望从一平台传输到另一平台的个人密钥混淆（后者存储在 PDU 内）。

对于公钥隐私模式，加密密钥对中的私钥保存在目标平台上，最终用于打开私有信封。对应的受信公钥称为 TPDestEncK。

对于公钥完整性模式，签名密钥对中的私钥保存在源平台上，用于对个人信息进行签名。对应的受信公钥称为 TPSrcSigK。

对于公钥/私钥对的两种用途，密钥对中的公钥必须传输到另一平台，使其被信任为源自正确的平台。判断公钥是否受信任最终必须由用户决定。有多种方法可以确保公钥受信任。

为密钥赋予信任以及验证密钥可信度的过程在本文档中不再进一步讨论。在下文中讨论非对称密钥时，假定公钥是受信任的。

### 3.4 AuthenticatedSafe

每个合规平台应能够导入和导出封装在 PFX PDU 中的 AuthenticatedSafe PDU。

对于完整性，AuthenticatedSafe 要么被签名（如果使用公钥完整性模式）要么被 MAC 保护（如果使用密码完整性模式）以生成 PFX PDU。如果 AuthenticatedSafe 被签名，则附带[[数字签名]]，该签名在源平台上用私钥签名密钥 VSrcSigK 产生，对应于受信公钥签名密钥 TPSrcSigK。TPSrcSigK 必须随 PFX 到达目标平台，用户可以在那里验证密钥的信任度并验证 AuthenticatedSafe 上的签名。如果 AuthenticatedSafe 被 MAC 保护，则附带从秘密完整性密码、salt 位、迭代次数和 AuthenticatedSafe 内容计算得出的 MAC。

AuthenticatedSafe 本身由一系列 ContentInfo 值组成，其中一些可能是明文（data），另一些可能是封装的（如果使用公钥隐私模式）或加密的（如果使用密码隐私模式）。如果内容被封装，则使用新生成的密钥通过对称密码加密，该密钥再通过 RSA 非[[对称加密]]进行加密。用于加密对称密钥的 RSA 公钥称为 TPDestEncK，对应目标平台上的 RSA 私钥 VDestEncK。TPDestEncK 需要在导出时被用户信任。如果内容被加密，则使用从秘密隐私密码、salt 位和迭代计数器派生的密钥通过对称密码加密。

每个 ContentInfo 包含任意的私钥、PKCS #8 遮蔽私钥、证书、CRL 或不透明数据对象的集合，由用户自行决定，存储在 SafeContents 类型的值中。

> [!tip] 未加密选项存在的原因
> 一些政府限制某些加密用途。AuthenticatedSafe 中的多部分设计保持了实现者的选择空间。例如，可能可以使用强加密来制作 PKCS #8 遮蔽密钥，但这些遮蔽密钥不应进一步加密，因为超级加密可能限制产品的可出口性。多部分 AuthenticatedSafe 设计允许了这种可能性。

AuthenticatedSafe 外围是完整性模式包装器，保护 AuthenticatedSafe 的全部内容（包括未加密部分，如果存在）。这与许多协议中的包装顺序相反，在那些协议中隐私是最外层的保护。后一种更常见的包装顺序避免了对加密数据的签名，在某些情况下这是不希望的；然而，这些情况不适用于本文档，因此最好保护尽可能多信息的完整性。

## 4. PFX PDU 语法

本格式对应上述数据模型，带有隐私和完整性包装器。本节大量引用 PKCS #7 [14] [21]，并假定读者熟悉该文档中定义的术语。

所有直接交换模式都使用相同的 PDU 格式。[[ASN.1]] 和 BER 编码确保了平台独立性。

本标准有一个 [[ASN.1]] 导出类型：PFX。这是外层完整性包装器。PFX 实例包含：

1. **版本指示器**。本文档版本的版本号应为 v3。
2. **PKCS #7 ContentInfo**，其 contentType 在公钥完整性模式下为 signedData，在密码完整性模式下为 data。
3. **可选的 MacData 实例**，仅在密码完整性模式下出现。此对象（如果存在）包含一个 PKCS #7 DigestInfo（保存 MAC 值）、一个 macSalt 和一个 iterationCount。如附录 B 所述，MAC 密钥从密码、macSalt 和 iterationCount 派生；如第 5 节所述，MAC 通过 HMAC [11] [20] 从 authSafe 值和 MAC 密钥计算得出。密码和 MAC 密钥实际上不存在于 PFX 中的任何位置。salt 和（在一定程度上）迭代次数阻止了对完整性密码的字典攻击。关于如何选择合理的迭代次数值，请参阅 NIST Special Publication [[800-132]] [12]。

```
PFX ::= SEQUENCE {
    version     INTEGER {v3(3)}(v3,...),
    authSafe    ContentInfo,
    macData     MacData OPTIONAL
}

MacData ::= SEQUENCE {
    mac         DigestInfo,
    macSalt     OCTET STRING,
    iterations  INTEGER DEFAULT 1
    -- Note: The default is for historical reasons and its
    --       use is deprecated.
}
```

### 4.1 AuthenticatedSafe 类型

如上所述，authSafe 的 contentType 字段应为 data 或 signedData 类型。authSafe 的 content 字段应直接（data 情况）或间接（signedData 情况）包含 AuthenticatedSafe 类型的 BER 编码值。

```
AuthenticatedSafe ::= SEQUENCE OF ContentInfo
    -- Data if unencrypted
    -- EncryptedData if password-encrypted
    -- EnvelopedData if public key-encrypted
```

AuthenticatedSafe 包含一系列 ContentInfo 值。这些 ContentInfo 值的 content 字段包含明文、加密或封装数据。在加密或封装数据的情况下，数据的明文保存 SafeContents 实例的 BER 编码。本文档第 5.1 节更详细地描述了 AuthenticatedSafe 类型值的构造。

### 4.2 SafeBag 类型

SafeContents 类型由 SafeBag 组成。每个 SafeBag 保存一条信息——一个密钥、一个证书等——由对象标识符标识。

```
SafeContents ::= SEQUENCE OF SafeBag

SafeBag ::= SEQUENCE {
    bagId          BAG-TYPE.&id ({PKCS12BagSet})
    bagValue       [0] EXPLICIT BAG-TYPE.&Type({PKCS12BagSet}{@bagId}),
    bagAttributes  SET OF PKCS12Attribute OPTIONAL
}

PKCS12Attribute ::= SEQUENCE {
    attrId      ATTRIBUTE.&id ({PKCS12AttrSet}),
    attrValues  SET OF ATTRIBUTE.&Type ({PKCS12AttrSet}{@attrId})
} -- This type is compatible with the X.500 type 'Attribute'

PKCS12AttrSet ATTRIBUTE ::= {
    friendlyName | -- from PKCS #9 [23]
    localKeyId,    -- from PKCS #9
    ... -- Other attributes are allowed
}
```

可选的 bagAttributes 字段允许用户为密钥等分配昵称和标识符，并允许可视化工具向用户显示有意义的字符串。

本文档此版本中定义了六种 SafeBag 类型：

```
bagtypes OBJECT IDENTIFIER ::= {pkcs-12 10 1}

BAG-TYPE ::= TYPE-IDENTIFIER

keyBag BAG-TYPE ::=
    {KeyBag IDENTIFIED BY {bagtypes 1}}
pkcs8ShroudedKeyBag BAG-TYPE ::=
    {PKCS8ShroudedKeyBag IDENTIFIED BY {bagtypes 2}}
certBag BAG-TYPE ::=
    {CertBag IDENTIFIED BY {bagtypes 3}}
crlBag BAG-TYPE ::=
    {CRLBag IDENTIFIED BY {bagtypes 4}}
secretBag BAG-TYPE ::=
    {SecretBag IDENTIFIED BY {bagtypes 5}}
safeContentsBag BAG-TYPE ::=
    {SafeContents IDENTIFIED BY {bagtypes 6}}

PKCS12BagSet BAG-TYPE ::= {
    keyBag |
    pkcs8ShroudedKeyBag |
    certBag |
    crlBag |
    secretBag |
    safeContentsBag,
    ... -- For future extensions
}
```

随着本标准未来版本中新的 bag 类型被认可，PKCS12BagSet 可以被扩展。

#### 4.2.1 KeyBag 类型

KeyBag 是一个 PKCS #8 PrivateKeyInfo。注意 KeyBag 只包含一个私钥。

```
KeyBag ::= PrivateKeyInfo
```

#### 4.2.2 PKCS8ShroudedKeyBag 类型

PKCS8ShroudedKeyBag 保存一个按照 PKCS #8 进行遮蔽的私钥。注意 PKCS8ShroudedKeyBag 只保存一个遮蔽私钥。

```
PKCS8ShroudedKeyBag ::= EncryptedPrivateKeyInfo
```

#### 4.2.3 CertBag 类型

CertBag 包含某种类型的证书。使用对象标识符来区分不同的证书类型。

```
CertBag ::= SEQUENCE {
    certId      BAG-TYPE.&id   ({CertTypes}),
    certValue   [0] EXPLICIT BAG-TYPE.&Type ({CertTypes}{@certId})
}

x509Certificate BAG-TYPE ::=
    {OCTET STRING IDENTIFIED BY {certTypes 1}}
    -- DER-encoded X.509 certificate stored in OCTET STRING
sdsiCertificate BAG-TYPE ::=
    {IA5String IDENTIFIED BY {certTypes 2}}
    -- Base64-encoded SDSI certificate stored in IA5String

CertTypes BAG-TYPE ::= {
    x509Certificate |
    sdsiCertificate,
    ... -- For future extensions
}
```

#### 4.2.4 CRLBag 类型

CRLBag 包含某种类型的证书撤销列表（CRL）。使用对象标识符来区分不同的 CRL 类型。

```
CRLBag ::= SEQUENCE {
    crlId      BAG-TYPE.&id  ({CRLTypes}),
    crlValue  [0] EXPLICIT BAG-TYPE.&Type ({CRLTypes}{@crlId})
}

x509CRL BAG-TYPE ::=
    {OCTET STRING IDENTIFIED BY {crlTypes 1}}
    -- DER-encoded X.509 CRL stored in OCTET STRING

CRLTypes BAG-TYPE ::= {
    x509CRL,
    ... -- For future extensions
}
```

#### 4.2.5 SecretBag 类型

用户的每个杂项个人秘密都包含在 SecretBag 实例中，保存一个依赖于对象标识符的值。注意 SecretBag 只包含一个秘密。

```
SecretBag ::= SEQUENCE {
    secretTypeId   BAG-TYPE.&id ({SecretTypes}),
    secretValue    [0] EXPLICIT BAG-TYPE.&Type ({SecretTypes}
                       {@secretTypeId})
}

SecretTypes BAG-TYPE ::= {
    ... -- For future extensions
}
```

实现者可以自行决定向此集合添加值。

#### 4.2.6 SafeContents 类型

SafeBag 中可以持有的第六种 bag 类型是 SafeContents。这种递归结构允许在顶层 SafeContents 中任意嵌套多个 KeyBag、PKCS8ShroudedKeyBag、CertBag、CRLBag 和 SecretBag。

## 5. 使用 PFX PDU

本节描述 PFX PDU 的创建和使用。

### 5.1 创建 PFX PDU

创建 PFX PDU 的步骤如下：

1. 从 [[ASN.1]] 可以清楚地看出如何创建多个 SafeContents 实例，每个包含多个（可能嵌套的）SafeBag 实例。假设有 SC_1, SC_2, ..., SC_n 个 SafeContents 实例。注意 PFX PDU 中可以有任意数量的 SafeContents 实例。如步骤 2 所见，每个实例可以分别加密（或不加密）。

2. 对于每个 SC_i，根据选择的加密选项：

   **A.** 如果 SC_i 不需要加密，创建一个 content type 为 Data 的 ContentInfo CI_i。Data OCTET STRING 的内容应为 SC_i 的 BER 编码（包括 tag、length 和 value 八位组）。

   **B.** 如果 SC_i 要使用密码加密，创建一个类型为 EncryptedData 的 ContentInfo CI_i。CI_i 的 encryptedContentInfo 字段的 contentType 字段设为 data，encryptedContent 字段设为 SC_i 的 BER 编码的加密结果（注意 tag 和 length 八位组必须存在）。

   **C.** 如果 SC_i 要使用公钥加密，创建一个类型为 EnvelopedData 的 ContentInfo CI_i，方式与步骤 B 中创建 EncryptedData ContentInfo 基本相同。

3. 将 CI_i 按顺序组成 SEQUENCE，创建一个 AuthenticatedSafe 实例。

4. 创建一个 content type 为 Data 的 ContentInfo T。Data OCTET STRING 的内容应为 AuthenticatedSafe 值的 BER 编码（包括 tag、length 和 value 八位组）。

5. 对于完整性保护：

   **A.** 如果 PFX PDU 要通过[[数字签名]]认证，创建一个类型为 SignedData 的 ContentInfo C。C 中 SignedData 的 contentInfo 字段包含 T。C 是顶层 PFX 结构中的 ContentInfo。

   **B.** 如果 PFX PDU 要通过 HMAC 认证，则对 T 中 Data 的内容（即排除 OCTET STRING tag 和 length 字节）计算使用 SHA-1、SHA-224、SHA-256、[[SHA-3]]84、SHA-512、SHA-512/224 或 SHA-512/256 的 HMAC。这与使用公钥认证时步骤 5A 中初始消化的内容完全相同。

### 5.2 从 PFX PDU 导入密钥等

从 PFX 导入基本上是创建 PFX 过程的逆向操作。一般来说，当应用程序从 PFX 导入密钥等内容时，应忽略不熟悉的对象标识符。有时，向用户提醒此类对象标识符的存在可能是合适的。

当导入 PFX 中的项目需要覆盖本地已存在的项目时，应用程序应特别小心。遇到此类项目时应用程序的行为可能取决于项目是什么（即 PKCS #8 遮蔽私钥和 CRL 可能需要不同处理）。适当的行为可能是询问用户应对此项目采取什么操作。

## 6. 安全考虑

> [!warning] 安全提醒
> 在隐私或完整性模式中使用密码时，需要考虑到基于密码的密码学通常在安全性方面存在局限，特别是对于本文档中定义的可以进行离线密码搜索的方法。虽然 salt 和迭代次数的使用可以增加攻击的复杂度，但密码的选择至关重要，应遵循相关指南（如 NIST SP 800-61-1）。如果密码被存储，良好的密码保护也很重要。

在密码隐私或完整性模式下选择 salt 值时，应考虑 PKCS #5 2.1 [13] [22] 第 4 节中的建议。理想情况下，salt 的长度应与所使用哈希函数的输出长度相同，并由随机生成的数据组成。

## 7. 规范引用

```
[1]   Dobbertin, H., "The status of MD5 after a recent attack.",
      CryptoBytes Vol. 2, #2, 1996.

[2]   ISO/IEC, "Information technology -- Abstract Syntax Notation
      One (ASN.1) -- Specification of basic notation", ISO/IEC
      8824-1:2008, 2008.

[3]   ISO/IEC, "Information technology -- Abstract Syntax Notation
      One (ASN.1) -- Information object specification", ISO/IEC
      8824-2:2008, 2008.

[4]   ISO/IEC, "Information technology -- Abstract Syntax Notation
      One (ASN.1) -- Constraint specification", ISO/IEC 88247-3:2008,
      2008.

[5]   ISO/IEC, "Information technology -- Abstract Syntax Notation
      One (ASN.1) -- Parameterization of ASN.1 specifications",
      ISO/IEC 8824-4:2008, 2008.

[6]   ISO/IEC, "Information Technology - ASN.1 Encoding Rules:
      Specification of Basic Encoding Rules (BER), Canonical Encoding
      Rules (CER), and Distinguished Encoding Rules", ISO/IEC
      8825-1:2008, 2008.

[7]   ISO/IEC, "Information technology -- Open Systems
      Interconnection -- The Directory: Models", ISO/IEC 9594-2:1997,
      1997.

[8]   ISO/IEC, "Information technology -- Open Systems
      Interconnection -- The Directory: Authentication Framework",
      ISO/IEC 9594-8:1997, 1997.

[9]   Microsoft, "PFX: Personal Exchange Syntax and Protocol
      Standard", ISO/IEC Version 0.020, January 1997.

[10]  National Institute of Standards and Technology (NIST), "Secure
      Hash Standard", FIPS Publication 180-4, March 2012.

[11]  National Institute of Standards and Technology (NIST), "The
      Keyed-Hash Message Authentication Code (HMAC)", FIPS
      Publication 198-1, July 2008.

[12]  National Institute of Standards and Technology (NIST), "The
      Recommendation for Password-Based Key Derivation, Part 1:
      Storage Applications", NIST Special Publication 800-132,
      December 2010.

[13]  RSA Laboratories, "PKCS #5: Password-Based Encryption
      Standard", PKCS Version 2.1, October 2012.

[14]  RSA Laboratories, "PKCS #7: Cryptographic Message Syntax
      Standard", PKCS Version 1.5, November 1993.

[15]  RSA Laboratories, "PKCS #8: Private-Key Information Syntax
      Standard", PKCS Version 1.2, November 1993.

[16]  RSA Laboratories, "PKCS #12: Personal Information Exchange
      Syntax", PKCS Version 1.1, December 2012.

[17]  Rivest, R. and B. Lampson, "SDSI - A Simple Distributed
      Security Infrastructure", 1996,
      <http://people.csail.mit.edu/rivest/sdsi10.html>.

[18]  Turner, S. and L. Chen, "MD2 to Historic Status", RFC 6149,
      March 2011.

[19]  Rivest, R., "The MD5 Message-Digest Algorithm", RFC 1321, April
      1992.

[20]  Krawczyk, H., Bellare, M., and R. Canetti, "HMAC: Keyed-
      Hashing for Message Authentication", RFC 2104, February 1997.

[21]  Kaliski, B., "PKCS #7: Cryptographic Message Syntax Version
      1.5", RFC 2315, March 1998.

[22]  Kaliski, B., "PKCS #5: Password-Based Cryptography
      Specification Version 2.0", RFC 2898, September 2000.

[23]  Nystrom, M. and B. Kaliski, "PKCS #9: Selected Object Classes
      and Attribute Types Version 2.0", RFC 2985, November 2000.

[24]  Turner, S., "Asymmetric Key Packages", RFC 5958, August 2010.

[25]  Turner, S. and L. Chen, "Updated Security Considerations for
      the MD5 Message-Digest and the HMAC-MD5 Algorithms", RFC 6151,
      March 2011.
```

## 附录 A. 消息认证码（MAC）

MAC 是消息（数据位）和完整性密钥的一种特殊函数。只有同时拥有消息和完整性密钥的人才能计算或验证它。其安全性基于完整性密钥的保密性。在本标准中，MAC 用于密码完整性模式。

本文档使用一种称为 HMAC [11] [20] 的特定 MAC 类型，它可以从多种哈希函数中的任何一种构建。注意 [20] 和 [11] 中的规范与 [9] 中的规范有所不同。HMAC 基于的哈希函数在保存 MAC 的 MacData 中标识；对于本标准此版本，哈希函数可以是以下之一：SHA-1、SHA-224、SHA-256、[[SHA-3]]84、SHA-512、SHA-512/224 或 SHA-512/256 [10]。如附录 B.4 所示，此结构意味着在密码完整性模式下必须使用相同的哈希算法来派生 MAC 密钥本身，且 MAC 密钥长度为 160、224、256、384 或 512 位。

当使用密码完整性模式保护 PFX PDU 时，对 PFX PDU 中 authSafe 字段的 content 字段内容的 BER 编码计算使用 SHA-1、SHA-224、SHA-256、[[SHA-3]]84、SHA-512、SHA-512/224 或 SHA-512/256 的 HMAC（见第 5.1 节）。

## 附录 B. 从密码和 Salt 派生密钥与 IV

> [!warning] 已弃用
> 此方法用于密码隐私模式**不推荐**，新用途中已弃用。应使用 PKCS #5 v2.1 [13] [22] 中定义的过程和算法替代。具体而言，应使用 PBES2 作为加密方案，PBKDF2 作为密钥派生函数。
>
> 此处介绍的方法仍用于在密码完整性模式下生成密钥。

以下介绍一种通用方法，使用哈希函数从密码和 salt 位串产生各种类型的伪随机位。此方法用于本标准中的密码隐私模式和密码完整性模式。

### B.1 密码格式

PKCS #5 v2.1 中底层的基于密码的加密方法将密码（和 salt）视为简单的字节串。本文档此版本中底层的基于密码的加密方法和基于密码的认证方法类似。

上述段落中未明确说明的是表示密码的字节串究竟从何而来。（这对 salt 串不是问题，因为 salt 作为基于密码的加密（或认证）参数提供。）PKCS #5 v2.1 说："[...] 密码被认为是任意长度的八位组串，其作为文本串的解释未指定。然而，为了互操作性，建议应用程序遵循一些通用的文本编码规则。ASCII 和 UTF-8 是两种可能的选择。"

然而，在本规范中，所有密码都从带有 NULL 终止符的 BMPString 创建。这意味着 BMPString 中的每个字符都以大端序格式（最高有效字节在前）编码为 2 个字节。没有 Unicode 字节顺序标记。BMPString 中最后一个字符产生的 2 个字节后面跟着 2 个值为 0x00 的额外字节。

用一个简单的例子说明，如果用户输入 6 字符密码 "Beavis"，PKCS #12 实现应将以下 14 字节串视为密码：

`0x00 0x42 0x00 0x65 0x00 0x61 0x00 0x76 0x00 0x69 0x00 0x73 0x00 0x00`

### B.2 通用方法

设 H 为围绕压缩函数 f 构建的哈希函数：

$$Z_2^u \times Z_2^v \rightarrow Z_2^u$$

（即 H 具有长度为 u 位的链式变量和输出，H 的压缩函数的消息输入为 v 位）。u 和 v 的值如下：

| 哈希函数 | u 值 | v 值 |
|----------|------|------|
| MD2, MD5 | 128 | 512 |
| SHA-1 | 160 | 512 |
| SHA-224 | 224 | 512 |
| SHA-256 | 256 | 512 |
| [[SHA-3]]84 | 384 | 1024 |
| SHA-512 | 512 | 1024 |
| SHA-512/224 | 224 | 1024 |
| SHA-512/256 | 256 | 1024 |

此外，设 r 为迭代次数。

这里假设 u 和 v 都是 8 的倍数，密码和 salt 串的长度（分别记为 p 和 s）以及所需的伪随机位数 n 也是如此。此外，u 和 v 当然是非零的。

关于 MD5 [19] 的安全考虑，参见 [25] 和 [1]；关于 MD2 的安全考虑，参见 [18]。

以下过程可用于为特定"目的"产生伪随机位，该目的由称为 "ID" 的字节标识。此 ID 字节的含义将在后面讨论。

1. 通过连接 v/8 个 ID 副本来构造字符串 D（"diversifier"， diversifier）。
2. 将 salt 的副本连接在一起，创建长度为 v(ceiling(s/v)) 位的字符串 S（salt 的最后一个副本可能被截断以创建 S）。注意如果 salt 是空字符串，则 S 也是。
3. 将密码的副本连接在一起，创建长度为 v(ceiling(p/v)) 位的字符串 P（密码的最后一个副本可能被截断以创建 P）。注意如果密码是空字符串，则 P 也是。
4. 设 I = S || P，即 S 和 P 的连接。
5. 设 c = ceiling(n/u)。
6. 对于 i = 1, 2, ..., c，执行以下操作：
   - **A.** 设 A_i = H^r(D || I)。（即 D||I 的第 r 次哈希，H(H(H(... H(D||I))))）
   - **B.** 将 A_i 的副本连接起来创建长度为 v 位的字符串 B（A_i 的最后一个副本可能被截断以创建 B）。
   - **C.** 将 I 视为 v 位块 I_0, I_1, ..., I_(k-1) 的连接，其中 k = ceiling(s/v) + ceiling(p/v)，通过对每个 j 设 I_j = (I_j + B + 1) mod 2^v 来修改 I。
7. 将 A_1, A_2, ..., A_c 连接在一起形成伪随机位串 A。
8. 使用 A 的前 n 位作为整个过程的输出。

> [!tip] 关于 DES 密钥
> 如果上述过程用于生成 DES 密钥，应使用该过程创建 64 个随机位，并在产生 64 位后设置密钥的奇偶校验位。类似的考虑也适用于 2 密钥和 3 密钥三重 DES 密钥、CDMF 密钥以及任何内置奇偶校验位的类似密钥。

### B.3 关于 ID 字节

本标准为上述 ID 字节指定了 3 个不同的值：

1. **ID=1**：产生的伪随机位将用作执行加密或解密的密钥材料。
2. **ID=2**：产生的伪随机位将用作加密或解密的 IV（Initial Value，初始值）。
3. **ID=3**：产生的伪随机位将用作 MAC 操作的完整性密钥。

### B.4 密码完整性模式的密钥

当使用密码完整性模式保护 PFX PDU 时，使用密码和 salt 来派生 MAC 密钥。与密码隐私模式一样，密码是 Unicode 字符串，salt 是字节串。本标准未对密码或 salt 规定特定长度，但附录 C 中关于密码和 salt 的一般建议在此也适用。

用于派生 MAC 密钥的哈希函数就是用于 MAC 操作的哈希函数。派生的 MAC 密钥与哈希函数的输出长度相同。在本标准此版本中，SHA-1、SHA-224、SHA-256、[[SHA-3]]84、SHA-512、SHA-512/224 或 SHA-512/256 可用于 MAC 操作，因此 MAC 密钥可以是 160、224、256、384 或 512 位。关于 MAC 操作的更多信息请参阅附录 A。

## 附录 C. 密码隐私模式的密钥和 IV

> [!warning] 已弃用
> 如附录 B 开头所述，此方法用于密码隐私模式不推荐；此密钥和 IV 规范仅为与 PKCS #12 v1.0 的向后兼容性而保留。

当使用密码隐私模式加密 PFX PDU 时，使用密码（通常由用户输入）、salt 和迭代参数来派生密钥（以及 IV，如有必要）。密码是 Unicode 字符串，因此每个字符由 2 个字节表示。salt 是字节串，可以直接表示为字节序列。

本标准未规定密码的长度。然而，过短的密码可能会损害隐私性。特定应用程序可能要求用户为创建 PFX PDU 输入的隐私密码超过某个特定长度。

本标准也未规定 salt 的长度。理想情况下，salt 的长度应与所使用哈希函数的输出长度相同，并由完全随机的位组成。

迭代次数建议为 1024 或更多。（更多信息参见 [22] 和 [13]。）

PKCS #5 中定义的 PBES1 加密方案提供了多个用于派生密钥和 IV 的算法标识符；这里我们再指定几个，它们都使用附录 B.2 和 B.3 中详述的过程来构造密钥（以及 IV，如有需要）。顾名思义，以下所有对象标识符都使用 SHA-1 哈希函数。

```
pkcs-12PbeIds                    OBJECT IDENTIFIER ::= {pkcs-12 1}
pbeWithSHAAnd128BitRC4           OBJECT IDENTIFIER ::= {pkcs-12PbeIds 1}
pbeWithSHAAnd40BitRC4            OBJECT IDENTIFIER ::= {pkcs-12PbeIds 2}
pbeWithSHAAnd3-KeyTripleDES-CBC  OBJECT IDENTIFIER ::= {pkcs-12PbeIds 3}
pbeWithSHAAnd2-KeyTripleDES-CBC  OBJECT IDENTIFIER ::= {pkcs-12PbeIds 4}
pbeWithSHAAnd128BitRC2-CBC       OBJECT IDENTIFIER ::= {pkcs-12PbeIds 5}
pbewithSHAAnd40BitRC2-CBC        OBJECT IDENTIFIER ::= {pkcs-12PbeIds 6}
```

上述六个 PBE 对象标识符各自具有以下 [[ASN.1]] 参数类型：

```
pkcs-12PbeParams ::= SEQUENCE {
    salt        OCTET STRING,
    iterations  INTEGER
}
```

pkcs-12PbeParams 保存用于生成密钥（以及 IV，如有必要）的 salt 和要执行的迭代次数。

> [!note]
> 上述前两个算法标识符（RC4 的算法标识符）只派生密钥；RC4 不需要派生 IV。

本节存在有两个原因：首先，如本节第一段所述，为了实现向后兼容性；其次，因为它在密码完整性模式中仍然使用。为了不在密码完整性模式中使用它，[[ASN.1]] 定义需要更新。本文档建议未来 PFX 结构的定义用新的对象定义替换现有的 MacData 对象（在密码完整性模式中可选存在），该新对象保存基于 PKCS#5 [13] [22] PBMAC1 消息认证方案的 MAC。此更改将简化 PFX 结构各部分使用[[的密钥派生函数]]的要求。

## 附录 D. ASN.1 模块

本附录记录本规范中定义的所有 [[ASN.1]] 类型、值和对象集。它通过提供一个名为 PKCS-12 的 [[ASN.1]] 模块来实现这一点。

```
PKCS-12 {
    iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-12(12)
    modules(0) pkcs-12(1)}

-- PKCS #12 v1.1 ASN.1 Module
-- Revised October 27, 2012

-- This module has been checked for conformance with the ASN.1 standard
-- by the OSS ASN.1 Tools

DEFINITIONS IMPLICIT TAGS ::=

BEGIN

-- EXPORTS ALL
-- All types and values defined in this module are exported for use
-- in other ASN.1 modules.

IMPORTS

informationFramework
    FROM UsefulDefinitions {joint-iso-itu-t(2) ds(5) module(1)
                            usefulDefinitions(0) 3}

ATTRIBUTE
    FROM InformationFramework informationFramework

ContentInfo, DigestInfo
    FROM PKCS-7 {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
                 pkcs-7(7) modules(0) pkcs-7(1)}

PrivateKeyInfo, EncryptedPrivateKeyInfo
    FROM PKCS-8 {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
                 pkcs-8(8) modules(1) pkcs-8(1)}

pkcs-9, friendlyName, localKeyId, certTypes, crlTypes
    FROM PKCS-9 {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
                 pkcs-9(9) modules(0) pkcs-9(1)};

-- ============================
-- Object identifiers
-- ============================

rsadsi  OBJECT IDENTIFIER ::= {iso(1) member-body(2) us(840)
                               rsadsi(113549)}
pkcs    OBJECT IDENTIFIER ::= {rsadsi pkcs(1)}
pkcs-12 OBJECT IDENTIFIER ::= {pkcs 12}
pkcs-12PbeIds OBJECT IDENTIFIER ::= {pkcs-12 1}
pbeWithSHAAnd128BitRC4          OBJECT IDENTIFIER ::= {pkcs-12PbeIds 1}
pbeWithSHAAnd40BitRC4           OBJECT IDENTIFIER ::= {pkcs-12PbeIds 2}
pbeWithSHAAnd3-KeyTripleDES-CBC OBJECT IDENTIFIER ::= {pkcs-12PbeIds 3}
pbeWithSHAAnd2-KeyTripleDES-CBC OBJECT IDENTIFIER ::= {pkcs-12PbeIds 4}
pbeWithSHAAnd128BitRC2-CBC      OBJECT IDENTIFIER ::= {pkcs-12PbeIds 5}
pbewithSHAAnd40BitRC2-CBC       OBJECT IDENTIFIER ::= {pkcs-12PbeIds 6}

bagtypes OBJECT IDENTIFIER ::= {pkcs-12 10 1}

-- ============================
-- The PFX PDU
-- ============================

PFX ::= SEQUENCE {
    version    INTEGER {v3(3)}(v3,...),
    authSafe   ContentInfo,
    macData    MacData OPTIONAL
}

MacData ::= SEQUENCE {
    mac        DigestInfo,
    macSalt    OCTET STRING,
    iterations INTEGER DEFAULT 1
    -- Note: The default is for historical reasons and its use is
    -- deprecated.
}

AuthenticatedSafe ::= SEQUENCE OF ContentInfo
    -- Data if unencrypted
    -- EncryptedData if password-encrypted
    -- EnvelopedData if public key-encrypted

SafeContents ::= SEQUENCE OF SafeBag

SafeBag ::= SEQUENCE {
    bagId         BAG-TYPE.&id ({PKCS12BagSet}),
    bagValue      [0] EXPLICIT BAG-TYPE.&Type({PKCS12BagSet}{@bagId}),
    bagAttributes SET OF PKCS12Attribute OPTIONAL
}

-- ============================
-- Bag types
-- ============================

keyBag BAG-TYPE ::=
    {KeyBag              IDENTIFIED BY {bagtypes 1}}
pkcs8ShroudedKeyBag BAG-TYPE ::=
    {PKCS8ShroudedKeyBag IDENTIFIED BY {bagtypes 2}}
certBag BAG-TYPE ::=
    {CertBag             IDENTIFIED BY {bagtypes 3}}
crlBag BAG-TYPE ::=
    {CRLBag              IDENTIFIED BY {bagtypes 4}}
secretBag BAG-TYPE ::=
    {SecretBag           IDENTIFIED BY {bagtypes 5}}
safeContentsBag BAG-TYPE ::=
    {SafeContents        IDENTIFIED BY {bagtypes 6}}

PKCS12BagSet BAG-TYPE ::= {
    keyBag |
    pkcs8ShroudedKeyBag |
    certBag |
    crlBag |
    secretBag |
    safeContentsBag,
    ... -- For future extensions
}

BAG-TYPE ::= TYPE-IDENTIFIER

-- KeyBag
KeyBag ::= PrivateKeyInfo

-- Shrouded KeyBag
PKCS8ShroudedKeyBag ::= EncryptedPrivateKeyInfo

-- CertBag
CertBag ::= SEQUENCE {
    certId    BAG-TYPE.&id   ({CertTypes}),
    certValue [0] EXPLICIT BAG-TYPE.&Type ({CertTypes}{@certId})
}

x509Certificate BAG-TYPE ::=
    {OCTET STRING IDENTIFIED BY {certTypes 1}}
    -- DER-encoded X.509 certificate stored in OCTET STRING
sdsiCertificate BAG-TYPE ::=
    {IA5String IDENTIFIED BY {certTypes 2}}
    -- Base64-encoded SDSI certificate stored in IA5String

CertTypes BAG-TYPE ::= {
    x509Certificate |
    sdsiCertificate,
    ... -- For future extensions
}

-- CRLBag
CRLBag ::= SEQUENCE {
    crlId     BAG-TYPE.&id ({CRLTypes}),
    crltValue [0] EXPLICIT BAG-TYPE.&Type ({CRLTypes}{@crlId})
}

x509CRL BAG-TYPE ::=
    {OCTET STRING IDENTIFIED BY {crlTypes 1}}
    -- DER-encoded X.509 CRL stored in OCTET STRING

CRLTypes BAG-TYPE ::= {
    x509CRL,
    ... -- For future extensions
}

-- Secret Bag
SecretBag ::= SEQUENCE {
    secretTypeId  BAG-TYPE.&id ({SecretTypes}),
    secretValue   [0] EXPLICIT BAG-TYPE.&Type ({SecretTypes}
                                               {@secretTypeId})
}

SecretTypes BAG-TYPE ::= {
    ... -- For future extensions
}

-- ============================
-- Attributes
-- ============================

PKCS12Attribute ::= SEQUENCE {
    attrId      ATTRIBUTE.&id ({PKCS12AttrSet}),
    attrValues  SET OF ATTRIBUTE.&Type ({PKCS12AttrSet}{@attrId})
} -- This type is compatible with the X.500 type 'Attribute'

PKCS12AttrSet ATTRIBUTE ::= {
    friendlyName |
    localKeyId,
    ... -- Other attributes are allowed
}

END
```

## 附录 E. 知识产权考虑

EMC Corporation 不对本文档中描述的通用构造提出专利主张，但特定的底层技术可能受到专利保护。

RC2 和 RC4 是 EMC Corporation 的商标。

EMC Corporation 不对他方的知识产权主张做出任何陈述。此类判定是用户的责任。

## 附录 F. 致谢

非常感谢 Microsoft Corporation 的 Dan Simon 和 Netscape Communications Corporation 的 Jim Spring 在准备本文档早期草案中的协助。特别感谢 Microsoft Corporation 的 Brian Beckman 撰写了本文档所基于的规范。

## 附录 G. 关于 PKCS

公钥密码标准（Public-Key Cryptography Standards）是由 RSA Laboratories 与全球安全系统开发者合作制定的规范，旨在加速公钥密码学的部署。PKCS 文档最初于 1991 年作为与一小批公钥技术早期采用者会议的结果发布，现已被广泛引用和实现。PKCS 系列的贡献已成为许多正式和事实标准的一部分，包括 ANSI X9 文档、PKIX、SET、[[S/MIME]] 和 SSL。

PKCS 的进一步发展通过 IETF 进行。欢迎提出改进建议。

## 作者地址

- **Kathleen M. Moriarty**（编辑），EMC Corporation，176 South Street，Hopkinton，MA，United States，Kathleen.Moriarty@emc.com
- **Magnus Nystrom**，Microsoft Corporation，1 Microsoft Way，Redmond，WA 98052，United States，mnystrom@microsoft.com
- **Sean Parkinson**，RSA Security Inc.，345 Queen Street，Brisbane，QLD，4000，Australia，Sean.Parkinson@rsa.com
- **Andreas Rusch**，RSA Security Inc.，345 Queen Street，Brisbane，QLD，4000，Australia，Andreas.Rusch@rsa.com
- **Michael Scott**，RSA Security Inc.，345 Queen Street，Brisbane，QLD，4000，Australia，Michael2.Scott@rsa.com
