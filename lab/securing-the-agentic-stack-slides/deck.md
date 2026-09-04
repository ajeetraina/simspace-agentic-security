<!-- chrome: false -->

<img src="assets/slide-01.webp" alt="Slide 1" width="1600" height="900" loading="eager" fetchpriority="high" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Welcome, everyone. Today we're talking about **Securing the Agentic Stack** - Docker Hardened Images and supply chain security. The reason those two things share a title is that the software supply chain has changed underneath us: it's not just humans pulling and building containers anymore, it's AI agents. Over the next stretch we'll walk a road from development to production and make every segment of it provable. Let's get into it.

---

<!-- chrome: false -->

<img src="assets/slide-02.webp" alt="Meet your instructor: Ajeet Singh Raina, Developer Advocate, co-author of Operational AI with Docker" width="1600" height="900" loading="eager" fetchpriority="low" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Quick hello before we dive in - I'm **Ajeet Singh Raina**, Developer Advocate at Docker. Twenty-plus years across system integration testing, consulting, and developer relations; I'm a former Docker Captain and I run the 17,000-member Docker Bengaluru meetup. I also co-authored **Operational AI with Docker** (Packt) with Harsh Manvar, on deploying, scaling, and operating agentic AI services with Docker and Kubernetes - which is exactly the world this workshop lives in. My whole job is meeting developers where they are, so please treat this as hands-on and interrupt me with questions. Let's look at where we're headed.

---

<!-- chrome: false -->

<img src="assets/slide-03.webp" alt="Slide 3" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the shape of our time together. We open with **why supply chain security matters now**, then the **building blocks** you need in your toolkit. From there we go head to head - **standard image versus DHI** - before moving into **securing your CI pipeline**, which is the gate that everything has to pass through. Then the main event, **securing the agentic stack**, and finally we **wrap up**. Notice this list actually traces a journey from the left edge of development all the way to production, so keep that road in mind as we go.

---

<!-- chrome: false -->

<img src="assets/slide-04.webp" alt="Slide 4" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: And here's how the workshop is actually structured - four hands-on labs, all running inside a Simspace simulator so nobody has to fight local setup. **Lab 1 - Prerequisite & Setup (about 2 minutes)** is just getting into the Simspace. **Lab 2 - Secure Software Supply Chain (15-20 minutes)** covers why this matters now, how agents expand your attack surface, the building blocks - SBOM, VEX, and SLSA - and standard image versus Docker Hardened Images. **Lab 3 - Securing your CI Pipeline (45 minutes)** is the biggest block, going deep on Docker Scout build policies and CI policy enforcement, because CI is our gate. And **Lab 4 - Securing the Agentic Stack (30 minutes)** brings it home: an overview of the agentic supply chain, MCP servers running on DHI, and building your own security framework. Each lab turns one segment of that development-to-production road green. And here's where you'll actually do them.

---

<!-- chrome: false -->

<img src="assets/slide-access.webp" alt="Accessing the Workshop - https://agentic.dockerworkshop.com" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Everything today lives at one URL: **agentic.dockerworkshop.com**. That's your hands-on environment - the Simspace simulator with all four labs, open all day, nothing to install. Bookmark it now, because you'll be typing into it shortly. But before we touch a keyboard, let me show you why we're all in this room - with something that actually happened.

---

<!-- chrome: false -->

<img src="assets/slide-incident-1.webp" alt="02:47 AM, a commit lands. Author: svc-build-agent" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This actually happened. At **2:47 in the morning**, a commit lands - and the author isn't a person. It's an agent: **svc-build-agent**.

---

<!-- chrome: false -->

<img src="assets/slide-incident-2.webp" alt="02:47 AM commit - Change: bumped a base image, regenerated the Dockerfile" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: What did it change? It **bumped a base image and regenerated the Dockerfile** - real changes to how the app actually gets built.

---

<!-- chrome: false -->

<img src="assets/slide-incident-3.webp" alt="02:47 AM commit - Reviewer: approved by CI, all checks green" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Who reviewed it? **CI did** - all checks green. That is the only review this change ever got.

---

<!-- chrome: false -->

<img src="assets/slide-incident-4.webp" alt="02:47 AM commit - Deployed: production, 03:12 AM" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: And it shipped - straight to **production, 3:12 AM.** Twenty-five minutes from an agent's commit to running in prod.

---

<!-- chrome: false -->

<img src="assets/slide-incident-5.webp" alt="02:47 AM commit - Reviewed by a human? No" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: And here's the row that matters. **Reviewed by a human? No.** Nobody was awake, nobody signed off - and it's running in prod right now.

---

<!-- chrome: false -->

<img src="assets/slide-incident.webp" alt="02:47 AM commit, full recap - reviewed by a human: No. Who approved that build?" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: So sit with the question: **who approved that build?** Everything we're about to do is really about being able to answer it - provably. Now let's ground ourselves in why this is suddenly so much harder.

---

<!-- chrome: false -->

<img src="assets/slide-05.webp" alt="Slide 5" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: So - **why does supply chain security matter?** We've been saying it for years, and it's always been true. But the subtitle is the part that's new: **especially when agents are doing the pulling.** For a long time the mental model was that a human made a deliberate choice about every dependency and every base image that entered the build. That assumption is quietly breaking. Once an agent is doing the pulling, the discipline you relied on - a person choosing, reviewing, deciding - isn't automatically there anymore. Let me show you exactly what changes.

---

<!-- chrome: false -->

<img src="assets/slide-06.webp" alt="Slide 6" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Put the two workflows side by side. On the left, the **traditional workflow**: a developer pulls the base image manually, with intent; installs dependencies that get reviewed in a PR; and CI runs against human-authored config. Every one of those steps has a person in the loop who chose it. On the right, the **agentic workflow**, and notice everything turns into a warning triangle - the agent pulls the base image autonomously, installs packages with no human review, invokes external tools with real credentials, and modifies the Dockerfile mid-pipeline. Same steps, but the judgment and the review are gone, and now there are live credentials in the mix. The line at the bottom is the one to remember: **"the better the agent, the bigger the blast radius."** A more capable agent does more, touches more, and can therefore break more. Let's visualize where all those agents actually sit.

---

<!-- chrome: false -->

