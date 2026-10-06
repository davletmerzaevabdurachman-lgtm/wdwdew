import os, json, base64, uuid
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import httpx
from capabilities import capability_status
from context import ContextInput, build_context
from router import route
from files import extract_text
from sandbox.runner import run_code

app=FastAPI(title="ABDULS AI Gateway", version="1.0.0")
OLLAMA=os.getenv("OLLAMA_BASE_URL","http://ollama:11434").rstrip("/")

class ChatRequest(BaseModel):
    messages:list[dict]=Field(default_factory=list)
    model:str|None=None
    stream:bool=True
    system:str|None=None
    summary:str=""
    project:str=""
    memories:list[str]=Field(default_factory=list)
    files:list[str]=Field(default_factory=list)

@app.get("/health")
async def health():
    return {"ok":True,"service":"abduls-ai-gateway","capabilities":capability_status()}

@app.post("/ai/chat")
async def chat(req:ChatRequest):
    model=route("chat",req.model)
    if not model: raise HTTPException(503,"No local chat model configured. Set CHAT_MODEL and install that model in Ollama.")
    messages=build_context(ContextInput(req.messages,req.summary,req.project,req.memories,req.files))
    if req.system: messages.insert(0,{"role":"system","content":req.system})
    payload={"model":model,"messages":messages,"stream":req.stream}
    async with httpx.AsyncClient(timeout=None) as client:
        if not req.stream:
            r=await client.post(f"{OLLAMA}/api/chat",json=payload)
            if r.status_code>=400: raise HTTPException(502,r.text)
            data=r.json()
            return {"message":data.get("message",{}),"model":model}
        async def gen():
            async with client.stream("POST",f"{OLLAMA}/api/chat",json=payload) as r:
                if r.status_code>=400:
                    yield json.dumps({"error":await r.aread()}).encode()+b"\n"; return
                async for line in r.aiter_lines():
                    if line: yield line.encode()+b"\n"
        return StreamingResponse(gen(),media_type="application/x-ndjson")

class VisionRequest(BaseModel):
    prompt:str
    image_base64:str
    model:str|None=None

@app.post("/ai/vision")
async def vision(req:VisionRequest):
    model=route("vision",req.model)
    if not model: raise HTTPException(503,"No local vision model configured.")
    payload={"model":model,"messages":[{"role":"user","content":req.prompt,"images":[req.image_base64]}],"stream":False}
    async with httpx.AsyncClient(timeout=None) as client:
        r=await client.post(f"{OLLAMA}/api/chat",json=payload)
        if r.status_code>=400: raise HTTPException(502,r.text)
        return r.json()

class EmbedRequest(BaseModel):
    input:str|list[str]
    model:str|None=None

@app.post("/ai/embed")
async def embed(req:EmbedRequest):
    model=route("embed",req.model)
    if not model: raise HTTPException(503,"No local embedding model configured.")
    async with httpx.AsyncClient(timeout=None) as client:
        r=await client.post(f"{OLLAMA}/api/embed",json={"model":model,"input":req.input})
        if r.status_code>=400: raise HTTPException(502,r.text)
        return r.json()

@app.post("/files/extract")
async def file_extract(file:UploadFile=File(...)):
    data=await file.read()
    try: text=extract_text(file.filename or "upload",data)
    except ValueError as e: raise HTTPException(415,str(e))
    return {"name":file.filename,"text":text,"size":len(data)}

class CodeRequest(BaseModel):
    code:str
    language:str="python"
    timeout:int=10

@app.post("/tools/run")
async def tools_run(req:CodeRequest):
    if os.getenv("SANDBOX_ENABLED","true").lower()!="true": raise HTTPException(503,"Sandbox disabled.")
    return run_code(req.code,req.language,req.timeout)

@app.post("/ai/image")
async def image(payload:dict):
    url=os.getenv("IMAGE_SERVER_URL")
    if not url: raise HTTPException(503,"No local image server configured.")
    async with httpx.AsyncClient(timeout=None) as client:
        r=await client.post(url.rstrip("/")+"/generate",json=payload)
        if r.status_code>=400: raise HTTPException(502,r.text)
        return r.json()

@app.post("/ai/research")
async def research(payload:dict):
    url=os.getenv("SEARCH_BACKEND_URL")
    if not url: raise HTTPException(503,"No search backend configured.")
    async with httpx.AsyncClient(timeout=30) as client:
        r=await client.post(url,json=payload)
        if r.status_code>=400: raise HTTPException(502,r.text)
        return r.json()
