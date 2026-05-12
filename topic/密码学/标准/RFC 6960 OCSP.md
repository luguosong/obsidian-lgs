---
title: RFC 6960 在线证书状态协议 OCSP
description: 定义 X.509 公钥基础设施中的在线证书状态协议（OCSP），用于实时查询数字证书的吊销状态，无需依赖证书吊销列表（CRL）。
tags:
  - 密码学
  - OCSP
  - 证书吊销
  - PKI
  - RFC
---

> [!info] RFC 信息
> **RFC 编号**：6960
> **标题**：X.509 Internet Public Key Infrastructure — Online Certificate Status Protocol - OCSP
> **类别**：Standards Track
> **日期**：2013 年 6 月
> **作者**：S. Santesson (3xA Security), M. Myers (TraceRoute Security), R. Ankney, A. Malpani (CA Technologies), S. Galperin (A9), C. Adams (University of Ottawa)
> **废止**：RFC 2560, RFC 6277
> **更新**：RFC 5912

## 摘要

本文档规定了一种协议，用于确定数字证书的当前状态，而无需依赖证书吊销列表（CRL, Certificate Revocation List）。解决 PKIX 运营需求的其他机制在独立文档中规定。本文档废止了 RFC 2560 和 RFC 6277，同时更新了 RFC 5912。

## 1. 引言

本文档规定了一种协议，用于在不依赖 CRL 的情况下确定数字证书的当前状态。其他解决 PKIX 运营需求的机制在独立文档中规定。

本规范废止了 [RFC2560] 和 [RFC6277]。发布本文档的主要原因是解决 RFC 2560 发布以来发现的歧义。本文档与 RFC 2560 仅在以下方面存在差异：

- 第 2.2 节扩展了 "revoked"（已吊销）响应的使用范围，允许对从未签发的证书也返回此响应状态。
- 第 2.3 节扩展了 "unauthorized"（未授权）错误响应的使用，如 [RFC5019] 所规定。
- 第 4.2.1 节和第 4.2.2.3 节说明响应可以包含请求中未涉及的证书的吊销状态信息，如 [RFC5019] 所允许。
- 第 4.2.2.2 节明确了何时将 responder（响应器）视为 Authorized Responder（授权响应器）。
- 第 4.2.2.3 节明确了 ResponderID 字段对应 OCSP responder 的签名证书。
- 第 4.3 节修改了客户端必须支持和应当支持的密码算法集合，如 [RFC6277] 所规定。
- 第 4.4.1 节为 nonce（随机数）扩展补充了 RFC 2560 中缺失的 [[ASN.1]] 语法定义。
- 第 4.4.7 节规定了一种新扩展，可在请求消息中指定客户端偏好服务器用于签名响应的签名算法，如 [RFC6277] 所规定。
- 第 4.4.8 节规定了一种新扩展，表明 responder 支持对未签发证书使用扩展的 "revoked" 响应，见第 2.2 节定义。
- 附录 B.2 提供了使用 [[ASN.1]] 2008 语法的 [[ASN.1]] 模块，更新了 [RFC5912]。

协议概述见第 2 节，功能需求见第 3 节，协议细节见第 4 节，安全问题在第 5 节讨论。附录 A 定义了基于 HTTP 的 OCSP 传输，附录 B 提供了 [[ASN.1]] 语法元素，附录 C 规定了消息的 MIME 类型。

### 1.1 规范语言

本文档中的关键词 "MUST"、"MUST NOT"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"SHOULD NOT"、"RECOMMENDED"、"MAY" 和 "OPTIONAL" 应按 RFC 2119 [RFC2119] 的描述进行解释。

## 2. 协议概述

作为定期检查 CRL 的替代或补充，有时需要获取有关证书吊销状态的及时信息（参见 [RFC5280] 第 3.3 节）。典型场景包括高额资金转账或大额股票交易。

在线证书状态协议（OCSP, Online Certificate Status Protocol）使应用程序能够确定已识别证书的（吊销）状态。OCSP 可用于满足比 CRL 更及时地提供吊销信息的运营需求，也可用于获取额外的状态信息。OCSP 客户端向 OCSP responder 发出状态请求，在 responder 提供响应之前暂停对所涉证书的接受。

本协议规定了检查一个或多个证书状态的应用程序与提供相应状态的服务器之间需要交换的数据。

### 2.1 请求

OCSP 请求包含以下数据：

- 协议版本
- 服务请求
- 目标证书标识符
- 可选扩展（OCSP responder MAY（可以）处理）

收到请求后，OCSP responder 判断：

1. 消息格式是否正确
2. responder 是否配置为提供所请求的服务
3. 请求是否包含 responder 所需的信息

如果以上任一条件不满足，OCSP responder 生成错误消息；否则返回确定性响应。

### 2.2 响应

OCSP 响应有多种类型。一个 OCSP 响应由响应类型和实际响应的字节组成。有一种基本的 OCSP 响应类型，所有 OCSP 服务器和客户端 MUST（必须）支持。本节其余部分仅涉及此基本响应类型。

所有确定性响应消息 SHALL（应当）进行[[数字签名]]。用于签名响应的密钥 MUST 属于以下之一：

- 签发所涉证书的 CA（证书颁发机构）
- 其公钥被请求方信任的 Trusted Responder（可信响应器）
- CA 指定的 responder（Authorized Responder（授权响应器），在第 4.2.2.2 节中定义），持有由 CA 直接签发的、带有特殊标记的证书，表明该 responder 可以为该 CA 签发 OCSP 响应

确定性响应消息由以下部分组成：

- 响应语法版本
- responder 标识符
- 响应生成时间
- 请求中每个证书的响应
- 可选扩展
- 签名算法 OID
- 对响应哈希值计算的签名

请求中每个证书的响应由以下部分组成：

- 目标证书标识符
- 证书状态值
- 响应有效期区间
- 可选扩展

本规范定义了以下用于证书状态值的确定性响应指示：

- **good**（良好）
- **revoked**（已吊销）
- **unknown**（未知）

> [!note] "good" 状态
> "good" 状态表示对状态查询的正面响应。至少，此正面响应表示在当前有效期内，不存在具有所请求证书序列号的已吊销证书。此状态不一定意味着该证书曾经被签发过，也不意味着响应生成的时间在证书有效期内。响应扩展可用于传递 responder 对证书状态所作的附加声明信息，例如关于签发、有效性等的正面声明。

> [!note] "revoked" 状态
> "revoked" 状态表示证书已被吊销，可以是临时吊销（吊销原因为 certificateHold）或永久吊销。如果关联的 CA 没有使用任何当前或以前的签发密钥签发过具有请求中证书序列号的证书的记录，此状态也可以被返回（在本文档中称为 "non-issued"（未签发）证书）。

> [!warning] "revoked" 与 "unknown" 的区别
> "revoked" 状态表示具有所请求序列号的证书应当被拒绝，而 "unknown" 状态表示此 responder 无法确定证书状态，从而允许客户端决定是否尝试其他状态信息来源（如 CRL）。这使得 "revoked" 响应适合用于未签发证书的情况——此时 responder 的意图是使客户端拒绝该证书，而不是去尝试其他状态信息来源。为了保持与 RFC 2560 部署的向后兼容性，对未签发证书使用 "revoked" 状态仍然是可选的。例如，responder 可能不知道某个请求的序列号是否被分配给了任何已签发的证书，或者 responder 可能按照 RFC 5019 提供预生成的响应，因此无法为所有未签发证书序列号提供签名响应。

当 responder 对未签发证书的状态请求发送 "revoked" 响应时，responder MUST 在响应中包含扩展吊销定义响应扩展（第 4.4.8 节），表明 OCSP responder 支持将 "revoked" 状态的扩展定义也覆盖未签发证书。此外，与该未签发证书相关的 SingleResponse：