<img src="assets/slide-06b.webp" alt="The Traditional Workflow: inner and outer development loops with a human developer at every stage" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the world we grew up in - **the traditional workflow**. A human writes, reviews, and ships at every stage, and the key line is at the top: **the attack surface is only what you choose to pull.** You've got the **inner loop** on the left - code, open source, build, test - the fast cycle on your own machine, and every icon around it is a person. Then you **push**, and it flows into the **outer loop** on the right - integrate, test, deploy - again, humans at every point. It's a chain of deliberate human decisions from left to right. Hold this picture in your head, because the next slide keeps the exact same map and swaps out just one thing.

---

<!-- chrome: false -->

<img src="assets/slide-07.webp" alt="The Agentic Workflow: the same inner and outer loops with an AI agent at every stage" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Same map, same inner and outer loops, same push in the middle - but look what changed: **every human icon is now an AI agent.** That's the whole point. In **the agentic workflow**, an agent sits at every single stage - code, open source, build, test, integrate, deploy - and so the attack surface is **no longer just what you pull.** It's every autonomous action, every tool call, every credential those agents touch across the entire road from inner loop to production. That's a lot of green robots and a lot of blast radius - the same failure mode as that 2:47 AM commit, now at every stage. Let me make it concrete - here's an agent turned loose on a build with no guardrails at all.

---

<!-- chrome: false -->

<img src="assets/slide-09.webp" alt="The ungoverned agent: agent running straight on your host with no boundary, FROM node:20 chosen with no guidance, 6 high CVEs" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is our ungoverned baseline - the **ungoverned agent** running straight on your host, and it's exactly how a lot of teams are running today. Look at the container: the agent is sitting right on **your host**, with the host daemon, host credentials, and no boundary at all. We hand it a simple **prompt** - "containerize this app" - and because it has **full permissions** and can reach **open registries with no allowlist**, it just grabs whatever it wants. What it picks is `FROM node:20`, chosen with **no guidance**. And the result, down at the bottom, is the number we're going to keep coming back to: **0 critical, 6 high, 30 medium, 54 low CVEs** - built from **431 packages**, with **no SBOM, no attestation, running as root**. That is our start line. And the app it mangled isn't a toy - let me show you the real service we're going to secure.

---

<!-- chrome: false -->

<img src="assets/slide-08.webp" alt="Slide 8" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: So this is the app we'll be securing all the way down that dev-to-prod road. It's a **Product Catalog** service, and it's deliberately realistic rather than a toy. In the middle you've got the **catalog-service** application, and it's not living alone: it writes product data to **PostgreSQL**, pushes product images to **AWS S3**, and publishes product updates through **Kafka**. Reaching outside its own boundary, it talks to an **Inventory service** and other downstream services. The point I want you to take away is that this is a real supply chain of moving parts - every one of those boxes is something we eventually have to trust and prove. Before we talk about how to fix any of it, I want you to feel it yourself - so let's try.

---

<!-- chrome: false -->

<img src="assets/slide-lets-try.webp" alt="Let's try - Agent containerising the Product Catalog application" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Your turn. Head into the workshop - **agentic.dockerworkshop.com** - and run the first hands-on: **let an agent containerize the Product Catalog application.** Give it the same simple prompt, with no guardrails, and watch what it does. It'll reach for `node:20` and hand you back the same ungoverned baseline you just saw - hundreds of packages, high CVEs, no SBOM, running as root. Take a few minutes, break it yourself, and once you've seen it happen on your own screen, come back - and we'll talk about how to govern it.

---

<!-- chrome: false -->

<img src="assets/slide-framework.webp" alt="Every agent-driven change answers four questions: Evidence (what is in it, where from), Baseline (did it start trustworthy), Gate (is it allowed to pass), Boundary (what could it reach)" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: No matter how the agent produced a change, governing it comes down to **four questions** - and these are the four layers of the road we're about to walk. **Evidence:** what is in this artifact, and where did it come from - SBOM, VEX, SLSA provenance. **Baseline:** did it start from something trustworthy - a Docker Hardened Image. **Gate:** is it allowed to pass - build policies, signing, admission. **Boundary:** what could it reach while it worked - the sandbox runtime. Evidence and baseline make governance possible; gate and boundary make it real. We'll take one question per lab, and I'll bring the matching card back each time. Next, the road itself.

---

<!-- chrome: false -->

<img src="assets/slide-journey-0.webp" alt="The journey, checkpoint 0 of 4: the whole development-to-production road, everything still to prove, red baseline hot" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the whole road we travel today - and it flows **left to right, development to production**.

- **Left = DEVELOPMENT:** the agent works inside an `sbx` microVM, host read-only.
- **Right = PRODUCTION:** the runtime is locked down - read-only, cap-drop ALL, non-root.
- **The CI GATE in the middle is the dev-to-prod boundary. It fails closed** - nothing crosses into production unless it's provable.

Code moves along the road: developed, based on a trusted image, built with attestations, signed - then it has to pass the gate before it's deployed and invoked.

Right now none of it is provable. The ungoverned baseline we just watched the agent ship is `FROM node:20`, 431 packages, no SBOM, running as root: **0 of 4 stages green**. Each of the four labs turns one segment of this road green, and we come back to this same picture at each checkpoint. This is checkpoint 0 of 4 - the start line.

---

<!-- chrome: false -->

<img src="assets/slide-framework-1.webp" alt="Question 1 of 4 - Evidence: what is in this, and where did it come from? SBOM, VEX, SLSA provenance" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Lab 1 is about the first question - **Evidence:** what is actually in the image, and where did it come from? The answer is **SBOM, VEX, and SLSA provenance** - the audit trail that finally lets you answer "who approved that build?" For the next stretch we're going to generate that evidence and learn to read it. Let's start with the threat model it all hangs on.

---

<!-- chrome: false -->

<img src="assets/slide-16.webp" alt="Slide 16" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the mental model I want you to carry through the whole lab - it's adapted from the SLSA threat overview. A **Producer** flows left to right through three stages: **Source**, your code; **Build**, where the Dockerfile turns it into an image; and **Package**, the container image that ships. Feeding into the build are **Dependencies** - other people's code that we have to check. And notice where the **vulnerability scan** sits - that question mark right after the build, before the package goes out the door. Every one of these arrows is a place something can go wrong, and every one is a place we can add proof instead. Let's actually mark up all the ways this chain gets attacked.

---

<!-- chrome: false -->

