# Securing the Agentic Stack

<img width="769" height="418" alt="image" src="https://github.com/user-attachments/assets/facffcfa-6c9c-4f9e-9e20-2d043825d861" />

## Start at the finish line

Here is where this workshop ends: one application on a single, verifiable path from a
developer's prompt to production. Read it left to right.

<svg viewBox="0 0 900 250" width="100%" role="img" aria-label="The dev-to-prod path. On the left, a DEVELOPMENT zone wrapped in an sbx sandbox boundary: the agent authors in a sandbox querying the DHI MCP server before FROM, starts from a hardened base with 0 CVEs, builds with an SBOM and provenance, and signs keyless. In the middle, a CI gate that fails closed - the boundary to production. On the right, a PRODUCTION zone wrapped in a runtime box (read_only, cap_drop ALL, non-root): the signed image is deployed and invoked by an agent or MCP client with signed, read-only tools. Beneath the development zone, a red strip marks the ungoverned baseline: node:20 picked blind, 431 packages, no SBOM, running as root.">
  <g font-family="ui-sans-serif, system-ui, sans-serif">
    <!-- DEV zone -->
    <rect x="6" y="30" width="470" height="150" rx="12" fill="#dce4ff" stroke="#2563eb" stroke-width="2" stroke-dasharray="7 5"/>
    <text x="20" y="52" font-size="14" font-weight="700" fill="#1e3a8a">DEVELOPMENT</text>
    <rect x="18" y="66" width="112" height="104" rx="8" fill="#eef3ff" stroke="#4f46e5" stroke-width="1.5" stroke-dasharray="4 4"/>
    <text x="74" y="82" text-anchor="middle" font-size="9.5" font-weight="700" fill="#3730a3">sbx microVM</text>
    <!-- DEV cards -->
    <rect x="24" y="90" width="100" height="72" rx="7" fill="#0b1533"/>
    <text x="34" y="108" font-size="10" font-weight="700" fill="#7da2ff">DEVELOP</text>
    <text x="34" y="126" font-size="10.5" font-weight="700" fill="#ffffff">Agent in box</text>
    <text x="34" y="142" font-size="9" fill="#9aa6c2">DHI MCP before</text>
    <text x="34" y="153" font-size="9" fill="#9aa6c2">it writes FROM</text>
    <rect x="136" y="90" width="100" height="72" rx="7" fill="#0b1533"/>
    <text x="146" y="108" font-size="10" font-weight="700" fill="#7da2ff">BASE</text>
    <text x="146" y="126" font-size="10.5" font-weight="700" fill="#ffffff">Hardened</text>
    <text x="146" y="142" font-size="9" fill="#9aa6c2">DHI · 0 CVEs</text>
    <text x="146" y="153" font-size="9" fill="#9aa6c2">SLSA L3</text>
    <rect x="248" y="90" width="100" height="72" rx="7" fill="#0b1533"/>
    <text x="258" y="108" font-size="10" font-weight="700" fill="#7da2ff">BUILD</text>
    <text x="258" y="126" font-size="10.5" font-weight="700" fill="#ffffff">Buildx</text>
    <text x="258" y="142" font-size="9" fill="#9aa6c2">SBOM +</text>
    <text x="258" y="153" font-size="9" fill="#9aa6c2">provenance</text>
    <rect x="360" y="90" width="100" height="72" rx="7" fill="#0b1533"/>
    <text x="370" y="108" font-size="10" font-weight="700" fill="#7da2ff">SIGN</text>
    <text x="370" y="126" font-size="10.5" font-weight="700" fill="#ffffff">Keyless</text>
    <text x="370" y="142" font-size="9" fill="#9aa6c2">bound to</text>
    <text x="370" y="153" font-size="9" fill="#9aa6c2">digest</text>
    <!-- GATE -->
    <rect x="492" y="66" width="86" height="104" rx="10" fill="#fff3e0" stroke="#d97706" stroke-width="2.5"/>
    <text x="535" y="96" text-anchor="middle" font-size="12" font-weight="700" fill="#9a3412">CI GATE</text>
    <text x="535" y="118" text-anchor="middle" font-size="9" fill="#9a3412">no crit CVEs</text>
    <text x="535" y="131" text-anchor="middle" font-size="9" fill="#9a3412">SBOM · prov</text>
    <text x="535" y="152" text-anchor="middle" font-size="10.5" font-weight="700" fill="#b91c1c">FAIL CLOSED</text>
    <!-- PROD zone -->
    <rect x="594" y="30" width="300" height="150" rx="12" fill="#e6f4ea" stroke="#1a7f37" stroke-width="2" stroke-dasharray="7 5"/>
    <text x="608" y="52" font-size="14" font-weight="700" fill="#14532d">PRODUCTION</text>
    <rect x="606" y="66" width="276" height="104" rx="8" fill="#f0faf3" stroke="#1a7f37" stroke-width="1.5" stroke-dasharray="4 4"/>
    <text x="744" y="82" text-anchor="middle" font-size="9.5" font-weight="700" fill="#14532d">runtime box · read_only · cap_drop ALL · non-root</text>
    <rect x="614" y="92" width="126" height="70" rx="7" fill="#0b1533"/>
    <text x="626" y="110" font-size="10" font-weight="700" fill="#6ee7a8">DEPLOY</text>
    <text x="626" y="128" font-size="10.5" font-weight="700" fill="#ffffff">Signed image</text>
    <text x="626" y="146" font-size="9" fill="#9aa6c2">verified · pinned by digest</text>
    <rect x="748" y="92" width="126" height="70" rx="7" fill="#0b1533"/>
    <text x="760" y="110" font-size="10" font-weight="700" fill="#6ee7a8">INVOKE</text>
    <text x="760" y="128" font-size="10.5" font-weight="700" fill="#ffffff">Agent / MCP client</text>
    <text x="760" y="146" font-size="9" fill="#9aa6c2">signed, read-only tools</text>
    <!-- arrows -->
    <g stroke="#64748b" stroke-width="2" fill="#64748b">
      <line x1="124" y1="126" x2="134" y2="126"/><polygon points="134,121 143,126 134,131"/>
      <line x1="236" y1="126" x2="246" y2="126"/><polygon points="246,121 255,126 246,131"/>
      <line x1="348" y1="126" x2="358" y2="126"/><polygon points="358,121 367,126 358,131"/>
      <line x1="460" y1="126" x2="490" y2="126"/><polygon points="490,121 499,126 490,131"/>
    </g>
    <g stroke="#1a7f37" stroke-width="2.5" fill="#1a7f37">
      <line x1="578" y1="126" x2="612" y2="126"/><polygon points="612,120 623,126 612,132"/>
    </g>
    <!-- red baseline strip -->
    <rect x="6" y="192" width="470" height="46" rx="8" fill="#fdecea" stroke="#f0b4ae" stroke-width="1.2"/>
    <text x="20" y="212" font-size="10.5" font-weight="700" fill="#b91c1c">UNGOVERNED BASELINE — what the agent ships on your host</text>
    <text x="20" y="229" font-size="10" fill="#8a1c13">FROM node:20 · 431 pkgs · no SBOM · root · nothing you can prove</text>
  </g>
