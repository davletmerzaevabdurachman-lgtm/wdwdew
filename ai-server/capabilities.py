import os

def capability_status():
    return {
      "chat": bool(os.getenv("CHAT_MODEL")),
      "vision": bool(os.getenv("VISION_MODEL")),
      "image": bool(os.getenv("IMAGE_SERVER_URL")),
      "embed": bool(os.getenv("EMBEDDING_MODEL")),
      "speech": bool(os.getenv("SPEECH_MODEL")),
      "video": bool(os.getenv("VIDEO_SERVER_URL")),
      "sandbox": os.getenv("SANDBOX_ENABLED","true").lower()=="true",
      "research": bool(os.getenv("SEARCH_BACKEND_URL")),
      "tools": True,
      "coding": True,
    }
