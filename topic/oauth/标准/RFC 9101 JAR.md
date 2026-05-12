| RFC 9101 | OAuth JAR | August 2021 |
| --- | --- | --- |
| Sakimura, et al. | Standards Track | \[Page\] |

## RFC 9101

## Abstract

The authorization request in OAuth 2.0 described in RFC 6749 utilizes query parameter serialization, which means that authorization request parameters are encoded in the URI of the request and sent through user agents such as web browsers. While it is easy to implement, it means that a) the communication through the user agents is not integrity protected and thus, the parameters can be tainted, b) the source of the communication is not authenticated, and c) the communication through the user agents can be monitored. Because of these weaknesses, several attacks to the protocol have now been put forward.[¶](#section-abstract-1)

This document introduces the ability to send request parameters in a JSON Web Token (JWT) instead, which allows the request to be signed with JSON Web Signature (JWS) and encrypted with JSON Web Encryption (JWE) so that the integrity, source authentication, and confidentiality properties of the authorization request are attained. The request can be sent by value or by reference.[¶](#section-abstract-2)

## Status of This Memo

This is an Internet Standards Track document.[¶](#section-boilerplate.1-1)

This document is a product of the Internet Engineering Task Force (IETF). It represents the consensus of the IETF community. It has received public review and has been approved for publication by the Internet Engineering Steering Group (IESG). Further information on Internet Standards is available in Section 2 of RFC 7841.[¶](#section-boilerplate.1-2)

Information about the current status of this document, any errata, and how to provide feedback on it may be obtained at [https://www.rfc-editor.org/info/rfc9101](https://www.rfc-editor.org/info/rfc9101).[¶](#section-boilerplate.1-3)

## 1.

The authorization request in \[\] utilizes query parameter serialization and is typically sent through user agents such as web browsers.[¶](#section-1-1)

For example, the parameters `response_type`, `client_id`, `state`, and `redirect_uri` are encoded in the URI of the request:[¶](#section-1-2)

```
GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb HTTP/1.1
Host: server.example.com
```
[¶](#section-1-3)

While it is easy to implement, the encoding in the URI does not allow application-layer security to be used to provide confidentiality and integrity protection. While TLS is used to offer communication security between the client and the user agent as well as the user agent and the authorization server, TLS sessions are terminated in the user agent. In addition, TLS sessions may be terminated prematurely at some middlebox (such as a load balancer).[¶](#section-1-4)

As a result, the authorization request of \[\] has shortcomings in that:[¶](#section-1-5)

(a)

the communication through the user agents is not integrity protected, and thus, the parameters can be tainted (integrity protection failure);[¶](#section-1-6.1)

(b)

the source of the communication is not authenticated (source authentication failure);[¶](#section-1-6.2)

(c)

the communication through the user agents can be monitored (containment/confidentiality failure).[¶](#section-1-6.3)

Due to these inherent weaknesses, several attacks against the protocol, such as redirection URI rewriting, have been identified.[¶](#section-1-7)

The use of application-layer security mitigates these issues.[¶](#section-1-8)

The use of application-layer security allows requests to be prepared by a trusted third party so that a client application cannot request more permissions than previously agreed upon.[¶](#section-1-9)

Furthermore, passing the request by reference allows the reduction of over-the-wire overhead.[¶](#section-1-10)

The \[\] encoding has been chosen because of:[¶](#section-1-11)

(1)

its close relationship with JSON, which is used as OAuth's response format [¶](#section-1-12.1)

(2)

its developer friendliness due to its textual nature [¶](#section-1-12.2)

(3)

its relative compactness compared to XML [¶](#section-1-12.3)

(4)

its development status as a Proposed Standard, along with the associated signing and encryption methods \[\] \[\] [¶](#section-1-12.4)

(5)

the relative ease of JWS and JWE compared to XML Signature and Encryption.[¶](#section-1-12.5)

The parameters `request` and `request_uri` are introduced as additional authorization request parameters for the \[\] flows. The `request` parameter is a \[\] whose JWT Claims Set holds the JSON-encoded OAuth 2.0 authorization request parameters. Note that, in contrast to RFC [[7519]], the elements of the Claims Set are encoded OAuth request parameters \[\], supplemented with only a few of the IANA-managed JSON Web Token Claims \[\], in particular, `iss` and `aud`. The JWT in the `request` parameter is integrity protected and source authenticated using JWS.[¶](#section-1-13)

The \[\] can be passed to the authorization endpoint by reference, in which case the parameter `request_uri` is used instead of `request`.[¶](#section-1-14)

Using \[\] as the request encoding instead of query parameters has several advantages:[¶](#section-1-15)

(a)

Integrity protection. The request can be signed so that the integrity of the request can be checked.[¶](#section-1-16.1)

(b)

Source authentication. The request can be signed so that the signer can be authenticated.[¶](#section-1-16.2)

(c)

Confidentiality protection. The request can be encrypted so that end-to-end confidentiality can be provided even if the TLS connection is terminated at one point or another (including at and before user agents).[¶](#section-1-16.3)

(d)

Collection minimization. The request can be signed by a trusted third party attesting that the authorization request is compliant with a certain policy. For example, a request can be pre-examined by a trusted third party to confirm that all the personal data requested is strictly necessary to perform the process that the end user asked for; the request would then be signed by that trusted third party. The authorization server then examines the signature and shows the conformance status to the end user who would have some assurance as to the legitimacy of the request when authorizing it. In some cases, it may even be desirable to skip the authorization dialogue under such circumstances.[¶](#section-1-16.4)

There are a few cases where request by reference is useful, such as:[¶](#section-1-17)

1. when it is desirable to reduce the size of a transmitted request. The use of application-layer security increases the size of the request particularly when public-key cryptography is used.[¶](#section-1-18.1)
2. when the client does not want to do the application-level cryptography. The authorization server may provide an endpoint to accept the authorization request through direct communication with the client, so that the client is authenticated and the channel is TLS protected.[¶](#section-1-18.2)

This capability is in use by [[OpenID Connect]] \[\].[¶](#section-1-19)

### 1.1.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 \[\] \[\] when, and only when, they appear in all capitals, as shown here.[¶](#section-1.1-1)

## 2.

For the purposes of this specification, the following terms and definitions apply in addition to what is defined in \[\], \[\], and \[\].[¶](#section-2-1)

### 2.1.

A Request Object is a \[\] whose JWT Claims Set holds the JSON-encoded OAuth 2.0 authorization request parameters.[¶](#section-2.1-1)

### 2.2.

A Request Object URI is an absolute URI that references the set of parameters comprising an OAuth 2.0 authorization request. The content of the resource referenced by the URI is a (), unless the URI was provided to the client by the same authorization server, in which case the content is an implementation detail at the discretion of the authorization server. The content being a Request Object is to ensure interoperability in cases where the provider of the `request_uri` is a separate entity from the consumer, such as when a client provides a URI referencing a Request Object stored on the client's backend service that is made accessible via HTTPS. In the latter case, where the authorization server is both provider and consumer of the URI, such as when it offers an endpoint that provides a URI in exchange for a Request Object, this interoperability concern does not apply.[¶](#section-2.2-1)

## 4.

A () is used to provide authorization request parameters for an OAuth 2.0 authorization request. It MUST contain all the parameters (including extension parameters) used to process the \[\] authorization request except the `request` and `request_uri` parameters that are defined in this document. The parameters are represented as the JWT Claims of the object. Parameter names and string values MUST be included as JSON strings. Since Request Objects are handled across domains and potentially outside of a closed ecosystem, per [Section 8.1](https://www.rfc-editor.org/rfc/rfc8259#section-8.1) of \[\], these JSON strings MUST be encoded using UTF-8 \[\]. Numerical values MUST be included as JSON numbers. The Request Object MAY include any extension parameters. This \[\] object constitutes the JWT Claims Set defined in \[\]. The JWT Claims Set is then signed or signed and encrypted.[¶](#section-4-1)

To sign, \[\] is used. The result is a JWS-signed \[\]. If signed, the Authorization Request Object SHOULD contain the Claims `iss` (issuer) and `aud` (audience) as members with their semantics being the same as defined in the \[\] specification. The value of `aud` should be the value of the authorization server (AS) `issuer`, as defined in \[\].[¶](#section-4-2)

To encrypt, \[\] is used. When both signature and encryption are being applied, the JWT MUST be signed, then encrypted, as described in [Section 11.2](https://www.rfc-editor.org/rfc/rfc7519#section-11.2) of \[\]. The result is a Nested JWT, as defined in \[\].[¶](#section-4-3)

The client determines the algorithms used to sign and encrypt Request Objects. The algorithms chosen need to be supported by both the client and the authorization server. The client can inform the authorization server of the algorithms that it supports in its dynamic client registration metadata \[\], specifically, the metadata values `request_object_signing_alg`, `request_object_encryption_alg`, and `request_object_encryption_enc`. Likewise, the authorization server can inform the client of the algorithms that it supports in its authorization server metadata \[\], specifically, the metadata values `request_object_signing_alg_values_supported`, `request_object_encryption_alg_values_supported`, and `request_object_encryption_enc_values_supported`.[¶](#section-4-4)

The Request Object MAY be sent by value, as described in, or by reference, as described in. `request` and `request_uri` parameters MUST NOT be included in Request Objects.[¶](#section-4-5)

A () has the media type \[\] `application/oauth-authz-req+jwt`. Note that some existing deployments may alternatively be using the type `application/jwt`.[¶](#section-4-6)

The following is an example of the Claims in a Request Object before base64url \[\] encoding and signing. Note that it includes the extension parameters `nonce` and `max_age`.[¶](#section-4-7)

```json
{
 "iss": "s6BhdRkqt3",
 "aud": "https://server.example.com",
 "response_type": "code id_token",
 "client_id": "s6BhdRkqt3",
 "redirect_uri": "https://client.example.org/cb",
 "scope": "openid",
 "state": "af0ifjsldkj",
 "nonce": "n-0S6_WzA2Mj",
 "max_age": 86400
}
```
[¶](#section-4-8)

Signing it with the `RS256` algorithm \[\] results in this Request Object value (with line wraps within values for display purposes only):[¶](#section-4-9)

```
eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyYmRjIn0.ewogICAgImlzcyI6ICJzNkJoZF
JrcXQzIiwKICAgICJhdWQiOiAiaHR0cHM6Ly9zZXJ2ZXIuZXhhbXBsZS5jb20iLAog
ICAgInJlc3BvbnNlX3R5cGUiOiAiY29kZSBpZF90b2tlbiIsCiAgICAiY2xpZW50X2
lkIjogInM2QmhkUmtxdDMiLAogICAgInJlZGlyZWN0X3VyaSI6ICJodHRwczovL2Ns
aWVudC5leGFtcGxlLm9yZy9jYiIsCiAgICAic2NvcGUiOiAib3BlbmlkIiwKICAgIC
JzdGF0ZSI6ICJhZjBpZmpzbGRraiIsCiAgICAibm9uY2UiOiAibi0wUzZfV3pBMk1q
IiwKICAgICJtYXhfYWdlIjogODY0MDAKfQ.Nsxa_18VUElVaPjqW_ToI1yrEJ67BgK
b5xsuZRVqzGkfKrOIX7BCx0biSxYGmjK9KJPctH1OC0iQJwXu5YVY-vnW0_PLJb1C2
HG-ztVzcnKZC2gE4i0vgQcpkUOCpW3SEYXnyWnKzuKzqSb1wAZALo5f89B_p6QA6j6
JwBSRvdVsDPdulW8lKxGTbH82czCaQ50rLAg3EYLYaCb4ik4I1zGXE4fvim9FIMs8O
CMmzwIB5S-ujFfzwFjoyuPEV4hJnoVUmXR_W9typPf846lGwA8h9G9oNTIuX8Ft2jf
pnZdFmLg3_wr3Wa5q3a-lfbgF3S9H_8nN3j1i7tLR_5Nz-g
```
[¶](#section-4-10)

The following RSA public key, represented in JSON Web Key (JWK) format, can be used to validate the Request Object signature in this and subsequent Request Object examples (with line wraps within values for display purposes only):[¶](#section-4-11)

```json
{
 "kty":"RSA",
 "kid":"k2bdc",
 "n":"x5RbkAZkmpRxia65qRQ1wwSMSxQUnS7gcpVTV_cdHmfmG2ltd2yabEO9XadD8
      pJNZubINPpmgHh3J1aD9WRwS05ucmFq3CfFsluLt13_7oX5yDRSKX7poXmT_5
      ko8k4NJZPMAO8fPToDTH7kHYbONSE2FYa5GZ60CUsFhSonI-dcMDJ0Ary9lxI
      w5k2z4TAdARVWcS7sD07VhlMMshrwsPHBQgTatlkxyIHXbYdtak8fqvNAwr7O
      lVEvM_Ipf5OfmdB8Sd-wjzaBsyP4VhJKoi_qdgSzpC694XZeYPq45Sw-q51iF
      UlcOlTCI7z6jltUtnR6ySn6XDGFnzH5Fe5ypw",
 "e":"AQAB"
}
```
[¶](#section-4-12)

## 5.

The client constructs the authorization request URI by adding the following parameters to the query component of the authorization endpoint URI using the `application/x-www-form-urlencoded` format:[¶](#section-5-1)

request

REQUIRED unless `request_uri` is specified. The () that holds authorization request parameters stated in [Section 4](https://www.rfc-editor.org/rfc/rfc6749#section-4) of \[\] (OAuth 2.0). If this parameter is present in the authorization request, `request_uri` MUST NOT be present.[¶](#section-5-2.2)

request\_uri

REQUIRED unless `request` is specified. The absolute URI, as defined by \[\], that is the () referencing the authorization request parameters stated in [Section 4](https://www.rfc-editor.org/rfc/rfc6749#section-4) of \[\] (OAuth 2.0). If this parameter is present in the authorization request, `request` MUST NOT be present.[¶](#section-5-2.4)

client\_id

REQUIRED. \[\] `client_id`. The value MUST match the `request` or `request_uri` () `client_id`.[¶](#section-5-2.6)

The client directs the resource owner to the constructed URI using an HTTP redirection response or by other means available to it via the user agent.[¶](#section-5-3)

For example, the client directs the end user's user agent to make the following HTTPS request:[¶](#section-5-4)

```
GET /authz?client_id=s6BhdRkqt3&request=eyJhbG..AlMGzw HTTP/1.1
Host: server.example.com
```
[¶](#section-5-5)

The value for the request parameter is abbreviated for brevity.[¶](#section-5-6)

The Authorization Request Object MUST be one of the following:[¶](#section-5-7)

(a)

JWS signed [¶](#section-5-8.1)

(b)

JWS signed and JWE encrypted [¶](#section-5-8.2)

The client MAY send the parameters included in the Request Object duplicated in the query parameters as well for backward compatibility, etc. However, the authorization server supporting this specification MUST only use the parameters included in the Request Object.[¶](#section-5-9)

### 5.1.

The client sends the authorization request as a Request Object to the authorization endpoint as the `request` parameter value.[¶](#section-5.1-1)

The following is an example of an authorization request using the `request` parameter (with line wraps within values for display purposes only):[¶](#section-5.1-2)

```
https://server.example.com/authorize?client_id=s6BhdRkqt3&
  request=eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyYmRjIn0.ewogICAgImlzcyI6
  ICJzNkJoZFJrcXQzIiwKICAgICJhdWQiOiAiaHR0cHM6Ly9zZXJ2ZXIuZXhhbXBs
  ZS5jb20iLAogICAgInJlc3BvbnNlX3R5cGUiOiAiY29kZSBpZF90b2tlbiIsCiAg
  ICAiY2xpZW50X2lkIjogInM2QmhkUmtxdDMiLAogICAgInJlZGlyZWN0X3VyaSI6
  ICJodHRwczovL2NsaWVudC5leGFtcGxlLm9yZy9jYiIsCiAgICAic2NvcGUiOiAi
  b3BlbmlkIiwKICAgICJzdGF0ZSI6ICJhZjBpZmpzbGRraiIsCiAgICAibm9uY2Ui
  OiAibi0wUzZfV3pBMk1qIiwKICAgICJtYXhfYWdlIjogODY0MDAKfQ.Nsxa_18VU
  ElVaPjqW_ToI1yrEJ67BgKb5xsuZRVqzGkfKrOIX7BCx0biSxYGmjK9KJPctH1OC
  0iQJwXu5YVY-vnW0_PLJb1C2HG-ztVzcnKZC2gE4i0vgQcpkUOCpW3SEYXnyWnKz
  uKzqSb1wAZALo5f89B_p6QA6j6JwBSRvdVsDPdulW8lKxGTbH82czCaQ50rLAg3E
  YLYaCb4ik4I1zGXE4fvim9FIMs8OCMmzwIB5S-ujFfzwFjoyuPEV4hJnoVUmXR_W
  9typPf846lGwA8h9G9oNTIuX8Ft2jfpnZdFmLg3_wr3Wa5q3a-lfbgF3S9H_8nN3
  j1i7tLR_5Nz-g
```
[¶](#section-5.1-3)

### 5.2.

The `request_uri` authorization request parameter enables OAuth authorization requests to be passed by reference rather than by value. This parameter is used identically to the `request` parameter, except that the Request Object value is retrieved from the resource identified by the specified URI rather than passed by value.[¶](#section-5.2-1)

The entire Request URI SHOULD NOT exceed 512 ASCII characters. There are two reasons for this restriction:[¶](#section-5.2-2)

1. Many phones on the market as of this writing still do not accept large payloads. The restriction is typically either 512 or 1024 ASCII characters.[¶](#section-5.2-3.1)
2. On a slow connection such as a 2G mobile connection, a large URL would cause a slow response; therefore, the use of such is not advisable from the user-experience point of view.[¶](#section-5.2-3.2)

The contents of the resource referenced by the `request_uri` MUST be a Request Object and MUST be reachable by the authorization server unless the URI was provided to the client by the authorization server. In the first case, the `request_uri` MUST be an `https` URI, as specified in [Section 2.7.2](https://www.rfc-editor.org/rfc/rfc7230#section-2.7.2) of \[\]. In the second case, it MUST be a URN, as specified in \[\].[¶](#section-5.2-4)

The following is an example of the contents of a Request Object resource that can be referenced by a `request_uri` (with line wraps within values for display purposes only):[¶](#section-5.2-5)

```
eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyYmRjIn0.ewogICAgImlzcyI6ICJzNkJoZF
JrcXQzIiwKICAgICJhdWQiOiAiaHR0cHM6Ly9zZXJ2ZXIuZXhhbXBsZS5jb20iLAog
ICAgInJlc3BvbnNlX3R5cGUiOiAiY29kZSBpZF90b2tlbiIsCiAgICAiY2xpZW50X2
lkIjogInM2QmhkUmtxdDMiLAogICAgInJlZGlyZWN0X3VyaSI6ICJodHRwczovL2Ns
aWVudC5leGFtcGxlLm9yZy9jYiIsCiAgICAic2NvcGUiOiAib3BlbmlkIiwKICAgIC
JzdGF0ZSI6ICJhZjBpZmpzbGRraiIsCiAgICAibm9uY2UiOiAibi0wUzZfV3pBMk1q
IiwKICAgICJtYXhfYWdlIjogODY0MDAKfQ.Nsxa_18VUElVaPjqW_ToI1yrEJ67BgK
b5xsuZRVqzGkfKrOIX7BCx0biSxYGmjK9KJPctH1OC0iQJwXu5YVY-vnW0_PLJb1C2
HG-ztVzcnKZC2gE4i0vgQcpkUOCpW3SEYXnyWnKzuKzqSb1wAZALo5f89B_p6QA6j6
JwBSRvdVsDPdulW8lKxGTbH82czCaQ50rLAg3EYLYaCb4ik4I1zGXE4fvim9FIMs8O
CMmzwIB5S-ujFfzwFjoyuPEV4hJnoVUmXR_W9typPf846lGwA8h9G9oNTIuX8Ft2jf
pnZdFmLg3_wr3Wa5q3a-lfbgF3S9H_8nN3j1i7tLR_5Nz-g
```
[¶](#section-5.2-6)

#### 5.2.1.

The client stores the Request Object resource either locally or remotely at a URI the authorization server can access. Such a facility may be provided by the authorization server or a trusted third party. For example, the authorization server may provide a URL to which the client POSTs the Request Object and obtains the Request URI. This URI is the Request Object URI, `request_uri`.[¶](#section-5.2.1-1)

It is possible for the Request Object to include values that are to be revealed only to the authorization server. As such, the `request_uri` MUST have appropriate entropy for its lifetime so that the URI is not guessable if publicly retrievable. For the guidance, refer to [Section 5.1.4.2.2](https://www.rfc-editor.org/rfc/rfc6819#section-5.1.4.2.2) of \[\] and "" \[\]. It is RECOMMENDED that the `request_uri` be removed after a reasonable timeout unless access control measures are taken.[¶](#section-5.2.1-2)

The following is an example of a Request Object URI value (with line wraps within values for display purposes only). In this example, a trusted third-party service hosts the Request Object.[¶](#section-5.2.1-3)

```
https://tfp.example.org/request.jwt/
  GkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM
```
[¶](#section-5.2.1-4)

#### 5.2.2.

The client sends the authorization request to the authorization endpoint.[¶](#section-5.2.2-1)

The following is an example of an authorization request using the `request_uri` parameter (with line wraps within values for display purposes only):[¶](#section-5.2.2-2)

```
https://server.example.com/authorize?
  client_id=s6BhdRkqt3
  &request_uri=https%3A%2F%2Ftfp.example.org%2Frequest.jwt
  %2FGkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM
```
[¶](#section-5.2.2-3)

#### 5.2.3.

Upon receipt of the Request, the authorization server MUST send an HTTP `GET` request to the `request_uri` to retrieve the referenced Request Object unless the Request Object is stored in a way so that the server can retrieve it through other mechanisms securely and parse it to recreate the authorization request parameters.[¶](#section-5.2.3-1)

The following is an example of this fetch process. In this example, a trusted third-party service hosts the Request Object.[¶](#section-5.2.3-2)

```
GET /request.jwt/GkurKxf5T0Y-mnPFCHqWOMiZi4VS138cQO_V7PZHAdM HTTP/1.1
Host: tfp.example.org
```
[¶](#section-5.2.3-3)

The following is an example of the fetch response:[¶](#section-5.2.3-4)

```
HTTP/1.1 200 OK
Date: Thu, 20 Aug 2020 23:52:39 GMT
Server: Apache/2.4.43 (tfp.example.org)
Content-type: application/oauth-authz-req+jwt
Content-Length: 797
Last-Modified: Wed, 19 Aug 2020 23:52:32 GMT

eyJhbGciOiJSUzI1NiIsImtpZCI6ImsyYmRjIn0.ewogICAgImlzcyI6ICJzNkJoZF
JrcXQzIiwKICAgICJhdWQiOiAiaHR0cHM6Ly9zZXJ2ZXIuZXhhbXBsZS5jb20iLAog
ICAgInJlc3BvbnNlX3R5cGUiOiAiY29kZSBpZF90b2tlbiIsCiAgICAiY2xpZW50X2
lkIjogInM2QmhkUmtxdDMiLAogICAgInJlZGlyZWN0X3VyaSI6ICJodHRwczovL2Ns
aWVudC5leGFtcGxlLm9yZy9jYiIsCiAgICAic2NvcGUiOiAib3BlbmlkIiwKICAgIC
JzdGF0ZSI6ICJhZjBpZmpzbGRraiIsCiAgICAibm9uY2UiOiAibi0wUzZfV3pBMk1q
IiwKICAgICJtYXhfYWdlIjogODY0MDAKfQ.Nsxa_18VUElVaPjqW_ToI1yrEJ67BgK
b5xsuZRVqzGkfKrOIX7BCx0biSxYGmjK9KJPctH1OC0iQJwXu5YVY-vnW0_PLJb1C2
HG-ztVzcnKZC2gE4i0vgQcpkUOCpW3SEYXnyWnKzuKzqSb1wAZALo5f89B_p6QA6j6
JwBSRvdVsDPdulW8lKxGTbH82czCaQ50rLAg3EYLYaCb4ik4I1zGXE4fvim9FIMs8O
CMmzwIB5S-ujFfzwFjoyuPEV4hJnoVUmXR_W9typPf846lGwA8h9G9oNTIuX8Ft2jf
pnZdFmLg3_wr3Wa5q3a-lfbgF3S9H_8nN3j1i7tLR_5Nz-g
```
[¶](#section-5.2.3-5)

## 6.

### 6.1.

If the Request Object is encrypted, the authorization server MUST decrypt the JWT in accordance with the \[\] specification.[¶](#section-6.1-1)

The result is a signed Request Object.[¶](#section-6.1-2)

If decryption fails, the authorization server MUST return an `invalid_request_object` error to the client in response to the authorization request.[¶](#section-6.1-3)

### 6.2.

The authorization server MUST validate the signature of the JWS-signed \[\] Request Object. If a `kid` Header Parameter is present, the key identified MUST be the key used and MUST be a key associated with the client. The signature MUST be validated using a key associated with the client and the algorithm specified in the `alg` Header Parameter. Algorithm verification MUST be performed, as specified in Sections [3.1](https://www.rfc-editor.org/rfc/rfc8725#section-3.1) and [3.2](https://www.rfc-editor.org/rfc/rfc8725#section-3.2) of \[\].[¶](#section-6.2-1)

If the key is not associated with the client or if signature validation fails, the authorization server MUST return an `invalid_request_object` error to the client in response to the authorization request.[¶](#section-6.2-2)

### 6.3.

The authorization server MUST extract the set of authorization request parameters from the Request Object value. The authorization server MUST only use the parameters in the Request Object, even if the same parameter is provided in the query parameter. The client ID values in the `client_id` request parameter and in the Request Object `client_id` claim MUST be identical. The authorization server then validates the request, as specified in \[\].[¶](#section-6.3-1)

If the Client ID check or the request validation fails, then the authorization server MUST return an error to the client in response to the authorization request, as specified in [Section 5.2](https://www.rfc-editor.org/rfc/rfc6749#section-5.2) of \[\] (OAuth 2.0).[¶](#section-6.3-2)

## 7.

The authorization server response is created and sent to the client as in [Section 4](https://www.rfc-editor.org/rfc/rfc6749#section-4) of \[\] (OAuth 2.0).[¶](#section-7-1)

In addition, this document uses these additional error values:[¶](#section-7-2)

invalid\_request\_uri

The `request_uri` in the authorization request returns an error or contains invalid data.[¶](#section-7-3.2)

invalid\_request\_object

The request parameter contains an invalid Request Object.[¶](#section-7-3.4)

request\_not\_supported

The authorization server does not support the use of the `request` parameter.[¶](#section-7-3.6)

request\_uri\_not\_supported

The authorization server does not support the use of the `request_uri` parameter.[¶](#section-7-3.8)

## 8.

Client implementations supporting the Request Object URI method MUST support TLS, following \[\].[¶](#section-8-1)

To protect against information disclosure and tampering, confidentiality protection MUST be applied using TLS with a cipher suite that provides confidentiality and integrity protection.[¶](#section-8-2)

HTTP clients MUST also verify the TLS server certificate, using DNS-ID \[\], to avoid man-in-the-middle attacks. The rules and guidelines defined in \[\] apply here, with the following considerations:[¶](#section-8-3)

- Support for DNS-ID identifier type (that is, the dNSName identity in the subjectAltName extension) is REQUIRED. Certification authorities that issue server certificates MUST support the DNS-ID identifier type, and the DNS-ID identifier type MUST be present in server certificates.[¶](#section-8-4.1)
- DNS names in server certificates MAY contain the wildcard character `*`.[¶](#section-8-4.2)
- Clients MUST NOT use CN-ID identifiers; a Common Name field (CN field) may be present in the server certificate's subject name but MUST NOT be used for authentication within the rules described in \[\].[¶](#section-8-4.3)
- SRV-ID and URI-ID as described in [Section 6.5](https://www.rfc-editor.org/rfc/rfc6125#section-6.5) of \[\] MUST NOT be used for comparison.[¶](#section-8-4.4)

## 9.

### 9.1.

Since the Request Object is a JWT, the core JWT claims cannot be used for any purpose in the Request Object other than for what JWT dictates. Thus, they have been registered as OAuth authorization request parameters to avoid future OAuth extensions using them with different meanings.[¶](#section-9.1-1)

This specification adds the following values to the "OAuth Parameters" registry \[\] established by \[\].[¶](#section-9.1-2)

Name:

`iss` [¶](#section-9.1-3.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-3.4)

Change Controller:

IETF [¶](#section-9.1-3.6)

Specification Document(s):

This document and [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.1) of \[\].[¶](#section-9.1-3.8)

Name:

`sub` [¶](#section-9.1-4.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-4.4)

Change Controller:

IETF [¶](#section-9.1-4.6)

Specification Document(s):

This document and [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.2) of \[\].[¶](#section-9.1-4.8)

Name:

`aud` [¶](#section-9.1-5.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-5.4)

Change Controller:

IETF [¶](#section-9.1-5.6)

Specification Document(s):

This document and [Section 4.1.3](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.3) of \[\].[¶](#section-9.1-5.8)

Name:

`exp` [¶](#section-9.1-6.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-6.4)

Change Controller:

IETF [¶](#section-9.1-6.6)

Specification Document(s):

This document and [Section 4.1.4](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.4) of \[\].[¶](#section-9.1-6.8)

Name:

`nbf` [¶](#section-9.1-7.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-7.4)

Change Controller:

IETF [¶](#section-9.1-7.6)

Specification Document(s):

This document and [Section 4.1.5](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.5) of \[\].[¶](#section-9.1-7.8)

Name:

`iat` [¶](#section-9.1-8.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-8.4)

Change Controller:

IETF [¶](#section-9.1-8.6)

Specification Document(s):

This document and [Section 4.1.6](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.6) of \[\].[¶](#section-9.1-8.8)

Name:

`jti` [¶](#section-9.1-9.2)

Parameter Usage Location:

authorization request [¶](#section-9.1-9.4)

Change Controller:

IETF [¶](#section-9.1-9.6)

Specification Document(s):

This document and [Section 4.1.7](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.7) of \[\].[¶](#section-9.1-9.8)

### 9.4.

#### 9.4.1.

This section registers the `application/oauth-authz-req+jwt` media type \[\] in the "Media Types" registry \[\] in the manner described in \[\]. It can be used to indicate that the content is a JWT containing Request Object claims.[¶](#section-9.4.1-1)

Type name:

application [¶](#section-9.4.1-2.2)

Subtype name:

oauth-authz-req+jwt [¶](#section-9.4.1-2.4)

Required parameters:

N/A [¶](#section-9.4.1-2.6)

Optional parameters:

N/A [¶](#section-9.4.1-2.8)

Encoding considerations:

binary; a Request Object is a JWT; JWT values are encoded as a series of base64url-encoded values (some of which may be the empty string) separated by period (`.`) characters.[¶](#section-9.4.1-2.10)

Security considerations:

See of RFC 9101 [¶](#section-9.4.1-2.12)

Interoperability considerations:

N/A [¶](#section-9.4.1-2.14)

Published specification:

of RFC 9101 [¶](#section-9.4.1-2.16)

Applications that use this media type:

Applications that use Request Objects to make an OAuth 2.0 authorization request [¶](#section-9.4.1-2.18)

Fragment identifier considerations:

N/A [¶](#section-9.4.1-2.20)

Additional information:

Deprecated alias names for this type:

N/A [¶](#section-9.4.1-2.22.2.2)

Magic number(s):

N/A [¶](#section-9.4.1-2.22.2.4)

File extension(s):

N/A [¶](#section-9.4.1-2.22.2.6)

Macintosh file type code(s):

N/A [¶](#section-9.4.1-2.22.2.8)

Person & email address to contact for further information:

Nat Sakimura <nat@nat.consulting> [¶](#section-9.4.1-2.24)

Intended usage:

COMMON [¶](#section-9.4.1-2.26)

Restrictions on usage:

none [¶](#section-9.4.1-2.28)

Author:

Nat Sakimura <nat@nat.consulting> [¶](#section-9.4.1-2.30)

Change controller:

IETF [¶](#section-9.4.1-2.32)

Provisional registration?

No [¶](#section-9.4.1-2.34)

## 10.

In addition to all the \[\], the security considerations in \[\], \[\], \[\], and \[\] need to be considered. Also, there are several academic papers such as \[\] that provide useful insight into the security properties of protocols like OAuth.[¶](#section-10-1)

In consideration of the above, this document advises taking the following security considerations into account.[¶](#section-10-2)

### 10.1.

When sending the Authorization Request Object through the `request` parameter, it MUST be either signed using \[\] or signed and then encrypted using \[\] and \[\], respectively, with algorithms considered appropriate at the time.[¶](#section-10.1-1)

### 10.2.

The source of the authorization request MUST always be verified. There are several ways to do it:[¶](#section-10.2-1)

(a)

Verifying the JWS Signature of the Request Object.[¶](#section-10.2-2.1)

(b)

Verifying that the symmetric key for the JWE encryption is the correct one if the JWE is using symmetric encryption. Note, however, that if public key encryption is used, no source authentication is enabled by the encryption, as any party can encrypt to the public key.[¶](#section-10.2-2.2)

(c)

Verifying the TLS Server Identity of the Request Object URI. In this case, the authorization server MUST know out-of-band that the client uses the Request Object URI and only the client is covered by the TLS certificate. In general, this is not a reliable method.[¶](#section-10.2-2.3)

(d)

When an authorization server implements a service that returns a Request Object URI in exchange for a Request Object, the authorization server MUST perform client authentication to accept the Request Object and bind the client identifier to the Request Object URI it is providing. It MUST validate the signature, per (a). Since the Request Object URI can be replayed, the lifetime of the Request Object URI MUST be short and preferably one-time use. The entropy of the Request Object URI MUST be sufficiently large. The adequate shortness of the validity and the entropy of the Request Object URI depends on the risk calculation based on the value of the resource being protected. A general guidance for the validity time would be less than a minute, and the Request Object URI is to include a cryptographic random value of 128 bits or more at the time of the writing of this specification.[¶](#section-10.2-2.4)

(e)

When a trusted third-party service returns a Request Object URI in exchange for a Request Object, it MUST validate the signature, per (a). In addition, the authorization server MUST be trusted by the third-party service and MUST know out-of-band that the client is also trusted by it.[¶](#section-10.2-2.5)

### 10.3.

Although this specification does not require them, research such as \[\] points out that it is a good practice to explicitly state the intended interaction endpoints and the message position in the sequence in a tamper-evident manner so that the intent of the initiator is unambiguous. It is RECOMMENDED by this specification to use this practice for the following endpoints defined in \[\], \[\], and \[\]:[¶](#section-10.3-1)

(a)

Protected resources (`protected_resources`) [¶](#section-10.3-2.1)

(b)

Authorization endpoint (`authorization_endpoint`) [¶](#section-10.3-2.2)

(c)

Redirection URI (`redirect_uri`) [¶](#section-10.3-2.3)

(d)

Token endpoint (`token_endpoint`) [¶](#section-10.3-2.4)

Further, if dynamic discovery is used, then this practice also applies to the discovery-related endpoints.[¶](#section-10.3-3)

In \[\], while the redirection URI is included in the authorization request, others are not. As a result, the same applies to the Authorization Request Object.[¶](#section-10.3-4)

### 10.4.

The introduction of `request_uri` introduces several attack possibilities. Consult the security considerations in [Section 7](https://www.rfc-editor.org/rfc/rfc3986#section-7) of \[\] for more information regarding risks associated with URIs.[¶](#section-10.4-1)

#### 10.4.1.

A set of malicious clients can launch a DoS attack to the authorization server by pointing the `request_uri` to a URI that returns extremely large content or is extremely slow to respond. Under such an attack, the server may use up its resource and start failing.[¶](#section-10.4.1-1)

Similarly, a malicious client can specify a `request_uri` value that itself points to an authorization request URI that uses `request_uri` to cause the recursive lookup.[¶](#section-10.4.1-2)

To prevent such an attack from succeeding, the server should a) check that the value of the `request_uri` parameter does not point to an unexpected location, b) check that the media type of the response is `application/oauth-authz-req+jwt`, c) implement a timeout for obtaining the content of `request_uri`, and d) not perform recursive GET on the `request_uri`.[¶](#section-10.4.1-3)

#### 10.4.2.

The value of `request_uri` is not signed; thus, it can be tampered with by a man-in-the-browser attacker. Several attack possibilities arise because of this. For example, a) an attacker may create another file that the rewritten URI points to, making it possible to request extra scope, or b) an attacker may launch a DoS attack on a victim site by setting the value of `request_uri` to be that of the victim.[¶](#section-10.4.2-1)

To prevent such an attack from succeeding, the server should a) check that the value of the `request_uri` parameter does not point to an unexpected location, b) check that the media type of the response is `application/oauth-authz-req+jwt`, and c) implement a timeout for obtaining the content of `request_uri`.[¶](#section-10.4.2-2)

### 10.5.

Unless the protocol used by the client and the server is locked down to use an OAuth JWT-Secured Authorization Request (JAR), it is possible for an attacker to use RFC 6749 requests to bypass all the protection provided by this specification.[¶](#section-10.5-1)

To prevent this kind of attack, this specification defines new client metadata and server metadata values, both named `require_signed_request_object`, whose values are both booleans.[¶](#section-10.5-2)

When the value of it as client metadata is `true`, then the server MUST reject the authorization request from the client that does not conform to this specification. It MUST also reject the request if the Request Object uses an `alg` value of `none` when this server metadata value is `true`. If omitted, the default value is `false`.[¶](#section-10.5-3)

When the value of it as server metadata is `true`, then the server MUST reject the authorization request from any client that does not conform to this specification. It MUST also reject the request if the Request Object uses an `alg` value of `none`. If omitted, the default value is `false`.[¶](#section-10.5-4)

Note that even if `require_signed_request_object` metadata values are not present, the client MAY use signed Request Objects, provided that there are signing algorithms mutually supported by the client and the server. Use of signing algorithm metadata is described in.[¶](#section-10.5-5)

### 10.6.

Current security considerations can be found in "" \[\]. This supersedes the TLS version recommendations in \[\].[¶](#section-10.6-1)

### 10.7.

Given that OAuth parameter values are being sent in two different places, as normal OAuth parameters and as Request Object claims, implementations must guard against attacks that could use mismatching parameter values to obtain unintended outcomes. That is the reason that the two client ID values MUST match, the reason that only the parameter values from the Request Object are to be used, and the reason that neither `request` nor `request_uri` can appear in a Request Object.[¶](#section-10.7-1)

### 10.8.

As described in [Section 2.8](https://www.rfc-editor.org/rfc/rfc8725#section-2.8) of \[\], attackers may attempt to use a JWT issued for one purpose in a context that it was not intended for. The mitigations described for these attacks can be applied to Request Objects.[¶](#section-10.8-1)

One way that an attacker might attempt to repurpose a Request Object is to try to use it as a client authentication JWT, as described in [Section 2.2](https://www.rfc-editor.org/rfc/rfc7523#section-2.2) of \[\]. A simple way to prevent this is to never use the client ID as the `sub` value in a Request Object.[¶](#section-10.8-2)

Another way to prevent cross-JWT confusion is to use explicit typing, as described in [Section 3.11](https://www.rfc-editor.org/rfc/rfc8725#section-3.11) of \[\]. One would explicitly type a Request Object by including a `typ` Header Parameter with the value `oauth-authz-req+jwt` (which is registered in ). Note, however, that requiring explicitly typed Request Objects at existing authorization servers will break most existing deployments, as existing clients are already commonly using untyped Request Objects, especially with [[OpenID Connect]] \[\]. However, requiring explicit typing would be a good idea for new OAuth deployment profiles where compatibility with existing deployments is not a consideration.[¶](#section-10.8-3)

Finally, yet another way to prevent cross-JWT confusion is to use a key management regime in which keys used to sign Request Objects are identifiably distinct from those used for other purposes. Then, if an adversary attempts to repurpose the Request Object in another context, a key mismatch will occur, thwarting the attack.[¶](#section-10.8-4)

## 11.

When the client is being granted access to a protected resource containing personal data, both the client and the authorization server need to adhere to Privacy Principles. "" \[\] gives excellent guidance on the enhancement of protocol design and implementation. The provisions listed in it should be followed.[¶](#section-11-1)

Most of the provisions would apply to "" \[\] and "" \[\] and are not specific to this specification. In what follows, only the provisions specific to this specification are noted.[¶](#section-11-2)

### 11.1.

When the client is being granted access to a protected resource containing personal data, the client SHOULD limit the collection of personal data to that which is within the bounds of applicable law and strictly necessary for the specified purpose(s).[¶](#section-11.1-1)

It is often hard for the user to find out if the personal data asked for is strictly necessary. A trusted third-party service can help the user by examining the client request, comparing it to the proposed processing by the client, and certifying the request. After the certification, the client, when making an authorization request, can submit an authorization request to the trusted third-party service to obtain the Request Object URI. This process has two steps:[¶](#section-11.1-2)

(1)

(Certification Process) The trusted third-party service examines the business process of the client and determines what claims they need; this is the certification process. Once the client is certified, they are issued a client credential to authenticate against to push Request Objects to the trusted third-party service to get the `request_uri`.[¶](#section-11.1-3.1)

(2)

(Translation Process) The client uses the client credential that it got to push the Request Object to the trusted third-party service to get the `request_uri`. The trusted third-party service also verifies that the Request Object is consistent with the claims that the client is eligible for, per the prior step.[¶](#section-11.1-3.2)

Upon receiving such a Request Object URI in the authorization request, the authorization server first verifies that the authority portion of the Request Object URI is a legitimate one for the trusted third-party service. Then, the authorization server issues an HTTP GET request to the Request Object URI. Upon connecting, the authorization server MUST verify that the server identity represented in the TLS certificate is legitimate for the Request Object URI. Then, the authorization server can obtain the Request Object, which includes the `client_id` representing the client.[¶](#section-11.1-4)

The Consent screen MUST indicate the client and SHOULD indicate that the request has been vetted by the trusted third-party service for the adherence to the collection limitation principle.[¶](#section-11.1-5)

## 12.

### 12.1.

\[RFC2119\]

Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, < [https://www.rfc-editor.org/info/rfc2119](https://www.rfc-editor.org/info/rfc2119) >.

\[RFC3629\]

Yergeau, F., "UTF-8, a transformation format of ISO 10646", STD 63, RFC 3629, DOI 10.17487/RFC3629, November 2003, < [https://www.rfc-editor.org/info/rfc3629](https://www.rfc-editor.org/info/rfc3629) >.

\[RFC[[3986]]\]

Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform Resource Identifier (URI): Generic Syntax", STD 66, RFC [[3986]], DOI 10.17487/RFC[[3986]], January 2005, < [https://www.rfc-editor.org/info/rfc3986](https://www.rfc-editor.org/info/rfc3986) >.

\[RFC6125\]

Saint-Andre, P. and J. Hodges, "Representation and Verification of Domain-Based Application Service Identity within Internet Public Key Infrastructure Using X.509 (PKIX) Certificates in the Context of Transport Layer Security (TLS)", RFC 6125, DOI 10.17487/RFC6125, March 2011, < [https://www.rfc-editor.org/info/rfc6125](https://www.rfc-editor.org/info/rfc6125) >.

\[RFC6749\]

Hardt, D., Ed., "The OAuth 2.0 Authorization Framework", RFC 6749, DOI 10.17487/RFC6749, October 2012, < [https://www.rfc-editor.org/info/rfc6749](https://www.rfc-editor.org/info/rfc6749) >.

\[RFC[[6750]]\]

Jones, M. and D. Hardt, "The OAuth 2.0 Authorization Framework: [[Bearer Token]] Usage", RFC [[6750]], DOI 10.17487/RFC[[6750]], October 2012, < [https://www.rfc-editor.org/info/rfc6750](https://www.rfc-editor.org/info/rfc6750) >.

\[RFC7230\]

Fielding, R., Ed. and J. Reschke, Ed., "Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing", RFC 7230, DOI 10.17487/RFC7230, June [[2014]], < [https://www.rfc-editor.org/info/rfc7230](https://www.rfc-editor.org/info/rfc7230) >.

\[RFC[[7515]]\]

Jones, M., Bradley, J., and N. Sakimura, "JSON Web Signature (JWS)", RFC [[7515]], DOI 10.17487/RFC[[7515]], May 2015, < [https://www.rfc-editor.org/info/rfc7515](https://www.rfc-editor.org/info/rfc7515) >.

\[RFC[[7516]]\]

Jones, M. and J. Hildebrand, "JSON Web Encryption (JWE)", RFC [[7516]], DOI 10.17487/RFC[[7516]], May 2015, < [https://www.rfc-editor.org/info/rfc7516](https://www.rfc-editor.org/info/rfc7516) >.

\[RFC[[7518]]\]

Jones, M., "JSON Web Algorithms (JWA)", RFC [[7518]], DOI 10.17487/RFC[[7518]], May 2015, < [https://www.rfc-editor.org/info/rfc7518](https://www.rfc-editor.org/info/rfc7518) >.

\[RFC[[7519]]\]

Jones, M., Bradley, J., and N. Sakimura, "JSON Web Token (JWT)", RFC [[7519]], DOI 10.17487/RFC[[7519]], May 2015, < [https://www.rfc-editor.org/info/rfc7519](https://www.rfc-editor.org/info/rfc7519) >.

\[RFC7525\]

Sheffer, Y., Holz, R., and P. Saint-Andre, "Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)", BCP 195, RFC 7525, DOI 10.17487/RFC7525, May 2015, < [https://www.rfc-editor.org/info/rfc7525](https://www.rfc-editor.org/info/rfc7525) >.

\[RFC8141\]

Saint-Andre, P. and J. Klensin, "Uniform Resource Names (URNs)", RFC 8141, DOI 10.17487/RFC8141, April 2017, < [https://www.rfc-editor.org/info/rfc8141](https://www.rfc-editor.org/info/rfc8141) >.

\[RFC8174\]

Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, < [https://www.rfc-editor.org/info/rfc8174](https://www.rfc-editor.org/info/rfc8174) >.

\[RFC8259\]

Bray, T., Ed., "The JavaScript Object Notation (JSON) Data Interchange Format", STD 90, RFC 8259, DOI 10.17487/RFC8259, December 2017, < [https://www.rfc-editor.org/info/rfc8259](https://www.rfc-editor.org/info/rfc8259) >.

\[RFC[[8414]]\]

Jones, M., Sakimura, N., and J. Bradley, [["OAuth 2.0]] Authorization Server Metadata", RFC [[8414]], DOI 10.17487/RFC[[8414]], June 2018, < [https://www.rfc-editor.org/info/rfc8414](https://www.rfc-editor.org/info/rfc8414) >.

### 12.2.

\[BASIN\]

Basin, D., Cremers, C., and S. Meier, "Provably Repairing the ISO/IEC 9798 Standard for [[Entity]] Authentication", Journal of Computer Security - Security and Trust Principles, Volume 21, Issue 6, pp. 817-846, November 2013, < [https://www.cs.ox.ac.uk/people/cas.cremers/downloads/papers/BCM2012-iso9798.pdf](https://www.cs.ox.ac.uk/people/cas.cremers/downloads/papers/BCM2012-iso9798.pdf) >.

\[CapURLs\]

Tennison, J., Ed., "Good Practices for Capability URLs", W3C First Public Working Draft, 18 February [[2014]], < [https://www.w3.org/TR/capability-urls/](https://www.w3.org/TR/capability-urls/) >.

\[IANA.JWT.Claims\]

IANA, "JSON Web Token (JWT)", < [https://www.iana.org/assignments/jwt](https://www.iana.org/assignments/jwt) >.

\[IANA.MediaTypes\]

IANA, "Media Types", < [https://www.iana.org/assignments/media-types](https://www.iana.org/assignments/media-types) >.

\[IANA.OAuth.Parameters\]

IANA, "OAuth Parameters", < [https://www.iana.org/assignments/oauth-parameters](https://www.iana.org/assignments/oauth-parameters) >.

\[OpenID.Core\]

Sakimura, N., Bradley, J., Jones, M.B., de Medeiros, B., and C. Mortimore, "[[OpenID Connect]] Core 1.0 incorporating errata set 1", OpenID Foundation Standards, 8 November [[2014]], < [http://openid.net/specs/openid-connect-core-1\_0.html](http://openid.net/specs/openid-connect-core-1_0.html) >.

\[RFC2046\]

Freed, N. and N. Borenstein, "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types", RFC 2046, DOI 10.17487/RFC2046, November 1996, < [https://www.rfc-editor.org/info/rfc2046](https://www.rfc-editor.org/info/rfc2046) >.

\[RFC[[6819]]\]

Lodderstedt, T., Ed., McGloin, M., and P. Hunt, [["OAuth 2.0]] [[Threat Model]] and Security Considerations", RFC [[6819]], DOI 10.17487/RFC[[6819]], January 2013, < [https://www.rfc-editor.org/info/rfc6819](https://www.rfc-editor.org/info/rfc6819) >.

\[RFC6838\]

Freed, N., Klensin, J., and T. Hansen, "Media Type Specifications and Registration Procedures", BCP 13, RFC 6838, DOI 10.17487/RFC6838, January 2013, < [https://www.rfc-editor.org/info/rfc6838](https://www.rfc-editor.org/info/rfc6838) >.

\[RFC6973\]

Cooper, A., Tschofenig, H., Aboba, B., Peterson, J., Morris, J., Hansen, M., and R. Smith, "Privacy Considerations for Internet Protocols", RFC 6973, DOI 10.17487/RFC6973, July 2013, < [https://www.rfc-editor.org/info/rfc6973](https://www.rfc-editor.org/info/rfc6973) >.

\[RFC[[7523]]\]

Jones, M., Campbell, B., and C. Mortimore, "JSON Web Token (JWT) [[Profile]] for OAuth 2.0 Client Authentication and Authorization Grants", RFC [[7523]], DOI 10.17487/RFC[[7523]], May 2015, < [https://www.rfc-editor.org/info/rfc7523](https://www.rfc-editor.org/info/rfc7523) >.

\[RFC[[7591]]\]

Richer, J., Ed., Jones, M., Bradley, J., Machulak, M., and P. Hunt, [["OAuth 2.0]] [[Dynamic Client Registration]] Protocol", RFC [[7591]], DOI 10.17487/RFC[[7591]], July 2015, < [https://www.rfc-editor.org/info/rfc7591](https://www.rfc-editor.org/info/rfc7591) >.

\[RFC8725\]

Sheffer, Y., Hardt, D., and M. Jones, "JSON Web Token Best Current Practices", BCP 225, RFC 8725, DOI 10.17487/RFC8725, February 2020, < [https://www.rfc-editor.org/info/rfc8725](https://www.rfc-editor.org/info/rfc8725) >.

## Acknowledgements

The following people contributed to the creation of this document in the OAuth Working Group and other IETF roles. (Affiliations at the time of the contribution are used.) [¶](#appendix-A-1)

(Amazon), (Google),, (as AD), (Ping Identity), (as AD), (as AD), (Connect2id), (as AD), (as GENART), (as AD), (as SECDIR), (as AD), (as OPSDIR), (as SECDIR), (yes.com),, (Telstra), (as AD), (Deutsche Telecom), (Google), (as AD), (Facebook), (Google), (Facebook), (Auth0), (ARM), (as AD), and (as AD).[¶](#appendix-A-2)

The following people contributed to creating this document through the \[\].[¶](#appendix-A-3)

(Ping Identity), (AOL), (Mixi), (Illumila), (Google), (TACT), and (MITRE).[¶](#appendix-A-4)

## Authors' Addresses

Nat Sakimura

NAT.Consulting

2-22-17 Naka

Kunitachi, Tokyo 186-0004

Japan

Phone: [+81-42-580-7401](tel:+81-42-580-7401)

Email: [nat@nat.consulting](mailto:nat@nat.consulting)

URI: [https://nat.sakimura.org/](https://nat.sakimura.org/)

John Bradley

Yubico

Sucursal Talagante

Casilla 177

Talagante

RM

Chile

Phone: [+1.202.630.5272](tel:+1.202.630.5272)

Email: [rfc9101@ve7jtb.com](mailto:rfc9101@ve7jtb.com)

URI: [http://www.thread-safe.com/](http://www.thread-safe.com/)

Michael B. Jones

Microsoft

One Microsoft Way

Redmond, Washington 98052

United States of America

Email: [mbj@microsoft.com](mailto:mbj@microsoft.com)

URI: [https://self-issued.info/](https://self-issued.info/)
## 相关笔记

- [[RFC 9449 DPoP]]
- [[RFC 9700 Security BCP]]
- [[RFC 8693 Token Exchange]]
- [[RFC 9068 JWT Access Token]]
- [[RFC 8705 mTLS]]
- [[RFC 9126 PAR]]
- [[RFC 9207 Issuer ID]]
- [["OAuth 2.0 授权框架（RFC 6749）"]]
