# Conclusion

<svg viewBox="0 0 1086 52" width="100%" role="img" aria-label="Supply-chain progress: done Agent build, done SBOM · VEX · SLSA, done Hardened base, done Verify &amp; Gate, done Agentic MCP, done Build Sandbox">
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
    <rect x="733" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="817" y="30" fill="#14532d">✓ Agentic MCP</text>
    <polygon points="904,22 912,26 904,30" fill="#9aa4b2"></polygon>
    <rect x="916" y="11" width="168" height="30" rx="15" fill="#e6f4ea" stroke="#1a7f37"></rect>
    <text x="1000" y="30" fill="#14532d">✓ Build Sandbox</text>
  </g>
</svg>

## What you did to one application

| Stage | The catalog | What you could prove |
|-------|------------|---------------------|
| An agent built it | Whatever base it chose | Nothing |
| Lab 1 | + vocabulary | What is in it, and which findings matter |
| Lab 2 | Hardened base | All three questions, inherited from the base |
| Lab 3 | + build attestations, + a gate | That it stays true |
| Lab 4 | + hardened MCP server | The same, for your agent's tools |
| Lab 5 | + a sandbox and the DHI MCP server | The agent starts from trusted inputs |

Nothing about the application changed. The source is identical. What changed is how much
of it you can account for.

---

## Run the agent again

Same agent. Same prompt. One difference: this time it has rails — a hardened base pinned
in its instructions and the Lab 3 policy gate live in the pipeline. It produces something
that passes on the first attempt.

> [!IMPORTANT]
> This is the point of the entire session.
>
> You did not slow the agent down, take away its autonomy, or add a human review step
> back into the loop. You made the fast path and the safe path the same path.
>
> The agent was never the problem. The absence of verifiable evidence was.

---

## Your security framework

1. **Know what is in your images** — SBOM and VEX
2. **Verify where they came from** — SLSA provenance and signatures
3. **Start from a trusted base** — hardened images
4. **Enforce at the pipeline** — build policies that fail closed
5. **Isolate your agents** — MCP servers in hardened containers
6. **Sandbox your agents** — run them in a microVM with only signed tools reachable

---

## Do this Monday

Pick your highest-volume base image. Swap one non-critical service to the hardened
equivalent, rebuild, and compare. That single measurement will tell you more about your
exposure than a week of reading. Then store the SBOM as a build artifact, and add one
policy gate that fails closed on signature verification.

---

## One last check

```bash terminal-id=build
docker images catalog-service
```

Two images, same source. One you can prove things about.

---

## Resources

| | |
|---|---|
| Docker Hardened Images | <https://docs.docker.com/dhi/> |
| Docker Scout | <https://docs.docker.com/scout/> |
| MCP Catalog | <https://hub.docker.com/mcp> |
| SLSA framework | <https://slsa.dev> |
| OpenVEX | <https://openvex.dev> |
| Build attestations (SBOM & provenance) | <https://docs.docker.com/build/metadata/attestations/> |
| Product Catalog sample | <https://github.com/dockersamples/catalog-service-node> |
