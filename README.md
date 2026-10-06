# ABDULS AI

A real self-hosted AI platform, not an API wrapper.

## Deployment model

The Next.js application is Vercel-compatible. Heavy inference stays on a separately hosted AI server because Vercel serverless functions are not a suitable place for persistent local LLM inference.

## No commercial AI dependency

Core inference uses a local model backend. There are no required OpenAI, Anthropic, Gemini, Groq or OpenRouter keys.

## Local development

```bash
cd web
npm install
npm run dev
```

Run the AI server:

```bash
cd ai-server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Run a local model backend such as Ollama separately and set `OLLAMA_BASE_URL` and `CHAT_MODEL`.

The project never presents unimplemented capabilities as completed.
