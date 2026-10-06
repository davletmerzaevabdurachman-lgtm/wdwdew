# Implementation status

## Implemented
- Next.js/Vercel web shell
- self-hosted AI gateway
- local Ollama adapter
- local model selection through environment
- chat API proxy
- health endpoint
- Docker Compose foundation
- PostgreSQL foundation
- explicit capability errors instead of fake outputs

## Architecture prepared
- streaming
- context manager
- memory
- files/RAG
- vision
- image generation
- speech
- video
- tools
- coding agent
- sandbox
- research

These must only be enabled after their actual worker/adapter is installed and tested.

## Required next milestones
1. Persistent authentication and database schema
2. Streaming UI
3. context + controlled memory
4. uploads + parser + embeddings + vector store
5. vision worker
6. tool registry
7. coding workspace
8. sandbox
9. image/speech workers
10. research/source pipeline