- MUST 指定吊销原因为 certificateHold (6)
- MUST 指定 revocationTime 为 1970 年 1 月 1 日
- MUST NOT 包含 CRL 引用扩展（第 4.4.2 节）或任何 CRL 条目扩展（第 4.4.5 节）

### 2.3 异常情况

发生错误时，OCSP responder 可以返回错误消息。这些消息不进行签名。错误类型包括：

- **malformedRequest**（格式错误的请求）
- **internalError**（内部错误）
- **tryLater**（稍后重试）
- **sigRequired**（需要签名）
- **unauthorized**（未授权）

当收到的请求不符合 OCSP 语法时，服务器产生 "malformedRequest" 响应。

"internalError" 响应表示 OCSP responder 达到了不一致的内部状态。应当重试查询，可以尝试其他 responder。

当 OCSP responder 处于运行状态但无法返回所请求证书的状态时，可以使用 "tryLater" 响应表示服务存在但暂时无法响应。

当服务器要求客户端对请求进行签名才能构造响应时，返回 "sigRequired" 响应。

当客户端未被授权向此服务器发起此查询，或服务器无法权威地响应时（参见 [RFC5019] 第 2.2.3 节），返回 "unauthorized" 响应。

### 2.4 thisUpdate、nextUpdate 和 producedAt 的语义

本文档定义的响应可以包含四个时间字段——thisUpdate、nextUpdate、producedAt 和 revocationTime。这些字段的语义如下：

| 字段 | 语义 |
|------|------|
| **thisUpdate** | responder 确知所指示状态为正确的最近时间 |
| **nextUpdate** | 在此时间或之前将可获得关于证书状态的新信息 |
| **producedAt** | OCSP responder 签名此响应的时间 |
| **revocationTime** | 证书被吊销或被暂停的时间 |

### 2.5 响应预生成

OCSP responder MAY 预生成签名响应，指定证书在特定时间的状态。状态确知为正确的时间 SHALL 反映在响应的 thisUpdate 字段中。可获得新信息的时间反映在 nextUpdate 字段中，而响应生成的时间出现在 producedAt 字段中。

### 2.6 OCSP 签名权限委托

签名证书状态信息的密钥不必与签名证书的密钥相同。证书签发者通过在 OCSP signer 的证书中签发包含扩展密钥用途扩展（extended key usage extension，定义在 [RFC5280] 第 4.2.1.12 节）的唯一值来显式委托 OCSP 签名权限。此证书 MUST 由主管 CA 直接签发给 responder。详见第 4.2.2.2 节。

### 2.7 CA 密钥泄露

如果 OCSP responder 知道某个 CA 的私钥已泄露，它 MAY 对该 CA 签发的所有证书返回 "revoked" 状态。

## 3. 功能需求

### 3.1 证书内容

为了向 OCSP 客户端传达一个众所周知的信息访问点，CA SHALL 提供在使用 OCSP 可检查的证书中包含授权信息访问扩展（authority information access extension，定义在 [RFC5280] 第 4.2.2.1 节）的能力。或者，OCSP provider 的 accessLocation 可以在 OCSP 客户端本地配置。

支持 OCSP 服务（无论是本地托管还是由 Authorized Responder 提供）的 CA MUST 提供在 AccessDescription SEQUENCE 中包含 URI [RFC[[3986]]] accessLocation 值和 id-ad-ocsp accessMethod OID 值的能力。

主体证书中 accessLocation 字段的值定义了用于访问 OCSP responder 的传输方式（如 HTTP），并可包含其他传输相关的信息（如 URL）。

### 3.2 签名响应接受要求

在接受特定证书的签名响应为有效之前，OCSP 客户端 SHALL 确认：

1. 收到的响应中标识的证书与相应请求中标识的证书相对应
2. 响应上的签名有效
3. 签名者的身份与请求的预期接收者匹配
4. 签名者当前被授权为所涉证书提供响应
5. 所指示状态确知为正确的时间（thisUpdate）足够近
6. 当可用时，可获得关于证书状态新信息的时间（nextUpdate）大于当前时间

## 4. 协议细节

[[ASN.1]] 语法导入了 [RFC5280] 中定义的术语。对于签名计算，待签名的数据使用 [[ASN.1]] 可分辨编码规则（DER, Distinguished Encoding Rules）[X.690] 进行编码。

除非另有说明，[[ASN.1]] 默认使用 EXPLICIT 标记。

从其他地方导入的术语包括：Extensions、CertificateSerialNumber、SubjectPublicKeyInfo、Name、AlgorithmIdentifier 和 CRLReason。

### 4.1 请求语法

本节规定了确认请求的 [[ASN.1]] 规范。消息的实际格式可能因所使用的传输机制（HTTP、SMTP、LDAP 等）而异。

#### 4.1.1 OCSP 请求的 ASN.1 规范

对应 OCSPRequest 的 [[ASN.1]] 结构如下：

```asn1
OCSPRequest     ::=     SEQUENCE {
    tbsRequest                  TBSRequest,
    optionalSignature   [0]     EXPLICIT Signature OPTIONAL }

TBSRequest      ::=     SEQUENCE {
    version             [0]     EXPLICIT Version DEFAULT v1,
    requestorName       [1]     EXPLICIT GeneralName OPTIONAL,
    requestList                 SEQUENCE OF Request,
    requestExtensions   [2]     EXPLICIT Extensions OPTIONAL }

Signature       ::=     SEQUENCE {
    signatureAlgorithm      AlgorithmIdentifier,
    signature               BIT STRING,
    certs               [0] EXPLICIT SEQUENCE OF Certificate
OPTIONAL}

Version         ::=             INTEGER  {  v1(0) }

Request         ::=     SEQUENCE {
    reqCert                     CertID,
    singleRequestExtensions     [0] EXPLICIT Extensions OPTIONAL }

CertID          ::=     SEQUENCE {
    hashAlgorithm       AlgorithmIdentifier,
    issuerNameHash      OCTET STRING, -- Hash of issuer's DN
    issuerKeyHash       OCTET STRING, -- Hash of issuer's public key
    serialNumber        CertificateSerialNumber }
```

OCSPRequest 中各字段的含义如下：

- **tbsRequest** 是可选签名的 OCSP 请求。
- **optionalSignature** 包含 signatureAlgorithm 中的算法标识符及关联参数；signature 中的签名值；以及可选地，服务器验证签名响应所需的证书（通常到但不包括客户端的根证书）。

TBSRequest 包含以下字段：

- **version** 表示协议版本，本文档为 v1(0)。
- **requestorName** 是可选的，表示 OCSP 请求者的名称。
- **requestList** 包含一个或多个单独的证书状态请求。
- **requestExtensions** 是可选的，包含适用于 reqCert 中请求的扩展。参见第 4.4 节。

Request 包含以下字段：

- **reqCert** 包含目标证书的标识符。
- **singleRequestExtensions** 是可选的，包含适用于此单个证书状态请求的扩展。参见第 4.4 节。

CertID 包含以下字段：

- **hashAlgorithm** 是用于生成 issuerNameHash 和 issuerKeyHash 值的哈希算法。
- **issuerNameHash** 是签发者可分辨名称（DN）的哈希值。该哈希应基于待检查证书中签发者名称字段的 DER 编码计算。
- **issuerKeyHash** 是签发者公钥的哈希值。该哈希应基于签发者证书中主体公钥字段的值（不包括标签和长度）计算。
- **serialNumber** 是请求状态的证书的序列号。

#### 4.1.2 OCSP 请求说明

除了使用 CA 名称的哈希外，还使用 CA 公钥哈希来标识签发者的主要原因是：两个 CA 可能选择使用相同的 Name（Name 的唯一性是无法强制执行的建议）。然而，除非两个 CA 显式决定共享其私钥，或者其中一个 CA 的密钥被泄露，否则两个 CA 永远不会有相同的公钥。

对任何特定扩展的支持都是 OPTIONAL。所有扩展的 critical 标志 SHOULD NOT（不应）被设置。第 4.4 节建议了几种有用的扩展。附加扩展 MAY 在附加 RFC 中定义。未识别的扩展 MUST 被忽略（除非它们设置了 critical 标志且未被理解）。

