# Lab 4 — Securing the Agentic Stack

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, done Hardened base, done Verify &amp; Gate, current Agentic MCP">
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
    <rect x="550" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="634" y="30" fill="#14532d">✓ Verify &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#2496ED" stroke="#0b3d91" stroke-width="2"></rect>
    <text x="817" y="30" fill="#ffffff" font-weight="700">Agentic MCP</text>
  </g>
</svg>

**14 minutes · hands-on**

Now an agent — not a human — decides when to invoke the catalog. The Gateway
verifies the server's signature before it runs, and the server itself is hardened
and sandboxed around the same database:

<svg viewBox="0 0 640 386" width="100%" role="img" aria-label="Securing the agent's tools: an AI Agent calls the MCP Gateway, which verifies signatures. Verified traffic reaches the hardened catalog-mcp:dhi server (read_only, cap_drop ALL, no-new-privileges) exposing list_products, search_products and get_product against the same PostgreSQL catalog DB; unsigned or tampered images are refused.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="250" y="8" width="140" height="32" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="320" y="29" text-anchor="middle" fill="#24292f">AI Agent</text>
    <line x1="320" y1="40" x2="320" y2="60" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="316,54 320,62 324,54" fill="#6b7280"></polygon>
    <rect x="206" y="62" width="228" height="38" rx="6" fill="#eef2ff" stroke="#6366f1"></rect>
    <text x="320" y="86" text-anchor="middle" fill="#3730a3" font-weight="700">MCP Gateway · verify signatures</text>
    <rect x="474" y="63" width="158" height="34" rx="6" fill="#fdecea" stroke="#b91c1c"></rect>
    <text x="553" y="84" text-anchor="middle" fill="#b91c1c" font-weight="700">unsigned / tampered</text>
    <line x1="434" y1="80" x2="472" y2="80" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="466,76 474,80 466,84" fill="#6b7280"></polygon>
    <text x="450" y="74" font-size="10" fill="#b91c1c" font-weight="700">refuses</text>
    <path d="M320,100 L320,126 L242,126 L242,150" stroke="#6b7280" stroke-width="1.5" fill="none"></path>
    <polygon points="238,144 242,152 246,144" fill="#6b7280"></polygon>
    <text x="250" y="120" font-size="10" fill="#1a7f37" font-weight="700">verified</text>
    <rect x="40" y="150" width="400" height="150" rx="10" fill="#eafaf0" stroke="#1a7f37"></rect>
    <text x="56" y="172" font-size="10" fill="#14532d" font-weight="700">catalog-mcp:dhi · read_only · cap_drop ALL · no-new-privileges</text>
    <rect x="64" y="196" width="140" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="134" y="217" text-anchor="middle" fill="#24292f">catalog-mcp</text>
    <rect x="250" y="184" width="150" height="26" rx="5" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="325" y="201" text-anchor="middle" fill="#24292f">list_products</text>
    <rect x="250" y="218" width="150" height="26" rx="5" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="325" y="235" text-anchor="middle" fill="#24292f">search_products</text>
    <rect x="250" y="252" width="150" height="26" rx="5" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="325" y="269" text-anchor="middle" fill="#24292f">get_product</text>
    <g stroke="#6b7280" stroke-width="1.5" fill="none">
      <path d="M204,208 L228,208 L228,197 L248,197"></path>
      <path d="M204,213 L228,213 L228,231 L248,231"></path>
      <path d="M204,218 L228,218 L228,265 L248,265"></path>
    </g>
    <g fill="#6b7280">
      <polygon points="242,193 250,197 242,201"></polygon>
      <polygon points="242,227 250,231 242,235"></polygon>
      <polygon points="242,261 250,265 242,269"></polygon>
    </g>
    <rect x="130" y="338" width="230" height="32" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="245" y="359" text-anchor="middle" fill="#24292f">PostgreSQL · same catalog DB</text>
    <path d="M134,230 L134,320 L245,320 L245,336" stroke="#6b7280" stroke-width="1.5" fill="none"></path>
    <polygon points="241,330 245,338 249,330" fill="#6b7280"></polygon>
  </g>
</svg>

Everything so far has been about an image *you* build and *a human* decides to deploy.
Now the catalog gets a second consumer, and the human leaves the loop entirely.

---

## Why an agent's tools are supply chain

An MCP server is an executable you hand tool-calling authority to. It gets credentials,
network reach, and often filesystem access. It is chosen from a catalogue — sometimes by
the agent itself — at run time.

| | |
|---|---|
| **Rug pull** | The server changes behaviour after you approved it |
| **Tool poisoning** | Instructions invisible to users, clear to the model |
| **Credential exfiltration** | Hardcoded environment variables are an easy target |

