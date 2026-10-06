import os, subprocess, tempfile, pathlib

def run_code(code: str, language: str="python", timeout: int=10) -> dict:
    if language != "python": return {"ok":False,"error":"Only Python sandbox is enabled in this worker."}
    timeout=max(1,min(timeout,30))
    with tempfile.TemporaryDirectory() as d:
        p=pathlib.Path(d)/"main.py"; p.write_text(code,encoding="utf-8")
        cmd=["docker","run","--rm","--network","none","--memory","256m","--cpus","0.5","--pids-limit","64","--read-only","-v",f"{d}:/work:ro","python:3.12-alpine","python","/work/main.py"]
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=timeout)
            return {"ok":r.returncode==0,"stdout":r.stdout[-12000:],"stderr":r.stderr[-12000:],"code":r.returncode}
        except subprocess.TimeoutExpired:
            return {"ok":False,"error":"Sandbox timeout"}
