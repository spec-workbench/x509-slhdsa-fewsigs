---
title: "Internet X.509 Public Key Infrastructure: Algorithm Identifiers for SLH-DSA with a Limited Number of Signatures (SLH-DSA-FEW)"
abbrev: "SLH-DSA-FEW for X.509"
category: std
updates: 9909

docname: draft-kousidis-lamps-x509-slhdsa-fewsigs-latest
submissiontype: IETF
number:
date:
consensus: true
v: 3
area: "Security"
workgroup: "Limited Additional Mechanisms for PKIX and SMIME"
keyword:
 - SLH-DSA
 - SLH-DSA-FEW
 - SP 800-230
 - PQ Signatures
 - post-quantum X.509
venue:
  group: "Limited Additional Mechanisms for PKIX and SMIME"
  type: "Working Group"
  mail: "spasm@ietf.org"
  arch: "https://mailarchive.ietf.org/arch/browse/spasm/"
  github: "spec-workbench/x509-slhdsa-fewsigs"
  latest: "https://spec-workbench.github.io/x509-slhdsa-fewsigs/draft-kousidis-lamps-x509-slhdsa-fewsigs.html"

author:
 -
    fullname: Kaveh Bashiri
    organization: BSI
    email: kaveh.bashiri.ietf@gmail.com
 -
    fullname: Felix Knopp
    organization: BSI
    email: felix.knopp.ietf@proton.me
 -
    fullname: Stavros Kousidis
    organization: TH Köln
    email: kousidis.ietf@gmail.com
 -
    fullname: Daniel Van Geest
    organization: CryptoNext Security
    email: daniel.vangeest@cryptonext-security.com

normative:
  RFC5280:
  RFC5912:
  RFC9909:
  FIPS205:
    target: https://doi.org/10.6028/NIST.FIPS.205
    title: "Stateless Hash-Based Digital Signature Standard"
    author:
    - org: National Institute of Standards and Technology (NIST)
    date: 2024-08-13
    seriesinfo:
      "FIPS PUB": "205"
  SP800-230:
    target: https://doi.org/10.6028/NIST.SP.800-230.ipd
    title: "Additional SLH-DSA Parameter Sets for Limited-Signature Use Cases"
    author:
    - name: Quynh Dang
    - name: Dustin Moody
    date: 2026-04-13
    seriesinfo:
      "NIST SP": "800-230 ipd (Initial Public Draft)"
  CSOR:
    target: https://csrc.nist.gov/projects/computer-security-objects-register/algorithm-registration
    title: Computer Security Objects Register
    author:
    - org: National Institute of Standards and Technology (NIST)
    date: false
  X680:
    target: https://www.itu.int/rec/T-REC-X.680
    title: >
      Information technology - Abstract Syntax Notation One (ASN.1):
      Specification of basic notation
    date: 2021-02
    author:
    -  org: ITU-T
    seriesinfo:
      ITU-T Recommendation: X.680
      ISO/IEC: 8824-1:2021
  X690:
    target: https://www.itu.int/rec/T-REC-X.690
    title: >
      Information technology - Abstract Syntax Notation One (ASN.1):
      ASN.1 encoding rules: Specification of Basic Encoding Rules (BER),
      Canonical Encoding Rules (CER) and Distinguished Encoding Rules (DER)
    date: 2021-02
    author:
    -  org: ITU-T
    seriesinfo:
      ITU-T Recommendation: X.690
      ISO/IEC: 8825-1:2021

informative:
  RFC9814:
  KP22:
    target: https://eprint.iacr.org/2022/1725
    title: "A note on SPHINCS+ parameter sets"
    author:
    - name: Stefan Kölbl
    - name: Jade Philipoom
    date: 2022
    seriesinfo:
      "Cryptology ePrint Archive": "Paper 2022/1725"
  FD24:
    target: https://eprint.iacr.org/2024/018
    title: "Smaller SPHINCS+"
    author:
    - name: Scott Fluhrer
    - name: Quynh Dang
    date: 2024
    seriesinfo:
      "Cryptology ePrint Archive": "Paper 2024/018"

...

--- abstract

RFC 9909 specifies the conventions for using the Stateless Hash-Based
Digital Signature Algorithm (SLH-DSA) in the X.509 Public Key
Infrastructure. NIST SP 800-230 adds six SLH-DSA parameter sets that are
restricted to at most 2^24 signatures per signing key. The security of these parameters depends on adhering to this limit.
This document specifies the algorithm identifiers for these parameter
sets in X.509 and updates RFC 9909 to address the much lower signature
limit.


--- middle

# Introduction {#intro}

