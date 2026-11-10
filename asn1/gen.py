#!/usr/bin/env python3
"""Generate the ASN.1 module X509-SLHDSA-FEW-2026.asn.

The module contains the same definitions for each of the 12 SLH-DSA-FEW
variants (6 Pure, 6 HashSLH-DSA). Generating it avoids copy-and-paste
errors between them. Edit this script, not the .asn file, and rerun:

    python3 asn1/gen.py           # (re)write the module
    python3 asn1/gen.py --check   # exit 1 if the module is out of date

The order of the parameter sets follows Table 1 of NIST SP 800-230.
The pre-hash functions follow the pairing of RFC 9909.
"""

import argparse
import pathlib
import sys

MODULE = pathlib.Path(__file__).with_name("X509-SLHDSA-FEW-2026.asn")
MAX_WIDTH = 69  # xml2rfc indents sourcecode by 3 columns in 72-column text

# (internal hash family, security level, pre-hash function)
SETS = [
    ("sha2", "128", "sha256"),
    ("shake", "128", "shake128"),
    ("sha2", "192", "sha512"),
    ("shake", "192", "shake256"),
    ("sha2", "256", "sha512"),
    ("shake", "256", "shake256"),
]

PURE = [f"slh-dsa-{h}-{lvl}-24" for h, lvl, _ in SETS]
HASHED = [f"hash-slh-dsa-{h}-{lvl}-24-with-{ph}" for h, lvl, ph in SETS]

HEADER = """\
X509-SLH-DSA-FEW-Module-2026
  { iso(1) identified-organization(3) dod(6) internet(1) security(5)
    mechanisms(5) pkix(7) id-mod(0)
    id-mod-x509-slh-dsa-few-2026(TBD0) }

DEFINITIONS IMPLICIT TAGS ::= BEGIN

EXPORTS ALL;

IMPORTS
  PUBLIC-KEY, SIGNATURE-ALGORITHM, SMIME-CAPS
    FROM AlgorithmInformation-2009  -- in [RFC5912]
    { iso(1) identified-organization(3) dod(6) internet(1)
      security(5) mechanisms(5) pkix(7) id-mod(0)
      id-mod-algorithmInformation-02(58) } ;

--
-- Object identifiers for the SLH-DSA-FEW parameter sets; see
-- [SP800-230]. TBD1 to TBD12 are to be assigned by NIST in [CSOR].
--

nistAlgorithms OBJECT IDENTIFIER ::= { joint-iso-itu-t(2)
  country(16) us(840) organization(1) gov(101) csor(3) 4 }

sigAlgs OBJECT IDENTIFIER ::= { nistAlgorithms 3 }
"""


def comment(title):
    return f"--\n-- {title}\n--\n"


def oids(title, names, first_tbd):
    out = [comment(f"{title} object identifiers")]
    for i, n in enumerate(names):
        line = f"id-{n} OBJECT IDENTIFIER ::= {{ sigAlgs TBD{first_tbd + i} }}"
        if len(line) > MAX_WIDTH:
            line = (f"id-{n} OBJECT IDENTIFIER ::= {{\n"
                    f"  sigAlgs TBD{first_tbd + i} }}")
        out.append(line + "\n")
    return out


def public_keys(title, names):
    out = [comment(f"{title} public key identifiers")]
    for n in names:
        out.append(f"""\
pk-{n} PUBLIC-KEY ::= {{
  IDENTIFIER id-{n}
  -- KEY no ASN.1 wrapping --
  CERT-KEY-USAGE
      {{ digitalSignature, nonRepudiation, keyCertSign, cRLSign }}
  -- PRIVATE-KEY no ASN.1 wrapping -- }}
""")
    return out


def signature_algorithms(title, names):
    out = [comment(f"{title} signature algorithm identifiers")]
    for n in names:
        out.append(f"""\
sa-{n} SIGNATURE-ALGORITHM ::= {{
  IDENTIFIER id-{n}
  PARAMS ARE absent
  PUBLIC-KEYS {{ pk-{n} }}
  SMIME-CAPS {{
    IDENTIFIED BY id-{n} }} }}
""")
    return out


def object_set(name, cls, items):
    body = " |\n".join("  " + x for x in items)
    return [comment(f"Expand {name} from [RFC5912]"),
            f"{name} {cls} ::= {{\n{body},\n  ... }}\n"]


def generate():
    names = PURE + HASHED
    parts = [HEADER]
    parts += oids("Pure SLH-DSA-FEW", PURE, 1)
    parts += oids("HashSLH-DSA-FEW", HASHED, 7)
    parts += public_keys("Pure SLH-DSA-FEW", PURE)
    parts += public_keys("HashSLH-DSA-FEW", HASHED)
    parts += signature_algorithms("Pure SLH-DSA-FEW", PURE)
    parts += signature_algorithms("HashSLH-DSA-FEW", HASHED)
    parts += object_set("SignatureAlgorithms", "SIGNATURE-ALGORITHM",
                        [f"sa-{n}" for n in names])
    parts += object_set("SMimeCaps", "SMIME-CAPS",
                        [f"sa-{n}.&smimeCaps" for n in names])
    parts += object_set("PublicKeyAlgorithms", "PUBLIC-KEY",
                        [f"pk-{n}" for n in names])
    parts.append("END\n")
    text = "\n".join(parts)

    too_wide = [i for i, line in enumerate(text.splitlines(), 1)
                if len(line) > MAX_WIDTH]
    if too_wide:
        sys.exit(f"lines wider than {MAX_WIDTH} columns: {too_wide}")
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="fail if the module differs from the output")
    args = parser.parse_args()

    text = generate()
    if args.check:
        current = MODULE.read_text() if MODULE.exists() else ""
        if current != text:
            sys.exit(f"{MODULE.name} is out of date; run asn1/gen.py")
        print(f"{MODULE.name} is up to date")
    else:
        MODULE.write_text(text)
        print(f"wrote {MODULE.name}")


if __name__ == "__main__":
    main()
