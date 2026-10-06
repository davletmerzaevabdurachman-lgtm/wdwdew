# ABDULS AI architecture

Browser requests go to the Next.js application. The web layer authenticates the request and communicates with the self-hosted AI gateway.

```
Browser
  |
  v
Next.js / Vercel
  |
  v
Authenticated AI Gateway
  |
  +--> Local LLM
  +--> Local Vision
  +--> Local Embeddings
  +--> Local Image Worker
  +--> Tools
  +--> Sandbox
```

The gateway owns model routing, streaming, context assembly, memory retrieval, tool execution policy, and error normalization.

Heavy inference never runs inside Vercel serverless functions.