<img src="assets/slide-17.webp" alt="Slide 17" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Now here's the same chain with every threat called out, all the way through to the **Consumer** on the right. At the source: **who** wrote it, and was it **compromised**? Between stages: was it **manipulated**, **tampered** with, **altered**? At the package: is it **compromised** or just **old**? And on dependencies, the one that bites hardest in the AI age - is it **genuine**? That's slopsquatting again; a hallucinated or typosquatted package that looks real. Count them - that's eight distinct question marks between a producer and a consumer, and today we can answer almost none of them. The whole rest of this lab is about turning each of these question marks into something we can prove. And the tools that answer them have names.

---

<!-- chrome: false -->

<img src="assets/slide-18.webp" alt="Slide 18" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: So here are the three questions that turn those question marks into answers, and each one maps to a piece of the chain. **What's in this software artifact?** That's the **SBOM** - a software bill of materials, an attestation describing the contents of the artifact. **Where has it come from?** That's **provenance** - an attestation about the history of an artifact: where it came from, who produced it, and how. And **can I verify the attestation source?** That's a **signed** attestation - a digital signature that verifies the source and lets you actually assess trustworthiness. Notice the through-line: everything here is an **attestation**, a signed statement of fact you can check later. This is the language of proof we've been building toward. Let's name the three building blocks and get to work.

---

<!-- chrome: false -->

<img src="assets/slide-19.webp" alt="Slide 19" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is our section marker for Lab 1 - the three building blocks: **SBOM, VEX, and SLSA**. SBOM tells you what's inside, VEX tells you which of those CVEs are actually exploitable in your context so you're not chasing noise, and SLSA gives you the provenance levels that prove how it was built. And the subtitle is the whole reason we're here: this matters **especially when agents are doing the pulling**, because the agent won't ask permission before grabbing a base image. So let's open the lab, inspect that `node:20` baseline with Docker Scout, and start generating the attestations that let us prove exactly what's in the image.

---

<!-- chrome: false -->

<img src="assets/slide-20.webp" alt="Slide 20" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: These are the three building blocks we'll lean on for the rest of this lab, so let's put names to them up front. **SBOM** is the software bill of materials - the full ingredient list of what's actually inside the image. **VEX** is the exploitability layer on top of that - which of the CVEs we find actually matter for this product. And **SLSA** is the provenance story - proof of how and where the artifact was built. Keep this left-to-right order in your head: SBOM tells you what's in the box, VEX tells you what to worry about, and SLSA tells you to trust where the box came from. We'll walk through each one in turn.

---

<!-- chrome: false -->

<img src="assets/slide-22.webp" alt="Slide 22" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Let's start with the **SBOM** - your software ingredient list. The SBOM is simply the complete list of every package inside the image, and image analysis uses it to understand exactly what packages and versions are present. Here's the key detail on the right: Docker Scout matches those packages, expressed as **PURLs**, against an advisory database aggregated from 23 sources. Notice it's PURL-based matching, not CPE - that's what keeps false positives down. And when it scores severity, it prioritizes the vendor advisory first, falls back to NIST, and prefers CVSS v4 over v3. One thing worth calling out: Scout will use an SBOM attestation if the image already has one, but if it doesn't, Scout just indexes the image contents and builds one on the fly. Next let's see how you actually generate and query these.

---

<!-- chrome: false -->

<img src="assets/slide-23.webp" alt="Slide 23" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's how you produce and read an SBOM in practice. At build time you attach it as an attestation with `docker buildx build --attest --type=sbom .` - that embeds the bill of materials right alongside the image. By default BuildKit uses the Syft-based scanner to generate it, but you can swap in a different generator plugin if your ecosystem needs one. Once it's there, you query it with Docker Scout: `docker scout sbom myorg/myapp:v1.0` to inspect, or add `--output` to write it to a file. The takeaway is that generating an SBOM is a single flag on your existing build - there's no separate pipeline to stand up. With the ingredient list in hand, the next question is which of those ingredients are actually dangerous, and that's where VEX comes in.

---

<!-- chrome: false -->

<img src="assets/slide-24.webp" alt="Slide 24" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Now for **VEX** - Vulnerability Exploitability eXchange - which is how we cut through CVE noise. VEX is a form of security advisory that states whether a product is actually affected by a known vulnerability. Instead of just dumping every CVE found in the image, VEX statements clarify whether each one is genuinely exploitable in this specific configuration, and why. Follow the diagram on the right: you match the SBOM against the CVE feeds and land at **200 findings** - that's the raw, scary number. Then you apply VEX, which drops the non-affected findings, and you're left with **20 to act on**. That's a ten-to-one reduction in what your team actually has to triage. This is the difference between drowning in alerts and making a risk-based decision. Let's make that contrast concrete.

---

<!-- chrome: false -->

<img src="assets/slide-25.webp" alt="Slide 25" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the side-by-side that really lands the value. On the left, **without VEX**, a standard scan lists every CVE against every package - look at libc6 showing up repeatedly with entries marked "won't fix." It tells you what's present, but nothing about whether any of it is actually exploitable, so a human has to chase every line. On the right, **with VEX**, each CVE comes with a statement: Not Affected, Affected, Fixed, or Under investigation. You pull it with a single command - `docker scout vex get dhi.io/python:3.13 --output vex.json`. And the punchline at the bottom is the whole point: **190 not affected, 10 fixed**. That's the noise gone and the signal left. Now that we know what's in the image and what's exploitable, the last question is whether we can trust how it was built - that's SLSA.

---

<!-- chrome: false -->

<img src="assets/slide-26.webp" alt="Slide 26" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: **SLSA** - Supply chain Levels for Software Artifacts - is our build provenance framework. It's a security framework for improving the integrity of software supply chains, and it defines four progressive levels from 0 to 3, each adding more rigorous controls around build provenance, source integrity, and the build environment. Walk the ladder on the right: L0 is no guarantees, L1 means provenance merely exists, L2 gets you a hosted build with signed provenance - GitHub Actions with OIDC achieves this - and L3 is the hardened, non-falsifiable target that DHI aims for. The one question SLSA makes answerable is right there in bold: can you prove this artifact came from that source and wasn't tampered with in transit? DHI gives you the signed provenance envelope, hermetic reproducible builds, and verification with Cosign or Notation. Let's see how you actually verify that provenance.

---

<!-- chrome: false -->

<img src="assets/slide-27.webp" alt="Slide 27" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: And verifying SLSA provenance is a single command. On the right you run `docker scout attest get` against your hardened image, pass `--predicate-type https://slsa.dev/provenance/v0.2`, and add `--verify`. That fetches the SLSA attestation and checks its authenticity in one step - so the "can you prove where this came from" question we posed on the last slide gets answered right at the terminal. The important thing for the audience is that consuming provenance doesn't require standing up any new infrastructure; if the image was built to L3, verifying it is a one-liner. Next we'll look at the compliance attestations that build on the same mechanism, starting with FIPS 140.

