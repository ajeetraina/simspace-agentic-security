Animated build placed immediately after the Agenda slide (slide-03), before the
workshop-structure slide. Deck is image-per-slide (no reveal fragments), so the
animation is 5 growing frames (slide-incident-1..5) + the full recap
(slide-incident), revealed one row at a time, newest spotlighted:

1. **Author** - This actually happened. At **2:47 in the morning**, a commit lands - and the author isn't a person. It's an agent: **svc-build-agent**.
2. **Change** - What did it change? It **bumped a base image and regenerated the Dockerfile** - real changes to how the app actually gets built.
3. **Reviewer** - Who reviewed it? **CI did** - all checks green. That is the only review this change ever got.
4. **Deployed** - And it shipped - straight to **production, 3:12 AM.** Twenty-five minutes from an agent's commit to running in prod.
5. **Reviewed by a human? No** - And here's the row that matters. Nobody was awake, nobody signed off - and it's running in prod right now.
6. **Who approved that build?** - So sit with the question. Every item on that agenda is really about being able to answer it - provably. Now, here's how we're going to get there.
