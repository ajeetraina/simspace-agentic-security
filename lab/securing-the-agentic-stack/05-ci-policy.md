# Lab 3 — Verify It, Then Gate It

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, done Hardened base, current Verify &amp; Gate, Build Sandbox">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12" text-anchor="middle">
    <rect x="1" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="85" y="30" fill="#14532d">✓ Agent build</text>
    <polygon points="172,22 180,26 172,30" fill="#9aa4b2"></polygon>
    <rect x="184" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="268" y="30" fill="#14532d">✓ SBOM · VEX · SLSA</text>
    <polygon points="355,22 363,26 355,30" fill="#9aa4b2"></polygon>
    <rect x="367" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="451" y="30" fill="#14532d">✓ Hardened base</text>
    <polygon points="538,22 546,26 538,30" fill="#9aa4b2"></polygon>
    <rect x="550" y="11" width="168" height="30" rx="15" fill="#2496ED" stroke="#0b3d91" stroke-width="2"></rect>
    <text x="634" y="30" fill="#ffffff" font-weight="700">Verify &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="817" y="30" fill="#5b6670">Build Sandbox</text>
  </g>
</svg>

**10 minutes · demo, with hands-on steps**

The pipeline you are about to build — the gate sits **before** the push, so an
image that fails policy never reaches the registry:

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
    <text x="612" y="115" text-anchor="middle" fill="#b91c1c" font-weight="700">blocked — never pushed</text>
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
can verify. Nothing yet stops the next person merging a Dockerfile that undoes all of it —
so you will do two things: **verify** the trust chain by hand once, then turn that check
into a **gate** that runs on every push.

> Verification you run once by hand is theatre. The value only compounds when the check
> is a gate.

---

## Attest it

Hardened base images arrive with signed attestations from Docker. Yours carries
attestations too — you built `catalog-service:dhi` in Lab 2 with `--sbom` and
`--provenance=mode=max` — attached at build time and bound to the image **digest**.
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

Presence is not trust — anyone can *attach* an SBOM. What makes it trustworthy is the
**signature** underneath it. Because you built on a Docker Hardened Image, the provenance
chain traces back to a base Docker **signed**, and you can verify that signature —
keyless, against Sigstore's transparency log. There is no key for you to manage; you
inherit and verify a signature from a builder you trust.

```bash terminal-id=build
docker scout attest get catalog-service:dhi --predicate-type https://slsa.dev/provenance/v0.2 --verify
```

The `--verify` flag is the whole point. `✓ Signature verified` means the provenance was
not forged and traces to a source commit you can open and read. **This is the image-signing
half of a secure pipeline — not a key you rotate, but a signature you *check*.** In a
moment you will make the pipeline check it for you, on every push.

---

## Now try to fool it

This is the most useful ninety seconds in the workshop.

1. Rebuild with a trivial change — a **plain build, no attestations** — and push to the
   **same tag**:

    ```bash terminal-id=build
    docker build -t registry.dockerlabs.xyz/catalog-service:dhi --no-cache .
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

2. Ask for the attestations again — they are gone:

    ```bash terminal-id=build
    docker scout attest list registry.dockerlabs.xyz/catalog-service:dhi
    ```

> [!IMPORTANT]
> **Tags are mutable. Digests are not. Attestations and signatures bind to a digest.**
>
> Any process that trusts a tag — a Dockerfile that says `FROM node:24`, a manifest that
> says `image: catalog-service:latest` — is trusting that nobody moved it. The tag now
> resolves to a new digest with no SBOM, no provenance, and nothing that would survive a
> `--verify`: exactly the substitution an attacker performs, and the missing, unverifiable
> attestations are what give it away.

3. Rebuild **with** attestations so the rest of the lab works:

    ```bash terminal-id=build
    docker build -t registry.dockerlabs.xyz/catalog-service:dhi --sbom=true --provenance=mode=max .
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

---

## Write the policy

You watched the default policy fail in Lab 1. That was an *evaluation*. Now make it a
*gate*. Open :filelink[docker-scout-policy.yaml]{path="docker-scout-policy.yaml"} — three
rules, one per question from the spine.

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
> This is a **simulated** CI environment — `git.dockerlabs.xyz` is a stand-in, not a live
> server you log into. The workspace behaves as a Gitea repo whose `moby` account owns it:
> anything under `.gitea/workflows/` "runs" automatically when you push, and you inspect
> the run right here in the terminal with `gitea run view` (below) — no browser needed.

**Gitea Actions** is Gitea's built-in CI — GitHub-Actions-compatible, so the workflow
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

