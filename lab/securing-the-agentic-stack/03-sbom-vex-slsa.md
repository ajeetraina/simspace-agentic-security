# Lab 1 — What Is In It? SBOM, VEX, SLSA

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, current SBOM · VEX · SLSA, Hardened base, Verify &amp; Gate, Agentic MCP">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12" text-anchor="middle">
    <rect x="1" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="85" y="30" fill="#14532d">✓ Agent build</text>
    <polygon points="172,22 180,26 172,30" fill="#9aa4b2"></polygon>
    <rect x="184" y="11" width="168" height="30" rx="15" fill="#2496ED" stroke="#0b3d91" stroke-width="2"></rect>
    <text x="268" y="30" fill="#ffffff" font-weight="700">SBOM · VEX · SLSA</text>
    <polygon points="355,22 363,26 355,30" fill="#9aa4b2"></polygon>
    <rect x="367" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="451" y="30" fill="#5b6670">Hardened base</text>
    <polygon points="538,22 546,26 538,30" fill="#9aa4b2"></polygon>
    <rect x="550" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="634" y="30" fill="#5b6670">Verify &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="817" y="30" fill="#5b6670">Agentic MCP</text>
  </g>
</svg>

**16 minutes · hands-on**

Before you fix anything, you need to be able to describe what is wrong. This lab is the
vocabulary, and you apply all of it to the image the agent built.

---

## SBOM — what is in it

A Software Bill of Materials is an inventory: every package, version, licence and
supplier in the image.

1. Generate one in SPDX format:

    ```bash terminal-id=build
    docker scout sbom --format spdx --output baseline.spdx.json catalog-service:baseline
    ```

2. Count what you are shipping:

    ```bash terminal-id=build
    jq '.packages | length' baseline.spdx.json
    ```

3. Look at what they actually are:

    ```bash terminal-id=build
    jq -r '.packages[].name' baseline.spdx.json
    ```

    Most of these you did not choose, did not install, and cannot name.

4. Now ask a question only an SBOM can answer — the one you get at 2am when a new CVE
   drops:

    ```bash terminal-id=build
    jq -r '.packages[] | select(.name | test("openssl|zlib|libxml")) | "\(.name) \(.versionInfo)"' baseline.spdx.json
    ```

> [!IMPORTANT]
> **Attested or indexed?** Docker Scout will index an image and construct an SBOM if it
> does not ship one. That is a reconstruction — an educated guess from the filesystem.
> An SBOM *attestation* is a signed statement from whoever built the image: *this is what
> I put in it*. One is evidence. The other is inference.

---

## VEX — which findings matter

1. Look at the unfiltered list:

    ```bash terminal-id=build
    docker scout cves catalog-service:baseline --org $$org$$ --only-severity critical,high
    ```

2. Pick any finding and ask three questions about it:

    - Is that package reachable from the catalog's code path?
    - Is the vulnerable function ever called?
    - Would exploiting it need access an attacker would not already have?

For most of this list the honest answer is *no, no, and yes*. Your pipeline is still
red, and somebody still has a ticket. `catalog-service:baseline` carries no
exploitability data, because nobody produced any. A hardened image does:

3. Pull a real VEX document and read one statement:

    ```bash terminal-id=build
    docker scout attest get $$dhiPrefix$$node:24-debian13 --predicate-type https://openvex.dev/ns/v0.2.0
    ```

    | Field | Meaning |
    |-------|---------|
    | `vulnerability` | Which CVE |
    | `products` | Which artifact, **by digest** |
    | `status` | `not_affected`, `affected`, `fixed`, `under_investigation` |
    | `justification` | *Why*, as a machine-readable enum |

> "Your image has 200 CVEs" and "190 not affected, 10 fixed" describe the same image.
> One sends four engineers into a triage meeting. The other is a decision somebody
> already made and signed.

---

## SLSA — where did it come from

SLSA defines build integrity levels. Remember what Level 3 buys you.

| Level | Meaning |
|-------|---------|
| L0 | No guarantees |
| L1 | Provenance exists — build metadata documented |
| L2 | Hosted build with signed provenance |
| **L3** | **Hardened, non-falsifiable provenance — hardened images ship this** |

1. Read your own provenance first. The agent's build recorded some:

    ```bash terminal-id=build
    docker buildx imagetools inspect catalog-service:baseline --format '{{json .Provenance}}'
    ```

2. Now read provenance you did not produce, and verify it:

    ```bash terminal-id=build
    docker scout attest get $$dhiPrefix$$node:24-debian13 --predicate-type https://slsa.dev/provenance/v0.2 --verify
    ```

You can trace it to a source repository and commit — go and read the code that produced
the image you are about to run in production.

---

## Signatures — can you verify it

An attestation is only worth the signature on it. Notice the `--verify` flag you just
used: that is the difference between a claim and evidence.

Run the VEX fetch again *without* `--verify` and compare — both return a document, only
one proves who wrote it:

```bash terminal-id=build
docker scout attest get $$dhiPrefix$$node:24-debian13 --predicate-type https://openvex.dev/ns/v0.2.0
```

You will sign your own images in Lab 3.

---

## Checkpoint

- [ ] You know how many packages are in the agent's image
- [ ] You have queried the SBOM for a specific package version
- [ ] You have read a VEX statement, including its justification
- [ ] You have traced a hardened image to its source commit
- [ ] You can say what `--verify` changes

## Go deeper

Generate a CycloneDX SBOM and compare the structure with SPDX:

```bash terminal-id=build
docker scout sbom --format cyclonedx --output baseline.cdx.json catalog-service:baseline
```

Search the SBOM for copyleft licences — most teams have never looked:

```bash terminal-id=build
jq -r '.packages[] | "\(.licenseConcluded)"' baseline.spdx.json | sort | uniq -c | sort -rn
```