</svg>

On the left, **development**: an agent authors the image inside a sandbox it cannot
escape, starts from a hardened base, and emits an SBOM, provenance and a signature. In the
middle, a **CI gate that fails closed** - the boundary you cross to reach production. On the
right, **production**: only that signed, verified artifact runs, in a runtime box of its
own, invoked by agents that can reach only signed, read-only tools.

That is the finish line. **Now the start line - the red box.**

The application in this workspace is going to be containerised by an AI agent, not by you.

It is a Node.js **catalog** service - a frontend, a backend API, and a Postgres
database, talking to **Kafka**, **LocalStack** and **WireMock**. Right now it is just
source: no Dockerfile, no image. In a moment you will hand it to an agent with one
instruction - *containerise this for production* - and in about a minute it will choose a
base image, resolve several hundred packages, write a Dockerfile, and build successfully.
Nothing will fail. Nothing will warn.

What it ships is that red strip: `node:20` picked blind, 431 packages, no SBOM, running as
root, on your host. It *works*. You can prove nothing about it. Over the next ninety minutes
you close the gap between the red box and the road above - one stage at a time.

## What changed

The software supply chain did not change. The review step did.

| Traditional workflow | Agentic workflow |
|---------------------|------------------|
| A developer picks a base image, with intent | An agent picks one, autonomously |
| Dependencies are reviewed in a pull request | Packages are resolved with no human review |
| CI runs configuration a human wrote | The agent wrote the Dockerfile |

> **The better the agent, the bigger the blast radius.**

The agent does not have to do anything *wrong* for this to be a problem. Suppose it
wrote an excellent Dockerfile - non-root, multi-stage, minimal. The vulnerabilities are
in the dependency tree either way, and you still cannot say where any of it came from.

## The three questions

Every tool in this workshop answers exactly one of these:

| Question | Answer |
|----------|--------|
| **What is in it?** | SBOM |
| **Where did it come from?** | SLSA provenance |
| **Can you verify that claim?** | Signatures |

And a fourth, once you have the first three: *which of these vulnerabilities actually
affects me?* → **VEX**

## Your journey - walking the road, one stage at a time

Each lab is a stage on the dev-to-prod path above. You reach the finish line by fixing what
breaks at each stage - measured against the red baseline you start with.

| Stage on the road | Lab | What breaks here without it | What the catalog gains |
|-------------------|-----|-----------------------------|------------------------|
| The start line | - | The agent ships blind - no evidence at all | A measurement of the red box |
| **BUILD** | 1 | You cannot say what is in it or which findings matter | SBOM, VEX and provenance you can read |
| **BASE** | 2 | CVEs accumulate from a base nobody chose | **A hardened base - the pivot** |
| **SIGN + GATE** | 3 | Nothing stops the next merge undoing all of it | A verified signature and a gate that fails closed |
| **DEVELOP** (+ INVOKE) | 4 | The fix only ever happens *after* the agent ships | A sandbox and the DHI MCP server - the fix moved to authoring time |

**Lab 2 is the centre of gravity.** Lab 1 teaches you to measure an image. Lab 2 is
where the measurement pays off, and every number you wrote down changes. **Lab 4 then moves
the whole fix left** - to development - so a well-boxed agent reaches the same result on its
own, and the red box never happens in the first place.

## What you are working with

You will be working with the Product Catalog service: a `frontend/` (React), a `src/`
backend (a REST API over a PostgreSQL product database, talking to Kafka, LocalStack (S3)
and WireMock), and the database schema in `db/`. There is no Dockerfile and no compose
file yet - the agent writes those next.

Continue to **Setup**.
