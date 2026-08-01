# Setup

Five minutes of configuration, then you never touch it again.

## 1. Your Docker organisation

Docker Scout needs to know which organisation to analyse under. Set it once and every
Scout command in this workshop uses it.

:variableDefinition[org]{prompt="What is your Docker Organization?"}

> [!NOTE]
> Every Scout command below reads `$$org$$`. If you skip this, it stays the default
> `demo-org` — fine for the simulation.

## 2. Log in

Log in to Docker Hub:

```bash terminal-id=main
docker login
```

Also log in to the hardened image registry (`dhi.io`), where the Docker Hardened
Images live:

```bash terminal-id=main
docker login dhi.io
```

Point Scout at your organisation:

```bash terminal-id=main
docker scout config organization $$org$$
```

## 3. Preflight

You will push to a Git repository in Lab 3. Confirm Git is available — it should print a
version:

```bash terminal-id=main
git --version
```

Everything else — image build attestations (`--sbom`, `--provenance`) and Docker Scout —
ships with the Docker Engine you just logged in to.

You are ready. Continue to **An Agent Built This**.
