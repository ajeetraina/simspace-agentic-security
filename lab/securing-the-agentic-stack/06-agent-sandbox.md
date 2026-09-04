# Lab 4 - The Agent's Build Sandbox

<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="Progress spine: the development-to-production road. Stages DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone (a read-only runtime box). Done stages are checked green, the current stage is marked.">
<g font-family="ui-sans-serif, system-ui, sans-serif">
<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>
<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>
<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>
<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>
<rect x="8" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#2563eb" stroke-width="3"/><text x="67.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">DEVELOP</text><text x="67.0" y="34" text-anchor="middle" font-size="10" font-weight="800" fill="#2563eb">▶ you are here</text>
<rect x="134" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="193.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BASE</text><circle cx="239" cy="52" r="9" fill="#1a7f37"/><path d="M235,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="260" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="319.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BUILD</text><circle cx="365" cy="52" r="9" fill="#1a7f37"/><path d="M361,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="386" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="445.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">SIGN</text><circle cx="491" cy="52" r="9" fill="#1a7f37"/><path d="M487,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="536" y="32" width="70" height="60" rx="10" fill="#fff3e0" stroke="#1a7f37" stroke-width="2.5"/><text x="571.0" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="#9a3412">GATE</text><text x="571.0" y="76" text-anchor="middle" font-size="8.5" fill="#9a3412">fail closed</text><circle cx="594" cy="44" r="9" fill="#1a7f37"/><path d="M590,44 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="628" y="40" width="126" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="691.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">DEPLOY</text><circle cx="741" cy="52" r="9" fill="#1a7f37"/><path d="M737,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="766" y="40" width="126" height="44" rx="9" fill="#0b1533" stroke="#2563eb" stroke-width="3"/><text x="829.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">INVOKE</text>
<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">
<line x1="126" y1="62" x2="134" y2="62"/><polygon points="134,59 139,62 134,65"/>
<line x1="252" y1="62" x2="260" y2="62"/><polygon points="260,59 265,62 260,65"/>
<line x1="378" y1="62" x2="386" y2="62"/><polygon points="386,59 391,62 386,65"/>
<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>
<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>
</g>
</g></svg>

**10 minutes · hands-on**

> **Where you are on the road:** all the way back at the **left edge - development**. Labs
> 1-3 fixed the artifact *after* the agent shipped it. This lab moves the fix to the moment
> of authoring, so the red box never happens. It is also the workshop's real punchline: a
> sandbox appears at **both ends** of the road. The agent that *builds* the image runs in a
> box it cannot escape (the sbx microVM here); the service it *becomes* runs in a box too
> (the `read_only`, `cap_drop ALL` runtime you saw at the production edge). Same discipline -
> least privilege - at authoring time and at runtime.

Every lab so far cleaned up something the agent already shipped. This one moves the fix
earlier. You give the agent a **sandbox** - its own microVM, off your host - and wire the
**DHI MCP server** into it, so the agent can ask *"what is the hardened base for Node, and
what CVEs does it carry?"* before it writes a single line of Dockerfile.

<svg viewBox="0 0 640 284" width="100%" role="img" aria-label="The sbx sandbox boundary. A prompt to containerise the app drives the agent; the agent calls the DHI MCP server, which exposes signed tools only, and chooses FROM dhi.io/node before writing the Dockerfile. The sandbox is a microVM with its own daemon and network and a read-only host. The resulting image has 0 critical, 0 high, 1 medium and 4 low CVEs, 78 packages, an attached SBOM, is signed and runs non-root.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12">
    <rect x="8" y="8" width="624" height="196" rx="14" fill="#eef4ff" stroke="#2563eb" stroke-dasharray="6 5"></rect>
    <text x="28" y="34" fill="#1e3a8a" font-weight="700" font-size="13">Sandbox boundary - sbx microVM</text>
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
    <text x="320" y="250" text-anchor="middle" fill="#1e3a8a" font-weight="700" font-size="14">0C · 0H · 1M · 4L CVEs</text>
    <text x="320" y="267" text-anchor="middle" fill="#3b5bdb" font-size="11">78 packages · SBOM attached · signed · non-root</text>
  </g>
</svg>

In **Section 2** the same agent, on your host, reached for `node:20` with no guidance and
built an image carrying **93 low, 41 medium, 8 high and 0 critical** CVEs - 431 packages,
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
| **Result** | 0C · 8H · 41M · 93L · 431 pkgs · root | 0C · 0H · 1M · 4L · 78 pkgs · signed · non-root |

You did not make the agent slower or less capable. You changed what it can reach.

---

## What `sbx` is

`sbx` runs an agent inside a lightweight microVM. The agent still gets full permissions -
but *inside the box*: its own Docker daemon, its own network, and a **read-only** view of
your host. A prompt-injected or misbehaving agent cannot reach your host daemon or your
credentials, because from inside the sandbox they are not there.

---

## Set up the sandbox

One-time host setup - install the CLI and point it at the Docker MCP gateway:

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

