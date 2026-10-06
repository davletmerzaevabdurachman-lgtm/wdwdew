import {NextRequest} from "next/server";
export async function POST(req:NextRequest,{params}:{params:Promise<{capability:string}>}){
 const {capability}=await params; const base=process.env.AI_SERVER_URL;
 if(!base)return Response.json({error:"AI_SERVER_URL not configured"},{status:503});
 const allowed=["chat","vision","image","embed","speech","research","tools","code"];
 if(!allowed.includes(capability))return Response.json({error:"Unknown capability"},{status:404});
 try{const r=await fetch(base.replace(/\/$/,"")+"/ai/"+capability,{method:"POST",headers:{"content-type":req.headers.get("content-type")||"application/json","x-abduls-internal-token":process.env.AI_SERVER_INTERNAL_TOKEN||""},body:await req.text(),cache:"no-store"});return new Response(r.body,{status:r.status,headers:{"content-type":r.headers.get("content-type")||"application/json"}})}catch{return Response.json({error:"Self-hosted AI server unavailable"},{status:503})}
}