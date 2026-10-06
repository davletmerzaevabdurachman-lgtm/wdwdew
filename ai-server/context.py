def build_context(current:list[dict],summaries:list[str],memories:list[str],project:str|None,documents:list[str],max_chars:int=24000)->list[dict]:
 parts=[]
 if project: parts.append("PROJECT:\n"+project)
 if summaries: parts.append("SUMMARIES:\n"+"
".join(summaries))
 if memories: parts.append("MEMORY:\n"+"
".join(memories))
 if documents: parts.append("RELEVANT FILES:\n"+"
".join(documents))
 system="\n\n".join(parts)
 if system: current=[{"role":"system","content":system}]+current
 text=0; out=[]
 for m in reversed(current):
  n=len(m.get("content",""))
  if text+n>max_chars: break
  out.append(m);text+=n
 return list(reversed(out))
