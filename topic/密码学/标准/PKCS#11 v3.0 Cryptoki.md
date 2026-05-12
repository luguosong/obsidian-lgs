![](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os_files/image001.jpg)

PKCS #11 Cryptographic Token Interface Base Specification Version 3.0

OASIS Standard

15 June 2020

This stage:

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.docx](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.docx) (Authoritative)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.html](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.html)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.pdf](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.pdf)

Previous stage:

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.docx](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.docx) (Authoritative)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.html](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.html)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.pdf](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/cs01/pkcs11-base-v3.0-cs01.pdf)

Latest stage:

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.docx](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.docx) (Authoritative)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html)

[https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.pdf](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.pdf)

Technical Committee:

[OASIS PKCS 11 TC](https://www.oasis-open.org/committees/pkcs11/)

Chairs:

Tony Cox ([\[email protected\]](https://docs.oasis-open.org/cdn-cgi/l/email-protection#d4a0bbbaadfab7bbac94b7a6ada4a0a7bbb2a0fab7bbb9)), [Cryptsoft Pty Ltd](https://cryptsoft.com/)

Robert Relyea ([\[email protected\]](https://docs.oasis-open.org/cdn-cgi/l/email-protection#2a58584f46534f4b6a584f4e424b5e04494547)), [Red Hat](http://www.redhat.com/)

Editors:

Chris Zimman ([\[email protected\]](https://docs.oasis-open.org/cdn-cgi/l/email-protection#7b18130912083b0c160b0b55181416)), Individual

Dieter Bong ([\[email protected\]](https://docs.oasis-open.org/cdn-cgi/l/email-protection#b5d1dcd0c1d0c79bd7dadbd2f5c0c1dcd8d4d6da9bd6dad8)), [Utimaco IS GmbH](https://hsm.utimaco.com/)

Additional artifacts:

This prose specification is one component of a Work Product that also includes:

Related work:

This specification replaces or supersedes:

This specification is related to:

Abstract:

This document defines data types, functions and other basic components of the PKCS #11 Cryptoki interface.

Status:

This document was last revised or approved by the membership of OASIS on the above date. The level of approval is also listed above. Check the "Latest stage" location noted above for possible later revisions of this document. Any other numbered Versions and other technical work produced by the Technical Committee (TC) are listed at [https://www.oasis-open.org/committees/tc\_home.php?wg\_abbrev=pkcs11#technical](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=pkcs11#technical).

TC members should send comments on this document to the TC's email list. Others should send comments to the TC's public comment list, after subscribing to it by following the instructions at the " [Send A Comment](https://www.oasis-open.org/committees/comments/index.php?wg_abbrev=pkcs11) " button on the TC's web page at [https://www.oasis-open.org/committees/pkcs11/](https://www.oasis-open.org/committees/pkcs11/).

This specification is provided under the [RF on RAND Terms](https://www.oasis-open.org/policies-guidelines/ipr#RF-on-RAND-Mode) Mode of the [OASIS IPR Policy](https://www.oasis-open.org/policies-guidelines/ipr), the mode chosen when the Technical Committee was established. For information on whether any patents have been disclosed that may be essential to implementing this specification, and any offers of patent licensing terms, please refer to the Intellectual Property Rights section of the TC's web page ([https://www.oasis-open.org/committees/pkcs11/ipr.php](https://www.oasis-open.org/committees/pkcs11/ipr.php)).

Note that any machine-readable content ([Computer Language Definitions](https://www.oasis-open.org/policies-guidelines/tc-process#wpComponentsCompLang)) declared Normative for this Work Product is provided in separate plain text files. In the event of a discrepancy between any such plain text file and display content in the Work Product's prose narrative document(s), the content in the separate plain text file prevails.

Citation format:

When referencing this specification the following citation format should be used:

\[PKCS11-Base-v3.0\]

*PKCS #11 Cryptographic Token Interface Base Specification Version 3.0*. Edited by Chris Zimman and Dieter Bong. 15 June 2020. OASIS Standard. [https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.html](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os.html). Latest stage: [https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/pkcs11-base-v3.0.html).

Notices

Copyright © OASIS Open 2020. All Rights Reserved.

All capitalized terms in the following text have the meanings assigned to them in the OASIS Intellectual Property Rights Policy (the "OASIS IPR Policy"). The full [Policy](https://www.oasis-open.org/policies-guidelines/ipr) may be found at the OASIS website.

This document and translations of it may be copied and furnished to others, and derivative works that comment on or otherwise explain it or assist in its implementation may be prepared, copied, published, and distributed, in whole or in part, without restriction of any kind, provided that the above copyright notice and this section are included on all such copies and derivative works. However, this document itself may not be modified in any way, including by removing the copyright notice or references to OASIS, except as needed for the purpose of developing any document or deliverable produced by an OASIS Technical Committee (in which case the rules applicable to copyrights, as set forth in the OASIS IPR Policy, must be followed) or as required to translate it into languages other than English.

The limited permissions granted above are perpetual and will not be revoked by OASIS or its successors or assigns.

This document and the information contained herein is provided on an "AS IS" basis and OASIS DISCLAIMS ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION HEREIN WILL NOT INFRINGE ANY OWNERSHIP RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.

OASIS requests that any OASIS Party or any other party that believes it has patent claims that would necessarily be infringed by implementations of this OASIS Committee Specification or OASIS Standard, to notify OASIS TC Administrator and provide an indication of its willingness to grant patent licenses to such patent claims in a manner consistent with the IPR Mode of the OASIS Technical Committee that produced this specification.

OASIS invites any party to contact the OASIS TC Administrator if it is aware of a claim of ownership of any patent claims that would necessarily be infringed by implementations of this specification by a patent holder that is not willing to provide a license to such patent claims in a manner consistent with the IPR Mode of the OASIS Technical Committee that produced this specification. OASIS may include such claims on its website, but disclaims any obligation to do so.

OASIS takes no position regarding the validity or scope of any intellectual property or other rights that might be claimed to pertain to the implementation or use of the technology described in this document or the extent to which any license under such rights might or might not be available; neither does it represent that it has made any effort to identify any such rights. Information on OASIS' procedures with respect to rights in any document or deliverable produced by an OASIS Technical Committee can be found on the OASIS website. Copies of claims of rights made available for publication and any assurances of licenses to be made available, or the result of an attempt made to obtain a general license or permission for the use of such proprietary rights by implementers or users of this OASIS Committee Specification or OASIS Standard, can be obtained from the OASIS TC Administrator. OASIS makes no representation that any information or list of intellectual property rights will at any time be complete, or that any claims in such list are, in fact, Essential Claims.

The name "OASIS" is a trademark of [OASIS](https://www.oasis-open.org/), the owner and developer of this specification, and should be used only to refer to the organization and its official outputs. OASIS welcomes reference to, and implementation and use of, specifications, while reserving the right to enforce its marks against misleading uses. Please see [https://www.oasis-open.org/policies-guidelines/trademark](https://www.oasis-open.org/policies-guidelines/trademark) for above guidance.

Table of Contents

[1 Introduction](#_Toc29976530)

[1.1 IPR Policy](#_Toc29976531)

[1.2 Terminology](#_Toc29976532)

[1.3 Definitions](#_Toc29976533)

[1.4 Symbols and abbreviations](#_Toc29976534)

[1.5 Normative References](#_Toc29976535)

[1.6 Non-Normative References](#_Toc29976536)

[2 Platform- and compiler-dependent directives for C or C++](#_Toc29976537)

[2.1 Structure packing](#_Toc29976538)

[2.2 Pointer-related macros](#_Toc29976539)

[3 General data types](#_Toc29976540)

[3.1 General information](#_Toc29976541)

[3.2 Slot and token types](#_Toc29976542)

[3.3 Session types](#_Toc29976543)

[3.4 Object types](#_Toc29976544)

[3.5 Data types for mechanisms](#_Toc29976545)

[3.6 Function types](#_Toc29976546)

[3.7 Locking-related types](#_Toc29976547)

[4 Objects](#_Toc29976548)

[4.1 Creating, modifying, and copying objects](#_Toc29976549)

[4.1.1 Creating objects](#_Toc29976550)

[4.1.2 Modifying objects](#_Toc29976551)

[4.1.3 Copying objects](#_Toc29976552)

[4.2 Common attributes](#_Toc29976553)

[4.3 Hardware Feature Objects](#_Toc29976554)

[4.3.1 Definitions](#_Toc29976555)

[4.3.2 Overview](#_Toc29976556)

[4.3.3 Clock](#_Toc29976557)

[4.3.3.1 Definition](#_Toc29976558)

[4.3.3.2 Description](#_Toc29976559)

[4.3.4 Monotonic Counter Objects](#_Toc29976560)

[4.3.4.1 Definition](#_Toc29976561)

[4.3.4.2 Description](#_Toc29976562)

[4.3.5 User Interface Objects](#_Toc29976563)

[4.3.5.1 Definition](#_Toc29976564)

[4.3.5.2 Description](#_Toc29976565)

[4.4 Storage Objects](#_Toc29976566)

[4.4.1 The CKA\_UNIQUE\_ID attribute](#_Toc29976567)

[4.5 Data objects](#_Toc29976568)

[4.5.1 Definitions](#_Toc29976569)

[4.5.2 Overview](#_Toc29976570)

[4.6 Certificate objects](#_Toc29976571)

[4.6.1 Definitions](#_Toc29976572)

[4.6.2 Overview](#_Toc29976573)

[4.6.3 X.509 public key certificate objects](#_Toc29976574)

[4.6.4 WTLS public key certificate objects](#_Toc29976575)

[4.6.5 X.509 attribute certificate objects](#_Toc29976576)

[4.7 Key objects](#_Toc29976577)

[4.7.1 Definitions](#_Toc29976578)

[4.7.2 Overview](#_Toc29976579)

[4.8 Public key objects](#_Toc29976580)

[4.9 Private key objects](#_Toc29976581)

[4.9.1 RSA private key objects](#_Toc29976582)

[4.10 Secret key objects](#_Toc29976583)

[4.11 Domain parameter objects](#_Toc29976584)

[4.11.1 Definitions](#_Toc29976585)

[4.11.2 Overview](#_Toc29976586)

[4.12 Mechanism objects](#_Toc29976587)

[4.12.1 Definitions](#_Toc29976588)

[4.12.2 Overview](#_Toc29976589)

[4.13 Profile objects](#_Toc29976590)

[4.13.1 Definitions](#_Toc29976591)

[4.13.2 Overview](#_Toc29976592)

[5 Functions](#_Toc29976593)

[5.1 Function return values](#_Toc29976594)

[5.1.1 Universal Cryptoki function return values](#_Toc29976595)

[5.1.2 Cryptoki function return values for functions that use a session handle](#_Toc29976596)

[5.1.3 Cryptoki function return values for functions that use a token](#_Toc29976597)

[5.1.4 Special return value for application-supplied callbacks](#_Toc29976598)

[5.1.5 Special return values for mutex-handling functions](#_Toc29976599)

[5.1.6 All other Cryptoki function return values](#_Toc29976600)

[5.1.7 More on relative priorities of Cryptoki errors](#_Toc29976601)

[5.1.8 Error code “gotchas”](#_Toc29976602)

[5.2 Conventions for functions returning output in a variable-length buffer](#_Toc29976603)

[5.3 Disclaimer concerning sample code](#_Toc29976604)

[5.4 General-purpose functions](#_Toc29976605)

[5.4.1 C\_Initialize](#_Toc29976606)

[5.4.2 C\_Finalize](#_Toc29976607)

[5.4.3 C\_GetInfo](#_Toc29976608)

[5.4.4 C\_GetFunctionList](#_Toc29976609)

[5.4.5 C\_GetInterfaceList](#_Toc29976610)

[5.4.6 C\_GetInterface](#_Toc29976611)

[5.5 Slot and token management functions](#_Toc29976612)

[5.5.1 C\_GetSlotList](#_Toc29976613)

[5.5.2 C\_GetSlotInfo](#_Toc29976614)

[5.5.3 C\_GetTokenInfo](#_Toc29976615)

[5.5.4 C\_WaitForSlotEvent](#_Toc29976616)

[5.5.5 C\_GetMechanismList](#_Toc29976617)

[5.5.6 C\_GetMechanismInfo](#_Toc29976618)

[5.5.7 C\_InitToken](#_Toc29976619)

[5.5.8 C\_InitPIN](#_Toc29976620)

[5.5.9 C\_SetPIN](#_Toc29976621)

[5.6 Session management functions](#_Toc29976622)

[5.6.1 C\_OpenSession](#_Toc29976623)

[5.6.2 C\_CloseSession](#_Toc29976624)

[5.6.3 C\_CloseAllSessions](#_Toc29976625)

[5.6.4 C\_GetSessionInfo](#_Toc29976626)

[5.6.5 C\_SessionCancel](#_Toc29976627)

[5.6.6 C\_GetOperationState](#_Toc29976628)

[5.6.7 C\_SetOperationState](#_Toc29976629)

[5.6.8 C\_Login](#_Toc29976630)

[5.6.9 C\_LoginUser](#_Toc29976631)

[5.6.10 C\_Logout](#_Toc29976632)

[5.7 Object management functions](#_Toc29976633)

[5.7.1 C\_CreateObject](#_Toc29976634)

[5.7.2 C\_CopyObject](#_Toc29976635)

[5.7.3 C\_DestroyObject](#_Toc29976636)

[5.7.4 C\_GetObjectSize](#_Toc29976637)

[5.7.5 C\_GetAttributeValue](#_Toc29976638)

[5.7.6 C\_SetAttributeValue](#_Toc29976639)

[5.7.7 C\_FindObjectsInit](#_Toc29976640)

[5.7.8 C\_FindObjects](#_Toc29976641)

[5.7.9 C\_FindObjectsFinal](#_Toc29976642)

[5.8 Encryption functions](#_Toc29976643)

[5.8.1 C\_EncryptInit](#_Toc29976644)

[5.8.2 C\_Encrypt](#_Toc29976645)

[5.8.3 C\_EncryptUpdate](#_Toc29976646)

[5.8.4 C\_EncryptFinal](#_Toc29976647)

[5.9 Message-based encryption functions](#_Toc29976648)

[5.9.1 C\_MessageEncryptInit](#_Toc29976649)

[5.9.2 C\_EncryptMessage](#_Toc29976650)

[5.9.3 C\_EncryptMessageBegin](#_Toc29976651)

[5.9.4 C\_EncryptMessageNext](#_Toc29976652)

[5.9.5 C\_ MessageEncryptFinal](#_Toc29976653)

[5.10 Decryption functions](#_Toc29976654)

[5.10.1 C\_DecryptInit](#_Toc29976655)

[5.10.2 C\_Decrypt](#_Toc29976656)

[5.10.3 C\_DecryptUpdate](#_Toc29976657)

[5.10.4 C\_DecryptFinal](#_Toc29976658)

[5.11 Message-based decryption functions](#_Toc29976659)

[5.11.1 C\_MessageDecryptInit](#_Toc29976660)

[5.11.2 C\_DecryptMessage](#_Toc29976661)

[5.11.3 C\_DecryptMessageBegin](#_Toc29976662)

[5.11.4 C\_DecryptMessageNext](#_Toc29976663)

[5.11.5 C\_MessageDecryptFinal](#_Toc29976664)

[5.12 Message digesting functions](#_Toc29976665)

[5.12.1 C\_DigestInit](#_Toc29976666)

[5.12.2 C\_Digest](#_Toc29976667)

[5.12.3 C\_DigestUpdate](#_Toc29976668)

[5.12.4 C\_DigestKey](#_Toc29976669)

[5.12.5 C\_DigestFinal](#_Toc29976670)

[5.13 Signing and MACing functions](#_Toc29976671)

[5.13.1 C\_SignInit](#_Toc29976672)

[5.13.2 C\_Sign](#_Toc29976673)

[5.13.3 C\_SignUpdate](#_Toc29976674)

[5.13.4 C\_SignFinal](#_Toc29976675)

[5.13.5 C\_SignRecoverInit](#_Toc29976676)

[5.13.6 C\_SignRecover](#_Toc29976677)

[5.14 Message-based signing and MACing functions](#_Toc29976678)

[5.14.1 C\_MessageSignInit](#_Toc29976679)

[5.14.2 C\_SignMessage](#_Toc29976680)

[5.14.3 C\_SignMessageBegin](#_Toc29976681)

[5.14.4 C\_SignMessageNext](#_Toc29976682)

[5.14.5 C\_MessageSignFinal](#_Toc29976683)

[5.15 Functions for verifying signatures and MACs](#_Toc29976684)

[5.15.1 C\_VerifyInit](#_Toc29976685)

[5.15.2 C\_Verify](#_Toc29976686)

[5.15.3 C\_VerifyUpdate](#_Toc29976687)

[5.15.4 C\_VerifyFinal](#_Toc29976688)

[5.15.5 C\_VerifyRecoverInit](#_Toc29976689)

[5.15.6 C\_VerifyRecover](#_Toc29976690)

[5.16 Message-based functions for verifying signatures and MACs](#_Toc29976691)

[5.16.1 C\_MessageVerifyInit](#_Toc29976692)

[5.16.2 C\_VerifyMessage](#_Toc29976693)

[5.16.3 C\_VerifyMessageBegin](#_Toc29976694)

[5.16.4 C\_VerifyMessageNext](#_Toc29976695)

[5.16.5 C\_MessageVerifyFinal](#_Toc29976696)

[5.17 Dual-function cryptographic functions](#_Toc29976697)

[5.17.1 C\_DigestEncryptUpdate](#_Toc29976698)

[5.17.2 C\_DecryptDigestUpdate](#_Toc29976699)

[5.17.3 C\_SignEncryptUpdate](#_Toc29976700)

[5.17.4 C\_DecryptVerifyUpdate](#_Toc29976701)

[5.18 Key management functions](#_Toc29976702)

[5.18.1 C\_GenerateKey](#_Toc29976703)

[5.18.2 C\_GenerateKeyPair](#_Toc29976704)

[5.18.3 C\_WrapKey](#_Toc29976705)

[5.18.4 C\_UnwrapKey](#_Toc29976706)

[5.18.5 C\_DeriveKey](#_Toc29976707)

[5.19 Random number generation functions](#_Toc29976708)

[5.19.1 C\_SeedRandom](#_Toc29976709)

[5.19.2 C\_GenerateRandom](#_Toc29976710)

[5.20 Parallel function management functions](#_Toc29976711)

[5.20.1 C\_GetFunctionStatus](#_Toc29976712)

[5.20.2 C\_CancelFunction](#_Toc29976713)

[5.21 Callback functions](#_Toc29976714)

[5.21.1 Surrender callbacks](#_Toc29976715)

[5.21.2 Vendor-defined callbacks](#_Toc29976716)

[6 PKCS #11 Implementation Conformance](#_Toc29976717)

[Appendix A. Acknowledgments](#_Toc29976718)

[Appendix B. Manifest constants](#_Toc29976719)

[Appendix C. Revision History](#_Toc29976720)

## 1 Introduction

This document describes the basic PKCS#11 token interface and token behavior.

The PKCS#11 standard specifies an application programming interface (API), called “Cryptoki,” for devices that hold cryptographic information and perform cryptographic functions. Cryptoki follows a simple object based approach, addressing the goals of technology independence (any kind of device) and resource sharing (multiple applications accessing multiple devices), presenting to applications a common, logical view of the device called a “cryptographic token”.

This document specifies the data types and functions available to an application requiring cryptographic services using the ANSI C programming language. The supplier of a Cryptoki library implementation typically provides these data types and functions via ANSI C header files. Generic ANSI C header files for Cryptoki are available from the PKCS#11 web page. This document and up-to-date errata for Cryptoki will also be available from the same place.

Additional documents may provide a generic, language-independent Cryptoki interface and/or bindings between Cryptoki and other programming languages.

Cryptoki isolates an application from the details of the cryptographic device. The application does not have to change to interface to a different type of device or to run in a different environment; thus, the application is portable. How Cryptoki provides this isolation is beyond the scope of this document, although some conventions for the support of multiple types of device will be addressed here and possibly in a separate document.

Details of cryptographic mechanisms (algorithms) may be found in the associated PKCS#11 Mechanisms documents.

## 1.1 IPR Policy

This specification is provided under the [RF on RAND Terms](https://www.oasis-open.org/policies-guidelines/ipr#RF-on-RAND-Mode) Mode of the [OASIS IPR Policy](https://www.oasis-open.org/policies-guidelines/ipr), the mode chosen when the Technical Committee was established. For information on whether any patents have been disclosed that may be essential to implementing this specification, and any offers of patent licensing terms, please refer to the Intellectual Property Rights section of the TC's web page ([https://www.oasis-open.org/committees/pkcs11/ipr.php](https://www.oasis-open.org/committees/pkcs11/ipr.php)).

## 1.2 Terminology

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in \[RFC2119\].

## 1.3 Definitions

For the purposes of this standard, the following definitions apply:

**API** Application programming interface.

**Application** Any computer program that calls the Cryptoki interface.

**[[ASN.1]]** Abstract Syntax Notation One, as defined in X.680.

**Attribute** A characteristic of an object.

**BER** Basic Encoding Rules, as defined in X.690.

**CBC** Cipher-Block Chaining mode, as defined in FIPS PUB 81.

**Certificate** A signed message binding a subject name and a public key, or a subject name and a set of attributes.

**CMS** Cryptographic Message Syntax (see RFC 5652)

**Cryptographic Device** A device storing cryptographic information and possibly performing cryptographic functions. May be implemented as a smart card, smart disk, PCMCIA card, or with some other technology, including software-only.

**Cryptoki** The Cryptographic Token Interface defined in this standard.

**Cryptoki library** A library that implements the functions specified in this standard.

**DER** Distinguished Encoding Rules, as defined in X.690.

**DES** Data Encryption Standard, as defined in FIPS PUB 46-3.

**DSA** Digital Signature Algorithm, as defined in FIPS PUB 186-4.

**EC** Elliptic Curve

**ECB** Electronic Codebook mode, as defined in FIPS PUB 81.

**IV** Initialization Vector.

**MAC** Message Authentication Code.

**Mechanism** A process for implementing a cryptographic operation.

**Object** An item that is stored on a token. May be data, a certificate, or a key.

**PIN** Personal Identification Number.

**PKCS** Public-Key Cryptography Standards.

**PRF** Pseudo random function.

**PTD** Personal Trusted Device, as defined in MeT-PTD

**RSA** The RSA public-key cryptosystem.

**Reader** The means by which information is exchanged with a device.

**Session** A logical connection between an application and a token.

**Slot** A logical reader that potentially contains a token.

**SSL** The Secure [[Socket]]s Layer 3.0 protocol.

**Subject Name** The X.500 distinguished name of the entity to which a key is assigned.

**SO** A Security Officer user.

**TLS** Transport Layer Security.

**Token** The logical view of a cryptographic device defined by Cryptoki.

**User** The person using an application that interfaces to Cryptoki.

**UTF-8** Universal Character Set (UCS) transformation format (UTF) that represents ISO 10646 and UNICODE strings with a variable number of octets.

**WIM** Wireless Identification Module.

**WTLS** Wireless Transport Layer Security.

## 1.4 Symbols and abbreviations

The following symbols are used in this standard:

Table 1, Symbols

| **Symbol** | **Definition** |
| --- | --- |
| N/A | Not applicable |
| R/O | Read-only |
| R/W | Read/write |

The following prefixes are used in this standard:

Table 2, Prefixes

| **Prefix** | **Description** |
| --- | --- |
| C\_ | Function |
| CK\_ | Data type or general constant |
| CKA\_ | Attribute |
| CKC\_ | Certificate type |
| CKD\_ | Key derivation function |
| CKF\_ | Bit flag |
| CKG\_ | Mask generation function |
| CKH\_ | Hardware feature type |
| CKK\_ | Key type |
| CKM\_ | Mechanism type |
| CKN\_ | Notification |
| CKO\_ | Object class |
| CKP\_ | Pseudo-random function |
| CKS\_ | Session state |
| CKR\_ | Return value |
| CKU\_ | User type |
| CKZ\_ | Salt/Encoding parameter source |
| h | a handle |
| ul | a CK\_ULONG |
| p | a pointer |
| pb | a pointer to a CK\_BYTE |
| ph | a pointer to a handle |
| pul | a pointer to a CK\_ULONG |

Cryptoki is based on ANSI C types, and defines the following data types:

/\* an unsigned 8-bit value \*/

typedef unsigned char CK\_BYTE;

/\* an unsigned 8-bit character \*/

typedef CK\_BYTE CK\_CHAR;

/\* an 8-bit UTF-8 character \*/

typedef CK\_BYTE CK\_UTF8CHAR;

/\* a BYTE-sized Boolean flag \*/

typedef CK\_BYTE CK\_BBOOL;

/\* an unsigned value, at least 32 bits long \*/

typedef unsigned long int CK\_ULONG;

/\* a signed value, the same size as a CK\_ULONG \*/

typedef long int CK\_LONG;

/\* at least 32 bits; each bit is a Boolean flag \*/

typedef CK\_ULONG CK\_FLAGS;

Cryptoki also uses pointers to some of these data types, as well as to the type void, which are implementation-dependent. These pointer types are:

CK\_BYTE\_PTR /\* Pointer to a CK\_BYTE \*/

CK\_CHAR\_PTR /\* Pointer to a CK\_CHAR \*/

CK\_UTF8CHAR\_PTR /\* Pointer to a CK\_UTF8CHAR \*/

CK\_ULONG\_PTR /\* Pointer to a CK\_ULONG \*/

CK\_VOID\_PTR /\* Pointer to a void \*/

Cryptoki also defines a pointer to a CK\_VOID\_PTR, which is implementation-dependent:

CK\_VOID\_PTR\_PTR /\* Pointer to a CK\_VOID\_PTR \*/

In addition, Cryptoki defines a C-style NULL pointer, which is distinct from any valid pointer:

NULL\_PTR /\* A NULL pointer \*/

It follows that many of the data and pointer types will vary somewhat from one environment to another (*e.g.*, a CK\_ULONG will sometimes be 32 bits, and sometimes perhaps 64 bits). However, these details should not affect an application, assuming it is compiled with Cryptoki header files consistent with the Cryptoki library to which the application is linked.

All numbers and values expressed in this document are decimal, unless they are preceded by “0x”, in which case they are hexadecimal values.

The **CK\_CHAR** data type holds characters from the following table, taken from ANSI C:

Table 3, Character Set

| **Category** | **Characters** |
| --- | --- |
| Letters | A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z |
| Numbers | 0 1 2 3 4 5 6 7 8 9 |
| Graphic characters | ! “ # % & ‘ ( ) \* +, -. /:; < = >? \[ \\ \] ^ \_ { \| } ~ |
| Blank character | ‘ ‘ |

The **CK\_UTF8CHAR** data type holds UTF-8 encoded Unicode characters as specified in RFC2279. UTF-8 allows internationalization while maintaining backward compatibility with the Local String definition of PKCS #11 version 2.01.

In Cryptoki, the **CK\_BBOOL** data type is a Boolean type that can be true or false. A zero value means false, and a nonzero value means true. Similarly, an individual bit flag, **CKF\_**..., can also be set (true) or unset (false). For convenience, Cryptoki defines the following macros for use with values of type **CK\_BBOOL**:

#define CK\_FALSE 0

#define CK\_TRUE 1

For backwards compatibility, header files for this version of Cryptoki also define TRUE and FALSE as (CK\_DISABLE\_TRUE\_FALSE may be set by the application vendor):

#ifndef CK\_DISABLE\_TRUE\_FALSE

#ifndef FALSE

#define FALSE CK\_FALSE

#endif

#ifndef TRUE

#define TRUE CK\_TRUE

#endif

#endif

## 1.5 Normative References

**\[FIPS PUB 46-3\]** NIST. *FIPS 46-3: Data Encryption Standard.* October 1999.  
URL: [http://csrc.nist.gov/publications/fips/fips46-3/fips46-3.pdf](http://csrc.nist.gov/publications/fips/fips46-3/fips46-3.pdf)

**\[FIPS PUB 81\]** NIST. *FIPS 81: DES Modes of Operation.* December 1980.  
URL: [http://csrc.nist.gov/publications/fips/fips81/fips81.htm](http://csrc.nist.gov/publications/fips/fips81/fips81.htm)

**\[FIPS PUB 186-4\]** NIST. FIPS 186-4: Digital Signature Standard. July, 2013.  
URL: [http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf](http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-4.pdf)

**\[PKCS11-Curr\]** *PKCS #11 Cryptographic Token Interface Current Mechanisms Specification Version 2.40*. Edited by Susan Gleeson and Chris Zimman. 14 April 2015. OASIS Standard. [http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/os/pkcs11-curr-v2.40-os.html](https://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/os/pkcs11-curr-v2.40-os.html). Latest version: [http://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/pkcs11-curr-v2.40.html](https://docs.oasis-open.org/pkcs11/pkcs11-curr/v2.40/pkcs11-curr-v2.40.html).

**\[PKCS11-Hist\]** *PKCS #11 Cryptographic Token Interface Historical Mechanisms Specification Version 2.40*. Edited by Susan Gleeson and Chris Zimman. 14 April 2015. OASIS Standard. [http://docs.oasis-open.org/pkcs11/pkcs11-hist/v2.40/os/pkcs11-hist-v2.40-os.html](https://docs.oasis-open.org/pkcs11/pkcs11-hist/v2.40/os/pkcs11-hist-v2.40-os.html). Latest version: [http://docs.oasis-open.org/pkcs11/pkcs11-hist/v2.40/pkcs11-hist-v2.40.html](https://docs.oasis-open.org/pkcs11/pkcs11-hist/v2.40/pkcs11-hist-v2.40.html).

**\[PKCS11-Prof\]** *PKCS #11 Cryptographic Token Interface [[Profile]]s Version 2.40*. Edited by Tim Hudson. 14 April 2015. OASIS Standard. [http://docs.oasis-open.org/pkcs11/pkcs11-profiles/v2.40/os/pkcs11-profiles-v2.40-os.html](https://docs.oasis-open.org/pkcs11/pkcs11-profiles/v2.40/os/pkcs11-profiles-v2.40-os.html). Latest version: [http://docs.oasis-open.org/pkcs11/pkcs11-profiles/v2.40/pkcs11-profiles-v2.40.html](https://docs.oasis-open.org/pkcs11/pkcs11-profiles/v2.40/pkcs11-profiles-v2.40.html).

**\[PKCS #1\]** RSA Laboratories. *RSA Cryptography Standard.* v2.1, June 14, 2002.  
URL: ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-1/pkcs-1v2-1.pdf

**\[PKCS #3\]** RSA Laboratories. *Diffie-Hellman Key-Agreement Standard.* v1.4, November 1993.  
URL: ftp://ftp.rsasecurity.com/pub/pkcs/doc/pkcs-3.doc

**\[PKCS #5\]** RSA Laboratories. *Password-Based Encryption Standard*. v2.0, March 25, 1999  
URL: ftp://ftp.rsasecurity.com/pub/pkcs/pkcs-5v2/pkcs5v2-0.pdf

**\[PKCS #7\]** RSA Laboratories. *Cryptographic Message Syntax Standard.* v1.5, November 1993  
URL: ftp://ftp.rsasecurity.com/pub/pkcs/doc/pkcs-7.doc

**\[PKCS #8\]** RSA Laboratories. *Private-Key Information Syntax Standard*. v1.2, November 1993.  
URL: ftp://ftp.rsasecurity.com/pub/pkcs/doc/pkcs-8.doc

**\[PKCS11-UG\]** *PKCS #11 Cryptographic Token Interface Usage Guide Version 2.40*. Edited by John Leiseboer and Robert Griffin. 16 November [[2014]]. OASIS Committee Note 02. [http://docs.oasis-open.org/pkcs11/pkcs11-ug/v2.40/cn02/pkcs11-ug-v2.40-cn02.html](https://docs.oasis-open.org/pkcs11/pkcs11-ug/v2.40/cn02/pkcs11-ug-v2.40-cn02.html). Latest version: [http://docs.oasis-open.org/pkcs11/pkcs11-ug/v2.40/pkcs11-ug-v2.40.html](https://docs.oasis-open.org/pkcs11/pkcs11-ug/v2.40/pkcs11-ug-v2.40.html).

**\[PKCS #12\]** RSA Laboratories. *Personal* *Information Exchange Syntax Standard*. v1.0, June 1999.

\[RFC2119\] Bradner, S., “Key words for use in RFCs to Indicate Requirement Levels”, BCP 14, RFC 2119, March 1997.  
URL: [http://www.ietf.org/rfc/rfc2119.txt](http://www.ietf.org/rfc/rfc2119.txt).

**\[RFC 2279\]** F. Yergeau. *RFC 2279:* UTF-8, a transformation format of ISO 10646 Alis Technologies, January 1998.  
URL: [http://www.ietf.org/rfc/rfc2279.txt](http://ietf.org/rfc/rfc2279.txt)

**\[RFC 2534\]** Masinter, L., Wing, D., Mutz, A., and K. Holtman. *RFC 2534: Media Features for Display, Print, and Fax.* March 1999.  
URL: [http://www.ietf.org/rfc/rfc2534.txt](http://ietf.org/rfc/rfc2534.txt)

**\[RFC 5652\]** R. Housley. *RFC 5652: Cryptographic Message Syntax*. Septmber 2009. URL:  
[http://www.ietf.org/rfc/rfc5652.txt](http://www.ietf.org/rfc/rfc5652.txt)

**\[RFC 5707\]** Rescorla, E., “The Keying Material Exporters for Transport Layer Security (TLS)”, RFC 5705, March 2010.  
URL: http://www.ietf.org/rfc/rfc5705.txt

**\[TLS\]** \[RFC2246\] Dierks, T. and C. Allen, "The TLS Protocol Version 1.0", RFC 2246, January 1999. URL: http://www.ietf.org/rfc/rfc2246.txt, superseded by \[RFC4346\] Dierks, T. and E. Rescorla, "The Transport Layer Security (TLS) Protocol Version 1.1", RFC 4346, April 2006. URL: http://www.ietf.org/rfc/rfc4346.txt, which was superseded by \[TLS12\].

**\[TLS12\]** \[RFC[[5246]]\] Dierks, T. and E. Rescorla, "The Transport Layer Security (TLS) Protocol Version 1.2", RFC [[5246]], August 2008.  
URL: http://www.ietf.org/rfc/rfc5246.txt

**\[X.500\]** ITU-T. Information Technology — Open Systems Interconnection — The Directory: Overview of Concepts, Models and Services. February 2001. Identical to ISO/IEC 9594-1

**\[X.509\]** ITU-T. Information Technology — Open Systems Interconnection — The Directory: Public-key and Attribute Certificate Frameworks. March 2000. Identical to ISO/IEC 9594-8

**\[X.680\]** ITU-T. Information Technology — Abstract Syntax Notation One ([[ASN.1]]): Specification of Basic Notation. July 2002. Identical to ISO/IEC 8824-1

**\[X.690\]** ITU-T. Information Technology — [[ASN.1]] Encoding Rules: Specification of Basic Encoding Rules (BER), Canonical Encoding Rules (CER), and Distinguished Encoding Rules (DER). July 2002. Identical to ISO/IEC 8825-1

## 1.6 Non-Normative References

**\[ANSI C\]** ANSI/ISO. American National Standard for Programming Languages – C. 1990.

**\[CC/PP\]** W3C. Composite Capability/Preference [[Profile]]s (CC/PP): Structure and Vocabularies. World Wide Web Consortium, January 2004.  
URL: [http://www.w3.org/TR/CCPP-struct-vocab/](http://www.w3.org/TR/CCPP-struct-vocab/)

**\[CDPD**\] Ameritech Mobile Communications et al. Cellular Digital Packet Data System Specifications: Part 406: Airlink Security. 1993.

**\[GCS-API\]** X/Open Company Ltd. Generic Cryptographic Service API (GCS-API), Base - Draft 2. February 14, 1995.

**\[ISO/IEC 7816-1\]** ISO. Information Technology — Identification Cards — Integrated Circuit(s) with Contacts — Part 1: Physical Characteristics. 1998.

**\[ISO/IEC 7816-4\]** ISO. Information Technology — Identification Cards — Integrated Circuit(s) with Contacts — Part 4: Interindustry Commands for Interchange. 1995.

**\[ISO/IEC 8824-1\]** ISO. Information Technology-- Abstract Syntax Notation One ([[ASN.1]]): Specification of Basic Notation. 2002.

**\[ISO/IEC 8825-1\]** ISO. Information Technology—[[ASN.1]] Encoding Rules: Specification of Basic Encoding Rules (BER), Canonical Encoding Rules (CER), and Distinguished Encoding Rules (DER). 2002.

**\[ISO/IEC 9594-1\]** ISO. Information Technology — Open Systems Interconnection — The Directory: Overview of Concepts, Models and Services. 2001.

**\[ISO/IEC 9594-8\]** ISO. Information Technology — Open Systems Interconnection — The Directory: Public-key and Attribute Certificate Frameworks. 2001

**\[ISO/IEC 9796-2\]** ISO. Information Technology — Security Techniques — Digital Signature Scheme Giving Message Recovery — Part 2: Integer factorization based mechanisms. 2002.

**\[Java MIDP\]** Java Community Process. Mobile Information Device [[Profile]] for Java 2 Micro Edition. November 2002.  
URL: [http://jcp.org/jsr/detail/118.jsp](http://jcp.org/jsr/detail/118.jsp)

**\[MeT-PTD\]** MeT. MeT PTD Definition – Personal Trusted Device Definition, Version 1.0, February 2003.  
URL: [http://www.mobiletransaction.org](http://www.mobiletransaction.org/)

**\[PCMCIA\]** Personal Computer Memory Card International Association. *PC Card Standard,* Release 2.1,. July 1993.

**\[SEC 1\]** Standards for Efficient Cryptography Group (SECG). *Standards for Efficient Cryptography (SEC) 1: Elliptic Curve Cryptography*. Version 1.0, September 20, 2000.

**\[SEC 2\]** Standards for Efficient Cryptography Group (SECG). Standards for Efficient Cryptography (SEC) 2: Recommended Elliptic Curve Domain Parameters. Version 1.0, September 20, 2000.

**\[WIM\]** WAP. Wireless Identity Module. — WAP-260-WIM-20010712-a. July 2001.  
URL: [http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-260-wim-20010712-a.pdf](http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-260-wim-20010712-a.pdf)

**\[WPKI\]** Wireless Application Protocol: Public Key Infrastructure Definition*.* *— WAP-217-WPKI-20010424-a*. April 2001.  
URL: [http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-217-wpki-20010424-a.pdf](http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-217-wpki-20010424-a.pdf)

**\[WTLS\]** WAP. Wireless Transport Layer Security Version — WAP-261-WTLS-20010406-a. April 2001.  
URL: [http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-261-wtls-20010406-a.pdf](http://technical.openmobilealliance.org/tech/affiliates/LicenseAgreement.asp?DocName=/wap/wap-261-wtls-20010406-a.pdf)

## 2 Platform- and compiler-dependent directives for C or C++

There is a large array of Cryptoki-related data types that are defined in the Cryptoki header files. Certain packing and pointer-related aspects of these types are platform and compiler-dependent; these aspects are therefore resolved on a platform-by-platform (or compiler-by-compiler) basis outside of the Cryptoki header files by means of preprocessor directives.

This means that when writing C or C++ code, certain preprocessor directives MUST be issued before including a Cryptoki header file. These directives are described in the remainder of this section.

Plattform specific implementation hints can be found in the pkcs11.h header file.

## 2.1 Structure packing

Cryptoki structures are packed to occupy as little space as is possible. Cryptoki structures SHALL be packed with 1-byte alignment.

## 2.2 Pointer-related macros

Because different platforms and compilers have different ways of dealing with different types of pointers, the following 6 macros SHALL be set outside the scope of Cryptoki:

¨ CK\_PTR

CK\_PTR is the “indirection string” a given platform and compiler uses to make a pointer to an object. It is used in the following fashion:

typedef CK\_BYTE CK\_PTR CK\_BYTE\_PTR;

¨ CK\_DECLARE\_FUNCTION

CK\_DECLARE\_FUNCTION(returnType, name), when followed by a parentheses-enclosed list of arguments and a semicolon, declares a Cryptoki API function in a Cryptoki library. returnType is the return type of the function, and name is its name. It SHALL be used in the following fashion:

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Initialize)(

CK\_VOID\_PTR pReserved

);

¨ CK\_DECLARE\_FUNCTION\_POINTER

CK\_DECLARE\_FUNCTION\_POINTER(returnType, name), when followed by a parentheses-enclosed list of arguments and a semicolon, declares a variable or type which is a pointer to a Cryptoki API function in a Cryptoki library. returnType is the return type of the function, and name is its name. It SHALL be used in either of the following fashions to define a function pointer variable, myC\_Initialize, which can point to a C\_Initialize function in a Cryptoki library (note that neither of the following code snippets actually assigns a value to myC\_Initialize):

CK\_DECLARE\_FUNCTION\_POINTER(CK\_RV, myC\_Initialize)(

CK\_VOID\_PTR pReserved

);

or:

typedef CK\_DECLARE\_FUNCTION\_POINTER(CK\_RV, myC\_InitializeType)(

CK\_VOID\_PTR pReserved

);

myC\_InitializeType myC\_Initialize;

¨ CK\_CALLBACK\_FUNCTION

CK\_CALLBACK\_FUNCTION(returnType, name), when followed by a parentheses-enclosed list of arguments and a semicolon, declares a variable or type which is a pointer to an application callback function that can be used by a Cryptoki API function in a Cryptoki library. returnType is the return type of the function, and name is its name. It SHALL be used in either of the following fashions to define a function pointer variable, myCallback, which can point to an application callback which takes arguments args and returns a CK\_RV (note that neither of the following code snippets actually assigns a value to myCallback):

CK\_CALLBACK\_FUNCTION(CK\_RV, myCallback)(args);

or:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, myCallbackType)(args);

myCallbackType myCallback;

¨ NULL\_PTR

NULL\_PTR is the value of a NULL pointer. In any ANSI C environment—and in many others as well—NULL\_PTR SHALL be defined simply as 0.

## 3 General data types

The general Cryptoki data types are described in the following subsections. The data types for holding parameters for various mechanisms, and the pointers to those parameters, are not described here; these types are described with the information on the mechanisms themselves, in Section 12.

A C or C++ source file in a Cryptoki application or library can define all these types (the types described here and the types that are specifically used for particular mechanism parameters) by including the top-level Cryptoki include file, pkcs11.h. pkcs11.h, in turn, includes the other Cryptoki include files, pkcs11t.h and pkcs11f.h. A source file can also include just pkcs11t.h (instead of pkcs11.h); this defines most (but not all) of the types specified here.

When including either of these header files, a source file MUST specify the preprocessor directives indicated in Section 2.

## 3.1 General information

Cryptoki represents general information with the following types:

¨ CK\_VERSION; CK\_VERSION\_PTR

**CK\_VERSION** is a structure that describes the version of a Cryptoki interface, a Cryptoki library, or an SSL or TLS implementation, or the hardware or firmware version of a slot or token. It is defined as follows:

typedef struct CK\_VERSION {

CK\_BYTE major;

CK\_BYTE minor;

} CK\_VERSION;

The fields of the structure have the following meanings:

*major* major version number (the integer portion of the version)

*minor* minor version number (the hundredths portion of the version)

Example: For version 1.0, *major* = 1 and *minor* = 0. For version 2.10, *major* = 2 and *minor* = 10. Table 4 below lists the major and minor version values for the officially published Cryptoki specifications.

Table 4, Major and minor version values for published Cryptoki specifications

| **Version** | **major** | **minor** |
| --- | --- | --- |
| 1.0 | 0x01 | 0x00 |
| 2.01 | 0x02 | 0x01 |
| 2.10 | 0x02 | 0x0a |
| 2.11 | 0x02 | 0x0b |
| 2.20 | 0x02 | 0x14 |
| 2.30 | 0x02 | 0x1e |
| 2.40 | 0x02 | 0x28 |
| 3.0 | 0x03 | 0x00 |

Minor revisions of the Cryptoki standard are always upwardly compatible within the same major version number.

**CK\_VERSION\_PTR** is a pointer to a **CK\_VERSION**.

¨ CK\_INFO; CK\_INFO\_PTR

**CK\_INFO** provides general information about Cryptoki. It is defined as follows:

typedef struct CK\_INFO {

CK\_VERSION cryptokiVersion;

CK\_UTF8CHAR manufacturerID\[32\];

CK\_FLAGS flags;

CK\_UTF8CHAR libraryDescription\[32\];

CK\_VERSION libraryVersion;

} CK\_INFO;  

The fields of the structure have the following meanings:

*cryptokiVersion* Cryptoki interface version number, for compatibility with future revisions of this interface

*manufacturerID* ID of the Cryptoki library manufacturer. MUST be padded with the blank character (‘ ‘). Should *not* be null-terminated.

*flags* bit flags reserved for future versions. MUST be zero for this version

*libraryDescription* character-string description of the library. MUST be padded with the blank character (‘ ‘). Should *not* be null-terminated.

*libraryVersion* Cryptoki library version number

For libraries written to this document, the value of *cryptokiVersion* should match the version of this specification; the value of *libraryVersion* is the version number of the library software itself.

**CK\_INFO\_PTR** is a pointer to a **CK\_INFO**.

¨ CK\_NOTIFICATION

**CK\_NOTIFICATION** holds the types of notifications that Cryptoki provides to an application. It is defined as follows:

typedef CK\_ULONG CK\_NOTIFICATION;

For this version of Cryptoki, the following types of notifications are defined:

CKN\_SURRENDER

The notifications have the following meanings:

*CKN\_SURRENDER* Cryptoki is surrendering the execution of a function executing in a session so that the application may perform other operations. After performing any desired operations, the application should indicate to Cryptoki whether to continue or cancel the function (see Section 5.21.1).

## 3.2 Slot and token types

Cryptoki represents slot and token information with the following types:

¨ CK\_SLOT\_ID; CK\_SLOT\_ID\_PTR

**CK\_SLOT\_ID** is a Cryptoki-assigned value that identifies a slot. It is defined as follows:

typedef CK\_ULONG CK\_SLOT\_ID;

A list of **CK\_SLOT\_ID** s is returned by **C\_GetSlotList**. A priori, *any* value of **CK\_SLOT\_ID** can be a valid slot identifier—in particular, a system may have a slot identified by the value 0. It need not have such a slot, however.

**CK\_SLOT\_ID\_PTR** is a pointer to a **CK\_SLOT\_ID**.

¨ CK\_SLOT\_INFO; CK\_SLOT\_INFO\_PTR

**CK\_SLOT\_INFO** provides information about a slot. It is defined as follows:

typedef struct CK\_SLOT\_INFO {

CK\_UTF8CHAR slotDescription\[64\];

CK\_UTF8CHAR manufacturerID\[32\];

CK\_FLAGS flags;

CK\_VERSION hardwareVersion;

CK\_VERSION firmwareVersion;

} CK\_SLOT\_INFO;

The fields of the structure have the following meanings:

*slotDescription* character-string description of the slot. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*manufacturerID* ID of the slot manufacturer. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*flags* bits flags that provide capabilities of the slot. The flags are defined below

*hardwareVersion* version number of the slot’s hardware

*firmwareVersion* version number of the slot’s firmware

The following table defines the *flags* field:

Table 5, Slot Information Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_TOKEN\_PRESENT | 0x00000001 | True if a token is present in the slot (*e.g.*, a device is in the reader) |
| CKF\_REMOVABLE\_DEVICE | 0x00000002 | True if the reader supports removable devices |
| CKF\_HW\_SLOT | 0x00000004 | True if the slot is a hardware slot, as opposed to a software slot implementing a “soft token” |

For a given slot, the value of the **CKF\_REMOVABLE\_DEVICE** flag *never changes*. In addition, if this flag is not set for a given slot, then the **CKF\_TOKEN\_PRESENT** flag for that slot is *always* set. That is, if a slot does not support a removable device, then that slot always has a token in it.

**CK\_SLOT\_INFO\_PTR** is a pointer to a **CK\_SLOT\_INFO**.

¨ CK\_TOKEN\_INFO; CK\_TOKEN\_INFO\_PTR

**CK\_TOKEN\_INFO** provides information about a token. It is defined as follows:

typedef struct CK\_TOKEN\_INFO {

CK\_UTF8CHAR label\[32\];

CK\_UTF8CHAR manufacturerID\[32\];

CK\_UTF8CHAR model\[16\];

CK\_CHAR serialNumber\[16\];

CK\_FLAGS flags;

CK\_ULONG ulMaxSessionCount;

CK\_ULONG ulSessionCount;

CK\_ULONG ulMaxRwSessionCount;

CK\_ULONG ulRwSessionCount;

CK\_ULONG ulMaxPinLen;

CK\_ULONG ulMinPinLen;

CK\_ULONG ulTotalPublicMemory;

CK\_ULONG ulFreePublicMemory;

CK\_ULONG ulTotalPrivateMemory;

CK\_ULONG ulFreePrivateMemory;

CK\_VERSION hardwareVersion;

CK\_VERSION firmwareVersion;

CK\_CHAR utcTime\[16\];

} CK\_TOKEN\_INFO;

The fields of the structure have the following meanings:

*label* application-defined label, assigned during token initialization. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*manufacturerID* ID of the device manufacturer. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*model* model of the device. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*serialNumber* character-string serial number of the device. MUST be padded with the blank character (‘ ‘). MUST NOT be null-terminated.

*flags* bit flags indicating capabilities and status of the device as defined below

*ulMaxSessionCount* maximum number of sessions that can be opened with the token at one time by a single application (see **CK\_TOKEN\_INFO Note** below)

*ulSessionCount* number of sessions that this application currently has open with the token (see **CK\_TOKEN\_INFO Note** below)

*ulMaxRwSessionCount* maximum number of read/write sessions that can be opened with the token at one time by a single application (see **CK\_TOKEN\_INFO Note** below)

*ulRwSessionCount* number of read/write sessions that this application currently has open with the token (see **CK\_TOKEN\_INFO Note** below)

*ulMaxPinLen* maximum length in bytes of the PIN

*ulMinPinLen* minimum length in bytes of the PIN

*ulTotalPublicMemory* the total amount of memory on the token in bytes in which public objects may be stored (see **CK\_TOKEN\_INFO Note** below)

*ulFreePublicMemory* the amount of free (unused) memory on the token in bytes for public objects (see **CK\_TOKEN\_INFO Note** below)

*ulTotalPrivateMemory* the total amount of memory on the token in bytes in which private objects may be stored (see **CK\_TOKEN\_INFO Note** below)

*ulFreePrivateMemory* the amount of free (unused) memory on the token in bytes for private objects (see **CK\_TOKEN\_INFO Note** below)

*hardwareVersion* version number of hardware

*firmwareVersion* version number of firmware

*utcTime* current time as a character-string of length 16, represented in the format YYYYMMDDhhmmssxx (4 characters for the year; 2 characters each for the month, the day, the hour, the minute, and the second; and 2 additional reserved ‘0’ characters). The value of this field only makes sense for tokens equipped with a clock, as indicated in the token information flags (see below)

The following table defines the *flags* field:

Table 6, Token Information Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_RNG | 0x00000001 | True if the token has its own random number generator |
| CKF\_WRITE\_PROTECTED | 0x00000002 | True if the token is write-protected (see below) |
| CKF\_LOGIN\_REQUIRED | 0x00000004 | True if there are some cryptographic functions that a user MUST be logged in to perform |
| CKF\_USER\_PIN\_INITIALIZED | 0x00000008 | True if the normal user’s PIN has been initialized |
| CKF\_RESTORE\_KEY\_NOT\_NEEDED | 0x00000020 | True if a successful save of a session’s cryptographic operations state *always* contains all keys needed to restore the state of the session |
| CKF\_CLOCK\_ON\_TOKEN | 0x00000040 | True if token has its own hardware clock |
| CKF\_PROTECTED\_AUTHENTICATION\_PATH | 0x00000100 | True if token has a “protected authentication path”, whereby a user can log into the token without passing a PIN through the Cryptoki library |
| CKF\_DUAL\_CRYPTO\_OPERATIONS | 0x00000200 | True if a single session with the token can perform dual cryptographic operations (see Section 5.14) |
| CKF\_TOKEN\_INITIALIZED | 0x00000400 | True if the token has been initialized using C\_InitToken or an equivalent mechanism outside the scope of this standard. Calling C\_InitToken when this flag is set will cause the token to be reinitialized. |
| CKF\_SECONDARY\_AUTHENTICATION | 0x00000800 | True if the token supports secondary authentication for private key objects. (Deprecated; new implementations MUST NOT set this flag) |
| CKF\_USER\_PIN\_COUNT\_LOW | 0x00010000 | True if an incorrect user login PIN has been entered at least once since the last successful authentication. |
| CKF\_USER\_PIN\_FINAL\_TRY | 0x00020000 | True if supplying an incorrect user PIN will cause it to become locked. |
| CKF\_USER\_PIN\_LOCKED | 0x00040000 | True if the user PIN has been locked. User login to the token is not possible. |
| CKF\_USER\_PIN\_TO\_BE\_CHANGED | 0x00080000 | True if the user PIN value is the default value set by token initialization or manufacturing, or the PIN has been expired by the card. |
| CKF\_SO\_PIN\_COUNT\_LOW | 0x00100000 | True if an incorrect SO login PIN has been entered at least once since the last successful authentication. |
| CKF\_SO\_PIN\_FINAL\_TRY | 0x00200000 | True if supplying an incorrect SO PIN will cause it to become locked. |
| CKF\_SO\_PIN\_LOCKED | 0x00400000 | True if the SO PIN has been locked. SO login to the token is not possible. |
| CKF\_SO\_PIN\_TO\_BE\_CHANGED | 0x00800000 | True if the SO PIN value is the default value set by token initialization or manufacturing, or the PIN has been expired by the card. |
| CKF\_ERROR\_STATE | 0x01000000 | True if the token failed a FIPS 140-2 self-test and entered an error state. |

Exactly what the **CKF\_WRITE\_PROTECTED** flag means is not specified in Cryptoki. An application may be unable to perform certain actions on a write-protected token; these actions can include any of the following, among others:

· Creating/modifying/deleting any object on the token.

· Creating/modifying/deleting a token object on the token.

· Changing the SO’s PIN.

· Changing the normal user’s PIN.

The token may change the value of the **CKF\_WRITE\_PROTECTED** flag depending on the session state to implement its object management policy. For instance, the token may set the **CKF\_WRITE\_PROTECTED** flag unless the session state is R/W SO or R/W User to implement a policy that does not allow any objects, public or private, to be created, modified, or deleted unless the user has successfully called C\_Login.

The **CKF\_USER\_PIN\_COUNT\_LOW**, **CKF\_USER\_PIN\_COUNT\_LOW**, **CKF\_USER\_PIN\_FINAL\_TRY**, and **CKF\_SO\_PIN\_FINAL\_TRY** flags may always be set to false if the token does not support the functionality or will not reveal the information because of its security policy.

The **CKF\_USER\_PIN\_TO\_BE\_CHANGED** and **CKF\_SO\_PIN\_TO\_BE\_CHANGED** flags may always be set to false if the token does not support the functionality. If a PIN is set to the default value, or has expired, the appropriate **CKF\_USER\_PIN\_TO\_BE\_CHANGED** or **CKF\_SO\_PIN\_TO\_BE\_CHANGED** flag is set to true. When either of these flags are true, logging in with the corresponding PIN will succeed, but only the C\_SetPIN function can be called. Calling any other function that required the user to be logged in will cause CKR\_PIN\_EXPIRED to be returned until C\_SetPIN is called successfully.

**CK\_TOKEN\_INFO Note**: The fields ulMaxSessionCount, ulSessionCount, ulMaxRwSessionCount, ulRwSessionCount, ulTotalPublicMemory, ulFreePublicMemory, ulTotalPrivateMemory, and ulFreePrivateMemory can have the special value CK\_UNAVAILABLE\_INFORMATION, which means that the token and/or library is unable or unwilling to provide that information. In addition, the fields ulMaxSessionCount and ulMaxRwSessionCount can have the special value CK\_EFFECTIVELY\_INFINITE, which means that there is no practical limit on the number of sessions (resp. R/W sessions) an application can have open with the token.

It is important to check these fields for these special values. This is particularly true for CK\_EFFECTIVELY\_INFINITE, since an application seeing this value in the ulMaxSessionCount or ulMaxRwSessionCount field would otherwise conclude that it can’t open any sessions with the token, which is far from being the case.

The upshot of all this is that the correct way to interpret (for example) the ulMaxSessionCount field is something along the lines of the following:

CK\_TOKEN\_INFO info;

.

.

if ((CK\_LONG) info.ulMaxSessionCount

\== CK\_UNAVAILABLE\_INFORMATION) {

/\* Token refuses to give value of ulMaxSessionCount \*/

.

.

} else if (info.ulMaxSessionCount == CK\_EFFECTIVELY\_INFINITE) {

/\* Application can open as many sessions as it wants \*/

.

.

} else {

/\* ulMaxSessionCount really does contain what it should \*/

.

.

}

CK\_TOKEN\_INFO\_PTR is a pointer to a CK\_TOKEN\_INFO.

## 3.3 Session types

Cryptoki represents session information with the following types:

¨ CK\_SESSION\_HANDLE; CK\_SESSION\_HANDLE\_PTR

**CK\_SESSION\_HANDLE** is a Cryptoki-assigned value that identifies a session. It is defined as follows:

typedef CK\_ULONG CK\_SESSION\_HANDLE;

*Valid session handles in Cryptoki always have nonzero values.* For developers’ convenience, Cryptoki defines the following symbolic value:

CK\_INVALID\_HANDLE

CK\_SESSION\_HANDLE\_PTR is a pointer to a CK\_SESSION\_HANDLE.

¨ CK\_USER\_TYPE

**CK\_USER\_TYPE** holds the types of Cryptoki users described in **\[PKCS11-UG\]** and, in addition, a context-specific type described in Section 4.9. It is defined as follows:

typedef CK\_ULONG CK\_USER\_TYPE;

For this version of Cryptoki, the following types of users are defined:

CKU\_SO

CKU\_USER

CKU\_CONTEXT\_SPECIFIC

¨ CK\_STATE

**CK\_STATE** holds the session state, as described in **\[PKCS11-UG\]**. It is defined as follows:

typedef CK\_ULONG CK\_STATE;

For this version of Cryptoki, the following session states are defined:

CKS\_RO\_PUBLIC\_SESSION

CKS\_RO\_USER\_FUNCTIONS

CKS\_RW\_PUBLIC\_SESSION

CKS\_RW\_USER\_FUNCTIONS

CKS\_RW\_SO\_FUNCTIONS

¨ CK\_SESSION\_INFO; CK\_SESSION\_INFO\_PTR

**CK\_SESSION\_INFO** provides information about a session. It is defined as follows:

typedef struct CK\_SESSION\_INFO {

CK\_SLOT\_ID slotID;

CK\_STATE state;

CK\_FLAGS flags;

CK\_ULONG ulDeviceError;

} CK\_SESSION\_INFO;

The fields of the structure have the following meanings:

*slotID* ID of the slot that interfaces with the token

*state* the state of the session

*flags* bit flags that define the type of session; the flags are defined below

*ulDeviceError* an error code defined by the cryptographic device. Used for errors not covered by Cryptoki.

The following table defines the *flags* field:

Table 7, Session Information Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_RW\_SESSION | 0x00000002 | True if the session is read/write; false if the session is read-only |
| CKF\_SERIAL\_SESSION | 0x00000004 | This flag is provided for backward compatibility, and should always be set to true |

CK\_SESSION\_INFO\_PTR is a pointer to a CK\_SESSION\_INFO.

## 3.4 Object types

Cryptoki represents object information with the following types:

¨ CK\_OBJECT\_HANDLE; CK\_OBJECT\_HANDLE\_PTR

**CK\_OBJECT\_HANDLE** is a token-specific identifier for an object. It is defined as follows:

typedef CK\_ULONG CK\_OBJECT\_HANDLE;

When an object is created or found on a token by an application, Cryptoki assigns it an object handle for that application’s sessions to use to access it. A particular object on a token does not necessarily have a handle which is fixed for the lifetime of the object; however, if a particular session can use a particular handle to access a particular object, then that session will continue to be able to use that handle to access that object as long as the session continues to exist, the object continues to exist, and the object continues to be accessible to the session.

*Valid object handles in Cryptoki always have nonzero values.* For developers’ convenience, Cryptoki defines the following symbolic value:

CK\_INVALID\_HANDLE

CK\_OBJECT\_HANDLE\_PTR is a pointer to a CK\_OBJECT\_HANDLE.

¨ CK\_OBJECT\_CLASS; CK\_OBJECT\_CLASS\_PTR

CK\_OBJECT\_CLASS is a value that identifies the classes (or types) of objects that Cryptoki recognizes. It is defined as follows:

typedef CK\_ULONG CK\_OBJECT\_CLASS;

Object classes are defined with the objects that use them. The type is specified on an object through the CKA\_CLASS attribute of the object.

Vendor defined values for this type may also be specified.

CKO\_VENDOR\_DEFINED

Object classes **CKO\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their object classes through the PKCS process.

**CK\_OBJECT\_CLASS\_PTR** is a pointer to a **CK\_OBJECT\_CLASS**.

¨ CK\_HW\_FEATURE\_TYPE

**CK\_HW\_FEATURE\_TYPE** is a value that identifies a hardware feature type of a device. It is defined as follows:

typedef CK\_ULONG CK\_HW\_FEATURE\_TYPE;

Hardware feature types are defined with the objects that use them. The type is specified on an object through the CKA\_HW\_FEATURE\_TYPE attribute of the object.

Vendor defined values for this type may also be specified.

CKH\_VENDOR\_DEFINED

Feature types **CKH\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their feature types through the PKCS process.

¨ CK\_KEY\_TYPE

**CK\_KEY\_TYPE** is a value that identifies a key type. It is defined as follows:

typedef CK\_ULONG CK\_KEY\_TYPE;

Key types are defined with the objects and mechanisms that use them. The key type is specified on an object through the CKA\_KEY\_TYPE attribute of the object.

Vendor defined values for this type may also be specified.

CKK\_VENDOR\_DEFINED

Key types **CKK\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their key types through the PKCS process.

¨ CK\_CERTIFICATE\_TYPE

**CK\_CERTIFICATE\_TYPE** is a value that identifies a certificate type. It is defined as follows:

typedef CK\_ULONG CK\_CERTIFICATE\_TYPE;

Certificate types are defined with the objects and mechanisms that use them. The certificate type is specified on an object through the CKA\_CERTIFICATE\_TYPE attribute of the object.

Vendor defined values for this type may also be specified.

CKC\_VENDOR\_DEFINED

Certificate types **CKC\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their certificate types through the PKCS process.

¨ CK\_CERTIFICATE\_CATEGORY

**CK\_CERTIFICATE\_CATEGORY** is a value that identifies a certificate category. It is defined as follows:

typedef CK\_ULONG CK\_CERTIFICATE\_CATEGORY;

For this version of Cryptoki, the following certificate categories are defined:

| **Constant** | **Value** | **Meaning** |
| --- | --- | --- |
| CK\_CERTIFICATE\_CATEGORY\_UNSPECIFIED | 0x00000000UL | No category specified |
| CK\_CERTIFICATE\_CATEGORY\_TOKEN\_USER | 0x00000001UL | Certificate belongs to owner of the token |
| CK\_CERTIFICATE\_CATEGORY\_AUTHORITY | 0x00000002UL | Certificate belongs to a certificate authority |
| CK\_CERTIFICATE\_CATEGORY\_OTHER\_ENTITY | 0x00000003UL | Certificate belongs to an end entity (i.e.: not a CA) |

¨ CK\_ATTRIBUTE\_TYPE

**CK\_ATTRIBUTE\_TYPE** is a value that identifies an attribute type. It is defined as follows:

typedef CK\_ULONG CK\_ATTRIBUTE\_TYPE;

Attributes are defined with the objects and mechanisms that use them. Attributes are specified on an object as a list of type, length value items. These are often specified as an attribute template.

Vendor defined values for this type may also be specified.

CKA\_VENDOR\_DEFINED

Attribute types **CKA\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their attribute types through the PKCS process.

¨ CK\_ATTRIBUTE; CK\_ATTRIBUTE\_PTR

**CK\_ATTRIBUTE** is a structure that includes the type, value, and length of an attribute. It is defined as follows:

typedef struct CK\_ATTRIBUTE {

CK\_ATTRIBUTE\_TYPE type;

CK\_VOID\_PTR pValue;

CK\_ULONG ulValueLen;

} CK\_ATTRIBUTE;

The fields of the structure have the following meanings:

*type* the attribute type

*pValue* pointer to the value of the attribute

*ulValueLen* length in bytes of the value

If an attribute has no value, then *ulValueLen* = 0, and the value of *pValue* is irrelevant. An array of **CK\_ATTRIBUTE** s is called a “template” and is used for creating, manipulating and searching for objects. The order of the attributes in a template *never* matters, even if the template contains vendor-specific attributes. Note that *pValue* is a “void” pointer, facilitating the passing of arbitrary values. Both the application and Cryptoki library MUST ensure that the pointer can be safely cast to the expected type (*i.e.*, without word-alignment errors).

The constant CK\_UNAVAILABLE\_INFORMATION is used in the ulValueLen field to denote an invalid or unavailable value. See C\_GetAttributeValue for further details.

**CK\_ATTRIBUTE\_PTR** is a pointer to a **CK\_ATTRIBUTE**.

¨ CK\_DATE

**CK\_DATE** is a structure that defines a date. It is defined as follows:

typedef struct CK\_DATE {

CK\_CHAR year\[4\];

CK\_CHAR month\[2\];

CK\_CHAR day\[2\];

} CK\_DATE;

The fields of the structure have the following meanings:

*year* the year (“1900” - “9999”)

*month* the month (“01” - “12”)

*day* the day (“01” - “31”)

The fields hold numeric characters from the character set in Table 3, not the literal byte values.

When a Cryptoki object carries an attribute of this type, and the default value of the attribute is specified to be "empty," then Cryptoki libraries SHALL set the attribute's *ulValueLen* to 0.

Note that implementations of previous versions of Cryptoki may have used other methods to identify an "empty" attribute of type CK\_DATE, and applications that needs to interoperate with these libraries therefore have to be flexible in what they accept as an empty value.

¨ CK\_PROFILE\_ID; CK\_PROFILE\_ID\_PTR

**CK\_PROFILE\_ID** is an unsigend ulong value represting a specific token profile. It is defined as follows:

typedef CK\_ULONG CK\_PROFILE\_ID;

[[Profile]]s are defines in the PKCS #11 Cryptographic Token Interface [[Profile]]s document. s. ID's greater than 0xffffffff may cause compatibility issues on platforms that have CK\_ULONG values of 32 bits, and should be avoided.

Vendor defined values for this type may also be specified.

CKP\_VENDOR\_DEFINED

[[Profile]] IDs **CKP\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their object classes through the PKCS process.

*Valid [[Profile]] IDs in Cryptoki always have nonzero values.* For developers’ convenience, Cryptoki defines the following symbolic value:

CKP\_INVALID\_ID

CK\_PROFILE\_ID\_PTR is a pointer to a CK\_PROFILE\_ID.

¨ CK\_JAVA\_MIDP\_SECURITY\_DOMAIN

CK\_JAVA\_MIDP\_SECURITY\_DOMAIN is a value that identifies the Java MIDP security domain of a certificate. It is defined as follows:

typedef CK\_ULONG CK\_JAVA\_MIDP\_SECURITY\_DOMAIN;

For this version of Cryptoki, the following security domains are defined. See the Java MIDP specification for further information:

| **Constant** | **Value** | **Meaning** |
| --- | --- | --- |
| CK\_SECURITY\_DOMAIN\_UNSPECIFIED | 0x00000000UL | No domain specified |
| CK\_SECURITY\_DOMAIN\_MANUFACTURER | 0x00000001UL | Manufacturer protection domain |
| CK\_SECURITY\_DOMAIN\_OPERATOR | 0x00000002UL | Operator protection domain |
| CK\_SECURITY\_DOMAIN\_THIRD\_PARTY | 0x00000003UL | Third party protection domain |

## 3.5 Data types for mechanisms

Cryptoki supports the following types for describing mechanisms and parameters to them:

¨ CK\_MECHANISM\_TYPE; CK\_MECHANISM\_TYPE\_PTR

**CK\_MECHANISM\_TYPE** is a value that identifies a mechanism type. It is defined as follows:

typedef CK\_ULONG CK\_MECHANISM\_TYPE;

Mechanism types are defined with the objects and mechanism descriptions that use them.

Vendor defined values for this type may also be specified.

CKM\_VENDOR\_DEFINED

Mechanism types **CKM\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their mechanism types through the PKCS process.

**CK\_MECHANISM\_TYPE\_PTR** is a pointer to a **CK\_MECHANISM\_TYPE**.

¨ CK\_MECHANISM; CK\_MECHANISM\_PTR

**CK\_MECHANISM** is a structure that specifies a particular mechanism and any parameters it requires. It is defined as follows:

typedef struct CK\_MECHANISM {

CK\_MECHANISM\_TYPE mechanism;

CK\_VOID\_PTR pParameter;

CK\_ULONG ulParameterLen;

} CK\_MECHANISM;

The fields of the structure have the following meanings:

*mechanism* the type of mechanism

*pParameter* pointer to the parameter if required by the mechanism

*ulParameterLen* length in bytes of the parameter

Note that *pParameter* is a “void” pointer, facilitating the passing of arbitrary values. Both the application and the Cryptoki library MUST ensure that the pointer can be safely cast to the expected type (*i.e.*, without word-alignment errors).

**CK\_MECHANISM\_PTR** is a pointer to a **CK\_MECHANISM**.

¨ CK\_MECHANISM\_INFO; CK\_MECHANISM\_INFO\_PTR

**CK\_MECHANISM\_INFO** is a structure that provides information about a particular mechanism. It is defined as follows:

typedef struct CK\_MECHANISM\_INFO {

CK\_ULONG ulMinKeySize;

CK\_ULONG ulMaxKeySize;

CK\_FLAGS flags;

} CK\_MECHANISM\_INFO;

The fields of the structure have the following meanings:

*ulMinKeySize* the minimum size of the key for the mechanism (whether this is measured in bits or in bytes is mechanism-dependent)

*ulMaxKeySize* the maximum size of the key for the mechanism (whether this is measured in bits or in bytes is mechanism-dependent)

*flags* bit flags specifying mechanism capabilities

For some mechanisms, the *ulMinKeySize* and *ulMaxKeySize* fields have meaningless values.

The following table defines the *flags* field:

Table 8, Mechanism Information Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_HW | 0x00000001 | True if the mechanism is performed by the device; false if the mechanism is performed in software |
| CKF\_MESSAGE\_ENCRYPT | 0x00000002 | True if the mechanism can be used with **C\_MessageEncryptInit** |
| CKF\_MESSAGE\_DECRYPT | 0x00000004 | True if the mechanism can be used with **C\_MessageDecryptInit** |
| CKF\_MESSAGE\_SIGN | 0x00000008 | True if the mechanism can be used with **C\_MessageSignInit** |
| CKF\_MESSAGE\_VERIFY | 0x00000010 | True if the mechanism can be used with **C\_MessageVerifyInit** |
| CKF\_MULTI\_MESSAGE | 0x00000020 | True if the mechanism can be used with **C\_\*MessageBegin**. One of CKF\_MESSAGE\_\* flag must also be set. |
| CKF\_FIND\_OBJECTS | 0x00000040 | This flag can be passed in as a parameter to **C\_SessionCancel** to cancel an active object search operation. Any other use of this flag is outside the scope of this standard. |
| CKF\_ENCRYPT | 0x00000100 | True if the mechanism can be used with **C\_EncryptInit** |
| CKF\_DECRYPT | 0x00000200 | True if the mechanism can be used with **C\_DecryptInit** |
| CKF\_DIGEST | 0x00000400 | True if the mechanism can be used with **C\_DigestInit** |
| CKF\_SIGN | 0x00000800 | True if the mechanism can be used with **C\_SignInit** |
| CKF\_SIGN\_RECOVER | 0x00001000 | True if the mechanism can be used with **C\_SignRecoverInit** |
| CKF\_VERIFY | 0x00002000 | True if the mechanism can be used with **C\_VerifyInit** |
| CKF\_VERIFY\_RECOVER | 0x00004000 | True if the mechanism can be used with **C\_VerifyRecoverInit** |
| CKF\_GENERATE | 0x00008000 | True if the mechanism can be used with **C\_GenerateKey** |
| CKF\_GENERATE\_KEY\_PAIR | 0x00010000 | True if the mechanism can be used with **C\_GenerateKeyPair** |
| CKF\_WRAP | 0x00020000 | True if the mechanism can be used with **C\_WrapKey** |
| CKF\_UNWRAP | 0x00040000 | True if the mechanism can be used with **C\_UnwrapKey** |
| CKF\_DERIVE | 0x00080000 | True if the mechanism can be used with **C\_DeriveKey** |
| CKF\_EXTENSION | 0x80000000 | True if there is an extension to the flags; false if no extensions. MUST be false for this version. |

CK\_MECHANISM\_INFO\_PTR is a pointer to a CK\_MECHANISM\_INFO.

## 3.6 Function types

Cryptoki represents information about functions with the following data types:

¨ CK\_RV

**CK\_RV** is a value that identifies the return value of a Cryptoki function. It is defined as follows:

typedef CK\_ULONG CK\_RV;

Vendor defined values for this type may also be specified.

CKR\_VENDOR\_DEFINED

Section 5.1 defines the meaning of each **CK\_RV** value. Return values **CKR\_VENDOR\_DEFINED** and above are permanently reserved for token vendors. For interoperability, vendors should register their return values through the PKCS process.

¨ CK\_NOTIFY

**CK\_NOTIFY** is the type of a pointer to a function used by Cryptoki to perform notification callbacks. It is defined as follows:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, CK\_NOTIFY)(

CK\_SESSION\_HANDLE hSession,

CK\_NOTIFICATION event,

CK\_VOID\_PTR pApplication

);

The arguments to a notification callback function have the following meanings:

*hSession* The handle of the session performing the callback

*event* The type of notification callback

*pApplication* An application-defined value. This is the same value as was passed to **C\_OpenSession** to open the session performing the callback

¨ CK\_C\_XXX

Cryptoki also defines an entire family of other function pointer types. For each function **C\_XXX** in the Cryptoki API (see Section 4.12 for detailed information about each of them), Cryptoki defines a type **CK\_C\_XXX**, which is a pointer to a function with the same arguments and return value as **C\_XXX** has. An appropriately-set variable of type **CK\_C\_XXX** may be used by an application to call the Cryptoki function **C\_XXX**.

¨ CK\_FUNCTION\_LIST; CK\_FUNCTION\_LIST\_PTR; CK\_FUNCTION\_LIST\_PTR\_PTR

**CK\_FUNCTION\_LIST** is a structure which contains a Cryptoki version and a function pointer to each function in the Cryptoki API. It is defined as follows:

typedef struct CK\_FUNCTION\_LIST {

CK\_VERSION version;

CK\_C\_Initialize C\_Initialize;

CK\_C\_Finalize C\_Finalize;

CK\_C\_GetInfo C\_GetInfo;

CK\_C\_GetFunctionList C\_GetFunctionList;

CK\_C\_GetSlotList C\_GetSlotList;

CK\_C\_GetSlotInfo C\_GetSlotInfo;

CK\_C\_GetTokenInfo C\_GetTokenInfo;

CK\_C\_GetMechanismList C\_GetMechanismList;

CK\_C\_GetMechanismInfo C\_GetMechanismInfo;

CK\_C\_InitToken C\_InitToken;

CK\_C\_InitPIN C\_InitPIN;

CK\_C\_SetPIN C\_SetPIN;

CK\_C\_OpenSession C\_OpenSession;

CK\_C\_CloseSession C\_CloseSession;

CK\_C\_CloseAllSessions C\_CloseAllSessions;

CK\_C\_GetSessionInfo C\_GetSessionInfo;

CK\_C\_GetOperationState C\_GetOperationState;

CK\_C\_SetOperationState C\_SetOperationState;

CK\_C\_Login C\_Login;

CK\_C\_Logout C\_Logout;

CK\_C\_CreateObject C\_CreateObject;

CK\_C\_CopyObject C\_CopyObject;

CK\_C\_DestroyObject C\_DestroyObject;

CK\_C\_GetObjectSize C\_GetObjectSize;

CK\_C\_GetAttributeValue C\_GetAttributeValue;

CK\_C\_SetAttributeValue C\_SetAttributeValue;

CK\_C\_FindObjectsInit C\_FindObjectsInit;

CK\_C\_FindObjects C\_FindObjects;

CK\_C\_FindObjectsFinal C\_FindObjectsFinal;

CK\_C\_EncryptInit C\_EncryptInit;

CK\_C\_Encrypt C\_Encrypt;

CK\_C\_EncryptUpdate C\_EncryptUpdate;

CK\_C\_EncryptFinal C\_EncryptFinal;

CK\_C\_DecryptInit C\_DecryptInit;

CK\_C\_Decrypt C\_Decrypt;

CK\_C\_DecryptUpdate C\_DecryptUpdate;

CK\_C\_DecryptFinal C\_DecryptFinal;

CK\_C\_DigestInit C\_DigestInit;

CK\_C\_Digest C\_Digest;

CK\_C\_DigestUpdate C\_DigestUpdate;

CK\_C\_DigestKey C\_DigestKey;

CK\_C\_DigestFinal C\_DigestFinal;

CK\_C\_SignInit C\_SignInit;

CK\_C\_Sign C\_Sign;

CK\_C\_SignUpdate C\_SignUpdate;

CK\_C\_SignFinal C\_SignFinal;

CK\_C\_SignRecoverInit C\_SignRecoverInit;

CK\_C\_SignRecover C\_SignRecover;

CK\_C\_VerifyInit C\_VerifyInit;

CK\_C\_Verify C\_Verify;

CK\_C\_VerifyUpdate C\_VerifyUpdate;

CK\_C\_VerifyFinal C\_VerifyFinal;

CK\_C\_VerifyRecoverInit C\_VerifyRecoverInit;

CK\_C\_VerifyRecover C\_VerifyRecover;

CK\_C\_DigestEncryptUpdate C\_DigestEncryptUpdate;

CK\_C\_DecryptDigestUpdate C\_DecryptDigestUpdate;

CK\_C\_SignEncryptUpdate C\_SignEncryptUpdate;

CK\_C\_DecryptVerifyUpdate C\_DecryptVerifyUpdate;

CK\_C\_GenerateKey C\_GenerateKey;

CK\_C\_GenerateKeyPair C\_GenerateKeyPair;

CK\_C\_WrapKey C\_WrapKey;

CK\_C\_UnwrapKey C\_UnwrapKey;

CK\_C\_DeriveKey C\_DeriveKey;

CK\_C\_SeedRandom C\_SeedRandom;

CK\_C\_GenerateRandom C\_GenerateRandom;

CK\_C\_GetFunctionStatus C\_GetFunctionStatus;

CK\_C\_CancelFunction C\_CancelFunction;

CK\_C\_WaitForSlotEvent C\_WaitForSlotEvent;

} CK\_FUNCTION\_LIST;

Each Cryptoki library has a static **CK\_FUNCTION\_LIST** structure, and a pointer to it (or to a copy of it which is also owned by the library) may be obtained by the **C\_GetFunctionList** function (see Section 5.2). The value that this pointer points to can be used by an application to quickly find out where the executable code for each function in the Cryptoki API is located. Every function in the Cryptoki API MUST have an entry point defined in the Cryptoki library’s **CK\_FUNCTION\_LIST** structure. If a particular function in the Cryptoki API is not supported by a library, then the function pointer for that function in the library’s **CK\_FUNCTION\_LIST** structure should point to a function stub which simply returns CKR\_FUNCTION\_NOT\_SUPPORTED.

In this structure ‘version’ is the cryptoki specification version number. The major and minor versions must be set to 0x02 and 0x28 indicating a version 2.40 compatible structure. The updated function list table for this version of the specification may be returned via **C\_GetInterfaceList** or **C\_GetInterface.**

An application may or may not be able to modify a Cryptoki library’s static **CK\_FUNCTION\_LIST** structure. Whether or not it can, it should never attempt to do so.

PKCS #11 modules must not add new functions at the end of the **CK\_FUNCTION\_LIST** that are not contained within the defined structure. If a PKCS#11 module needs to define additional functions, they should be placed within a vendor defined interface returned via **C\_GetInterfaceList** or **C\_GetInterface**.

**CK\_FUNCTION\_LIST\_PTR** is a pointer to a **CK\_FUNCTION\_LIST**.

**CK\_FUNCTION\_LIST\_PTR\_PTR** is a pointer to a **CK\_FUNCTION\_LIST\_PTR**.

¨ CK\_FUNCTION\_LIST\_3\_0; CK\_FUNCTION\_LIST\_3\_0\_PTR; CK\_FUNCTION\_LIST\_3\_0\_PTR\_PTR

**CK\_FUNCTION\_LIST\_3\_0** is a structure which contains the same function pointers as in **CK\_FUNCTION\_LIST** and additional functions added to the end of the structure that were defined in Cryptoki version 3.0. It is defined as follows:

typedef struct CK\_FUNCTION\_LIST\_3\_0 {

CK\_VERSION version;

CK\_C\_Initialize C\_Initialize;

CK\_C\_Finalize C\_Finalize;

CK\_C\_GetInfo C\_GetInfo;

CK\_C\_GetFunctionList C\_GetFunctionList;

CK\_C\_GetSlotList C\_GetSlotList;

CK\_C\_GetSlotInfo C\_GetSlotInfo;

CK\_C\_GetTokenInfo C\_GetTokenInfo;

CK\_C\_GetMechanismList C\_GetMechanismList;

CK\_C\_GetMechanismInfo C\_GetMechanismInfo;

CK\_C\_InitToken C\_InitToken;

CK\_C\_InitPIN C\_InitPIN;

CK\_C\_SetPIN C\_SetPIN;

CK\_C\_OpenSession C\_OpenSession;

CK\_C\_CloseSession C\_CloseSession;

CK\_C\_CloseAllSessions C\_CloseAllSessions;

CK\_C\_GetSessionInfo C\_GetSessionInfo;

CK\_C\_GetOperationState C\_GetOperationState;

CK\_C\_SetOperationState C\_SetOperationState;

CK\_C\_Login C\_Login;

CK\_C\_Logout C\_Logout;

CK\_C\_CreateObject C\_CreateObject;

CK\_C\_CopyObject C\_CopyObject;

CK\_C\_DestroyObject C\_DestroyObject;

CK\_C\_GetObjectSize C\_GetObjectSize;

CK\_C\_GetAttributeValue C\_GetAttributeValue;

CK\_C\_SetAttributeValue C\_SetAttributeValue;

CK\_C\_FindObjectsInit C\_FindObjectsInit;

CK\_C\_FindObjects C\_FindObjects;

CK\_C\_FindObjectsFinal C\_FindObjectsFinal;

CK\_C\_EncryptInit C\_EncryptInit;

CK\_C\_Encrypt C\_Encrypt;

CK\_C\_EncryptUpdate C\_EncryptUpdate;

CK\_C\_EncryptFinal C\_EncryptFinal;

CK\_C\_DecryptInit C\_DecryptInit;

CK\_C\_Decrypt C\_Decrypt;

CK\_C\_DecryptUpdate C\_DecryptUpdate;

CK\_C\_DecryptFinal C\_DecryptFinal;

CK\_C\_DigestInit C\_DigestInit;

CK\_C\_Digest C\_Digest;

CK\_C\_DigestUpdate C\_DigestUpdate;

CK\_C\_DigestKey C\_DigestKey;

CK\_C\_DigestFinal C\_DigestFinal;

CK\_C\_SignInit C\_SignInit;

CK\_C\_Sign C\_Sign;

CK\_C\_SignUpdate C\_SignUpdate;

CK\_C\_SignFinal C\_SignFinal;

CK\_C\_SignRecoverInit C\_SignRecoverInit;

CK\_C\_SignRecover C\_SignRecover;

CK\_C\_VerifyInit C\_VerifyInit;

CK\_C\_Verify C\_Verify;

CK\_C\_VerifyUpdate C\_VerifyUpdate;

CK\_C\_VerifyFinal C\_VerifyFinal;

CK\_C\_VerifyRecoverInit C\_VerifyRecoverInit;

CK\_C\_VerifyRecover C\_VerifyRecover;

CK\_C\_DigestEncryptUpdate C\_DigestEncryptUpdate;

CK\_C\_DecryptDigestUpdate C\_DecryptDigestUpdate;

CK\_C\_SignEncryptUpdate C\_SignEncryptUpdate;

CK\_C\_DecryptVerifyUpdate C\_DecryptVerifyUpdate;

CK\_C\_GenerateKey C\_GenerateKey;

CK\_C\_GenerateKeyPair C\_GenerateKeyPair;

CK\_C\_WrapKey C\_WrapKey;

CK\_C\_UnwrapKey C\_UnwrapKey;

CK\_C\_DeriveKey C\_DeriveKey;

CK\_C\_SeedRandom C\_SeedRandom;

CK\_C\_GenerateRandom C\_GenerateRandom;

CK\_C\_GetFunctionStatus C\_GetFunctionStatus;

CK\_C\_CancelFunction C\_CancelFunction;

CK\_C\_WaitForSlotEvent C\_WaitForSlotEvent;

CK\_C\_GetInterfaceList C\_GetInterfaceList;

CK\_C\_GetInterface C\_GetInterface;

CK\_C\_LoginUser C\_LoginUser;

CK\_C\_SessionCancel C\_SessionCancel;

CK\_C\_MessageEncryptInit C\_MessageEncryptInit;

CK\_C\_EncryptMessage C\_EncryptMessage;

CK\_C\_EncryptMessageBegin C\_EncryptMessageBegin;

CK\_C\_EncryptMessageNext C\_EncryptMessageNext;

CK\_C\_MessageEncryptFinal C\_MessageEncryptFinal;

CK\_C\_MessageDecryptInit C\_MessageDecryptInit;

CK\_C\_DecryptMessage C\_DecryptMessage;

CK\_C\_DecryptMessageBegin C\_DecryptMessageBegin;

CK\_C\_DecryptMessageNext C\_DecryptMessageNext;

CK\_C\_MessageDecryptFinal C\_MessageDecryptFinal;

CK\_C\_MessageSignInit C\_MessageSignInit;

CK\_C\_SignMessage C\_SignMessage;

CK\_C\_SignMessageBegin C\_SignMessageBegin;

CK\_C\_SignMessageNext C\_SignMessageNext;

CK\_C\_MessageSignFinal C\_MessageSignFinal;

CK\_C\_MessageVerifyInit C\_MessageVerifyInit;

CK\_C\_VerifyMessage C\_VerifyMessage;

CK\_C\_VerifyMessageBegin C\_VerifyMessageBegin;

CK\_C\_VerifyMessageNext C\_VerifyMessageNext;

CK\_C\_MessageVerifyFinal C\_MessageVerifyFinal;

} CK\_FUNCTION\_LIST\_3\_0;

For a general description of **CK\_FUNCTION\_LIST\_3\_0** see **CK\_FUNCTION\_LIST**.

In this structure, *version* is the cryptoki specification version number. It should match the value of *cryptokiVersion* returned in the **CK\_INFO** structure, but must be 3.0 at minimum.

This function list may be returned via **C\_GetInterfaceList** or **C\_GetInterface**

**CK\_FUNCTION\_LIST\_3\_0\_PTR** is a pointer to a **CK\_FUNCTION\_LIST\_3\_0**.

**CK\_FUNCTION\_LIST\_3\_0\_PTR\_PTR** is a pointer to a **CK\_FUNCTION\_LIST\_3\_0\_PTR**.

¨ CK\_INTERFACE; CK\_INTERFACE\_PTR; CK\_INTERFACE\_PTR\_PTR

**CK\_INTERFACE** is a structure which contains an interface name with a function list and flag.

It is defined as follows:

typedef struct CK\_INTERFACE {

CK\_UTF8CHAR\_PTR pInterfaceName;

CK\_VOID\_PTR pFunctionList;

CK\_FLAGS flags;

} CK\_INTERFACE;

The fields of the structure have the following meanings:

*pInterfaceName* the name of the interface

*pFunctionList* the interface function list which must always begin with a CK\_VERSION structure as the first field

*flags* bit flags specifying interface capabilities

The interface name “PKCS 11” is reserved for use by interfaces defined within the cryptoki specification.

Interfaces starting with the string: “Vendor ” are reserved for vendor use and will not oetherwise be defined as interfaces in the PKCS #11 specification. Vendors should supply new functions with interface names of “Vendor {vendor name}”. For example “Vendor ACME Inc”.

The following table defines the flags field:

Table 9, CK\_INTERFACE Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_INTERFACE\_FORK\_SAFE | 0x00000001 | The returned interface will have fork tolerant semantics. When the application forks, each process will get its own copy of all session objects, session states, login states, and encryption states. Each process will also maintain access to token objects with their previously supplied handles. |

**CK\_INTERFACE\_PTR** is a pointer to a **CK\_INTERFACE**.

**CK\_INTERFACE\_PTR\_PTR** is a pointer to a **CK\_INTERFACE\_PTR**.

## 3.7 Locking-related types

The types in this section are provided solely for applications which need to access Cryptoki from multiple threads simultaneously. *Applications which will not do this need not use any of these types.*

¨ CK\_CREATEMUTEX

**CK\_CREATEMUTEX** is the type of a pointer to an application-supplied function which creates a new mutex object and returns a pointer to it. It is defined as follows:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, CK\_CREATEMUTEX)(

CK\_VOID\_PTR\_PTR ppMutex

);

Calling a CK\_CREATEMUTEX function returns the pointer to the new mutex object in the location pointed to by ppMutex. Such a function should return one of the following values:

CKR\_OK, CKR\_GENERAL\_ERROR

CKR\_HOST\_MEMORY

¨ CK\_DESTROYMUTEX

**CK\_DESTROYMUTEX** is the type of a pointer to an application-supplied function which destroys an existing mutex object. It is defined as follows:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, CK\_DESTROYMUTEX)(

CK\_VOID\_PTR pMutex

);

The argument to a CK\_DESTROYMUTEX function is a pointer to the mutex object to be destroyed. Such a function should return one of the following values:

CKR\_OK, CKR\_GENERAL\_ERROR

CKR\_HOST\_MEMORY

CKR\_MUTEX\_BAD

¨ CK\_LOCKMUTEX and CK\_UNLOCKMUTEX

**CK\_LOCKMUTEX** is the type of a pointer to an application-supplied function which locks an existing mutex object. **CK\_UNLOCKMUTEX** is the type of a pointer to an application-supplied function which unlocks an existing mutex object. The proper behavior for these types of functions is as follows:

· If a CK\_LOCKMUTEX function is called on a mutex which is not locked, the calling thread obtains a lock on that mutex and returns.

· If a CK\_LOCKMUTEX function is called on a mutex which is locked by some thread other than the calling thread, the calling thread blocks and waits for that mutex to be unlocked.

· If a CK\_LOCKMUTEX function is called on a mutex which is locked by the calling thread, the behavior of the function call is undefined.

· If a CK\_UNLOCKMUTEX function is called on a mutex which is locked by the calling thread, that mutex is unlocked and the function call returns. Furthermore:

o If exactly one thread was blocking on that particular mutex, then that thread stops blocking, obtains a lock on that mutex, and its CK\_LOCKMUTEX call returns.

o If more than one thread was blocking on that particular mutex, then exactly one of the blocking threads is selected somehow. That lucky thread stops blocking, obtains a lock on the mutex, and its CK\_LOCKMUTEX call returns. All other threads blocking on that particular mutex continue to block.

· If a CK\_UNLOCKMUTEX function is called on a mutex which is not locked, then the function call returns the error code CKR\_MUTEX\_NOT\_LOCKED.

· If a CK\_UNLOCKMUTEX function is called on a mutex which is locked by some thread other than the calling thread, the behavior of the function call is undefined.

**CK\_LOCKMUTEX** is defined as follows:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, CK\_LOCKMUTEX)(

CK\_VOID\_PTR pMutex

);

The argument to a CK\_LOCKMUTEX function is a pointer to the mutex object to be locked. Such a function should return one of the following values:

CKR\_OK, CKR\_GENERAL\_ERROR

CKR\_HOST\_MEMORY,

CKR\_MUTEX\_BAD

**CK\_UNLOCKMUTEX** is defined as follows:

typedef CK\_CALLBACK\_FUNCTION(CK\_RV, CK\_UNLOCKMUTEX)(

CK\_VOID\_PTR pMutex

);

The argument to a CK\_UNLOCKMUTEX function is a pointer to the mutex object to be unlocked. Such a function should return one of the following values:

CKR\_OK, CKR\_GENERAL\_ERROR

CKR\_HOST\_MEMORY

CKR\_MUTEX\_BAD

CKR\_MUTEX\_NOT\_LOCKED

¨ CK\_C\_INITIALIZE\_ARGS; CK\_C\_INITIALIZE\_ARGS\_PTR

**CK\_C\_INITIALIZE\_ARGS** is a structure containing the optional arguments for the **C\_Initialize** function. For this version of Cryptoki, these optional arguments are all concerned with the way the library deals with threads. **CK\_C\_INITIALIZE\_ARGS** is defined as follows:

typedef struct CK\_C\_INITIALIZE\_ARGS {

CK\_CREATEMUTEX CreateMutex;

CK\_DESTROYMUTEX DestroyMutex;

CK\_LOCKMUTEX LockMutex;

CK\_UNLOCKMUTEX UnlockMutex;

CK\_FLAGS flags;

CK\_VOID\_PTR pReserved;

} CK\_C\_INITIALIZE\_ARGS;

The fields of the structure have the following meanings:

*CreateMutex* pointer to a function to use for creating mutex objects

*DestroyMutex* pointer to a function to use for destroying mutex objects

*LockMutex* pointer to a function to use for locking mutex objects

*UnlockMutex* pointer to a function to use for unlocking mutex objects

*flags* bit flags specifying options for **C\_Initialize**; the flags are defined below

*pReserved* reserved for future use. Should be NULL\_PTR for this version of Cryptoki

The following table defines the flags field:

Table 10, C\_Initialize Parameter Flags

| **Bit Flag** | **Mask** | **Meaning** |
| --- | --- | --- |
| CKF\_LIBRARY\_CANT\_CREATE\_OS\_THREADS | 0x00000001 | True if application threads which are executing calls to the library may *not* use native operating system calls to spawn new threads; false if they may |
| CKF\_OS\_LOCKING\_OK | 0x00000002 | True if the library can use the native operation system threading model for locking; false otherwise |

CK\_C\_INITIALIZE\_ARGS\_PTR is a pointer to a CK\_C\_INITIALIZE\_ARGS.

## 4 Objects

Cryptoki recognizes a number of classes of objects, as defined in the **CK\_OBJECT\_CLASS** data type. An object consists of a set of attributes, each of which has a given value. Each attribute that an object possesses has precisely one value. The following figure illustrates the high-level hierarchy of the Cryptoki objects and some of the attributes they support:

![](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/pkcs11-base-v3.0-os_files/image002.png)

Figure 1, Object Attribute Hierarchy

Cryptoki provides functions for creating, destroying, and copying objects in general, and for obtaining and modifying the values of their attributes. Some of the cryptographic functions (*e.g.*, **C\_GenerateKey**) also create key objects to hold their results.

Objects are always “well-formed” in Cryptoki—that is, an object always contains all required attributes, and the attributes are always consistent with one another from the time the object is created. This contrasts with some object-based paradigms where an object has no attributes other than perhaps a class when it is created, and is uninitialized for some time. In Cryptoki, objects are always initialized.

Tables throughout most of Section 4 define each Cryptoki attribute in terms of the data type of the attribute value and the meaning of the attribute, which may include a default initial value. Some of the data types are defined explicitly by Cryptoki (*e.g.*, **CK\_OBJECT\_CLASS**). Attribute values may also take the following types:

Byte array an arbitrary string (array) of **CK\_BYTE** s

Big integer a string of **CK\_BYTE** s representing an unsigned integer of arbitrary size, most-significant byte first (*e.g.*, the integer 32768 is represented as the 2-byte string 0x80 0x00)

Local string an unpadded string of **CK\_CHAR** s (see Table 3) with no null-termination

RFC2279 string an unpadded string of **CK\_UTF8CHAR** **s** with no null-termination

A token can hold several identical objects, *i.e.*, it is permissible for two or more objects to have exactly the same values for all their attributes.

In most cases each type of object in the Cryptoki specification possesses a completely well-defined set of Cryptoki attributes. Some of these attributes possess default values, and need not be specified when creating an object; some of these default values may even be the empty string (“”). Nonetheless, the object possesses these attributes. A given object has a single value for each attribute it possesses, even if the attribute is a vendor-specific attribute whose meaning is outside the scope of Cryptoki.

In addition to possessing Cryptoki attributes, objects may possess additional vendor-specific attributes whose meanings and values are not specified by Cryptoki.

## 4.1 Creating, modifying, and copying objects

All Cryptoki functions that create, modify, or copy objects take a template as one of their arguments, where the template specifies attribute values. Cryptographic functions that create objects (see Section 5.18) may also contribute some additional attribute values themselves; which attributes have values contributed by a cryptographic function call depends on which cryptographic mechanism is being performed (see \[PKCS11-Curr\] and \[PKCS11-Hist\] for specification of mechanisms for PKCS #11). In any case, all the required attributes supported by an object class that do not have default values MUST be specified when an object is created, either in the template or by the function itself.

### 4.1.1 Creating objects

Objects may be created with the Cryptoki functions **C\_CreateObject** (see Section 5.7), **C\_GenerateKey**, **C\_GenerateKeyPair**, **C\_UnwrapKey**, and **C\_DeriveKey** (see Section 5.18). In addition, copying an existing object (with the function **C\_CopyObject**) also creates a new object, but we consider this type of object creation separately in Section 4.1.3.

Attempting to create an object with any of these functions requires an appropriate template to be supplied.

1\. If the supplied template specifies a value for an invalid attribute, then the attempt should fail with the error code CKR\_ATTRIBUTE\_TYPE\_INVALID. An attribute is valid if it is either one of the attributes described in the Cryptoki specification or an additional vendor-specific attribute supported by the library and token.

2\. If the supplied template specifies an invalid value for a valid attribute, then the attempt should fail with the error code CKR\_ATTRIBUTE\_VALUE\_INVALID. The valid values for Cryptoki attributes are described in the Cryptoki specification.

3\. If the supplied template specifies a value for a read-only attribute, then the attempt should fail with the error code CKR\_ATTRIBUTE\_READ\_ONLY. Whether or not a given Cryptoki attribute is read-only is explicitly stated in the Cryptoki specification; however, a particular library and token may be even more restrictive than Cryptoki specifies. In other words, an attribute which Cryptoki says is not read-only may nonetheless be read-only under certain circumstances (*i.e.*, in conjunction with some combinations of other attributes) for a particular library and token. Whether or not a given non-Cryptoki attribute is read-only is obviously outside the scope of Cryptoki.

4\. If the attribute values in the supplied template, together with any default attribute values and any attribute values contributed to the object by the object-creation function itself, are insufficient to fully specify the object to create, then the attempt should fail with the error code CKR\_TEMPLATE\_INCOMPLETE.

5\. If the attribute values in the supplied template, together with any default attribute values and any attribute values contributed to the object by the object-creation function itself, are inconsistent, then the attempt should fail with the error code CKR\_TEMPLATE\_INCONSISTENT. A set of attribute values is inconsistent if not all of its members can be satisfied simultaneously *by the token*, although each value individually is valid in Cryptoki. One example of an inconsistent template would be using a template which specifies two different values for the same attribute. Another example would be trying to create a secret key object with an attribute which is appropriate for various types of public keys or private keys, but not for secret keys. A final example would be a template with an attribute that violates some token specific requirement. Note that this final example of an inconsistent template is token-dependent—on a different token, such a template might *not* be inconsistent.

6\. If the supplied template specifies the same value for a particular attribute more than once (or the template specifies the same value for a particular attribute that the object-creation function itself contributes to the object), then the behavior of Cryptoki is not completely specified. The attempt to create an object can either succeed—thereby creating the same object that would have been created if the multiply-specified attribute had only appeared once—or it can fail with error code CKR\_TEMPLATE\_INCONSISTENT. Library developers are encouraged to make their libraries behave as though the attribute had only appeared once in the template; application developers are strongly encouraged never to put a particular attribute into a particular template more than once.

If more than one of the situations listed above applies to an attempt to create an object, then the error code returned from the attempt can be any of the error codes from above that applies.

### 4.1.2 Modifying objects

Objects may be modified with the Cryptoki function **C\_SetAttributeValue** (see Section 5.7). The template supplied to **C\_SetAttributeValue** can contain new values for attributes which the object already possesses; values for attributes which the object does not yet possess; or both.

Some attributes of an object may be modified after the object has been created, and some may not. In addition, attributes which Cryptoki specifies are modifiable may actually *not* be modifiable on some tokens. That is, if a Cryptoki attribute is described as being modifiable, that really means only that it is modifiable *insofar as the Cryptoki specification is concerned*. A particular token might not actually support modification of some such attributes. Furthermore, whether or not a particular attribute of an object on a particular token is modifiable might depend on the values of certain attributes of the object. For example, a secret key object’s **CKA\_SENSITIVE** attribute can be changed from CK\_FALSE to CK\_TRUE, but not the other way around.

All the scenarios in Section 4.1.1—and the error codes they return—apply to modifying objects with **C\_SetAttributeValue**, except for the possibility of a template being incomplete.

### 4.1.3 Copying objects

Unless an object's CKA\_COPYABLE (see Table 17) attribute is set to CK\_FALSE, it may be copied with the Cryptoki function **C\_CopyObject** (see Section 5.7). In the process of copying an object, **C\_CopyObject** also modifies the attributes of the newly-created copy according to an application-supplied template.

The Cryptoki attributes which can be modified during the course of a **C\_CopyObject** operation are the same as the Cryptoki attributes which are described as being modifiable, plus the four special attributes **CKA\_TOKEN**, **CKA\_PRIVATE**, **CKA\_MODIFIABLE and CKA\_DESTROYABLE**. To be more precise, these attributes are modifiable during the course of a **C\_CopyObject** operation *insofar as the Cryptoki specification is concerned*. A particular token might not actually support modification of some such attributes during the course of a **C\_CopyObject** operation. Furthermore, whether or not a particular attribute of an object on a particular token is modifiable during the course of a **C\_CopyObject** operation might depend on the values of certain attributes of the object. For example, a secret key object’s **CKA\_SENSITIVE** attribute can be changed from CK\_FALSE to CK\_TRUE during the course of a **C\_CopyObject** operation, but not the other way around.

If the CKA\_COPYABLE attribute of the object to be copied is set to CK\_FALSE, C\_CopyObject returns CKR\_ACTION\_PROHIBITED. Otherwise, the scenarios described in 10.1.1 - and the error codes they return - apply to copying objects with C\_CopyObject, except for the possibility of a template being incomplete.

## 4.2 Common attributes

Table 11, Common footnotes for object attribute tables

<sup>1</sup> MUST be specified when object is created with **C\_CreateObject**.

<sup>2</sup> MUST *not* be specified when object is created with **C\_CreateObject**.

<sup>3</sup> MUST be specified when object is generated with **C\_GenerateKey** or **C\_GenerateKeyPair**.

<sup>4</sup> MUST *not* be specified when object is generated with **C\_GenerateKey** or **C\_GenerateKeyPair**.

<sup>5</sup> MUST be specified when object is unwrapped with **C\_UnwrapKey**.

<sup>6</sup> MUST *not* be specified when object is unwrapped with **C\_UnwrapKey**.

<sup>7</sup> Cannot be revealed if object has its **CKA\_SENSITIVE** attribute set to CK\_TRUE or its **CKA\_EXTRACTABLE** attribute set to CK\_FALSE.

<sup>8</sup> May be modified after object is created with a **C\_SetAttributeValue** call, or in the process of copying object with a **C\_CopyObject** call. However, it is possible that a particular token may not permit modification of the attribute during the course of a **C\_CopyObject** call.

<sup>9</sup> Default value is token-specific, and may depend on the values of other attributes.

<sup>10</sup> Can only be set to CK\_TRUE by the SO user.

<sup>11</sup> Attribute cannot be changed once set to CK\_TRUE. It becomes a read only attribute.

<sup>12</sup> Attribute cannot be changed once set to CK\_FALSE. It becomes a read only attribute.

Table 12, Common Object Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_CLASS <sup>1</sup> | CK\_OBJECT\_CLASS | Object class (type) |

Refer to Table 11 for footnotes

The above table defines the attributes common to all objects.

## 4.3 Hardware Feature Objects

### 4.3.1 Definitions

This section defines the object class CKO\_HW\_FEATURE for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.3.2 Overview

Hardware feature objects (**CKO\_HW\_FEATURE**) represent features of the device. They provide an easily expandable method for introducing new value-based features to the Cryptoki interface.

When searching for objects using **C\_FindObjectsInit** and **C\_FindObjects**, hardware feature objects are not returned unless the **CKA\_CLASS** attribute in the template has the value **CKO\_HW\_FEATURE**. This protects applications written to previous versions of Cryptoki from finding objects that they do not understand.

Table 13, Hardware Feature Common Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_HW\_FEATURE\_TYPE <sup>1</sup> | CK\_HW\_FEATURE\_TYPE | Hardware feature (type) |

<sup>-</sup> Refer to Table 11 for footnotes

### 4.3.3 Clock

#### 4.3.3.1 Definition

The CKA\_HW\_FEATURE\_TYPE attribute takes the value CKH\_CLOCK of type CK\_HW\_FEATURE\_TYPE.

#### 4.3.3.2 Description

Clock objects represent real-time clocks that exist on the device. This represents the same clock source as the **utcTime** field in the **CK\_TOKEN\_INFO** structure.

Table 14, Clock Object Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_VALUE | CK\_CHAR\[16\] | Current time as a character-string of length 16, represented in the format YYYYMMDDhhmmssxx (4 characters for the year; 2 characters each for the month, the day, the hour, the minute, and the second; and 2 additional reserved ‘0’ characters). |

The **CKA\_VALUE** attribute may be set using the **C\_SetAttributeValue** function if permitted by the device. The session used to set the time MUST be logged in. The device may require the SO to be the user logged in to modify the time value. **C\_SetAttributeValue** will return the error CKR\_USER\_NOT\_LOGGED\_IN to indicate that a different user type is required to set the value.

### 4.3.4 Monotonic Counter Objects

#### 4.3.4.1 Definition

The CKA\_HW\_FEATURE\_TYPE attribute takes the value CKH\_MONOTONIC\_COUNTER of type CK\_HW\_FEATURE\_TYPE.

#### 4.3.4.2 Description

Monotonic counter objects represent hardware counters that exist on the device. The counter is guaranteed to increase each time its value is read, but not necessarily by one. This might be used by an application for generating serial numbers to get some assurance of uniqueness per token.

Table 15, Monotonic Counter Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_RESET\_ON\_INIT <sup>1</sup> | CK\_BBOOL | The value of the counter will reset to a previously returned value if the token is initialized using **C\_InitToken**. |
| CKA\_HAS\_RESET <sup>1</sup> | CK\_BBOOL | The value of the counter has been reset at least once at some point in time. |
| CKA\_VALUE <sup>1</sup> | Byte Array | The current version of the monotonic counter. The value is returned in big endian order. |

<sup>1</sup> Read Only

The **CKA\_VALUE** attribute may not be set by the client.

### 4.3.5 User Interface Objects

#### 4.3.5.1 Definition

The CKA\_HW\_FEATURE\_TYPE attribute takes the value CKH\_USER\_INTERFACE of type CK\_HW\_FEATURE\_TYPE.

#### 4.3.5.2 Description

User interface objects represent the presentation capabilities of the device.

Table 16, User Interface Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_PIXEL\_X | CK\_ULONG | Screen resolution (in pixels) in X-axis (e.g. 1280) |
| CKA\_PIXEL\_Y | CK\_ULONG | Screen resolution (in pixels) in Y-axis (e.g. 1024) |
| CKA\_RESOLUTION | CK\_ULONG | DPI, pixels per inch |
| CKA\_CHAR\_ROWS | CK\_ULONG | For character-oriented displays; number of character rows (e.g. 24) |
| CKA\_CHAR\_COLUMNS | CK\_ULONG | For character-oriented displays: number of character columns (e.g. 80). If display is of proportional-font type, this is the width of the display in “em”-s (letter “M”), see CC/PP Struct. |
| CKA\_COLOR | CK\_BBOOL | Color support |
| CKA\_BITS\_PER\_PIXEL | CK\_ULONG | The number of bits of color or grayscale information per pixel. |
| CKA\_CHAR\_SETS | RFC 2279 string | String indicating supported character sets, as defined by IANA MIBenum sets ([www.iana.org](http://www.iana.org/)). Supported character sets are separated with “;”. E.g. a token supporting iso-8859-1 and US-ASCII would set the attribute value to “4;3”. |
| CKA\_ENCODING\_METHODS | RFC 2279 string | String indicating supported content transfer encoding methods, as defined by IANA ([www.iana.org](http://www.iana.org/)). Supported methods are separated with “;”. E.g. a token supporting 7bit, 8bit and base64 could set the attribute value to “7bit;8bit;base64”. |
| CKA\_MIME\_TYPES | RFC 2279 string | String indicating supported (presentable) MIME-types, as defined by IANA ([www.iana.org](http://www.iana.org/)). Supported types are separated with “;”. E.g. a token supporting MIME types "a/b", "a/c" and "a/d" would set the attribute value to “a/b;a/c;a/d”. |

The selection of attributes, and associated data types, has been done in an attempt to stay as aligned with RFC 2534 and CC/PP Struct as possible. The special value CK\_UNAVAILABLE\_INFORMATION may be used for CK\_ULONG-based attributes when information is not available or applicable.

None of the attribute values may be set by an application.

The value of the **CKA\_ENCODING\_METHODS** attribute may be used when the application needs to send MIME objects with encoded content to the token.

## 4.4 Storage Objects

This is not an object class; hence no CKO\_ definition is required. It is a category of object classes with common attributes for the object classes that follow.

Table 17, Common Storage Object Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_TOKEN | CK\_BBOOL | CK\_TRUE if object is a token object; CK\_FALSE if object is a session object. Default is CK\_FALSE. |
| CKA\_PRIVATE | CK\_BBOOL | CK\_TRUE if object is a private object; CK\_FALSE if object is a public object. Default value is token-specific, and may depend on the values of other attributes of the object. |
| CKA\_MODIFIABLE | CK\_BBOOL | CK\_TRUE if object can be modified Default is CK\_TRUE. |
| CKA\_LABEL | RFC2279 string | Description of the object (default empty). |
| CKA\_COPYABLE | CK\_BBOOL | CK\_TRUE if object can be copied using C\_CopyObject. Defaults to CK\_TRUE. Can’t be set to TRUE once it is set to FALSE. |
| CKA\_DESTROYABLE | CK\_BBOOL | CK\_TRUE if the object can be destroyed using C\_DestroyObject. Default is CK\_TRUE. |
| CKA\_UNIQUE\_ID <sup>246</sup> | RFC2279 string | The unique identifier assigned to the object. |

Only the **CKA\_LABEL** attribute can be modified after the object is created. (The **CKA\_TOKEN**, **CKA\_PRIVATE**, and **CKA\_MODIFIABLE** attributes can be changed in the process of copying an object, however.)

The **CKA\_TOKEN** attribute identifies whether the object is a token object or a session object.

When the **CKA\_PRIVATE** attribute is CK\_TRUE, a user may not access the object until the user has been authenticated to the token.

The value of the **CKA\_MODIFIABLE** attribute determines whether or not an object is read-only.

The **CKA\_LABEL** attribute is intended to assist users in browsing.

The value of the CKA\_COPYABLE attribute determines whether or not an object can be copied. This attribute can be used in conjunction with CKA\_MODIFIABLE to prevent changes to the permitted usages of keys and other objects.

The value of the CKA\_DESTROYABLE attribute determines whether the object can be destroyed using C\_DestroyObject.

### 4.4.1 The CKA\_UNIQUE\_ID attribute

Any time a new object is created, a value for CKA\_UNIQUE\_ID MUST be generated by the token and stored with the object. The specific algorithm used to generate unique ID values for objects is token-specific, but values generated MUST be unique across all objects visible to any particular session, and SHOULD be unique across all objects created by the token. Reinitializing the token, such as by calling C\_InitToken, MAY cause reuse of CKA\_UNIQUE\_ID values.

Any attempt to modify the CKA\_UNIQUE\_ID attribute of an existing object or to specify the value of the CKA\_UNIQUE\_ID attribute in the template for an operation that creates one or more objects MUST fail. Operations failing for this reason return the error code CKR\_ATTRIBUTE\_READ\_ONLY.

## 4.5 Data objects

### 4.5.1 Definitions

This section defines the object class CKO\_DATA for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.5.2 Overview

Data objects (object class **CKO\_DATA**) hold information defined by an application. Other than providing access to it, Cryptoki does not attach any special meaning to a data object. The following table lists the attributes supported by data objects, in addition to the common attributes defined for this object class:

Table 18, Data Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_APPLICATION | RFC2279 string | Description of the application that manages the object (default empty) |
| CKA\_OBJECT\_ID | Byte Array | DER-encoding of the object identifier indicating the data object type (default empty) |
| CKA\_VALUE | Byte array | Value of the object (default empty) |

The **CKA\_APPLICATION** attribute provides a means for applications to indicate ownership of the data objects they manage. Cryptoki does not provide a means of ensuring that only a particular application has access to a data object, however.

The **CKA\_OBJECT\_ID** attribute provides an application independent and expandable way to indicate the type of the data object value. Cryptoki does not provide a means of insuring that the data object identifier matches the data value.

The following is a sample template containing attributes for creating a data object:

CK\_OBJECT\_CLASS class = CKO\_DATA;

CK\_UTF8CHAR label\[\] = “A data object”;

CK\_UTF8CHAR application\[\] = “An application”;

CK\_BYTE data\[\] = “Sample data”;

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] = {

{CKA\_CLASS, &class, sizeof(class)},

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_LABEL, label, sizeof(label)-1},

{CKA\_APPLICATION, application, sizeof(application)-1},

{CKA\_VALUE, data, sizeof(data)}

};

## 4.6 Certificate objects

### 4.6.1 Definitions

This section defines the object class CKO\_CERTIFICATE for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.6.2 Overview

Certificate objects (object class **CKO\_CERTIFICATE**) hold public-key or attribute certificates. Other than providing access to certificate objects, Cryptoki does not attach any special meaning to certificates. The following table defines the common certificate object attributes, in addition to the common attributes defined for this object class:

Table 19, Common Certificate Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_CERTIFICATE\_TYPE <sup>1</sup> | CK\_CERTIFICATE\_TYPE | Type of certificate |
| CKA\_TRUSTED <sup>10</sup> | CK\_BBOOL | The certificate can be trusted for the application that it was created. |
| CKA\_CERTIFICATE\_CATEGORY | CKA\_CERTIFICATE\_CATEGORY | (default CK\_CERTIFICATE\_CATEGORY\_UNSPECIFIED) |
| CKA\_CHECK\_VALUE | Byte array | Checksum |
| CKA\_START\_DATE | CK\_DATE | Start date for the certificate (default empty) |
| CKA\_END\_DATE | CK\_DATE | End date for the certificate (default empty) |
| CKA\_PUBLIC\_KEY\_INFO | Byte Array | DER-encoding of the SubjectPublicKeyInfo for the public key contained in this certificate (default empty) |

<sup>-</sup> Refer to Table 11 for footnotes

Cryptoki does not enforce the relationship of the CKA\_PUBLIC\_KEY\_INFO to the public key in the certificate, but does recommend that the key be extracted from the certificate to create this value.

The **CKA\_CERTIFICATE\_TYPE** attribute may not be modified after an object is created. This version of Cryptoki supports the following certificate types:

· X.509 public key certificate

- WTLS public key certificate

· X.509 attribute certificate

The **CKA\_TRUSTED** attribute cannot be set to CK\_TRUE by an application. It MUST be set by a token initialization application or by the token’s SO. Trusted certificates cannot be modified.

The **CKA\_CERTIFICATE\_CATEGORY** attribute is used to indicate if a stored certificate is a user certificate for which the corresponding private key is available on the token (“token user”), a CA certificate (“authority”), or another end-entity certificate (“other entity”). This attribute may not be modified after an object is created.

The **CKA\_CERTIFICATE\_CATEGORY** and **CKA\_TRUSTED** attributes will together be used to map to the categorization of the certificates.

**CKA\_CHECK\_VALUE**: The value of this attribute is derived from the certificate by taking the first three bytes of the SHA-1 hash of the certificate object’s CKA\_VALUE attribute.

The **CKA\_START\_DATE** and **CKA\_END\_DATE** attributes are for reference only; Cryptoki does not attach any special meaning to them. When present, the application is responsible to set them to values that match the certificate’s encoded “not before” and “not after” fields (if any).

### 4.6.3 X.509 public key certificate objects

X.509 certificate objects (certificate type **CKC\_X\_509**) hold X.509 public key certificates. The following table defines the X.509 certificate object attributes, in addition to the common attributes defined for this object class:

Table 20, X.509 Certificate Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_SUBJECT <sup>1</sup> | Byte array | DER-encoding of the certificate subject name |
| CKA\_ID | Byte array | Key identifier for public/private key pair (default empty) |
| CKA\_ISSUER | Byte array | DER-encoding of the certificate issuer name (default empty) |
| CKA\_SERIAL\_NUMBER | Byte array | DER-encoding of the certificate serial number (default empty) |
| CKA\_VALUE <sup>2</sup> | Byte array | BER-encoding of the certificate |
| CKA\_URL <sup>3</sup> | RFC2279 string | If not empty this attribute gives the URL where the complete certificate can be obtained (default empty) |
| CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY <sup>4</sup> | Byte array | Hash of the subject public key (default empty). Hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM |
| CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY <sup>4</sup> | Byte array | Hash of the issuer public key (default empty). Hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM |
| CKA\_JAVA\_MIDP\_SECURITY\_DOMAIN | CK\_JAVA\_MIDP\_SECURITY\_DOMAIN | Java MIDP security domain. (default CK\_SECURITY\_DOMAIN\_UNSPECIFIED) |
| CKA\_NAME\_HASH\_ALGORITHM | CK\_MECHANISM\_TYPE | Defines the mechanism used to calculate CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY and CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY. If the attribute is not present then the type defaults to SHA-1. |

<sup>1</sup> MUST be specified when the object is created.<sup><br>2</sup> MUST be specified when the object is created. MUST be non-empty if CKA\_URL is empty.

<sup>3</sup> MUST be non-empty if CKA\_VALUE is empty.

<sup>4</sup> Can only be empty if CKA\_URL is empty.

Only the **CKA\_ID**, **CKA\_ISSUER**, and **CKA\_SERIAL\_NUMBER** attributes may be modified after the object is created.

The **CKA\_ID** attribute is intended as a means of distinguishing multiple public-key/private-key pairs held by the same subject (whether stored in the same token or not). (Since the keys are distinguished by subject name as well as identifier, it is possible that keys for different subjects may have the same **CKA\_ID** value without introducing any ambiguity.)

It is intended in the interests of interoperability that the subject name and key identifier for a certificate will be the same as those for the corresponding public and private keys (though it is not required that all be stored in the same token). However, Cryptoki does not enforce this association, or even the uniqueness of the key identifier for a given subject; in particular, an application may leave the key identifier empty.

The **CKA\_ISSUER** and **CKA\_SERIAL\_NUMBER** attributes are for compatibility with PKCS #7 and Privacy Enhanced Mail (RFC1421). Note that with the version 3 extensions to X.509 certificates, the key identifier may be carried in the certificate. It is intended that the **CKA\_ID** value be identical to the key identifier in such a certificate extension, although this will not be enforced by Cryptoki.

The **CKA\_URL** attribute enables the support for storage of the URL where the certificate can be found instead of the certificate itself. Storage of a URL instead of the complete certificate is often used in mobile environments.

The **CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY** and **CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY** attributes are used to store the hashes of the public keys of the subject and the issuer. They are particularly important when only the URL is available to be able to correlate a certificate with a private key and when searching for the certificate of the issuer. The hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM.

The **CKA\_JAVA\_MIDP\_SECURITY\_DOMAIN** attribute associates a certificate with a Java MIDP security domain.

The following is a sample template for creating an X.509 certificate object:

CK\_OBJECT\_CLASS class = CKO\_CERTIFICATE;

CK\_CERTIFICATE\_TYPE certType = CKC\_X\_509;

CK\_UTF8CHAR label\[\] = “A certificate object”;

CK\_BYTE subject\[\] = {...};

CK\_BYTE id\[\] = {123};

CK\_BYTE certificate\[\] = {...};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] = {

{CKA\_CLASS, &class, sizeof(class)},

{CKA\_CERTIFICATE\_TYPE, &certType, sizeof(certType)};

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_LABEL, label, sizeof(label)-1},

{CKA\_SUBJECT, subject, sizeof(subject)},

{CKA\_ID, id, sizeof(id)},

{CKA\_VALUE, certificate, sizeof(certificate)}

};

### 4.6.4 WTLS public key certificate objects

WTLS certificate objects (certificate type **CKC\_WTLS**) hold WTLS public key certificates. The following table defines the WTLS certificate object attributes, in addition to the common attributes defined for this object class.

Table 21: WTLS Certificate Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_SUBJECT <sup>1</sup> | Byte array | WTLS-encoding (Identifier type) of the certificate subject |
| CKA\_ISSUER | Byte array | WTLS-encoding (Identifier type) of the certificate issuer (default empty) |
| CKA\_VALUE <sup>2</sup> | Byte array | WTLS-encoding of the certificate |
| CKA\_URL <sup>3</sup> | RFC2279 string | If not empty this attribute gives the URL where the complete certificate can be obtained |
| CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY <sup>4</sup> | Byte array | SHA-1 hash of the subject public key (default empty). Hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM |
| CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY <sup>4</sup> | Byte array | SHA-1 hash of the issuer public key (default empty). Hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM |
| CKA\_NAME\_HASH\_ALGORITHM | CK\_MECHANISM\_TYPE | Defines the mechanism used to calculate CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY and CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY. If the attribute is not present then the type defaults to SHA-1. |

<sup>1</sup> MUST be specified when the object is created. Can only be empty if CKA\_VALUE is empty.

<sup>2</sup> MUST be specified when the object is created. MUST be non-empty if CKA\_URL is empty.

<sup>3</sup> MUST be non-empty if CKA\_VALUE is empty.

<sup>4</sup> Can only be empty if CKA\_URL is empty.

Only the **CKA\_ISSUER** attribute may be modified after the object has been created.

The encoding for the **CKA\_SUBJECT**, **CKA\_ISSUER**, and **CKA\_VALUE** attributes can be found in \[WTLS\].

The **CKA\_URL** attribute enables the support for storage of the URL where the certificate can be found instead of the certificate itself. Storage of a URL instead of the complete certificate is often used in mobile environments.

The **CKA\_HASH\_OF\_SUBJECT\_PUBLIC\_KEY** and **CKA\_HASH\_OF\_ISSUER\_PUBLIC\_KEY** attributes are used to store the hashes of the public keys of the subject and the issuer. They are particularly important when only the URL is available to be able to correlate a certificate with a private key and when searching for the certificate of the issuer. The hash algorithm is defined by CKA\_NAME\_HASH\_ALGORITHM.

The following is a sample template for creating a WTLS certificate object:

CK\_OBJECT\_CLASS class = CKO\_CERTIFICATE;

CK\_CERTIFICATE\_TYPE certType = CKC\_WTLS;

CK\_UTF8CHAR label\[\] = “A certificate object”;

CK\_BYTE subject\[\] = {...};

CK\_BYTE certificate\[\] = {...};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] =

{

{CKA\_CLASS, &class, sizeof(class)},

{CKA\_CERTIFICATE\_TYPE, &certType, sizeof(certType)};

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_LABEL, label, sizeof(label)-1},

{CKA\_SUBJECT, subject, sizeof(subject)},

{CKA\_VALUE, certificate, sizeof(certificate)}

};

### 4.6.5 X.509 attribute certificate objects

X.509 attribute certificate objects (certificate type **CKC\_X\_509\_ATTR\_CERT**) hold X.509 attribute certificates. The following table defines the X.509 attribute certificate object attributes, in addition to the common attributes defined for this object class:

Table 22, X.509 Attribute Certificate Object Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_OWNER <sup>1</sup> | Byte Array | DER-encoding of the attribute certificate's subject field. This is distinct from the CKA\_SUBJECT attribute contained in CKC\_X\_509 certificates because the [[ASN.1]] syntax and encoding are different. |
| CKA\_AC\_ISSUER | Byte Array | DER-encoding of the attribute certificate's issuer field. This is distinct from the CKA\_ISSUER attribute contained in CKC\_X\_509 certificates because the [[ASN.1]] syntax and encoding are different. (default empty) |
| CKA\_SERIAL\_NUMBER | Byte Array | DER-encoding of the certificate serial number. (default empty) |
| CKA\_ATTR\_TYPES | Byte Array | BER-encoding of a sequence of object identifier values corresponding to the attribute types contained in the certificate. When present, this field offers an opportunity for applications to search for a particular attribute certificate without fetching and parsing the certificate itself. (default empty) |
| CKA\_VALUE <sup>1</sup> | Byte Array | BER-encoding of the certificate. |

<sup>1</sup> MUST be specified when the object is created

Only the **CKA\_AC\_ISSUER**, **CKA\_SERIAL\_NUMBER** and **CKA\_ATTR\_TYPES** attributes may be modified after the object is created.

The following is a sample template for creating an X.509 attribute certificate object:

CK\_OBJECT\_CLASS class = CKO\_CERTIFICATE;

CK\_CERTIFICATE\_TYPE certType = CKC\_X\_509\_ATTR\_CERT;

CK\_UTF8CHAR label\[\] = "An attribute certificate object";

CK\_BYTE owner\[\] = {...};

CK\_BYTE certificate\[\] = {...};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] = {

{CKA\_CLASS, &class, sizeof(class)},

{CKA\_CERTIFICATE\_TYPE, &certType, sizeof(certType)};

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_LABEL, label, sizeof(label)-1},

{CKA\_OWNER, owner, sizeof(owner)},

{CKA\_VALUE, certificate, sizeof(certificate)}

};

## 4.7 Key objects

### 4.7.1 Definitions

There is no CKO\_ definition for the base key object class, only for the key types derived from it.

This section defines the object class CKO\_PUBLIC\_KEY, CKO\_PRIVATE\_KEY and CKO\_SECRET\_KEY for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.7.2 Overview

Key objects hold encryption or authentication keys, which can be public keys, private keys, or secret keys. The following common footnotes apply to all the tables describing attributes of keys:

The following table defines the attributes common to public key, private key and secret key classes, in addition to the common attributes defined for this object class:

Table 23, Common Key Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_KEY\_TYPE <sup>1,5</sup> | CK\_KEY\_TYPE | Type of key |
| CKA\_ID <sup>8</sup> | Byte array | Key identifier for key (default empty) |
| CKA\_START\_DATE <sup>8</sup> | CK\_DATE | Start date for the key (default empty) |
| CKA\_END\_DATE <sup>8</sup> | CK\_DATE | End date for the key (default empty) |
| CKA\_DERIVE <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports key derivation (*i.e.*, if other keys can be derived from this one (default CK\_FALSE) |
| CKA\_LOCAL <sup>2,4,6</sup> | CK\_BBOOL | CK\_TRUE only if key was either  · generated locally (*i.e.*, on the token) with a **C\_GenerateKey** or **C\_GenerateKeyPair** call  · created with a **C\_CopyObject** call as a copy of a key which had its **CKA\_LOCAL** attribute set to CK\_TRUE |
| CKA\_KEY\_GEN\_   MECHANISM <sup>2,4,6</sup> | CK\_MECHANISM\_TYPE | Identifier of the mechanism used to generate the key material. |
| CKA\_ALLOWED\_MECHANISMS | CK\_MECHANISM\_TYPE \_PTR, pointer to a CK\_MECHANISM\_TYPE array | A list of mechanisms allowed to be used with this key. The number of mechanisms in the array is the *ulValueLen* component of the attribute divided by the size  of CK\_MECHANISM\_TYPE. |

<sup>-</sup> Refer to Table 11 for footnotes

The **CKA\_ID** field is intended to distinguish among multiple keys. In the case of public and private keys, this field assists in handling multiple keys held by the same subject; the key identifier for a public key and its corresponding private key should be the same. The key identifier should also be the same as for the corresponding certificate, if one exists. Cryptoki does not enforce these associations, however. (See Section 0 for further commentary.)

In the case of secret keys, the meaning of the **CKA\_ID** attribute is up to the application.

Note that the **CKA\_START\_DATE** and **CKA\_END\_DATE** attributes are for reference only; Cryptoki does not attach any special meaning to them. In particular, it does not restrict usage of a key according to the dates; doing this is up to the application.

The **CKA\_DERIVE** attribute has the value CK\_TRUE if and only if it is possible to derive other keys from the key.

The **CKA\_LOCAL** attribute has the value CK\_TRUE if and only if the value of the key was originally generated on the token by a **C\_GenerateKey** or **C\_GenerateKeyPair** call.

The **CKA\_KEY\_GEN\_MECHANISM** attribute identifies the key generation mechanism used to generate the key material. It contains a valid value only if the **CKA\_LOCAL** attribute has the value CK\_TRUE. If **CKA\_LOCAL** has the value CK\_FALSE, the value of the attribute is CK\_UNAVAILABLE\_INFORMATION.

## 4.8 Public key objects

Public key objects (object class **CKO\_PUBLIC\_KEY**) hold public keys. The following table defines the attributes common to all public keys, in addition to the common attributes defined for this object class:

Table 24, Common Public Key Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_SUBJECT <sup>8</sup> | Byte array | DER-encoding of the key subject name (default empty) |
| CKA\_ENCRYPT <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports encryption <sup>9</sup> |
| CKA\_VERIFY <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports verification where the signature is an appendix to the data <sup>9</sup> |
| CKA\_VERIFY\_RECOVER <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports verification where the data is recovered from the signature <sup>9</sup> |
| CKA\_WRAP <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports wrapping (*i.e.*, can be used to wrap other keys) <sup>9</sup> |
| CKA\_TRUSTED <sup>10</sup> | CK\_BBOOL | The key can be trusted for the application that it was created.  The wrapping key can be used to wrap keys with CKA\_WRAP\_WITH\_TRUSTED set to CK\_TRUE. |
| CKA\_WRAP\_TEMPLATE | CK\_ATTRIBUTE\_PTR | For wrapping keys. The attribute template to match against any keys wrapped using this wrapping key. Keys that do not match cannot be wrapped. The number of attributes in the array is the *ulValueLen* component of the attribute divided by the size of CK\_ATTRIBUTE. |
| CKA\_PUBLIC\_KEY\_INFO | Byte array | DER-encoding of the SubjectPublicKeyInfo for this public key. (MAY be empty, DEFAULT derived from the underlying public key data) |

<sup>-</sup> Refer to Table 11 for footnotes

It is intended in the interests of interoperability that the subject name and key identifier for a public key will be the same as those for the corresponding certificate and private key. However, Cryptoki does not enforce this, and it is not required that the certificate and private key also be stored on the token.

To map between ISO/IEC 9594-8 (X.509) **keyUsage** flags for public keys and the PKCS #11 attributes for public keys, use the following table.

Table 25, Mapping of X.509 key usage flags to Cryptoki attributes for public keys

| **Key usage flags for public keys in X.509 public key certificates** | **Corresponding cryptoki attributes for public keys.** |
| --- | --- |
| dataEncipherment | CKA\_ENCRYPT |
| digitalSignature, keyCertSign, cRLSign | CKA\_VERIFY |
| digitalSignature, keyCertSign, cRLSign | CKA\_VERIFY\_RECOVER |
| keyAgreement | CKA\_DERIVE |
| keyEncipherment | CKA\_WRAP |
| nonRepudiation | CKA\_VERIFY |
| nonRepudiation | CKA\_VERIFY\_RECOVER |

The value of the CKA\_PUBLIC\_KEY\_INFO attribute is the DER encoded value of SubjectPublicKeyInfo:

SubjectPublicKeyInfo **::**\= SEQUENCE {

algorithm AlgorithmIdentifier,

subjectPublicKey BIT\_STRING }

The encodings for the subjectPublicKey field are specified in the description of the public key types in the appropriate \[PKCS11-Curr\]document for the key types defined within this specification.

## 4.9 Private key objects

Private key objects (object class **CKO\_PRIVATE\_KEY**) hold private keys. The following table defines the attributes common to all private keys, in addition to the common attributes defined for this object class:

Table 26, Common Private Key Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_SUBJECT <sup>8</sup> | Byte array | DER-encoding of certificate subject name (default empty) |
| CKA\_SENSITIVE <sup>8,11</sup> | CK\_BBOOL | CK\_TRUE if key is sensitive <sup>9</sup> |
| CKA\_DECRYPT <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports decryption <sup>9</sup> |
| CKA\_SIGN <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports signatures where the signature is an appendix to the data <sup>9</sup> |
| CKA\_SIGN\_RECOVER <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports signatures where the data can be recovered from the signature <sup>9</sup> |
| CKA\_UNWRAP <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports unwrapping (*i.e.*, can be used to unwrap other keys) <sup>9</sup> |
| CKA\_EXTRACTABLE <sup>8,12</sup> | CK\_BBOOL | CK\_TRUE if key is extractable and can be wrapped <sup>9</sup> |
| CKA\_ALWAYS\_SENSITIVE <sup>2,4,6</sup> | CK\_BBOOL | CK\_TRUE if key has *always* had the CKA\_SENSITIVE attribute set to CK\_TRUE |
| CKA\_NEVER\_EXTRACTABLE <sup>2,4,6</sup> | CK\_BBOOL | CK\_TRUE if key has *never* had the CKA\_EXTRACTABLE attribute set to CK\_TRUE |
| CKA\_WRAP\_WITH\_TRUSTED <sup>11</sup> | CK\_BBOOL | CK\_TRUE if the key can only be wrapped with a wrapping key that has CKA\_TRUSTED set to CK\_TRUE.  Default is CK\_FALSE. |
| CKA\_UNWRAP\_TEMPLATE | CK\_ATTRIBUTE\_PTR | For wrapping keys. The attribute template to apply to any keys unwrapped using this wrapping key. Any user supplied template is applied after this template as if the object has already been created. The number of attributes in the array is the *ulValueLen* component of the attribute divided by the size of  CK\_ATTRIBUTE. |
| CKA\_ALWAYS\_AUTHENTICATE | CK\_BBOOL | If CK\_TRUE, the user has to supply the PIN for each use (sign or decrypt) with the key. Default is CK\_FALSE. |
| CKA\_PUBLIC\_KEY\_INFO <sup>8</sup> | Byte Array | DER-encoding of the SubjectPublicKeyInfo for the associated public key (MAY be empty; DEFAULT derived from the underlying private key data; MAY be manually set for specific key types; if set; MUST be consistent with the underlying private key data) |

<sup>-</sup> Refer to Table 11 for footnotes

It is intended in the interests of interoperability that the subject name and key identifier for a private key will be the same as those for the corresponding certificate and public key. However, this is not enforced by Cryptoki, and it is not required that the certificate and public key also be stored on the token.

If the **CKA\_SENSITIVE** attribute is CK\_TRUE, or if the **CKA\_EXTRACTABLE** attribute is CK\_FALSE, then certain attributes of the private key cannot be revealed in plaintext outside the token. Which attributes these are is specified for each type of private key in the attribute table in the section describing that type of key.

The **CKA\_ALWAYS\_AUTHENTICATE** attribute can be used to force re-authentication (i.e. force the user to provide a PIN) for each use of a private key. “Use” in this case means a cryptographic operation such as sign or decrypt. This attribute may only be set to CK\_TRUE when **CKA\_PRIVATE** is also CK\_TRUE.

Re-authentication occurs by calling **C\_Login** with *userType* set to **CKU\_CONTEXT\_SPECIFIC** immediately after a cryptographic operation using the key has been initiated (e.g. after **C\_SignInit**). In this call, the actual user type is implicitly given by the usage requirements of the active key. If **C\_Login** returns CKR\_OK the user was successfully authenticated and this sets the active key in an authenticated state that lasts until the cryptographic operation has successfully or unsuccessfully been completed (e.g. by **C\_Sign**, **C\_SignFinal**,..). A return value CKR\_PIN\_INCORRECT from **C\_Login** means that the user was denied permission to use the key and continuing the cryptographic operation will result in a behavior as if **C\_Login** had not been called. In both of these cases the session state will remain the same, however repeated failed re-authentication attempts may cause the PIN to be locked. **C\_Login** returns in this case CKR\_PIN\_LOCKED and this also logs the user out from the token. Failing or omitting to re-authenticate when CKA\_ALWAYS\_AUTHENTICATE is set to CK\_TRUE will result in CKR\_USER\_NOT\_LOGGED\_IN to be returned from calls using the key. **C\_Login** will return CKR\_OPERATION\_NOT\_INITIALIZED, but the active cryptographic operation will not be affected, if an attempt is made to re-authenticate when CKA\_ALWAYS\_AUTHENTICATE is set to CK\_FALSE.

The **CKA\_PUBLIC\_KEY\_INFO** attribute represents the public key associated with this private key. The data it represents may either be stored as part of the private key data, or regenerated as needed from the private key.

If this attribute is supplied as part of a template for **C\_CreateObject, C\_CopyObject** or C **\_SetAttributeValue** for a private key, the token MUST verify correspondence between the private key data and the public key data as supplied in **CKA\_PUBLIC\_KEY\_INFO**. This can be done either by deriving a public key from the private key and comparing the values, or by doing a sign and verify operation. If there is a mismatch, the command SHALL return **CKR\_ATTRIBUTE\_VALUE\_INVALID.** A token MAY choose not to support the **CKA\_PUBLIC\_KEY\_INFO** attribute for commands which create new private keys. If it does not support the attribute, the command SHALL return **CKR\_ATTRIBUTE\_TYPE\_INVALID**.

As a general guideline, private keys of any type SHOULD store sufficient information to retrieve the public key information. In particular, the RSA private key description has been modified in <this version> to add the CKA\_PUBLIC\_EXPONENT to the list of attributes required for an RSA private key. All other private key types described in this specification contain sufficient information to recover the associated public key.

### 4.9.1 RSA private key objects

RSA private key objects (object class **CKO\_PRIVATE\_KEY,** key type **CKK\_RSA**) hold RSA private keys. The following table defines the RSA private key object attributes, in addition to the common attributes defined for this object class:

Table 27, RSA Private Key Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_MODULUS <sup>1,4,6</sup> | Big integer | Modulus *n* |
| CKA\_PUBLIC\_EXPONENT <sup>1,4,6</sup> | Big integer | Public exponent *e* |
| CKA\_PRIVATE\_EXPONENT <sup>1,4,6,7</sup> | Big integer | Private exponent *d* |
| CKA\_PRIME\_1 <sup>4,6,7</sup> | Big integer | Prime *p* |
| CKA\_PRIME\_2 <sup>4,6,7</sup> | Big integer | Prime *q* |
| CKA\_EXPONENT\_1 <sup>4,6,7</sup> | Big integer | Private exponent *d* modulo *p* -1 |
| CKA\_EXPONENT\_2 <sup>4,6,7</sup> | Big integer | Private exponent *d* modulo *q* -1 |
| CKA\_COEFFICIENT <sup>4,6,7</sup> | Big integer | CRT coefficient *q* <sup>-1</sup> mod *p* |

Refer to Table 11 for footnotes

Depending on the token, there may be limits on the length of the key components. See PKCS #1 for more information on RSA keys.

Tokens vary in what they actually store for RSA private keys. Some tokens store all of the above attributes, which can assist in performing rapid RSA computations. Other tokens might store only the **CKA\_MODULUS** and **CKA\_PRIVATE\_EXPONENT** values. Effective with version 2.40, tokens MUST also store CKA\_PUBLIC\_EXPONENT. This permits the retrieval of sufficient data to reconstitute the associated public key.

Because of this, Cryptoki is flexible in dealing with RSA private key objects. When a token generates an RSA private key, it stores whichever of the fields in Table 27 it keeps track of. Later, if an application asks for the values of the key’s various attributes, Cryptoki supplies values only for attributes whose values it can obtain (*i.e.*, if Cryptoki is asked for the value of an attribute it cannot obtain, the request fails). Note that a Cryptoki implementation may or may not be able and/or willing to supply various attributes of RSA private keys which are not actually stored on the token. *E.g.*, if a particular token stores values only for the **CKA\_PRIVATE\_EXPONENT, CKA\_PUBLIC\_EXPONENT**, **CKA\_PRIME\_1**, and **CKA\_PRIME\_2** attributes, then Cryptoki is certainly *able* to report values for all the attributes above (since they can all be computed efficiently from these four values). However, a Cryptoki implementation may or may not actually do this extra computation. The only attributes from Table 27 for which a Cryptoki implementation is *required* to be able to return values are **CKA\_MODULUS, CKA\_PRIVATE\_EXPONENT, and CKA\_PUBLIC\_EXPONENT**. A token SHOULD also be able to return **CKA\_PUBLIC\_KEY\_INFO** for an RSA private key. See the general guidance for Private Keys above.

## 4.10 Secret key objects

Secret key objects (object class **CKO\_SECRET\_KEY**) hold secret keys. The following table defines the attributes common to all secret keys, in addition to the common attributes defined for this object class:

Table 28, Common Secret Key Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_SENSITIVE <sup>8,11</sup> | CK\_BBOOL | CK\_TRUE if object is sensitive (default CK\_FALSE) |
| CKA\_ENCRYPT <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports encryption <sup>9</sup> |
| CKA\_DECRYPT <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports decryption <sup>9</sup> |
| CKA\_SIGN <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports signatures (*i.e.*, authentication codes) where the signature is an appendix to the data <sup>9</sup> |
| CKA\_VERIFY <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports verification (*i.e.*, of authentication codes) where the signature is an appendix to the data <sup>9</sup> |
| CKA\_WRAP <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports wrapping (*i.e.*, can be used to wrap other keys) <sup>9</sup> |
| CKA\_UNWRAP <sup>8</sup> | CK\_BBOOL | CK\_TRUE if key supports unwrapping (*i.e.*, can be used to unwrap other keys) <sup>9</sup> |
| CKA\_EXTRACTABLE <sup>8,12</sup> | CK\_BBOOL | CK\_TRUE if key is extractable and can be wrapped <sup>9</sup> |
| CKA\_ALWAYS\_SENSITIVE <sup>2,4,6</sup> | CK\_BBOOL | CK\_TRUE if key has *always* had the CKA\_SENSITIVE attribute set to CK\_TRUE |
| CKA\_NEVER\_EXTRACTABLE <sup>2,4,6</sup> | CK\_BBOOL | CK\_TRUE if key has *never* had the CKA\_EXTRACTABLE attribute set to CK\_TRUE |
| CKA\_CHECK\_VALUE | Byte array | Key checksum |
| CKA\_WRAP\_WITH\_TRUSTED <sup>11</sup> | CK\_BBOOL | CK\_TRUE if the key can only be wrapped with a wrapping key that has CKA\_TRUSTED set to CK\_TRUE.  Default is CK\_FALSE. |
| CKA\_TRUSTED <sup>10</sup> | CK\_BBOOL | The wrapping key can be used to wrap keys with CKA\_WRAP\_WITH\_TRUSTED set to CK\_TRUE. |
| CKA\_WRAP\_TEMPLATE | CK\_ATTRIBUTE\_PTR | For wrapping keys. The attribute template to match against any keys wrapped using this wrapping key. Keys that do not match cannot be wrapped. The number of attributes in the array is the  *ulValueLen* component of the attribute divided by the size of  CK\_ATTRIBUTE |
| CKA\_UNWRAP\_TEMPLATE | CK\_ATTRIBUTE\_PTR | For wrapping keys. The attribute template to apply to any keys unwrapped using this wrapping key. Any user supplied template is applied after this template as if the object has already been created. The number of attributes in the array is the *ulValueLen* component of the attribute divided by the size of  CK\_ATTRIBUTE. |

<sup>-</sup> Refer to Table 11 for footnotes

If the **CKA\_SENSITIVE** attribute is CK\_TRUE, or if the **CKA\_EXTRACTABLE** attribute is CK\_FALSE, then certain attributes of the secret key cannot be revealed in plaintext outside the token. Which attributes these are is specified for each type of secret key in the attribute table in the section describing that type of key.

The key check value (KCV) attribute for symmetric key objects to be called **CKA\_CHECK\_VALUE,** of type byte array, length 3 bytes, operates like a fingerprint, or checksum of the key. They are intended to be used to cross-check symmetric keys against other systems where the same key is shared, and as a validity check after manual key entry or restore from backup. Refer to object definitions of specific key types for KCV algorithms.

Properties:

1. For two keys that are cryptographically identical the value of this attribute should be identical.
2. CKA\_CHECK\_VALUE should not be usable to obtain any part of the key value.
3. Non-uniqueness. Two different keys can have the same CKA\_CHECK\_VALUE. This is unlikely (the probability can easily be calculated) but possible.

The attribute is optional, but if supported, regardless of how the key object is created or derived, the value of the attribute is always supplied. It SHALL be supplied even if the encryption operation for the key is forbidden (i.e. when CKA\_ENCRYPT is set to CK\_FALSE).

If a value is supplied in the application template (allowed but never necessary) then, if supported, it MUST match what the library calculates it to be or the library returns a CKR\_ATTRIBUTE\_VALUE\_INVALID. If the library does not support the attribute then it should ignore it. Allowing the attribute in the template this way does no harm and allows the attribute to be treated like any other attribute for the purposes of key wrap and unwrap where the attributes are preserved also.

The generation of the KCV may be prevented by the application supplying the attribute in the template as a no-value (0 length) entry. The application can query the value at any time like any other attribute using C\_GetAttributeValue. C\_SetAttributeValue may be used to destroy the attribute, by supplying no-value.

Unless otherwise specified for the object definition, the value of this attribute is derived from the key object by taking the first three bytes of an encryption of a single block of null (0x00) bytes, using the default cipher and mode (e.g. ECB) associated with the key type of the secret key object.

## 4.11 Domain parameter objects

### 4.11.1 Definitions

This section defines the object class CKO\_DOMAIN\_PARAMETERS for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.11.2 Overview

This object class was created to support the storage of certain algorithm's extended parameters. DSA and DH both use domain parameters in the key-pair generation step. In particular, some libraries support the generation of domain parameters (originally out of scope for PKCS11) so the object class was added.

To use a domain parameter object you MUST extract the attributes into a template and supply them (still in the template) to the corresponding key-pair generation function.

Domain parameter objects (object class **CKO\_DOMAIN\_PARAMETERS**) hold public domain parameters.

The following table defines the attributes common to domain parameter objects in addition to the common attributes defined for this object class:

Table 29, Common Domain Parameter Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_KEY\_TYPE <sup>1</sup> | CK\_KEY\_TYPE | Type of key the domain parameters can be used to generate. |
| CKA\_LOCAL <sup>2,4</sup> | CK\_BBOOL | CK\_TRUE only if domain parameters were either  · generated locally (*i.e.*, on the token) with a **C\_GenerateKey**  · created with a **C\_CopyObject** call as a copy of domain parameters which had its **CKA\_LOCAL** attribute set to CK\_TRUE |

<sup>-</sup> Refer to Table 11 for footnotes

The **CKA\_LOCAL** attribute has the value CK\_TRUE if and only if the values of the domain parameters were originally generated on the token by a **C\_GenerateKey** call.

## 4.12 Mechanism objects

### 4.12.1 Definitions

This section defines the object class CKO\_MECHANISM for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.12.2 Overview

Mechanism objects provide information about mechanisms supported by a device beyond that given by the **CK\_MECHANISM\_INFO** structure.

When searching for objects using **C\_FindObjectsInit** and **C\_FindObjects**, mechanism objects are not returned unless the **CKA\_CLASS** attribute in the template has the value **CKO\_MECHANISM**. This protects applications written to previous versions of Cryptoki from finding objects that they do not understand.

Table 30, Common Mechanism Attributes

| **Attribute** | **Data Type** | **Meaning** |
| --- | --- | --- |
| CKA\_MECHANISM\_TYPE | CK\_MECHANISM\_TYPE | The type of mechanism object |

The **CKA\_MECHANISM\_TYPE** attribute may not be set.

## 4.13 Profile objects

### 4.13.1 Definitions

This section defines the object class CKO\_PROFILE for type CK\_OBJECT\_CLASS as used in the CKA\_CLASS attribute of objects.

### 4.13.2 Overview

[[Profile]] objects (object class CKO\_PROFILE) describe which PKCS #11 profiles the token implements. [[Profile]]s are defined in the OASIS PKCS #11 Cryptographic Token Interface [[Profile]]s document. A given token can contain more than one profile ID. The following table lists the attributes supported by profile objects, in addition to the common attributes defined for this object class:

Table 31, [[Profile]] Object Attributes

| **Attribute** | **Data type** | **Meaning** |
| --- | --- | --- |
| CKA\_PROFILE\_ID | CK\_PROFILE\_ID | ID of the supported profile. |

The **CKA\_PROFILE\_ID** attribute identifies a profile that the token supports.

## 5 Functions

Cryptoki's functions are organized into the following categories:

· general-purpose functions (4 functions)

· slot and token management functions (9 functions)

· session management functions (8 functions)

· object management functions (9 functions)

· encryption functions (4 functions)

· message-based encryption functions (5 functions)

· decryption functions (4 functions)

· message digesting functions (5 functions)

· signing and MACing functions (6 functions)

· functions for verifying signatures and MACs (6 functions)

· dual-purpose cryptographic functions (4 functions)

· key management functions (5 functions)

· random number generation functions (2 functions)

· parallel function management functions (2 functions)

In addition to these functions, Cryptoki can use application-supplied callback functions to notify an application of certain events, and can also use application-supplied functions to handle mutex objects for safe multi-threaded library access.

The Cryptoki API functions are presented in the following table:

Table 32, Summary of Cryptoki Functions

<table><thead><tr><td width="116"><p><b>Category</b></p></td><td width="178"><p><b>Function</b></p></td><td width="288"><p><b>Description</b></p></td></tr></thead><tbody><tr><td width="116"><p>General</p></td><td width="178"><p>C_Initialize</p></td><td width="288"><p>initializes Cryptoki</p></td></tr><tr><td width="116"><p>purpose functions</p></td><td width="178"><p>C_Finalize</p></td><td width="288"><p>clean up miscellaneous Cryptoki-associated resources</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetInfo</p></td><td width="288"><p>obtains general information about Cryptoki</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetFunctionList</p></td><td width="288"><p>obtains entry points of Cryptoki library functions</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetInterfaceList</p></td><td width="288"><p>obtains list of interfaces supported by Cryptoki library</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetInterface</p></td><td width="288"><p>obtains interface specific entry points to Cryptoki library functions</p></td></tr><tr><td width="116"><p>Slot and token</p></td><td width="178"><p>C_GetSlotList</p></td><td width="288"><p>obtains a list of slots in the system</p></td></tr><tr><td width="116"><p>management</p></td><td width="178"><p>C_GetSlotInfo</p></td><td width="288"><p>obtains information about a particular slot</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_GetTokenInfo</p></td><td width="288"><p>obtains information about a particular token</p></td></tr><tr><td width="116"></td><td width="178"><p>C_WaitForSlotEvent</p></td><td width="288"><p>waits for a slot event (token insertion, removal, etc.) to occur</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetMechanismList</p></td><td width="288"><p>obtains a list of mechanisms supported by a token</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetMechanismInfo</p></td><td width="288"><p>obtains information about a particular mechanism</p></td></tr><tr><td width="116"></td><td width="178"><p>C_InitToken</p></td><td width="288"><p>initializes a token</p></td></tr><tr><td width="116"></td><td width="178"><p>C_InitPIN</p></td><td width="288"><p>initializes the normal user’s PIN</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SetPIN</p></td><td width="288"><p>modifies the PIN of the current user</p></td></tr><tr><td width="116"><p>Session management functions</p></td><td width="178"><p>C_OpenSession</p></td><td width="288"><p>opens a connection between an application and a particular token or sets up an application callback for token insertion</p></td></tr><tr><td width="116"></td><td width="178"><p>C_CloseSession</p></td><td width="288"><p>closes a session</p></td></tr><tr><td width="116"></td><td width="178"><p>C_CloseAllSessions</p></td><td width="288"><p>closes all sessions with a token</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetSessionInfo</p></td><td width="288"><p>obtains information about the session</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SessionCancel</p></td><td width="288"><p>terminates active session based operations</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetOperationState</p></td><td width="288"><p>obtains the cryptographic operations state of a session</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SetOperationState</p></td><td width="288"><p>sets the cryptographic operations state of a session</p></td></tr><tr><td width="116"></td><td width="178"><p>C_Login</p></td><td width="288"><p>logs into a token</p></td></tr><tr><td width="116"></td><td width="178"><p>C_LoginUser</p></td><td width="288"><p>logs into a token with explicit user name</p></td></tr><tr><td width="116"></td><td width="178"><p>C_Logout</p></td><td width="288"><p>logs out from a token</p></td></tr><tr><td width="116"><p>Object</p></td><td width="178"><p>C_CreateObject</p></td><td width="288"><p>creates an object</p></td></tr><tr><td width="116"><p>management</p></td><td width="178"><p>C_CopyObject</p></td><td width="288"><p>creates a copy of an object</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_DestroyObject</p></td><td width="288"><p>destroys an object</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetObjectSize</p></td><td width="288"><p>obtains the size of an object in bytes</p></td></tr><tr><td width="116"></td><td width="178"><p>C_GetAttributeValue</p></td><td width="288"><p>obtains an attribute value of an object</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SetAttributeValue</p></td><td width="288"><p>modifies an attribute value of an object</p></td></tr><tr><td width="116"></td><td width="178"><p>C_FindObjectsInit</p></td><td width="288"><p>initializes an object search operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_FindObjects</p></td><td width="288"><p>continues an object search operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_FindObjectsFinal</p></td><td width="288"><p>finishes an object search operation</p></td></tr><tr><td width="116"><p>Encryption</p></td><td width="178"><p>C_EncryptInit</p></td><td width="288"><p>initializes an encryption operation</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_Encrypt</p></td><td width="288"><p>encrypts single-part data</p></td></tr><tr><td width="116"></td><td width="178"><p>C_EncryptUpdate</p></td><td width="288"><p>continues a multiple-part encryption operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_EncryptFinal</p></td><td width="288"><p>finishes a multiple-part encryption operation</p></td></tr><tr><td width="116" rowspan="5"><p>Message-based Encryption Functions</p></td><td width="178"><p>C_MessageEncryptInit</p></td><td width="288"><p>initializes a message-based encryption process</p></td></tr><tr><td width="178"><p>C_EncryptMessage</p></td><td width="288"><p>encrypts a single-part message</p></td></tr><tr><td width="178"><p>C_EncryptMessageBegin</p></td><td width="288"><p>begins a multiple-part message encryption operation</p></td></tr><tr><td width="178"><p>C_EncryptMessageNext</p></td><td width="288"><p>continues or finishes a multiple-part message encryption operation</p></td></tr><tr><td width="178"><p>C_MessageEncryptFinal</p></td><td width="288"><p>finishes a message-based encryption process</p></td></tr><tr><td width="116"><p>Decryption</p></td><td width="178"><p>C_DecryptInit</p></td><td width="288"><p>initializes a decryption operation</p></td></tr><tr><td width="116"><p>Functions</p></td><td width="178"><p>C_Decrypt</p></td><td width="288"><p>decrypts single-part encrypted data</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DecryptUpdate</p></td><td width="288"><p>continues a multiple-part decryption operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DecryptFinal</p></td><td width="288"><p>finishes a multiple-part decryption operation</p></td></tr><tr><td width="116" rowspan="5"><p>Message-based</p><p>Decryption</p><p>Functions</p></td><td width="178"><p>C_MessageDecryptInit</p></td><td width="288"><p>initializes a message decryption operation</p></td></tr><tr><td width="178"><p>C_DecryptMessage</p></td><td width="288"><p>decrypts single-part data</p></td></tr><tr><td width="178"><p>C_DecryptMessageBegin</p></td><td width="288"><p>starts a multiple-part message decryption operation</p></td></tr><tr><td width="178"><p>C_DecryptMessageNext</p></td><td width="288"><p>Continues and finishes a multiple-part message decryption operation</p></td></tr><tr><td width="178"><p>C_MessageDecryptFinal</p></td><td width="288"><p>finishes a message decryption operation</p></td></tr><tr><td width="116"><p>Message</p></td><td width="178"><p>C_DigestInit</p></td><td width="288"><p>initializes a message-digesting operation</p></td></tr><tr><td width="116"><p><span>Digesting</span></p></td><td width="178"><p><span>C_Digest</span></p></td><td width="288"><p>digests single-part data</p></td></tr><tr><td width="116"><p>Functions</p></td><td width="178"><p>C_DigestUpdate</p></td><td width="288"><p>continues a multiple-part digesting operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DigestKey</p></td><td width="288"><p>digests a key</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DigestFinal</p></td><td width="288"><p>finishes a multiple-part digesting operation</p></td></tr><tr><td width="116"><p><span>Signing</span></p></td><td width="178"><p><span>C_SignInit</span></p></td><td width="288"><p>initializes a signature operation</p></td></tr><tr><td width="116"><p>and MACing</p></td><td width="178"><p>C_Sign</p></td><td width="288"><p>signs single-part data</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_SignUpdate</p></td><td width="288"><p>continues a multiple-part signature operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SignFinal</p></td><td width="288"><p>finishes a multiple-part signature operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SignRecoverInit</p></td><td width="288"><p>initializes a signature operation, where the data can be recovered from the signature</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SignRecover</p></td><td width="288"><p>signs single-part data, where the data can be recovered from the signature</p></td></tr><tr><td width="116" rowspan="5"><p>Message-based Signature functions</p></td><td width="178"><p>C_MessageSignInit</p></td><td width="288"><p>initializes a message signature operation</p></td></tr><tr><td width="178"><p>C_SignMessage</p></td><td width="288"><p>signs single-part data</p></td></tr><tr><td width="178"><p>C_SignMessageBegin</p></td><td width="288"><p>starts a multiple-part message signature operation</p></td></tr><tr><td width="178"><p>C_SignMessageNext</p></td><td width="288"><p>continues and finishes a multiple-part message signature operation</p></td></tr><tr><td width="178"><p>C_MessageSignFinal</p></td><td width="288"><p>finishes a message signature operation</p></td></tr><tr><td width="116"><p>Functions for verifying</p></td><td width="178"><p>C_VerifyInit</p></td><td width="288"><p>initializes a verification operation</p></td></tr><tr><td width="116"><p>signatures</p></td><td width="178"><p>C_Verify</p></td><td width="288"><p>verifies a signature on single-part data</p></td></tr><tr><td width="116"><p>and MACs</p></td><td width="178"><p>C_VerifyUpdate</p></td><td width="288"><p>continues a multiple-part verification operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_VerifyFinal</p></td><td width="288"><p>finishes a multiple-part verification operation</p></td></tr><tr><td width="116"></td><td width="178"><p>C_VerifyRecoverInit</p></td><td width="288"><p>initializes a verification operation where the data is recovered from the signature</p></td></tr><tr><td width="116"></td><td width="178"><p>C_VerifyRecover</p></td><td width="288"><p>verifies a signature on single-part data, where the data is recovered from the signature</p></td></tr><tr><td width="116" rowspan="5"><p>Message-based Functions for verifying signatures and MACs</p></td><td width="178"><p>C_MessageVerifyInit</p></td><td width="288"><p>initializes a message verification operation</p></td></tr><tr><td width="178"><p>C_VerifyMessage</p></td><td width="288"><p>verifies single-part data</p></td></tr><tr><td width="178"><p>C_VerifyMessageBegin</p></td><td width="288"><p>starts a multiple-part message verification operation</p></td></tr><tr><td width="178"><p>C_VerifyMessageNext</p></td><td width="288"><p>continues and finishes a multiple-part message verification operation</p></td></tr><tr><td width="178"><p>C_MessageVerifyFinal</p></td><td width="288"><p>finishes a message verification operation</p></td></tr><tr><td width="116"><p>Dual-purpose cryptographic</p></td><td width="178"><p>C_DigestEncryptUpdate</p></td><td width="288"><p>continues simultaneous multiple-part digesting and encryption operations</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_DecryptDigestUpdate</p></td><td width="288"><p>continues simultaneous multiple-part decryption and digesting operations</p></td></tr><tr><td width="116"></td><td width="178"><p>C_SignEncryptUpdate</p></td><td width="288"><p>continues simultaneous multiple-part signature and encryption operations</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DecryptVerifyUpdate</p></td><td width="288"><p>continues simultaneous multiple-part decryption and verification operations</p></td></tr><tr><td width="116"><p>Key</p></td><td width="178"><p>C_GenerateKey</p></td><td width="288"><p>generates a secret key</p></td></tr><tr><td width="116"><p>management</p></td><td width="178"><p>C_GenerateKeyPair</p></td><td width="288"><p>generates a public-key/private-key pair</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_WrapKey</p></td><td width="288"><p>wraps (encrypts) a key</p></td></tr><tr><td width="116"></td><td width="178"><p>C_UnwrapKey</p></td><td width="288"><p>unwraps (decrypts) a key</p></td></tr><tr><td width="116"></td><td width="178"><p>C_DeriveKey</p></td><td width="288"><p>derives a key from a base key</p></td></tr><tr><td width="116"><p><span>Random number generation</span></p></td><td width="178"><p>C_SeedRandom</p></td><td width="288"><p>mixes in additional seed material to the random number generator</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_GenerateRandom</p></td><td width="288"><p>generates random data</p></td></tr><tr><td width="116"><p>Parallel function management</p></td><td width="178"><p>C_GetFunctionStatus</p></td><td width="288"><p>legacy function which always returns CKR_FUNCTION_NOT_PARALLEL</p></td></tr><tr><td width="116"><p>functions</p></td><td width="178"><p>C_CancelFunction</p></td><td width="288"><p>legacy function which always returns CKR_FUNCTION_NOT_PARALLEL</p></td></tr><tr><td width="116"><p>Callback function</p></td><td width="178"></td><td width="288"><p>application-supplied function to process notifications from Cryptoki</p></td></tr></tbody></table>

Execution of a Cryptoki function call is in general an all-or-nothing affair, *i.e.*, a function call accomplishes either its entire goal, or nothing at all.

· If a Cryptoki function executes successfully, it returns the value CKR\_OK.

· If a Cryptoki function does not execute successfully, it returns some value other than CKR\_OK, and the token is in the same state as it was in prior to the function call. If the function call was supposed to modify the contents of certain memory addresses on the host computer, these memory addresses may have been modified, despite the failure of the function.

· In unusual (and extremely unpleasant!) circumstances, a function can fail with the return value CKR\_GENERAL\_ERROR. When this happens, the token and/or host computer may be in an inconsistent state, and the goals of the function may have been partially achieved.

There are a small number of Cryptoki functions whose return values do not behave precisely as described above; these exceptions are documented individually with the description of the functions themselves.

A Cryptoki library need not support every function in the Cryptoki API. However, even an unsupported function MUST have a “stub” in the library which simply returns the value CKR\_FUNCTION\_NOT\_SUPPORTED. The function’s entry in the library’s **CK\_FUNCTION\_LIST** structure (as obtained by **C\_GetFunctionList**) should point to this stub function (see Section 3.6).

## 5.1 Function return values

The Cryptoki interface possesses a large number of functions and return values. In Section 5.1, we enumerate the various possible return values for Cryptoki functions; most of the remainder of Section 5.1 details the behavior of Cryptoki functions, including what values each of them may return.

Because of the complexity of the Cryptoki specification, it is recommended that Cryptoki applications attempt to give some leeway when interpreting Cryptoki functions’ return values. We have attempted to specify the behavior of Cryptoki functions as completely as was feasible; nevertheless, there are presumably some gaps. For example, it is possible that a particular error code which might apply to a particular Cryptoki function is unfortunately not actually listed in the description of that function as a possible error code. It is conceivable that the developer of a Cryptoki library might nevertheless permit his/her implementation of that function to return that error code. It would clearly be somewhat ungraceful if a Cryptoki application using that library were to terminate by abruptly dumping core upon receiving that error code for that function. It would be far preferable for the application to examine the function’s return value, see that it indicates some sort of error (even if the application doesn’t know precisely *what* kind of error), and behave accordingly.

See Section 5.1.8 for some specific details on how a developer might attempt to make an application that accommodates a range of behaviors from Cryptoki libraries.

### 5.1.1 Universal Cryptoki function return values

Any Cryptoki function can return any of the following values:

· CKR\_GENERAL\_ERROR: Some horrible, unrecoverable error has occurred. In the worst case, it is possible that the function only partially succeeded, and that the computer and/or token is in an inconsistent state.

· CKR\_HOST\_MEMORY: The computer that the Cryptoki library is running on has insufficient memory to perform the requested function.

· CKR\_FUNCTION\_FAILED: The requested function could not be performed, but detailed information about why not is not available in this error return. If the failed function uses a session, it is possible that the **CK\_SESSION\_INFO** structure that can be obtained by calling **C\_GetSessionInfo** will hold useful information about what happened in its *ulDeviceError* field. In any event, although the function call failed, the situation is not necessarily totally hopeless, as it is likely to be when CKR\_GENERAL\_ERROR is returned. Depending on what the root cause of the error actually was, it is possible that an attempt to make the exact same function call again would succeed.

· CKR\_OK: The function executed successfully. Technically, CKR\_OK is not *quite* a “universal” return value; in particular, the legacy functions **C\_GetFunctionStatus** and **C\_CancelFunction** (see Section 5.20) cannot return CKR\_OK.

The relative priorities of these errors are in the order listed above, *e.g.*, if either of CKR\_GENERAL\_ERROR or CKR\_HOST\_MEMORY would be an appropriate error return, then CKR\_GENERAL\_ERROR should be returned.

### 5.1.2 Cryptoki function return values for functions that use a session handle

Any Cryptoki function that takes a session handle as one of its arguments (i.e., any Cryptoki function except for C\_Initialize, C\_Finalize, C\_GetInfo, C\_GetFunctionList, C\_GetSlotList, C\_GetSlotInfo, C\_GetTokenInfo, C\_WaitForSlotEvent, C\_GetMechanismList, C\_GetMechanismInfo, C\_InitToken, C\_OpenSession, and C\_CloseAllSessions) can return the following values:

· CKR\_SESSION\_HANDLE\_INVALID: The specified session handle was invalid *at the time that the function was invoked*. Note that this can happen if the session’s token is removed before the function invocation, since removing a token closes all sessions with it.

· CKR\_DEVICE\_REMOVED: The token was removed from its slot *during the execution of the function*.

· CKR\_SESSION\_CLOSED: The session was closed *during the execution of the function*. Note that, as stated in **\[PKCS11-UG\]**, the behavior of Cryptoki is *undefined* if multiple threads of an application attempt to access a common Cryptoki session simultaneously. Therefore, there is actually no guarantee that a function invocation could ever return the value CKR\_SESSION\_CLOSED. An example of multiple threads accessing a common session simultaneously is where one thread is using a session when another thread closes that same session.

The relative priorities of these errors are in the order listed above, *e.g.*, if either of CKR\_SESSION\_HANDLE\_INVALID or CKR\_DEVICE\_REMOVED would be an appropriate error return, then CKR\_SESSION\_HANDLE\_INVALID should be returned.

In practice, it is often not crucial (or possible) for a Cryptoki library to be able to make a distinction between a token being removed *before* a function invocation and a token being removed *during* a function execution.

### 5.1.3 Cryptoki function return values for functions that use a token

Any Cryptoki function that uses a particular token (*i.e.*, any Cryptoki function except for **C\_Initialize**, **C\_Finalize**, **C\_GetInfo**, **C\_GetFunctionList**, **C\_GetSlotList**, **C\_GetSlotInfo**, or **C\_WaitForSlotEvent**) can return any of the following values:

· CKR\_DEVICE\_MEMORY: The token does not have sufficient memory to perform the requested function.

· CKR\_DEVICE\_ERROR: Some problem has occurred with the token and/or slot. This error code can be returned by more than just the functions mentioned above; in particular, it is possible for **C\_GetSlotInfo** to return CKR\_DEVICE\_ERROR.

· CKR\_TOKEN\_NOT\_PRESENT: The token was not present in its slot *at the time that the function was invoked*.

· CKR\_DEVICE\_REMOVED: The token was removed from its slot *during the execution of the function*.

The relative priorities of these errors are in the order listed above, *e.g.*, if either of CKR\_DEVICE\_MEMORY or CKR\_DEVICE\_ERROR would be an appropriate error return, then CKR\_DEVICE\_MEMORY should be returned.

In practice, it is often not critical (or possible) for a Cryptoki library to be able to make a distinction between a token being removed *before* a function invocation and a token being removed *during* a function execution.

### 5.1.4 Special return value for application-supplied callbacks

There is a special-purpose return value which is not returned by any function in the actual Cryptoki API, but which may be returned by an application-supplied callback function. It is:

· CKR\_CANCEL: When a function executing in serial with an application decides to give the application a chance to do some work, it calls an application-supplied function with a CKN\_SURRENDER callback (see Section 5.21). If the callback returns the value CKR\_CANCEL, then the function aborts and returns CKR\_FUNCTION\_CANCELED.

### 5.1.5 Special return values for mutex-handling functions

There are two other special-purpose return values which are not returned by any actual Cryptoki functions. These values may be returned by application-supplied mutex-handling functions, and they may safely be ignored by application developers who are not using their own threading model. They are:

· CKR\_MUTEX\_BAD: This error code can be returned by mutex-handling functions that are passed a bad mutex object as an argument. Unfortunately, it is possible for such a function not to recognize a bad mutex object. There is therefore no guarantee that such a function will successfully detect bad mutex objects and return this value.

· CKR\_MUTEX\_NOT\_LOCKED: This error code can be returned by mutex-unlocking functions. It indicates that the mutex supplied to the mutex-unlocking function was not locked.

### 5.1.6 All other Cryptoki function return values

Descriptions of the other Cryptoki function return values follow. Except as mentioned in the descriptions of particular error codes, there are in general no particular priorities among the errors listed below, *i.e.*, if more than one error code might apply to an execution of a function, then the function may return any applicable error code.

· CKR\_ACTION\_PROHIBITED: This value can only be returned by C\_CopyObject, C\_SetAttributeValue and C\_DestroyObject. It denotes that the action may not be taken, either because of underlying policy restrictions on the token, or because the object has the relevant CKA\_COPYABLE, CKA\_MODIFIABLE or CKA\_DESTROYABLE policy attribute set to CK\_FALSE.

· CKR\_ARGUMENTS\_BAD: This is a rather generic error code which indicates that the arguments supplied to the Cryptoki function were in some way not appropriate.

· CKR\_ATTRIBUTE\_READ\_ONLY: An attempt was made to set a value for an attribute which may not be set by the application, or which may not be modified by the application. See Section 4.1 for more information.

· CKR\_ATTRIBUTE\_SENSITIVE: An attempt was made to obtain the value of an attribute of an object which cannot be satisfied because the object is either sensitive or un-extractable.

· CKR\_ATTRIBUTE\_TYPE\_INVALID: An invalid attribute type was specified in a template. See Section 4.1 for more information.

· CKR\_ATTRIBUTE\_VALUE\_INVALID: An invalid value was specified for a particular attribute in a template. See Section 4.1 for more information.

· CKR\_BUFFER\_TOO\_SMALL: The output of the function is too large to fit in the supplied buffer.

· CKR\_CANT\_LOCK: This value can only be returned by **C\_Initialize**. It means that the type of locking requested by the application for thread-safety is not available in this library, and so the application cannot make use of this library in the specified fashion.

· CKR\_CRYPTOKI\_ALREADY\_INITIALIZED: This value can only be returned by **C\_Initialize**. It means that the Cryptoki library has already been initialized (by a previous call to **C\_Initialize** which did not have a matching **C\_Finalize** call).

· CKR\_CRYPTOKI\_NOT\_INITIALIZED: This value can be returned by any function other than **C\_Initialize,** **C\_GetFunctionList, C\_GetInterfaceList** and **C\_GetInterface**. It indicates that the function cannot be executed because the Cryptoki library has not yet been initialized by a call to **C\_Initialize**.

· CKR\_CURVE\_NOT\_SUPPORTED: This curve is not supported by this token. Used with Elliptic Curve mechanisms.

· CKR\_DATA\_INVALID: The plaintext input data to a cryptographic operation is invalid. This return value has lower priority than CKR\_DATA\_LEN\_RANGE.

· CKR\_DATA\_LEN\_RANGE: The plaintext input data to a cryptographic operation has a bad length. Depending on the operation’s mechanism, this could mean that the plaintext data is too short, too long, or is not a multiple of some particular block size. This return value has higher priority than CKR\_DATA\_INVALID.

· CKR\_DOMAIN\_PARAMS\_INVALID: Invalid or unsupported domain parameters were supplied to the function. Which representation methods of domain parameters are supported by a given mechanism can vary from token to token.

· CKR\_ENCRYPTED\_DATA\_INVALID: The encrypted input to a decryption operation has been determined to be invalid ciphertext. This return value has lower priority than CKR\_ENCRYPTED\_DATA\_LEN\_RANGE.

· CKR\_ENCRYPTED\_DATA\_LEN\_RANGE: The ciphertext input to a decryption operation has been determined to be invalid ciphertext solely on the basis of its length. Depending on the operation’s mechanism, this could mean that the ciphertext is too short, too long, or is not a multiple of some particular block size. This return value has higher priority than CKR\_ENCRYPTED\_DATA\_INVALID.

· CKR\_EXCEEDED\_MAX\_ITERATIONS: An iterative algorithm (for key pair generation, domain parameter generation etc.) failed because we have exceeded the maximum number of iterations. This error code has precedence over CKR\_FUNCTION\_FAILED. Examples of iterative algorithms include DSA signature generation (retry if either r = 0 or s = 0) and generation of DSA primes p and q specified in FIPS 186-4.

· CKR\_FIPS\_SELF\_TEST\_FAILED: A FIPS 140-2 power-up self-test or conditional self-test failed. The token entered an error state. Future calls to cryptographic functions on the token will return CKR\_GENERAL\_ERROR. CKR\_FIPS\_SELF\_TEST\_FAILED has a higher precedence over CKR\_GENERAL\_ERROR. This error may be returned by C\_Initialize, if a power-up self-test failed, by C\_GenerateRandom or C\_SeedRandom, if the continuous random number generator test failed, or by C\_GenerateKeyPair, if the pair-wise consistency test failed.

· CKR\_FUNCTION\_CANCELED: The function was canceled in mid-execution. This happens to a cryptographic function if the function makes a **CKN\_SURRENDER** application callback which returns CKR\_CANCEL (see CKR\_CANCEL). It also happens to a function that performs PIN entry through a protected path. The method used to cancel a protected path PIN entry operation is device dependent.

· CKR\_FUNCTION\_NOT\_PARALLEL: There is currently no function executing in parallel in the specified session. This is a legacy error code which is only returned by the legacy functions **C\_GetFunctionStatus** and **C\_CancelFunction**.

· CKR\_FUNCTION\_NOT\_SUPPORTED: The requested function is not supported by this Cryptoki library. Even unsupported functions in the Cryptoki API should have a “stub” in the library; this stub should simply return the value CKR\_FUNCTION\_NOT\_SUPPORTED.

· CKR\_FUNCTION\_REJECTED: The signature request is rejected by the user.

· CKR\_INFORMATION\_SENSITIVE: The information requested could not be obtained because the token considers it sensitive, and is not able or willing to reveal it.

· CKR\_KEY\_CHANGED: This value is only returned by **C\_SetOperationState**. It indicates that one of the keys specified is not the same key that was being used in the original saved session.

· CKR\_KEY\_FUNCTION\_NOT\_PERMITTED: An attempt has been made to use a key for a cryptographic purpose that the key’s attributes are not set to allow it to do. For example, to use a key for performing encryption, that key MUST have its **CKA\_ENCRYPT** attribute set to CK\_TRUE (the fact that the key MUST have a **CKA\_ENCRYPT** attribute implies that the key cannot be a private key). This return value has lower priority than CKR\_KEY\_TYPE\_INCONSISTENT.

· CKR\_KEY\_HANDLE\_INVALID: The specified key handle is not valid. It may be the case that the specified handle is a valid handle for an object which is not a key. We reiterate here that 0 is never a valid key handle.

· CKR\_KEY\_INDIGESTIBLE: This error code can only be returned by **C\_DigestKey**. It indicates that the value of the specified key cannot be digested for some reason (perhaps the key isn’t a secret key, or perhaps the token simply can’t digest this kind of key).

· CKR\_KEY\_NEEDED: This value is only returned by **C\_SetOperationState**. It indicates that the session state cannot be restored because **C\_SetOperationState** needs to be supplied with one or more keys that were being used in the original saved session.

· CKR\_KEY\_NOT\_NEEDED: An extraneous key was supplied to **C\_SetOperationState**. For example, an attempt was made to restore a session that had been performing a message digesting operation, and an encryption key was supplied.

· CKR\_KEY\_NOT\_WRAPPABLE: Although the specified private or secret key does not have its CKA\_EXTRACTABLE attribute set to CK\_FALSE, Cryptoki (or the token) is unable to wrap the key as requested (possibly the token can only wrap a given key with certain types of keys, and the wrapping key specified is not one of these types). Compare with CKR\_KEY\_UNEXTRACTABLE.

· CKR\_KEY\_SIZE\_RANGE: Although the requested keyed cryptographic operation could in principle be carried out, this Cryptoki library (or the token) is unable to actually do it because the supplied key‘s size is outside the range of key sizes that it can handle.

· CKR\_KEY\_TYPE\_INCONSISTENT: The specified key is not the correct type of key to use with the specified mechanism. This return value has a higher priority than CKR\_KEY\_FUNCTION\_NOT\_PERMITTED.

· CKR\_KEY\_UNEXTRACTABLE: The specified private or secret key can’t be wrapped because its CKA\_EXTRACTABLE attribute is set to CK\_FALSE. Compare with CKR\_KEY\_NOT\_WRAPPABLE.

· CKR\_LIBRARY\_LOAD\_FAILED: The Cryptoki library could not load a dependent shared library.

· CKR\_MECHANISM\_INVALID: An invalid mechanism was specified to the cryptographic operation. This error code is an appropriate return value if an unknown mechanism was specified or if the mechanism specified cannot be used in the selected token with the selected function.

· CKR\_MECHANISM\_PARAM\_INVALID: Invalid parameters were supplied to the mechanism specified to the cryptographic operation. Which parameter values are supported by a given mechanism can vary from token to token.

· CKR\_NEED\_TO\_CREATE\_THREADS: This value can only be returned by **C\_Initialize**. It is returned when two conditions hold:

1. The application called **C\_Initialize** in a way which tells the Cryptoki library that application threads executing calls to the library cannot use native operating system methods to spawn new threads.
2. The library cannot function properly without being able to spawn new threads in the above fashion.

· CKR\_NO\_EVENT: This value can only be returned by **C\_WaitForSlotEvent**. It is returned when **C\_WaitForSlotEvent** is called in non-blocking mode and there are no new slot events to return.

· CKR\_OBJECT\_HANDLE\_INVALID: The specified object handle is not valid. We reiterate here that 0 is never a valid object handle.

· CKR\_OPERATION\_ACTIVE: There is already an active operation (or combination of active operations) which prevents Cryptoki from activating the specified operation. For example, an active object-searching operation would prevent Cryptoki from activating an encryption operation with **C\_EncryptInit**. Or, an active digesting operation and an active encryption operation would prevent Cryptoki from activating a signature operation. Or, on a token which doesn’t support simultaneous dual cryptographic operations in a session (see the description of the **CKF\_DUAL\_CRYPTO\_OPERATIONS** flag in the **CK\_TOKEN\_INFO** structure), an active signature operation would prevent Cryptoki from activating an encryption operation.

· CKR\_OPERATION\_NOT\_INITIALIZED: There is no active operation of an appropriate type in the specified session. For example, an application cannot call **C\_Encrypt** in a session without having called **C\_EncryptInit** first to activate an encryption operation.

· CKR\_PIN\_EXPIRED: The specified PIN has expired, and the requested operation cannot be carried out unless C\_SetPIN is called to change the PIN value. Whether or not the normal user’s PIN on a token ever expires varies from token to token.

· CKR\_PIN\_INCORRECT: The specified PIN is incorrect, *i.e.*, does not match the PIN stored on the token. More generally-- when authentication to the token involves something other than a PIN-- the attempt to authenticate the user has failed.

· CKR\_PIN\_INVALID: The specified PIN has invalid characters in it. This return code only applies to functions which attempt to set a PIN.

· CKR\_PIN\_LEN\_RANGE: The specified PIN is too long or too short. This return code only applies to functions which attempt to set a PIN.

· CKR\_PIN\_LOCKED: The specified PIN is “locked”, and cannot be used. That is, because some particular number of failed authentication attempts has been reached, the token is unwilling to permit further attempts at authentication. Depending on the token, the specified PIN may or may not remain locked indefinitely.

· CKR\_PIN\_TOO\_WEAK: The specified PIN is too weak so that it could be easy to guess. If the PIN is too short, CKR\_PIN\_LEN\_RANGE should be returned instead. This return code only applies to functions which attempt to set a PIN.

· CKR\_PUBLIC\_KEY\_INVALID: The public key fails a public key validation. For example, an EC public key fails the public key validation specified in Section 5.2.2 of ANSI X9.62. This error code may be returned by C\_CreateObject, when the public key is created, or by C\_VerifyInit or C\_VerifyRecoverInit, when the public key is used. It may also be returned by C\_DeriveKey, in preference to CKR\_MECHANISM\_PARAM\_INVALID, if the other party's public key specified in the mechanism's parameters is invalid.

· CKR\_RANDOM\_NO\_RNG: This value can be returned by **C\_SeedRandom** and **C\_GenerateRandom**. It indicates that the specified token doesn’t have a random number generator. This return value has higher priority than CKR\_RANDOM\_SEED\_NOT\_SUPPORTED.

· CKR\_RANDOM\_SEED\_NOT\_SUPPORTED: This value can only be returned by **C\_SeedRandom**. It indicates that the token’s random number generator does not accept seeding from an application. This return value has lower priority than CKR\_RANDOM\_NO\_RNG.

· CKR\_SAVED\_STATE\_INVALID: This value can only be returned by **C\_SetOperationState**. It indicates that the supplied saved cryptographic operations state is invalid, and so it cannot be restored to the specified session.

· CKR\_SESSION\_COUNT: This value can only be returned by **C\_OpenSession**. It indicates that the attempt to open a session failed, either because the token has too many sessions already open, or because the token has too many read/write sessions already open.

· CKR\_SESSION\_EXISTS: This value can only be returned by **C\_InitToken**. It indicates that a session with the token is already open, and so the token cannot be initialized.

· CKR\_SESSION\_PARALLEL\_NOT\_SUPPORTED: The specified token does not support parallel sessions. This is a legacy error code—in Cryptoki Version 2.01 and up, *no* token supports parallel sessions. CKR\_SESSION\_PARALLEL\_NOT\_SUPPORTED can only be returned by **C\_OpenSession**, and it is only returned when **C\_OpenSession** is called in a particular \[deprecated\] way.

· CKR\_SESSION\_READ\_ONLY: The specified session was unable to accomplish the desired action because it is a read-only session. This return value has lower priority than CKR\_TOKEN\_WRITE\_PROTECTED.

· CKR\_SESSION\_READ\_ONLY\_EXISTS: A read-only session already exists, and so the SO cannot be logged in.

· CKR\_SESSION\_READ\_WRITE\_SO\_EXISTS: A read/write SO session already exists, and so a read-only session cannot be opened.

· CKR\_SIGNATURE\_LEN\_RANGE: The provided signature/MAC can be seen to be invalid solely on the basis of its length. This return value has higher priority than CKR\_SIGNATURE\_INVALID.

· CKR\_SIGNATURE\_INVALID: The provided signature/MAC is invalid. This return value has lower priority than CKR\_SIGNATURE\_LEN\_RANGE.

· CKR\_SLOT\_ID\_INVALID: The specified slot ID is not valid.

· CKR\_STATE\_UNSAVEABLE: The cryptographic operations state of the specified session cannot be saved for some reason (possibly the token is simply unable to save the current state). This return value has lower priority than CKR\_OPERATION\_NOT\_INITIALIZED.

· CKR\_TEMPLATE\_INCOMPLETE: The template specified for creating an object is incomplete, and lacks some necessary attributes. See Section 4.1 for more information.

· CKR\_TEMPLATE\_INCONSISTENT: The template specified for creating an object has conflicting attributes. See Section 4.1 for more information.

· CKR\_TOKEN\_NOT\_RECOGNIZED: The Cryptoki library and/or slot does not recognize the token in the slot.

· CKR\_TOKEN\_WRITE\_PROTECTED: The requested action could not be performed because the token is write-protected. This return value has higher priority than CKR\_SESSION\_READ\_ONLY.

· CKR\_UNWRAPPING\_KEY\_HANDLE\_INVALID: This value can only be returned by **C\_UnwrapKey**. It indicates that the key handle specified to be used to unwrap another key is not valid.

· CKR\_UNWRAPPING\_KEY\_SIZE\_RANGE: This value can only be returned by **C\_UnwrapKey**. It indicates that although the requested unwrapping operation could in principle be carried out, this Cryptoki library (or the token) is unable to actually do it because the supplied key’s size is outside the range of key sizes that it can handle.

· CKR\_UNWRAPPING\_KEY\_TYPE\_INCONSISTENT: This value can only be returned by **C\_UnwrapKey**. It indicates that the type of the key specified to unwrap another key is not consistent with the mechanism specified for unwrapping.

· CKR\_USER\_ALREADY\_LOGGED\_IN: This value can only be returned by **C\_Login**. It indicates that the specified user cannot be logged into the session, because it is already logged into the session. For example, if an application has an open SO session, and it attempts to log the SO into it, it will receive this error code.

· CKR\_USER\_ANOTHER\_ALREADY\_LOGGED\_IN: This value can only be returned by **C\_Login**. It indicates that the specified user cannot be logged into the session, because another user is already logged into the session. For example, if an application has an open SO session, and it attempts to log the normal user into it, it will receive this error code.

· CKR\_USER\_NOT\_LOGGED\_IN: The desired action cannot be performed because the appropriate user (or *an* appropriate user) is not logged in. One example is that a session cannot be logged out unless it is logged in. Another example is that a private object cannot be created on a token unless the session attempting to create it is logged in as the normal user. A final example is that cryptographic operations on certain tokens cannot be performed unless the normal user is logged in.

· CKR\_USER\_PIN\_NOT\_INITIALIZED: This value can only be returned by **C\_Login**. It indicates that the normal user’s PIN has not yet been initialized with **C\_InitPIN**.

· CKR\_USER\_TOO\_MANY\_TYPES: An attempt was made to have more distinct users simultaneously logged into the token than the token and/or library permits. For example, if some application has an open SO session, and another application attempts to log the normal user into a session, the attempt may return this error. It is not required to, however. Only if the simultaneous distinct users cannot be supported does **C\_Login** have to return this value. Note that this error code generalizes to true multi-user tokens.

· CKR\_USER\_TYPE\_INVALID: An invalid value was specified as a **CK\_USER\_TYPE**. Valid types are **CKU\_SO**, **CKU\_USER**, and **CKU\_CONTEXT\_SPECIFIC**.

· CKR\_WRAPPED\_KEY\_INVALID: This value can only be returned by **C\_UnwrapKey**. It indicates that the provided wrapped key is not valid. If a call is made to **C\_UnwrapKey** to unwrap a particular type of key (*i.e.*, some particular key type is specified in the template provided to **C\_UnwrapKey**), and the wrapped key provided to **C\_UnwrapKey** is recognizably not a wrapped key of the proper type, then **C\_UnwrapKey** should return CKR\_WRAPPED\_KEY\_INVALID. This return value has lower priority than CKR\_WRAPPED\_KEY\_LEN\_RANGE.

· CKR\_WRAPPED\_KEY\_LEN\_RANGE: This value can only be returned by **C\_UnwrapKey**. It indicates that the provided wrapped key can be seen to be invalid solely on the basis of its length. This return value has higher priority than CKR\_WRAPPED\_KEY\_INVALID.

· CKR\_WRAPPING\_KEY\_HANDLE\_INVALID: This value can only be returned by **C\_WrapKey**. It indicates that the key handle specified to be used to wrap another key is not valid.

· CKR\_WRAPPING\_KEY\_SIZE\_RANGE: This value can only be returned by **C\_WrapKey**. It indicates that although the requested wrapping operation could in principle be carried out, this Cryptoki library (or the token) is unable to actually do it because the supplied wrapping key’s size is outside the range of key sizes that it can handle.

· CKR\_WRAPPING\_KEY\_TYPE\_INCONSISTENT: This value can only be returned by **C\_WrapKey**. It indicates that the type of the key specified to wrap another key is not consistent with the mechanism specified for wrapping.

· CKR\_OPERATION\_CANCEL\_FAILED: This value can only be returned by **C\_SessionCancel**. It means that one or more of the requested operations could not be cancelled for implementation or vendor-specific reasons.

### 5.1.7 More on relative priorities of Cryptoki errors

In general, when a Cryptoki call is made, error codes from Section 5.1.1 (other than CKR\_OK) take precedence over error codes from Section 5.1.2, which take precedence over error codes from Section 5.1.3, which take precedence over error codes from Section 5.1.6. One minor implication of this is that functions that use a session handle (*i.e.*, *most* functions!) never return the error code CKR\_TOKEN\_NOT\_PRESENT (they return CKR\_SESSION\_HANDLE\_INVALID instead). Other than these precedences, if more than one error code applies to the result of a Cryptoki call, any of the applicable error codes may be returned. Exceptions to this rule will be explicitly mentioned in the descriptions of functions.

### 5.1.8 Error code “gotchas”

Here is a short list of a few particular things about return values that Cryptoki developers might want to be aware of:

1\. As mentioned in Sections 5.1.2 and 5.1.3, a Cryptoki library may not be able to make a distinction between a token being removed *before* a function invocation and a token being removed *during* a function invocation.

2\. As mentioned in Section 5.1.2, an application should never count on getting a CKR\_SESSION\_CLOSED error.

3\. The difference between CKR\_DATA\_INVALID and CKR\_DATA\_LEN\_RANGE can be somewhat subtle. Unless an application *needs* to be able to distinguish between these return values, it is best to always treat them equivalently.

4\. Similarly, the difference between CKR\_ENCRYPTED\_DATA\_INVALID and CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, and between CKR\_WRAPPED\_KEY\_INVALID and CKR\_WRAPPED\_KEY\_LEN\_RANGE, can be subtle, and it may be best to treat these return values equivalently.

5\. Even with the guidance of Section 4.1, it can be difficult for a Cryptoki library developer to know which of CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_TEMPLATE\_INCOMPLETE, or CKR\_TEMPLATE\_INCONSISTENT to return. When possible, it is recommended that application developers be generous in their interpretations of these error codes.

## 5.2 Conventions for functions returning output in a variable-length buffer

A number of the functions defined in Cryptoki return output produced by some cryptographic mechanism. The amount of output returned by these functions is returned in a variable-length application-supplied buffer. An example of a function of this sort is **C\_Encrypt**, which takes some plaintext as an argument, and outputs a buffer full of ciphertext.

These functions have some common calling conventions, which we describe here. Two of the arguments to the function are a pointer to the output buffer (say *pBuf*) and a pointer to a location which will hold the length of the output produced (say *pulBufLen*). There are two ways for an application to call such a function:

1\. If *pBuf* is NULL\_PTR, then all that the function does is return (in \* *pulBufLen*) a number of bytes which would suffice to hold the cryptographic output produced from the input to the function. This number may somewhat exceed the precise number of bytes needed, but should not exceed it by a large amount. CKR\_OK is returned by the function.

2\. If *pBuf* is not NULL\_PTR, then \* *pulBufLen* MUST contain the size in bytes of the buffer pointed to by *pBuf*. If that buffer is large enough to hold the cryptographic output produced from the input to the function, then that cryptographic output is placed there, and CKR\_OK is returned by the function. If the buffer is not large enough, then CKR\_BUFFER\_TOO\_SMALL is returned. In either case, \* *pulBufLen* is set to hold the *exact* number of bytes needed to hold the cryptographic output produced from the input to the function.

All functions which use the above convention will explicitly say so.

Cryptographic functions which return output in a variable-length buffer should always return as much output as can be computed from what has been passed in to them thus far. As an example, consider a session which is performing a multiple-part decryption operation with DES in cipher-block chaining mode with PKCS padding. Suppose that, initially, 8 bytes of ciphertext are passed to the **C\_DecryptUpdate** function. The block size of DES is 8 bytes, but the PKCS padding makes it unclear at this stage whether the ciphertext was produced from encrypting a 0-byte string, or from encrypting some string of length at least 8 bytes. Hence the call to **C\_DecryptUpdate** should return 0 bytes of plaintext. If a single additional byte of ciphertext is supplied by a subsequent call to **C\_DecryptUpdate**, then that call should return 8 bytes of plaintext (one full DES block).

## 5.3 Disclaimer concerning sample code

For the remainder of this section, we enumerate the various functions defined in Cryptoki. Most functions will be shown in use in at least one sample code snippet. For the sake of brevity, sample code will frequently be somewhat incomplete. In particular, sample code will generally ignore possible error returns from C library functions, and also will not deal with Cryptoki error returns in a realistic fashion.

## 5.4 General-purpose functions

Cryptoki provides the following general-purpose functions:

### 5.4.1 C\_Initialize

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Initialize) {

CK\_VOID\_PTR pInitArgs

);

**C\_Initialize** initializes the Cryptoki library. *pInitArgs* either has the value NULL\_PTR or points to a **CK\_C\_INITIALIZE\_ARGS** structure containing information on how the library should deal with multi-threaded access. If an application will not be accessing Cryptoki through multiple threads simultaneously, it can generally supply the value NULL\_PTR to **C\_Initialize** (the consequences of supplying this value will be explained below).

If *pInitArgs* is non-NULL\_PTR, **C\_Initialize** should cast it to a **CK\_C\_INITIALIZE\_ARGS\_PTR** and then dereference the resulting pointer to obtain the **CK\_C\_INITIALIZE\_ARGS** fields *CreateMutex*, *DestroyMutex*, *LockMutex*, *UnlockMutex*, *flags*, and *pReserved*. For this version of Cryptoki, the value of *pReserved* thereby obtained MUST be NULL\_PTR; if it’s not, then **C\_Initialize** should return with the value CKR\_ARGUMENTS\_BAD.

If the **CKF\_LIBRARY\_CANT\_CREATE\_OS\_THREADS** flag in the *flags* field is set, that indicates that application threads which are executing calls to the Cryptoki library are not permitted to use the native operation system calls to spawn off new threads. In other words, the library’s code may not create its own threads. If the library is unable to function properly under this restriction, **C\_Initialize** should return with the value CKR\_NEED\_TO\_CREATE\_THREADS.

A call to **C\_Initialize** specifies one of four different ways to support multi-threaded access via the value of the **CKF\_OS\_LOCKING\_OK** flag in the *flags* field and the values of the *CreateMutex*, *DestroyMutex*, *LockMutex*, and *UnlockMutex* function pointer fields:

1\. If the flag *isn’t* set, and the function pointer fields *aren’t* supplied (*i.e.*, they all have the value NULL\_PTR), that means that the application *won’t* be accessing the Cryptoki library from multiple threads simultaneously.

2\. If the flag *is* set, and the function pointer fields *aren’t* supplied (*i.e.*, they all have the value NULL\_PTR), that means that the application *will* be performing multi-threaded Cryptoki access, and the library needs to use the native operating system primitives to ensure safe multi-threaded access. If the library is unable to do this, **C\_Initialize** should return with the value CKR\_CANT\_LOCK.

3\. If the flag *isn’t* set, and the function pointer fields *are* supplied (*i.e.*, they all have non-NULL\_PTR values), that means that the application *will* be performing multi-threaded Cryptoki access, and the library needs to use the supplied function pointers for mutex-handling to ensure safe multi-threaded access. If the library is unable to do this, **C\_Initialize** should return with the value CKR\_CANT\_LOCK.

4\. If the flag *is* set, and the function pointer fields *are* supplied (*i.e.*, they all have non-NULL\_PTR values), that means that the application *will* be performing multi-threaded Cryptoki access, and the library needs to use either the native operating system primitives or the supplied function pointers for mutex-handling to ensure safe multi-threaded access. If the library is unable to do this, **C\_Initialize** should return with the value CKR\_CANT\_LOCK.

If some, but not all, of the supplied function pointers to **C\_Initialize** are non-NULL\_PTR, then **C\_Initialize** should return with the value CKR\_ARGUMENTS\_BAD.

A call to **C\_Initialize** with *pInitArgs* set to NULL\_PTR is treated like a call to **C\_Initialize** with *pInitArgs* pointing to a **CK\_C\_INITIALIZE\_ARGS** which has the *CreateMutex*, *DestroyMutex*, *LockMutex*, *UnlockMutex*, and *pReserved* fields set to NULL\_PTR, and has the *flags* field set to 0.

**C\_Initialize** should be the first Cryptoki call made by an application, except for calls to **C\_GetFunctionList**, **C\_GetInterfaceList**, or **C\_GetInterface**. What this function actually does is implementation-dependent; typically, it might cause Cryptoki to initialize its internal memory buffers, or any other resources it requires.

If several applications are using Cryptoki, each one should call **C\_Initialize**. Every call to **C\_Initialize** should (eventually) be succeeded by a single call to **C\_Finalize**. See **\[PKCS11-UG\]** for further details.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CANT\_LOCK, CKR\_CRYPTOKI\_ALREADY\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_NEED\_TO\_CREATE\_THREADS, CKR\_OK.

Example: see **C\_GetInfo**.

### 5.4.2 C\_Finalize

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Finalize)(

CK\_VOID\_PTR pReserved

);

**C\_Finalize** is called to indicate that an application is finished with the Cryptoki library. It should be the last Cryptoki call made by an application. The *pReserved* parameter is reserved for future versions; for this version, it should be set to NULL\_PTR (if **C\_Finalize** is called with a non-NULL\_PTR value for *pReserved*, it should return the value CKR\_ARGUMENTS\_BAD.

If several applications are using Cryptoki, each one should call **C\_Finalize**. Each application’s call to **C\_Finalize** should be preceded by a single call to **C\_Initialize**; in between the two calls, an application can make calls to other Cryptoki functions. See **\[PKCS11-UG\]** for further details.

*Despite the fact that the parameters supplied to **C\_Initialize** can in general allow for safe multi-threaded access to a Cryptoki library, the behavior of **C\_Finalize** is nevertheless undefined if it is called by an application while other threads of the application are making Cryptoki calls. The exception to this exceptional behavior of **C\_Finalize** occurs when a thread calls **C\_Finalize** while another of the application’s threads is blocking on Cryptoki’s **C\_WaitForSlotEvent** function. When this happens, the blocked thread becomes unblocked and returns the value CKR\_CRYPTOKI\_NOT\_INITIALIZED. See **C\_WaitForSlotEvent** for more information.*

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example: see **C\_GetInfo**.

### 5.4.3 C\_GetInfo

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetInfo)(

CK\_INFO\_PTR pInfo

);

**C\_GetInfo** returns general information about Cryptoki. *pInfo* points to the location that receives the information.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example:

CK\_INFO info;

CK\_RV rv;

CK\_C\_INITIALIZE\_ARGS InitArgs;

InitArgs.CreateMutex = &MyCreateMutex;

InitArgs.DestroyMutex = &MyDestroyMutex;

InitArgs.LockMutex = &MyLockMutex;

InitArgs.UnlockMutex = &MyUnlockMutex;

InitArgs.flags = CKF\_OS\_LOCKING\_OK;

InitArgs.pReserved = NULL\_PTR;

rv = C\_Initialize((CK\_VOID\_PTR)&InitArgs);

assert(rv == CKR\_OK);

rv = C\_GetInfo(&info);

assert(rv == CKR\_OK);

if(info.cryptokiVersion.major == 2) {

/\* Do lots of interesting cryptographic things with the token \*/

.

.

}

rv = C\_Finalize(NULL\_PTR);

assert(rv == CKR\_OK);

### 5.4.4 C\_GetFunctionList

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetFunctionList)(

CK\_FUNCTION\_LIST\_PTR\_PTR ppFunctionList

);

**C\_GetFunctionList** obtains a pointer to the Cryptoki library’s list of function pointers. *ppFunctionList* points to a value which will receive a pointer to the library’s **CK\_FUNCTION\_LIST** structure, which in turn contains function pointers for all the Cryptoki API routines in the library. *The pointer thus obtained may point into memory which is owned by the Cryptoki library, and which may or may not be writable*. Whether or not this is the case, no attempt should be made to write to this memory.

**C\_GetFunctionList**, **C\_GetInterfaceList**, and **C\_GetInterface** are the only Cryptoki functions which an application may call before calling **C\_Initialize**. It is provided to make it easier and faster for applications to use shared Cryptoki libraries and to use more than one Cryptoki library simultaneously.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example:

CK\_FUNCTION\_LIST\_PTR pFunctionList;

CK\_C\_Initialize pC\_Initialize;

CK\_RV rv;

/\* It’s OK to call C\_GetFunctionList before calling C\_Initialize \*/

rv = C\_GetFunctionList(&pFunctionList);

assert(rv == CKR\_OK);

pC\_Initialize = pFunctionList -> C\_Initialize;

/\* Call the C\_Initialize function in the library \*/

rv = (\*pC\_Initialize)(NULL\_PTR);

### 5.4.5 C\_GetInterfaceList

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetInterfaceList)(

CK\_INTERFACE\_PTR pInterfaceList,

CK\_ULONG\_PTR pulCount

);

**C\_GetInterfaceList** is used to obtain a list of interfaces supported by a Cryptoki library. *pulCount* points to the location that receives the number of interfaces.

There are two ways for an application to call **C\_GetInterfaceList**:

1\. If *pInterfaceList* is NULL\_PTR, then all that **C\_GetInterfaceList** does is return (in \* *pulCount*) the number of interfaces, without actually returning a list of interfaces. The contents of \* *pulCount* on entry to **C\_GetInterfaceList** has no meaning in this case, and the call returns the value CKR\_OK.

2\. If *pIntrerfaceList* is not NULL\_PTR, then \* *pulCount* MUST contain the size (in terms of **CK\_INTERFACE** elements) of the buffer pointed to by *pInterfaceList*. If that buffer is large enough to hold the list of interfaces, then the list is returned in it, and CKR\_OK is returned. If not, then the call to **C\_GetInterfaceList** returns the value CKR\_BUFFER\_TOO\_SMALL. In either case, the value \* *pulCount* is set to hold the number of interfaces.

Because **C\_GetInterfaceList** does not allocate any space of its own, an application will often call **C\_GetInterfaceList** twice. However, this behavior is by no means required.

**C\_GetInterfaceList** obtains (in \* *pFunctionList* of each interface) a pointer to the Cryptoki library’s list of function pointers. *The pointer thus obtained may point into memory which is owned by the Cryptoki library, and which may or may not be writable*. Whether or not this is the case, no attempt should be made to write to this memory. The same caveat applies to the interface names returned.

**C\_GetFunctionList**, **C\_GetInterfaceList**, and **C\_GetInterface** are the only Cryptoki functions which an application may call before calling **C\_Initialize**. It is provided to make it easier and faster for applications to use shared Cryptoki libraries and to use more than one Cryptoki library simultaneously.

Return values: CKR\_BUFFER\_TOO\_SMALL, CKR\_ARGUMENTS\_BAD, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example:

CK\_ULONG ulCount=0;

CK\_INTERFACE\_PTR interfaceList=NULL;

CK\_RV rv;

int I;

/\* get number of interfaces \*/

rv = C\_GetInterfaceList(NULL,&ulCount);

if (rv == CKR\_OK) {

/\* get copy of interfaces \*/

interfaceList = (CK\_INTERFACE\_PTR)malloc(ulCount\*sizeof(CK\_INTERFACE));

rv = C\_GetInterfaceList(interfaceList,&ulCount);

for(i=0;i<ulCount;i++) {

printf("interface %s version %d.%d funcs %p flags 0x%lu\\n",

interfaceList\[i\].pInterfaceName,

((CK\_VERSION \*)interfaceList\[i\].pFunctionList)->major,

((CK\_VERSION \*)interfaceList\[i\].pFunctionList)->minor,

interfaceList\[i\].pFunctionList,

interfaceList\[i\].flags);

}

}

### 5.4.6 C\_GetInterface

CK\_DECLARE\_FUNCTION(CK\_RV,C\_GetInterface)(

CK\_UTF8CHAR\_PTR pInterfaceName,

CK\_VERSION\_PTR pVersion,

CK\_INTERFACE\_PTR\_PTR ppInterface,

CK\_FLAGS flags

);

**C\_GetInterface** is used to obtain an interface supported by a Cryptoki library. *pInterfaceName* specifies the name of the interface, *pVersion* specifies the interface version, *ppInterface* points to the location that receives the interface, *flags* specifies the required interface flags.

There are multiple ways for an application to specify a particular interface when calling **C\_GetInterface**:

1\. If *pInterfaceName* is not NULL\_PTR, the name of the interface returned must match. If *pInterfaceName* is NULL\_PTR, the cryptoki library can return a default interface of its choice

2\. If *pVersion* is not NULL\_PTR, the version of the interface returned must match. If *pVersion* is NULL\_PTR, the cryptoki library can return an interface of any version

3\. If *flags* is non-zero, the interface returned must match all of the supplied flag values (but may include additional flags not specified). If *flags* is 0, the cryptoki library can return an interface with any flags

**C\_GetInterface** obtains (in \* *pFunctionList* of each interface) a pointer to the Cryptoki library’s list of function pointers. *The pointer thus obtained may point into memory which is owned by the Cryptoki library, and which may or may not be writable*. Whether or not this is the case, no attempt should be made to write to this memory. The same caveat applies to the interface names returned.

**C\_GetFunctionList**, **C\_GetInterfaceList**, and **C\_GetInterface** are the only Cryptoki functions which an application may call before calling **C\_Initialize**. It is provided to make it easier and faster for applications to use shared Cryptoki libraries and to use more than one Cryptoki library simultaneously.

Return values: CKR\_BUFFER\_TOO\_SMALL, CKR\_ARGUMENTS\_BAD, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example:

CK\_INTERFACE\_PTR interface;

CK\_RV rv;

CK\_VERSION version;

CK\_FLAGS flags=CKF\_ INTERFACE\_FORK\_SAFE;

/\* get default interface \*/

rv = C\_GetInterface(NULL,NULL,&interface,flags);

if (rv == CKR\_OK) {

printf("interface %s version %d.%d funcs %p flags 0x%lu\\n",

interface->pInterfaceName,

((CK\_VERSION \*)interface->pFunctionList)->major,

((CK\_VERSION \*)interface->pFunctionList)->minor,

interface->pFunctionList,

interface->flags);

}

/\* get default standard interface \*/

rv = C\_GetInterface((CK\_UTF8CHAR\_PTR)"PKCS 11",NULL,&interface,flags);

if (rv == CKR\_OK) {

printf("interface %s version %d.%d funcs %p flags 0x%lu\\n",

interface->pInterfaceName,

((CK\_VERSION \*)interface->pFunctionList)->major,

((CK\_VERSION \*)interface->pFunctionList)->minor,

interface->pFunctionList,

interface->flags);

}

/\* get specific standard version interface \*/

version.major=3;

version.minor=0;

rv = C\_GetInterface((CK\_UTF8CHAR\_PTR)"PKCS 11",&version,&interface,flags);

if (rv == CKR\_OK) {

CK\_FUNCTION\_LIST\_3\_0\_PTR pkcs11=interface->pFunctionList;

/\*... use the new functions \*/

pkcs11->C\_LoginUser(hSession,userType,pPin,ulPinLen,  
pUsername,ulUsernameLen);

}

/\* get specific vendor version interface \*/

version.major=1;

version.minor=0;

rv = C\_GetInterface((CK\_UTF8CHAR\_PTR)

"Vendor VendorName",&version,&interface,flags);

if (rv == CKR\_OK) {

CK\_FUNCTION\_LIST\_VENDOR\_1\_0\_PTR pkcs11=interface->pFunctionList;

/\*... use vendor specific functions \*/

pkcs11->C\_VendorFunction1(param1,param2,param3);

}

## 5.5 Slot and token management functions

Cryptoki provides the following functions for slot and token management:

### 5.5.1 C\_GetSlotList

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetSlotList)(

CK\_BBOOL tokenPresent,

CK\_SLOT\_ID\_PTR pSlotList,

CK\_ULONG\_PTR pulCount

);

**C\_GetSlotList** is used to obtain a list of slots in the system. *tokenPresent* indicates whether the list obtained includes only those slots with a token present (CK\_TRUE), or all slots (CK\_FALSE); *pulCount* points to the location that receives the number of slots.

There are two ways for an application to call **C\_GetSlotList**:

1\. If *pSlotList* is NULL\_PTR, then all that **C\_GetSlotList** does is return (in \* *pulCount*) the number of slots, without actually returning a list of slots. The contents of the buffer pointed to by *pulCount* on entry to **C\_GetSlotList** has no meaning in this case, and the call returns the value CKR\_OK.

2\. If *pSlotList* is not NULL\_PTR, then \* *pulCount* MUST contain the size (in terms of **CK\_SLOT\_ID** elements) of the buffer pointed to by *pSlotList*. If that buffer is large enough to hold the list of slots, then the list is returned in it, and CKR\_OK is returned. If not, then the call to **C\_GetSlotList** returns the value CKR\_BUFFER\_TOO\_SMALL. In either case, the value \* *pulCount* is set to hold the number of slots.

Because **C\_GetSlotList** does not allocate any space of its own, an application will often call **C\_GetSlotList** twice (or sometimes even more times—if an application is trying to get a list of all slots with a token present, then the number of such slots can (unfortunately) change between when the application asks for how many such slots there are and when the application asks for the slots themselves). However, multiple calls to **C\_GetSlotList** are by no means *required*.

All slots which **C\_GetSlotList** reports MUST be able to be queried as valid slots by **C\_GetSlotInfo**. Furthermore, the set of slots accessible through a Cryptoki library is checked at the time that **C\_GetSlotList,** for list length prediction (NULL pSlotList argument) is called. If an application calls **C\_GetSlotList** with a non-NULL pSlotList, and *then* the user adds or removes a hardware device, the changed slot list will only be visible and effective if **C\_GetSlotList** is called again with NULL. Even if **C\_ GetSlotList** is successfully called this way, it may or may not be the case that the changed slot list will be successfully recognized depending on the library implementation. On some platforms, or earlier PKCS11 compliant libraries, it may be necessary to successfully call **C\_Initialize** or to restart the entire system.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK.

Example:

CK\_ULONG ulSlotCount, ulSlotWithTokenCount;

CK\_SLOT\_ID\_PTR pSlotList, pSlotWithTokenList;

CK\_RV rv;

/\* Get list of all slots \*/

rv = C\_GetSlotList(CK\_FALSE, NULL\_PTR, &ulSlotCount);

if (rv == CKR\_OK) {

pSlotList =

(CK\_SLOT\_ID\_PTR) malloc(ulSlotCount\*sizeof(CK\_SLOT\_ID));

rv = C\_GetSlotList(CK\_FALSE, pSlotList, &ulSlotCount);

if (rv == CKR\_OK) {

/\* Now use that list of all slots \*/

.

.

}

free(pSlotList);

}

/\* Get list of all slots with a token present \*/

pSlotWithTokenList = (CK\_SLOT\_ID\_PTR) malloc(0);

ulSlotWithTokenCount = 0;

while (1) {

rv = C\_GetSlotList(

CK\_TRUE, pSlotWithTokenList, &ulSlotWithTokenCount);

if (rv!= CKR\_BUFFER\_TOO\_SMALL)

break;

pSlotWithTokenList = realloc(

pSlotWithTokenList,

ulSlotWithTokenList\*sizeof(CK\_SLOT\_ID));

}

if (rv == CKR\_OK) {

/\* Now use that list of all slots with a token present \*/

.

.

}

free(pSlotWithTokenList);

### 5.5.2 C\_GetSlotInfo

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetSlotInfo)(

CK\_SLOT\_ID slotID,

CK\_SLOT\_INFO\_PTR pInfo

);

**C\_GetSlotInfo** obtains information about a particular slot in the system. *slotID* is the ID of the slot; *pInfo* points to the location that receives the slot information.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SLOT\_ID\_INVALID.

Example: see **C\_GetTokenInfo.**

### 5.5.3 C\_GetTokenInfo

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetTokenInfo)(

CK\_SLOT\_ID slotID,

CK\_TOKEN\_INFO\_PTR pInfo

);

**C\_GetTokenInfo** obtains information about a particular token in the system. *slotID* is the ID of the token’s slot; *pInfo* points to the location that receives the token information.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT, CKR\_TOKEN\_NOT\_RECOGNIZED, CKR\_ARGUMENTS\_BAD.

Example:

CK\_ULONG ulCount;

CK\_SLOT\_ID\_PTR pSlotList;

CK\_SLOT\_INFO slotInfo;

CK\_TOKEN\_INFO tokenInfo;

CK\_RV rv;

rv = C\_GetSlotList(CK\_FALSE, NULL\_PTR, &ulCount);

if ((rv == CKR\_OK) && (ulCount > 0)) {

pSlotList = (CK\_SLOT\_ID\_PTR) malloc(ulCount\*sizeof(CK\_SLOT\_ID));

rv = C\_GetSlotList(CK\_FALSE, pSlotList, &ulCount);

assert(rv == CKR\_OK);

/\* Get slot information for first slot \*/

rv = C\_GetSlotInfo(pSlotList\[0\], &slotInfo);

assert(rv == CKR\_OK);

/\* Get token information for first slot \*/

rv = C\_GetTokenInfo(pSlotList\[0\], &tokenInfo);

if (rv == CKR\_TOKEN\_NOT\_PRESENT) {

.

.

}

.

.

free(pSlotList);

}

### 5.5.4 C\_WaitForSlotEvent

CK\_DECLARE\_FUNCTION(CK\_RV, C\_WaitForSlotEvent)(

CK\_FLAGS flags,

CK\_SLOT\_ID\_PTR pSlot,

CK\_VOID\_PTR pReserved

);

**C\_WaitForSlotEvent** waits for a slot event, such as token insertion or token removal, to occur. *flags* determines whether or not the **C\_WaitForSlotEvent** call blocks (*i.e.*, waits for a slot event to occur); *pSlot* points to a location which will receive the ID of the slot that the event occurred in. *pReserved* is reserved for future versions; for this version of Cryptoki, it should be NULL\_PTR.

At present, the only flag defined for use in the *flags* argument is **CKF\_DONT\_BLOCK**:

Internally, each Cryptoki application has a flag for each slot which is used to track whether or not any unrecognized events involving that slot have occurred. When an application initially calls **C\_Initialize**, every slot’s event flag is cleared. Whenever a slot event occurs, the flag corresponding to the slot in which the event occurred is set.

If **C\_WaitForSlotEvent** is called with the **CKF\_DONT\_BLOCK** flag set in the *flags* argument, and some slot’s event flag is set, then that event flag is cleared, and the call returns with the ID of that slot in the location pointed to by *pSlot*. If more than one slot’s event flag is set at the time of the call, one such slot is chosen by the library to have its event flag cleared and to have its slot ID returned.

If **C\_WaitForSlotEvent** is called with the **CKF\_DONT\_BLOCK** flag set in the *flags* argument, and no slot’s event flag is set, then the call returns with the value CKR\_NO\_EVENT. In this case, the contents of the location pointed to by *pSlot* when **C\_WaitForSlotEvent** are undefined.

If **C\_WaitForSlotEvent** is called with the **CKF\_DONT\_BLOCK** flag clear in the *flags* argument, then the call behaves as above, except that it will block. That is, if no slot’s event flag is set at the time of the call, **C\_WaitForSlotEvent** will wait until some slot’s event flag becomes set. If a thread of an application has a **C\_WaitForSlotEvent** call blocking when another thread of that application calls **C\_Finalize**, the **C\_WaitForSlotEvent** call returns with the value CKR\_CRYPTOKI\_NOT\_INITIALIZED.

*Although the parameters supplied to **C\_Initialize** can in general allow for safe multi-threaded access to a Cryptoki library, **C\_WaitForSlotEvent** is exceptional in that the behavior of Cryptoki is undefined if multiple threads of a single application make simultaneous calls to **C\_WaitForSlotEvent**.*

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_NO\_EVENT, CKR\_OK.

Example:

CK\_FLAGS flags = 0;

CK\_SLOT\_ID slotID;

CK\_SLOT\_INFO slotInfo;

CK\_RV rv;

.

.

/\* Block and wait for a slot event \*/

rv = C\_WaitForSlotEvent(flags, &slotID, NULL\_PTR);

assert(rv == CKR\_OK);

/\* See what’s up with that slot \*/

rv = C\_GetSlotInfo(slotID, &slotInfo);

assert(rv == CKR\_OK);

### 5.5.5 C\_GetMechanismList

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetMechanismList)(

CK\_SLOT\_ID slotID,

CK\_MECHANISM\_TYPE\_PTR pMechanismList,

CK\_ULONG\_PTR pulCount

);

**C\_GetMechanismList** is used to obtain a list of mechanism types supported by a token. *SlotID* is the ID of the token’s slot; *pulCount* points to the location that receives the number of mechanisms.

There are two ways for an application to call **C\_GetMechanismList**:

1\. If *pMechanismList* is NULL\_PTR, then all that **C\_GetMechanismList** does is return (in \* *pulCount*) the number of mechanisms, without actually returning a list of mechanisms. The contents of \* *pulCount* on entry to **C\_GetMechanismList** has no meaning in this case, and the call returns the value CKR\_OK.

2\. If *pMechanismList* is not NULL\_PTR, then \* *pulCount* MUST contain the size (in terms of **CK\_MECHANISM\_TYPE** elements) of the buffer pointed to by *pMechanismList*. If that buffer is large enough to hold the list of mechanisms, then the list is returned in it, and CKR\_OK is returned. If not, then the call to **C\_GetMechanismList** returns the value CKR\_BUFFER\_TOO\_SMALL. In either case, the value \* *pulCount* is set to hold the number of mechanisms.

Because **C\_GetMechanismList** does not allocate any space of its own, an application will often call **C\_GetMechanismList** twice. However, this behavior is by no means required.

Return values: CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT, CKR\_TOKEN\_NOT\_RECOGNIZED, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SLOT\_ID slotID;

CK\_ULONG ulCount;

CK\_MECHANISM\_TYPE\_PTR pMechanismList;

CK\_RV rv;

.

.

rv = C\_GetMechanismList(slotID, NULL\_PTR, &ulCount);

if ((rv == CKR\_OK) && (ulCount > 0)) {

pMechanismList =

(CK\_MECHANISM\_TYPE\_PTR)

malloc(ulCount\*sizeof(CK\_MECHANISM\_TYPE));

rv = C\_GetMechanismList(slotID, pMechanismList, &ulCount);

if (rv == CKR\_OK) {

.

.

}

free(pMechanismList);

}

### 5.5.6 C\_GetMechanismInfo

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetMechanismInfo)(

CK\_SLOT\_ID slotID,

CK\_MECHANISM\_TYPE type,

CK\_MECHANISM\_INFO\_PTR pInfo

);

**C\_GetMechanismInfo** obtains information about a particular mechanism possibly supported by a token. *slotID* is the ID of the token’s slot; *type* is the type of mechanism; *pInfo* points to the location that receives the mechanism information.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_MECHANISM\_INVALID, CKR\_OK, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT, CKR\_TOKEN\_NOT\_RECOGNIZED, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SLOT\_ID slotID;

CK\_MECHANISM\_INFO info;

CK\_RV rv;

.

.

/\* Get information about the CKM\_MD2 mechanism for this token \*/

rv = C\_GetMechanismInfo(slotID, CKM\_MD2, &info);

if (rv == CKR\_OK) {

if (info.flags & CKF\_DIGEST) {

.

.

}

}

### 5.5.7 C\_InitToken

CK\_DECLARE\_FUNCTION(CK\_RV, C\_InitToken)(

CK\_SLOT\_ID slotID,

CK\_UTF8CHAR\_PTR pPin,

CK\_ULONG ulPinLen,

CK\_UTF8CHAR\_PTR pLabel

);

**C\_InitToken** initializes a token. *slotID* is the ID of the token’s slot; *pPin* points to the SO’s initial PIN (which need *not* be null-terminated); *ulPinLen* is the length in bytes of the PIN; *pLabel* points to the 32-byte label of the token (which MUST be padded with blank characters, and which MUST *not* be null-terminated). This standard allows PIN values to contain any valid UTF8 character, but the token may impose subset restrictions.

If the token has not been initialized (i.e. new from the factory), then the *pPin* parameter becomes the initial value of the SO PIN. If the token is being reinitialized, the *pPin* parameter is checked against the existing SO PIN to authorize the initialization operation. In both cases, the SO PIN is the value *pPin* after the function completes successfully. If the SO PIN is lost, then the card MUST be reinitialized using a mechanism outside the scope of this standard. The **CKF\_TOKEN\_INITIALIZED** flag in the **CK\_TOKEN\_INFO** structure indicates the action that will result from calling **C\_InitToken**. If set, the token will be reinitialized, and the client MUST supply the existing SO password in *pPin*.

When a token is initialized, all objects that can be destroyed are destroyed (*i.e.*, all except for “indestructible” objects such as keys built into the token). Also, access by the normal user is disabled until the SO sets the normal user’s PIN. Depending on the token, some “default” objects may be created, and attributes of some objects may be set to default values.

If the token has a “protected authentication path”, as indicated by the **CKF\_PROTECTED\_AUTHENTICATION\_PATH** flag in its **CK\_TOKEN\_INFO** being set, then that means that there is some way for a user to be authenticated to the token without having the application send a PIN through the Cryptoki library. One such possibility is that the user enters a PIN on a PINpad on the token itself, or on the slot device. To initialize a token with such a protected authentication path, the *pPin* parameter to **C\_InitToken** should be NULL\_PTR. During the execution of **C\_InitToken**, the SO’s PIN will be entered through the protected authentication path.

If the token has a protected authentication path other than a PINpad, then it is token-dependent whether or not **C\_InitToken** can be used to initialize the token.

A token cannot be initialized if Cryptoki detects that *any* application has an open session with it; when a call to **C\_InitToken** is made under such circumstances, the call fails with error CKR\_SESSION\_EXISTS. Unfortunately, it may happen when **C\_InitToken** is called that some other application *does* have an open session with the token, but Cryptoki cannot detect this, because it cannot detect anything about other applications using the token. If this is the case, then the consequences of the **C\_InitToken** call are undefined.

The **C\_InitToken** function may not be sufficient to properly initialize complex tokens. In these situations, an initialization mechanism outside the scope of Cryptoki MUST be employed. The definition of “complex token” is product specific.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_PIN\_INCORRECT, CKR\_PIN\_LOCKED, CKR\_SESSION\_EXISTS, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT, CKR\_TOKEN\_NOT\_RECOGNIZED, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SLOT\_ID slotID;

CK\_UTF8CHAR pin\[\] = {“MyPIN”};

CK\_UTF8CHAR label\[32\];

CK\_RV rv;

.

.

memset(label, ‘ ’, sizeof(label));

memcpy(label, “My first token”, strlen(“My first token”));

rv = C\_InitToken(slotID, pin, strlen(pin), label);

if (rv == CKR\_OK) {

.

.

}

### 5.5.8 C\_InitPIN

CK\_DECLARE\_FUNCTION(CK\_RV, C\_InitPIN)(  
CK\_SESSION\_HANDLE hSession,  
CK\_UTF8CHAR\_PTR pPin,  
CK\_ULONG ulPinLen  
);

**C\_InitPIN** initializes the normal user’s PIN. *hSession* is the session’s handle; *pPin* points to the normal user’s PIN; *ulPinLen* is the length in bytes of the PIN. This standard allows PIN values to contain any valid UTF8 character, but the token may impose subset restrictions.

**C\_InitPIN** can only be called in the “R/W SO Functions” state. An attempt to call it from a session in any other state fails with error CKR\_USER\_NOT\_LOGGED\_IN.

If the token has a “protected authentication path”, as indicated by the CKF\_PROTECTED\_AUTHENTICATION\_PATH flag in its **CK\_TOKEN\_INFO** being set, then that means that there is some way for a user to be authenticated to the token without having to send a PIN through the Cryptoki library. One such possibility is that the user enters a PIN on a PIN pad on the token itself, or on the slot device. To initialize the normal user’s PIN on a token with such a protected authentication path, the *pPin* parameter to **C\_InitPIN** should be NULL\_PTR. During the execution of **C\_InitPIN**, the SO will enter the new PIN through the protected authentication path.

If the token has a protected authentication path other than a PIN pad, then it is token-dependent whether or not **C\_InitPIN** can be used to initialize the normal user’s token access.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_PIN\_INVALID, CKR\_PIN\_LEN\_RANGE, CKR\_SESSION\_CLOSED, CKR\_SESSION\_READ\_ONLY, CKR\_SESSION\_HANDLE\_INVALID, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_UTF8CHAR newPin\[\]= {“NewPIN”};

CK\_RV rv;

rv = C\_InitPIN(hSession, newPin, sizeof(newPin)-1);

if (rv == CKR\_OK) {

.

.

}

### 5.5.9 C\_SetPIN

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SetPIN)(  
CK\_SESSION\_HANDLE hSession,  
CK\_UTF8CHAR\_PTR pOldPin,  
CK\_ULONG ulOldLen,  
CK\_UTF8CHAR\_PTR pNewPin,  
CK\_ULONG ulNewLen  
);

**C\_SetPIN** modifies the PIN of the user that is currently logged in, or the CKU\_USER PIN if the session is not logged in. *hSession* is the session’s handle; *pOldPin* points to the old PIN; *ulOldLen* is the length in bytes of the old PIN; *pNewPin* points to the new PIN; *ulNewLen* is the length in bytes of the new PIN. This standard allows PIN values to contain any valid UTF8 character, but the token may impose subset restrictions.

**C\_SetPIN** can only be called in the “R/W Public Session” state, “R/W SO Functions” state, or “R/W User Functions” state. An attempt to call it from a session in any other state fails with error CKR\_SESSION\_READ\_ONLY.

If the token has a “protected authentication path”, as indicated by the CKF\_PROTECTED\_AUTHENTICATION\_PATH flag in its **CK\_TOKEN\_INFO** being set, then that means that there is some way for a user to be authenticated to the token without having to send a PIN through the Cryptoki library. One such possibility is that the user enters a PIN on a PIN pad on the token itself, or on the slot device. To modify the current user’s PIN on a token with such a protected authentication path, the *pOldPin* and *pNewPin* parameters to **C\_SetPIN** should be NULL\_PTR. During the execution of **C\_SetPIN**, the current user will enter the old PIN and the new PIN through the protected authentication path. It is not specified how the PIN pad should be used to enter *two* PINs; this varies.

If the token has a protected authentication path other than a PIN pad, then it is token-dependent whether or not **C\_SetPIN** can be used to modify the current user’s PIN.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_PIN\_INCORRECT, CKR\_PIN\_INVALID, CKR\_PIN\_LEN\_RANGE, CKR\_PIN\_LOCKED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_UTF8CHAR oldPin\[\] = {“OldPIN”};

CK\_UTF8CHAR newPin\[\] = {“NewPIN”};

CK\_RV rv;

rv = C\_SetPIN(

hSession, oldPin, sizeof(oldPin)-1, newPin, sizeof(newPin)-1);

if (rv == CKR\_OK) {

.

.

}

## 5.6 Session management functions

A typical application might perform the following series of steps to make use of a token (note that there are other reasonable sequences of events that an application might perform):

1\. Select a token.

2\. Make one or more calls to **C\_OpenSession** to obtain one or more sessions with the token.

3\. Call **C\_Login** to log the user into the token. Since all sessions an application has with a token have a shared login state, **C\_Login** only needs to be called for one of the sessions.

4\. Perform cryptographic operations using the sessions with the token.

5\. Call **C\_CloseSession** once for each session that the application has with the token, or call **C\_CloseAllSessions** to close all the application’s sessions simultaneously.

As has been observed, an application may have concurrent sessions with more than one token. It is also possible for a token to have concurrent sessions with more than one application.

Cryptoki provides the following functions for session management:

### 5.6.1 C\_OpenSession

CK\_DECLARE\_FUNCTION(CK\_RV, C\_OpenSession)(  
CK\_SLOT\_ID slotID,  
CK\_FLAGS flags,  
CK\_VOID\_PTR pApplication,  
CK\_NOTIFY Notify,  
CK\_SESSION\_HANDLE\_PTR phSession  
);

**C\_OpenSession** opens a session between an application and a token in a particular slot. *slotID* is the slot’s ID; *flags* indicates the type of session; *pApplication* is an application-defined pointer to be passed to the notification callback; *Notify* is the address of the notification callback function (see Section 5.21); *phSession* points to the location that receives the handle for the new session.

When opening a session with **C\_OpenSession**, the *flags* parameter consists of the logical OR of zero or more bit flags defined in the **CK\_SESSION\_INFO** data type. For legacy reasons, the **CKF\_SERIAL\_SESSION** bit MUST always be set; if a call to **C\_OpenSession** does not have this bit set, the call should return unsuccessfully with the error code CKR\_SESSION\_PARALLEL\_NOT\_SUPPORTED.

There may be a limit on the number of concurrent sessions an application may have with the token, which may depend on whether the session is “read-only” or “read/write”. An attempt to open a session which does not succeed because there are too many existing sessions of some type should return CKR\_SESSION\_COUNT.

If the token is write-protected (as indicated in the **CK\_TOKEN\_INFO** structure), then only read-only sessions may be opened with it.

If the application calling **C\_OpenSession** already has a R/W SO session open with the token, then any attempt to open a R/O session with the token fails with error code CKR\_SESSION\_READ\_WRITE\_SO\_EXISTS (see **\[PKCS11-UG\]** for further details).

The *Notify* callback function is used by Cryptoki to notify the application of certain events. If the application does not wish to support callbacks, it should pass a value of NULL\_PTR as the *Notify* parameter. See Section 5.21 for more information about application callbacks.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SESSION\_COUNT, CKR\_SESSION\_PARALLEL\_NOT\_SUPPORTED, CKR\_SESSION\_READ\_WRITE\_SO\_EXISTS, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT, CKR\_TOKEN\_NOT\_RECOGNIZED, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_ARGUMENTS\_BAD.

Example: see **C\_CloseSession**.

### 5.6.2 C\_CloseSession

CK\_DECLARE\_FUNCTION(CK\_RV, C\_CloseSession)(  
CK\_SESSION\_HANDLE hSession  
);

**C\_CloseSession** closes a session between an application and a token. *hSession* is the session’s handle.

When a session is closed, all session objects created by the session are destroyed automatically, even if the application has other sessions “using” the objects (see **\[PKCS11-UG\]** for further details).

If this function is successful and it closes the last session between the application and the token, the login state of the token for the application returns to public sessions. Any new sessions to the token opened by the application will be either R/O Public or R/W Public sessions.

Depending on the token, when the last open session any application has with the token is closed, the token may be “ejected” from its reader (if this capability exists).

Despite the fact this **C\_CloseSession** is supposed to close a session, the return value CKR\_SESSION\_CLOSED is an *error* return. It actually indicates the (probably somewhat unlikely) event that while this function call was executing, another call was made to **C\_CloseSession** to close this particular session, and that call finished executing first. Such uses of sessions are a bad idea, and Cryptoki makes little promise of what will occur in general if an application indulges in this sort of behavior.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

CK\_SLOT\_ID slotID;

CK\_BYTE application;

CK\_NOTIFY MyNotify;

CK\_SESSION\_HANDLE hSession;

CK\_RV rv;

.

.

application = 17;

MyNotify = &EncryptionSessionCallback;

rv = C\_OpenSession(

slotID, CKF\_SERIAL\_SESSION | CKF\_RW\_SESSION,

(CK\_VOID\_PTR) &application, MyNotify,

&hSession);

if (rv == CKR\_OK) {

.

.

C\_CloseSession(hSession);

}

### 5.6.3 C\_CloseAllSessions

CK\_DECLARE\_FUNCTION(CK\_RV, C\_CloseAllSessions)(  
CK\_SLOT\_ID slotID  
);

**C\_CloseAllSessions** closes all sessions an application has with a token. *slotID* specifies the token’s slot.

When a session is closed, all session objects created by the session are destroyed automatically.

After successful execution of this function, the login state of the token for the application returns to public sessions. Any new sessions to the token opened by the application will be either R/O Public or R/W Public sessions.

Depending on the token, when the last open session any application has with the token is closed, the token may be “ejected” from its reader (if this capability exists).

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SLOT\_ID\_INVALID, CKR\_TOKEN\_NOT\_PRESENT.

Example:

CK\_SLOT\_ID slotID;

CK\_RV rv;

.

.

rv = C\_CloseAllSessions(slotID);

### 5.6.4 C\_GetSessionInfo

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetSessionInfo)(  
CK\_SESSION\_HANDLE hSession,  
CK\_SESSION\_INFO\_PTR pInfo  
);

**C\_GetSessionInfo** obtains information about a session. *hSession* is the session’s handle; *pInfo* points to the location that receives the session information.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_SESSION\_INFO info;

CK\_RV rv;

.

.

rv = C\_GetSessionInfo(hSession, &info);

if (rv == CKR\_OK) {

if (info.state == CKS\_RW\_USER\_FUNCTIONS) {

.

.

}

.

.

}

### 5.6.5 C\_SessionCancel

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SessionCancel)(  
CK\_SESSION\_HANDLE hSession  
CK\_FLAGS flags  
);

**C\_SessionCancel** terminates active session based operations. *hSession* is the session’s handle; *flags* indicates the operations to cancel.

To identify which operation(s) should be terminated, the *flags* parameter should be assigned the logical bitwise OR of one or more of the bit flags defined in the **CK\_MECHANISM\_INFO** structure.

If no flags are set, the session state will not be modified and CKR\_OK will be returned.

If a flag is set for an operation that has not been initialized in the session, the operation flag will be ignored and **C\_SessionCancel** will behave as if the operation flag was not set.

If any of the operations indicated by the *flags* parameter cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned. If multiple operation flags were set and CKR\_OPERATION\_CANCEL\_FAILED is returned, this function does not provide any information about which operation(s) could not be cancelled. If an application desires to know if any single operation could not be cancelled, the application should not call **C\_SessionCancel** with multiple flags set.

If **C\_SessionCancel** is called from an application callback (see Section 5.16), no action will be taken by the library and CKR\_FUNCTION\_FAILED must be returned.

If **C\_SessionCancel** is used to cancel one half of a dual-function operation, the remaining operation should still be left in an active state. However, it is expected that some Cryptoki implementations may not support this and return CKR\_OPERATION\_CANCEL\_FAILED unless flags for both operations are provided.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_CANCEL\_FAILED, CKR\_TOKEN\_NOT\_PRESENT.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_RV rv;

rv = C\_EncryptInit(hSession, &mechanism, hKey);

if (rv!= CKR\_OK)

{

.

.

}

rv = C\_SessionCancel (hSession, CKF\_ENCRYPT);

if (rv!= CKR\_OK)

{

.

.

}

rv = C\_EncryptInit(hSession, &mechanism, hKey);

if (rv!= CKR\_OK)

{

.

.

}

Below are modifications to existing API descriptions to allow an alternate method of cancelling individual operations. The additional text is highlighted.

### 5.6.6 C\_GetOperationState

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetOperationState)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pOperationState,  
CK\_ULONG\_PTR pulOperationStateLen  
);

**C\_GetOperationState** obtains a copy of the cryptographic operations state of a session, encoded as a string of bytes. *hSession* is the session’s handle; *pOperationState* points to the location that receives the state; *pulOperationStateLen* points to the location that receives the length in bytes of the state.

Although the saved state output by **C\_GetOperationState** is not really produced by a “cryptographic mechanism”, **C\_GetOperationState** nonetheless uses the convention described in Section 5.2 on producing output.

Precisely what the “cryptographic operations state” this function saves is varies from token to token; however, this state is what is provided as input to **C\_SetOperationState** to restore the cryptographic activities of a session.

Consider a session which is performing a message digest operation using SHA-1 (*i.e.*, the session is using the **CKM\_SHA\_1** mechanism). Suppose that the message digest operation was initialized properly, and that precisely 80 bytes of data have been supplied so far as input to SHA-1. The application now wants to “save the state” of this digest operation, so that it can continue it later. In this particular case, since SHA-1 processes 512 bits (64 bytes) of input at a time, the cryptographic operations state of the session most likely consists of three distinct parts: the state of SHA-1’s 160-bit internal chaining variable; the 16 bytes of unprocessed input data; and some administrative data indicating that this saved state comes from a session which was performing SHA-1 hashing. Taken together, these three pieces of information suffice to continue the current hashing operation at a later time.

Consider next a session which is performing an encryption operation with DES (a block cipher with a block size of 64 bits) in CBC (cipher-block chaining) mode (*i.e.*, the session is using the **CKM\_DES\_CBC** mechanism). Suppose that precisely 22 bytes of data (in addition to an IV for the CBC mode) have been supplied so far as input to DES, which means that the first two 8-byte blocks of ciphertext have already been produced and output. In this case, the cryptographic operations state of the session most likely consists of three or four distinct parts: the second 8-byte block of ciphertext (this will be used for cipher-block chaining to produce the next block of ciphertext); the 6 bytes of data still awaiting encryption; some administrative data indicating that this saved state comes from a session which was performing DES encryption in CBC mode; and possibly the DES key being used for encryption (see **C\_SetOperationState** for more information on whether or not the key is present in the saved state).

If a session is performing two cryptographic operations simultaneously (see Section 5.14), then the cryptographic operations state of the session will contain all the necessary information to restore both operations.

An attempt to save the cryptographic operations state of a session which does not currently have some active savable cryptographic operation(s) (encryption, decryption, digesting, signing without message recovery, verification without message recovery, or some legal combination of two of these) should fail with the error CKR\_OPERATION\_NOT\_INITIALIZED.

An attempt to save the cryptographic operations state of a session which is performing an appropriate cryptographic operation (or two), but which cannot be satisfied for any of various reasons (certain necessary state information and/or key information can’t leave the token, for example) should fail with the error CKR\_STATE\_UNSAVEABLE.

Return values: CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_STATE\_UNSAVEABLE, CKR\_ARGUMENTS\_BAD.

Example: see **C\_SetOperationState**.

### 5.6.7 C\_SetOperationState

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SetOperationState)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pOperationState,  
CK\_ULONG ulOperationStateLen,  
CK\_OBJECT\_HANDLE hEncryptionKey,  
CK\_OBJECT\_HANDLE hAuthenticationKey  
);

**C\_SetOperationState** restores the cryptographic operations state of a session from a string of bytes obtained with **C\_GetOperationState**. *hSession* is the session’s handle; *pOperationState* points to the location holding the saved state; *ulOperationStateLen* holds the length of the saved state; *hEncryptionKey* holds a handle to the key which will be used for an ongoing encryption or decryption operation in the restored session (or 0 if no encryption or decryption key is needed, either because no such operation is ongoing in the stored session or because all the necessary key information is present in the saved state); *hAuthenticationKey* holds a handle to the key which will be used for an ongoing signature, MACing, or verification operation in the restored session (or 0 if no such key is needed, either because no such operation is ongoing in the stored session or because all the necessary key information is present in the saved state).

The state need not have been obtained from the same session (the “source session”) as it is being restored to (the “destination session”). However, the source session and destination session should have a common session state (*e.g.*, CKS\_RW\_USER\_FUNCTIONS), and should be with a common token. There is also no guarantee that cryptographic operations state may be carried across logins, or across different Cryptoki implementations.

If **C\_SetOperationState** is supplied with alleged saved cryptographic operations state which it can determine is not valid saved state (or is cryptographic operations state from a session with a different session state, or is cryptographic operations state from a different token), it fails with the error CKR\_SAVED\_STATE\_INVALID.

Saved state obtained from calls to **C\_GetOperationState** may or may not contain information about keys in use for ongoing cryptographic operations. If a saved cryptographic operations state has an ongoing encryption or decryption operation, and the key in use for the operation is not saved in the state, then it MUST be supplied to **C\_SetOperationState** in the *hEncryptionKey* argument. If it is not, then **C\_SetOperationState** will fail and return the error CKR\_KEY\_NEEDED. If the key in use for the operation *is* saved in the state, then it *can* be supplied in the *hEncryptionKey* argument, but this is not required.

Similarly, if a saved cryptographic operations state has an ongoing signature, MACing, or verification operation, and the key in use for the operation is not saved in the state, then it MUST be supplied to **C\_SetOperationState** in the *hAuthenticationKey* argument. If it is not, then **C\_SetOperationState** will fail with the error CKR\_KEY\_NEEDED. If the key in use for the operation *is* saved in the state, then it *can* be supplied in the *hAuthenticationKey* argument, but this is not required.

If an *irrelevant* key is supplied to **C\_SetOperationState** call (*e.g.*, a nonzero key handle is submitted in the *hEncryptionKey* argument, but the saved cryptographic operations state supplied does not have an ongoing encryption or decryption operation, then **C\_SetOperationState** fails with the error CKR\_KEY\_NOT\_NEEDED.

If a key is supplied as an argument to **C\_SetOperationState**, and **C\_SetOperationState** can somehow detect that this key was not the key being used in the source session for the supplied cryptographic operations state (it may be able to detect this if the key or a hash of the key is present in the saved state, for example), then **C\_SetOperationState** fails with the error CKR\_KEY\_CHANGED.

An application can look at the **CKF\_RESTORE\_KEY\_NOT\_NEEDED** flag in the flags field of the **CK\_TOKEN\_INFO** field for a token to determine whether or not it needs to supply key handles to **C\_SetOperationState** calls. If this flag is true, then a call to **C\_SetOperationState** *never* needs a key handle to be supplied to it. If this flag is false, then at least some of the time, **C\_SetOperationState** requires a key handle, and so the application should probably *always* pass in any relevant key handles when restoring cryptographic operations state to a session.

**C\_SetOperationState** can successfully restore cryptographic operations state to a session even if that session has active cryptographic or object search operations when **C\_SetOperationState** is called (the ongoing operations are abruptly cancelled).

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_CHANGED, CKR\_KEY\_NEEDED, CKR\_KEY\_NOT\_NEEDED, CKR\_OK, CKR\_SAVED\_STATE\_INVALID, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_ARGUMENTS\_BAD.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_MECHANISM digestMechanism;

CK\_BYTE\_PTR pState;

CK\_ULONG ulStateLen;

CK\_BYTE data1\[\] = {0x01, 0x03, 0x05, 0x07};

CK\_BYTE data2\[\] = {0x02, 0x04, 0x08};

CK\_BYTE data3\[\] = {0x10, 0x0F, 0x0E, 0x0D, 0x0C};

CK\_BYTE pDigest\[20\];

CK\_ULONG ulDigestLen;

CK\_RV rv;

.

.

/\* Initialize hash operation \*/

rv = C\_DigestInit(hSession, &digestMechanism);

assert(rv == CKR\_OK);

/\* Start hashing \*/

rv = C\_DigestUpdate(hSession, data1, sizeof(data1));

assert(rv == CKR\_OK);

/\* Find out how big the state might be \*/

rv = C\_GetOperationState(hSession, NULL\_PTR, &ulStateLen);

assert(rv == CKR\_OK);

/\* Allocate some memory and then get the state \*/

pState = (CK\_BYTE\_PTR) malloc(ulStateLen);

rv = C\_GetOperationState(hSession, pState, &ulStateLen);

/\* Continue hashing \*/

rv = C\_DigestUpdate(hSession, data2, sizeof(data2));

assert(rv == CKR\_OK);

/\* Restore state. No key handles needed \*/

rv = C\_SetOperationState(hSession, pState, ulStateLen, 0, 0);

assert(rv == CKR\_OK);

/\* Continue hashing from where we saved state \*/

rv = C\_DigestUpdate(hSession, data3, sizeof(data3));

assert(rv == CKR\_OK);

/\* Conclude hashing operation \*/

ulDigestLen = sizeof(pDigest);

rv = C\_DigestFinal(hSession, pDigest, &ulDigestLen);

if (rv == CKR\_OK) {

/\* pDigest\[\] now contains the hash of 0x01030507100F0E0D0C \*/

.

.

}

### 5.6.8 C\_Login

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Login)(  
CK\_SESSION\_HANDLE hSession,  
CK\_USER\_TYPE userType,  
CK\_UTF8CHAR\_PTR pPin,  
CK\_ULONG ulPinLen  
);

**C\_Login** logs a user into a token. *hSession* is a session handle; *userType* is the user type; *pPin* points to the user’s PIN; *ulPinLen* is the length of the PIN. This standard allows PIN values to contain any valid UTF8 character, but the token may impose subset restrictions.

When the user type is either CKU\_SO or CKU\_USER, if the call succeeds, each of the application's sessions will enter either the "R/W SO Functions" state, the "R/W User Functions" state, or the "R/O User Functions" state. If the user type is CKU\_CONTEXT\_SPECIFIC, the behavior of C\_Login depends on the context in which it is called. Improper use of this user type will result in a return value CKR\_OPERATION\_NOT\_INITIALIZED..

If the token has a “protected authentication path”, as indicated by the **CKF\_PROTECTED\_AUTHENTICATION\_PATH** flag in its **CK\_TOKEN\_INFO** being set, then that means that there is some way for a user to be authenticated to the token without having to send a PIN through the Cryptoki library. One such possibility is that the user enters a PIN on a PIN pad on the token itself, or on the slot device. Or the user might not even use a PIN—authentication could be achieved by some fingerprint-reading device, for example. To log into a token with a protected authentication path, the *pPin* parameter to **C\_Login** should be NULL\_PTR. When **C\_Login** returns, whatever authentication method supported by the token will have been performed; a return value of CKR\_OK means that the user was successfully authenticated, and a return value of CKR\_PIN\_INCORRECT means that the user was denied access.

If there are any active cryptographic or object finding operations in an application’s session, and then **C\_Login** is successfully executed by that application, it may or may not be the case that those operations are still active. Therefore, before logging in, any active operations should be finished.

If the application calling **C\_Login** has a R/O session open with the token, then it will be unable to log the SO into a session (see **\[PKCS11-UG\]** for further details). An attempt to do this will result in the error code CKR\_SESSION\_READ\_ONLY\_EXISTS.

C\_Login may be called repeatedly, without intervening **C\_Logout** calls, if (and only if) a key with the CKA\_ALWAYS\_AUTHENTICATE attribute set to CK\_TRUE exists, and the user needs to do cryptographic operation on this key. See further Section 4.9.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_PIN\_INCORRECT, CKR\_PIN\_LOCKED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY\_EXISTS, CKR\_USER\_ALREADY\_LOGGED\_IN, CKR\_USER\_ANOTHER\_ALREADY\_LOGGED\_IN, CKR\_USER\_PIN\_NOT\_INITIALIZED, CKR\_USER\_TOO\_MANY\_TYPES, CKR\_USER\_TYPE\_INVALID.

Example: see **C\_Logout**.

### 5.6.9 C\_LoginUser

CK\_DECLARE\_FUNCTION(CK\_RV, C\_LoginUser)(  
CK\_SESSION\_HANDLE hSession,

CK\_USER\_TYPE userType,

CK\_UTF8CHAR\_PTR pPin,

CK\_ULONG ulPinLen,

CK\_UTF8CHAR\_PTR pUsername,

CK\_ULONG ulUsernameLen  
);

**C\_LoginUser** logs a user into a token. *hSession* is a session handle; *userType* is the user type; *pPin* points to the user’s PIN; *ulPinLen* is the length of the PIN, *pUsername* points to the user name, *ulUsernameLen* is the length of the user name. This standard allows PIN and user name values to contain any valid UTF8 character, but the token may impose subset restrictions.

When the user type is either CKU\_SO or CKU\_USER, if the call succeeds, each of the application's sessions will enter either the "R/W SO Functions" state, the "R/W User Functions" state, or the "R/O User Functions" state. If the user type is CKU\_CONTEXT\_SPECIFIC, the behavior of **C\_LoginUser** depends on the context in which it is called. Improper use of this user type will result in a return value CKR\_OPERATION\_NOT\_INITIALIZED.

If the token has a “protected authentication path”, as indicated by the CKF\_PROTECTED\_AUTHENTICATION\_PATH flag in its CK\_TOKEN\_INFO being set, then that means that there is some way for a user to be authenticated to the token without having to send a PIN through the Cryptoki library. One such possibility is that the user enters a PIN on a PIN pad on the token itself, or on the slot device. The user might not even use a PIN—authentication could be achieved by some fingerprint-reading device, for example. To log into a token with a protected authentication path, the *pPin* parameter to **C\_LoginUser** should be NULL\_PTR. When **C\_LoginUser** returns, whatever authentication method supported by the token will have been performed; a return value of CKR\_OK means that the user was successfully authenticated, and a return value of CKR\_PIN\_INCORRECT means that the user was denied access.

If there are any active cryptographic or object finding operations in an application’s session, and then **C\_LoginUser** is successfully executed by that application, it may or may not be the case that those operations are still active. Therefore, before logging in, any active operations should be finished.

If the application calling **C\_LoginUser** has a R/O session open with the token, then it will be unable to log the SO into a session (see \[PKCS11-UG\] for further details). An attempt to do this will result in the error code CKR\_SESSION\_READ\_ONLY\_EXISTS.

**C\_LoginUser** may be called repeatedly, without intervening **C\_Logout** calls, if (and only if) a key with the CKA\_ALWAYS\_AUTHENTICATE attribute set to CK\_TRUE exists, and the user needs to do cryptographic operation on this key. See further Section 4.9.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_PIN\_INCORRECT, CKR\_PIN\_LOCKED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY\_EXISTS, CKR\_USER\_ALREADY\_LOGGED\_IN, CKR\_USER\_ANOTHER\_ALREADY\_LOGGED\_IN, CKR\_USER\_PIN\_NOT\_INITIALIZED, CKR\_USER\_TOO\_MANY\_TYPES, CKR\_USER\_TYPE\_INVALID.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_UTF8CHAR userPin\[\] = {“MyPIN”};

CK\_UTF8CHAR userName\[\] = {“MyUserName”};

CK\_RV rv;

rv = C\_LoginUser(hSession, CKU\_USER, userPin, sizeof(userPin)-1, userName,

sizeof(userName)-1);

if (rv == CKR\_OK) {

.

.

rv = C\_Logout(hSession);

if (rv == CKR\_OK) {

.

.

}

}

### 5.6.10 C\_Logout

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Logout)(  
CK\_SESSION\_HANDLE hSession  
);

**C\_Logout** logs a user out from a token. *hSession* is the session’s handle.

Depending on the current user type, if the call succeeds, each of the application’s sessions will enter either the “R/W Public Session” state or the “R/O Public Session” state.

When **C\_Logout** successfully executes, any of the application’s handles to private objects become invalid (even if a user is later logged back into the token, those handles remain invalid). In addition, all private session objects from sessions belonging to the application are destroyed.

If there are any active cryptographic or object-finding operations in an application’s session, and then **C\_Logout** is successfully executed by that application, it may or may not be the case that those operations are still active. Therefore, before logging out, any active operations should be finished.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_UTF8CHAR userPin\[\] = {“MyPIN”};

CK\_RV rv;

rv = C\_Login(hSession, CKU\_USER, userPin, sizeof(userPin)-1);

if (rv == CKR\_OK) {

.

.

rv = C\_Logout(hSession);

if (rv == CKR\_OK) {

.

.

}

}

## 5.7 Object management functions

Cryptoki provides the following functions for managing objects. Additional functions provided specifically for managing key objects are described in Section 5.18.

### 5.7.1 C\_CreateObject

CK\_DECLARE\_FUNCTION(CK\_RV, C\_CreateObject)(  
CK\_SESSION\_HANDLE hSession,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount,  
CK\_OBJECT\_HANDLE\_PTR phObject  
);

**C\_CreateObject** creates a new object. *hSession* is the session’s handle; *pTemplate* points to the object’s template; *ulCount* is the number of attributes in the template; *phObject* points to the location that receives the new object’s handle.

If a call to **C\_CreateObject** cannot support the precise template supplied to it, it will fail and return without creating any object.

If **C\_CreateObject** is used to create a key object, the key object will have its **CKA\_LOCAL** attribute set to CK\_FALSE. If that key object is a secret or private key then the new key will have the **CKA\_ALWAYS\_SENSITIVE** attribute set to CK\_FALSE, and the **CKA\_NEVER\_EXTRACTABLE** attribute set to CK\_FALSE.

Only session objects can be created during a read-only session. Only public objects can be created unless the normal user is logged in.

Whenever an object is created, a value for CKA\_UNIQUE\_ID is generated and assigned to the new object (See Section 4.4.1).

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_CURVE\_NOT\_SUPPORTED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_DOMAIN\_PARAMS\_INVALID, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCOMPLETE, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE

hData,

hCertificate,

hKey;

CK\_OBJECT\_CLASS

dataClass = CKO\_DATA,

certificateClass = CKO\_CERTIFICATE,

keyClass = CKO\_PUBLIC\_KEY;

CK\_KEY\_TYPE keyType = CKK\_RSA;

CK\_UTF8CHAR application\[\] = {“My Application”};

CK\_BYTE dataValue\[\] = {...};

CK\_BYTE subject\[\] = {...};

CK\_BYTE id\[\] = {...};

CK\_BYTE certificateValue\[\] = {...};

CK\_BYTE modulus\[\] = {...};

CK\_BYTE exponent\[\] = {...};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE dataTemplate\[\] = {

{CKA\_CLASS, &dataClass, sizeof(dataClass)},

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_APPLICATION, application, sizeof(application)-1},

{CKA\_VALUE, dataValue, sizeof(dataValue)}

};

CK\_ATTRIBUTE certificateTemplate\[\] = {

{CKA\_CLASS, &certificateClass, sizeof(certificateClass)},

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_SUBJECT, subject, sizeof(subject)},

{CKA\_ID, id, sizeof(id)},

{CKA\_VALUE, certificateValue, sizeof(certificateValue)}

};

CK\_ATTRIBUTE keyTemplate\[\] = {

{CKA\_CLASS, &keyClass, sizeof(keyClass)},

{CKA\_KEY\_TYPE, &keyType, sizeof(keyType)},

{CKA\_WRAP, &true, sizeof(true)},

{CKA\_MODULUS, modulus, sizeof(modulus)},

{CKA\_PUBLIC\_EXPONENT, exponent, sizeof(exponent)}

};

CK\_RV rv;

.

.

/\* Create a data object \*/

rv = C\_CreateObject(hSession, dataTemplate, 4, &hData);

if (rv == CKR\_OK) {

.

.

}

/\* Create a certificate object \*/

rv = C\_CreateObject(

hSession, certificateTemplate, 5, &hCertificate);

if (rv == CKR\_OK) {

.

.

}

/\* Create an RSA public key object \*/

rv = C\_CreateObject(hSession, keyTemplate, 5, &hKey);

if (rv == CKR\_OK) {

.

.

}

### 5.7.2 C\_CopyObject

CK\_DECLARE\_FUNCTION(CK\_RV, C\_CopyObject)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hObject,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount,  
CK\_OBJECT\_HANDLE\_PTR phNewObject  
);

**C\_CopyObject** copies an object, creating a new object for the copy. *hSession* is the session’s handle; *hObject* is the object’s handle; *pTemplate* points to the template for the new object; *ulCount* is the number of attributes in the template; *phNewObject* points to the location that receives the handle for the copy of the object.

The template may specify new values for any attributes of the object that can ordinarily be modified (*e.g.*, in the course of copying a secret key, a key’s **CKA\_EXTRACTABLE** attribute may be changed from CK\_TRUE to CK\_FALSE, but not the other way around. If this change is made, the new key’s **CKA\_NEVER\_EXTRACTABLE** attribute will have the value CK\_FALSE. Similarly, the template may specify that the new key’s **CKA\_SENSITIVE** attribute be CK\_TRUE; the new key will have the same value for its **CKA\_ALWAYS\_SENSITIVE** attribute as the original key). It may also specify new values of the **CKA\_TOKEN** and **CKA\_PRIVATE** attributes (*e.g.*, to copy a session object to a token object). If the template specifies a value of an attribute which is incompatible with other existing attributes of the object, the call fails with the return code CKR\_TEMPLATE\_INCONSISTENT.

If a call to **C\_CopyObject** cannot support the precise template supplied to it, it will fail and return without creating any object. If the object indicated by hObject has its CKA\_COPYABLE attribute set to CK\_FALSE, C\_CopyObject will return CKR\_ACTION\_PROHIBITED.

Whenever an object is copied, a new value for CKA\_UNIQUE\_ID is generated and assigned to the new object (See Section 4.4.1).

Only session objects can be created during a read-only session. Only public objects can be created unless the normal user is logged in.

Return values:, CKR\_ACTION\_PROHIBITED, CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OBJECT\_HANDLE\_INVALID, CKR\_OK, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey, hNewKey;

CK\_OBJECT\_CLASS keyClass = CKO\_SECRET\_KEY;

CK\_KEY\_TYPE keyType = CKK\_DES;

CK\_BYTE id\[\] = {...};

CK\_BYTE keyValue\[\] = {...};

CK\_BBOOL false = CK\_FALSE;

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE keyTemplate\[\] = {

{CKA\_CLASS, &keyClass, sizeof(keyClass)},

{CKA\_KEY\_TYPE, &keyType, sizeof(keyType)},

{CKA\_TOKEN, &false, sizeof(false)},

{CKA\_ID, id, sizeof(id)},

{CKA\_VALUE, keyValue, sizeof(keyValue)}

};

CK\_ATTRIBUTE copyTemplate\[\] = {

{CKA\_TOKEN, &true, sizeof(true)}

};

CK\_RV rv;

.

.

/\* Create a DES secret key session object \*/

rv = C\_CreateObject(hSession, keyTemplate, 5, &hKey);

if (rv == CKR\_OK) {

/\* Create a copy which is a token object \*/

rv = C\_CopyObject(hSession, hKey, copyTemplate, 1, &hNewKey);

.

.

}

### 5.7.3 C\_DestroyObject

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DestroyObject)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hObject  
);

**C\_DestroyObject** destroys an object. *hSession* is the session’s handle; and *hObject* is the object’s handle.

Only session objects can be destroyed during a read-only session. Only public objects can be destroyed unless the normal user is logged in.

Certain objects may not be destroyed. Calling C\_DestroyObject on such objects will result in the CKR\_ACTION\_PROHIBITED error code. An application can consult the object's CKA\_DESTROYABLE attribute to determine if an object may be destroyed or not.

Return values: CKR\_ACTION\_PROHIBITED, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OBJECT\_HANDLE\_INVALID, CKR\_OK, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TOKEN\_WRITE\_PROTECTED.

Example: see **C\_GetObjectSize**.

### 5.7.4 C\_GetObjectSize

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetObjectSize)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hObject,  
CK\_ULONG\_PTR pulSize  
);

**C\_GetObjectSize** gets the size of an object in bytes. *hSession* is the session’s handle; *hObject* is the object’s handle; *pulSize* points to the location that receives the size in bytes of the object.

Cryptoki does not specify what the precise meaning of an object’s size is. Intuitively, it is some measure of how much token memory the object takes up. If an application deletes (say) a private object of size S, it might be reasonable to assume that the *ulFreePrivateMemory* field of the token’s **CK\_TOKEN\_INFO** structure increases by approximately S.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_INFORMATION\_SENSITIVE, CKR\_OBJECT\_HANDLE\_INVALID, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hObject;

CK\_OBJECT\_CLASS dataClass = CKO\_DATA;

CK\_UTF8CHAR application\[\] = {“My Application”};

CK\_BYTE value\[\] = {...};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] = {

{CKA\_CLASS, &dataClass, sizeof(dataClass)},

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_APPLICATION, application, sizeof(application)-1},

{CKA\_VALUE, value, sizeof(value)}

};

CK\_ULONG ulSize;

CK\_RV rv;

.

.

rv = C\_CreateObject(hSession, template, 4, &hObject);

if (rv == CKR\_OK) {

rv = C\_GetObjectSize(hSession, hObject, &ulSize);

if (rv!= CKR\_INFORMATION\_SENSITIVE) {

.

.

}

rv = C\_DestroyObject(hSession, hObject);

.

.

}

### 5.7.5 C\_GetAttributeValue

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetAttributeValue)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hObject,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount  
);

**C\_GetAttributeValue** obtains the value of one or more attributes of an object. *hSession* is the session’s handle; *hObject* is the object’s handle; *pTemplate* points to a template that specifies which attribute values are to be obtained, and receives the attribute values; *ulCount* is the number of attributes in the template.

For each (*type*, *pValue*, *ulValueLen*) triple in the template, **C\_GetAttributeValue** performs the following algorithm:

1\. If the specified attribute (i.e., the attribute specified by the type field) for the object cannot be revealed because the object is sensitive or unextractable, then the ulValueLen field in that triple is modified to hold the value CK\_UNAVAILABLE\_INFORMATION.

2\. Otherwise, if the specified value for the object is invalid (the object does not possess such an attribute), then the ulValueLen field in that triple is modified to hold the value CK\_UNAVAILABLE\_INFORMATION.

3\. Otherwise, if the *pValue* field has the value NULL\_PTR, then the *ulValueLen* field is modified to hold the exact length of the specified attribute for the object.

4\. Otherwise, if the length specified in *ulValueLen* is large enough to hold the value of the specified attribute for the object, then that attribute is copied into the buffer located at *pValue*, and the *ulValueLen* field is modified to hold the exact length of the attribute.

5\. Otherwise, the ulValueLen field is modified to hold the value CK\_UNAVAILABLE\_INFORMATION.

If case 1 applies to any of the requested attributes, then the call should return the value CKR\_ATTRIBUTE\_SENSITIVE. If case 2 applies to any of the requested attributes, then the call should return the value CKR\_ATTRIBUTE\_TYPE\_INVALID. If case 5 applies to any of the requested attributes, then the call should return the value CKR\_BUFFER\_TOO\_SMALL. As usual, if more than one of these error codes is applicable, Cryptoki may return any of them. Only if none of them applies to any of the requested attributes will CKR\_OK be returned.

In the special case of an attribute whose value is an array of attributes, for example CKA\_WRAP\_TEMPLATE, where it is passed in with pValue not NULL, the length specified in ulValueLen MUST be large enough to hold all attributes in the array. If the pValue of elements within the array is NULL\_PTR then the ulValueLen of elements within the array will be set to the required length. If the pValue of elements within the array is not NULL\_PTR, then the ulValueLen element of attributes within the array MUST reflect the space that the corresponding pValue points to, and pValue is filled in if there is sufficient room. Therefore it is important to initialize the contents of a buffer before calling C\_GetAttributeValue to get such an array value. Note that the type element of attributes within the array MUST be ignored on input and MUST be set on output. If any ulValueLen within the array isn't large enough, it will be set to CK\_UNAVAILABLE\_INFORMATION and the function will return CKR\_BUFFER\_TOO\_SMALL, as it does if an attribute in the pTemplate argument has ulValueLen too small. Note that any attribute whose value is an array of attributes is identifiable by virtue of the attribute type having the CKF\_ARRAY\_ATTRIBUTE bit set.

Note that the error codes CKR\_ATTRIBUTE\_SENSITIVE, CKR\_ATTRIBUTE\_TYPE\_INVALID, and CKR\_BUFFER\_TOO\_SMALL do not denote true errors for **C\_GetAttributeValue**. If a call to **C\_GetAttributeValue** returns any of these three values, then the call MUST nonetheless have processed *every* attribute in the template supplied to **C\_GetAttributeValue**. Each attribute in the template whose value *can be* returned by the call to **C\_GetAttributeValue** *will be* returned by the call to **C\_GetAttributeValue**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_SENSITIVE, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OBJECT\_HANDLE\_INVALID, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hObject;

CK\_BYTE\_PTR pModulus, pExponent;

CK\_ATTRIBUTE template\[\] = {

{CKA\_MODULUS, NULL\_PTR, 0},

{CKA\_PUBLIC\_EXPONENT, NULL\_PTR, 0}

};

CK\_RV rv;

.

.

rv = C\_GetAttributeValue(hSession, hObject, template, 2);

if (rv == CKR\_OK) {

pModulus = (CK\_BYTE\_PTR) malloc(template\[0\].ulValueLen);

template\[0\].pValue = pModulus;

/\* template\[0\].ulValueLen was set by C\_GetAttributeValue \*/

pExponent = (CK\_BYTE\_PTR) malloc(template\[1\].ulValueLen);

template\[1\].pValue = pExponent;

/\* template\[1\].ulValueLen was set by C\_GetAttributeValue \*/

rv = C\_GetAttributeValue(hSession, hObject, template, 2);

if (rv == CKR\_OK) {

.

.

}

free(pModulus);

free(pExponent);

}

### 5.7.6 C\_SetAttributeValue

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SetAttributeValue)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hObject,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount  
);

**C\_SetAttributeValue** modifies the value of one or more attributes of an object. *hSession* is the session’s handle; *hObject* is the object’s handle; *pTemplate* points to a template that specifies which attribute values are to be modified and their new values; *ulCount* is the number of attributes in the template.

Certain objects may not be modified. Calling C\_SetAttributeValue on such objects will result in the CKR\_ACTION\_PROHIBITED error code. An application can consult the object's CKA\_MODIFIABLE attribute to determine if an object may be modified or not.

Only session objects can be modified during a read-only session.

The template may specify new values for any attributes of the object that can be modified. If the template specifies a value of an attribute which is incompatible with other existing attributes of the object, the call fails with the return code CKR\_TEMPLATE\_INCONSISTENT.

Not all attributes can be modified; see Section 4.1.2 for more details.

Return values: CKR\_ACTION\_PROHIBITED, CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OBJECT\_HANDLE\_INVALID, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hObject;

CK\_UTF8CHAR label\[\] = {“New label”};

CK\_ATTRIBUTE template\[\] = {

{CKA\_LABEL, label, sizeof(label)-1}

};

CK\_RV rv;

.

.

rv = C\_SetAttributeValue(hSession, hObject, template, 1);

if (rv == CKR\_OK) {

.

.

}

### 5.7.7 C\_FindObjectsInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_FindObjectsInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount  
);

**C\_FindObjectsInit** initializes a search for token and session objects that match a template. *hSession* is the session’s handle; *pTemplate* points to a search template that specifies the attribute values to match; *ulCount* is the number of attributes in the search template. The matching criterion is an exact byte-for-byte match with all attributes in the template. To find all objects, set *ulCount* to 0.

After calling **C\_FindObjectsInit**, the application may call **C\_FindObjects** one or more times to obtain handles for objects matching the template, and then eventually call **C\_FindObjectsFinal** to finish the active search operation. At most one search operation may be active at a given time in a given session.

The object search operation will only find objects that the session can view. For example, an object search in an “R/W Public Session” will not find any private objects (even if one of the attributes in the search template specifies that the search is for private objects).

If a search operation is active, and objects are created or destroyed which fit the search template for the active search operation, then those objects may or may not be found by the search operation. Note that this means that, under these circumstances, the search operation may return invalid object handles.

Even though **C\_FindObjectsInit** can return the values CKR\_ATTRIBUTE\_TYPE\_INVALID and CKR\_ATTRIBUTE\_VALUE\_INVALID, it is not required to. For example, if it is given a search template with nonexistent attributes in it, it can return CKR\_ATTRIBUTE\_TYPE\_INVALID, or it can initialize a search operation which will match no objects and return CKR\_OK.

If the CKA\_UNIQUE\_ID attribute is present in the search template, either zero or one objects will be found, since at most one object can have any particular CKA\_UNIQUE\_ID value.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_FindObjectsFinal**.

### 5.7.8 C\_FindObjects

CK\_DECLARE\_FUNCTION(CK\_RV, C\_FindObjects)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE\_PTR phObject,  
CK\_ULONG ulMaxObjectCount,  
CK\_ULONG\_PTR pulObjectCount  
);

**C\_FindObjects** continues a search for token and session objects that match a template, obtaining additional object handles. *hSession* is the session’s handle; *phObject* points to the location that receives the list (array) of additional object handles; *ulMaxObjectCount* is the maximum number of object handles to be returned; *pulObjectCount* points to the location that receives the actual number of object handles returned.

If there are no more objects matching the template, then the location that *pulObjectCount* points to receives the value 0.

The search MUST have been initialized with **C\_FindObjectsInit**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_FindObjectsFinal**.

### 5.7.9 C\_FindObjectsFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_FindObjectsFinal)(  
CK\_SESSION\_HANDLE hSession  
);

**C\_FindObjectsFinal** terminates a search for token and session objects. *hSession* is the session’s handle.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hObject;

CK\_ULONG ulObjectCount;

CK\_RV rv;

.

.

rv = C\_FindObjectsInit(hSession, NULL\_PTR, 0);

assert(rv == CKR\_OK);

while (1) {

rv = C\_FindObjects(hSession, &hObject, 1, &ulObjectCount);

if (rv!= CKR\_OK || ulObjectCount == 0)

break;

.

.

}

rv = C\_FindObjectsFinal(hSession);

assert(rv == CKR\_OK);

## 5.8 Encryption functions

Cryptoki provides the following functions for encrypting data:

### 5.8.1 C\_EncryptInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_EncryptInit** initializes an encryption operation. *hSession* is the session’s handle; *pMechanism* points to the encryption mechanism; *hKey* is the handle of the encryption key.

The **CKA\_ENCRYPT** attribute of the encryption key, which indicates whether the key supports encryption, MUST be CK\_TRUE.

After calling **C\_EncryptInit**, the application can either call **C\_Encrypt** to encrypt data in a single part; or call **C\_EncryptUpdate** zero or more times, followed by **C\_EncryptFinal**, to encrypt data in multiple parts. The encryption operation is active until the application uses a call to **C\_Encrypt** or **C\_EncryptFinal** *to actually obtain* the final piece of ciphertext. To process additional data (in single or multiple parts), the application MUST call **C\_EncryptInit** again.

**C\_EncryptInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active encryption operation. If an active operation operations cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_EncryptFinal**.

### 5.8.2 C\_Encrypt

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Encrypt)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pData,  
CK\_ULONG ulDataLen,  
CK\_BYTE\_PTR pEncryptedData,  
CK\_ULONG\_PTR pulEncryptedDataLen  
);

**C\_Encrypt** encrypts single-part data. *hSession* is the session’s handle; *pData* points to the data; *ulDataLen* is the length in bytes of the data; *pEncryptedData* points to the location that receives the encrypted data; *pulEncryptedDataLen* points to the location that holds the length in bytes of the encrypted data.

**C\_Encrypt** uses the convention described in Section 5.2 on producing output.

The encryption operation MUST have been initialized with **C\_EncryptInit**. A call to **C\_Encrypt** always terminates the active encryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the ciphertext.

**C\_Encrypt** cannot be used to terminate a multi-part operation, and MUST be called after **C\_EncryptInit** without intervening **C\_EncryptUpdate** calls.

For some encryption mechanisms, the input plaintext data has certain length constraints (either because the mechanism can only encrypt relatively short pieces of plaintext, or because the mechanism’s input data MUST consist of an integral number of blocks). If these constraints are not satisfied, then **C\_Encrypt** will fail with return code CKR\_DATA\_LEN\_RANGE.

The plaintext and ciphertext can be in the same place, *i.e.*, it is OK if *pData* and *pEncryptedData* point to the same location.

For most mechanisms, **C\_Encrypt** is equivalent to a sequence of **C\_EncryptUpdate** operations followed by **C\_EncryptFinal**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_EncryptFinal** for an example of similar functions.

### 5.8.3 C\_EncryptUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG\_PTR pulEncryptedPartLen  
);

**C\_EncryptUpdate** continues a multiple-part encryption operation, processing another data part. *hSession* is the session’s handle; *pPart* points to the data part; *ulPartLen* is the length of the data part; *pEncryptedPart* points to the location that receives the encrypted data part; *pulEncryptedPartLen* points to the location that holds the length in bytes of the encrypted data part.

**C\_EncryptUpdate** uses the convention described in Section 5.2 on producing output.

The encryption operation MUST have been initialized with **C\_EncryptInit**. This function may be called any number of times in succession. A call to **C\_EncryptUpdate** which results in an error other than CKR\_BUFFER\_TOO\_SMALL terminates the current encryption operation.

The plaintext and ciphertext can be in the same place, *i.e.*, it is OK if *pPart* and *pEncryptedPart* point to the same location.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_EncryptFinal.**

### 5.8.4 C\_EncryptFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptFinal)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pLastEncryptedPart,  
CK\_ULONG\_PTR pulLastEncryptedPartLen  
);

**C\_EncryptFinal** finishes a multiple-part encryption operation. *hSession* is the session’s handle; *pLastEncryptedPart* points to the location that receives the last encrypted data part, if any; *pulLastEncryptedPartLen* points to the location that holds the length of the last encrypted data part.

**C\_EncryptFinal** uses the convention described in Section 5.2 on producing output.

The encryption operation MUST have been initialized with **C\_EncryptInit**. A call to **C\_EncryptFinal** always terminates the active encryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the ciphertext.

For some multi-part encryption mechanisms, the input plaintext data has certain length constraints, because the mechanism’s input data MUST consist of an integral number of blocks. If these constraints are not satisfied, then **C\_EncryptFinal** will fail with return code CKR\_DATA\_LEN\_RANGE.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

#define PLAINTEXT\_BUF\_SZ 200

#define CIPHERTEXT\_BUF\_SZ 256

CK\_ULONG firstPieceLen, secondPieceLen;

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM mechanism = {

CKM\_DES\_CBC\_PAD, iv, sizeof(iv)

};

CK\_BYTE data\[PLAINTEXT\_BUF\_SZ\];

CK\_BYTE encryptedData\[CIPHERTEXT\_BUF\_SZ\];

CK\_ULONG ulEncryptedData1Len;

CK\_ULONG ulEncryptedData2Len;

CK\_ULONG ulEncryptedData3Len;

CK\_RV rv;

.

.

firstPieceLen = 90;

secondPieceLen = PLAINTEXT\_BUF\_SZ-firstPieceLen;

rv = C\_EncryptInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

/\* Encrypt first piece \*/

ulEncryptedData1Len = sizeof(encryptedData);

rv = C\_EncryptUpdate(

hSession,

&data\[0\], firstPieceLen,

&encryptedData\[0\], &ulEncryptedData1Len);

if (rv!= CKR\_OK) {

.

.

}

/\* Encrypt second piece \*/

ulEncryptedData2Len = sizeof(encryptedData)-ulEncryptedData1Len;

rv = C\_EncryptUpdate(

hSession,

&data\[firstPieceLen\], secondPieceLen,

&encryptedData\[ulEncryptedData1Len\], &ulEncryptedData2Len);

if (rv!= CKR\_OK) {

.

.

}

/\* Get last little encrypted bit \*/

ulEncryptedData3Len =

sizeof(encryptedData)-ulEncryptedData1Len-ulEncryptedData2Len;

rv = C\_EncryptFinal(

hSession,

&encryptedData\[ulEncryptedData1Len+ulEncryptedData2Len\],

&ulEncryptedData3Len);

if (rv!= CKR\_OK) {

.

.

}

}

## 5.9 Message-based encryption functions

Message-based encryption refers to the process of encrypting multiple messages using the same encryption mechanism and encryption key. The encryption mechanism can be either an authenticated encryption with associated data (AEAD) algorithm or a pure encryption algorithm.

Cryptoki provides the following functions for message-based encryption:

### 5.9.1 C\_MessageEncryptInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageEncryptInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_MessageEncryptInit** prepares a session for one or more encryption operations that use the same encryption mechanism and encryption key. hSession is the session’s handle; pMechanism points to the encryption mechanism; hKey is the handle of the encryption key.

The CKA\_ENCRYPT attribute of the encryption key, which indicates whether the key supports encryption, MUST be CK\_TRUE.

After calling **C\_MessageEncryptInit**, the application can either call **C\_EncryptMessage** to encrypt a message in a single part, or call **C\_EncryptMessageBegin**, followed by **C\_EncryptMessageNext** one or more times, to encrypt a message in multiple parts. This may be repeated several times. The message-based encryption process is active until the application calls **C\_MessageEncryptFinal** to finish the message-based encryption process.

**C\_MessageEncryptInit** can be called with *pMechanism* set to NULL\_PTR to terminate a message-based encryption process. If a multi-part message encryption operation is active, it will also be terminated. If an active operation has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

### 5.9.2 C\_EncryptMessage

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptMessage)(  
CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pAssociatedData,

CK\_ULONG ulAssociatedDataLen,

CK\_BYTE\_PTR pPlaintext,

CK\_ULONG ulPlaintextLen,

CK\_BYTE\_PTR pCiphertext,

CK\_ULONG\_PTR pulCiphertextLen

);

**C\_EncryptMessage** encrypts a message in a single part. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message encryption operation; *pAssociatedData* and *ulAssociatedDataLen* specify the associated data for an AEAD mechanism; *pPlaintext* points to the plaintext data; *ulPlaintextLen* is the length in bytes of the plaintext data; *pCiphertext* points to the location that receives the encrypted data; *pulCiphertextLen* points to the location that holds the length in bytes of the encrypted data.

Typically, *pParameter* is an initialization vector (IV) or nonce. Depending on the mechanism parameter passed to **C\_MessageEncryptInit**, *pParameter* may be either an input or an output parameter. For example, if the mechanism parameter specifies an IV generator mechanism, the IV generated by the IV generator will be output to the *pParameter* buffer.

If the encryption mechanism is not AEAD, *pAssociatedData* and *ulAssociatedDataLen* are not used and should be set to (NULL, 0).

**C\_EncryptMessage** uses the convention described in Section 5.2 on producing output.

The message-based encryption process MUST have been initialized with **C\_MessageEncryptInit**. A call to **C\_EncryptMessage** begins and terminates a message encryption operation.

**C\_EncryptMessage** cannot be called in the middle of a multi-part message encryption operation.

For some encryption mechanisms, the input plaintext data has certain length constraints (either because the mechanism can only encrypt relatively short pieces of plaintext, or because the mechanism’s input data MUST consist of an integral number of blocks). If these constraints are not satisfied, then **C\_EncryptMessage** will fail with return code CKR\_DATA\_LEN\_RANGE. The plaintext and ciphertext can be in the same place, i.e., it is OK if *pPlaintext* and *pCiphertext* point to the same location.

For most mechanisms, **C\_EncryptMessage** is equivalent to **C\_EncryptMessageBegin** followed by a sequence of **C\_EncryptMessageNext** operations.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

### 5.9.3 C\_EncryptMessageBegin

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptMessageBegin)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pAssociatedData,

CK\_ULONG ulAssociatedDataLen

);

**C\_EncryptMessageBegin** begins a multiple-part message encryption operation. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message encryption operation*; pAssociatedData* and *ulAssociatedDataLen* specify the associated data for an AEAD mechanism.

Typically, *pParameter* is an initialization vector (IV) or nonce. Depending on the mechanism parameter passed to **C\_MessageEncryptInit**, *pParameter* may be either an input or an output parameter. For example, if the mechanism parameter specifies an IV generator mechanism, the IV generated by the IV generator will be output to the *pParameter* buffer.

If the mechanism is not AEAD, *pAssociatedData* and *ulAssociatedDataLen* are not used and should be set to (NULL, 0).

After calling **C\_EncryptMessageBegin**, the application should call **C\_EncryptMessageNext** one or more times to encrypt the message in multiple parts. The message encryption operation is active until the application uses a call to **C\_EncryptMessageNext** with flags=CKF\_END\_OF\_MESSAGE to actually obtain the final piece of ciphertext. To process additional messages (in single or multiple parts), the application MUST call **C\_EncryptMessage** or **C\_EncryptMessageBegin** again.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.9.4 C\_EncryptMessageNext

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptMessageNext)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pPlaintextPart,

CK\_ULONG ulPlaintextPartLen,

CK\_BYTE\_PTR pCiphertextPart,

CK\_ULONG\_PTR pulCiphertextPartLen,

CK\_FLAGS flags

);

**C\_EncryptMessageNext** continues a multiple-part message encryption operation, processing another message part. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message encryption operation; *pPlaintextPart* points to the plaintext message part; *ulPlaintextPartLen* is the length of the plaintext message part; *pCiphertextPart* points to the location that receives the encrypted message part; *pulCiphertextPartLen* points to the location that holds the length in bytes of the encrypted message part;flags is set to 0 if there is more plaintext data to follow, or set to CKF\_END\_OF\_MESSAGE if this is the last plaintext part.

Typically, *pParameter* is an initialization vector (IV) or nonce. Depending on the mechanism parameter passed to **C\_EncryptMessageNext**, *pParameter* may be either an input or an output parameter. For example, if the mechanism parameter specifies an IV generator mechanism, the IV generated by the IV generator will be output to the *pParameter* buffer.

**C\_EncryptMessageNext** uses the convention described in Section 5.2 on producing output.

The message encryption operation MUST have been started with **C\_EncryptMessageBegin**. This function may be called any number of times in succession. A call to C\_EncryptMessageNext with flags=0 which results in an error other than CKR\_BUFFER\_TOO\_SMALL terminates the current message encryption operation. A call to **C\_EncryptMessageNext** with flags=CKF\_END\_OF\_MESSAGE always terminates the active message encryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (i.e., one which returns **CKR\_OK**) to determine the length of the buffer needed to hold the ciphertext.

Although the last **C\_EncryptMessageNext** call ends the encryption of a message, it does not finish the message-based encryption process. Additional **C\_EncryptMessage** or **C\_EncryptMessageBegin** and **C\_EncryptMessageNext** calls may be made on the session.

The plaintext and ciphertext can be in the same place, i.e., it is OK if *pPlaintextPart* and *pCiphertextPart* point to the same location.

For some multi-part encryption mechanisms, the input plaintext data has certain length constraints, because the mechanism’s input data MUST consist of an integral number of blocks. If these constraints are not satisfied when the final message part is supplied (i.e., with flags=CKF\_END\_OF\_MESSAGE), then **C\_EncryptMessageNext** will fail with return code CKR\_DATA\_LEN\_RANGE.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

### 5.9.5 C\_ MessageEncryptFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_EncryptMessageNext)(

CK\_SESSION\_HANDLE hSession

);

**C\_MessageEncryptFinal** finishes a message-based encryption process. hSession is the session’s handle.

The message-based encryption process MUST have been initialized with **C\_MessageEncryptInit**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR,

CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

#define PLAINTEXT\_BUF\_SZ 200

#define AUTH\_BUF\_SZ 100

#define CIPHERTEXT\_BUF\_SZ 256

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_BYTE iv\[\] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 };

CK\_BYTE tag\[16\];

CK\_GCM\_MESSAGE\_PARAMS gcmParams = {

iv,

sizeof(iv) \* 8,

0,

CKG\_NO\_GENERATE,

tag,

sizeof(tag) \* 8

};

CK\_MECHANISM mechanism = {

CKM\_AES\_GCM, &gcmParams, sizeof(gcmParams)

};

CK\_BYTE data\[2\]\[PLAINTEXT\_BUF\_SZ\];

CK\_BYTE auth\[2\]\[AUTH\_BUF\_SZ\];

CK\_BYTE encryptedData\[2\]\[CIPHERTEXT\_BUF\_SZ\];

CK\_ULONG ulEncryptedDataLen, ulFirstEncryptedDataLen;

CK\_ULONG firstPieceLen = PLAINTEXT\_BUF\_SZ / 2;

/\* error handling is omitted for better readability \*/

.

.

C\_MessageEncryptInit(hSession, &mechanism, hKey);

/\* encrypt message en bloc with given IV \*/

ulEncryptedDataLen = sizeof(encryptedData\[0\]);

C\_EncryptMessage(hSession,

&gcmParams, sizeof(gcmParams),

&auth\[0\]\[0\], sizeof(auth\[0\]),

&data\[0\]\[0\], sizeof(data\[0\]),

&encryptedData\[0\]\[0\], &ulEncryptedDataLen);

/\* iv and tag are set now for message \*/

/\* encrypt message in two steps with generated IV \*/

gcmParams.ivGenerator = CKG\_GENERATE;

C\_EncryptMessageBegin(hSession,

&gcmParams, sizeof(gcmParams),

&auth\[1\]\[0\], sizeof(auth\[1\])

);

/\* encrypt first piece \*/

ulFirstEncryptedDataLen = sizeof(encryptedData\[1\]);

C\_EncryptMessageNext(hSession,

&gcmParams, sizeof(gcmParams),

&data\[1\]\[0\], firstPieceLen,

&encryptedData\[1\]\[0\], &ulFirstEncryptedDataLen,

0

);

/\* encrypt second piece \*/

ulEncryptedDataLen = sizeof(encryptedData\[1\]) - ulFirstEncryptedDataLen;

C\_EncryptMessageNext(hSession,

&gcmParams, sizeof(gcmParams),

&data\[1\]\[firstPieceLen\], sizeof(data\[1\])-firstPieceLen,

&encryptedData\[1\]\[ulFirstEncryptedDataLen\], &ulEncryptedDataLen,

CKF\_END\_OF\_MESSAGE

);

/\* tag is set now for message \*/

/\* finalize \*/

C\_MessageEncryptFinal(hSession);

## 5.10 Decryption functions

Cryptoki provides the following functions for decrypting data:

### 5.10.1 C\_DecryptInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_DecryptInit** initializes a decryption operation. *hSession* is the session’s handle; *pMechanism* points to the decryption mechanism; *hKey* is the handle of the decryption key.

The **CKA\_DECRYPT** attribute of the decryption key, which indicates whether the key supports decryption, MUST be CK\_TRUE.

After calling **C\_DecryptInit**, the application can either call **C\_Decrypt** to decrypt data in a single part; or call **C\_DecryptUpdate** zero or more times, followed by **C\_DecryptFinal**, to decrypt data in multiple parts. The decryption operation is active until the application uses a call to **C\_Decrypt** or **C\_DecryptFinal** *to actually obtain* the final piece of plaintext. To process additional data (in single or multiple parts), the application MUST call **C\_DecryptInit** again.

**C\_DecryptInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active decryption operation. If an active operation cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_DecryptFinal**.

### 5.10.2 C\_Decrypt

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Decrypt)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pEncryptedData,  
CK\_ULONG ulEncryptedDataLen,  
CK\_BYTE\_PTR pData,  
CK\_ULONG\_PTR pulDataLen  
);

**C\_Decrypt** decrypts encrypted data in a single part. *hSession* is the session’s handle; *pEncryptedData* points to the encrypted data; *ulEncryptedDataLen* is the length of the encrypted data; *pData* points to the location that receives the recovered data; *pulDataLen* points to the location that holds the length of the recovered data.

**C\_Decrypt** uses the convention described in Section 5.2 on producing output.

The decryption operation MUST have been initialized with **C\_DecryptInit**. A call to **C\_Decrypt** always terminates the active decryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the plaintext.

**C\_Decrypt** cannot be used to terminate a multi-part operation, and MUST be called after **C\_DecryptInit** without intervening **C\_DecryptUpdate** calls.

The ciphertext and plaintext can be in the same place, *i.e.*, it is OK if *pEncryptedData* and *pData* point to the same location.

If the input ciphertext data cannot be decrypted because it has an inappropriate length, then either CKR\_ENCRYPTED\_DATA\_INVALID or CKR\_ENCRYPTED\_DATA\_LEN\_RANGE may be returned.

For most mechanisms, **C\_Decrypt** is equivalent to a sequence of **C\_DecryptUpdate** operations followed by **C\_DecryptFinal**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example: see **C\_DecryptFinal** for an example of similar functions.

### 5.10.3 C\_DecryptUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG ulEncryptedPartLen,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG\_PTR pulPartLen  
);

**C\_DecryptUpdate** continues a multiple-part decryption operation, processing another encrypted data part. *hSession* is the session’s handle; *pEncryptedPart* points to the encrypted data part; *ulEncryptedPartLen* is the length of the encrypted data part; *pPart* points to the location that receives the recovered data part; *pulPartLen* points to the location that holds the length of the recovered data part.

**C\_DecryptUpdate** uses the convention described in Section 5.2 on producing output.

The decryption operation MUST have been initialized with **C\_DecryptInit**. This function may be called any number of times in succession. A call to **C\_DecryptUpdate** which results in an error other than CKR\_BUFFER\_TOO\_SMALL terminates the current decryption operation.

The ciphertext and plaintext can be in the same place, *i.e.*, it is OK if *pEncryptedPart* and *pPart* point to the same location.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example: See **C\_DecryptFinal**.

### 5.10.4 C\_DecryptFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptFinal)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pLastPart,  
CK\_ULONG\_PTR pulLastPartLen  
);

**C\_DecryptFinal** finishes a multiple-part decryption operation. *hSession* is the session’s handle; *pLastPart* points to the location that receives the last recovered data part, if any; *pulLastPartLen* points to the location that holds the length of the last recovered data part.

**C\_DecryptFinal** uses the convention described in Section 5.2 on producing output.

The decryption operation MUST have been initialized with **C\_DecryptInit**. A call to **C\_DecryptFinal** always terminates the active decryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the plaintext.

If the input ciphertext data cannot be decrypted because it has an inappropriate length, then either CKR\_ENCRYPTED\_DATA\_INVALID or CKR\_ENCRYPTED\_DATA\_LEN\_RANGE may be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

#define CIPHERTEXT\_BUF\_SZ 256

#define PLAINTEXT\_BUF\_SZ 256

CK\_ULONG firstEncryptedPieceLen, secondEncryptedPieceLen;

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM mechanism = {

CKM\_DES\_CBC\_PAD, iv, sizeof(iv)

};

CK\_BYTE data\[PLAINTEXT\_BUF\_SZ\];

CK\_BYTE encryptedData\[CIPHERTEXT\_BUF\_SZ\];

CK\_ULONG ulData1Len, ulData2Len, ulData3Len;

CK\_RV rv;

.

.

firstEncryptedPieceLen = 90;

secondEncryptedPieceLen = CIPHERTEXT\_BUF\_SZ-firstEncryptedPieceLen;

rv = C\_DecryptInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

/\* Decrypt first piece \*/

ulData1Len = sizeof(data);

rv = C\_DecryptUpdate(

hSession,

&encryptedData\[0\], firstEncryptedPieceLen,

&data\[0\], &ulData1Len);

if (rv!= CKR\_OK) {

.

.

}

/\* Decrypt second piece \*/

ulData2Len = sizeof(data)-ulData1Len;

rv = C\_DecryptUpdate(

hSession,

&encryptedData\[firstEncryptedPieceLen\],

secondEncryptedPieceLen,

&data\[ulData1Len\], &ulData2Len);

if (rv!= CKR\_OK) {

.

.

}

/\* Get last little decrypted bit \*/

ulData3Len = sizeof(data)-ulData1Len-ulData2Len;

rv = C\_DecryptFinal(

hSession,

&data\[ulData1Len+ulData2Len\], &ulData3Len);

if (rv!= CKR\_OK) {

.

.

}

}

## 5.11 Message-based decryption functions

Message-based decryption refers to the process of decrypting multiple encrypted messages using the same decryption mechanism and decryption key. The decryption mechanism can be either an authenticated encryption with associated data (AEAD) algorithm or a pure encryption algorithm.

Cryptoki provides the following functions for message-based decryption.

### 5.11.1 C\_MessageDecryptInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageDecryptInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,

CK\_OBJECT\_HANDLE hKey  
);

**C\_MessageDecryptInit** initializes a message-based decryption process, preparing a session for one or more decryption operations that use the same decryption mechanism and decryption key. *hSession* is the session’s handle; *pMechanism* points to the decryption mechanism; *hKey* is the handle of the decryption key.

The CKA\_DECRYPT attribute of the decryption key, which indicates whether the key supports decryption, MUST be CK\_TRUE.

After calling **C\_MessageDecryptInit**, the application can either call **C\_DecryptMessage** to decrypt an encrypted message in a single part; or call **C\_DecryptMessageBegin**, followed by **C\_DecryptMessageNext** one or more times, to decrypt an encrypted message in multiple parts. This may be repeated several times. The message-based decryption process is active until the application uses a call to **C\_MessageDecryptFinal** to finish the message-based decryption process.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

### 5.11.2 C\_DecryptMessage

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptMessage)(  
CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pAssociatedData,

CK\_ULONG ulAssociatedDataLen,

CK\_BYTE\_PTR pCiphertext,

CK\_ULONG ulCiphertextLen,

CK\_BYTE\_PTR pPlaintext,

CK\_ULONG\_PTR pulPlaintextLen

);

**C\_DecryptMessage** decrypts an encrypted message in a single part. *hSession* is the session’s handle;*pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message decryption operation; *pAssociatedData* and *ulAssociatedDataLen* specify the associated data for an AEAD mechanism; *pCiphertext* points to the encrypted message; *ulCiphertextLen* is the length of the encrypted message; *pPlaintext* points to the location that receives the recovered message; *pulPlaintextLen* points to the location that holds the length of the recovered message.

Typically, *pParameter* is an initialization vector (IV) or nonce. Unlike the *pParameter* parameter of **C\_EncryptMessage**, *pParameter* is always an input parameter.

If the decryption mechanism is not AEAD, *pAssociatedData* and *ulAssociatedDataLen* are not used and should be set to (NULL, 0).

**C\_DecryptMessage** uses the convention described in Section 5.2 on producing output.

The message-based decryption process MUST have been initialized with **C\_MessageDecryptInit**. A call to **C\_DecryptMessage** begins and terminates a message decryption operation.

**C\_DecryptMessage** cannot be called in the middle of a multi-part message decryption operation.

The ciphertext and plaintext can be in the same place, i.e., it is OK if *pCiphertext* and *pPlaintext* point to the same location.

If the input ciphertext data cannot be decrypted because it has an inappropriate length, then either CKR\_ENCRYPTED\_DATA\_INVALID or CKR\_ENCRYPTED\_DATA\_LEN\_RANGE may be returned.

If the decryption mechanism is an AEAD algorithm and the authenticity of the associated data or ciphertext cannot be verified, then CKR\_AEAD\_DECRYPT\_FAILED is returned.

For most mechanisms, **C\_DecryptMessage** is equivalent to **C\_DecryptMessageBegin** followed by a sequence of **C\_DecryptMessageNext** operations.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_AEAD\_DECRYPT\_FAILED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

### 5.11.3 C\_DecryptMessageBegin

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptMessageBegin)(  
CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pAssociatedData,

CK\_ULONG ulAssociatedDataLen

);

**C\_DecryptMessageBegin** begins a multiple-part message decryption operation. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message decryption operation; *pAssociatedData* and *ulAssociatedDataLen* specify the associated data for an AEAD mechanism.

Typically, *pParameter* is an initialization vector (IV) or nonce. Unlike the *pParameter* parameter of **C\_EncryptMessageBegin**, *pParameter* is always an input parameter.

If the decryption mechanism is not AEAD, *pAssociatedData* and *ulAssociatedDataLen* are not used and should be set to (NULL, 0).

After calling **C\_DecryptMessageBegin**, the application should call **C\_DecryptMessageNext** one or more times to decrypt the encrypted message in multiple parts. The message decryption operation is active until the application uses a call to **C\_DecryptMessageNext** with flags=CKF\_END\_OF\_MESSAGE to actually obtain the final piece of plaintext. To process additional encrypted messages (in single or multiple parts), the application MUST call **C\_DecryptMessage** or **C\_DecryptMessageBegin** again.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.11.4 C\_DecryptMessageNext

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptMessageNext)(  
CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pCiphertextPart,

CK\_ULONG ulCiphertextPartLen,

CK\_BYTE\_PTR pPlaintextPart,

CK\_ULONG\_PTR pulPlaintextPartLen,

CK\_FLAGS flags

);

**C\_DecryptMessageNext** continues a multiple-part message decryption operation, processing another encrypted message part. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message decryption operation; *pCiphertextPart* points to the encrypted message part; *ulCiphertextPartLen* is the length of the encrypted message part; *pPlaintextPart* points to the location that receives the recovered message part; *pulPlaintextPartLen* points to the location that holds the length of the recovered message part;flags is set to 0 if there is more ciphertext data to follow, or set to CKF\_END\_OF\_MESSAGE if this is the last ciphertext part.

Typically, *pParameter* is an initialization vector (IV) or nonce. Unlike the *pParameter* parameter of **C\_EncryptMessageNext**, *pParameter* is always an input parameter.

**C\_DecryptMessageNext** uses the convention described in Section 5.2 on producing output.

The message decryption operation MUST have been started with **C\_DecryptMessageBegin.** This function may be called any number of times in succession. A call to **C\_DecryptMessageNext** with flags=0 which results in an error other than CKR\_BUFFER\_TOO\_SMALL terminates the current message decryption operation. A call to **C\_DecryptMessageNext** with flags=CKF\_END\_OF\_MESSAGE always terminates the active message decryption operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (i.e., one which returns CKR\_OK) to determine the length of the buffer needed to hold the plaintext.

The ciphertext and plaintext can be in the same place, i.e., it is OK if *pCiphertextPart* and *pPlaintextPart* point to the same location.

Although the last **C\_DecryptMessageNext** call ends the decryption of a message, it does not finish the message-based decryption process. Additional **C\_DecryptMessage** or **C\_DecryptMessageBegin** and **C\_DecryptMessageNext c** alls may be made on the session.

If the input ciphertext data cannot be decrypted because it has an inappropriate length, then either CKR\_ENCRYPTED\_DATA\_INVALID or CKR\_ENCRYPTED\_DATA\_LEN\_RANGE may be returned by the last **C\_DecryptMessageNext** call.

If the decryption mechanism is an AEAD algorithm and the authenticity of the associated data or ciphertext cannot be verified, then CKR\_AEAD\_DECRYPT\_FAILED is returned by the last **C\_DecryptMessageNext** call.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_AEAD\_DECRYPT\_FAILED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.11.5 C\_MessageDecryptFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageDecryptFinal)(  
CK\_SESSION\_HANDLE hSession  
);

**C\_MessageDecryptFinal** finishes a message-based decryption process. *hSession* is the session’s handle.

The message-based decryption process MUST have been initialized with **C\_MessageDecryptInit.**

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

## 5.12 Message digesting functions

Cryptoki provides the following functions for digesting data:

### 5.12.1 C\_DigestInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DigestInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism  
);

**C\_DigestInit** initializes a message-digesting operation. *hSession* is the session’s handle; *pMechanism* points to the digesting mechanism.

After calling **C\_DigestInit**, the application can either call **C\_Digest** to digest data in a single part; or call **C\_DigestUpdate** zero or more times, followed by **C\_DigestFinal**, to digest data in multiple parts. The message-digesting operation is active until the application uses a call to **C\_Digest** or **C\_DigestFinal** *to actually obtain* the message digest. To process additional data (in single or multiple parts), the application MUST call **C\_DigestInit** again.

**C\_DigestInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active message-digesting operation. If an operation has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_DigestFinal**.

### 5.12.2 C\_Digest

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Digest)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pData,  
CK\_ULONG ulDataLen,  
CK\_BYTE\_PTR pDigest,  
CK\_ULONG\_PTR pulDigestLen  
);

**C\_Digest** digests data in a single part. *hSession* is the session’s handle, *pData* points to the data; *ulDataLen* is the length of the data; *pDigest* points to the location that receives the message digest; *pulDigestLen* points to the location that holds the length of the message digest.

**C\_Digest** uses the convention described in Section 5.2 on producing output.

The digest operation MUST have been initialized with **C\_DigestInit**. A call to **C\_Digest** always terminates the active digest operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the message digest.

**C\_Digest** cannot be used to terminate a multi-part operation, and MUST be called after **C\_DigestInit** without intervening **C\_DigestUpdate** calls.

The input data and digest output can be in the same place, *i.e.*, it is OK if *pData* and *pDigest* point to the same location.

**C\_Digest** is equivalent to a sequence of **C\_DigestUpdate** operations followed by **C\_DigestFinal**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_DigestFinal** for an example of similar functions.

### 5.12.3 C\_DigestUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DigestUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen  
);

**C\_DigestUpdate** continues a multiple-part message-digesting operation, processing another data part. *hSession* is the session’s handle, *pPart* points to the data part; *ulPartLen* is the length of the data part.

The message-digesting operation MUST have been initialized with **C\_DigestInit**. Calls to this function and **C\_DigestKey** may be interspersed any number of times in any order. A call to **C\_DigestUpdate** which results in an error terminates the current digest operation.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_DigestFinal**.

### 5.12.4 C\_DigestKey

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DigestKey)(  
CK\_SESSION\_HANDLE hSession,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_DigestKey** continues a multiple-part message-digesting operation by digesting the value of a secret key. *hSession* is the session’s handle; *hKey* is the handle of the secret key to be digested.

The message-digesting operation MUST have been initialized with **C\_DigestInit**. Calls to this function and **C\_DigestUpdate** may be interspersed any number of times in any order.

If the value of the supplied key cannot be digested purely for some reason related to its length, **C\_DigestKey** should return the error code CKR\_KEY\_SIZE\_RANGE.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_INDIGESTIBLE, CKR\_KEY\_SIZE\_RANGE, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example: see **C\_DigestFinal**.

### 5.12.5 C\_DigestFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DigestFinal)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pDigest,  
CK\_ULONG\_PTR pulDigestLen  
);

**C\_DigestFinal** finishes a multiple-part message-digesting operation, returning the message digest. *hSession* is the session’s handle; *pDigest* points to the location that receives the message digest; *pulDigestLen* points to the location that holds the length of the message digest.

**C\_DigestFinal** uses the convention described in Section 5.2 on producing output.

The digest operation MUST have been initialized with **C\_DigestInit**. A call to **C\_DigestFinal** always terminates the active digest operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the message digest.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_MD5, NULL\_PTR, 0

};

CK\_BYTE data\[\] = {...};

CK\_BYTE digest\[16\];

CK\_ULONG ulDigestLen;

CK\_RV rv;

.

.

rv = C\_DigestInit(hSession, &mechanism);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_DigestUpdate(hSession, data, sizeof(data));

if (rv!= CKR\_OK) {

.

.

}

rv = C\_DigestKey(hSession, hKey);

if (rv!= CKR\_OK) {

.

.

}

ulDigestLen = sizeof(digest);

rv = C\_DigestFinal(hSession, digest, &ulDigestLen);

.

.

## 5.13 Signing and MACing functions

Cryptoki provides the following functions for signing data (for the purposes of Cryptoki, these operations also encompass message authentication codes).

### 5.13.1 C\_SignInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_SignInit** initializes a signature operation, where the signature is an appendix to the data. *hSession* is the session’s handle; *pMechanism* points to the signature mechanism; *hKey* is the handle of the signature key.

The **CKA\_SIGN** attribute of the signature key, which indicates whether the key supports signatures with appendix, MUST be CK\_TRUE.

After calling **C\_SignInit**, the application can either call **C\_Sign** to sign in a single part; or call **C\_SignUpdate** one or more times, followed by **C\_SignFinal,** to sign data in multiple parts. The signature operation is active until the application uses a call to **C\_Sign** or **C\_SignFinal** *to actually obtain* the signature. To process additional data (in single or multiple parts), the application MUST call **C\_SignInit** again.

**C\_SignInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active signature operation. If an operation has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED,CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_SignFinal**.

### 5.13.2 C\_Sign

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Sign)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pData,  
CK\_ULONG ulDataLen,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG\_PTR pulSignatureLen  
);

**C\_Sign** signs data in a single part, where the signature is an appendix to the data. *hSession* is the session’s handle; *pData* points to the data; *ulDataLen* is the length of the data; *pSignature* points to the location that receives the signature; *pulSignatureLen* points to the location that holds the length of the signature.

**C\_Sign** uses the convention described in Section 5.2 on producing output.

The signing operation MUST have been initialized with **C\_SignInit**. A call to **C\_Sign** always terminates the active signing operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the signature.

**C\_Sign** cannot be used to terminate a multi-part operation, and MUST be called after **C\_SignInit** without intervening **C\_SignUpdate** calls.

For most mechanisms, **C\_Sign** is equivalent to a sequence of **C\_SignUpdate** operations followed by **C\_SignFinal**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_FUNCTION\_REJECTED, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example: see **C\_SignFinal** for an example of similar functions.

### 5.13.3 C\_SignUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen  
);

**C\_SignUpdate** continues a multiple-part signature operation, processing another data part. *hSession* is the session’s handle, *pPart* points to the data part; *ulPartLen* is the length of the data part.

The signature operation MUST have been initialized with **C\_SignInit**. This function may be called any number of times in succession. A call to **C\_SignUpdate** which results in an error terminates the current signature operation.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example: see **C\_SignFinal**.

### 5.13.4 C\_SignFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignFinal)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG\_PTR pulSignatureLen  
);

**C\_SignFinal** finishes a multiple-part signature operation, returning the signature. *hSession* is the session’s handle; *pSignature* points to the location that receives the signature; *pulSignatureLen* points to the location that holds the length of the signature.

**C\_SignFinal** uses the convention described in Section 5.2 on producing output.

The signing operation MUST have been initialized with **C\_SignInit**. A call to **C\_SignFinal** always terminates the active signing operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the signature.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_FUNCTION\_REJECTED, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_DES\_MAC, NULL\_PTR, 0

};

CK\_BYTE data\[\] = {...};

CK\_BYTE mac\[4\];

CK\_ULONG ulMacLen;

CK\_RV rv;

.

.

rv = C\_SignInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

rv = C\_SignUpdate(hSession, data, sizeof(data));

.

.

ulMacLen = sizeof(mac);

rv = C\_SignFinal(hSession, mac, &ulMacLen);

.

.

}

### 5.13.5 C\_SignRecoverInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignRecoverInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_SignRecoverInit** initializes a signature operation, where the data can be recovered from the signature. *hSession* is the session’s handle; *pMechanism* points to the structure that specifies the signature mechanism; *hKey* is the handle of the signature key.

The **CKA\_SIGN\_RECOVER** attribute of the signature key, which indicates whether the key supports signatures where the data can be recovered from the signature, MUST be CK\_TRUE.

After calling **C\_SignRecoverInit**, the application may call **C\_SignRecover** to sign in a single part. The signature operation is active until the application uses a call to **C\_SignRecover** *to actually obtain* the signature. To process additional data in a single part, the application MUST call **C\_SignRecoverInit** again.

**C\_SignRecoverInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active signature with data recovery operation. If an active operation has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_SignRecover**.

### 5.13.6 C\_SignRecover

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignRecover)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pData,  
CK\_ULONG ulDataLen,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG\_PTR pulSignatureLen  
);

**C\_SignRecover** signs data in a single operation, where the data can be recovered from the signature. *hSession* is the session’s handle; *pData* points to the data; *uLDataLen* is the length of the data; *pSignature* points to the location that receives the signature; *pulSignatureLen* points to the location that holds the length of the signature.

**C\_SignRecover** uses the convention described in Section 5.2 on producing output.

The signing operation MUST have been initialized with **C\_SignRecoverInit**. A call to **C\_SignRecover** always terminates the active signing operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the signature.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_RSA\_9796, NULL\_PTR, 0

};

CK\_BYTE data\[\] = {...};

CK\_BYTE signature\[128\];

CK\_ULONG ulSignatureLen;

CK\_RV rv;

.

.

rv = C\_SignRecoverInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

ulSignatureLen = sizeof(signature);

rv = C\_SignRecover(

hSession, data, sizeof(data), signature, &ulSignatureLen);

if (rv == CKR\_OK) {

.

.

}

}

## 5.14 Message-based signing and MACing functions

Message-based signature refers to the process of signing multiple messages using the same signature mechanism and signature key.

Cryptoki provides the following functions for for signing messages (for the purposes of Cryptoki, these operations also encompass message authentication codes).

### 5.14.1 C\_MessageSignInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageSignInit)(

CK\_SESSION\_HANDLE hSession,

CK\_MECHANISM\_PTR pMechanism,

CK\_OBJECT\_HANDLE hKey

);

**C\_MessageSignInit** initializes a message-based signature process, preparing a session for one or more signature operations (where the signature is an appendix to the data) that use the same signature mechanism and signature key. *hSession* is the session’s handle; *pMechanism* points to the signature mechanism; *hKey* is the handle of the signature key.

The **CKA\_SIGN** attribute of the signature key, which indicates whether the key supports signatures with appendix, MUST be CK\_TRUE.

After calling **C\_MessageSignInit**, the application can either call **C\_SignMessage** to sign a message in a single part; or call **C\_SignMessageBegin**, followed by **C\_SignMessageNext** one or more times, to sign a message in multiple parts. This may be repeated several times. The message-based signature process is active until the application calls **C\_MessageSignFinal** to finish the message-based signature process.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED,CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.14.2 C\_SignMessage

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignMessage)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pData,

CK\_ULONG ulDataLen,

CK\_BYTE\_PTR pSignature,

CK\_ULONG\_PTR pulSignatureLen

);

**C\_SignMessage** signs a message in a single part, where the signature is an appendix to the message. **C\_MessageSignInit** must previously been called on the session. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message signature operation; *pData* points to the data; *ulDataLen* is the length of the data; *pSignature* points to the location that receives the signature; *pulSignatureLen* points to the location that holds the length of the signature.

Depending on the mechanism parameter passed to **C\_MessageSignInit**, *pParameter* may be either an input or an output parameter.

**C\_SignMessage** uses the convention described in Section 5.2 on producing output.

The message-based signing process MUST have been initialized with **C\_MessageSignInit**. A call to **C\_SignMessage** begins and terminates a message signing operation unless it returns CKR\_BUFFER\_TOO\_SMALL to determine the length of the buffer needed to hold the signature, or is a successful call (i.e., one which returns CKR\_OK).

**C\_SignMessage** cannot be called in the middle of a multi-part message signing operation.

**C\_SignMessage** does not finish the message-based signing process. Additional **C\_SignMessage** or **C\_SignMessageBegin** and **C\_SignMessageNext** calls may be made on the session.

For most mechanisms, **C\_SignMessage** is equivalent to **C\_SignMessageBegin** followed by a sequence of **C\_SignMessageNext** operations.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_FUNCTION\_REJECTED, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

### 5.14.3 C\_SignMessageBegin

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignMessageBegin)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen

);

**C\_SignMessageBegin** begins a multiple-part message signature operation, where the signature is an appendix to the message. **C\_MessageSignInit** must previously been called on the session. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message signature operation.

Depending on the mechanism parameter passed to **C\_MessageSignInit**, *pParameter* may be either an input or an output parameter.

After calling **C\_SignMessageBegin**, the application should call **C\_SignMessageNext** one or more times to sign the message in multiple parts. The message signature operation is active until the application uses a call to **C\_SignMessageNext** with a non-NULL *pulSignatureLen* to actually obtain the signature. To process additional messages (in single or multiple parts), the application MUST call **C\_SignMessage** or **C\_SignMessageBegin** again.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

### 5.14.4 C\_SignMessageNext

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignMessageNext)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pDataPart,

CK\_ULONG ulDataPartLen,

CK\_BYTE\_PTR pSignature,

CK\_ULONG\_PTR pulSignatureLen

);

**C\_SignMessageNext** continues a multiple-part message signature operation, processing another data part, or finishes a multiple-part message signature operation, returning the signature. *hSession* is the session’s handle, *pDataPart* points to the data part; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message signature operation; *ulDataPartLen* is the length of the data part; *pSignature* points to the location that receives the signature; *pulSignatureLen* points to the location that holds the length of the signature.

The *pulSignatureLen* argument is set to NULL if there is more data part to follow, or set to a non-NULL value (to receive the signature length) if this is the last data part.

**C\_SignMessageNext** uses the convention described in Section 5.2 on producing output.

The message signing operation MUST have been started with **C\_SignMessageBegin**. This function may be called any number of times in succession. A call to **C\_SignMessageNext** with a NULL *pulSignatureLen* which results in an error terminates the current message signature operation. A call to **C\_SignMessageNext** with a non-NULL *pulSignatureLen* always terminates the active message signing operation unless it returns CKR\_BUFFER\_TOO\_SMALL to determine the length of the buffer needed to hold the signature, or is a successful call (i.e., one which returns CKR\_OK).

Although the last **C\_SignMessageNext** call ends the signing of a message, it does not finish the message-based signing process. Additional **C\_SignMessage** or **C\_SignMessageBegin** and **C\_SignMessageNext** calls may be made on the session.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_FUNCTION\_REJECTED, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

### 5.14.5 C\_MessageSignFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageSignFinal)(

CK\_SESSION\_HANDLE hSession

);

**C\_MessageSignFinal** finishes a message-based signing process. *hSession* is the session’s handle.

The message-based signing process MUST have been initialized with **C\_MessageSignInit**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_FUNCTION\_REJECTED, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

## 5.15 Functions for verifying signatures and MACs

Cryptoki provides the following functions for verifying signatures on data (for the purposes of Cryptoki, these operations also encompass message authentication codes):

### 5.15.1 C\_VerifyInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_VerifyInit** initializes a verification operation, where the signature is an appendix to the data. *hSession* is the session’s handle; *pMechanism* points to the structure that specifies the verification mechanism; *hKey* is the handle of the verification key.

The **CKA\_VERIFY** attribute of the verification key, which indicates whether the key supports verification where the signature is an appendix to the data, MUST be CK\_TRUE.

After calling **C\_VerifyInit**, the application can either call **C\_Verify** to verify a signature on data in a single part; or call **C\_VerifyUpdate** one or more times, followed by **C\_VerifyFinal,** to verify a signature on data in multiple parts. The verification operation is active until the application calls **C\_Verify** or **C\_VerifyFinal**. To process additional data (in single or multiple parts), the application MUST call **C\_VerifyInit** again.

**C\_VerifyInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active verification operation. If an active operation has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_VerifyFinal**.

### 5.15.2 C\_Verify

CK\_DECLARE\_FUNCTION(CK\_RV, C\_Verify)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pData,  
CK\_ULONG ulDataLen,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG ulSignatureLen  
);

**C\_Verify** verifies a signature in a single-part operation, where the signature is an appendix to the data. *hSession* is the session’s handle; *pData* points to the data; *ulDataLen* is the length of the data; *pSignature* points to the signature; *ulSignatureLen* is the length of the signature.

The verification operation MUST have been initialized with **C\_VerifyInit**. A call to **C\_Verify** always terminates the active verification operation.

A successful call to **C\_Verify** should return either the value CKR\_OK (indicating that the supplied signature is valid) or CKR\_SIGNATURE\_INVALID (indicating that the supplied signature is invalid). If the signature can be seen to be invalid purely on the basis of its length, then CKR\_SIGNATURE\_LEN\_RANGE should be returned. In any of these cases, the active signing operation is terminated.

**C\_Verify** cannot be used to terminate a multi-part operation, and MUST be called after **C\_VerifyInit** without intervening **C\_VerifyUpdate** calls.

For most mechanisms, **C\_Verify** is equivalent to a sequence of **C\_VerifyUpdate** operations followed by **C\_VerifyFinal**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SIGNATURE\_INVALID, CKR\_SIGNATURE\_LEN\_RANGE, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example: see **C\_VerifyFinal** for an example of similar functions.

### 5.15.3 C\_VerifyUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen  
);

**C\_VerifyUpdate** continues a multiple-part verification operation, processing another data part. *hSession* is the session’s handle, *pPart* points to the data part; *ulPartLen* is the length of the data part.

The verification operation MUST have been initialized with **C\_VerifyInit**. This function may be called any number of times in succession. A call to **C\_VerifyUpdate** which results in an error terminates the current verification operation.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example: see **C\_VerifyFinal**.

### 5.15.4 C\_VerifyFinal

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyFinal)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG ulSignatureLen  
);

**C\_VerifyFinal** finishes a multiple-part verification operation, checking the signature. *hSession* is the session’s handle; *pSignature* points to the signature; *ulSignatureLen* is the length of the signature.

The verification operation MUST have been initialized with **C\_VerifyInit**. A call to **C\_VerifyFinal** always terminates the active verification operation.

A successful call to **C\_VerifyFinal** should return either the value CKR\_OK (indicating that the supplied signature is valid) or CKR\_SIGNATURE\_INVALID (indicating that the supplied signature is invalid). If the signature can be seen to be invalid purely on the basis of its length, then CKR\_SIGNATURE\_LEN\_RANGE should be returned. In any of these cases, the active verifying operation is terminated.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SIGNATURE\_INVALID, CKR\_SIGNATURE\_LEN\_RANGE, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_DES\_MAC, NULL\_PTR, 0

};

CK\_BYTE data\[\] = {...};

CK\_BYTE mac\[4\];

CK\_RV rv;

.

.

rv = C\_VerifyInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

rv = C\_VerifyUpdate(hSession, data, sizeof(data));

.

.

rv = C\_VerifyFinal(hSession, mac, sizeof(mac));

.

.

}

### 5.15.5 C\_VerifyRecoverInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyRecoverInit)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hKey  
);

**C\_VerifyRecoverInit** initializes a signature verification operation, where the data is recovered from the signature. *hSession* is the session’s handle; *pMechanism* points to the structure that specifies the verification mechanism; *hKey* is the handle of the verification key.

The **CKA\_VERIFY\_RECOVER** attribute of the verification key, which indicates whether the key supports verification where the data is recovered from the signature, MUST be CK\_TRUE.

After calling **C\_VerifyRecoverInit**, the application may call **C\_VerifyRecover** to verify a signature on data in a single part. The verification operation is active until the application uses a call to **C\_VerifyRecover** *to actually obtain* the recovered message.

**C\_VerifyRecoverInit** can be called with *pMechanism* set to NULL\_PTR to terminate an active verification with data recovery operation. If an active operations has been initialized and it cannot be cancelled, CKR\_OPERATION\_CANCEL\_FAILED must be returned.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_OPERATION\_CANCEL\_FAILED.

Example: see **C\_VerifyRecover**.

### 5.15.6 C\_VerifyRecover

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyRecover)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pSignature,  
CK\_ULONG ulSignatureLen,  
CK\_BYTE\_PTR pData,  
CK\_ULONG\_PTR pulDataLen  
);

**C\_VerifyRecover** verifies a signature in a single-part operation, where the data is recovered from the signature. *hSession* is the session’s handle; *pSignature* points to the signature; *ulSignatureLen* is the length of the signature; *pData* points to the location that receives the recovered data; and *pulDataLen* points to the location that holds the length of the recovered data.

**C\_VerifyRecover** uses the convention described in Section 5.2 on producing output.

The verification operation MUST have been initialized with **C\_VerifyRecoverInit**. A call to **C\_VerifyRecover** always terminates the active verification operation unless it returns CKR\_BUFFER\_TOO\_SMALL or is a successful call (*i.e.*, one which returns CKR\_OK) to determine the length of the buffer needed to hold the recovered data.

A successful call to **C\_VerifyRecover** should return either the value CKR\_OK (indicating that the supplied signature is valid) or CKR\_SIGNATURE\_INVALID (indicating that the supplied signature is invalid). If the signature can be seen to be invalid purely on the basis of its length, then CKR\_SIGNATURE\_LEN\_RANGE should be returned. The return codes CKR\_SIGNATURE\_INVALID and CKR\_SIGNATURE\_LEN\_RANGE have a higher priority than the return code CKR\_BUFFER\_TOO\_SMALL, *i.e.*, if **C\_VerifyRecover** is supplied with an invalid signature, it will never return CKR\_BUFFER\_TOO\_SMALL.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SIGNATURE\_LEN\_RANGE, CKR\_SIGNATURE\_INVALID, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_RSA\_9796, NULL\_PTR, 0

};

CK\_BYTE data\[\] = {...};

CK\_ULONG ulDataLen;

CK\_BYTE signature\[128\];

CK\_RV rv;

.

.

rv = C\_VerifyRecoverInit(hSession, &mechanism, hKey);

if (rv == CKR\_OK) {

ulDataLen = sizeof(data);

rv = C\_VerifyRecover(

hSession, signature, sizeof(signature), data, &ulDataLen);

.

.

}

## 5.16 Message-based functions for verifying signatures and MACs

Message-based verification refers to the process of verifying signatures on multiple messages using the same verification mechanism and verification key.

Cryptoki provides the following functions for verifying signatures on messages (for the purposes of Cryptoki, these operations also encompass message authentication codes).

### 5.16.1 C\_MessageVerifyInit

CK\_DECLARE\_FUNCTION(CK\_RV, C\_MessageVerifyInit)(

CK\_SESSION\_HANDLE hSession,

CK\_MECHANISM\_PTR pMechanism,

CK\_OBJECT\_HANDLE hKey

);

**C\_MessageVerifyInit** initializes a message-based verification process, preparing a session for one or more verification operations (where the signature is an appendix to the data) that use the same verification mechanism and verification key. *hSession* is the session’s handle; *pMechanism* points to the structure that specifies the verification mechanism; *hKey* is the handle of the verification key.

The **CKA\_VERIFY** attribute of the verification key, which indicates whether the key supports verification where the signature is an appendix to the data, MUST be CK\_TRUE.

After calling **C\_MessageVerifyInit**, the application can either call **C\_VerifyMessage** to verify a signature on a message in a single part; or call **C\_VerifyMessageBegin**, followed by **C\_VerifyMessageNext** one or more times, to verify a signature on a message in multiple parts. This may be repeated several times. The message-based verification process is active until the application calls **C\_MessageVerifyFinal** to finish the message-based verification process.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_FUNCTION\_NOT\_PERMITTED, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.16.2 C\_VerifyMessage

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyMessage)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pData,

CK\_ULONG ulDataLen,

CK\_BYTE\_PTR pSignature,

CK\_ULONG ulSignatureLen

);

**C\_VerifyMessage** verifies a signature on a message in a single part operation, where the signature is an appendix to the data. **C\_MessageVerifyInit** must previously been called on the session. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message verification operation; *pData* points to the data; *ulDataLen* is the length of the data; *pSignature* points to the signature; *ulSignatureLen* is the length of the signature.

Unlike the *pParameter* parameter of **C\_SignMessage**, *pParameter* is always an input parameter.

The message-based verification process MUST have been initialized with **C\_MessageVerifyInit**. A call to **C\_VerifyMessage** starts and terminates a message verification operation.

A successful call to **C\_VerifyMessage** should return either the value CKR\_OK (indicating that the supplied signature is valid) or CKR\_SIGNATURE\_INVALID (indicating that the supplied signature is invalid). If the signature can be seen to be invalid purely on the basis of its length, then CKR\_SIGNATURE\_LEN\_RANGE should be returned.

**C\_VerifyMessage** does not finish the message-based verification process. Additional **C\_VerifyMessage** or **C\_VerifyMessageBegin** and **C\_VerifyMessageNext** calls may be made on the session.

For most mechanisms, **C\_VerifyMessage** is equivalent to **C\_VerifyMessageBegin** followed by a sequence of **C\_VerifyMessageNext** operations.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_INVALID, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SIGNATURE\_INVALID, CKR\_SIGNATURE\_LEN\_RANGE, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

### 5.16.3 C\_VerifyMessageBegin

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyMessageBegin)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen

);

**C\_VerifyMessageBegin** begins a multiple-part message verification operation, where the signature is an appendix to the message. **C\_MessageVerifyInit** must previously been called on the session. *hSession* is the session’s handle; *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message verification operation.

Unlike the *pParameter* parameter of **C\_SignMessageBegin**, *pParameter* is always an input parameter.

After calling **C\_VerifyMessageBegin**, the application should call **C\_VerifyMessageNext** one or more times to verify a signature on a message in multiple parts. The message verification operation is active until the application calls **C\_VerifyMessageNext** with a non-NULL *pSignature*. To process additional messages (in single or multiple parts), the application MUST call **C\_VerifyMessage** or **C\_VerifyMessageBegin** again.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

### 5.16.4 C\_VerifyMessageNext

CK\_DECLARE\_FUNCTION(CK\_RV, C\_VerifyMessageNext)(

CK\_SESSION\_HANDLE hSession,

CK\_VOID\_PTR pParameter,

CK\_ULONG ulParameterLen,

CK\_BYTE\_PTR pDataPart,

CK\_ULONG ulDataPartLen,

CK\_BYTE\_PTR pSignature,

CK\_ULONG ulSignatureLen

);

**C\_VerifyMessageNext** continues a multiple-part message verification operation, processing another data part, or finishes a multiple-part message verification operation, checking the signature. *hSession* is the session’s handle, *pParameter* and *ulParameterLen* specify any mechanism-specific parameters for the message verification operation, *pPart* points to the data part; *ulPartLen* is the length of the data part; *pSignature* points to the signature; *ulSignatureLen* is the length of the signature.

The *pSignature* argument is set to NULL if there is more data part to follow, or set to a non-NULL value (pointing to the signature to verify) if this is the last data part.

The message verification operation MUST have been started with **C\_VerifyMessageBegin**. This function may be called any number of times in succession. A call to **C\_VerifyMessageNext** with a NULL *pSignature* which results in an error terminates the current message verification operation. A call to **C\_VerifyMessageNext** with a non-NULL *pSignature* always terminates the active message verification operation.

A successful call to **C\_VerifyMessageNext** with a non-NULL *pSignature* should return either the value CKR\_OK (indicating that the supplied signature is valid) or CKR\_SIGNATURE\_INVALID (indicating that the supplied signature is invalid). If the signature can be seen to be invalid purely on the basis of its length, then CKR\_SIGNATURE\_LEN\_RANGE should be returned. In any of these cases, the active message verifying operation is terminated.

Although the last **C\_VerifyMessageNext** call ends the verification of a message, it does not finish the message-based verification process. Additional **C\_VerifyMessage** or **C\_VerifyMessageBegin** and **C\_VerifyMessageNext** calls may be made on the session.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SIGNATURE\_INVALID, CKR\_SIGNATURE\_LEN\_RANGE, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

### 5.16.5 C\_MessageVerifyFinal

CK\_DECLARE\_FUNCTION(CK\_RV,C\_MessageVerifyFinal)(

CK\_SESSION\_HANDLE hSession

);

**C\_MessageVerifyFinal** finishes a message-based verification process. *hSession* is the session’s handle.

The message-based verification process MUST have been initialized with **C\_MessageVerifyInit**.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_TOKEN\_RESOURCE\_EXCEEDED.

## 5.17 Dual-function cryptographic functions

Cryptoki provides the following functions to perform two cryptographic operations “simultaneously” within a session. These functions are provided so as to avoid unnecessarily passing data back and forth to and from a token.

### 5.17.1 C\_DigestEncryptUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DigestEncryptUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG\_PTR pulEncryptedPartLen  
);

**C\_DigestEncryptUpdate** continues multiple-part digest and encryption operations, processing another data part. *hSession* is the session’s handle; *pPart* points to the data part; *ulPartLen* is the length of the data part; *pEncryptedPart* points to the location that receives the digested and encrypted data part; *pulEncryptedPartLen* points to the location that holds the length of the encrypted data part.

**C\_DigestEncryptUpdate** uses the convention described in Section 5.2 on producing output. If a **C\_DigestEncryptUpdate** call does not produce encrypted output (because an error occurs, or because *pEncryptedPart* has the value NULL\_PTR, or because *pulEncryptedPartLen* is too small to hold the entire encrypted part output), then no plaintext is passed to the active digest operation.

Digest and encryption operations MUST both be active (they MUST have been initialized with **C\_DigestInit** and **C\_EncryptInit,** respectively). This function may be called any number of times in succession, and may be interspersed with **C\_DigestUpdate**, **C\_DigestKey**, and **C\_EncryptUpdate** calls (it would be somewhat unusual to intersperse calls to **C\_DigestEncryptUpdate** with calls to **C\_DigestKey**, however).

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

#define BUF\_SZ 512

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM digestMechanism = {

CKM\_MD5, NULL\_PTR, 0

};

CK\_MECHANISM encryptionMechanism = {

CKM\_DES\_ECB, iv, sizeof(iv)

};

CK\_BYTE encryptedData\[BUF\_SZ\];

CK\_ULONG ulEncryptedDataLen;

CK\_BYTE digest\[16\];

CK\_ULONG ulDigestLen;

CK\_BYTE data\[(2\*BUF\_SZ)+8\];

CK\_RV rv;

int i;

.

.

memset(iv, 0, sizeof(iv));

memset(data, ‘A’, ((2\*BUF\_SZ)+5));

rv = C\_EncryptInit(hSession, &encryptionMechanism, hKey);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_DigestInit(hSession, &digestMechanism);

if (rv!= CKR\_OK) {

.

.

}

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_DigestEncryptUpdate(

hSession,

&data\[0\], BUF\_SZ,

encryptedData, &ulEncryptedDataLen);

.

.

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_DigestEncryptUpdate(

hSession,

&data\[BUF\_SZ\], BUF\_SZ,

encryptedData, &ulEncryptedDataLen);

.

.

/\*

\* The last portion of the buffer needs to be

\* handled with separate calls to deal with

\* padding issues in ECB mode

\*/

/\* First, complete the digest on the buffer \*/

rv = C\_DigestUpdate(hSession, &data\[BUF\_SZ\*2\], 5);

.

.

ulDigestLen = sizeof(digest);

rv = C\_DigestFinal(hSession, digest, &ulDigestLen);

.

.

/\* Then, pad last part with 3 0x00 bytes, and complete encryption \*/

for(i=0;i<3;i++)

data\[((BUF\_SZ\*2)+5)+i\] = 0x00;

/\* Now, get second-to-last piece of ciphertext \*/

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_EncryptUpdate(

hSession,

&data\[BUF\_SZ\*2\], 8,

encryptedData, &ulEncryptedDataLen);

.

.

/\* Get last piece of ciphertext (should have length 0, here) \*/

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_EncryptFinal(hSession, encryptedData, &ulEncryptedDataLen);

.

.

### 5.17.2 C\_DecryptDigestUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptDigestUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG ulEncryptedPartLen,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG\_PTR pulPartLen  
);

**C\_DecryptDigestUpdate** continues a multiple-part combined decryption and digest operation, processing another data part. *hSession* is the session’s handle; *pEncryptedPart* points to the encrypted data part; *ulEncryptedPartLen* is the length of the encrypted data part; *pPart* points to the location that receives the recovered data part; *pulPartLen* points to the location that holds the length of the recovered data part.

**C\_DecryptDigestUpdate** uses the convention described in Section 5.2 on producing output. If a **C\_DecryptDigestUpdate** call does not produce decrypted output (because an error occurs, or because *pPart* has the value NULL\_PTR, or because *pulPartLen* is too small to hold the entire decrypted part output), then no plaintext is passed to the active digest operation.

Decryption and digesting operations MUST both be active (they MUST have been initialized with **C\_DecryptInit** and **C\_DigestInit,** respectively). This function may be called any number of times in succession, and may be interspersed with **C\_DecryptUpdate**, **C\_DigestUpdate**, and **C\_DigestKey** calls (it would be somewhat unusual to intersperse calls to **C\_DigestEncryptUpdate** with calls to **C\_DigestKey**, however).

Use of **C\_DecryptDigestUpdate** involves a pipelining issue that does not arise when using **C\_DigestEncryptUpdate**, the “inverse function” of **C\_DecryptDigestUpdate**. This is because when **C\_DigestEncryptUpdate** is called, precisely the same input is passed to both the active digesting operation and the active encryption operation; however, when **C\_DecryptDigestUpdate** is called, the input passed to the active digesting operation is the *output of* the active decryption operation. This issue comes up only when the mechanism used for decryption performs padding.

In particular, envision a 24-byte ciphertext which was obtained by encrypting an 18-byte plaintext with DES in CBC mode with PKCS padding. Consider an application which will simultaneously decrypt this ciphertext and digest the original plaintext thereby obtained.

After initializing decryption and digesting operations, the application passes the 24-byte ciphertext (3 DES blocks) into **C\_DecryptDigestUpdate**. **C\_DecryptDigestUpdate** returns exactly 16 bytes of plaintext, since at this point, Cryptoki doesn’t know if there’s more ciphertext coming, or if the last block of ciphertext held any padding. These 16 bytes of plaintext are passed into the active digesting operation.

Since there is no more ciphertext, the application calls **C\_DecryptFinal**. This tells Cryptoki that there’s no more ciphertext coming, and the call returns the last 2 bytes of plaintext. However, since the active decryption and digesting operations are linked *only* through the **C\_DecryptDigestUpdate** call, these 2 bytes of plaintext are *not* passed on to be digested.

A call to **C\_DigestFinal**, therefore, would compute the message digest of *the first 16 bytes of the plaintext*, not the message digest of the entire plaintext. It is crucial that, before **C\_DigestFinal** is called, the last 2 bytes of plaintext get passed into the active digesting operation via a **C\_DigestUpdate** call.

Because of this, it is critical that when an application uses a padded decryption mechanism with **C\_DecryptDigestUpdate**, it knows exactly how much plaintext has been passed into the active digesting operation. *Extreme caution is warranted when using a padded decryption mechanism with **C\_DecryptDigestUpdate**.*

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

#define BUF\_SZ 512

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM decryptionMechanism = {

CKM\_DES\_ECB, iv, sizeof(iv)

};

CK\_MECHANISM digestMechanism = {

CKM\_MD5, NULL\_PTR, 0

};

CK\_BYTE encryptedData\[(2\*BUF\_SZ)+8\];

CK\_BYTE digest\[16\];

CK\_ULONG ulDigestLen;

CK\_BYTE data\[BUF\_SZ\];

CK\_ULONG ulDataLen, ulLastUpdateSize;

CK\_RV rv;

.

.

memset(iv, 0, sizeof(iv));

memset(encryptedData, ‘A’, ((2\*BUF\_SZ)+8));

rv = C\_DecryptInit(hSession, &decryptionMechanism, hKey);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_DigestInit(hSession, &digestMechanism);

if (rv!= CKR\_OK){

.

.

}

ulDataLen = sizeof(data);

rv = C\_DecryptDigestUpdate(

hSession,

&encryptedData\[0\], BUF\_SZ,

data, &ulDataLen);

.

.

ulDataLen = sizeof(data);

rv = C\_DecryptDigestUpdate(

hSession,

&encryptedData\[BUF\_SZ\], BUF\_SZ,

data, &ulDataLen);

.

.

/\*

\* The last portion of the buffer needs to be handled with

\* separate calls to deal with padding issues in ECB mode

\*/

/\* First, complete the decryption of the buffer \*/

ulLastUpdateSize = sizeof(data);

rv = C\_DecryptUpdate(

hSession,

&encryptedData\[BUF\_SZ\*2\], 8,

data, &ulLastUpdateSize);

.

.

/\* Get last piece of plaintext (should have length 0, here) \*/

ulDataLen = sizeof(data)-ulLastUpdateSize;

rv = C\_DecryptFinal(hSession, &data\[ulLastUpdateSize\], &ulDataLen);

if (rv!= CKR\_OK) {

.

.

}

/\* Digest last bit of plaintext \*/

rv = C\_DigestUpdate(hSession, data, 5);

if (rv!= CKR\_OK) {

.

.

}

ulDigestLen = sizeof(digest);

rv = C\_DigestFinal(hSession, digest, &ulDigestLen);

if (rv!= CKR\_OK) {

.

.

}

### 5.17.3 C\_SignEncryptUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SignEncryptUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG ulPartLen,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG\_PTR pulEncryptedPartLen  
);

**C\_SignEncryptUpdate** continues a multiple-part combined signature and encryption operation, processing another data part. *hSession* is the session’s handle; *pPart* points to the data part; *ulPartLen* is the length of the data part; *pEncryptedPart* points to the location that receives the digested and encrypted data part; and *pulEncryptedPartLen* points to the location that holds the length of the encrypted data part.

**C\_SignEncryptUpdate** uses the convention described in Section 5.2 on producing output. If a **C\_SignEncryptUpdate** call does not produce encrypted output (because an error occurs, or because *pEncryptedPart* has the value NULL\_PTR, or because *pulEncryptedPartLen* is too small to hold the entire encrypted part output), then no plaintext is passed to the active signing operation.

Signature and encryption operations MUST both be active (they MUST have been initialized with **C\_SignInit** and **C\_EncryptInit,** respectively). This function may be called any number of times in succession, and may be interspersed with **C\_SignUpdate** and **C\_EncryptUpdate** calls.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

#define BUF\_SZ 512

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hEncryptionKey, hMacKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM signMechanism = {

CKM\_DES\_MAC, NULL\_PTR, 0

};

CK\_MECHANISM encryptionMechanism = {

CKM\_DES\_ECB, iv, sizeof(iv)

};

CK\_BYTE encryptedData\[BUF\_SZ\];

CK\_ULONG ulEncryptedDataLen;

CK\_BYTE MAC\[4\];

CK\_ULONG ulMacLen;

CK\_BYTE data\[(2\*BUF\_SZ)+8\];

CK\_RV rv;

int i;

.

.

memset(iv, 0, sizeof(iv));

memset(data, ‘A’, ((2\*BUF\_SZ)+5));

rv = C\_EncryptInit(hSession, &encryptionMechanism, hEncryptionKey);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_SignInit(hSession, &signMechanism, hMacKey);

if (rv!= CKR\_OK) {

.

.

}

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_SignEncryptUpdate(

hSession,

&data\[0\], BUF\_SZ,

encryptedData, &ulEncryptedDataLen);

.

.

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_SignEncryptUpdate(

hSession,

&data\[BUF\_SZ\], BUF\_SZ,

encryptedData, &ulEncryptedDataLen);

.

.

/\*

\* The last portion of the buffer needs to be handled with

\* separate calls to deal with padding issues in ECB mode

\*/

/\* First, complete the signature on the buffer \*/

rv = C\_SignUpdate(hSession, &data\[BUF\_SZ\*2\], 5);

.

.

ulMacLen = sizeof(MAC);

rv = C\_SignFinal(hSession, MAC, &ulMacLen);

.

.

/\* Then pad last part with 3 0x00 bytes, and complete encryption \*/

for(i=0;i<3;i++)

data\[((BUF\_SZ\*2)+5)+i\] = 0x00;

/\* Now, get second-to-last piece of ciphertext \*/

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_EncryptUpdate(

hSession,

&data\[BUF\_SZ\*2\], 8,

encryptedData, &ulEncryptedDataLen);

.

.

/\* Get last piece of ciphertext (should have length 0, here) \*/

ulEncryptedDataLen = sizeof(encryptedData);

rv = C\_EncryptFinal(hSession, encryptedData, &ulEncryptedDataLen);

.

.

### 5.17.4 C\_DecryptVerifyUpdate

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DecryptVerifyUpdate)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pEncryptedPart,  
CK\_ULONG ulEncryptedPartLen,  
CK\_BYTE\_PTR pPart,  
CK\_ULONG\_PTR pulPartLen  
);

**C\_DecryptVerifyUpdate** continues a multiple-part combined decryption and verification operation, processing another data part. *hSession* is the session’s handle; *pEncryptedPart* points to the encrypted data; *ulEncryptedPartLen* is the length of the encrypted data; *pPart* points to the location that receives the recovered data; and *pulPartLen* points to the location that holds the length of the recovered data.

**C\_DecryptVerifyUpdate** uses the convention described in Section 5.2 on producing output. If a **C\_DecryptVerifyUpdate** call does not produce decrypted output (because an error occurs, or because *pPart* has the value NULL\_PTR, or because *pulPartLen* is too small to hold the entire encrypted part output), then no plaintext is passed to the active verification operation.

Decryption and signature operations MUST both be active (they MUST have been initialized with **C\_DecryptInit** and **C\_VerifyInit,** respectively). This function may be called any number of times in succession, and may be interspersed with **C\_DecryptUpdate** and **C\_VerifyUpdate** calls.

Use of **C\_DecryptVerifyUpdate** involves a pipelining issue that does not arise when using **C\_SignEncryptUpdate**, the “inverse function” of **C\_DecryptVerifyUpdate**. This is because when **C\_SignEncryptUpdate** is called, precisely the same input is passed to both the active signing operation and the active encryption operation; however, when **C\_DecryptVerifyUpdate** is called, the input passed to the active verifying operation is the *output of* the active decryption operation. This issue comes up only when the mechanism used for decryption performs padding.

In particular, envision a 24-byte ciphertext which was obtained by encrypting an 18-byte plaintext with DES in CBC mode with PKCS padding. Consider an application which will simultaneously decrypt this ciphertext and verify a signature on the original plaintext thereby obtained.

After initializing decryption and verification operations, the application passes the 24-byte ciphertext (3 DES blocks) into **C\_DecryptVerifyUpdate**. **C\_DecryptVerifyUpdate** returns exactly 16 bytes of plaintext, since at this point, Cryptoki doesn’t know if there’s more ciphertext coming, or if the last block of ciphertext held any padding. These 16 bytes of plaintext are passed into the active verification operation.

Since there is no more ciphertext, the application calls **C\_DecryptFinal**. This tells Cryptoki that there’s no more ciphertext coming, and the call returns the last 2 bytes of plaintext. However, since the active decryption and verification operations are linked *only* through the **C\_DecryptVerifyUpdate** call, these 2 bytes of plaintext are *not* passed on to the verification mechanism.

A call to **C\_VerifyFinal**, therefore, would verify whether or not the signature supplied is a valid signature on *the first 16 bytes of the plaintext*, not on the entire plaintext. It is crucial that, before **C\_VerifyFinal** is called, the last 2 bytes of plaintext get passed into the active verification operation via a **C\_VerifyUpdate** call.

Because of this, it is critical that when an application uses a padded decryption mechanism with **C\_DecryptVerifyUpdate**, it knows exactly how much plaintext has been passed into the active verification operation. *Extreme caution is warranted when using a padded decryption mechanism with **C\_DecryptVerifyUpdate**.*

Return values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DATA\_LEN\_RANGE, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_ENCRYPTED\_DATA\_INVALID, CKR\_ENCRYPTED\_DATA\_LEN\_RANGE, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_NOT\_INITIALIZED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID.

Example:

#define BUF\_SZ 512

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hDecryptionKey, hMacKey;

CK\_BYTE iv\[8\];

CK\_MECHANISM decryptionMechanism = {

CKM\_DES\_ECB, iv, sizeof(iv)

};

CK\_MECHANISM verifyMechanism = {

CKM\_DES\_MAC, NULL\_PTR, 0

};

CK\_BYTE encryptedData\[(2\*BUF\_SZ)+8\];

CK\_BYTE MAC\[4\];

CK\_ULONG ulMacLen;

CK\_BYTE data\[BUF\_SZ\];

CK\_ULONG ulDataLen, ulLastUpdateSize;

CK\_RV rv;

.

.

memset(iv, 0, sizeof(iv));

memset(encryptedData, ‘A’, ((2\*BUF\_SZ)+8));

rv = C\_DecryptInit(hSession, &decryptionMechanism, hDecryptionKey);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_VerifyInit(hSession, &verifyMechanism, hMacKey);

if (rv!= CKR\_OK){

.

.

}

ulDataLen = sizeof(data);

rv = C\_DecryptVerifyUpdate(

hSession,

&encryptedData\[0\], BUF\_SZ,

data, &ulDataLen);

.

.

ulDataLen = sizeof(data);

rv = C\_DecryptVerifyUpdate(

hSession,

&encryptedData\[BUF\_SZ\], BUF\_SZ,

data, &ulDataLen);

.

.

/\*

\* The last portion of the buffer needs to be handled with

\* separate calls to deal with padding issues in ECB mode

\*/

/\* First, complete the decryption of the buffer \*/

ulLastUpdateSize = sizeof(data);

rv = C\_DecryptUpdate(

hSession,

&encryptedData\[BUF\_SZ\*2\], 8,

data, &ulLastUpdateSize);

.

.

/\* Get last little piece of plaintext. Should have length 0 \*/

ulDataLen = sizeof(data)-ulLastUpdateSize;

rv = C\_DecryptFinal(hSession, &data\[ulLastUpdateSize\], &ulDataLen);

if (rv!= CKR\_OK) {

.

.

}

/\* Send last bit of plaintext to verification operation \*/

rv = C\_VerifyUpdate(hSession, data, 5);

if (rv!= CKR\_OK) {

.

.

}

rv = C\_VerifyFinal(hSession, MAC, ulMacLen);

if (rv == CKR\_SIGNATURE\_INVALID) {

.

.

}

## 5.18 Key management functions

Cryptoki provides the following functions for key management:

### 5.18.1 C\_GenerateKey

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GenerateKey)(  
CK\_SESSION\_HANDLE hSession  
CK\_MECHANISM\_PTR pMechanism,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulCount,  
CK\_OBJECT\_HANDLE\_PTR phKey  
);

**C\_GenerateKey** generates a secret key or set of domain parameters, creating a new object. *hSession* is the session’s handle; *pMechanism* points to the generation mechanism; *pTemplate* points to the template for the new key or set of domain parameters; *ulCount* is the number of attributes in the template; *phKey* points to the location that receives the handle of the new key or set of domain parameters.

If the generation mechanism is for domain parameter generation, the **CKA\_CLASS** attribute will have the value CKO\_DOMAIN\_PARAMETERS; otherwise, it will have the value CKO\_SECRET\_KEY.

Since the type of key or domain parameters to be generated is implicit in the generation mechanism, the template does not need to supply a key type. If it does supply a key type which is inconsistent with the generation mechanism, **C\_GenerateKey** fails and returns the error code CKR\_TEMPLATE\_INCONSISTENT. The CKA\_CLASS attribute is treated similarly.

If a call to **C\_GenerateKey** cannot support the precise template supplied to it, it will fail and return without creating an object.

The object created by a successful call to **C\_GenerateKey** will have its **CKA\_LOCAL** attribute set to CK\_TRUE. In addition, the object created will have a value for CKA\_UNIQUE\_ID generated and assigned (See Section 4.4.1).

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_CURVE\_NOT\_SUPPORTED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCOMPLETE, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hKey;

CK\_MECHANISM mechanism = {

CKM\_DES\_KEY\_GEN, NULL\_PTR, 0

};

CK\_RV rv;

.

.

rv = C\_GenerateKey(hSession, &mechanism, NULL\_PTR, 0, &hKey);

if (rv == CKR\_OK) {

.

.

}

### 5.18.2 C\_GenerateKeyPair

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GenerateKeyPair)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_ATTRIBUTE\_PTR pPublicKeyTemplate,  
CK\_ULONG ulPublicKeyAttributeCount,  
CK\_ATTRIBUTE\_PTR pPrivateKeyTemplate,  
CK\_ULONG ulPrivateKeyAttributeCount,  
CK\_OBJECT\_HANDLE\_PTR phPublicKey,  
CK\_OBJECT\_HANDLE\_PTR phPrivateKey  
);

**C\_GenerateKeyPair** generates a public/private key pair, creating new key objects. *hSession* is the session’s handle; *pMechanism* points to the key generation mechanism; *pPublicKeyTemplate* points to the template for the public key; *ulPublicKeyAttributeCount* is the number of attributes in the public-key template; *pPrivateKeyTemplate* points to the template for the private key; *ulPrivateKeyAttributeCount* is the number of attributes in the private-key template; *phPublicKey* points to the location that receives the handle of the new public key; *phPrivateKey* points to the location that receives the handle of the new private key.

Since the types of keys to be generated are implicit in the key pair generation mechanism, the templates do not need to supply key types. If one of the templates does supply a key type which is inconsistent with the key generation mechanism, **C\_GenerateKeyPair** fails and returns the error code CKR\_TEMPLATE\_INCONSISTENT. The CKA\_CLASS attribute is treated similarly.

If a call to **C\_GenerateKeyPair** cannot support the precise templates supplied to it, it will fail and return without creating any key objects.

A call to **C\_GenerateKeyPair** will never create just one key and return. A call can fail, and create no keys; or it can succeed, and create a matching public/private key pair.

The key objects created by a successful call to **C\_GenerateKeyPair** will have their **CKA\_LOCAL** attributes set to CK\_TRUE. In addition, the key objects created will both have values for CKA\_UNIQUE\_ID generated and assigned (See Section 4.4.1).

*Note carefully the order of the arguments to **C\_GenerateKeyPair**. The last two arguments do not have the same order as they did in the original Cryptoki Version 1.0 document. The order of these two arguments has caused some unfortunate confusion.*

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_CURVE\_NOT\_SUPPORTED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_DOMAIN\_PARAMS\_INVALID, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCOMPLETE, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hPublicKey, hPrivateKey;

CK\_MECHANISM mechanism = {

CKM\_RSA\_PKCS\_KEY\_PAIR\_GEN, NULL\_PTR, 0

};

CK\_ULONG modulusBits = 3072;

CK\_BYTE publicExponent\[\] = { 3 };

CK\_BYTE subject\[\] = {...};

CK\_BYTE id\[\] = {123};

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE publicKeyTemplate\[\] = {

{CKA\_ENCRYPT, &true, sizeof(true)},

{CKA\_VERIFY, &true, sizeof(true)},

{CKA\_WRAP, &true, sizeof(true)},

{CKA\_MODULUS\_BITS, &modulusBits, sizeof(modulusBits)},

{CKA\_PUBLIC\_EXPONENT, publicExponent, sizeof (publicExponent)}

};

CK\_ATTRIBUTE privateKeyTemplate\[\] = {

{CKA\_TOKEN, &true, sizeof(true)},

{CKA\_PRIVATE, &true, sizeof(true)},

{CKA\_SUBJECT, subject, sizeof(subject)},

{CKA\_ID, id, sizeof(id)},

{CKA\_SENSITIVE, &true, sizeof(true)},

{CKA\_DECRYPT, &true, sizeof(true)},

{CKA\_SIGN, &true, sizeof(true)},

{CKA\_UNWRAP, &true, sizeof(true)}

};

CK\_RV rv;

rv = C\_GenerateKeyPair(

hSession, &mechanism,

publicKeyTemplate, 5,

privateKeyTemplate, 8,

&hPublicKey, &hPrivateKey);

if (rv == CKR\_OK) {

.

.

}

### 5.18.3 C\_WrapKey

CK\_DECLARE\_FUNCTION(CK\_RV, C\_WrapKey)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hWrappingKey,  
CK\_OBJECT\_HANDLE hKey,  
CK\_BYTE\_PTR pWrappedKey,  
CK\_ULONG\_PTR pulWrappedKeyLen  
);

**C\_WrapKey** wraps (*i.e.*, encrypts) a private or secret key. *hSession* is the session’s handle; *pMechanism* points to the wrapping mechanism; *hWrappingKey* is the handle of the wrapping key; *hKey* is the handle of the key to be wrapped; *pWrappedKey* points to the location that receives the wrapped key; and *pulWrappedKeyLen* points to the location that receives the length of the wrapped key.

**C\_WrapKey** uses the convention described in Section 5.2 on producing output.

The **CKA\_WRAP** attribute of the wrapping key, which indicates whether the key supports wrapping, MUST be CK\_TRUE. The **CKA\_EXTRACTABLE** attribute of the key to be wrapped MUST also be CK\_TRUE.

If the key to be wrapped cannot be wrapped for some token-specific reason, despite its having its **CKA\_EXTRACTABLE** attribute set to CK\_TRUE, then **C\_WrapKey** fails with error code CKR\_KEY\_NOT\_WRAPPABLE. If it cannot be wrapped with the specified wrapping key and mechanism solely because of its length, then **C\_WrapKey** fails with error code CKR\_KEY\_SIZE\_RANGE.

**C\_WrapKey** can be used in the following situations:

· To wrap any secret key with a public key that supports encryption and decryption.

· To wrap any secret key with any other secret key. Consideration MUST be given to key size and mechanism strength or the token may not allow the operation.

· To wrap a private key with any secret key.

Of course, tokens vary in which types of keys can actually be wrapped with which mechanisms.

To partition the wrapping keys so they can only wrap a subset of extractable keys the attribute CKA\_WRAP\_TEMPLATE can be used on the wrapping key to specify an attribute set that will be compared against the attributes of the key to be wrapped. If all attributes match according to the C\_FindObject rules of attribute matching then the wrap will proceed. The value of this attribute is an attribute template and the size is the number of items in the template times the size of CK\_ATTRIBUTE. If this attribute is not supplied then any template is acceptable. If an attribute is not present, it will not be checked. If any attribute mismatch occurs on an attempt to wrap a key then the function SHALL return CKR\_KEY\_HANDLE\_INVALID.

Return Values: CKR\_ARGUMENTS\_BAD, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_NOT\_WRAPPABLE, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_UNEXTRACTABLE, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_WRAPPING\_KEY\_HANDLE\_INVALID, CKR\_WRAPPING\_KEY\_SIZE\_RANGE, CKR\_WRAPPING\_KEY\_TYPE\_INCONSISTENT.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hWrappingKey, hKey;

CK\_MECHANISM mechanism = {

CKM\_DES3\_ECB, NULL\_PTR, 0

};

CK\_BYTE wrappedKey\[8\];

CK\_ULONG ulWrappedKeyLen;

CK\_RV rv;

.

.

ulWrappedKeyLen = sizeof(wrappedKey);

rv = C\_WrapKey(

hSession, &mechanism,

hWrappingKey, hKey,

wrappedKey, &ulWrappedKeyLen);

if (rv == CKR\_OK) {

.

.

}

### 5.18.4 C\_UnwrapKey

CK\_DECLARE\_FUNCTION(CK\_RV, C\_UnwrapKey)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hUnwrappingKey,  
CK\_BYTE\_PTR pWrappedKey,  
CK\_ULONG ulWrappedKeyLen,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulAttributeCount,  
CK\_OBJECT\_HANDLE\_PTR phKey  
);

**C\_UnwrapKey** unwraps (*i.e.* decrypts) a wrapped key, creating a new private key or secret key object. *hSession* is the session’s handle; *pMechanism* points to the unwrapping mechanism; *hUnwrappingKey* is the handle of the unwrapping key; *pWrappedKey* points to the wrapped key; *ulWrappedKeyLen* is the length of the wrapped key; *pTemplate* points to the template for the new key; *ulAttributeCount* is the number of attributes in the template; *phKey* points to the location that receives the handle of the recovered key.

The **CKA\_UNWRAP** attribute of the unwrapping key, which indicates whether the key supports unwrapping, MUST be CK\_TRUE.

The new key will have the **CKA\_ALWAYS\_SENSITIVE** attribute set to CK\_FALSE, and the **CKA\_NEVER\_EXTRACTABLE** attribute set to CK\_FALSE. The **CKA\_EXTRACTABLE** attribute is by default set to CK\_TRUE.

Some mechanisms may modify, or attempt to modify. the contents of the pMechanism structure at the same time that the key is unwrapped.

If a call to **C\_UnwrapKey** cannot support the precise template supplied to it, it will fail and return without creating any key object.

The key object created by a successful call to **C\_UnwrapKey** will have its **CKA\_LOCAL** attribute set to CK\_FALSE. In addition, the object created will have a value for CKA\_UNIQUE\_ID generated and assigned (See Section 4.4.1).

To partition the unwrapping keys so they can only unwrap a subset of keys the attribute CKA\_UNWRAP\_TEMPLATE can be used on the unwrapping key to specify an attribute set that will be added to attributes of the key to be unwrapped. If the attributes do not conflict with the user supplied attribute template, in ‘pTemplate’, then the unwrap will proceed. The value of this attribute is an attribute template and the size is the number of items in the template times the size of CK\_ATTRIBUTE. If this attribute is not present on the unwrapping key then no additional attributes will be added. If any attribute conflict occurs on an attempt to unwrap a key then the function SHALL return CKR\_TEMPLATE\_INCONSISTENT.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_BUFFER\_TOO\_SMALL, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_CURVE\_NOT\_SUPPORTED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_DOMAIN\_PARAMS\_INVALID, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCOMPLETE, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_UNWRAPPING\_KEY\_HANDLE\_INVALID, CKR\_UNWRAPPING\_KEY\_SIZE\_RANGE, CKR\_UNWRAPPING\_KEY\_TYPE\_INCONSISTENT, CKR\_USER\_NOT\_LOGGED\_IN, CKR\_WRAPPED\_KEY\_INVALID, CKR\_WRAPPED\_KEY\_LEN\_RANGE.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hUnwrappingKey, hKey;

CK\_MECHANISM mechanism = {

CKM\_DES3\_ECB, NULL\_PTR, 0

};

CK\_BYTE wrappedKey\[8\] = {...};

CK\_OBJECT\_CLASS keyClass = CKO\_SECRET\_KEY;

CK\_KEY\_TYPE keyType = CKK\_DES;

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE template\[\] = {

{CKA\_CLASS, &keyClass, sizeof(keyClass)},

{CKA\_KEY\_TYPE, &keyType, sizeof(keyType)},

{CKA\_ENCRYPT, &true, sizeof(true)},

{CKA\_DECRYPT, &true, sizeof(true)}

};

CK\_RV rv;

.

.

rv = C\_UnwrapKey(

hSession, &mechanism, hUnwrappingKey,

wrappedKey, sizeof(wrappedKey), template, 4, &hKey);

if (rv == CKR\_OK) {

.

.

}

### 5.18.5 C\_DeriveKey

CK\_DECLARE\_FUNCTION(CK\_RV, C\_DeriveKey)(  
CK\_SESSION\_HANDLE hSession,  
CK\_MECHANISM\_PTR pMechanism,  
CK\_OBJECT\_HANDLE hBaseKey,  
CK\_ATTRIBUTE\_PTR pTemplate,  
CK\_ULONG ulAttributeCount,  
CK\_OBJECT\_HANDLE\_PTR phKey  
);

**C\_DeriveKey** derives a key from a base key, creating a new key object. *hSession* is the session’s handle; *pMechanism* points to a structure that specifies the key derivation mechanism; *hBaseKey* is the handle of the base key; *pTemplate* points to the template for the new key; *ulAttributeCount* is the number of attributes in the template; and *phKey* points to the location that receives the handle of the derived key.

The values of the **CKA\_SENSITIVE**, **CKA\_ALWAYS\_SENSITIVE**, **CKA\_EXTRACTABLE**, and **CKA\_NEVER\_EXTRACTABLE** attributes for the base key affect the values that these attributes can hold for the newly-derived key. See the description of each particular key-derivation mechanism in Section 5.21.2 for any constraints of this type.

If a call to **C\_DeriveKey** cannot support the precise template supplied to it, it will fail and return without creating any key object.

The key object created by a successful call to **C\_DeriveKey** will have its **CKA\_LOCAL** attribute set to CK\_FALSE. In addition, the object created will have a value for CKA\_UNIQUE\_ID generated and assigned (See Section 4.4.1).

Return values: CKR\_ARGUMENTS\_BAD, CKR\_ATTRIBUTE\_READ\_ONLY, CKR\_ATTRIBUTE\_TYPE\_INVALID, CKR\_ATTRIBUTE\_VALUE\_INVALID, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_CURVE\_NOT\_SUPPORTED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_DOMAIN\_PARAMS\_INVALID, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_KEY\_HANDLE\_INVALID, CKR\_KEY\_SIZE\_RANGE, CKR\_KEY\_TYPE\_INCONSISTENT, CKR\_MECHANISM\_INVALID, CKR\_MECHANISM\_PARAM\_INVALID, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_PIN\_EXPIRED, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_READ\_ONLY, CKR\_TEMPLATE\_INCOMPLETE, CKR\_TEMPLATE\_INCONSISTENT, CKR\_TOKEN\_WRITE\_PROTECTED, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_OBJECT\_HANDLE hPublicKey, hPrivateKey, hKey;

CK\_MECHANISM keyPairMechanism = {

CKM\_DH\_PKCS\_KEY\_PAIR\_GEN, NULL\_PTR, 0

};

CK\_BYTE prime\[\] = {...};

CK\_BYTE base\[\] = {...};

CK\_BYTE publicValue\[128\];

CK\_BYTE otherPublicValue\[128\];

CK\_MECHANISM mechanism = {

CKM\_DH\_PKCS\_DERIVE, otherPublicValue, sizeof(otherPublicValue)

};

CK\_ATTRIBUTE template\[\] = {

{CKA\_VALUE, &publicValue, sizeof(publicValue)}

};

CK\_OBJECT\_CLASS keyClass = CKO\_SECRET\_KEY;

CK\_KEY\_TYPE keyType = CKK\_DES;

CK\_BBOOL true = CK\_TRUE;

CK\_ATTRIBUTE publicKeyTemplate\[\] = {

{CKA\_PRIME, prime, sizeof(prime)},

{CKA\_BASE, base, sizeof(base)}

};

CK\_ATTRIBUTE privateKeyTemplate\[\] = {

{CKA\_DERIVE, &true, sizeof(true)}

};

CK\_ATTRIBUTE derivedKeyTemplate\[\] = {

{CKA\_CLASS, &keyClass, sizeof(keyClass)},

{CKA\_KEY\_TYPE, &keyType, sizeof(keyType)},

{CKA\_ENCRYPT, &true, sizeof(true)},

{CKA\_DECRYPT, &true, sizeof(true)}

};

CK\_RV rv;

.

.

rv = C\_GenerateKeyPair(

hSession, &keyPairMechanism,

publicKeyTemplate, 2,

privateKeyTemplate, 1,

&hPublicKey, &hPrivateKey);

if (rv == CKR\_OK) {

rv = C\_GetAttributeValue(hSession, hPublicKey, template, 1);

if (rv == CKR\_OK) {

/\* Put other guy’s public value in otherPublicValue \*/

.

.

rv = C\_DeriveKey(

hSession, &mechanism,

hPrivateKey, derivedKeyTemplate, 4, &hKey);

if (rv == CKR\_OK) {

.

.

}

}

}

## 5.19 Random number generation functions

Cryptoki provides the following functions for generating random numbers:

### 5.19.1 C\_SeedRandom

CK\_DECLARE\_FUNCTION(CK\_RV, C\_SeedRandom)(  
CK\_SESSION\_HANDLE hSession,  
CK\_BYTE\_PTR pSeed,  
CK\_ULONG ulSeedLen  
);

**C\_SeedRandom** mixes additional seed material into the token’s random number generator. *hSession* is the session’s handle; *pSeed* points to the seed material; and *ulSeedLen* is the length in bytes of the seed material.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_RANDOM\_SEED\_NOT\_SUPPORTED, CKR\_RANDOM\_NO\_RNG, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example: see **C\_GenerateRandom**.

### 5.19.2 C\_GenerateRandom

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GenerateRandom)(

CK\_SESSION\_HANDLE hSession,

CK\_BYTE\_PTR pRandomData,

CK\_ULONG ulRandomLen

);

**C\_GenerateRandom** generates random or pseudo-random data. *hSession* is the session’s handle; *pRandomData* points to the location that receives the random data; and *ulRandomLen* is the length in bytes of the random or pseudo-random data to be generated.

Return values: CKR\_ARGUMENTS\_BAD, CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_DEVICE\_ERROR, CKR\_DEVICE\_MEMORY, CKR\_DEVICE\_REMOVED, CKR\_FUNCTION\_CANCELED, CKR\_FUNCTION\_FAILED, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_OK, CKR\_OPERATION\_ACTIVE, CKR\_RANDOM\_NO\_RNG, CKR\_SESSION\_CLOSED, CKR\_SESSION\_HANDLE\_INVALID, CKR\_USER\_NOT\_LOGGED\_IN.

Example:

CK\_SESSION\_HANDLE hSession;

CK\_BYTE seed\[\] = {...};

CK\_BYTE randomData\[\] = {...};

CK\_RV rv;

.

.

rv = C\_SeedRandom(hSession, seed, sizeof(seed));

if (rv!= CKR\_OK) {

.

.

}

rv = C\_GenerateRandom(hSession, randomData, sizeof(randomData));

if (rv == CKR\_OK) {

.

.

}

## 5.20 Parallel function management functions

Cryptoki provides the following functions for managing parallel execution of cryptographic functions. These functions exist only for backwards compatibility.

### 5.20.1 C\_GetFunctionStatus

CK\_DECLARE\_FUNCTION(CK\_RV, C\_GetFunctionStatus)(  
CK\_SESSION\_HANDLE hSession  
);

In previous versions of Cryptoki, **C\_GetFunctionStatus** obtained the status of a function running in parallel with an application. Now, however, **C\_GetFunctionStatus** is a legacy function which should simply return the value CKR\_FUNCTION\_NOT\_PARALLEL.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_FUNCTION\_NOT\_PARALLEL, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_CLOSED.

### 5.20.2 C\_CancelFunction

CK\_DECLARE\_FUNCTION(CK\_RV, C\_CancelFunction)(  
CK\_SESSION\_HANDLE hSession  
);

In previous versions of Cryptoki, **C\_CancelFunction** cancelled a function running in parallel with an application. Now, however, **C\_CancelFunction** is a legacy function which should simply return the value CKR\_FUNCTION\_NOT\_PARALLEL.

Return values: CKR\_CRYPTOKI\_NOT\_INITIALIZED, CKR\_FUNCTION\_FAILED, CKR\_FUNCTION\_NOT\_PARALLEL, CKR\_GENERAL\_ERROR, CKR\_HOST\_MEMORY, CKR\_SESSION\_HANDLE\_INVALID, CKR\_SESSION\_CLOSED.

## 5.21 Callback functions

Cryptoki sessions can use function pointers of type **CK\_NOTIFY** to notify the application of certain events.

### 5.21.1 Surrender callbacks

Cryptographic functions (*i.e.*, any functions falling under one of these categories: encryption functions; decryption functions; message digesting functions; signing and MACing functions; functions for verifying signatures and MACs; dual-purpose cryptographic functions; key management functions; random number generation functions) executing in Cryptoki sessions can periodically surrender control to the application who called them if the session they are executing in had a notification callback function associated with it when it was opened. They do this by calling the session’s callback with the arguments (hSession, CKN\_SURRENDER, pApplication), where hSession is the session’s handle and pApplication was supplied to **C\_OpenSession** when the session was opened. Surrender callbacks should return either the value CKR\_OK (to indicate that Cryptoki should continue executing the function) or the value CKR\_CANCEL (to indicate that Cryptoki should abort execution of the function). Of course, before returning one of these values, the callback function can perform some computation, if desired.

A typical use of a surrender callback might be to give an application user feedback during a lengthy key pair generation operation. Each time the application receives a callback, it could display an additional “.” to the user. It might also examine the keyboard’s activity since the last surrender callback, and abort the key pair generation operation (probably by returning the value CKR\_CANCEL) if the user hit <ESCAPE>.

A Cryptoki library is not *required* to make *any* surrender callbacks.

### 5.21.2 Vendor-defined callbacks

Library vendors can also define additional types of callbacks. Because of this extension capability, application-supplied notification callback routines should examine each callback they receive, and if they are unfamiliar with the type of that callback, they should immediately give control back to the library by returning with the value CKR\_OK.

## 6 PKCS #11 Implementation Conformance

An implementation is a conforming implementation if it meets the conditions specified in one or more server profiles specified in **\[PKCS #11-Prof\]**.

If a PKCS #11 implementation claims support for a particular profile, then the implementation SHALL conform to all normative statements within the clauses specified for that profile and for any subclauses to each of those clauses.

The following individuals have participated in the creation of this specification and are gratefully acknowledged:

Participants:

Benton Stark - Cisco Systems

Anthony Berglas - Cryptsoft Pty Ltd.

Justin Corlett - Cryptsoft Pty Ltd.

Tony Cox - Cryptsoft Pty Ltd.

Tim Hudson - Cryptsoft Pty Ltd.

Bruce Rich - Cryptsoft Pty Ltd.

Greg Scott - Cryptsoft Pty Ltd.

Jason Thatcher - Cryptsoft Pty Ltd.

Magda Zdunkiewicz - Cryptsoft Pty Ltd.

Andrew Byrne - Dell

David Horton - Dell

Kevin Mooney - Fornetix

Gerald Stueve - Fornetix

Charles White - Fornetix

Matt Bauer - Galois, Inc.

Wan-Teh Chang - Google Inc.

Patrick Steuer - IBM

Michele Drgon - Individual

Gershon Janssen - Individual

Oscar So - Individual

Michelle Brochmann - Information Security Corporation

Michael Mrkowitz - Information Security Corporation

Jonathan Schulze-Hewett - Information Security Corporation

Philip Lafrance - ISARA Corporation

Thomas Hardjono - M.I.T.

Hamish Cameron - nCipher

Paul King - nCipher

Sander Temme - nCipher

Chet Ensign - OASIS

Jane Harnad - OASIS

Web Master - OASIS

Dee Schur - OASIS

Xuelei Fan - Oracle

Jan Friedel - Oracle

Susan Gleeson - Oracle

Dina Kurktchi-Nimeh - Oracle

John Leser - Oracle

Darren Moffat - Oracle

Mark Joseph - P6R, Inc

Jim Susoy - P6R, Inc

Roland Bramm - PrimeKey Solutions AB

Warren Armstrong - QuintessenceLabs Pty Ltd.

Kenli Chong - QuintessenceLabs Pty Ltd.

John Leiseboer - QuintessenceLabs Pty Ltd.

Florian Poppa - QuintessenceLabs Pty Ltd.

Martin Shannon - QuintessenceLabs Pty Ltd.

Jakub Jelen - Red Hat

Chris Malafis - Red Hat

Robert Relyea - Red Hat

Christian Bollich - Utimaco IS GmbH

Dieter Bong - Utimaco IS GmbH

Chris Meyer - Utimaco IS GmbH

Daniel Minder - Utimaco IS GmbH

Roland Reichenberg - Utimaco IS GmbH

Manish Upasani - Utimaco IS GmbH

Steven Wierenga - Utimaco IS GmbH

The definitions for manifest constants specified in this document can be found in the following normative computer language definition files:

· [include/pkcs11-v3.00/pkcs11.h](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/include/pkcs11-v3.0/pkcs11.h)

· [include/pkcs11-v3.00/pkcs11t.h](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/include/pkcs11-v3.0/pkcs11t.h)

· [include/pkcs11-v3.00/pkcs11f.h](https://docs.oasis-open.org/pkcs11/pkcs11-base/v3.0/os/include/pkcs11-v3.0/pkcs11f.h)

| **Revision** | **Date** | **Editor** | **Changes Made** |
| --- | --- | --- | --- |
| csprd 02 wd01 | Oct 8 2019 | Dieter Bong | Created csprd02 based on csprd01 |
| csprd 02 wd02 | Nov 8 2019 | Dieter Bong | Item #26 as per “PKCS11 mechnisms review” document |
| csprd 02 wd03 | Dec 3 2019 | Dieter Bong | Changes as per “PKCS11 base spec review” document |
## 相关笔记

- [[RFC 6962 证书透明]]
- [["X.509 公钥基础设施证书与 CRL"]]
- [[密码消息语法 (CMS)]]
- [[TOTP 基于时间的一次性密码算法]]
- [[RFC 6960 在线证书状态协议 OCSP]]
- [[PKCS#12 个人信息交换语法 v1.1]]
- [[RFC 9580 OpenPGP 新版]]
- [[FIPS 180-4 安全哈希标准（SHS）]]