请求者 MAY 选择对 OCSP 请求进行签名。在这种情况下，签名基于 tbsRequest 结构计算。如果请求已签名，请求者 SHALL 在 requestorName 字段中指定其名称。此外，对于已签名的请求，请求者 MAY 在 Signature 的 certs 字段中包含帮助 OCSP responder 验证请求者签名的证书。

### 4.2 响应语法

本节规定了确认响应的 [[ASN.1]] 规范。消息的实际格式可能因所使用的传输机制（HTTP、SMTP、LDAP 等）而异。

#### 4.2.1 OCSP 响应的 ASN.1 规范

OCSP 响应至少包含一个 responseStatus 字段，指示先前请求的处理状态。如果 responseStatus 的值是某种错误条件，则不设置 responseBytes 字段。

```asn1
OCSPResponse ::= SEQUENCE {
   responseStatus         OCSPResponseStatus,
   responseBytes          [0] EXPLICIT ResponseBytes OPTIONAL }

OCSPResponseStatus ::= ENUMERATED {
    successful            (0),  -- Response has valid confirmations
    malformedRequest      (1),  -- Illegal confirmation request
    internalError         (2),  -- Internal error in issuer
    tryLater              (3),  -- Try again later
                                -- (4) is not used
    sigRequired           (5),  -- Must sign the request
    unauthorized          (6)   -- Request unauthorized
}
```

responseBytes 的值由一个 OBJECT IDENTIFIER 和由该 OID 标识的响应语法（编码为 OCTET STRING）组成。

```asn1
ResponseBytes ::=       SEQUENCE {
    responseType   OBJECT IDENTIFIER,
    response       OCTET STRING }
```

对于基本 OCSP responder，responseType 将为 id-pkix-ocsp-basic。

```asn1
id-pkix-ocsp           OBJECT IDENTIFIER ::= { id-ad-ocsp }
id-pkix-ocsp-basic     OBJECT IDENTIFIER ::= { id-pkix-ocsp 1 }
```

OCSP responder SHALL 能够生成 id-pkix-ocsp-basic 响应类型的响应。相应地，OCSP 客户端 SHALL 能够接收和处理 id-pkix-ocsp-basic 响应类型的响应。

response 的值 SHALL 为 BasicOCSPResponse 的 DER 编码。

```asn1
BasicOCSPResponse       ::= SEQUENCE {
   tbsResponseData      ResponseData,
   signatureAlgorithm   AlgorithmIdentifier,
   signature            BIT STRING,
   certs            [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }
```

signature 的值 SHALL 基于 ResponseData 的 DER 编码的哈希计算。responder MAY 在 BasicOCSPResponse 的 certs 字段中包含帮助 OCSP 客户端验证 responder 签名的证书。如果不包含证书，则 certs SHOULD（应该）省略。

```asn1
ResponseData ::= SEQUENCE {
   version              [0] EXPLICIT Version DEFAULT v1,
   responderID              ResponderID,
   producedAt               GeneralizedTime,
   responses                SEQUENCE OF SingleResponse,
   responseExtensions   [1] EXPLICIT Extensions OPTIONAL }

ResponderID ::= CHOICE {
   byName               [1] Name,
   byKey                [2] KeyHash }

KeyHash ::= OCTET STRING -- SHA-1 hash of responder's public key
(excluding the tag and length fields)

SingleResponse ::= SEQUENCE {
   certID                       CertID,
   certStatus                   CertStatus,
   thisUpdate                   GeneralizedTime,
   nextUpdate         [0]       EXPLICIT GeneralizedTime OPTIONAL,
   singleExtensions   [1]       EXPLICIT Extensions OPTIONAL }

CertStatus ::= CHOICE {
    good        [0]     IMPLICIT NULL,
    revoked     [1]     IMPLICIT RevokedInfo,
    unknown     [2]     IMPLICIT UnknownInfo }

RevokedInfo ::= SEQUENCE {
    revocationTime              GeneralizedTime,
    revocationReason    [0]     EXPLICIT CRLReason OPTIONAL }

UnknownInfo ::= NULL
```

#### 4.2.2 OCSP 响应说明

##### 4.2.2.1 时间

响应可以包含四个时间——thisUpdate、nextUpdate、producedAt 和 revocationTime。这些字段的语义在第 2.4 节中定义。GeneralizedTime 的格式如 [RFC5280] 第 4.1.2.5.2 节所规定。

thisUpdate 和 nextUpdate 字段定义了一个推荐的有效区间。此区间对应于 CRL 中的 {thisUpdate, nextUpdate} 区间。nextUpdate 值早于本地系统时间的响应 SHOULD（应该）被视为不可靠。thisUpdate 时间晚于本地系统时间的响应 SHOULD 被视为不可靠。

如果未设置 nextUpdate，则 responder 表示新的吊销信息始终可用。

##### 4.2.2.2 授权响应器（Authorized Responders）

签名证书状态信息的密钥不必与签名证书的密钥相同。然而，必须确保签名此信息的实体被授权这样做。因此，证书签发者 MUST 执行以下操作之一：

- 自行签名 OCSP 响应，或
- 显式将此权限委托给另一个实体

OCSP 签名委托 SHALL 通过在 OCSP 响应签名者证书中包含的扩展密钥用途证书扩展中纳入 id-kp-OCSPSigning 来指定。此证书 MUST 由请求中标识的 CA 直接签发。

> [!tip] 使用相同的签发密钥
> CA SHOULD 使用与签名待检查吊销状态的证书相同的签发密钥来签发委托证书。依赖 OCSP 响应的系统 MUST 仅当委托证书和待检查吊销状态的证书由同一密钥签名时，才将委托证书识别为由签发所涉证书的 CA 所签发。

> [!warning] 向后兼容性说明
> 为了与 RFC 2560 [RFC2560] 向后兼容，并不禁止使用与签名待检查吊销状态证书不同的签发密钥来签发 Authorized Responder 的证书。然而，这种做法强烈不建议使用，因为客户端不要求将持有此类证书的 responder 识别为 Authorized Responder。

```asn1
id-kp-OCSPSigning OBJECT IDENTIFIER ::= {id-kp 9}
```

依赖 OCSP 响应的系统或应用程序 MUST 能够检测和执行上述 id-kp-OCSPSigning 值的使用。它们 MAY 提供本地配置一个或多个 OCSP 签名权限机构并指定每个签名权限机构所信任的 CA 集合的方法。如果验证响应签名所需的证书不满足以下至少一个条件，它们 MUST 拒绝该响应：

1. 与所涉证书的 OCSP 签名权限机构的本地配置匹配，或
2. 是签发所涉证书的 CA 的证书，或
3. 在扩展密钥用途扩展中包含 id-kp-OCSPSigning 的值，并且由签发所涉证书的 CA 如上所述签发。

对响应本身或用于验证响应签名的证书，可以适用额外的接受或拒绝标准。

###### 4.2.2.2.1 授权响应器的吊销检查

由于授权 OCSP responder 为一个或多个 CA 提供状态信息，OCSP 客户端需要知道如何检查 Authorized Responder 的证书是否已被吊销。CA 可以选择以下三种方式之一来处理此问题：

- CA 可以指定 OCSP 客户端在 responder 证书的整个有效期内都可以信任该 responder。CA 通过包含扩展 id-pkix-ocsp-nocheck 来实现。这 SHOULD 是一个非关键扩展。扩展值 SHALL 为 NULL。签发此类证书的 CA 应意识到，responder 密钥的泄露与签名 CRL 的 CA 密钥的泄露同样严重，至少在该证书的有效期内如此。CA 可以选择签发有效期非常短的此类证书并频繁续签。

```asn1
id-pkix-ocsp-nocheck OBJECT IDENTIFIER ::= { id-pkix-ocsp 5 }
```

