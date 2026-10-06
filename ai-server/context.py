from dataclasses import dataclass
from typing import Any

@dataclass
class ContextInput:
    messages: list[dict[str, Any]]
    summary: str = ""
    project: str = ""
    memories: list[str] | None = None
    files: list[str] | None = None

def build_context(data: ContextInput) -> list[dict[str, Any]]:
    out=[]
    if data.project: out.append({"role":"system","content":f"Project context:\n{data.project}"})
    if data.summary: out.append({"role":"system","content":f"Conversation summary:\n{data.summary}"})
    if data.memories: out.append({"role":"system","content":"Relevant memories:\n" + "\n".join(f"- {x}" for x in data.memories[-20:])})
    if data.files: out.append({"role":"system","content":"Available project files:\n" + "\n".join(f"- {x}" for x in data.files[-100:])})
    out.extend(data.messages[-40:])
    return out