Every question you have asked in this workshop applies here. Almost nobody asks them.

---

## Look at the tool surface

The MCP server in this workspace exposes **the same PostgreSQL database the catalog API
uses**.

Open :filelink[catalog_mcp.py]{path="mcp/src/catalog_mcp.py"}. Three tools:
`list_products`, `search_products`, `get_product`. Note what the process holds — a
database connection string. That is the thing an attacker wants, and the thing you are
about to hand to an agent.

---

## Build it on a hardened base

1. Create the Dockerfile:

    ```dockerfile save-as=mcp/Dockerfile
    FROM $$dhiPrefix$$python:3.13

    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY src/ ./src/

    # No shell. No curl. No package manager.
    # Only what the server needs to answer a question about products.
    CMD ["python", "src/catalog_mcp.py"]
    ```

2. Build it:

    ```bash terminal-id=build
    docker build -t catalog-mcp:dhi ./mcp
    ```

---

## Harden the runtime too

A hardened image with a careless runtime configuration is half a job.

1. Create the compose file:

    ```yaml save-as=mcp/compose.yaml
    services:
      catalog-mcp:
        build: .
        image: catalog-mcp:dhi

        # Three lines that change what a compromised server can do next.
        read_only: true
        cap_drop: [ALL]
        security_opt: [no-new-privileges]

        environment:
          DATABASE_URL: postgres://postgres:postgres@postgres:5432/catalog
    ```

2. Start it:

    ```bash terminal-id=main
    docker compose -f mcp/compose.yaml up -d
    ```

3. Confirm the restrictions actually applied:

    ```bash terminal-id=build
    docker inspect catalog-mcp --format '{{.HostConfig.ReadonlyRootfs}} {{.HostConfig.CapDrop}}'
    ```

---

## Verify before you invoke

1. Check what you just built:

    ```bash terminal-id=build
    docker scout quickview catalog-mcp:dhi --org $$org$$
    ```

2. List its attestations:

    ```bash terminal-id=build
    docker scout attest list catalog-mcp:dhi
    ```

---

## Let the Gateway verify for you

Nobody verifies by hand on every invocation. The MCP Gateway performs provenance
verification on pull and run, checks for an SBOM, runs supply-chain checks, and mounts
secrets only into the target container.

```bash terminal-id=main
docker mcp gateway run --verify-signatures
```

Point the Gateway at an unsigned or tampered server image and it declines to run it.
Same lesson as the broken signature in Lab 3, one layer up: **a check is only worth
something once you have seen it say no.**

---

## Don't hand-harden every server — pull the hardened catalog

You hardened `catalog-mcp` because it is *your* code. But most tools an agent reaches for —
filesystem, git, GitHub, a database client — are off-the-shelf. Docker publishes those
already hardened, signed and attested as the **Docker Hardened Images MCP Catalog**
(`docker/mcp-catalog-dhi`) — the same catalog you can browse under **MCP Toolkit** in
Docker Desktop. Same guarantees as the image you just built, none of the Dockerfile work.

1. Pull the hardened catalog from the registry:

    ```bash terminal-id=main
    docker mcp catalog pull docker/mcp-catalog-dhi:latest
    ```

2. List what it ships — hardened variants of the servers an agent commonly wants:

    ```bash terminal-id=build
    docker mcp catalog server ls docker/mcp-catalog-dhi
    ```

3. Run one through the Gateway. The signature check you just saw still applies — these
   arrive signed, so it passes without you building anything:

    ```bash terminal-id=main
    docker mcp gateway run --catalog docker/mcp-catalog-dhi:latest --servers filesystem
    ```

> [!NOTE]
> **Two DHI tools, one theme.** This *catalog* gives the agent hardened servers to **run**.
> Docker also hosts a **DHI MCP server** at `dhi.io/mcp` the agent can **query** to pick
> hardened base images — search by name, CVEs, attestations, or FIPS/STIG compliance. Both
> put the same evidence one `docker mcp` command away.
> See <https://docs.docker.com/dhi/tools/mcp/>.

---

## Checkpoint

- [ ] The catalog MCP server builds on a hardened base
- [ ] It runs read-only, with all capabilities dropped
- [ ] You have inspected its attestations
- [ ] You have seen verification reject something
- [ ] You have pulled a pre-hardened server from Docker's DHI MCP catalog

## What you should be thinking

The catalog API and the catalog MCP server are the same kind of object: software you did
not write all of, pulled from a registry, running with credentials against your data. The
only difference is that a human decided to deploy one, and an agent decides when to invoke
the other.

The answer is not a new category of tool. It is the same supply chain controls — SBOM,
VEX, provenance, signatures, policy — applied to a surface most teams have not yet noticed
is part of their supply chain. Same three questions. Same answers. Different layer.
