# Conclusion

<svg viewBox="0 0 900 104" width="100%" role="img" aria-label="Progress spine: the development-to-production road. Stages DEVELOP, BASE, BUILD, SIGN sit in the development zone (an sbx sandbox); a CI GATE is the boundary; DEPLOY and INVOKE sit in the production zone (a read-only runtime box). Done stages are checked green, the current stage is marked.">
<g font-family="ui-sans-serif, system-ui, sans-serif">
<rect x="2" y="14" width="516" height="82" rx="10" fill="#dce4ff" stroke="#2563eb" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="10" y="28" font-size="10.5" font-weight="800" fill="#1e3a8a">DEVELOPMENT</text>
<text x="120" y="28" font-size="9" fill="#3730a3">sbx microVM · host read-only</text>
<rect x="618" y="14" width="280" height="82" rx="10" fill="#e6f4ea" stroke="#1a7f37" stroke-width="1.3" stroke-dasharray="6 4"/>
<text x="626" y="28" font-size="10.5" font-weight="800" fill="#14532d">PRODUCTION</text>
<text x="720" y="28" font-size="9" fill="#14532d">read_only · cap_drop ALL</text>
<rect x="8" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="67.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">DEVELOP</text><circle cx="113" cy="52" r="9" fill="#1a7f37"/><path d="M109,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="134" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="193.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BASE</text><circle cx="239" cy="52" r="9" fill="#1a7f37"/><path d="M235,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="260" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="319.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">BUILD</text><circle cx="365" cy="52" r="9" fill="#1a7f37"/><path d="M361,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="386" y="40" width="118" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="445.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">SIGN</text><circle cx="491" cy="52" r="9" fill="#1a7f37"/><path d="M487,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="536" y="32" width="70" height="60" rx="10" fill="#fff3e0" stroke="#1a7f37" stroke-width="2.5"/><text x="571.0" y="58" text-anchor="middle" font-size="12" font-weight="800" fill="#9a3412">GATE</text><text x="571.0" y="76" text-anchor="middle" font-size="8.5" fill="#9a3412">fail closed</text><circle cx="594" cy="44" r="9" fill="#1a7f37"/><path d="M590,44 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="628" y="40" width="126" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="691.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">DEPLOY</text><circle cx="741" cy="52" r="9" fill="#1a7f37"/><path d="M737,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="766" y="40" width="126" height="44" rx="9" fill="#0b1533" stroke="#1a7f37" stroke-width="2.5"/><text x="829.0" y="67" text-anchor="middle" font-size="13" font-weight="700" fill="#ffffff">INVOKE</text><circle cx="879" cy="52" r="9" fill="#1a7f37"/><path d="M875,52 l3,3.5 l5.5,-6.5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<g stroke="#9aa6c2" stroke-width="1.6" fill="#9aa6c2">
<line x1="126" y1="62" x2="134" y2="62"/><polygon points="134,59 139,62 134,65"/>
<line x1="252" y1="62" x2="260" y2="62"/><polygon points="260,59 265,62 260,65"/>
<line x1="378" y1="62" x2="386" y2="62"/><polygon points="386,59 391,62 386,65"/>
<line x1="504" y1="62" x2="536" y2="62"/><polygon points="536,59 541,62 536,65"/>
<line x1="606" y1="62" x2="628" y2="62"/><polygon points="628,59 633,62 628,65"/>
</g>
</g></svg>

## You reached the finish line

You opened this workshop looking at a road from development to production with every stage
verifiable - and a red box where the agent actually starts. You have now walked the whole
road: measured the red box, changed where it starts, signed it and put a gate at the border,
and finally moved the fix all the way back to development. Same application, same source. The
difference is that every stage on that road is now one you can prove.

## What you did to one application

| Stage | The catalog | What you could prove |
|-------|------------|---------------------|
| An agent built it | Whatever base it chose | Nothing |
| Lab 1 | + vocabulary | What is in it, and which findings matter |
| Lab 2 | Hardened base | All three questions, inherited from the base |
| Lab 3 | + build attestations, + a gate | That it stays true |
| Lab 4 | + a sandbox and the DHI MCP server | The agent starts from trusted inputs |

Nothing about the application changed. The source is identical. What changed is how much
of it you can account for.

---

## Run the agent again

Same agent. Same prompt. One difference: this time it has rails - a hardened base pinned
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

1. **Know what is in your images** - SBOM and VEX *(the BUILD stage)*
2. **Verify where they came from** - SLSA provenance and signatures *(SIGN)*
3. **Start from a trusted base** - hardened images *(BASE)*
4. **Enforce at the border** - a pipeline gate that fails closed *(the dev-to-prod boundary)*
5. **Box the agent at both ends** - the microVM it builds in, and the `read_only` runtime it ships to. Least privilege at authoring time *and* at runtime.

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
| Docker Sandboxes | <https://docs.docker.com/ai/sandboxes/> |
| Docker Hardened Images | <https://docs.docker.com/dhi/> |
| Docker Scout | <https://docs.docker.com/scout/> |
| MCP Catalog | <https://hub.docker.com/mcp> |
| SLSA framework | <https://slsa.dev> |
| OpenVEX | <https://openvex.dev> |
| Build attestations (SBOM & provenance) | <https://docs.docker.com/build/metadata/attestations/> |
| Product Catalog sample | <https://github.com/dockersamples/catalog-service-node> |
