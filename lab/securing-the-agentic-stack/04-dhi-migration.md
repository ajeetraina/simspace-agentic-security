# Lab 2 — Start From a Trusted Base

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, current Hardened base, Verify &amp; Gate, Agentic MCP">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12" text-anchor="middle">
    <rect x="1" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="85" y="30" fill="#14532d">✓ Agent build</text>
    <polygon points="172,22 180,26 172,30" fill="#9aa4b2"></polygon>
    <rect x="184" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="268" y="30" fill="#14532d">✓ SBOM · VEX · SLSA</text>
    <polygon points="355,22 363,26 355,30" fill="#9aa4b2"></polygon>
    <rect x="367" y="11" width="168" height="30" rx="15" fill="#2496ED" stroke="#0b3d91" stroke-width="2"></rect>
    <text x="451" y="30" fill="#ffffff" font-weight="700">Hardened base</text>
    <polygon points="538,22 546,26 538,30" fill="#9aa4b2"></polygon>
    <rect x="550" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="634" y="30" fill="#5b6670">Verify &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="817" y="30" fill="#5b6670">Agentic MCP</text>
  </g>
</svg>

**16 minutes · hands-on**

The migration in one picture — a builder stage with a shell and npm produces
`node_modules`, and only that output is copied into a distroless runtime:

<svg viewBox="0 0 700 200" width="100%" role="img" aria-label="Multi-stage build: a builder stage on node:24-debian13-dev runs npm ci, then only node_modules is copied into a distroless final stage on node:24-debian13 (248MB, no shell, no npm, no curl).">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="8" y="20" width="296" height="162" rx="10" fill="#eef2ff" stroke="#6366f1"></rect>
    <text x="20" y="40" font-weight="700" fill="#3730a3">builder · node:24-debian13-dev</text>
    <rect x="30" y="54" width="244" height="30" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="152" y="74" text-anchor="middle" fill="#24292f">shell + npm</text>
    <line x1="152" y1="84" x2="152" y2="110" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="148,104 152,112 156,104" fill="#6b7280"></polygon>
    <rect x="30" y="112" width="244" height="30" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="152" y="132" text-anchor="middle" fill="#24292f">npm ci --production</text>
    <rect x="396" y="20" width="296" height="162" rx="10" fill="#eafaf0" stroke="#1a7f37"></rect>
    <text x="408" y="40" font-weight="700" fill="#14532d">final · node:24-debian13 · distroless · 248MB</text>
    <rect x="418" y="54" width="252" height="30" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="544" y="74" text-anchor="middle" fill="#24292f">node src/index.js</text>
    <line x1="544" y1="112" x2="544" y2="88" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="540,94 544,86 548,94" fill="#6b7280"></polygon>
    <rect x="418" y="112" width="252" height="30" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="544" y="132" text-anchor="middle" fill="#24292f">node_modules + src</text>
    <text x="544" y="168" text-anchor="middle" font-size="11" fill="#b91c1c" font-weight="700">no shell · no npm · no curl</text>
    <line x1="304" y1="127" x2="416" y2="127" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="410,123 418,127 410,131" fill="#6b7280"></polygon>
    <text x="360" y="119" text-anchor="middle" font-size="10" fill="#57606a">COPY node_modules</text>
  </g>
</svg>

This is the pivot of the workshop. You spent Lab 1 learning to measure an image. Now you
change one thing about where it starts, and measure it again.

---

## Two variants, and why it matters

Docker Hardened Images come in two flavours, and you need both:

| Variant | Tag | What it has |
|---------|-----|-------------|
| Dev | `$$dhiPrefix$$node:24-debian13-dev` | A shell and npm — for building |
| Runtime | `$$dhiPrefix$$node:24-debian13` | Distroless — no shell, no package manager |

Because the runtime variant has no shell, you cannot run `npm install` in it. That
forces a multi-stage build: the dev image installs dependencies, the runtime image
receives only the output. An image with no shell is one an attacker cannot drop into.

---

## Migrate

1. Replace the Dockerfile with a multi-stage build on hardened bases:

    ```dockerfile save-as=Dockerfile
    ###########################################################
    # Stage: base — DHI dev variant, has shell and npm
    ###########################################################
    FROM $$dhiPrefix$$node:24-debian13-dev AS base

    WORKDIR /usr/local/app
    COPY package.json package-lock.json ./

    ###########################################################
    # Stage: production-dependencies
    ###########################################################
    FROM base AS production-dependencies
    ENV NODE_ENV=production
    RUN npm ci --production --ignore-scripts && npm cache clean --force

    ###########################################################
    # Stage: final — DHI runtime variant, distroless
    ###########################################################
    FROM $$dhiPrefix$$node:24-debian13 AS final
    ENV NODE_ENV=production
    WORKDIR /usr/local/app

    COPY --from=production-dependencies /usr/local/app/node_modules ./node_modules
    COPY ./src ./src

    EXPOSE 3000
    CMD ["node", "src/index.js"]
    ```

2. Build it:

    ```bash terminal-id=build
    docker build -t catalog-service:dhi --sbom=true --provenance=mode=max .
    ```

---

## Confirm it still works

A hardened image that breaks your application is not a security win.

```bash terminal-id=build
docker run --rm catalog-service:dhi node --version
```

Same runtime, same app.

---

## Now measure it

1. The overview:

    ```bash terminal-id=build
    docker scout quickview catalog-service:dhi --org $$org$$
    ```

2. The direct comparison:

    ```bash terminal-id=build
    docker scout compare --to catalog-service:baseline catalog-service:dhi --org $$org$$
    ```

3. The size difference:

    ```bash terminal-id=build
    docker images catalog-service
    ```

4. Fill in your table:

    | | Critical | High | Medium | Low | Size |
    |---|---|---|---|---|---|
    | `catalog-service:baseline` | 0 | 8 | 41 | 93 | 1.1GB |
    | `catalog-service:dhi` | 0 | 0 | 1 | 4 | 248MB |

---

## Where did the CVEs go?

This is the part people misunderstand. They were not patched.

1. Count the packages again and compare with Lab 1:

    ```bash terminal-id=build
    docker scout sbom --format spdx --output dhi.spdx.json catalog-service:dhi
    ```

    ```bash terminal-id=build
    jq '.packages | length' dhi.spdx.json
    ```

2. Try to get a shell:

    ```bash terminal-id=build
    docker run --rm catalog-service:dhi sh -c "echo hello"
    ```

The vulnerable packages are **gone**, not fixed. There is no shell to drop into, no
package manager to install with, and no `curl` to fetch a second stage.

---

## Re-run Lab 1 against the base

Everything you learned now returns a different answer.

```bash terminal-id=build
docker scout attest list $$dhiPrefix$$node:24-debian13
```

An SBOM, a VEX document, SLSA provenance and a signature — all shipped with the base
image, all verifiable, none of which you had to produce. Compare that with the agent's
image, which shipped nothing but itself.

---

## Checkpoint

- [ ] `catalog-service:dhi` builds from the same source
- [ ] The runtime still works
- [ ] You have recorded the severity and size deltas
- [ ] You have confirmed there is no shell in the final image
- [ ] You have listed the attestations that arrived with the base

## What you should be thinking

**The attack surface shrank.** Fewer packages, and no shell means a compromised process
has far less to work with. **The evidence burden moved.** In Lab 1 you generated an SBOM
and had nothing to verify. Starting from a hardened base, all of that arrives with the
image, signed by somebody whose job is keeping it current. You still own your application
layer; you are no longer responsible for proving things about an OS you did not assemble.