---

<!-- chrome: false -->

<img src="assets/slide-28.webp" alt="Slide 28" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: **FIPS 140** is the Federal Information Processing Standard for validated cryptography, and it mandates that crypto modules meet NIST-validated standards - required for US government contracts, healthcare under HIPAA, finance, and defense workloads. The nice part is how little this changes your workflow: DHI ships a `-fips` tag variant per image backed by the OpenSSL FIPS Provider, which is CMVP validated, plus a signed, machine-readable FIPS attestation for auditors. On the right you see it in action - you pull `dhi.io/node:24-debian13-fips`, then run `docker scout attest get` with the FIPS predicate type and `--verify`. The output gives auditors exactly what they need: standard FIPS 140-3, certification CMVP #4985, status active. So compliance evidence becomes something you query, not a binder you assemble by hand. One more compliance attestation to cover - STIG.

---

<!-- chrome: false -->

<img src="assets/slide-29.webp" alt="Slide 29" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Last one: **STIG** - the Security Technical Implementation Guide, DISA's DoD hardening standard. There's an interesting wrinkle here: DISA hasn't yet published a container-specific STIG, so Docker builds custom profiles based on the GPOS SRG and the DoD Container Hardening Process Guide. DHI ships signed STIG scan attestations, which cuts down the false positives that plague normal container STIG scans - and the STIG variant does require a Docker subscription. The command pattern is exactly what you've seen: `docker scout attest get` with the STIG predicate and `--verify`, or `attest list` to see everything on an image. And that list is the payoff for this whole section - on one image you'll now see SBOM, OpenVEX, SLSA, FIPS, STIG, Scout health, and secrets scan, all signed. That's checkpoint one: the BUILD stage turns green, because for the first time we can actually see and trust what's inside the image. Let's mark that on the road.

---

<!-- chrome: false -->

<img src="assets/slide-journey-1.webp" alt="The journey, checkpoint 1 of 4: Lab 1 done, the BUILD stage is now green - you can see what is in the image" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Checkpoint one - Lab 1 is done, so **BUILD** is green on the road. We can now see what's inside the image: Buildx attached an **SBOM plus provenance at build time**, so the box is no longer a black hole. Notice the progress bar - **1 of 4 stages provable** - and that ungoverned baseline strip underneath is the reminder of where we started: `FROM node:20`, 431 packages, no SBOM, running as root, nothing you can prove. Same discipline shows up at both ends of this road: the agent that builds runs in a box, and the service it becomes runs in a box. Next we tackle the segment just to the left of BUILD - the base image itself.

---

<!-- chrome: false -->

<img src="assets/slide-framework-2.webp" alt="Question 2 of 4 - Baseline: did it start from something trustworthy? Docker Hardened Images" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: That segment is the second question - **Baseline:** did the image start from something trustworthy? The answer is a **Docker Hardened Image** instead of whatever the agent grabbed off the internet. Evidence told us what's in the box; baseline makes sure we began from a good one. Here's what that looks like in practice.

---

<!-- chrome: false -->

<img src="assets/slide-30.webp" alt="Slide 30" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This kicks off Lab 2: **Standard Image versus Docker Hardened Images**. Everything upstream in your supply chain rides on the base image you pick, so this is the highest-leverage decision you make. The promise on the subtitle is the one I want you to hold onto - you'll **watch the CVE count change with a single `FROM` line swap**. No refactor, no re-architecture, just a better starting point. Let me show you what actually makes a hardened image hardened.

---

<!-- chrome: false -->

<img src="assets/slide-31.webp" alt="Slide 31" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Three properties define a Docker Hardened Image. **Minimal**: built from source with only the packages your runtime actually needs - no shell, no curl, no extras, which is where that **95% smaller** number comes from and also why the attack surface shrinks. **Attested**: every image ships with an **SBOM, a VEX document, SLSA L3 provenance, and a digital signature** - so you can verify what's inside in one command rather than trusting a label. **Patched**: continuously updated, so you get **near-zero CVEs on day one** and the Docker team keeps it that way as new vulnerabilities land. Minimal shrinks the surface, attested makes it provable, patched keeps it clean - and none of that is theoretical, so let's put real numbers on it.

---

<!-- chrome: false -->

<img src="assets/slide-32.webp" alt="Slide 32" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the same `docker scout compare` you'd run yourself, side by side. On the left, the Docker Official `node:22-slim`: **2 Critical, 26 High, 25 Medium, 122 Low**, 806 packages, 398 MB. On the right, `dhi.io/node:24-debian13`: **0, 0, 0, 0** - every severity bucket zeroed out. And it's not just the CVEs: packages drop from 806 to **211**, that's 595 fewer things to patch and audit, and size falls from 398 MB to **40 MB**, a 90% cut. Fewer packages is *why* there are fewer CVEs - you can't have a vulnerability in software you never shipped. That entire column of zeros is what a one-line base swap buys you, so let's look at exactly what that swap is in a real Dockerfile.

---

<!-- chrome: false -->

<img src="assets/slide-33.webp" alt="Slide 33" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the actual migration for `catalog-service-node`, before on the left and after on the right. The change that matters is the **`FROM` line**: `node:22-slim` becomes a two-stage build - `dhi.io/node:24-debian13-dev` for the build stage where you run `npm ci`, and the distroless `dhi.io/node:24-debian13` for the final stage, copying `node_modules` across with `--from=base`. Notice what *drops out* on the right: no more `RUN useradd` and `USER appuser`, because DHI already runs as non-root for you. As the callout says, the runtime stage is **distroless - no shell, no npm** - your build tooling lives only in the dev stage, the **source is unchanged, and the Compose file doesn't change at all**. This is a base swap, not a rewrite. Now let's zoom out from one service to the whole stack.

---

<!-- chrome: false -->