- CA 可以指定如何检查 responder 证书的吊销状态。如果应使用 CRL 进行检查，可以通过 CRL Distribution Points 来完成；如果应以其他方式进行检查，可以通过 Authority Information Access 来完成。指定这两种机制的详细信息见 [RFC5280]。

- CA 可以选择不为 responder 证书指定任何吊销检查方法，在这种情况下，由 OCSP 客户端的本地安全策略决定是否应检查该证书的吊销状态。

##### 4.2.2.3 基本响应

基本响应类型包含：

- 响应语法版本，对于本版本的基本响应语法 MUST 为 v1（值为 0）
- responder 的名称或 responder 公钥的哈希作为 ResponderID
- 响应生成时间
- 请求中每个证书的响应
- 可选扩展
- 基于响应哈希计算的签名
- 签名算法 OID

> [!tip] ResponderID 的用途
> ResponderID 信息的目的是允许客户端找到用于签名已签名 OCSP 响应的证书。因此，该信息 MUST 与用于签名响应的证书相对应。

responder MAY 在 BasicOCSPResponse 的 certs 字段中包含帮助 OCSP 客户端验证 responder 签名的证书。

请求中每个证书的响应由以下部分组成：

- 正提供吊销状态信息的证书标识符（即目标证书）
- 证书的吊销状态（good、revoked 或 unknown）；如果已吊销，则指示证书被吊销的时间，可选地指示吊销原因
- 响应的有效区间
- 可选扩展

响应 MUST 为请求中的每个证书包含一个 SingleResponse。响应 SHOULD NOT（不应）包含任何额外的 SingleResponse 元素，但例如预生成状态响应的 OCSP responder 可能为了改善响应预生成性能或缓存效率而包含额外的 SingleResponse 元素（根据 [RFC5019] 第 2.2.1 节）。

### 4.3 必需和可选的密码算法

请求 OCSP 服务的客户端 SHALL 能够处理使用 SHA-256 的 RSA 签名的响应（由 [RFC4055] 中指定的 sha256WithRSAEncryption OID 标识）。客户端 SHOULD 也能够处理使用 SHA-1 的 RSA 签名的响应（由 [RFC3279] 中指定的 sha1WithRSAEncryption OID 标识）以及使用 SHA-1 的[[数字签名]]算法（DSA）签名的响应（由 [RFC3279] 中指定的 id-dsa-with-sha1 OID 标识）。客户端 MAY 支持其他算法。

### 4.4 扩展

本节定义了一些标准扩展，基于 X.509 版本 3 证书中使用的扩展模型（参见 [RFC5280]）。所有扩展的支持对于客户端和 responder 都是可选的。对于每个扩展，定义说明了其语法、OCSP responder 执行的处理以及相应响应中包含的任何扩展。

#### 4.4.1 Nonce（随机数）

Nonce 将请求和响应进行密码学绑定，以防止重放攻击（replay attack）。Nonce 作为 requestExtensions 之一包含在请求中，在响应中则作为 responseExtensions 之一包含。在请求和响应中，nonce 由对象标识符 id-pkix-ocsp-nonce 标识，extnValue 为 nonce 的值。

```asn1
id-pkix-ocsp           OBJECT IDENTIFIER ::= { id-ad-ocsp }
id-pkix-ocsp-nonce     OBJECT IDENTIFIER ::= { id-pkix-ocsp 2 }

Nonce ::= OCTET STRING
```

#### 4.4.2 CRL 引用

OCSP responder 可能需要指示找到已吊销或暂停证书的 CRL。这在 OCSP 用于仓库之间的场景中以及作为审计机制时非常有用。CRL 可以通过 URL（CRL 可用的 URL）、编号（CRL 编号）或时间（相关 CRL 的创建时间）来指定。这些扩展将作为 singleExtensions 指定。此扩展的标识符为 id-pkix-ocsp-crl，值为 CrlID。

```asn1
id-pkix-ocsp-crl       OBJECT IDENTIFIER ::= { id-pkix-ocsp 3 }

CrlID ::= SEQUENCE {
   crlUrl               [0]     EXPLICIT IA5String OPTIONAL,
   crlNum               [1]     EXPLICIT INTEGER OPTIONAL,
   crlTime              [2]     EXPLICIT GeneralizedTime OPTIONAL }
```

对于 crlUrl 选项，IA5String 指定 CRL 可用的 URL。对于 crlNum，INTEGER 指定相关 CRL 的 CRL 编号扩展的值。对于 crlTime，GeneralizedTime 指示相关 CRL 的签发时间。

#### 4.4.3 可接受的响应类型

OCSP 客户端 MAY 希望指定它理解的响应类型。为此，它 SHOULD 使用 OID 为 id-pkix-ocsp-response、值为 AcceptableResponses 的扩展。此扩展作为 requestExtensions 之一包含在请求中。AcceptableResponses 中包含的 OID 是此客户端可接受的各种响应类型的 OID（如 id-pkix-ocsp-basic）。

```asn1
id-pkix-ocsp-response  OBJECT IDENTIFIER ::= { id-pkix-ocsp 4 }

AcceptableResponses ::= SEQUENCE OF OBJECT IDENTIFIER
```

如第 4.2.1 节所述，OCSP responder SHALL 能够使用 id-pkix-ocsp-basic 响应类型进行响应。相应地，OCSP 客户端 SHALL 能够接收和处理 id-pkix-ocsp-basic 响应类型的响应。

#### 4.4.4 归档截止时间

OCSP responder MAY 选择在证书过期后保留吊销信息。从响应中的 producedAt 时间减去此保留间隔值所得到的日期，定义为证书的 "archive cutoff"（归档截止）日期。

启用 OCSP 的应用程序将使用 OCSP 归档截止日期来为[[数字签名]]在产生日期时是否可靠提供证据，即使验证签名所需的证书早已过期。

支持此类历史参考的 OCSP 服务器 SHOULD 在响应中包含归档截止日期扩展。如果包含，此值 SHALL 作为 OCSP singleExtensions 扩展提供，由 id-pkix-ocsp-archive-cutoff 标识，语法为 GeneralizedTime。

```asn1
id-pkix-ocsp-archive-cutoff OBJECT IDENTIFIER ::= {id-pkix-ocsp 6}

ArchiveCutoff ::= GeneralizedTime
```

举例说明：如果服务器以 7 年保留间隔策略运行，状态在时间 t1 生成，则响应中 ArchiveCutoff 的值为 (t1 - 7 年)。

#### 4.4.5 CRL 条目扩展

[RFC5280] 第 5.3 节中规定为 CRL 条目扩展的所有扩展，也作为 singleExtensions 受支持。

#### 4.4.6 服务定位器

OCSP 服务器可以在一种模式下运行，即服务器接收请求并将其路由到已知对所标识证书具有权威性的 OCSP 服务器。为此定义了 serviceLocator 请求扩展。此扩展作为 singleRequestExtensions 之一包含在请求中。

```asn1
id-pkix-ocsp-service-locator OBJECT IDENTIFIER ::= {id-pkix-ocsp 7}

ServiceLocator ::= SEQUENCE {
    issuer    Name,
    locator   AuthorityInfoAccessSyntax OPTIONAL }
```

这些字段的值从主体证书中的相应字段获取。

#### 4.4.7 首选签名算法

由于允许使用强制实现算法之外的其他算法，且客户端当前没有机制来指示其算法偏好，因此始终存在服务器选择非强制算法并生成客户端可能不支持的响应的风险。

虽然 OCSP responder 可以应用算法选择规则（例如使用 CA 签名 CRL 和证书时使用的签名算法），但此类规则在常见情况下可能失败：

- 签名 CRL 和证书所使用的算法可能与 OCSP responder 用于签名响应的密钥对不一致。
- 对未知证书的请求没有为 responder 提供从多个算法选项中进行选择的依据。

最后一个条件无法通过 RFC 2560 [RFC2560] 协议的带内信令来解决，除非修改协议。

