# Lab 4 — The Agent's Build Sandbox

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, done Hardened base, done Verify &amp; Gate, current Build Sandbox">
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
    <text x="817" y="30" fill="#ffffff" font-weight="700">Build Sandbox</text>
  </g>
</svg>

**10 minutes · hands-on**

Every lab so far cleaned up something the agent already shipped. This one moves the fix
earlier. You give the agent a **sandbox** — its own microVM, off your host — and wire the
**DHI MCP server** into it, so the agent can ask *"what is the hardened base for Node, and
what CVEs does it carry?"* before it writes a single line of Dockerfile.

<svg viewBox="0 0 640 284" width="100%" role="img" aria-label="The sbx sandbox boundary. A prompt to containerise the app drives the agent; the agent calls the DHI MCP server, which exposes signed tools only, and chooses FROM dhi.io/node before writing the Dockerfile. The sandbox is a microVM with its own daemon and network and a read-only host. The resulting image has zero critical, high, medium and low CVEs, 211 packages, an attached SBOM, is signed and runs non-root.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="8" y="8" width="624" height="196" rx="14" fill="#eef4ff" stroke="#2563eb" stroke-dasharray="6 5"></rect>
    <text x="28" y="34" fill="#1e3a8a" font-weight="700" font-size="13">Sandbox boundary — sbx microVM</text>
    <text x="28" y="52" fill="#3b5bdb" font-size="11">Own daemon · own network · host read-only</text>
    <rect x="28" y="74" width="120" height="44" rx="6" fill="#f3f4f6" stroke="#8c959f"></rect>
    <text x="88" y="98" text-anchor="middle" fill="#24292f" font-weight="700">Prompt</text>
    <text x="88" y="112" text-anchor="middle" fill="#5b6670" font-size="10">containerise app</text>
    <rect x="250" y="74" width="120" height="44" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="310" y="98" text-anchor="middle" fill="#24292f" font-weight="700">Agent</text>
    <text x="310" y="112" text-anchor="middle" fill="#5b6670" font-size="10">full permissions</text>
    <rect x="470" y="74" width="150" height="44" rx="6" fill="#eef2ff" stroke="#6366f1"></rect>
    <text x="545" y="98" text-anchor="middle" fill="#3730a3" font-weight="700">DHI MCP server</text>
    <text x="545" y="112" text-anchor="middle" fill="#4f46e5" font-size="10">signed tools only</text>
    <line x1="148" y1="96" x2="246" y2="96" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="246,92 254,96 246,100" fill="#6b7280"></polygon>
    <line x1="370" y1="96" x2="466" y2="96" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="466,92 474,96 466,100" fill="#6b7280"></polygon>
    <line x1="310" y1="118" x2="310" y2="146" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="306,146 310,154 314,146" fill="#6b7280"></polygon>
    <rect x="235" y="152" width="150" height="40" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="310" y="170" text-anchor="middle" fill="#24292f" font-weight="700">FROM dhi.io/node</text>
    <text x="310" y="184" text-anchor="middle" fill="#5b6670" font-size="10">queried before writing</text>
    <line x1="320" y1="204" x2="320" y2="220" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="316,220 320,228 324,220" fill="#6b7280"></polygon>
    <rect x="8" y="228" width="624" height="48" rx="10" fill="#dbeafe" stroke="#2563eb"></rect>
    <text x="320" y="250" text-anchor="middle" fill="#1e3a8a" font-weight="700" font-size="14">0C · 0H · 0M · 0L CVEs</text>
    <text x="320" y="267" text-anchor="middle" fill="#3b5bdb" font-size="11">211 packages · SBOM attached · signed · non-root</text>
  </g>
</svg>

In **Section 2** the same agent, on your host, reached for `node:20` with no guidance and
built an image carrying **122 low, 25 medium, 26 high and 2 critical** CVEs — 806 packages,
no SBOM, running as root. Nothing failed. Nothing warned. This lab is the environment that
run should have happened in: the agent boxed in, and pointed at trusted tools.

---

## Two runs, one prompt

The prompt does not change. The environment around the agent does.

| | Agent on your host | Agent in the sbx sandbox |
|---|---|---|
| **Boundary** | Host daemon, host credentials, no boundary | microVM: own daemon, own network, host read-only |
| **Base image** | `FROM node:20`, chosen with no guidance | `FROM dhi.io/node`, queried before writing |
| **Tools** | Open registries, no allowlist | DHI MCP server, signed tools, policy-gated |
| **Result** | 2C · 26H · 25M · 122L · 806 pkgs · root | 0C · 0H · 0M · 0L · 211 pkgs · signed · non-root |

You did not make the agent slower or less capable. You changed what it can reach.

---

## What `sbx` is

`sbx` runs an agent inside a lightweight microVM. The agent still gets full permissions —
but *inside the box*: its own Docker daemon, its own network, and a **read-only** view of
your host. A prompt-injected or misbehaving agent cannot reach your host daemon or your
credentials, because from inside the sandbox they are not there.