<img src="assets/slide-11.webp" alt="Catalog service, where vulnerabilities enter: without the DHI MCP the agent picks base images freely (2 Critical, 46+ High CVEs); with the DHI MCP every service resolves to a hardened image (0 Critical, 0 High)" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the whole Product Catalog stack, and it's where vulnerabilities actually enter. On the left - **without the DHI MCP, the agent picks base images freely**: the application on `node:20` brings 2 Critical and 26 High, PostgreSQL adds 8 High-plus, Kafka on `confluentinc/cp-kafka:7.6` piles on 12 High-plus, aws-sdk drags in more, and the **total stack exposure is 2 Critical and 46-plus High CVEs**. On the right - **with the DHI MCP, the agent queries first** and every service resolves to a hardened image: `dhi.io/node`, `dhi.io/postgresql`, `dhi.io/kafka`. Watch the right column collapse to **0 across the board - total stack exposure 0 Critical, 0 High**. The point isn't just that DHI is cleaner; it's that when the agent has to *ask* before it picks, the vulnerabilities never enter the stack in the first place. That prevention-at-the-source is the whole idea, and it closes out Lab 2 - let's mark it on the journey map.

---

<!-- chrome: false -->

<img src="assets/slide-journey-2.webp" alt="The journey, checkpoint 2 of 4: Lab 2 done, BASE is now green - hardened base, the CVEs collapse" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Checkpoint two - **Lab 2 is done, BASE turns green**. The hardened image now feeds the build: **DHI, 0 CVEs, SLSA L3**, and you can see the CVEs collapse right where we started this segment. The progress bar reads **2 of 4 stages provable**, Lab 1 and Lab 2 both lit. Two segments of the road are green; the base and the build are both trustworthy now. Next we push toward the CI gate that turns all of this into an enforced boundary.

---

<!-- chrome: false -->

<img src="assets/slide-framework-3.webp" alt="Question 3 of 4 - Gate: is it allowed to pass? Build policies, image signing, admission" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: That boundary is the third question - **Gate:** is this artifact allowed to pass? The answer is **build policies, image signing, and admission** - the check in the middle of the pipeline that fails closed, so nothing crosses into production unless it's provable. Evidence and baseline made governance possible; this is where we make it real.

---

<!-- chrome: false -->

<img src="assets/slide-35.webp" alt="Slide 35" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is **Part 3 of 4**: Securing Your CI Pipeline. We've come a long way on the dev-to-prod road. The agent already builds on a hardened base with zero CVEs, and we've got an SBOM, provenance, and SLSA attestations attached. But building a good image and *proving* it's good are two different things, and nothing yet stops a bad image from reaching production. This part is where we make the boundary real: **build policies**, **image signing**, and a **GitHub Actions** gate that fails closed. The theme for the next few slides is simple - verify it, then gate it. Let's start with the policies that decide whether an image is even allowed to leave the pipeline.

---

<!-- chrome: false -->

<img src="assets/slide-36.webp" alt="Slide 36" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is **security as code**. Instead of a human eyeballing a scan report, you define rules that **automatically fail the build** before anything insecure reaches your registry or production. One command does it: `docker scout policy catalog-service:dhi --exit-code`. That exit code is the whole point - a non-zero exit stops the pipeline dead. The policies we're enforcing today are on the left: **no fixable critical or high CVEs**, **supply chain attestations present**, **no unapproved base images**, and a **default non-root user**. And you're not limited to the defaults - the optional `policy-config.json` on the right lets you tune thresholds, for instance scoping fixable-vulnerabilities to just CRITICAL and HIGH, or disabling a policy you don't want yet. When all seven pass, the image earns its way to the registry. Next, let's see the full menu of policies Scout gives you out of the box.

---

<!-- chrome: false -->

<img src="assets/slide-37.webp" alt="Slide 37" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Passing a policy tells you an image is clean; **signing** tells you it's *authentic* - that this exact digest is the one your pipeline produced and nobody swapped it. We use **Cosign** with keyless signing, and the flow is four steps: build with attestations, sign with Cosign via **OIDC**, the signature lands in the **Sigstore transparency log**, and you verify at deploy time in a CI gate or admission controller. The magic word is keyless - `cosign sign` mints a short-lived certificate from your OIDC identity, so there's **no private key to manage, rotate, or leak**. Verification pins both the identity and the issuer with `--certificate-identity-regexp` and `--certificate-oidc-issuer`, and `docker scout attest list` and `attest get --verify` let you inspect and check the attestations bound to that image. This works with Docker Hub, ECR, ACR, GHCR - any OCI registry. Now let's assemble policy plus signing into one CI pipeline.

---

<!-- chrome: false -->

<img src="assets/slide-38.webp" alt="Slide 38" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the whole secure CI pipeline in four steps, running on **GitHub Actions**. Step one, **checkout** with `actions/checkout@v4`. Step two, **build and attest** - `docker build --sbom=true --provenance=mode=max -t $IMAGE`, so the SBOM and provenance are generated at build time and bound to the digest. Step three is the **key step**, the **policy gate**: `command: policy` with `exit-on: policy`. That's the dev-to-prod boundary in one line - if any policy fails, the step exits non-zero and, critically, **push never runs**. Only when the gate passes do we reach step four, **push** - `docker push "$IMAGE"` - with attestations bound to the digest that ships. The gate sits *before* the push on purpose: an unprovable image simply cannot be promoted. Let's look more closely at exactly which policies that gate evaluates.

---

<!-- chrome: false -->

<img src="assets/slide-39.webp" alt="Slide 39" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: These are the **7 built-in Scout policies**, and the headline is **zero config required** - one command, `docker scout policy IMAGE --exit-code`, evaluates all of them. On the vulnerability side: **no fixable critical or high CVEs**, and **no high-profile vulnerabilities** - think Log4Shell, the XZ backdoor, anything in the CISA KEV catalog. On hygiene: **no copyleft licenses** like AGPL or GPL, **no outdated base images**, and **no unapproved base images** that must match an allowlist. And the two that tie back to our supply chain work: **supply chain attestations** - SBOM plus SLSA provenance must be present - and **default non-root user**. Everything is **configurable via JSON**, you can write **custom policies in Rego** with OPA, and it all **runs fully local** - no Scout service call needed, which matters for air-gapped or privacy-sensitive pipelines. Next, the complete workflow file you can copy straight into your repo.

---

<!-- chrome: false -->

<img src="assets/slide-40.webp" alt="Slide 40" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the **complete `secure-build.yaml` workflow, ready to copy**. It triggers `on: [push]`, sets `IMAGE` to your image tagged with the commit SHA, and runs five steps. Checkout, then **login** to Docker Hub with `docker/login-action` using `DOCKER_USER` and `DOCKER_PAT` secrets. Step three **builds on the DHI base and attaches SBOM and provenance** - `docker build --sbom=true --provenance=mode=max`. Step four is the **policy gate** via `docker/scout-action@v1` with `command: policy` and `exit-on: policy` - the comment says it plainly, before push, and if it fails the push never runs. Step five **pushes only if the gate passes**. The point I want to land: this is not pseudocode - it's a real file living at `.gitea/workflows/secure-build.yaml` in the repo, so you can lift it today and adapt the secret names. Now let's contrast what this gate actually does with a hardened base versus an ordinary one.