此外，OCSP responder 可能希望使用与 CA 签名证书和 CRL 不同的签名算法，原因有两个：

- responder 可能使用计算需求低于签名证书本身的算法来进行证书状态响应签名。
- 实现可能希望通过使用两个独立的签名算法来防范因签名算法泄露而导致的妥协风险。

本节描述了：

- 允许客户端指示首选签名算法集的扩展。
- 在未指定支持的首选算法时，最大化成功运行概率的签名算法选择规则。

##### 4.4.7.1 扩展语法

客户端 MAY 通过在 OCSPRequest 的 requestExtensions 中包含首选签名算法扩展来在请求中声明首选算法集。

```asn1
id-pkix-ocsp-pref-sig-algs OBJECT IDENTIFIER ::= { id-pkix-ocsp 8 }

PreferredSignatureAlgorithms ::= SEQUENCE OF
                                     PreferredSignatureAlgorithm

PreferredSignatureAlgorithm ::= SEQUENCE {
   sigIdentifier        AlgorithmIdentifier,
   pubKeyAlgIdentifier  SMIMECapability OPTIONAL
   }
```

AlgorithmIdentifier 的语法定义在 RFC 5280 [RFC5280] 第 4.1.1.2 节中。SMIMECapability 的语法定义在 RFC [[5751]] [RFC[[5751]]] 中。

sigIdentifier 指定客户端首选的签名算法，例如 algorithm=ecdsa-with-sha256。对于大多数常见签名算法，参数不存在。

pubKeyAlgIdentifier 指定客户端偏好服务器证书中使用的主体公钥算法标识符，用于验证 OCSP 响应，例如 algorithm=id-ecPublicKey 且 parameters=secp256r1。

pubKeyAlgIdentifier 是可选的，提供了一种指定区分特定算法不同使用方式所需参数的方法，例如可用于客户端指定其对给定椭圆曲线算法支持哪条曲线。

客户端 MUST 支持每个指定的首选签名算法，并且客户端 MUST 按偏好顺序指定算法，从最偏好到最不偏好。

本文档第 4.4.7.2 节描述了服务器如何为向请求客户端签名的 OCSP 响应选择算法。

##### 4.4.7.2 Responder 签名算法选择

RFC 2560 [RFC2560] 没有规定用于决定 OCSP 响应中使用的签名算法的机制。这无法为所选算法提供足够程度的确定性来促进互操作性。

###### 4.4.7.2.1 动态响应

Responder MAY 通过使用以下优先级顺序选择支持的签名算法来最大化确保互操作性的潜力，前提是所选算法满足 OCSP responder 的所有安全要求，其中第一个选择机制具有最高优先级：

1. 选择客户端请求中指定为首选签名算法的算法。
2. 选择由证书签发者签发的证书吊销列表（CRL）所使用的签名算法，该签发者为 CertID 指定的证书提供状态信息。
3. 选择用于签名 OCSPRequest 的签名算法。
4. 选择通过带外机制公布为签名服务默认签名算法的签名算法。
5. 选择当前 OCSP 版本指定的强制或推荐签名算法。

Responder SHOULD 始终应用能选出已知且受支持的算法（满足 responder 密码算法强度标准）的编号最小的选择机制。

###### 4.4.7.2.2 静态响应

出于效率考虑，允许 OCSP responder 在收到请求之前预生成静态响应。在这种情况下，responder 可能无法在响应生成期间利用客户端请求数据；然而，responder SHOULD 在选择要返回的预生成响应时仍然使用客户端请求数据。Responder MAY 将历史客户端请求作为决定使用哪些不同算法签名预生成响应的输入的一部分。

#### 4.4.8 扩展吊销定义

此扩展表示 responder 支持将 "revoked" 状态的扩展定义也包含未签发证书（根据第 2.2 节）。其主要目的之一是允许审计确定 responder 的操作类型。客户端不必解析此扩展即可确定响应中证书的状态。

当 OCSP 响应包含未签发证书的 "revoked" 状态时，此扩展 MUST 包含在响应中。此扩展 MAY 出现在其他响应中以表明 responder 实现了扩展吊销定义。当包含时，此扩展 MUST 放置在 responseExtensions 中，且 MUST NOT 出现在 singleExtensions 中。

此扩展由对象标识符 id-pkix-ocsp-extended-revoke 标识。

```asn1
id-pkix-ocsp-extended-revoke OBJECT IDENTIFIER ::= {id-pkix-ocsp 9}
```

扩展值 SHALL 为 NULL。此扩展 MUST NOT 标记为 critical。

## 5. 安全考量

为了使此服务有效，使用证书的系统必须连接到证书状态服务提供者。如果无法获得此类连接，使用证书的系统可以实现 CRL 处理逻辑作为后备方案。

拒绝服务（denial of service）漏洞在大量查询洪泛方面是显而易见的。密码签名的生成显著影响响应生成周期时间，从而加剧了这种情况。未签名的错误响应使协议面临另一种拒绝服务攻击，即攻击者发送虚假的错误响应。

使用预计算的响应允许重放攻击，即旧的（good）响应在证书被吊销之后但在过期日期之前被重放。OCSP 的部署应仔细评估预计算响应的收益与重放攻击的概率及其成功执行的代价。

请求不包含它们所指向的 responder。这允许攻击者将请求重放至任意数量的 OCSP responder。

在某些部署场景中对 HTTP 缓存的依赖可能导致意外结果，前提是中间服务器配置不正确或已知存在缓存管理缺陷。建议实现在通过 HTTP 部署 OCSP 时考虑 HTTP 缓存机制的可靠性。

> [!warning] 序列号预测风险
> 对从未签发的证书返回 "revoked" 状态可能使某人能够获取尚未签发但即将签发的证书的吊销响应，前提是请求者可以预测或猜到将要签发的证书的证书序列号。对于使用顺序证书序列号分配的 CA，这种预测很容易。本规范通过要求合规实现使用 certificateHold 原因代码来处理此风险，该代码避免了永久吊销序列号。对于支持对未签发证书的状态请求返回 "revoked" 响应的 CA，完全避免此问题的一种方法是分配具有高熵的随机证书序列号值。

### 5.1 首选签名算法

用于选择响应签名算法的机制 MUST 被认为对于预期应用具有足够的安全性来抵御密码分析攻击。

在大多数应用中，签名算法至少与签名其状态正在被查询的原始证书所使用的签名算法一样安全就足够了。然而，此标准在长期归档应用中可能不成立，在这些应用中，证书的状态是在很久以前的某个日期被查询的，而签名算法早已不再被认为是可信赖的。

#### 5.1.1 使用不安全的算法

并不总是能让 responder 生成客户端预期理解且满足当代密码安全标准的响应。在这种情况下，OCSP responder 运营者 MUST 在使用已妥协的安全解决方案的风险与强制升级的代价之间进行权衡，包括最终用户选择的替代方案可能提供更少安全性或根本没有安全性的风险。

在归档应用中，OCSP responder 可能被要求报告证书在很久以前的某个日期的有效性。此类证书可能使用了不再被认为可接受安全的签名方法。在这种情况下，responder MUST NOT 使用不被认为可接受安全的签名机制生成签名。

客户端 MUST 接受响应中其作为首选签名算法在请求中指定的任何签名算法。因此，客户端 MUST NOT 将不受支持或被认为不可接受安全的任何算法指定为首选签名算法。

#### 5.1.2 中间人降级攻击

支持客户端指示首选签名算法的机制不受中间人降级攻击（man-in-the-middle downgrade attack）保护。此约束不被认为是重大的安全问题，因为 OCSP responder MUST NOT 即使在客户端请求时也不使用弱算法签名 OCSP 响应。此外，客户端可以拒绝不满足其自身可接受密码安全标准的 OCSP 响应，无论使用什么机制来确定响应的签名算法。

#### 5.1.3 拒绝服务攻击