{{RFC9909}} defines the conventions for the use of the twelve SLH-DSA
parameter sets of {{FIPS205}} in the X.509 Public Key Infrastructure.
These parameter sets are designed to be secure for up to 2^64 signatures
per key, which is the reason for their large signatures of 7,856 to
49,856 bytes.

{{SP800-230}} specifies six additional parameter sets for NIST security
categories 1, 3, and 5 that reduce signature size and verification time
by limiting a signing key to 2^24 (16,777,216) signatures; see {{KP22}}
and {{FD24}} for background. The resulting signatures are 3,856, 7,752,
and 14,944 bytes long, while signing is less efficient than with the parameter
sets of {{FIPS205}}. If a key is used to generate more than 2^24
signatures, its security is no longer guaranteed to meet the security
category of its parameter set.
{{SP800-230}} names signing of software, firmware, and
digital certificates as the intended use cases, and states that these
parameter sets are not approved for general-purpose use.

This document refers to these additional parameter sets as SLH-DSA-FEW.
The corresponding pure version is referred to as Pure SLH-DSA-FEW, and
the pre-hash version as HashSLH-DSA-FEW. The signature algorithms are
those of {{FIPS205}}; only the parameter sets differ.

This document:

* defines the algorithm identifiers for the six SLH-DSA-FEW parameter
  sets, for both Pure SLH-DSA-FEW and HashSLH-DSA-FEW ({{sec-alg-ids}}),
* specifies how the conventions of {{RFC9909}} apply to them
  ({{sec-use}}),
* defines the associated ASN.1 module ({{sec-asn1}}), and
* updates the Operational Considerations and Security Considerations of
  {{RFC9909}} to address the 2^24 signature limit ({{sec-ops}} and
  {{sec-cons}}).

<aside markdown="block">
EDITOR'S NOTE: Open issues for this version:

* The object identifiers are to be assigned by NIST in {{CSOR}}.
* {{SP800-230}} is an initial public draft. The parameter set names, the
  values in {{tab-strengths}}, and the signature limit need to be
  re-verified against the final publication.
* Whether HashSLH-DSA-FEW identifiers are needed, and whether NIST will
  assign OIDs for them in {{CSOR}}, remains open. Their names, number,
  and pre-hash function pairings in {{sec-alg-ids}} are provisional.
* Whether CMS {{RFC9814}} is covered in this document or a separate one
  is to be discussed in the LAMPS Working Group.
</aside>

## Notation

`id-slh-dsa-*-24`: A shorthand to refer to all six OIDs used to specify the
different parameter combinations for Pure SLH-DSA-FEW.

`id-hash-slh-dsa-*-24-*`: A shorthand to refer to all six OIDs used to
specify the different parameter combinations for HashSLH-DSA-FEW.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

Terms and notation not defined here, such as Pure SLH-DSA and
HashSLH-DSA, are as defined in {{RFC9909}}.


# Algorithm Identifiers {#sec-alg-ids}

The AlgorithmIdentifier type and the meaning of its fields are as
described in {{Section 3 of RFC9909}}.

The object identifiers for the SLH-DSA-FEW parameter sets are to be
defined by NIST in the Computer Security Objects Register {{CSOR}}. The
same algorithm identifiers are used for identifying a public key, a
private key, and a signature. As in {{RFC9909}}, there are separate
identifiers for Pure SLH-DSA-FEW and HashSLH-DSA-FEW.

The Pure SLH-DSA-FEW OIDs are:

~~~ asn.1
   nistAlgorithms OBJECT IDENTIFIER ::= { joint-iso-itu-t(2)
     country(16) us(840) organization(1) gov(101) csor(3) 4 }

   sigAlgs OBJECT IDENTIFIER ::= { nistAlgorithms 3 }

   id-slh-dsa-sha2-128-24 OBJECT IDENTIFIER ::= { sigAlgs TBD1 }

   id-slh-dsa-shake-128-24 OBJECT IDENTIFIER ::= { sigAlgs TBD2 }

   id-slh-dsa-sha2-192-24 OBJECT IDENTIFIER ::= { sigAlgs TBD3 }

   id-slh-dsa-shake-192-24 OBJECT IDENTIFIER ::= { sigAlgs TBD4 }

   id-slh-dsa-sha2-256-24 OBJECT IDENTIFIER ::= { sigAlgs TBD5 }

   id-slh-dsa-shake-256-24 OBJECT IDENTIFIER ::= { sigAlgs TBD6 }
~~~

The HashSLH-DSA-FEW OIDs are:

~~~ asn.1
   id-hash-slh-dsa-sha2-128-24-with-sha256 OBJECT IDENTIFIER ::= {
      sigAlgs TBD7 }

   id-hash-slh-dsa-shake-128-24-with-shake128 OBJECT IDENTIFIER ::= {
      sigAlgs TBD8 }

   id-hash-slh-dsa-sha2-192-24-with-sha512 OBJECT IDENTIFIER ::= {
      sigAlgs TBD9 }

   id-hash-slh-dsa-shake-192-24-with-shake256 OBJECT IDENTIFIER ::= {
      sigAlgs TBD10 }

   id-hash-slh-dsa-sha2-256-24-with-sha512 OBJECT IDENTIFIER ::= {
      sigAlgs TBD11 }

   id-hash-slh-dsa-shake-256-24-with-shake256 OBJECT IDENTIFIER ::= {
      sigAlgs TBD12 }
~~~

Each OID identifies the corresponding parameter set of Table 1 in
{{SP800-230}}; for example, id-slh-dsa-shake-192-24 identifies
SLH-DSA-SHAKE-192-24. The pre-hash functions follow the pairing used in
{{RFC9909}}: SHA-256 for the SHA2 128-bit parameter set, SHA-512 for the
SHA2 192-bit and 256-bit parameter sets, SHAKE128 for the SHAKE 128-bit
parameter set, and SHAKE256 for the SHAKE 192-bit and 256-bit parameter
sets.

<aside markdown="block">
RFC EDITOR: Please replace TBD1 through TBD12 throughout this document
with the values assigned by NIST in {{CSOR}}, and remove this note.
</aside>

The contents of the parameters component for each algorithm MUST be
absent.


# Use in X.509 {#sec-use}

The following sections of {{RFC9909}} apply to the `id-slh-dsa-*-24` and
`id-hash-slh-dsa-*-24-*` object identifiers in the same way as to the
`id-slh-dsa-*` and `id-hash-slh-dsa-*` object identifiers, respectively,
with the sizes in {{tab-strengths}}:

* SLH-DSA Signatures ({{Section 4 of RFC9909}}). Signatures are generated
  and verified with the algorithms of {{FIPS205}} named there, using the
  parameter set identified by the algorithm identifier and the empty
  context string, and are encoded as the raw octet string
  R \|\| SIG_FORS \|\| SIG_HT.
* Subject Public Key Fields ({{Section 5 of RFC9909}}). The
  AlgorithmIdentifier for an SLH-DSA-FEW public key MUST use one of the
  `id-slh-dsa-*-24` or `id-hash-slh-dsa-*-24-*` object identifiers from
  {{sec-alg-ids}}, and its parameters field MUST be absent. The public key
  identifiers are defined in {{sec-asn1}}.
* Key Usage Bits ({{Section 6 of RFC9909}}). The requirements apply to
  certificates that indicate an `id-slh-dsa-*-24` or `id-hash-slh-dsa-*-24-*`
  identifier in the SubjectPublicKeyInfo.
* Private Key Format ({{Section 7 of RFC9909}}). The private key is the
  concatenation SK.seed \|\| SK.prf \|\| PK.seed \|\| PK.root of length
  4*n bytes, where n is 16, 24, or 32, depending on the security
  category.

As in {{RFC9909}}, a key identified by a Pure SLH-DSA-FEW OID is not
permitted to be used with a HashSLH-DSA-FEW OID, and vice versa. A key
pair generated for an SLH-DSA-FEW parameter set MUST NOT be used with
any other parameter set, including the {{FIPS205}} parameter set of the
same security category and hash function.


# Operational Considerations {#sec-ops}

This section is in addition to the Operational Considerations of
{{RFC9909}}, whose note on the very large (2^64) number of signatures
does not apply to SLH-DSA-FEW.

Unlike the parameter sets of {{FIPS205}}, an SLH-DSA-FEW parameter set
limits a single signing key to 2^24 signatures (see {{sec-cons}}). This
limit can be reached in some realistic use cases; for example, a key
that produces one signature per second reaches it in about 194 days.
The Operational Considerations of {{SP800-230}} apply here. In particular, if an application's requirements or operational controls cannot guarantee that the 2^24 signatures limit will be respected, the parameter sets specified in this document must not be used.

SLH-DSA-FEW is not suited for keys that sign on demand in response to
external requests, such as keys used for authentication in interactive
protocols (for example, in TLS handshakes) or OCSP responder keys.
Unless the number of signatures generated with such a key can be
bounded reliably, SLH-DSA-FEW MUST NOT be used for that key.


# Security Considerations {#sec-cons}

