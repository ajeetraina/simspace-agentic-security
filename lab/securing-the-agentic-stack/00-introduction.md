# Securing the Agentic Stack

<img width="769" height="418" alt="image" src="https://github.com/user-attachments/assets/facffcfa-6c9c-4f9e-9e20-2d043825d861" />


The application in this workspace is going to be containerised by an AI agent, not by you.

It is a Node.js **catalog** service - a frontend, a backend API, and a Postgres
database, talking to **Kafka**, **LocalStack** and **WireMock**. Right now it is just
source: no Dockerfile, no image. In a moment you will hand it to an agent with one
instruction - *containerise this for production* - and in about a minute it will choose a
base image, resolve several hundred packages, write a Dockerfile, and build successfully.
Nothing will fail. Nothing will warn.

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

## What you are working with

You will be working with the Product Catalog service: a `frontend/` (React), a `src/`
backend (a REST API over a PostgreSQL product database, talking to Kafka, LocalStack (S3)
and WireMock), and the database schema in `db/`. There is no Dockerfile and no compose
file yet - the agent writes those next.

Continue to **Setup**.
