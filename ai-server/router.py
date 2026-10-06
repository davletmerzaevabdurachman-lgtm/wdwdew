def choose_model(task:str,env:dict)->str|None:
 keys={"chat":"CHAT_MODEL","code":"CODE_MODEL","vision":"VISION_MODEL","image":"IMAGE_MODEL","embed":"EMBEDDING_MODEL","speech":"SPEECH_MODEL"}
 return env.get(keys.get(task,"CHAT_MODEL")) or env.get("CHAT_MODEL")
