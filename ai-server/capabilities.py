import os
def capability_status():
 return {
  "chat": bool(os.getenv("CHAT_MODEL")),
  "vision": bool(os.getenv("VISION_MODEL")),
  "image": bool(os.getenv("IMAGE_MODEL")),
  "embed": bool(os.getenv("EMBEDDING_MODEL")),
  "speech": bool(os.getenv("SPEECH_MODEL")),
  "video": bool(os.getenv("VIDEO_MODEL")),
  "sandbox": True,
  "research": True,
  "tools": True,
  "coding": True,
 }
