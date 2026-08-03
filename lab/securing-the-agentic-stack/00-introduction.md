# Securing the Agentic Stack

Something built the application in this workspace, and it was not you.

An AI agent was handed a Node.js project - a product **catalog** with a frontend, a
backend, and a compose stack wiring in **Kafka**, **LocalStack** and **WireMock** - and
one instruction: *containerise this for production*. A minute later it had chosen a base
image, resolved several hundred packages, written a Dockerfile, and built successfully.
Nothing failed. Nothing warned.

Over the next ninety minutes you will find out what it actually shipped, and turn it
into something you can prove things about.

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

## Your journey

| Lab | Question | What the catalog gains |
|-----|----------|------------------------|
| — | What did the agent do? | A measurement |
| 1 | What is in it, and what matters? | SBOM, VEX and provenance you can read |
| 2 | Can you start from something better? | **A hardened base — the pivot** |
| 3 | How do you stop it regressing? | A verified signature and a gate that fails closed |
| 4 | What if the agent started right? | A sandbox and the DHI MCP server |

**Lab 2 is the centre of gravity.** Lab 1 teaches you to measure an image. Lab 2 is
where the measurement pays off, and every number you wrote down changes.

## Check your environment

Look at what you are working with:

```bash terminal-id=main
ls
```

That is the Product Catalog service: a REST API over a PostgreSQL product database,
with Kafka, LocalStack (S3) and WireMock wired in through :filelink[compose.yaml]{path="compose.yaml"}.
Open :filelink[package.json]{path="package.json"} to see what it depends on.

Continue to **Setup**.
