import os,json
from fastapi import FastAPI,HTTPException,UploadFile,File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
from capabilities import capability_status
from router import choose_model
from tools import calculator

app=FastAPI(title="ABDULS AI Gateway",version="1.0.0")
OLLAMA=os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
DEFAULT=os.getenv("CHAT_MODEL","llama3.2")
class Chat(BaseModel):
 message:str=""
 messages:list[dict]|None=None
 conversation_id:str|None=None
 stream:bool=False
 task:str="chat"
class ToolRequest(BaseModel):
 name:str
 arguments:dict={}

@app.get("/health")
async def health(): return {"status":"ok","local_inference":True,"capabilities":capability_status()}

@app.get("/models")
async def models(): return {"chat":os.getenv("CHAT_MODEL"),"vision":os.getenv("VISION_MODEL"),"image":os.getenv("IMAGE_MODEL"),"embedding":os.getenv("EMBEDDING_MODEL"),"speech":os.getenv("SPEECH_MODEL"),"video":os.getenv("VIDEO_MODEL")}

@app.post("/ai/chat")
async def chat(req:Chat):
 model=choose_model(req.task,dict(os.environ)) or DEFAULT
 msgs=req.messages or [{"role":"user","content":req.message}]
 if req.stream:
  async def gen():
   async with httpx.AsyncClient(timeout=None) as c:
    async with c.stream("POST",OLLAMA+"/api/chat",json={"model":model,"messages":msgs,"stream":True}) as r:
     if r.status_code>=400: yield (json.dumps({"error":"local inference failed"})+"\n").encode();return
     async for line in r.aiter_lines():
      if line: yield (line+"\n").encode()
  return StreamingResponse(gen(),media_type="application/x-ndjson")
 async with httpx.AsyncClient(timeout=None) as c:
  r=await c.post(OLLAMA+"/api/chat",json={"model":model,"messages":msgs,"stream":False})
 if r.status_code>=400: raise HTTPException(502,"Local model failed")
 return {"message":r.json().get("message",{}).get("content",""),"model":model,"local":True}

@app.post("/ai/tools")
async def tools(req:ToolRequest):
 if req.name=="calculator": return {"result":calculator(str(req.arguments.get("expression","")))}
 raise HTTPException(404,"Tool unavailable")

@app.post("/ai/{capability}")
async def capability(capability:str):
 if capability in {"vision","image","embed","speech","video"}:
  raise HTTPException(501,f"Local {capability} model is not configured")
 raise HTTPException(404,"Unknown capability")