---

<!-- chrome: false -->

<img src="assets/slide-41.webp" alt="Slide 41" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's why all the earlier hardening pays off at the gate. **With a DHI base** on the left: no critical or high CVEs, SBOM and provenance present, non-root by default, up-to-date base - the **gate passes and the image is pushed**. **With a standard base** on the right: CVEs found, no SBOM, running as root - the **gate fails, and push never runs**. Same pipeline, same policies, opposite outcomes - the only variable is the base image the agent built on. This is the concrete cash-out of Labs 1 and 2: the hardened base isn't just nice-to-have hygiene, it's what lets you cleanly clear a fail-closed gate instead of getting blocked at the boundary. That's Lab 3 done - let's mark it on the journey map.

---

<!-- chrome: false -->

<img src="assets/slide-journey-3.webp" alt="The journey, checkpoint 3 of 4: Lab 3 done, SIGN, GATE and DEPLOY are now green - signed, gated, promoted to production" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: **Checkpoint 3 - Lab 3 is done.** Trace the road: the agent develops in a sandbox, builds on a hardened DHI base with zero CVEs, attaches SBOM and provenance at build, and now **SIGNs keylessly, bound to the digest**. The **CI GATE** - no critical CVEs, SBOM present, provenance verified - **fails closed** at the dev-to-prod boundary, and because our image is provable it passes and gets promoted: **DEPLOY** goes green with a signed image, verified and pinned by digest. **Three of four stages provable now** - Labs 1, 2, and 3 are lit. Compare that to the ungoverned baseline the agent shipped on your host: `FROM node:20`, 431 packages, no SBOM, root, nothing you can prove. The one box still grey is **INVOKE** - the running Agent/MCP client at the far right. Same discipline at both ends: the agent that *builds* runs in a box, and the service it *becomes* must run in a box too. That runtime end - MCP servers and tool isolation - is Lab 4, and it's next.

---

<!-- chrome: false -->

<img src="assets/slide-framework-4.webp" alt="Question 4 of 4 - Boundary: what could it reach while it worked? Sandbox runtime - network, filesystem, credentials" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Lab 4 is the last question - **Boundary:** what could the agent reach while it worked? The answer is the **sandbox runtime** - network, filesystem, and credentials, bounded so the agent can act without an open blast radius. This is the fourth layer, and it closes the loop: same discipline at both ends of the road.

---

<!-- chrome: false -->

<img src="assets/slide-43.webp" alt="Slide 43" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is our last segment, **Part 4 of 4: Securing the Agentic Stack**. We've walked the road from development to production, we've made CI fail closed, and now we close the loop on the piece that changes everything about that road - the agent itself. MCP servers, tool isolation, trusted foundations: that's what the next few slides are about. Because once an agent can build and ship for you, the tools it reaches for become part of your supply chain.

---

<!-- chrome: false -->

<img src="assets/slide-10.webp" alt="Agent with a Sandbox: sbx microVM boundary, DHI MCP server, hardened base, zero CVEs" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is where we're headed - the clean end-state, the counterpart to the ungoverned-agent baseline from earlier. Everything the agent does now happens inside a **sandbox boundary, an `sbx` microVM** with its own daemon, its own network, and the host mounted read-only. Same prompt as before - "containerize app" - but watch the flow: the agent has full permissions inside the box, it queries the **DHI MCP server** which only serves signed tools, and it writes `FROM dhi.io/node` because it checked the trusted source before writing the line. The result at the bottom is the whole point: **0 critical, 0 high, 0 medium, 0 low CVEs**, 211 packages, SBOM attached, signed, non-root. Contrast that with the ungoverned `FROM node:20` baseline we started with - same agent, radically different outcome. Let me show you how that sandbox actually works.

---

<!-- chrome: false -->

<img src="assets/slide-sandboxes.webp" alt="Sandboxes (experimental): run agents in isolation rather than on your bare machine - the agent runs in an isolated sandbox mirroring your workspace, you define its access, and your real files, data and secrets stay safe even if it goes off the rails" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the boundary itself - **Docker Sandboxes**, still experimental but exactly the primitive we want. Instead of letting an agent or Claude run loose on your bare machine, it runs in an **isolated sandbox that mirrors your workspace**. You define what access it gets - filesystem, network, internal resources, and tools - and your real files, data, and secrets **stay safe even if the agent goes off the rails**. On the right you can see it: `sbx run claude` starts the agent in a sandbox, mounts just the workspace, and applies a **deny-all network policy with an explicit allowlist**. Let me show you what's actually inside that box.

---

<!-- chrome: false -->

<img src="assets/slide-sandbox-arch.webp" alt="Sandbox architecture: on the host machine, the agent container runs inside a microVM-based sandbox fed by workspace directories, network policies and secrets; outbound traffic flows through a network proxy to external systems" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the architecture. Everything sits on your **host machine**, but the agent runs inside a **microVM-based sandbox** - a real isolation boundary, not just a container namespace. You feed it three things from outside the box: the **workspace directories** it's allowed to see, the **network policies** that govern what it can reach, and the **secrets** it needs. Outbound traffic doesn't go straight out - it flows through a **network proxy** that enforces those policies before anything reaches **external systems**. The agent gets exactly the access you granted and nothing more. That's the runtime boundary for Lab 4 - here's what it looks like in day-to-day use.

---

<!-- chrome: false -->

<img src="assets/slide-sandbox-tui.webp" alt="The Sandbox TUI: Docker Sandboxes live view - sandboxes on the left (claude-docs running, claude-agent-demo stopped) and the per-sandbox network log on the right with allowed and blocked hosts" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the Sandbox TUI - `sbx` gives you a live view of every sandbox on your machine. On the left, each sandbox with its status, workspace, and resource use - `claude-docs` running, `claude-agent-demo` stopped - with controls to stop, exec, or remove. On the right, the **network log** for the selected sandbox: every outbound connection the agent attempted, with a hit count and an allowed-or-blocked status. Notice `api.anthropic.com`, `api.github.com`, and `registry.npmjs.org` allowed, while `http-intake.logs.us5.datadoghq.com` is **blocked**. This is the boundary made observable - you can see exactly what the agent reached for and what the policy stopped.

