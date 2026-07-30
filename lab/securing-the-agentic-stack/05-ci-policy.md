# Lab 3 — Sign It, Then Gate It

**10 minutes · demo, with two hands-on steps**

You have a hardened, attested image. Nothing yet stops the next person merging a
Dockerfile that undoes it.

> Verification you run once by hand is theatre. The value only compounds when the check
> is a gate.

---

## Sign it

Hardened base images arrive signed. Yours does not — until you sign it.

1. Generate a keypair. A real pipeline would use keyless OIDC signing; a local key makes
   the mechanics visible. Press enter twice for an empty password:

    ```bash terminal-id=build
    cosign generate-key-pair
    ```

2. Tag and push to the local registry:

    ```bash terminal-id=build
    docker tag catalog-service:dhi registry.dockerlabs.xyz/catalog-service:dhi
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

3. Sign it:

    ```bash terminal-id=build
    cosign sign --key cosign.key registry.dockerlabs.xyz/catalog-service:dhi --yes
    ```

4. Verify:

    ```bash terminal-id=build
    cosign verify --key cosign.pub registry.dockerlabs.xyz/catalog-service:dhi
    ```

---

## Now try to fool it

This is the most useful ninety seconds in the workshop.

1. Rebuild with a trivial change and push to the **same tag**:

    ```bash terminal-id=build
    docker build -t registry.dockerlabs.xyz/catalog-service:dhi --no-cache .
    ```

    ```bash terminal-id=build
    docker push registry.dockerlabs.xyz/catalog-service:dhi
    ```

2. Verify again — it fails:

    ```bash terminal-id=build
    cosign verify --key cosign.pub registry.dockerlabs.xyz/catalog-service:dhi
    ```

> [!IMPORTANT]
> **Tags are mutable. Digests are not. Signatures bind a claim to a digest.**
>
> Any process that trusts a tag — a Dockerfile that says `FROM node:24`, a manifest that
> says `image: catalog-service:latest` — is trusting that nobody moved it. You just
> watched exactly the substitution an attacker performs get caught.

3. Re-sign so the rest of the lab works:

    ```bash terminal-id=build
    cosign sign --key cosign.key registry.dockerlabs.xyz/catalog-service:dhi --yes
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

1. Add the signing secrets in Gitea → your repo → **Settings → Actions → Secrets**:
   `COSIGN_PRIVATE_KEY` (contents of `cosign.key`) and `COSIGN_PASSWORD` (empty). Print
   the key to copy it:

    ```bash terminal-id=build
    cat cosign.key
    ```

2. Create the workflow. **The gate sits before the push** — an image that fails policy
   never reaches the registry:

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

          - name: Sign
            env:
              COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
              COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
            run: cosign sign --key env://COSIGN_PRIVATE_KEY "$IMAGE" --yes

          - name: Push
            run: docker push "$IMAGE"
    ```

3. Commit and push — watch the run stream back:

    ```bash terminal-id=main
    git add .gitea/workflows/secure-build.yaml
    ```

    ```bash terminal-id=main
    git commit -m "Add secure build pipeline"
    ```

    ```bash terminal-id=main
    git push
    ```

The pipeline builds with attestations, evaluates the policy gate, signs and pushes — with
nobody running a verification command by hand.

---

## Checkpoint

- [ ] You have signed an image with cosign
- [ ] You have watched verification fail on a moved tag
- [ ] You have evaluated the policy locally against both images
- [ ] You have watched CI build, gate, sign and push

## Four patterns that survive contact with a real team

1. **Gate on exploitable findings, not raw CVE counts.** This is what VEX bought you in
   Lab 1. Without it a strict gate is unusable and teams switch it off within a month.
2. **Require provenance to a *known builder*,** not merely provenance that exists.
3. **Separate base-image findings from application-layer findings.** Different owners,
   different remediation paths.
4. **Fail closed on signature verification. Fail open with an alert on scanner
   availability.** A scanner outage should page somebody, not block every deploy.
