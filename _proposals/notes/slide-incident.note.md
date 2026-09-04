Cold-open build (slide-incident-1..5 + slide-incident, revealed one row at a time):

1. **Author** - Before I introduce myself or this talk, look at this. At **2:47 in the morning**, a commit lands - and the author isn't a person. It's an agent: **svc-build-agent**.
2. **Change** - What did it change? It **bumped a base image and regenerated the Dockerfile** - real changes to how your app actually gets built.
3. **Reviewer** - Who reviewed it? **CI did** - all checks green. That is the only review this change ever got.
4. **Deployed** - And it shipped - straight to **production, 3:12 AM.** Twenty-five minutes from an agent's commit to running in prod.
5. **Reviewed by a human? No** - And here's the row that matters. Nobody was awake, nobody signed off - and it is running in prod right now.
6. **Who approved that build?** - So before anything else, sit with the question. Hold onto it - everything we do today is about being able to answer it, provably. Now, let me introduce this session.

Reused later as a callback (see [[slide-incident-callback]]).