The Security Considerations of {{RFC9909}} apply, except as changed
below.

{{RFC9909}} states that an SLH-DSA tree MUST NOT be used for more than
2^64 signing operations. This applies to the parameter sets of
{{FIPS205}} only. A key pair for an SLH-DSA-FEW parameter set MUST NOT
be used for more than 2^24 signing operations.

Beyond 2^24 signatures, the security of the key is no longer guaranteed
to meet the security category listed in {{tab-strengths}}. A relying party
cannot detect that the limit
has been exceeded: neither a certificate nor a signature reveals how many
signatures have been generated with a key, and a forgery made possible
by exceeding the limit is indistinguishable from a genuine signature.
Therefore, before using SLH-DSA-FEW, the operator MUST evaluate the
operational environment of each signing key, taking into account at
least:

* the intended number of signatures signed with the signing key,
* the number of physical or virtual devices that share the signing key,
* the maximum possible speed of each signing operation,
* the projected frequency of signature generation across all devices,
  and
* the intended operational lifetime of the key.

If the evaluation and the operational controls cannot guarantee that no
more than 2^24 signatures will be generated with a key, SLH-DSA-FEW MUST
NOT be used for that key; the parameter sets of {{FIPS205}} can be used
instead.

All signing operations made with the key count against the limit.
For a CA key, this
includes signatures on certificates, CRLs, and, if the CA key is also
used for this purpose, OCSP responses.
Because of this, SLH-DSA-FEW is best suited to keys that sign few
objects, for example a code signing key or a CA key with a low issuance
volume.

According to {{SP800-230}}, caching parts of or the whole SLH-DSA
hypertree to speed up signing is permitted and does not affect the
security properties of the algorithm. Cached values need to be
protected against modification, since corrupted values lead to invalid
signatures.

<aside markdown="block">
EDITOR'S NOTE: Consider quantifying how fast security degrades beyond
2^24 signatures, based on the analysis of {{SP800-230}} or the
literature (e.g., {{KP22}}).
</aside>


# IANA Considerations {#iana}

For the ASN.1 module in {{sec-asn1}}, IANA is requested to assign an
object identifier (OID) for the module identifier (TBD0) with a
Description of "id-mod-x509-slh-dsa-few-2026". The OID for the module
should be allocated in the "SMI Security for PKIX Module Identifier"
registry (1.3.6.1.5.5.7.0).

The object identifiers for the SLH-DSA-FEW parameter sets are assigned
by NIST {{CSOR}} and not by IANA.


--- back

# ASN.1 Module {#sec-asn1}

This appendix includes the ASN.1 module {{X680}} for SLH-DSA-FEW. Note
that as per {{RFC5280}}, certificates use the Distinguished Encoding
Rules; see {{X690}}. This module imports objects from {{RFC5912}}.

~~~ asn.1
<CODE BEGINS>
{::include asn1/X509-SLHDSA-FEW-2026.asn}
<CODE ENDS>
~~~

# Security Strengths

The SLH-DSA-FEW parameter sets are defined for NIST security categories
1, 3, and 5; see {{Appendix B of RFC9909}} for the definition of the
categories. The resulting signature, public key, and private key sizes in
bytes are listed in {{tab-strengths}}. The HashSLH-DSA-FEW parameter
sets have the same values as the Pure SLH-DSA-FEW equivalents. These
parameter sets are only secure for up to 2^24 signatures per key; see
{{sec-cons}}.

| OID                            | NIST Category | Sig.  | Pub. Key | Priv. Key |
|---                             |---            |---    |---       |---        |
| id-(hash-)slh-dsa-sha2-128-24  | 1             | 3856  | 32       | 64        |
| id-(hash-)slh-dsa-shake-128-24 | 1             | 3856  | 32       | 64        |
| id-(hash-)slh-dsa-sha2-192-24  | 3             | 7752  | 48       | 96        |
| id-(hash-)slh-dsa-shake-192-24 | 3             | 7752  | 48       | 96        |
| id-(hash-)slh-dsa-sha2-256-24  | 5             | 14944 | 64       | 128       |
| id-(hash-)slh-dsa-shake-256-24 | 5             | 14944 | 64       | 128       |
{: #tab-strengths title="SLH-DSA-FEW Security Strengths"}

# Examples

<aside markdown="block">
EDITOR'S NOTE: Examples of a public key, a private key, and a
self-signed certificate will be added once the object identifiers are
assigned and implementations of the parameter sets are available.
</aside>


# Acknowledgments
{:numbered="false"}

Much of the structure and text of this document is taken from
{{RFC9909}}. Thanks to its authors and contributors.
