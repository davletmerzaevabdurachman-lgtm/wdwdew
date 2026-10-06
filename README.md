# ABDULS AI

Self-hosted AI workspace with a Next.js frontend and a separate local inference gateway. Core AI does not require OpenAI, Anthropic, Gemini, Groq or OpenRouter API keys.

## What is actually implemented

- Next.js chat workspace with streaming responses, stop and clean error handling
- FastAPI AI gateway
- Ollama local chat inference
- configurable local vision and embeddings through Ollama
- PDF/DOCX/XLSX/text/code extraction
- Docker-isolated Python sandbox with no network and resource limits
- PostgreSQL + pgvector schema
- capability detection so unavailable media backends are not presented as ready
- Vercel-compatible frontend deployment
- GitHub Actions build/type-check path

## Local start

1. Install Docker.
2. Start the stack:

```bash
docker compose up -d --build
```

3. Pull a local model:

```docker compose exec ollama ollama pull llama3.2:3b```

Optional embeddings:

```docker compose exec ollama ollama pull nomic-embed-text```

4. Start the web app:

```bash
cd web
npm install
npm run dev
```

Open http://localhost:3000.

## Vercel

Deploy the `web` directory as the Vercel Root Directory and set `AI_SERVER_URL` to a reachable HTTPS address for your self-hosted gateway. Do not put model API keys in Vercel; the local inference server owns the models.

## Important

Heavy local inference, Docker sandboxing and local media models cannot run inside a normal Vercel function. Vercel hosts the interface; your own machine/server hosts inference and workers.

Only capabilities with a configured backend are reported as available.
