# Lab 1 - What Is In It? SBOM, VEX, SLSA

<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="Progress spine: the development-to-production road. Stages DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone (a read-only runtime box). Done stages are checked green, the current stage is marked.">
<g font-family="ui-sans-serif, system-ui, sans-serif">
<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>
<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>
<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>
<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>
<rect x="8" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="67.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">DEVELOP</text>
<rect x="134" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="193.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">BASE</text>
<rect x="260" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#2563eb" stroke-width="3"/><text x="319.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BUILD</text><text x="319.0" y="34" text-anchor="middle" font-size="10" font-weight="800" fill="#2563eb">▶ you are here</text>
<rect x="386" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="445.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">SIGN</text>
<rect x="536" y="32" width="70" height="60" rx="10" fill="#efe4d2" stroke="#d9a066" stroke-width="1.5"/><text x="571.0" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="#b79878">GATE</text><text x="571.0" y="76" text-anchor="middle" font-size="8.5" fill="#b79878">fail closed</text>
<rect x="628" y="40" width="126" height="44" rx="9" fill="#e2e7f5"/><text x="691.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">DEPLOY</text>
<rect x="766" y="40" width="126" height="44" rx="9" fill="#e2e7f5"/><text x="829.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">INVOKE</text>
<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">
<line x1="126" y1="62" x2="134" y2="62"/><polygon points="134,59 139,62 134,65"/>
<line x1="252" y1="62" x2="260" y2="62"/><polygon points="260,59 265,62 260,65"/>
<line x1="378" y1="62" x2="386" y2="62"/><polygon points="386,59 391,62 386,65"/>
<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>
<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>
</g>
</g></svg>

**16 minutes · hands-on**

> **Where you are on the road:** the **BUILD** stage. Before you can move a single stage
> toward production, you have to be able to say what came out of the build - what is in the
> image, and which of it matters.

Before you fix anything, you need to be able to describe what is wrong. This lab is the
vocabulary, and you apply all of it to the image the agent built.

---

## SBOM - what is in it

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

4. Now ask a question only an SBOM can answer - the one you get at 2am when a new CVE
   drops:

    ```bash terminal-id=build
    jq -r '.packages[] | select(.name | test("openssl|zlib|libxml")) | "\(.name) \(.versionInfo)"' baseline.spdx.json
    ```

> [!IMPORTANT]
> **Attested or indexed?** Docker Scout will index an image and construct an SBOM if it
> does not ship one. That is a reconstruction - an educated guess from the filesystem.
> An SBOM *attestation* is a signed statement from whoever built the image: *this is what
> I put in it*. One is evidence. The other is inference.

---

## VEX - which findings matter

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

## SLSA - where did it come from

SLSA defines build integrity levels. Remember what Level 3 buys you.

| Level | Meaning |
|-------|---------|
| L0 | No guarantees |
| L1 | Provenance exists - build metadata documented |
| L2 | Hosted build with signed provenance |
| **L3** | **Hardened, non-falsifiable provenance - hardened images ship this** |

1. Read your own provenance first. The agent's build recorded some:

    ```bash terminal-id=build
    docker buildx imagetools inspect catalog-service:baseline --format '{{json .Provenance}}'
    ```

2. Now read provenance you did not produce, and verify it:

    ```bash terminal-id=build
    docker scout attest get $$dhiPrefix$$node:24-debian13 --predicate-type https://slsa.dev/provenance/v0.2 --verify
    ```

You can trace it to a source repository and commit - go and read the code that produced
the image you are about to run in production.

---

## Signatures - can you verify it

An attestation is only worth the signature on it. Notice the `--verify` flag you just
used: that is the difference between a claim and evidence.

Run the VEX fetch again *without* `--verify` and compare - both return a document, only
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

Search the SBOM for copyleft licences - most teams have never looked:

```bash terminal-id=build
jq -r '.packages[] | "\(.licenseConcluded)"' baseline.spdx.json | sort | uniq -c | sort -rn
```
