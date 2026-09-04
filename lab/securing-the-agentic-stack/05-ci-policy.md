# Lab 3 - Verify It, Then Gate It

<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="Progress spine: the development-to-production road. Stages DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone (a read-only runtime box). Done stages are checked green, the current stage is marked.">
<g font-family="ui-sans-serif, system-ui, sans-serif">
<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>
<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>
<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>
<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>
<rect x="8" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="67.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">DEVELOP</text>
<rect x="134" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="193.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BASE</text><circle cx="239" cy="52" r="9" fill="#1a7f37"/><path d="M235,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="260" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="319.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BUILD</text><circle cx="365" cy="52" r="9" fill="#1a7f37"/><path d="M361,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="386" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#2563eb" stroke-width="3"/><text x="445.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">SIGN</text><text x="445.0" y="34" text-anchor="middle" font-size="10" font-weight="800" fill="#2563eb">▶ you are here</text>
<rect x="536" y="32" width="70" height="60" rx="10" fill="#fff3e0" stroke="#2563eb" stroke-width="3"/><text x="571.0" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="#9a3412">GATE</text><text x="571.0" y="76" text-anchor="middle" font-size="8.5" fill="#9a3412">fail closed</text>
<rect x="628" y="40" width="126" height="44" rx="9" fill="#0b1533" stroke="#2563eb" stroke-width="3"/><text x="691.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">DEPLOY</text>
<rect x="766" y="40" width="126" height="44" rx="9" fill="#e2e7f5"/><text x="829.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">INVOKE</text>
<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">
<line x1="126" y1="62" x2="134" y2="62"/><polygon points="134,59 139,62 134,65"/>
<line x1="252" y1="62" x2="260" y2="62"/><polygon points="260,59 265,62 260,65"/>
<line x1="378" y1="62" x2="386" y2="62"/><polygon points="386,59 391,62 386,65"/>
<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>
<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>
</g>
</g></svg>

**10 minutes · demo, with hands-on steps**

> **Where you are on the road:** the **boundary itself**. Everything so far happened in
> *development* - you authored an image, hardened its base, attached evidence. This lab is
> the border you cross to reach *production*. The CI gate is not a side-topic bolted onto the
> chain; it is the one place the dev-to-prod path is allowed to be stopped. A signed, hardened
> image on the left of the gate; only what clears it runs on the right.

The pipeline you are about to build - the gate sits **before** the push, so an
image that fails policy never reaches the registry. It is the amber gate in the middle of the
road from the Introduction:

<svg viewBox="0 0 720 150" width="100%" role="img" aria-label="CI pipeline: git push, then build with SBOM and provenance attestations, then a policy gate. On pass: push the attested image to the registry. On fail: blocked, never pushed.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="8" y="54" width="96" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="56" y="75" text-anchor="middle" fill="#24292f">git push</text>
    <rect x="128" y="54" width="176" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="216" y="75" text-anchor="middle" fill="#24292f">build · sbom · provenance</text>
    <rect x="328" y="54" width="116" height="34" rx="6" fill="#fff7ed" stroke="#d97706"></rect>
    <text x="386" y="75" text-anchor="middle" fill="#9a3412" font-weight="700">policy gate</text>
    <rect x="512" y="14" width="200" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="612" y="35" text-anchor="middle" fill="#24292f">push attested image → registry</text>
    <rect x="512" y="94" width="200" height="34" rx="6" fill="#fdecea" stroke="#b91c1c"></rect>
    <text x="612" y="115" text-anchor="middle" fill="#b91c1c" font-weight="700">blocked - never pushed</text>
    <g stroke="#6b7280" stroke-width="1.5" fill="none">
      <line x1="104" y1="71" x2="126" y2="71"></line>
      <line x1="304" y1="71" x2="326" y2="71"></line>
      <path d="M444,71 L488,71 L488,31 L510,31"></path>
      <path d="M444,71 L488,71 L488,111 L510,111"></path>
    </g>
    <g fill="#6b7280">
      <polygon points="120,67 128,71 120,75"></polygon>
      <polygon points="320,67 328,71 320,75"></polygon>
      <polygon points="504,27 512,31 504,35"></polygon>
      <polygon points="504,107 512,111 504,115"></polygon>
    </g>
    <text x="496" y="20" font-size="10" fill="#1a7f37" font-weight="700">pass</text>
    <text x="496" y="106" font-size="10" fill="#b91c1c" font-weight="700">fail</text>
  </g>
</svg>

You have a hardened image, built on a base Docker **signed**, carrying attestations you
can verify. Nothing yet stops the next person merging a Dockerfile that undoes all of it -
so you will do two things: **verify** the trust chain by hand once, then turn that check
into a **gate** that runs on every push.

> Verification you run once by hand is theatre. The value only compounds when the check
> is a gate.

---

## Attest it

