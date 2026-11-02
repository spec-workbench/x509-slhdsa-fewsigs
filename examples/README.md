# Examples

This directory will hold the examples for the draft (public key, private key,
self-signed certificate) for the SLH-DSA parameter sets of NIST SP 800-230.

They will be generated reproducibly by a script in this directory (fixed seeds,
so the output is deterministic) and included into the draft with
`{::include examples/...}`. CI will regenerate them and fail on any difference.

Blocked on: OID assignment by NIST (CSOR) and an implementation of the
SP 800-230 parameter sets.
