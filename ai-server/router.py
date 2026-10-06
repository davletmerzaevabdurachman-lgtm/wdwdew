import os

def route(capability: str, requested: str | None = None) -> str:
    if requested:
        return requested
    names={"chat":"CHAT_MODEL","vision":"VISION_MODEL","image":"IMAGE_MODEL","embed":"EMBEDDING_MODEL","speech":"SPEECH_MODEL"}
    return os.getenv(names.get(capability,"CHAT_MODEL"), "")