---

## Set up the sandbox

One-time host setup — install the CLI and point it at the Docker MCP gateway:

```bash no-run-button
brew install docker/tap/sbx
export SBX_MCP_URL=https://gateway.docker.com
```

Start the sandbox daemon:

```bash terminal-id=main
sbx daemon start -d
```

Nothing is wired in yet. Confirm the sandbox has no MCP servers:

```bash terminal-id=build
sbx mcp ls
```

---

## Govern the tools first

Before you hand the agent any tools, decide what it is allowed to do with them. `sbx`
enforces a **Cedar** access policy over three MCP actions: `register` a server,
`invokeTool` on it, and `invokePrimordial` (the built-in gateway primitives). Save a policy
that permits them:

```cedar save-as=mcp-policy.cedar
permit (
    principal,
    action == MCP::Action::"register",
    resource
);

permit (
    principal,
    action == MCP::Action::"invokeTool",
    resource
);

permit (
    principal,
    action == MCP::Action::"invokePrimordial",
    resource
);
```

> [!WARNING]
> This policy permits **every** action against **every** resource — fine to unblock the
> lab, but it is "governance turned off." In production you scope `invokeTool` to the
> read-only DHI tools and deny the mutating ones (`dhi_create_mirror`, `dhi_remove_mirror`):
>
> ```cedar
> permit (principal, action == MCP::Action::"invokeTool", resource)
> when {
>   resource.server == "remotedhi" &&
>   ["dhi_get_image_cves","dhi_get_image_details","dhi_get_image_packages",
>    "dhi_get_image_attestations","dhi_get_tag_definition","dhi_get_repository",
>    "dhi_list_repositories","dhi_list_mirrors"].contains(resource.tool)
> };
> ```

---

## Wire in the DHI MCP server

Docker hosts the **DHI MCP server** at `https://dhi.io/mcp` — a remote server the agent
queries to choose hardened base images (search by name, CVEs, attestations, packages, or
compliance). Register it with the sandbox by URL:

```bash terminal-id=main
sbx mcp add remotedhi --url https://dhi.io/mcp
```

Inspect what you just added:

```bash terminal-id=build
sbx mcp inspect remotedhi
```

It is a **remote** server over `streamable-http`. The tools it now exposes to the sandboxed
agent are read-only queries against Docker's hardened catalog —
`dhi_get_image_cves`, `dhi_get_image_details`, `dhi_get_image_packages`,
`dhi_get_image_attestations`, `dhi_get_tag_definition`, `dhi_get_repository`,
`dhi_list_repositories` — plus mirror management (`dhi_list_mirrors`, `dhi_create_mirror`,
`dhi_remove_mirror`), which your policy above is where you'd lock down.

Confirm it registered:

```bash terminal-id=build
sbx mcp ls
```

Now the agent, boxed inside the sandbox, can call `dhi_get_image_cves` on a base image
*before* it writes `FROM` — and the CVE report it gets back is the same signed evidence you
measured by hand in Labs 1–3.

---

## Access the tools from the agent

Drop the sandboxed agent into a session with the DHI MCP server statically attached:

```bash terminal-id=main
sbx run codex --static-mcp remotedhi
```

Inside the session, type `/mcp` to list the tools now reachable:

```bash terminal-id=main
/mcp
```

You'll see the gateway plus every DHI tool, each prefixed with the server name:

- **read-only queries** — `remotedhi__dhi_get_image_cves`, `dhi_get_image_details`,
  `dhi_get_image_packages`, `dhi_get_image_attestations`, `dhi_get_tag_definition`,
  `dhi_get_repository`, `dhi_list_repositories`, `dhi_list_mirrors`
- **mirror mutators** — `remotedhi__dhi_create_mirror`, `remotedhi__dhi_remove_mirror`

The read-only `dhi_get_*` / `dhi_list_*` queries are what a good agent calls to check a base
image before it writes `FROM`. The two mirror mutators are exactly what the scoped Cedar
policy above keeps out of reach.

---

## Checkpoint

- [ ] The `sbx` daemon is running — an agent here works inside a microVM, not on your host
- [ ] An MCP access policy governs `register` / `invokeTool` / `invokePrimordial`
- [ ] The DHI MCP server is registered as a remote server by URL
- [ ] `sbx mcp inspect` shows it as `remote` over `streamable-http`
- [ ] `sbx mcp ls` lists `remotedhi`

## What you should be thinking

The other labs asked the same three questions *after* the agent shipped. This one moves them
to the moment of authoring: a boundary so a bad agent cannot reach your host, a policy so it
can only use the tools you allow, and a signed tool so a good agent can check a base image's
CVEs before it commits to it.

The fast path and the safe path become the same path — not because you reviewed the output,
but because the agent could only reach hardened, verified, policy-gated inputs in the first
place.
