import os,json
from typing import AsyncIterator
from fastapi import FastAPI,HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

app=FastAPI(title="ABDULS AI Gateway",version="1.0.0")
OLLAMA=os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
MODEL=os.getenv("CHAT_MODEL","llama3.2")
TOKEN=os.getenv("AI_SERVER_INTERNAL_TOKEN","")

class ChatRequest(BaseModel):
 message:str
 conversation_id:str|None=None
 messages:list[dict]|None=None
 stream:bool=False

@app.get("/health")
async def health(): return {"status":"ok","inference":"local","model":MODEL}

async def local_chat(req:ChatRequest):
 payload={"model":MODEL,"messages":req.messages or [{"role":"user","content":req.message}],"stream":req.stream}
 async with httpx.AsyncClient(timeout=None) as c:
  return await c.post(OLLAMA+"/api/chat",json=payload)

@app.post("/ai/chat")
async def chat(req:ChatRequest):
 if not req.message and not req.messages: raise HTTPException(400,"message or messages required")
 if req.stream:
  async def gen()->AsyncIterator[bytes]:
   async with httpx.AsyncClient(timeout=None) as c:
    async with c.stream("POST",OLLAMA+"/api/chat",json={"model":MODEL,"messages":req.messages or [{"role":"user","content":req.message}],"stream":True}) as r:
     if r.status_code>=400: yield json.dumps({"error":"local model error"}).encode()+b"\n"; return
     async for line in r.aiter_lines():
      if line: yield (line+"\n").encode()
  return StreamingResponse(gen(),media_type="application/x-ndjson")
 r=await local_chat(req)
 if r.status_code>=400: return Response(status_code=502,content=json.dumps({"message":"Local model failed"}),media_type="application/json")
 data=r.json(); return {"message":data.get("message",{}).get("content",""),"model":MODEL,"local":True}

@app.post("/ai/vision")
async def vision(): raise HTTPException(501,"Vision adapter is not configured")

@app.post("/ai/image")
async def image(): raise HTTPException(501,"Local image worker is not configured")

@app.post("/ai/embed")
async def embed(): raise HTTPException(501,"Local embedding worker is not configured")

@app.post("/ai/speech")
async def speech(): raise HTTPException(501,"Local speech worker is not configured")
