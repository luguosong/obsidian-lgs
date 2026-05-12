| RFC 9068 | OAuth 2.0 Access Token JWT [[Profile]] | October 2021 |
| --- | --- | --- |
| Bertocci | Standards Track | \[Page\] |

## RFC 9068

## Abstract

This specification defines a profile for issuing OAuth 2.0 access tokens in JSON Web Token (JWT) format. Authorization servers and resource servers from different vendors can leverage this profile to issue and consume access tokens in an interoperable manner.[¶](#section-abstract-1)

## Status of This Memo

This is an Internet Standards Track document.[¶](#section-boilerplate.1-1)

This document is a product of the Internet Engineering Task Force (IETF). It represents the consensus of the IETF community. It has received public review and has been approved for publication by the Internet Engineering Steering Group (IESG). Further information on Internet Standards is available in Section 2 of RFC 7841.[¶](#section-boilerplate.1-2)

Information about the current status of this document, any errata, and how to provide feedback on it may be obtained at [https://www.rfc-editor.org/info/rfc9068](https://www.rfc-editor.org/info/rfc9068).[¶](#section-boilerplate.1-3)

## 1.

The original \[\] specification does not mandate any specific format for access tokens. While that remains perfectly appropriate for many important scenarios, in-market use has shown that many commercial OAuth 2.0 implementations elected to issue access tokens using a format that can be parsed and validated by resource servers directly, without further authorization server involvement. The approach is particularly common in topologies where the authorization server and resource server are not co-located, are not run by the same entity, or are otherwise separated by some boundary. At the time of writing, many commercial implementations leverage the \[\] format.[¶](#section-1-1)

Many vendor-specific JWT access tokens share the same functional layout, using JWT claims to convey the information needed to support a common set of use cases: token validation, transporting authorization information in the form of scopes and entitlements, carrying identity information about the subject, and so on. The differences are mostly confined to the claim names and syntax used to represent the same entities, suggesting that interoperability could be easily achieved by standardizing a common set of claims and validation rules.[¶](#section-1-2)

The assumption that access tokens are associated with specific information doesn't appear only in commercial implementations. Various specifications in the OAuth 2.0 family (such as \[\], \[\], and others) postulate the presence of scoping mechanisms, such as an audience, in access tokens. The family of specifications associated with introspection also indirectly suggests a fundamental set of information that access tokens are expected to carry or at least be associated with.[¶](#section-1-3)

This specification aims to provide a standardized and interoperable profile as an alternative to the proprietary JWT access token layouts going forward. Besides defining a common set of mandatory and optional claims, the profile provides clear indications on how authorization request parameters determine the content of the issued JWT access token, how an authorization server can publish metadata relevant to the JWT access tokens it issues, and how a resource server should validate incoming JWT access tokens.[¶](#section-1-4)

Finally, this specification provides security and privacy considerations meant to prevent common mistakes and anti-patterns that are likely to occur in naive use of the JWT format to represent access tokens.[¶](#section-1-5)

Please note: Although both this document and \[\] use JSON Web Tokens in the context of the [[OAuth2]] framework, the two specifications differ in both intent and mechanics. Whereas \[\] defines how a JWT [[Bearer Token]] can be used to request an access token, this document describes how to encode access tokens in JWT format.[¶](#section-1-6)

### 1.1.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 \[\] \[\] when, and only when, they appear in all capitals, as shown here.[¶](#section-1.1-1)

### 1.2.

JWT access token:

An OAuth 2.0 access token encoded in JWT format and complying with the requirements described in this specification.[¶](#section-1.2-1.2)

This specification uses the terms "access token", "refresh token", "authorization server", "resource server", "authorization endpoint", "authorization request", "authorization response", "token endpoint", "grant type", "access token request", "access token response", and "client" defined by \[\].[¶](#section-1.2-2)

## 2.

### 2.2.

The following claims are used in the JWT access token data structure.[¶](#section-2.2-1)

iss

REQUIRED - as defined in [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.1) of \[\].[¶](#section-2.2-2.2)

exp

REQUIRED - as defined in [Section 4.1.4](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.4) of \[\].[¶](#section-2.2-2.4)

aud

REQUIRED - as defined in [Section 4.1.3](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.3) of \[\]. See for indications on how an authorization server should determine the value of "aud" depending on the request.[¶](#section-2.2-2.6)

sub

REQUIRED - as defined in [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.2) of \[\]. In cases of access tokens obtained through grants where a resource owner is involved, such as the authorization code grant, the value of "sub" SHOULD correspond to the subject identifier of the resource owner. In cases of access tokens obtained through grants where no resource owner is involved, such as the client credentials grant, the value of "sub" SHOULD correspond to an identifier the authorization server uses to indicate the client application. See for more details on this scenario. Also, see for a discussion about how different choices in assigning "sub" values can impact privacy.[¶](#section-2.2-2.8)

client\_id

REQUIRED - as defined in [Section 4.3](https://www.rfc-editor.org/rfc/rfc8693#section-4.3) of \[\].[¶](#section-2.2-2.10)

iat

REQUIRED - as defined in [Section 4.1.6](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.6) of \[\]. This claim identifies the time at which the JWT access token was issued.[¶](#section-2.2-2.12)

jti

REQUIRED - as defined in [Section 4.1.7](https://www.rfc-editor.org/rfc/rfc7519#section-4.1.7) of \[\].[¶](#section-2.2-2.14)

#### 2.2.1.

The claims listed in this section MAY be issued in the context of authorization grants involving the resource owner and reflect the types and strength of authentication in the access token that the authentication server enforced prior to returning the authorization response to the client. Their values are fixed and remain the same across all access tokens that derive from a given authorization response, whether the access token was obtained directly in the response (e.g., via the implicit flow) or after one or more token exchanges (e.g., obtaining a fresh access token using a refresh token or exchanging one access token for another via \[\] procedures).[¶](#section-2.2.1-1)

auth\_time

OPTIONAL - as defined in Section 2 of \[\].[¶](#section-2.2.1-2.2)

acr

OPTIONAL - as defined in Section 2 of \[\].[¶](#section-2.2.1-2.4)

amr

OPTIONAL - as defined in Section 2 of \[\].[¶](#section-2.2.1-2.6)

#### 2.2.2.

In the context of authorization grants involving the resource owner, commercial authorization servers will often include resource owner attributes directly in access tokens so that resource servers can consume them directly for authorization or other purposes without any further round trips to introspection (\[\]) or UserInfo (\[\]) endpoints. This is particularly common in scenarios where the client and the resource server belong to the same entity and are part of the same solution, as is the case for first-party clients invoking their own backend API.[¶](#section-2.2.2-1)

This profile does not introduce any mechanism for a client to directly request the presence of specific claims in JWT access tokens, as the authorization server can determine what additional claims are required by a particular resource server by taking the client\_id of the client and the "scope" and the "resource" parameters included in the request into consideration.[¶](#section-2.2.2-2)

Any additional identity attribute whose semantic is well described by an entry in the "JSON Web Token (JWT)" IANA registry introduced in \[\] SHOULD be encoded using the corresponding claim name, if that attribute is to be included in the JWT access token. Note that the JWT IANA registry includes the claims found in Section 5.1 of \[\].[¶](#section-2.2.2-3)

Authorization servers MAY return arbitrary attributes not defined in any existing specification, as long as the corresponding claim names are collision resistant or the access tokens are meant to be used only within a private subsystem. Please refer to Sections [4.2](https://www.rfc-editor.org/rfc/rfc7519#section-4.2) and [4.3](https://www.rfc-editor.org/rfc/rfc7519#section-4.3) of \[\] for details.[¶](#section-2.2.2-4)

Authorization servers including resource owner attributes in JWT access tokens need to exercise care and verify that all privacy requirements are met, as discussed in.[¶](#section-2.2.2-5)

#### 2.2.3.

If an authorization request includes a scope parameter, the corresponding issued JWT access token SHOULD include a "scope" claim as defined in [Section 4.2](https://www.rfc-editor.org/rfc/rfc8693#section-4.2) of \[\].[¶](#section-2.2.3-1)

All the individual scope strings in the "scope" claim MUST have meaning for the resources indicated in the "aud" claim. See for more considerations about the relationship between scope strings and resources indicated by the "aud" claim.[¶](#section-2.2.3-2)

##### 2.2.3.1.

Many authorization servers embed authorization attributes that go beyond the delegated scenarios described by \[\] in the access tokens they issue. Typical examples include resource owner memberships in roles and groups that are relevant to the resource being accessed, entitlements assigned to the resource owner for the targeted resource that the authorization server knows about, and so on.[¶](#section-2.2.3.1-1)

An authorization server wanting to include such attributes in a JWT access token SHOULD use the "groups", "roles", and "entitlements" attributes of the "User" resource schema defined by [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7643#section-4.1.2) of \[\]) as claim types.[¶](#section-2.2.3.1-2)

Authorization servers SHOULD encode the corresponding claim values according to the guidance defined in \[\]. In particular, a non-normative example of a "groups" attribute can be found in [Section 8.2](https://www.rfc-editor.org/rfc/rfc7643#section-8.2) of \[\]. No specific vocabulary is provided for "roles" and "entitlements".[¶](#section-2.2.3.1-3)

of this document provides entries for registering "groups", "roles", and "entitlements" attributes from \[\] as claim types to be used in this profile.[¶](#section-2.2.3.1-4)

## 3.

An authorization server can issue a JWT access token in response to any authorization grant defined by \[\] and subsequent extensions meant to result in an access token.[¶](#section-3-1)

If the request includes a "resource" parameter (as defined in \[\]), the resulting JWT access token "aud" claim SHOULD have the same value as the "resource" parameter in the request.[¶](#section-3-2)

Example request below:[¶](#section-3-3)

```
GET /as/authorization.oauth2?response_type=code
        &client_id=s6BhdRkqt3
        &state=xyz
        &scope=openid%20profile%20reademail
        &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
        &resource=https%3A%2F%2Frs.example.com%2F HTTP/1.1
     Host: authorization-server.example.com
```

:

Once redeemed, the code obtained from the request above will result in a JWT access token in the form shown below:[¶](#section-3-5)

```json
Header:

   {"typ":"at+JWT","alg":"RS256","kid":"RjEwOwOA"}

Claims:

   {
     "iss": "https://authorization-server.example.com/",
     "sub": "5ba552d67",
     "aud":   "https://rs.example.com/",
     "exp": 1639528912,
     "iat": 1618354090,
     "jti" : "dbe39bf3a3ba4238a513f51d6e1691c4",
     "client_id": "s6BhdRkqt3",
     "scope": "openid profile reademail"
   }
```

:

The authorization server MUST NOT issue a JWT access token if the authorization granted by the token would be ambiguous. See for more details about common cases that might lead to ambiguity and strategies an authorization server can enact to prevent them.[¶](#section-3-7)

If the request does not include a "resource" parameter, the authorization server MUST use a default resource indicator in the "aud" claim. If a "scope" parameter is present in the request, the authorization server SHOULD use it to infer the value of the default resource indicator to be used in the "aud" claim. The mechanism through which scopes are associated with default resource indicator values is outside the scope of this specification. If the values in the "scope" parameter refer to different default resource indicator values, the authorization server SHOULD reject the request with "invalid\_scope" as described in [Section 4.1.2.1](https://www.rfc-editor.org/rfc/rfc6749#section-4.1.2.1) of \[\].[¶](#section-3-8)

## 4.

For the purpose of facilitating validation data retrieval, it is RECOMMENDED here that authorization servers sign JWT access tokens with an asymmetric algorithm.[¶](#section-4-1)

Authorization servers SHOULD use \[\] to advertise to resource servers their signing keys via "jwks\_uri" and what "iss" claim value to expect via the "issuer" metadata value. Alternatively, authorization servers implementing [[OpenID Connect]] MAY use the \[\] document for the same purpose. If an authorization server supports both OAuth 2.0 Authorization Server Metadata and [[OpenID Connect]] discovery, the values provided MUST be consistent across the two publication methods.[¶](#section-4-2)

An authorization server MAY elect to use different keys to sign [[OpenID Connect]] ID Tokens and JWT access tokens. This specification does not provide a mechanism for identifying a specific key as the one used to sign JWT access tokens. An authorization server can sign JWT access tokens with any of the keys advertised via authorization server (AS) metadata or [[OpenID Connect]] discovery. See for further guidance on security implications.[¶](#section-4-3)

Resource servers receiving a JWT access token MUST validate it in the following manner.[¶](#section-4-4)

- The resource server MUST verify that the "typ" header value is "at+jwt" or "application/at+jwt" and reject tokens carrying any other value.[¶](#section-4-5.1)
- If the JWT access token is encrypted, decrypt it using the keys and algorithms that the resource server specified during registration. If encryption was negotiated with the authorization server at registration time and the incoming JWT access token is not encrypted, the resource server SHOULD reject it.[¶](#section-4-5.2)
- The issuer identifier for the authorization server (which is typically obtained during discovery) MUST exactly match the value of the "iss" claim.[¶](#section-4-5.3)
- The resource server MUST validate that the "aud" claim contains a resource indicator value corresponding to an identifier the resource server expects for itself. The JWT access token MUST be rejected if "aud" does not contain a resource indicator of the current resource server as a valid audience.[¶](#section-4-5.4)
- The resource server MUST validate the signature of all incoming JWT access tokens according to \[\] using the algorithm specified in the JWT "alg" Header Parameter. The resource server MUST reject any JWT in which the value of "alg" is "none". The resource server MUST use the keys provided by the authorization server.[¶](#section-4-5.5)
- The current time MUST be before the time represented by the "exp" claim. Implementers MAY provide for some small leeway, usually no more than a few minutes, to account for clock skew.[¶](#section-4-5.6)

The resource server MUST handle errors as described in [Section 3.1](https://www.rfc-editor.org/rfc/rfc6750#section-3.1) of \[\]. In particular, in case of any failure in the validation checks listed above, the authorization server response MUST include the error code "invalid\_token". Please note that this requirement does not prevent JWT access tokens from using authentication schemes other than "Bearer".[¶](#section-4-6)

If the JWT access token includes authorization claims as described in, the resource server SHOULD use them in combination with any other contextual information available to determine whether the current call should be authorized or rejected. Details about how a resource server performs those checks is beyond the scope of this profile specification.[¶](#section-4-7)

## 5.

The JWT access token data layout described here is very similar to that of the id\_token as defined by \[\]. The explicit typing required in this profile, in line with the recommendations in \[\], helps the resource server to distinguish between JWT access tokens and [[OpenID Connect]] ID Tokens.[¶](#section-5-1)

Authorization servers should prevent scenarios where clients can affect the value of the "sub" claim in ways that could confuse resource servers. For example, if the authorization server elects to use the client\_id as the "sub" value for access tokens issued using the client credentials grant, the authorization server should prevent clients from registering an arbitrary client\_id value, as this would allow malicious clients to select the sub of a high-privilege resource owner and confuse any authorization logic on the resource server relying on the "sub" value. For more details, please refer to [Section 4.14](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-18#section-4.14) of \[\].[¶](#section-5-2)

To prevent cross-JWT confusion, authorization servers MUST use a distinct identifier as an "aud" claim value to uniquely identify access tokens issued by the same issuer for distinct resources. For more details on cross-JWT confusion, please refer to [Section 2.8](https://www.rfc-editor.org/rfc/rfc8725#section-2.8) of \[\].[¶](#section-5-3)

Authorization servers should use particular care when handling requests that might lead to ambiguous authorization grants. For example, if a request includes multiple resource indicators, the authorization server should ensure that each scope string included in the resulting JWT access token, if any, can be unambiguously correlated to a specific resource among the ones listed in the "aud" claim. The details on how to recognize and mitigate this and other ambiguous situations is highly scenario dependent and hence is out of scope for this profile.[¶](#section-5-4)

Authorization servers cannot rely on the use of different keys for signing [[OpenID Connect]] ID Tokens and JWT tokens as a method to safeguard against the consequences of leaking specific keys. Given that resource servers have no way of knowing what key should be used to validate JWT access tokens in particular, they have to accept signatures performed with any of the keys published in AS metadata or [[OpenID Connect]] discovery; consequently, an attacker just needs to compromise any key among the ones published to be able to generate and sign JWTs that will be accepted as valid by the resource server.[¶](#section-5-5)

## 6.

As JWT access tokens carry information by value, it now becomes possible for clients and potentially even end users to directly peek inside the token claims collection of unencrypted tokens.[¶](#section-6-1)

The client MUST NOT inspect the content of the access token: the authorization server and the resource server might decide to change the token format at any time (for example, by switching from this profile to opaque tokens); hence, any logic in the client relying on the ability to read the access token content would break without recourse. The OAuth 2.0 framework assumes that access tokens are treated as opaque by clients. Administrators of authorization servers should also take into account that the content of an access token is visible to the client. Whenever client access to the access token content presents privacy issues for a given scenario, the authorization server needs to take explicit steps to prevent them.[¶](#section-6-2)

In scenarios in which JWT access tokens are accessible to the end user, it should be evaluated whether the information can be accessed without privacy violations (for example, if an end user would simply access his or her own personal information) or if steps must be taken to enforce confidentiality.[¶](#section-6-3)

Possible measures to prevent leakage of information to clients and end users include: encrypting the access token, encrypting the sensitive claims, omitting the sensitive claims or not using this profile, and falling back on opaque access tokens.[¶](#section-6-4)

In every scenario, the content of the JWT access token will eventually be accessible to the resource server. It's important to evaluate whether the resource server gained the proper entitlement to have access to any content received in the form of claims, for example, through user consent in some form, policies and agreements with the organization running the authorization servers, and so on. For example, a user might not wish to consent to granting given resource server information about any of the non-mandatory claims enumerated in (and its subsections).[¶](#section-6-5)

This profile mandates the presence of the "sub" claim in every JWT access token, making it possible for resource servers to rely on that information for correlating incoming requests with data stored locally for the authenticated principal. Although the ability to correlate requests might be required by design in many scenarios, there are scenarios where the authorization server might want to prevent correlation. The "sub" claim should be populated by the authorization servers according to a privacy impact assessment. For instance, if a solution requires preventing tracking of principal activities across multiple resource servers, the authorization server should ensure that JWT access tokens meant for different resource servers have distinct "sub" values that cannot be correlated in the event of resource server collusion. Similarly, if a solution requires preventing a resource server from correlating the principal's activity within the resource itself, the authorization server should assign different "sub" values for every JWT access token issued. In turn, the client should obtain a new JWT access token for every call to the resource server to ensure that the resource server receives different "sub" and "jti" values at every call, thus preventing correlation between distinct requests.[¶](#section-6-6)

## 7.

### 7.1.

#### 7.1.1.

This section registers "application/at+jwt", a new media type \[\] in the "Media Types" registry \[\] in the manner described in \[\]. It can be used to indicate that the content is an access token encoded in JWT format.[¶](#section-7.1.1-1)

Type name:

Application [¶](#section-7.1.1-2.2)

Subtype name:

at+jwt [¶](#section-7.1.1-2.4)

Required parameters:

N/A [¶](#section-7.1.1-2.6)

Optional parameters:

N/A [¶](#section-7.1.1-2.8)

Encoding considerations:

Binary; JWT values are encoded as a series of base64url-encoded values (with trailing '=' characters removed), some of which may be the empty string, separated by period ('.') characters.[¶](#section-7.1.1-2.10)

Security considerations:

See the Security Considerations section of RFC 9068.[¶](#section-7.1.1-2.12)

Interoperability considerations:

N/A [¶](#section-7.1.1-2.14)

Published specification:

RFC 9068 [¶](#section-7.1.1-2.16)

Applications that use this media type:

Applications that access resource servers using OAuth 2.0 access tokens encoded in JWT format [¶](#section-7.1.1-2.18)

Fragment identifier considerations:

N/A [¶](#section-7.1.1-2.20)

Additional information:

Magic number(s):

N/A [¶](#section-7.1.1-2.22.2.2)

File extension(s):

N/A [¶](#section-7.1.1-2.22.2.4)

Macintosh file type code(s):

N/A [¶](#section-7.1.1-2.22.2.6)

Person & email address to contact for further information:

Vittorio Bertocci <vittorio@auth0.com> [¶](#section-7.1.1-2.24.1)

Intended usage:

COMMON [¶](#section-7.1.1-2.26)

Restrictions on usage:

None [¶](#section-7.1.1-2.28)

Author:

Vittorio Bertocci <vittorio@auth0.com> [¶](#section-7.1.1-2.30)

Change controller:

IETF [¶](#section-7.1.1-2.32)

Provisional registration?

No [¶](#section-7.1.1-2.34)

### 7.2.

of this specification refers to the attributes "roles", "groups", "entitlements" defined in \[\] to express authorization information in JWT access tokens. This section registers those attributes as claims in the "JSON Web Token (JWT)" IANA registry introduced in \[\].[¶](#section-7.2-1)

#### 7.2.1.

##### 7.2.1.1.

Claim Name:

roles [¶](#section-7.2.1.1-1.2)

Claim Description:

Roles [¶](#section-7.2.1.1-1.4)

Change Controller:

IETF [¶](#section-7.2.1.1-1.6)

Specification Document(s):

[Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7643#section-4.1.2) of \[\] and of RFC 9068 [¶](#section-7.2.1.1-1.8)

##### 7.2.1.2.

Claim Name:

groups [¶](#section-7.2.1.2-1.2)

Claim Description:

Groups [¶](#section-7.2.1.2-1.4)

Change Controller:

IETF [¶](#section-7.2.1.2-1.6)

Specification Document(s):

[Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7643#section-4.1.2) of \[\] and of RFC 9068 [¶](#section-7.2.1.2-1.8)

##### 7.2.1.3.

Claim Name:

entitlements [¶](#section-7.2.1.3-1.2)

Claim Description:

Entitlements [¶](#section-7.2.1.3-1.4)

Change Controller:

IETF [¶](#section-7.2.1.3-1.6)

Specification Document(s):

[Section 4.1.2](https://www.rfc-editor.org/rfc/rfc7643#section-4.1.2) of \[\] and of RFC 9068 [¶](#section-7.2.1.3-1.8)

## 8.

### 8.1.

\[OpenID.Core\]

Sakimura, N., Bradley, J., Jones, M., de Medeiros, B., and C. Mortimore, "[[OpenID Connect]] Core 1.0 incorporating errata set 1", November [[2014]], < [https://openid.net/specs/openid-connect-core-1\_0.html](https://openid.net/specs/openid-connect-core-1_0.html) >.

\[OpenID.Discovery\]

Sakimura, N., Bradley, J., Jones, M., and E. Jay, "[[OpenID Connect]] Discovery 1.0 incorporating errata set 1", November [[2014]], < [https://openid.net/specs/openid-connect-discovery-1\_0.html](https://openid.net/specs/openid-connect-discovery-1_0.html) >.

\[RFC2046\]

Freed, N. and N. Borenstein, "Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types", RFC 2046, DOI 10.17487/RFC2046, November 1996, < [https://www.rfc-editor.org/info/rfc2046](https://www.rfc-editor.org/info/rfc2046) >.

\[RFC2119\]

Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, < [https://www.rfc-editor.org/info/rfc2119](https://www.rfc-editor.org/info/rfc2119) >.

\[RFC6749\]

Hardt, D., Ed., "The OAuth 2.0 Authorization Framework", RFC 6749, DOI 10.17487/RFC6749, October 2012, < [https://www.rfc-editor.org/info/rfc6749](https://www.rfc-editor.org/info/rfc6749) >.

\[RFC6838\]

Freed, N., Klensin, J., and T. Hansen, "Media Type Specifications and Registration Procedures", BCP 13, RFC 6838, DOI 10.17487/RFC6838, January 2013, < [https://www.rfc-editor.org/info/rfc6838](https://www.rfc-editor.org/info/rfc6838) >.

\[RFC[[7515]]\]

Jones, M., Bradley, J., and N. Sakimura, "JSON Web Signature (JWS)", RFC [[7515]], DOI 10.17487/RFC[[7515]], May 2015, < [https://www.rfc-editor.org/info/rfc7515](https://www.rfc-editor.org/info/rfc7515) >.

\[RFC[[7518]]\]

Jones, M., "JSON Web Algorithms (JWA)", RFC [[7518]], DOI 10.17487/RFC[[7518]], May 2015, < [https://www.rfc-editor.org/info/rfc7518](https://www.rfc-editor.org/info/rfc7518) >.

\[RFC[[7519]]\]

Jones, M., Bradley, J., and N. Sakimura, "JSON Web Token (JWT)", RFC [[7519]], DOI 10.17487/RFC[[7519]], May 2015, < [https://www.rfc-editor.org/info/rfc7519](https://www.rfc-editor.org/info/rfc7519) >.

\[RFC7643\]

Hunt, P., Ed., Grizzle, K., Wahlstroem, E., and C. Mortimore, "System for Cross-domain Identity Management: Core Schema", RFC 7643, DOI 10.17487/RFC7643, September 2015, < [https://www.rfc-editor.org/info/rfc7643](https://www.rfc-editor.org/info/rfc7643) >.

\[RFC8174\]

Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, < [https://www.rfc-editor.org/info/rfc8174](https://www.rfc-editor.org/info/rfc8174) >.

\[RFC[[8414]]\]

Jones, M., Sakimura, N., and J. Bradley, [["OAuth 2.0]] Authorization Server Metadata", RFC [[8414]], DOI 10.17487/RFC[[8414]], June 2018, < [https://www.rfc-editor.org/info/rfc8414](https://www.rfc-editor.org/info/rfc8414) >.

\[RFC[[8693]]\]

Jones, M., Nadalin, A., Campbell, B., Ed., Bradley, J., and C. Mortimore, [["OAuth 2.0]] [[Token Exchange]]", RFC [[8693]], DOI 10.17487/RFC[[8693]], January 2020, < [https://www.rfc-editor.org/info/rfc8693](https://www.rfc-editor.org/info/rfc8693) >.

\[RFC[[8707]]\]

Campbell, B., Bradley, J., and H. Tschofenig, "[[Resource Indicators]] for OAuth 2.0", RFC [[8707]], DOI 10.17487/RFC[[8707]], February 2020, < [https://www.rfc-editor.org/info/rfc8707](https://www.rfc-editor.org/info/rfc8707) >.

\[RFC8725\]

Sheffer, Y., Hardt, D., and M. Jones, "JSON Web Token Best Current Practices", BCP 225, RFC 8725, DOI 10.17487/RFC8725, February 2020, < [https://www.rfc-editor.org/info/rfc8725](https://www.rfc-editor.org/info/rfc8725) >.

### 8.2.

\[IANA.MediaTypes\]

IANA, "Media Types", < [https://www.iana.org/assignments/media-types/](https://www.iana.org/assignments/media-types/) >.

\[[[OAuth2]].Security.BestPractices\]

Lodderstedt, T., Bradley, J., Labunets, A., and D. Fett, [["OAuth 2.0]] Security Best Current Practice", Work in Progress, Internet-Draft, draft-ietf-oauth-security-topics-18, 13 April 2021, < [https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-18](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-18) >.

\[RFC[[6750]]\]

Jones, M. and D. Hardt, "The OAuth 2.0 Authorization Framework: [[Bearer Token]] Usage", RFC [[6750]], DOI 10.17487/RFC[[6750]], October 2012, < [https://www.rfc-editor.org/info/rfc6750](https://www.rfc-editor.org/info/rfc6750) >.

\[RFC[[7523]]\]

Jones, M., Campbell, B., and C. Mortimore, "JSON Web Token (JWT) [[Profile]] for OAuth 2.0 Client Authentication and Authorization Grants", RFC [[7523]], DOI 10.17487/RFC[[7523]], May 2015, < [https://www.rfc-editor.org/info/rfc7523](https://www.rfc-editor.org/info/rfc7523) >.

\[RFC[[7662]]\]

Richer, J., Ed., [["OAuth 2.0]] [[Token Introspection]]", RFC [[7662]], DOI 10.17487/RFC[[7662]], October 2015, < [https://www.rfc-editor.org/info/rfc7662](https://www.rfc-editor.org/info/rfc7662) >.

## Acknowledgements

The initial set of requirements informing this specification was extracted by numerous examples of access tokens issued in JWT format by production systems. Thanks to (IdentityServer), (Ping Identity), (Microsoft), and (Okta) for providing sample tokens issued by their products and services. and provided early feedback that shaped the direction of the specification. This profile was discussed at length during the OAuth Security Workshop 2019, with several individuals contributing ideas and feedback. The author would like to acknowledge the contributions of:[¶](#appendix-A-1)

,,,,,, and everyone who actively participated in the unconference discussions.[¶](#appendix-A-2)

The following individuals contributed useful feedback and insights on the drafts, both at the IETF OAuth 2.0 WG mailing list and during the 28th Internet Identity Workshop (IIW 28):[¶](#appendix-A-3)

,,,,,,,,,,,,,,,, and everyone who actively participated in the IIW 28 unconference discussions and the IETF OAuth 2.0 WG mailing list discussions. Thanks to for the AD review; and for the SECDIR and GENART reviews; and,,,,, for the IESG reviews.[¶](#appendix-A-4)

## Author's Address

Vittorio Bertocci

Auth0

Email: [vittorio@auth0.com](mailto:vittorio@auth0.com)
## 相关笔记

- [[RFC 9449 DPoP]]
- [[RFC 8693 Token Exchange]]
- [[RFC 9101 JAR]]
- [[RFC 8705 mTLS]]
- [[RFC 9700 Security BCP]]
- [[RFC 9126 PAR]]
- [[RFC 8707 Resource Indicators]]
- [[RFC 9207 Issuer ID]]
