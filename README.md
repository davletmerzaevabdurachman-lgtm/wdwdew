# ABDULS AI

Self-hosted, general-purpose AI platform.

## Architecture

- `web/` — Next.js frontend designed for Vercel
- `ai-server/` — self-hosted AI gateway and local inference
- `workers/` — isolated background workers
- `sandbox/` — isolated code execution
- `database/` — database schema and migrations
- `docs/` — architecture and deployment documentation

## Core rule

ABDULS AI does not require commercial AI API keys. Core inference is performed by locally hosted models.

## Development order

1. Web shell and chat
2. Self-hosted LLM gateway
3. Streaming
4. Context and memory
5. Files and RAG
6. Vision
7. Tools and coding agent
8. Sandbox
9. Image generation
10. Research and speech

Only implemented capabilities are exposed to users.
