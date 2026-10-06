import {NextRequest} from "next/server";
export async function POST(req:NextRequest){
 const body=await req.json();
 const base=process.env.AI_SERVER_URL;
 if(!base)return Response.json({message:"AI_SERVER_URL ist nicht konfiguriert."},{status:503});
 try{
  const r=await fetch(base.replace(/\/$/,"")+"/ai/chat",{method:"POST",headers:{"content-type":"application/json","x-abduls-internal-token":process.env.AI_SERVER_INTERNAL_TOKEN??""},body:JSON.stringify(body),cache:"no-store"});
  const data=await r.json();
  return Response.json(data,{status:r.status});
 }catch{return Response.json({message:"Self-hosted AI Gateway nicht erreichbar."},{status:503});}
}