---

<!-- chrome: false -->

<img src="assets/slide-credentials.webp" alt="Managing credentials: always prefer stored secrets over env vars (keychain encrypts at rest), never set API keys inside the sandbox; sbx secret set/ls/rm; supported services anthropic, openai, github, google and more" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Credentials are the thing you least want an agent to leak, so two rules. **Always prefer stored secrets over environment variables** - the OS keychain encrypts them at rest. And **never set API keys manually inside the sandbox** - anything in there is readable by the agent. The CLI is small: `sbx secret set -g anthropic` stores a key for all sandboxes; scope it to one with `sbx secret set my-sandbox openai`. You can pipe a GitHub token straight in - `gh auth token | sbx secret set -g github` - so the agent can use the `gh` CLI without ever seeing the raw value. `sbx secret ls` and `rm` manage them, and the major providers are supported out of the box.

---

<!-- chrome: false -->

<img src="assets/slide-protecting-mcp.webp" alt="Protecting MCP: tools are how agents act on the world - govern which servers exist and which tools an agent may actually call, at one gateway" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: That's the sandbox itself - the boundary the agent runs in. Now the other half of Lab 4: **protecting MCP**. Tools are how an agent acts on the world, so the question shifts from "what can it reach" to "which servers exist, and which tools is it actually allowed to call?" The answer is to govern all of that at **one gateway**.

---

<!-- chrome: false -->

<img src="assets/slide-mcp-gateway.webp" alt="The agent talks to one gateway, never to servers directly: the sandboxed agent reaches an mcp-gateway via SBX_MCP_URL, and local-wiki, GitHub/Notion and DuckDuckGo are aggregated behind it; every tool call flows through one chokepoint" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the shape of it. The agent inside the sandbox never talks to MCP servers directly - it talks to **one endpoint**, the **mcp-gateway**, through a single `SBX_MCP_URL`. Behind that gateway all your servers - local-wiki, GitHub, Notion, DuckDuckGo - are aggregated. The payoff is the line at the bottom: **every tool call flows through one chokepoint**. Tools are namespaced `mcp__mcp-gateway__<tool>`, and that single point is where policy and audit apply - one place to govern instead of N servers to chase.

---

<!-- chrome: false -->

<img src="assets/slide-gateway-options.webp" alt="Point it at a real gateway: local gateway http://localhost:8811 (Compose or Desktop MCP Toolkit) or hosted control plane https://gateway.docker.com (MCP Gateway Enterprise); fail-closed by design - no policy means deny-all" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: The `sbx mcp` subtree stays hidden until you set `SBX_MCP_URL`, and only two values carry the full governed flow. A **local gateway** at `http://localhost:8811` - Compose or the Desktop MCP Toolkit, you run it and control what's registered, best for learning the mechanics. Or a **hosted control plane** at `gateway.docker.com` - MCP Gateway Enterprise, where org policy governs what's invocable with central audit, the real governance story. And the crucial default: it is **fail-closed by design** - no policy loaded means deny-all. Policy is authored in Docker Hub, fetched at `docker login`, and developers can't override it.

---

<!-- chrome: false -->

<img src="assets/slide-hub-governance.webp" alt="Author once in Docker Hub, enforce around the sandbox and at the gateway: Docker Hub AI Governance syncs at docker login to the sbx daemon (network proxy + policy, filesystem policy, audit log) and the MCP Gateway checks policy on every call" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the whole enforcement picture. You **author policy once in Docker Hub** - the AI Governance settings UI or the Governance API. It syncs to the host at `docker login`, takes precedence, and fails closed. On the developer laptop the agent runs in the microVM, and the **sbx daemon** enforces the network proxy, network policy, and filesystem policy - writing **every decision to an audit log** as JSONL. Tool calls leave via `SBX_MCP_URL` to the **MCP Gateway** - local 8811 or gateway.docker.com - which runs its own **policy check and audit on every call**. Same policy, enforced in two places: around the sandbox and at the gateway.

---

<!-- chrome: false -->

<img src="assets/slide-mcp-lifecycle.webp" alt="The server lifecycle - five commands: sbx mcp add to register, sbx mcp ls/inspect to see the record, --static-mcp to attach to a sandbox, and /mcp inside the agent to verify" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Hands-on, the `sbx mcp` lifecycle is basically five commands. **add** registers a server - `sbx mcp add local-wiki --command docker --args "run,-i,--rm,mcp/wikipedia-mcp"` - and it takes a list, stdio, remote-OAuth, or a docker.io image. **ls / inspect** shows the record, registration only - it doesn't start anything. **--static-mcp** attaches it to a sandbox at launch - `sbx run claude --static-mcp local-wiki` - or `sbx mcp load` into a live one; note the flag is `--static-mcp`, not `--mcp`. And inside the agent, **/mcp** verifies it's wired up - you'll see `mcp-gateway connected, 24 tools`, one aggregated gateway, not your individual servers.

---

<!-- chrome: false -->

<img src="assets/slide-cedar-policy.webp" alt="Default-deny allow-list over (server, tool), authored in Cedar: a permit policy allowing exactly get_me on github-official; everything else blocked, evaluated at the gateway on every invoke, same engine as network and filesystem policy" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: And here's what the policy actually looks like - a **default-deny allow-list over (server, tool) pairs, authored in Cedar**, the open-source authorization engine from AWS. Cedar answers "can principal X do action Y on resource Z in context C." This policy permits **exactly one tool - `get_me` on `github-official`** - and by default-deny, every other tool and every other server is **blocked**. It's evaluated **at the gateway on every invoke**, using the **same engine as your network and filesystem policy** - one surface, no bypass. The takeaway: author once, sync everywhere. A developer can `sbx mcp add` any server they like, but if org policy doesn't permit its tools, the calls are denied and audited.

---

<!-- chrome: false -->

