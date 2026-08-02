# Securing the Agentic Stack 

An interactive, fully in-browser lab built on
[Simspace](https://github.com/dockersamples/simspace). Everything in the terminal
is simulated — no real Docker, backend, or network — so it runs the same for
everyone, with nothing to install.

**The story:** an AI agent containerises a real Node.js catalog service — frontend,
backend, Kafka, LocalStack and WireMock — without supervision. Over eight sections
you turn what it shipped into a signed, attested, policy-gated artifact, then extend
the same guarantees to the tools the agent itself calls:

1. **An Agent Built This** — prompt the agent (`claude -p "…"`) and watch it build
2. **SBOM, VEX, SLSA** — learn to measure what's inside the image
3. **Start From a Trusted Base** — migrate to Docker Hardened Images (the pivot)
4. **Sign It, Then Gate It** — cosign + a Scout policy gate in CI
5. **Securing the Agentic Stack** — a hardened, sandboxed MCP server

The lab lives under [`lab/securing-the-agentic-stack/`](lab/securing-the-agentic-stack/):
`labspace.yaml` (config + seeded virtual filesystem), `simulator.yaml` (command
behaviour), and one markdown file per section. It's loaded at runtime by a prebuilt
image, so there's no build step for content.

## Author locally

You only need Docker.

```bash
docker compose up dev              # live preview at http://localhost:5173
docker compose run --rm validate   # lint the lab (fails on errors)
```

Edit the files under `lab/securing-the-agentic-stack/` and refresh the browser to
see changes:

- `labspace.yaml` — title, terminals, seed files, sections, variables
- `simulator.yaml` — what each command does (scenarios)
- `*.md` — one file per section of instructions

Pin the toolchain to a released version for reproducibility:

```bash
export SIMSPACE_AUTHORING_IMAGE=dockersamples/simspaceweb-authoring:1
```

## Deploy

**GitHub Pages (default):** enable Pages (Settings → Pages → Source: "GitHub
Actions"), then push to `main`. The workflow in
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) validates the lab
and publishes it. Pin `runtime-tag` there to a released version for a stable lab.
Pull requests are validated first by
[`.github/workflows/validate.yml`](.github/workflows/validate.yml).

**As a container:** the [`Dockerfile`](Dockerfile) bases on the runtime image and
swaps in your lab.

```bash
docker build -t my-lab .
docker run --rm -p 8080:80 my-lab    # http://localhost:8080
```

## Authoring with an AI agent

This repo is set up for agent authoring. In Claude Code, an `authoring-lab` skill
(under `.claude/`) knows the workflow, `docker compose` / `validate-lab` are
pre-allowed, and a hook auto-validates the lab after every edit under `lab/`.
[`CLAUDE.md`](CLAUDE.md) loads the guide automatically.

## Learn more

See [`AGENTS.md`](AGENTS.md) for an authoring cheat-sheet, and the
[Simspace specs](https://github.com/dockersamples/simspace/tree/main/spec) for the
full `simulator.yaml` / `labspace.yaml` reference.