本文档中定义的算法敏捷性机制为拒绝服务攻击略微增加了攻击面，客户端请求可能被篡改为要求服务器不支持的算法。RFC 4732 [RFC4732] 中讨论的拒绝服务考量与本文档相关。

## 6. IANA 考量

本文档包含了在 RFC 2560 发布时注册的 ocsp-request 和 ocsp-response 的媒体类型注册（在附录 C 中）。由于本文档废止 RFC 2560，IANA 已将 "Application Media Types" 注册表中 ocsp-request 和 ocsp-response 的引用更新为指向本文档。

## 7. 参考文献

### 7.1 规范性引用

- [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, March 1997.
- [RFC2616] Fielding, R., Gettys, J., Mogul, J., Frystyk, H., Masinter, L., Leach, P., and T. Berners-Lee, "Hypertext Transfer Protocol -- HTTP/1.1", RFC 2616, June 1999.
- [RFC3279] Bassham, L., Polk, W., and R. Housley, "Algorithms and Identifiers for the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) [[Profile]]", RFC 3279, April 2002.
- [RFC[[3986]]] Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform Resource Identifier (URI): Generic Syntax", STD 66, RFC [[3986]], January 2005.
- [RFC4055] Schaad, J., Kaliski, B., and R. Housley, "Additional Algorithms and Identifiers for RSA Cryptography for use in the Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) [[Profile]]", RFC 4055, June 2005.
- [RFC5280] Cooper, D., Santesson, S., Farrell, S., Boeyen, S., Housley, R., and W. Polk, "Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) [[Profile]]", RFC 5280, May 2008.
- [RFC[[5751]]] Ramsdell, B. and S. Turner, "Secure/Multipurpose Internet Mail Extensions ([[S/MIME]]) Version 3.2 Message Specification", RFC [[5751]], January 2010.
- [RFC6277] Santesson, S. and P. Hallam-Baker, "Online Certificate Status Protocol Algorithm Agility", RFC 6277, June 2011.
- [X.690] ITU-T Recommendation X.690 (2008) | ISO/IEC 8825-1:2008, "Information Technology - [[ASN.1]] encoding rules: Specification of Basic Encoding Rules (BER), Canonical Encoding Rules (CER) and Distinguished Encoding Rules (DER)", November 2008.

### 7.2 信息性引用

- [RFC2560] Myers, M., Ankney, R., Malpani, A., Galperin, S., and C. Adams, [["X.509]] Internet Public Key Infrastructure Online Certificate Status Protocol - OCSP", RFC 2560, June 1999.
- [RFC4732] Handley, M., Ed., Rescorla, E., Ed., and IAB, "Internet Denial-of-Service Considerations", RFC 4732, December 2006.
- [RFC5019] Deacon, A. and R. Hurst, "The Lightweight Online Certificate Status Protocol (OCSP) [[Profile]] for High-Volume Environments", RFC 5019, September 2007.
- [RFC5912] Hoffman, P. and J. Schaad, "New [[ASN.1]] Modules for the Public Key Infrastructure Using X.509 (PKIX)", RFC 5912, June 2010.

## 8. 致谢

本文档的开发得益于 PKIX 工作组成员的大量投入。

Jim Schaad 通过编写和检查本规范的 [[ASN.1]] 模块提供了宝贵的支持。

## 附录 A. 基于 HTTP 的 OCSP

本节描述为支持 HTTP [RFC2616] 而对请求和响应进行的格式化处理。

### A.1 请求

基于 HTTP 的 OCSP 请求可以使用 GET 或 POST 方法提交。为了启用 HTTP 缓存，小请求（编码后小于 255 字节）MAY 使用 GET 提交。如果 HTTP 缓存不重要或请求大于 255 字节，请求 SHOULD 使用 POST 提交。如果隐私是要求，使用 HTTP 交换的 OCSP 事务 MAY 使用传输层安全/安全套接字层（TLS/SSL）或其他低层协议进行保护。

使用 GET 方法的 OCSP 请求构造如下：

```
GET {url}/{url-encoding of base-64 encoding of the DER encoding of the OCSPRequest}
```

其中 {url} 可以从待检查吊销状态的证书中的授权信息访问扩展的值或 OCSP 客户端的其他本地配置中获取。

使用 POST 方法的 OCSP 请求构造如下：Content-Type 头的值为 "application/ocsp-request"，消息体为 OCSPRequest 的 DER 编码的二进制值。

### A.2 响应

基于 HTTP 的 OCSP 响应由适当的 HTTP 头和 OCSPResponse 的 DER 编码的二进制值组成。Content-Type 头的值为 "application/ocsp-response"。Content-Length 头 SHOULD 指定响应的长度。其他 HTTP 头 MAY 存在，如果请求者不理解则 MAY 忽略。

## 附录 B. ASN.1 模块

本附录包含 OCSP 的 [[ASN.1]] 模块。附录 B.1 包含一个符合 [[ASN.1]] 1998 版本的 [[ASN.1]] 模块，涵盖 OCSP 的所有语法元素，包括 [RFC6277] 中定义的首选签名算法扩展。此模块替换 [RFC2560] 附录 B 和 [RFC6277] 附录 A.2 中的模块。附录 B.2 包含一个与 B.1 中模块对应的、符合 [[ASN.1]] 2008 版本的 [[ASN.1]] 模块。此模块替换 [RFC5912] 第 12 节和 [RFC6277] 附录 A.1 中的模块。虽然提供了 2008 [[ASN.1]] 模块，但根据 PKIX 工作组的策略，附录 B.1 中的模块仍为规范性模块。

### B.1 OCSP ASN.1 - 1998 语法

```asn1
OCSP-2013-88
      {iso(1) identified-organization(3) dod(6) internet(1)
      security(5) mechanisms(5) pkix(7) id-mod(0)
      id-mod-ocsp-2013-88(81)}

DEFINITIONS EXPLICIT TAGS ::=

BEGIN

IMPORTS

   -- PKIX Certificate Extensions
      AuthorityInfoAccessSyntax, CRLReason, GeneralName
      FROM PKIX1Implicit88 { iso(1) identified-organization(3)
           dod(6) internet(1) security(5) mechanisms(5) pkix(7)
           id-mod(0) id-pkix1-implicit(19) }

      Name, CertificateSerialNumber, Extensions,
      id-kp, id-ad-ocsp, Certificate, AlgorithmIdentifier
      FROM PKIX1Explicit88 { iso(1) identified-organization(3)
           dod(6) internet(1) security(5) mechanisms(5) pkix(7)
           id-mod(0) id-pkix1-explicit(18) };

OCSPRequest ::= SEQUENCE {
   tbsRequest              TBSRequest,
   optionalSignature   [0] EXPLICIT Signature OPTIONAL }

TBSRequest ::= SEQUENCE {
   version             [0] EXPLICIT Version DEFAULT v1,
   requestorName       [1] EXPLICIT GeneralName OPTIONAL,
   requestList             SEQUENCE OF Request,
   requestExtensions   [2] EXPLICIT Extensions OPTIONAL }

Signature ::= SEQUENCE {
   signatureAlgorithm      AlgorithmIdentifier,
   signature               BIT STRING,
   certs               [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }

Version ::= INTEGER { v1(0) }

Request ::= SEQUENCE {
   reqCert                     CertID,
   singleRequestExtensions [0] EXPLICIT Extensions OPTIONAL }

CertID ::= SEQUENCE {
   hashAlgorithm           AlgorithmIdentifier,
   issuerNameHash          OCTET STRING, -- Hash of issuer's DN
   issuerKeyHash           OCTET STRING, -- Hash of issuer's public key
   serialNumber            CertificateSerialNumber }

OCSPResponse ::= SEQUENCE {
   responseStatus          OCSPResponseStatus,
   responseBytes       [0] EXPLICIT ResponseBytes OPTIONAL }

OCSPResponseStatus ::= ENUMERATED {
   successful          (0),  -- Response has valid confirmations
   malformedRequest    (1),  -- Illegal confirmation request
   internalError       (2),  -- Internal error in issuer
   tryLater            (3),  -- Try again later
                             -- (4) is not used
   sigRequired         (5),  -- Must sign the request
   unauthorized        (6)   -- Request unauthorized
}

ResponseBytes ::= SEQUENCE {
   responseType            OBJECT IDENTIFIER,
   response                OCTET STRING }

BasicOCSPResponse ::= SEQUENCE {
  tbsResponseData          ResponseData,
  signatureAlgorithm       AlgorithmIdentifier,
  signature                BIT STRING,
  certs                [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }

ResponseData ::= SEQUENCE {
   version             [0] EXPLICIT Version DEFAULT v1,
   responderID             ResponderID,
   producedAt              GeneralizedTime,
   responses               SEQUENCE OF SingleResponse,
   responseExtensions  [1] EXPLICIT Extensions OPTIONAL }

ResponderID ::= CHOICE {
   byName              [1] Name,
   byKey               [2] KeyHash }

KeyHash ::= OCTET STRING -- SHA-1 hash of responder's public key
                         -- (i.e., the SHA-1 hash of the value of the
                         -- BIT STRING subjectPublicKey [excluding
                         -- the tag, length, and number of unused
                         -- bits] in the responder's certificate)

SingleResponse ::= SEQUENCE {
   certID                  CertID,
   certStatus              CertStatus,
   thisUpdate              GeneralizedTime,
   nextUpdate          [0] EXPLICIT GeneralizedTime OPTIONAL,
   singleExtensions    [1] EXPLICIT Extensions OPTIONAL }

CertStatus ::= CHOICE {
   good                [0] IMPLICIT NULL,
   revoked             [1] IMPLICIT RevokedInfo,
   unknown             [2] IMPLICIT UnknownInfo }

RevokedInfo ::= SEQUENCE {
   revocationTime          GeneralizedTime,
   revocationReason    [0] EXPLICIT CRLReason OPTIONAL }

UnknownInfo ::= NULL

ArchiveCutoff ::= GeneralizedTime

AcceptableResponses ::= SEQUENCE OF OBJECT IDENTIFIER

ServiceLocator ::= SEQUENCE {
   issuer                  Name,
   locator                 AuthorityInfoAccessSyntax }

CrlID ::= SEQUENCE {
    crlUrl               [0]     EXPLICIT IA5String OPTIONAL,
    crlNum               [1]     EXPLICIT INTEGER OPTIONAL,
    crlTime              [2]     EXPLICIT GeneralizedTime OPTIONAL }

PreferredSignatureAlgorithms ::= SEQUENCE OF PreferredSignatureAlgorithm

PreferredSignatureAlgorithm ::= SEQUENCE {
   sigIdentifier   AlgorithmIdentifier,
   certIdentifier  AlgorithmIdentifier OPTIONAL }

-- Object Identifiers

id-kp-OCSPSigning            OBJECT IDENTIFIER ::= { id-kp 9 }
id-pkix-ocsp                 OBJECT IDENTIFIER ::= { id-ad-ocsp }
id-pkix-ocsp-basic           OBJECT IDENTIFIER ::= { id-pkix-ocsp 1 }
id-pkix-ocsp-nonce           OBJECT IDENTIFIER ::= { id-pkix-ocsp 2 }
id-pkix-ocsp-crl             OBJECT IDENTIFIER ::= { id-pkix-ocsp 3 }
id-pkix-ocsp-response        OBJECT IDENTIFIER ::= { id-pkix-ocsp 4 }
id-pkix-ocsp-nocheck         OBJECT IDENTIFIER ::= { id-pkix-ocsp 5 }
id-pkix-ocsp-archive-cutoff  OBJECT IDENTIFIER ::= { id-pkix-ocsp 6 }
id-pkix-ocsp-service-locator OBJECT IDENTIFIER ::= { id-pkix-ocsp 7 }
id-pkix-ocsp-pref-sig-algs   OBJECT IDENTIFIER ::= { id-pkix-ocsp 8 }
id-pkix-ocsp-extended-revoke OBJECT IDENTIFIER ::= { id-pkix-ocsp 9 }

END
```

### B.2 OCSP ASN.1 - 2008 语法

```asn1
OCSP-2013-08
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0) id-mod-ocsp-2013-08(82)}

DEFINITIONS EXPLICIT TAGS ::=

BEGIN

IMPORTS

Extensions{}, EXTENSION, ATTRIBUTE
FROM PKIX-CommonTypes-2009 -- From [RFC5912]
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0) id-mod-pkixCommon-02(57)}

AlgorithmIdentifier{}, DIGEST-ALGORITHM, SIGNATURE-ALGORITHM, PUBLIC-KEY
FROM AlgorithmInformation-2009 -- From [RFC5912]
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0)
    id-mod-algorithmInformation-02(58)}

AuthorityInfoAccessSyntax, GeneralName, CrlEntryExtensions
FROM PKIX1Implicit-2009 -- From [RFC5912]
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0) id-mod-pkix1-implicit-02(59)}

Name, CertificateSerialNumber, id-kp, id-ad-ocsp, Certificate
FROM PKIX1Explicit-2009 -- From [RFC5912]
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0) id-mod-pkix1-explicit-02(51)}

sa-dsaWithSHA1, sa-rsaWithMD2, sa-rsaWithMD5, sa-rsaWithSHA1
FROM PKIXAlgs-2009 -- From [RFC5912]
    {iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0)
    id-mod-pkix1-algorithms2008-02(56)};

OCSPRequest     ::=     SEQUENCE {
    tbsRequest                  TBSRequest,
    optionalSignature   [0]     EXPLICIT Signature OPTIONAL }

TBSRequest      ::=     SEQUENCE {
    version             [0] EXPLICIT Version DEFAULT v1,
    requestorName       [1] EXPLICIT GeneralName OPTIONAL,
    requestList             SEQUENCE OF Request,
    requestExtensions   [2] EXPLICIT Extensions {{re-ocsp-nonce |
                     re-ocsp-response, ...,
                     re-ocsp-preferred-signature-algorithms}} OPTIONAL }

Signature       ::=     SEQUENCE {
    signatureAlgorithm   AlgorithmIdentifier
                             { SIGNATURE-ALGORITHM, {...}},
    signature            BIT STRING,
    certs            [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }

Version  ::=  INTEGER  {  v1(0) }

Request ::=     SEQUENCE {
    reqCert                    CertID,
    singleRequestExtensions    [0] EXPLICIT Extensions
                                       { {re-ocsp-service-locator,
                                              ...}} OPTIONAL }

CertID ::= SEQUENCE {
    hashAlgorithm            AlgorithmIdentifier
                                 {DIGEST-ALGORITHM, {...}},
    issuerNameHash     OCTET STRING, -- Hash of issuer's DN
    issuerKeyHash      OCTET STRING, -- Hash of issuer's public key
    serialNumber       CertificateSerialNumber }

OCSPResponse ::= SEQUENCE {
   responseStatus         OCSPResponseStatus,
   responseBytes          [0] EXPLICIT ResponseBytes OPTIONAL }

OCSPResponseStatus ::= ENUMERATED {
    successful            (0), -- Response has valid confirmations
    malformedRequest      (1), -- Illegal confirmation request
    internalError         (2), -- Internal error in issuer
    tryLater              (3), -- Try again later
                               -- (4) is not used
    sigRequired           (5), -- Must sign the request
    unauthorized          (6)  -- Request unauthorized
}

RESPONSE ::= TYPE-IDENTIFIER

ResponseSet RESPONSE ::= {basicResponse, ...}

ResponseBytes ::=       SEQUENCE {
    responseType        RESPONSE.
                            &id ({ResponseSet}),
    response            OCTET STRING (CONTAINING RESPONSE.
                            &Type({ResponseSet}{@responseType}))}

basicResponse RESPONSE ::=
    { BasicOCSPResponse IDENTIFIED BY id-pkix-ocsp-basic }

BasicOCSPResponse       ::= SEQUENCE {
   tbsResponseData      ResponseData,
   signatureAlgorithm   AlgorithmIdentifier{SIGNATURE-ALGORITHM,
                            {sa-dsaWithSHA1 | sa-rsaWithSHA1 |
                                 sa-rsaWithMD5 | sa-rsaWithMD2, ...}},
   signature            BIT STRING,
   certs            [0] EXPLICIT SEQUENCE OF Certificate OPTIONAL }

ResponseData ::= SEQUENCE {
   version              [0] EXPLICIT Version DEFAULT v1,
   responderID              ResponderID,
   producedAt               GeneralizedTime,
   responses                SEQUENCE OF SingleResponse,
   responseExtensions   [1] EXPLICIT Extensions
                               {{re-ocsp-nonce, ...,
                                 re-ocsp-extended-revoke}} OPTIONAL }

ResponderID ::= CHOICE {
   byName   [1] Name,
   byKey    [2] KeyHash }

KeyHash ::= OCTET STRING -- SHA-1 hash of responder's public key
                         -- (excluding the tag and length fields)

SingleResponse ::= SEQUENCE {
   certID                       CertID,
   certStatus                   CertStatus,
   thisUpdate                   GeneralizedTime,
   nextUpdate           [0]     EXPLICIT GeneralizedTime OPTIONAL,
   singleExtensions     [1]     EXPLICIT Extensions{{re-ocsp-crl |
                                             re-ocsp-archive-cutoff |
                                             CrlEntryExtensions, ...}
                                             } OPTIONAL }

CertStatus ::= CHOICE {
    good                [0]     IMPLICIT NULL,
    revoked             [1]     IMPLICIT RevokedInfo,
    unknown             [2]     IMPLICIT UnknownInfo }

RevokedInfo ::= SEQUENCE {
    revocationTime              GeneralizedTime,
    revocationReason    [0]     EXPLICIT CRLReason OPTIONAL }

UnknownInfo ::= NULL

ArchiveCutoff ::= GeneralizedTime

AcceptableResponses ::= SEQUENCE OF RESPONSE.&id({ResponseSet})

ServiceLocator ::= SEQUENCE {
    issuer    Name,
    locator   AuthorityInfoAccessSyntax }

CrlID ::= SEQUENCE {
    crlUrl               [0]     EXPLICIT IA5String OPTIONAL,
    crlNum               [1]     EXPLICIT INTEGER OPTIONAL,
    crlTime              [2]     EXPLICIT GeneralizedTime OPTIONAL }

PreferredSignatureAlgorithms ::= SEQUENCE OF PreferredSignatureAlgorithm

PreferredSignatureAlgorithm ::= SEQUENCE {
   sigIdentifier  AlgorithmIdentifier{SIGNATURE-ALGORITHM, {...}},
   certIdentifier AlgorithmIdentifier{PUBLIC-KEY, {...}} OPTIONAL
}

-- Certificate Extensions

ext-ocsp-nocheck EXTENSION ::= { SYNTAX NULL IDENTIFIED
                                 BY id-pkix-ocsp-nocheck }

-- Request Extensions

re-ocsp-nonce EXTENSION ::= { SYNTAX OCTET STRING IDENTIFIED
                              BY id-pkix-ocsp-nonce }

re-ocsp-response EXTENSION ::= { SYNTAX AcceptableResponses IDENTIFIED
                                 BY id-pkix-ocsp-response }

re-ocsp-service-locator EXTENSION ::= { SYNTAX ServiceLocator
                                        IDENTIFIED BY
                                        id-pkix-ocsp-service-locator }

re-ocsp-preferred-signature-algorithms EXTENSION ::= {
   SYNTAX PreferredSignatureAlgorithms
   IDENTIFIED BY id-pkix-ocsp-pref-sig-algs  }

-- Response Extensions

re-ocsp-crl EXTENSION ::= { SYNTAX CrlID IDENTIFIED BY
                                id-pkix-ocsp-crl }

re-ocsp-archive-cutoff EXTENSION ::= { SYNTAX ArchiveCutoff
                                       IDENTIFIED BY
                                       id-pkix-ocsp-archive-cutoff }

re-ocsp-extended-revoke EXTENSION ::= { SYNTAX NULL IDENTIFIED BY
                                        id-pkix-ocsp-extended-revoke }

-- Object Identifiers

id-kp-OCSPSigning            OBJECT IDENTIFIER ::= { id-kp 9 }
id-pkix-ocsp                 OBJECT IDENTIFIER ::= id-ad-ocsp
id-pkix-ocsp-basic           OBJECT IDENTIFIER ::= { id-pkix-ocsp 1 }
id-pkix-ocsp-nonce           OBJECT IDENTIFIER ::= { id-pkix-ocsp 2 }
id-pkix-ocsp-crl             OBJECT IDENTIFIER ::= { id-pkix-ocsp 3 }
id-pkix-ocsp-response        OBJECT IDENTIFIER ::= { id-pkix-ocsp 4 }
id-pkix-ocsp-nocheck         OBJECT IDENTIFIER ::= { id-pkix-ocsp 5 }
id-pkix-ocsp-archive-cutoff  OBJECT IDENTIFIER ::= { id-pkix-ocsp 6 }
id-pkix-ocsp-service-locator OBJECT IDENTIFIER ::= { id-pkix-ocsp 7 }
id-pkix-ocsp-pref-sig-algs   OBJECT IDENTIFIER ::= { id-pkix-ocsp 8 }
id-pkix-ocsp-extended-revoke OBJECT IDENTIFIER ::= { id-pkix-ocsp 9 }

END
```

## 附录 C. MIME 注册

### C.1 application/ocsp-request

- **MIME 媒体类型名称**：application
- **MIME 子类型名称**：ocsp-request
- **必需参数**：无
- **可选参数**：无
- **编码考量**：binary
- **安全考量**：携带信息请求。此请求可以可选地进行密码签名。
- **互操作性考量**：无
- **发布规范**：IETF PKIX 工作组关于在线证书状态协议（OCSP）的文档
- **使用此媒体类型的应用程序**：OCSP 客户端
- **附加信息**：Magic number(s): 无；File extension(s): .ORQ；Macintosh File Type Code(s): 无
- **联系人**：Stefan Santesson <sts@aaa-sec.com>
- **预期用途**：COMMON
- **作者/变更控制者**：IETF

### C.2 application/ocsp-response

- **MIME 媒体类型名称**：application
- **MIME 子类型名称**：ocsp-response
- **必需参数**：无
- **可选参数**：无
- **编码考量**：binary
- **安全考量**：携带密码签名响应。
- **互操作性考量**：无
- **发布规范**：IETF PKIX 工作组关于在线证书状态协议（OCSP）的文档
- **使用此媒体类型的应用程序**：OCSP 服务器
- **附加信息**：Magic number(s): 无；File extension(s): .ORS；Macintosh File Type Code(s): 无
- **联系人**：Stefan Santesson <sts@aaa-sec.com>
- **预期用途**：COMMON
- **作者/变更控制者**：IETF

## 作者地址

| 姓名 | 组织 | 联系方式 |
|------|------|---------|
| Stefan Santesson | 3xA Security AB, Scheelev. 17, 223 70 Lund, Sweden | sts@aaa-sec.com |
| Michael Myers | TraceRoute Security | mmyers@fastq.com |
| Rich Ankney | — | — |
| Ambarish Malpani | CA Technologies, 455 West Maude Ave. Suite 210, Sunnyvale, CA 94085, United States | ambarish@gmail.com |
| Slava Galperin | A9.com Inc., 130 Lytton Ave. Suite 300, Palo Alto, CA 94301, United States | slava.galperin@gmail.com |
| Carlisle Adams | University of Ottawa, 800 King Edward Avenue, Ottawa ON K1N 6N5, Canada | cadams@eecs.uottawa.ca |
