# An Agent Built This

<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="Progress spine: the development-to-production road. Stages DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone (a read-only runtime box). Done stages are checked green, the current stage is marked.">
<g font-family="ui-sans-serif, system-ui, sans-serif">
<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>
<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>
<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>
<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>
<rect x="8" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="67.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">DEVELOP</text>
<rect x="134" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="193.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">BASE</text>
<rect x="260" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="319.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">BUILD</text>
<rect x="386" y="40" width="118" height="44" rx="9" fill="#e2e7f5"/><text x="445.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">SIGN</text>
<rect x="536" y="32" width="70" height="60" rx="10" fill="#efe4d2" stroke="#d9a066" stroke-width="1.5"/><text x="571.0" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="#b79878">GATE</text><text x="571.0" y="76" text-anchor="middle" font-size="8.5" fill="#b79878">fail closed</text>
<rect x="628" y="40" width="126" height="44" rx="9" fill="#e2e7f5"/><text x="691.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">DEPLOY</text>
<rect x="766" y="40" width="126" height="44" rx="9" fill="#e2e7f5"/><text x="829.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#7a86a8">INVOKE</text>
<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">
<line x1="126" y1="62" x2="134" y2="62"/><polygon points="134,59 139,62 134,65"/>
<line x1="252" y1="62" x2="260" y2="62"/><polygon points="260,59 265,62 260,65"/>
<line x1="378" y1="62" x2="386" y2="62"/><polygon points="386,59 391,62 386,65"/>
<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>
<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>
</g>
<text x="10" y="90" font-size="9" font-weight="700" fill="#b91c1c">baseline: node:20 · 431 pkgs · no SBOM · root — nothing to prove</text>
</g></svg>

> **Where you are on the road:** the start line. Everything the agent produces here is the
> red box from the Introduction - the ungoverned baseline every later stage is measured
> against.

You are going to give an AI agent one instruction and watch it containerise the whole
service - with no mention of base images, versions, security, or best practice.

Here is the stack it has to reason about - a backend API fronted by a UI, talking to
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

Two products come back - the catalog is live. **This works.** No crash, no warning, nothing
that would make you stop and look. That is exactly why the three questions below matter: the
image is the artifact every later lab inspects, hardens, signs and gates - and nothing about
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
of them. Neither did the agent - resolving a dependency and evaluating it are different
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