1. Create the workflow. The build attaches the SBOM and provenance attestations, and
   **the gate sits before the push** — an image that fails policy never reaches the
   registry:

    ```yaml save-as=.gitea/workflows/secure-build.yaml
    name: secure-build

    on: [push]

    env:
      IMAGE: ${{ secrets.DOCKER_REGISTRY }}/catalog-service:${{ github.sha }}

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Build with attestations
            run: |
              docker build -t "$IMAGE" \
                --sbom=true \
                --provenance=mode=max .

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

2. Commit and push — watch the run stream back:

    ```bash terminal-id=main
    git add .gitea/workflows/secure-build.yaml
    ```

    ```bash terminal-id=main
    git commit -m "Add secure build pipeline"
    ```

    ```bash terminal-id=main
    git push
    ```

The pipeline builds with attestations, evaluates the policy gate, then pushes — with
nobody running a verification command by hand.

---

## See the run in Gitea

In a real setup you would open the **Actions** tab in the Gitea web UI. Here, render that
same run page in the terminal:

```bash terminal-id=main
gitea run view secure-build
```

That expands every step with its log — the same view the browser shows:

<svg viewBox="0 0 720 324" width="100%" role="img" aria-label="Gitea Actions run page for secure-build run number 12 on branch main, commit a9d0e42, succeeded in 38 seconds. Job build on ubuntu-latest. Steps: Set up job 2s, actions/checkout@v4 3s, Build with attestations (sbom + provenance) 21s, Policy gate 9s with 3 of 3 policies passed, Push 3s attestations bound to digest, Complete job. secure-build succeeded because the gate passed before the push.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="13">
    <rect x="1" y="1" width="718" height="322" rx="8" fill="#ffffff" stroke="#d0d7de"></rect>
    <rect x="1" y="1" width="718" height="32" rx="8" fill="#24292f"></rect>
    <rect x="1" y="17" width="718" height="16" fill="#24292f"></rect>
    <text x="16" y="22" fill="#ffffff" font-size="12">git.dockerlabs.xyz / moby / catalog-service — Actions</text>
    <text x="20" y="58" fill="#1a7f37" font-weight="700">✓</text>
    <text x="40" y="58" fill="#24292f" font-weight="700">secure-build #12</text>
    <text x="190" y="58" fill="#57606a" font-size="12">main · a9d0e42 · pushed by moby · trigger: push</text>
    <text x="700" y="58" fill="#57606a" font-size="12" text-anchor="end">38s</text>
    <line x1="16" y1="72" x2="704" y2="72" stroke="#d0d7de"></line>
    <text x="20" y="96" fill="#57606a" font-size="12" font-weight="700">build  ·  runs-on: ubuntu-latest</text>
    <text x="24" y="128" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="128" fill="#24292f">Set up job</text>
    <text x="700" y="128" fill="#57606a" font-size="12" text-anchor="end">2s</text>
    <text x="24" y="158" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="158" fill="#24292f">actions/checkout@v4</text>
    <text x="700" y="158" fill="#57606a" font-size="12" text-anchor="end">3s</text>
    <text x="24" y="188" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="188" fill="#24292f">Build with attestations</text>
    <text x="270" y="188" fill="#57606a" font-size="12">sbom + provenance</text>
    <text x="700" y="188" fill="#57606a" font-size="12" text-anchor="end">21s</text>
    <text x="24" y="218" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="218" fill="#24292f">Policy gate</text>
    <text x="270" y="218" fill="#1a7f37" font-size="12">3/3 policies passed — image allowed</text>
    <text x="700" y="218" fill="#57606a" font-size="12" text-anchor="end">9s</text>
    <text x="24" y="248" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="248" fill="#24292f">Push</text>
    <text x="270" y="248" fill="#57606a" font-size="12">attestations bound to digest</text>
    <text x="700" y="248" fill="#57606a" font-size="12" text-anchor="end">3s</text>
    <text x="24" y="278" fill="#1a7f37" font-weight="700">✓</text>
    <text x="46" y="278" fill="#24292f">Complete job</text>
    <text x="700" y="278" fill="#57606a" font-size="12" text-anchor="end">0s</text>
    <line x1="16" y1="296" x2="704" y2="296" stroke="#d0d7de"></line>
    <text x="20" y="313" fill="#1a7f37" font-size="12" font-weight="700">secure-build succeeded — the gate passed before the push.</text>
  </g>
</svg>

> [!TIP]
> **The gate sits before Push.** Had the policy step failed, the run would stop there in
> red and `Push` would never execute — a non-compliant image never reaches the registry.

---

## Checkpoint

- [ ] You have confirmed the SBOM and provenance attestations bound to the image digest
- [ ] You have verified the provenance signature (`--verify`) traces to a trusted builder
- [ ] You have watched the attestations vanish when the tag was moved
- [ ] You have evaluated the policy locally against both images
- [ ] You have watched CI build, gate and push

## Four patterns that survive contact with a real team

1. **Gate on exploitable findings, not raw CVE counts.** This is what VEX bought you in
   Lab 1. Without it a strict gate is unusable and teams switch it off within a month.
2. **Require provenance to a *known builder*,** not merely provenance that exists.
3. **Separate base-image findings from application-layer findings.** Different owners,
   different remediation paths.
4. **Fail closed on missing or unverifiable attestations. Fail open with an alert on
   scanner availability.** A scanner outage should page somebody, not block every deploy.