<img src="assets/slide-47.webp" alt="Slide 47" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the whole talk in one frame - **two paths, same agent, same prompt**, "containerize catalog service." The **traditional agentic SDLC** on the left pulls packages from random internet repos - npm, DockerHub community, apt, pip - writes `FROM node:20` with no security guidance, and lands at **2 critical, 26 high, 25 medium, 122 low CVEs**, 806 packages, no SBOM, no attestation, running as root. The **agentic SDLC with sbx plus DHI MCP** on the right runs the agent inside an isolated microVM, queries the DHI MCP server first with `dhi_list_repositories` and `dhi_get_image_cves`, and writes `FROM dhi.io/node:24-debian13` - the DHI-recommended base, 0 CVEs, signed, SLSA L3. Result: **all zeros**, 211 packages, SBOM attached, signed, non-root. Same intelligence, same instruction - the only variable is whether the agent is sandboxed and pointed at a trusted source. Let me show you that MCP server up close.

---

<!-- chrome: false -->

<img src="assets/slide-48.webp" alt="Slide 48" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here's the beautiful turn in the story: **the same agent that introduced the vulnerabilities can now query what's secure before it picks a base image**. Connecting it is one config - drop a `dhi` entry pointing at `https://dhi.io/mcp` into Claude Desktop, or a single `claude mcp add dhi --url https://dhi.io/mcp` in Claude Code. That gives the agent **10 tools**: `dhi_list_repositories` to search by name, FIPS, or STIG; `dhi_get_image_cves` with CVSS, EPSS, and fix versions; `dhi_get_image_packages` for the full SBOM; attestations, repository details, even `dhi_create_mirror`. So the agent can answer real questions - "find the Node.js hardened image with the fewest CVEs," "does this image have FIPS and STIG attestations." The line to land: the agent that triggered the vulnerabilities now has the tools to **never make that mistake again**, by querying DHI before every FROM line. Now let's wire that DHI MCP server into the sandbox.

---

<!-- chrome: false -->

<img src="assets/slide-50.webp" alt="Slide 50" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Now we connect the two halves - **wire the DHI MCP server into the sandbox**. On the left, one-time setup: install `sbx`, export the gateway URL, start the sandbox daemon, then register the server by URL with `sbx mcp add remotedhi --url https://dhi.io/mcp`. Inspect it and you see it's a remote server over streamable-http - nothing hand-built. On the right you query it from the agent: `sbx run codex --static-mcp remotedhi`, and the agent's `/mcp` view now lists the tools through the gateway - `dhi_get_image_cves`, `dhi_get_image_details`, and eight more. The callout is the important nuance: **10 tools are now available**, but most are read-only queries. The mutating ones - `dhi_create_mirror`, `dhi_remove_mirror` - are exactly what you want to scope with policy. And that's the next slide.

---

<!-- chrome: false -->

<img src="assets/slide-51.webp" alt="Slide 51" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Last technical slide, and it's the one that separates a demo from production - **govern the tools first, with a Cedar access policy**. On the left is the lab default: a quick unblock that permits every principal, every action - register, invokeTool, invokePrimordial - against every resource. It gets the lab moving, but as the note says, that's governance turned off; don't ship it as your exemplar, and never hand the gateway's built-in primordials a wide-open pass. On the right is the production-scoped version: anyone may register, but `invokeTool` is permitted only when the server is `remotedhi` **and** the tool is one of the named read-only queries - `dhi_get_image_cves`, `dhi_get_image_packages`, `dhi_list_repositories`, and so on. Scoped by design: `dhi_create_mirror`, `dhi_remove_mirror`, and wide-open primordials are deliberately left out - query the catalog, don't mutate it. One gotcha worth flagging - the real action name is `invokeTool`, not `invoke`. That completes the road: development to production, CI failing closed, and the agent sandboxed and governed on both ends. Let's wrap up.

---

<!-- chrome: false -->

<img src="assets/slide-journey-4.webp" alt="The journey, checkpoint 4 of 4: Lab 4 done, DEVELOP and INVOKE green, both sandbox boxes solid, the road is provable end to end" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: This is the final checkpoint, **4 of 4** - the whole road is green. On the left, **DEVELOPMENT** sits inside its own dashed box: the agent develops in an sbx microVM with the host read-only, on a hardened base with 0 CVEs and SLSA L3, buildx attaches SBOM and provenance, and signing binds everything to a verifiable digest. In the middle the **CI GATE** does its job - no critical CVEs, SBOM present, provenance verified - and it **FAILS CLOSED** at the dev-to-prod boundary. On the right, **PRODUCTION** is boxed too: the signed image is deployed pinned by digest, and the agent invokes MCP as a signed, read-only client under `cap_drop ALL` and non-root. The one line to land is at the bottom - **same discipline at both ends**: the agent that BUILDS runs in a box, and the service it BECOMES runs in a box. Least privilege on the left and the right of the road, and 4 of 4 stages provable.

---

<!-- chrome: false -->

<img src="assets/slide-54.webp" alt="Slide 54" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: If you take one slide home, take this one: **your security framework in five steps**. First, **know what is in your images** - SBOM plus VEX, so you can see every package and cut the noise on the ones that do not apply. Second, **verify where they came from** - SLSA provenance and image signing, so trust is bound to a digest, not a hope. Third, **start from a trusted base** - Docker Hardened Images, so you begin near zero CVEs instead of digging out of a pile. Fourth, **enforce at the pipeline** - Docker Scout build policies that fail closed at the dev-to-prod boundary. And fifth, **isolate your agents** - run MCP servers in hardened containers so the agent's tools stay in a box. Each of those was one of our labs; together they are a repeatable playbook you can apply to any agentic stack.

---

<!-- chrome: false -->

<img src="assets/slide-55.webp" alt="Slide 55" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: Here are the **resources and next steps** so you can keep going after today. Everything from this workshop lives in the **lab repo** at `github.com/ajeetraina/simspace-agentic-security` - clone it and run the four labs again at your own pace. Under **Docker docs** you have Hardened Images in Trusted Content, Docker Scout, and the MCP Catalog on Docker Hub. And on the **standards** side, these are the specs behind what we did - SLSA at slsa.dev, VEX at openvex.dev, Cosign and Sigstore for signing, and the MCP specification at modelcontextprotocol.io. Snap a photo of this slide, and then **come find us at the Docker booth** - we would love to hear what you build.

---

<!-- chrome: false -->

<img src="assets/slide-56.webp" alt="Slide 56" width="1600" height="900" loading="lazy" decoding="async" style="position:absolute;inset:0;width:100%;height:100%;max-width:none;max-height:none;object-fit:fill" />

Note: That is the journey - **provable trust, end to end**. Agents now build and ship our containers, and with hardened images, attestation, and sandboxing on both ends of the road, we can prove what they produced instead of just trusting it. Go run the lab, apply the five steps to your own stack, and come say hi at the booth. **Thank you.**