Hardened base images arrive with signed attestations from Docker. Yours carries
attestations too - you built `catalog-service:dhi` in Lab 2 with `--sbom` and
`--provenance=mode=max` - attached at build time and bound to the image **digest**.
Confirm they rode along, then push.

1. Tag and push to the local registry:

    ```bash terminal-id=build
    docker tag catalog-service:dhi registry.dockerlabs.xyz/catalog-service:dhi
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

2. Ask Scout what is attested on that digest:

    ```bash terminal-id=build
    docker scout attest list registry.dockerlabs.xyz/catalog-service:dhi
    ```

    An SBOM and SLSA provenance, both attached at build and bound to the digest you just
    pushed.

---

## Verify it

Presence is not trust - anyone can *attach* an SBOM. What makes it trustworthy is the
**signature** underneath it. Because you built on a Docker Hardened Image, the provenance
chain traces back to a base Docker **signed**, and you can verify that signature -
keyless, against Sigstore's transparency log. There is no key for you to manage; you
inherit and verify a signature from a builder you trust.

```bash terminal-id=build
docker scout attest get catalog-service:dhi --predicate-type https://slsa.dev/provenance/v0.2 --verify
```

The `--verify` flag is the whole point. `✓ Signature verified` means the provenance was
not forged and traces to a source commit you can open and read. **This is the image-signing
half of a secure pipeline - not a key you rotate, but a signature you *check*.** In a
moment you will make the pipeline check it for you, on every push.

---

## Now try to fool it

This is the most useful ninety seconds in the workshop.

1. Rebuild with a trivial change - a **plain build, no attestations** - and push to the
   **same tag**:

    ```bash terminal-id=build
    docker build -t registry.dockerlabs.xyz/catalog-service:dhi --no-cache .
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

2. Ask for the attestations again - they are gone:

    ```bash terminal-id=build
    docker scout attest list registry.dockerlabs.xyz/catalog-service:dhi
    ```

> [!IMPORTANT]
> **Tags are mutable. Digests are not. Attestations and signatures bind to a digest.**
>
> Any process that trusts a tag - a Dockerfile that says `FROM node:24`, a manifest that
> says `image: catalog-service:latest` - is trusting that nobody moved it. The tag now
> resolves to a new digest with no SBOM, no provenance, and nothing that would survive a
> `--verify`: exactly the substitution an attacker performs, and the missing, unverifiable
> attestations are what give it away.

**Leave the tag like this.** The registry now holds an unsigned image where a verified one
used to be - a check you ran by hand caught it. In a moment you'll turn that same check into
a gate and watch your pipeline catch the *identical* substitution automatically, then fix it.

---

## Write the policy

You watched the default policy fail in Lab 1. That was an *evaluation*. Now make it a
*gate*. Save this `docker-scout-policy.yaml` - three rules, one per question from the spine:

```yaml save-as=docker-scout-policy.yaml
version: "1"
policies:
  - name: no-critical-cves
    type: vulnerability
    severity: critical
    action: fail

  - name: require-sbom
    type: attestation
    attestation: sbom
    action: fail

  - name: require-provenance
    type: attestation
    attestation: slsa-provenance
    action: fail
```

Evaluate both images and compare:

```bash terminal-id=build
docker scout policy catalog-service:baseline --org $$org$$
```

```bash terminal-id=build
docker scout policy catalog-service:dhi --org $$org$$
```

One fails. One passes. You now know what the pipeline will say before you push.

---

## Put it in the pipeline

> [!NOTE]
> This is a **simulated** CI environment - `git.dockerlabs.xyz` is a stand-in, not a live
> server you log into. The workspace behaves as a Gitea repo whose `moby` account owns it:
> anything under `.gitea/workflows/` "runs" automatically when you push, and the run
> renders in the **CI Pipeline** tab at the top right - no browser needed.

**Gitea Actions** is Gitea's built-in CI - GitHub-Actions-compatible, so the workflow
below is the *same* YAML you would commit to GitHub. Here is what happens the moment you
push:

<svg viewBox="0 0 720 90" width="100%" role="img" aria-label="How Gitea Actions runs the workflow: git push reaches the Gitea server, which stores the commit; the act_runner picks up .gitea/workflows/secure-build.yaml, runs the job steps in a container, and reports a pass or fail status back on the commit.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="6" y="30" width="118" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="65" y="51" text-anchor="middle" fill="#24292f">git push</text>
    <rect x="148" y="30" width="140" height="34" rx="6" fill="#eef1f5" stroke="#8c959f"></rect>
    <text x="218" y="51" text-anchor="middle" fill="#24292f">Gitea stores commit</text>
    <rect x="312" y="30" width="152" height="34" rx="6" fill="#eef1f5" stroke="#8c959f"></rect>
    <text x="388" y="46" text-anchor="middle" fill="#24292f">act_runner picks up</text>
    <text x="388" y="59" text-anchor="middle" fill="#57606a" font-size="10">.gitea/workflows/*.yaml</text>
    <rect x="488" y="30" width="120" height="34" rx="6" fill="#fff7ed" stroke="#d97706"></rect>
    <text x="548" y="51" text-anchor="middle" fill="#9a3412">runs job steps</text>
    <rect x="632" y="30" width="82" height="34" rx="6" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="673" y="51" text-anchor="middle" fill="#14532d">✓ status</text>
    <g stroke="#6b7280" stroke-width="1.5" fill="none">
      <line x1="124" y1="47" x2="146" y2="47"></line>
      <line x1="288" y1="47" x2="310" y2="47"></line>
      <line x1="464" y1="47" x2="486" y2="47"></line>
      <line x1="608" y1="47" x2="630" y2="47"></line>
    </g>
    <g fill="#6b7280">
      <polygon points="140,43 148,47 140,51"></polygon>
      <polygon points="304,43 312,47 304,51"></polygon>
      <polygon points="480,43 488,47 480,51"></polygon>
      <polygon points="624,43 632,47 624,51"></polygon>
    </g>
  </g>
</svg>

1. Create the workflow. It **verifies the signed attestations** already bound to the
   pushed digest, then runs the **policy gate** - and only a run that clears both
   **promotes** the image. The gate sits before the push, so a non-compliant image never
   reaches the registry:

    ```yaml save-as=.gitea/workflows/secure-build.yaml
    name: secure-build

    on: [push]

    env:
      IMAGE: ${{ secrets.DOCKER_REGISTRY }}/catalog-service:dhi

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          # The by-hand `--verify` from earlier, now a gate. A tag rebuilt
          # without --sbom/--provenance has nothing to verify - this step fails.
          - name: Verify attestations
            uses: docker/scout-action@v1
            with:
              command: attestation
              image: ${{ env.IMAGE }}
              predicate-type: https://slsa.dev/provenance/v0.2
              # signature must trace to a trusted builder (keyless, Sigstore)

          # The gate sits BEFORE the push.
          - name: Policy gate
            uses: docker/scout-action@v1
            with:
              command: policy
              image: ${{ env.IMAGE }}
              organization: ${{ secrets.DOCKER_SCOUT_ORG }}
              exit-on: policy

          - name: Push
            run: docker push "$IMAGE"
    ```

2. Commit and push. The tag on the registry is **still the tampered, unsigned image** you
   left a moment ago - so watch this run go red:

    ```bash terminal-id=main
    git add .gitea/workflows/secure-build.yaml
    ```

    ```bash terminal-id=main
    git commit -m "Add secure build pipeline"
    ```

    ```bash terminal-id=main
    git push
    ```

Switch to the **CI Pipeline** tab. The run stops at **Verify attestations** - the digest
carries nothing to verify - and `Policy gate` and `Push` are skipped. The unsigned image
never reaches the registry. The `--verify` you ran once by hand is now enforced on every
push.

---

## Fix it, then re-run

The pipeline caught the substitution. Now fix the artifact - rebuild **with** attestations,
so a signed image sits on the tag again:

```bash terminal-id=build
docker build -t registry.dockerlabs.xyz/catalog-service:dhi --sbom=true --provenance=mode=max .
```

```bash terminal-id=build
docker push registry.dockerlabs.xyz/catalog-service:dhi
```

Back in the **CI Pipeline** tab, press **Re-run jobs** on the failed run. No new commit -
the *same* pipeline re-evaluates against the fixed tag, and this time every step is green:

- **Verify attestations** → SBOM + provenance present, signature verified ✓
- **Policy gate** → 3 / 3 policies satisfied ✓
- **Push** → image promoted to the registry ✓

> [!TIP]
> **Fix the state, re-run, green.** Re-run pushed nothing by hand - it re-evaluated the
> pipeline against the current state, and because a signed image now sits on the tag, the
> gate passed and the pipeline promoted it. That is the whole point of a gate: the same
> check runs on every push and every re-run, and nobody has to remember to run it.

---

## Checkpoint

- [ ] You have confirmed the SBOM and provenance attestations bound to the image digest
- [ ] You have verified the provenance signature (`--verify`) traces to a trusted builder
- [ ] You have watched the attestations vanish when the tag was moved
- [ ] You have evaluated the policy locally against both images
- [ ] You have watched the pipeline go **red** on the tampered tag in the CI Pipeline tab
- [ ] You have fixed the artifact and used **Re-run** to watch the same pipeline go green

## Four patterns that survive contact with a real team

1. **Gate on exploitable findings, not raw CVE counts.** This is what VEX bought you in
   Lab 1. Without it a strict gate is unusable and teams switch it off within a month.
2. **Require provenance to a *known builder*,** not merely provenance that exists.
3. **Separate base-image findings from application-layer findings.** Different owners,
   different remediation paths.
4. **Fail closed on missing or unverifiable attestations. Fail open with an alert on
   scanner availability.** A scanner outage should page somebody, not block every deploy.
