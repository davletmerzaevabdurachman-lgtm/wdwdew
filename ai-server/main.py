from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="ABDULS AI Gateway", version="0.1.0")


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "abduls-ai-gateway"}


@app.post("/ai/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    # Real local inference adapter will be connected in the next stage.
    # Do not silently fall back to a commercial provider.
    return {
        "status": "not_ready",
        "message": "Local inference adapter is not configured yet.",
        "conversation_id": request.conversation_id,
    }
