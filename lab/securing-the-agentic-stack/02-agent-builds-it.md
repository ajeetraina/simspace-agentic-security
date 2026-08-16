# An Agent Built This

<svg viewBox="0 0 900 52" width="100%" role="img" aria-label="Supply-chain progress: current Agent build, SBOM · VEX · SLSA, Hardened base, Verify &amp; Gate, Build Sandbox">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="12" text-anchor="middle">
    <rect x="1" y="11" width="168" height="30" rx="15" fill="#2496ED" stroke="#0b3d91" stroke-width="2"></rect>
    <text x="85" y="30" fill="#ffffff" font-weight="700">Agent build</text>
    <polygon points="172,22 180,26 172,30" fill="#9aa4b2"></polygon>
    <rect x="184" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="268" y="30" fill="#5b6670">SBOM · VEX · SLSA</text>
    <polygon points="355,22 363,26 355,30" fill="#9aa4b2"></polygon>
    <rect x="367" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="451" y="30" fill="#5b6670">Hardened base</text>
    <polygon points="538,22 546,26 538,30" fill="#9aa4b2"></polygon>
    <rect x="550" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="634" y="30" fill="#5b6670">Verify &amp; Gate</text>
    <polygon points="721,22 729,26 721,30" fill="#9aa4b2"></polygon>
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#eef1f5" stroke="#9aa4b2"></rect>
    <text x="817" y="30" fill="#5b6670">Build Sandbox</text>
  </g>
</svg>

You are going to give an AI agent one instruction and watch it containerise the whole
service - with no mention of base images, versions, security, or best practice.

Here is the stack it has to reason about — a backend API fronted by a UI, talking to
PostgreSQL, Kafka, LocalStack (S3) and WireMock:

<svg viewBox="0 0 620 300" width="100%" role="img" aria-label="Architecture: the catalog-service:baseline image contains Frontend and Backend API; Backend API talks to PostgreSQL, Kafka, LocalStack S3 and WireMock.">
  <g font-family="ui-sans-serif, system-ui, sans-serif" font-size="13">
    <rect x="8" y="8" width="604" height="150" rx="10" fill="#fdf7e3" stroke="#caa93a"></rect>
    <text x="20" y="30" font-size="12" fill="#6b5b12" font-weight="700">image · catalog-service:baseline  (node:20 · ~1.1GB · 431 pkgs)</text>
    <rect x="250" y="46" width="120" height="32" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="310" y="66" text-anchor="middle" fill="#24292f">Frontend</text>
    <rect x="240" y="110" width="140" height="32" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="310" y="130" text-anchor="middle" fill="#24292f">Backend API</text>
    <line x1="310" y1="78" x2="310" y2="108" stroke="#6b7280" stroke-width="1.5"></line>
    <polygon points="306,102 310,110 314,102" fill="#6b7280"></polygon>
    <rect x="8" y="248" width="130" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="73" y="269" text-anchor="middle" fill="#24292f">PostgreSQL</text>
    <rect x="158" y="248" width="110" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="213" y="269" text-anchor="middle" fill="#24292f">Kafka</text>
    <rect x="288" y="248" width="150" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="363" y="269" text-anchor="middle" fill="#24292f">LocalStack (S3)</text>
    <rect x="458" y="248" width="150" height="34" rx="6" fill="#ffffff" stroke="#8c959f"></rect>
    <text x="533" y="269" text-anchor="middle" fill="#24292f">WireMock</text>
    <g stroke="#6b7280" stroke-width="1.5" fill="none">
      <path d="M310,142 L310,200 L73,200 L73,248"></path>
      <path d="M310,200 L213,200 L213,248"></path>
      <path d="M310,200 L363,200 L363,248"></path>
      <path d="M310,200 L533,200 L533,248"></path>
    </g>
    <g fill="#6b7280">
      <polygon points="69,242 73,250 77,242"></polygon>
      <polygon points="209,242 213,250 217,242"></polygon>
      <polygon points="359,242 363,250 367,242"></polygon>
      <polygon points="529,242 533,250 537,242"></polygon>
    </g>
  </g>
