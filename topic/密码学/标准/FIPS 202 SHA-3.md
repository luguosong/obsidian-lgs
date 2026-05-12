**Official websites use.gov**  
A **.gov** website belongs to an official government organization in the United States.

**Secure.gov websites use HTTPS**  
A **lock** ( <svg xmlns="http://www.w3.org/2000/svg" width="52" height="64" viewBox="0 0 52 64" role="img" aria-labelledby="banner-lock-description-default" focusable="false"><title id="banner-lock-title-default">Lock</title> <desc id="banner-lock-description-default">Locked padlock icon</desc> <path fill="#000000" fill-rule="evenodd" d="M26 0c10.493 0 19 8.507 19 19v9h3a4 4 0 0 1 4 4v28a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V32a4 4 0 0 1 4-4h3v-9C7 8.507 15.507 0 26 0zm0 8c-5.979 0-10.843 4.77-10.996 10.712L15 19v9h22v-9c0-6.075-4.925-11-11-11z"></path></svg> ) or **https://** means you’ve safely connected to the.gov website. Share sensitive information only on official, secure websites.

## SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions

**Planning Note (03/13/2025):**

NIST has decided to update this publication. See this [announcement](https://csrc.nist.gov/pubs/fips/202/68bf317d-a87e-454f-b8f0-35f9d8ab740b) for more details.

---

A typographical error has been identified in (non-normative) Appendix B, on page 26. In the description of Algorithm 10, step 1 begins:

1\. For each integer \\(i\\) such that \\(0 \\leq i < 2m-1, \\dots\\)

but instead the correct notation should be:

1\. For each integer \\(i\\) such that \\(0 \\leq i < 2m, \\dots\\)

This correction will be incorporated in any future revision of this standard.

#### Author(s)

National Institute of Standards and Technology

#### Abstract

This Standard specifies the Secure Hash Algorithm-3 (SHA-3) family of functions on binary data. Each of the SHA-3 functions is based on an instance of the K ECCAK algorithm that NIST selected as the winner of the SHA-3 Cryptographic Hash Algorithm Competition. This Standard also specifies the K ECCAK -p family of mathematical permutations, including the permutation that underlies K ECCAK, in order to facilitate the development of additional permutation-based cryptographic functions. The SHA-3 family consists of four cryptographic hash functions, called SHA3-224, SHA3-256, SHA3-384, and SHA3-512, and two extendable-output functions (XOFs), called SHAKE128 and SHAKE256. Hash functions are components for many important information security applications, including 1) the generation and verification of digital signatures, 2) key derivation, and 3) pseudorandom bit generation. The hash functions specified in this Standard supplement the SHA-1 hash function and the SHA-2 family of hash functions that are specified in FIPS [[180-4]], the Secure Hash Standard. Extendable-output functions are different from hash functions, but it is possible to use them in similar ways, with the flexibility to be adapted directly to the requirements of individual applications, subject to additional security considerations.

This Standard specifies the Secure Hash Algorithm-3 (SHA-3) family of functions on binary data. Each of the SHA-3 functions is based on an instance of the KECCAK algorithm that NIST selected as the winner of the SHA-3 Cryptographic Hash Algorithm Competition. This Standard also specifies the... [See full abstract](#pubs-abstract-header)

#### Keywords

hash function; information security; message digest; permutation; SHA-3; sponge construction; sponge function; cryptography; extendable-output function; Federal Information Processing Standard; KECCAK; XOF; hash algorithm; computer security

##### Control Families

None selected

#### Documentation

**Publication:**  
[https://doi.org/10.6028/NIST.FIPS.202](https://doi.org/10.6028/NIST.FIPS.202)  
[Download URL](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

**Supplemental Material:**  
[Federal Register Notice](https://federalregister.gov/a/2015-19181)  
[Press Release](http://www.nist.gov/itl/csd/201508_sha3.cfm)  
[Comments received on Draft FIPS 202 (pdf)](https://csrc.nist.gov/files/pubs/fips/202/final/docs/fips202-public-comments-aug2014.pdf)  
[Draft FIPS 202 (May 2014) (pdf)](https://csrc.nist.gov/files/pubs/fips/202/final/docs/fips_202_draft.pdf)

**Related NIST Publications:**

**Document History:**  
08/04/15: FIPS 202 (Final)