> [!NOTE]
> You are wiring this sandbox up by hand, one command at a time. The whole environment -
> agent, MCP servers, and policy - can also be declared once in a **sandbox environment
> file** and recreated on demand, which is how you'd keep it reproducible across a team or a
> CI job. You'll assemble that file at the end of this lab, in
> [One file, the whole sandbox](#one-file-the-whole-sandbox). Full field reference:
> [Docker Sandbox environments](https://docs.docker.com/ai/sandboxes/sandbox-environments/).

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
> This policy permits **every** action against **every** resource - fine to unblock the
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

Docker hosts the **DHI MCP server** at `https://dhi.io/mcp` - a remote server the agent
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
agent are read-only queries against Docker's hardened catalog -
`dhi_get_image_cves`, `dhi_get_image_details`, `dhi_get_image_packages`,
`dhi_get_image_attestations`, `dhi_get_tag_definition`, `dhi_get_repository`,
`dhi_list_repositories` - plus mirror management (`dhi_list_mirrors`, `dhi_create_mirror`,
`dhi_remove_mirror`), which your policy above is where you'd lock down.

Confirm it registered:

```bash terminal-id=build
sbx mcp ls
```

Now the agent, boxed inside the sandbox, can call `dhi_get_image_cves` on a base image
*before* it writes `FROM` - and the CVE report it gets back is the same signed evidence you
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

- **read-only queries** - `remotedhi__dhi_get_image_cves`, `dhi_get_image_details`,
  `dhi_get_image_packages`, `dhi_get_image_attestations`, `dhi_get_tag_definition`,
  `dhi_get_repository`, `dhi_list_repositories`, `dhi_list_mirrors`
- **mirror mutators** - `remotedhi__dhi_create_mirror`, `remotedhi__dhi_remove_mirror`

The read-only `dhi_get_*` / `dhi_list_*` queries are what a good agent calls to check a base
image before it writes `FROM`. The two mirror mutators are exactly what the scoped Cedar
policy above keeps out of reach.

---

## Now let the agent build it

The server is wired in - so close the loop. Hand the sandboxed agent the **same containerise
prompt from Section 2**, the one that shipped 2 critical CVEs on your host. Nothing about the
prompt changes; only the environment around the agent does.

```bash terminal-id=main
sbx run codex --static-mcp remotedhi -p "Containerise catalog-service for production. Choose a hardened base image, keep the final image shell-free, and attach an SBOM."
```

Read the transcript top to bottom. Before it writes a single `FROM`, the agent calls
`remotedhi__dhi_get_image_cves` and `dhi_get_tag_definition` against Docker's hardened
catalog, sees that `dhi.io/node:24-debian13` carries zero CVEs and ships its own
attestations, and *only then* writes a multi-stage Dockerfile - the `-dev` variant to build,
the distroless runtime to ship.

Now measure what it produced, with the exact commands you ran by hand in Lab 2:

```bash terminal-id=build
docker scout quickview catalog-service:dhi --org $$org$$
```

```bash terminal-id=build
docker scout compare --to catalog-service:baseline catalog-service:dhi --org $$org$$
```

Same base, same multi-stage shape, same numbers. **In Lab 2 you rewrote the Dockerfile
yourself to reach this image. Here the agent reached it on its own** - unattended, inside a
box it could not escape, from signed catalog data it could not forge. The fast path it took
by itself *is* the hardened one.

---

## One file, the whole sandbox

You wired this box up one command at a time - start the daemon, add the MCP server, point it
at a policy, run the agent. That is fine to learn on, but it lives in your shell history and
nobody else can reproduce it. A **sandbox environment file** declares the same thing once -
the agent, the DHI MCP server, and the governing policy - so a teammate or a CI job recreates
the identical box from a file committed to the repo.

Save it at the repo root as `.sbxenv.yaml`:

```yaml save-as=.sbxenv.yaml
schemaVersion: "1"
name: catalog-sandbox
agent: codex

workspace:
  path: catalog-service
  clone: true

# Governance profile that carries the Cedar policy below -
# the scoped, read-only DHI rules, not the wide-open one.
sandboxOptions:
  profile: dhi-readonly

mcp:
  servers:
    - name: remotedhi
      url: https://dhi.io/mcp
```

The env file has no field for inline Cedar - governance is referenced by profile name. The
`dhi-readonly` profile carries the scoped policy from the warning earlier: register and the
built-in primitives are allowed, but `invokeTool` is permitted **only** for the read-only
`dhi_get_*` / `dhi_list_*` queries, so the two mirror mutators stay out of reach.

```cedar save-as=dhi-readonly.cedar
permit (principal, action == MCP::Action::"register", resource);
permit (principal, action == MCP::Action::"invokePrimordial", resource);

permit (principal, action == MCP::Action::"invokeTool", resource)
when {
  resource.server == "remotedhi" &&
  ["dhi_get_image_cves","dhi_get_image_details","dhi_get_image_packages",
   "dhi_get_image_attestations","dhi_get_tag_definition","dhi_get_repository",
   "dhi_list_repositories","dhi_list_mirrors"].contains(resource.tool)
};
```

Now the three commands you ran by hand collapse into one. `sbx env run` creates the sandbox
if it doesn't exist, registers `remotedhi`, applies the profile, and attaches you to the
`codex` session - reading `.sbxenv.yaml` from the working directory:

```bash terminal-id=main
sbx env run
```

Same boundary, same signed tools, same policy - except now it is a file in the repo, not a
sequence you have to remember. Tear it down just as declaratively when you're done:

```bash terminal-id=build
sbx env rm
```

---

## Checkpoint

- [ ] The `sbx` daemon is running - an agent here works inside a microVM, not on your host
- [ ] An MCP access policy governs `register` / `invokeTool` / `invokePrimordial`
- [ ] The DHI MCP server is registered as a remote server by URL
- [ ] `sbx mcp inspect` shows it as `remote` over `streamable-http`
- [ ] `sbx mcp ls` lists `remotedhi`
- [ ] The sandboxed agent queried the DHI catalog *before* choosing a base
- [ ] The image it built matches the `catalog-service:dhi` you made by hand in Lab 2

## What you should be thinking

The other labs asked the same three questions *after* the agent shipped. This one moves them
to the moment of authoring: a boundary so a bad agent cannot reach your host, a policy so it
can only use the tools you allow, and a signed tool so a good agent can check a base image's
CVEs before it commits to it.

The fast path and the safe path become the same path - not because you reviewed the output,
but because the agent could only reach hardened, verified, policy-gated inputs in the first
place.