</svg>

## Ask the agent to containerise it

Run this. The agent reads the project, picks a base image on its own, writes a
Dockerfile, resolves the dependency tree, and builds:

```bash terminal-id=main
claude -p "Containerise this Node.js app (frontend, backend, LocalStack, Kafka, WireMock) for production. Add a Dockerfile and build the image as catalog-service:baseline."
```

> [!NOTE]
> **On your own laptop this pauses for approval.** `claude -p` runs headless, but Claude
> Code still asks before it writes files or runs `docker build` — you'll see permission
> prompts, not a silent run. Approve them to continue, or pre-grant so it runs unattended:
> add `--dangerously-skip-permissions` (simplest), or scope it with
> `--allowedTools "Write" "Edit" "Bash(docker build:*)" "Bash(docker images:*)"`.
> That choice — approve every step, or hand a model full write-and-shell access to your
> host — is exactly the risk **Lab 4** removes by running the agent in a sandbox. Here in
> the simulator it just runs.

It succeeded. No errors, no warnings, no questions. The terminal prints a summary of
what it built. 

<img width="909" height="429" alt="image" src="https://github.com/user-attachments/assets/9cbe04c0-9ff7-4dbd-9b71-c23476e95dfa" />


See the project it worked from and the `Dockerfile` it added:

```bash terminal-id=main
tree
```

Read what it wrote:

```bash terminal-id=main
cat Dockerfile
```

## See it actually run

A Dockerfile you can read is one thing; a service answering requests is another. Bring the
whole stack up the way the agent wired it in `compose.yaml`:

```bash terminal-id=main
docker compose up -d
```

Then hit the API it exposes:

```bash terminal-id=main
curl http://localhost:3000/api/products
```

Two products come back — the catalog is live. **This works.** No crash, no warning, nothing
that would make you stop and look. That is exactly why the three questions below matter: the
image is the artifact every later lab inspects, hardens, signs and gates — and nothing about
it *behaving correctly* tells you what it is built from.

## Freeze here. Three questions.

### What base image did it pick, and who decided that?

Nobody in your organisation chose `node:20`. The agent pattern-matched against whatever
was most common in its training data, which skews toward what was popular a year or two
ago.

### How many packages did that resolve?

```bash terminal-id=build
npm ls --all --parseable 2>/dev/null | wc -l
```

Every one is a package, with a version, with a vulnerability history. You reviewed none
of them. Neither did the agent — resolving a dependency and evaluating it are different
activities, and it only did the first.

### Can you prove where any of it came from?

No. Not the base image, not the packages, not the build itself. That is the subject of
the next eighty minutes.

## Measure it

This image is the baseline every later lab compares against.

1. Get the vulnerability overview:

    ```bash terminal-id=build
    docker scout quickview catalog-service:baseline --org $$org$$
    ```

2. Run the default policy evaluation - watch it fail:

    ```bash terminal-id=build
    docker scout policy catalog-service:baseline --org $$org$$
    ```

3. Note the size:

    ```bash terminal-id=build
    docker images catalog-service:baseline
    ```

**Write these down.** Severity counts, policy pass rate, image size. You fill in the
second row in Lab 2:

| | Critical | High | Medium | Low | Size |
|---|---|---|---|---|---|
| `catalog-service:baseline` | 0 | 8 | 41 | 93 | 1.1GB |
| `catalog-service:dhi` | | | | | |

## Checkpoint

- [ ] You watched the agent choose a base image and build the app
- [ ] You have read the Dockerfile the agent wrote
- [ ] You know how many packages the image contains
- [ ] You have recorded the baseline severity counts and size
- [ ] You have seen the default policy evaluation fail
