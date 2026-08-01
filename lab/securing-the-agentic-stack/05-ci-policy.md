# Lab 3 — Attest It, Then Gate It

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, done Hardened base, current Attest &amp; Gate, Agentic MCP">
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
    <text x="634" y="30" fill="#ffffff" font-weight="700">Attest &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="817" y="30" fill="#5b6670">Agentic MCP</text>
  </g>
</svg>

**10 minutes · demo, with two hands-on steps**

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

You have a hardened, attested image. Nothing yet stops the next person merging a
Dockerfile that undoes it.

> Verification you run once by hand is theatre. The value only compounds when the check
> is a gate.

---

## Attest it

Hardened base images arrive with signed attestations from Docker. Yours carries
attestations too — you built `catalog-service:dhi` in Lab 2 with `--sbom` and
`--provenance=mode=max` — attached at build time and bound to the image **digest**.
(They are attached to the digest, not cryptographically signed — the digest binding is
what the policy gate checks.) Confirm they rode along, then push.

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
> **Tags are mutable. Digests are not. Attestations bind to a digest.**
>
> Any process that trusts a tag — a Dockerfile that says `FROM node:24`, a manifest that
> says `image: catalog-service:latest` — is trusting that nobody moved it. The tag now
> resolves to a new digest with no SBOM and no provenance: exactly the substitution an
> attacker performs, and the missing attestations are what gives it away.

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
> The files in this workspace are committed to a Gitea repository at
> `git.dockerlabs.xyz` (log in as `moby` / `moby1234`). Anything under
> `.gitea/workflows/` runs automatically when you push.

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

## Checkpoint

- [ ] You have confirmed the SBOM and provenance attestations bound to the image digest
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
