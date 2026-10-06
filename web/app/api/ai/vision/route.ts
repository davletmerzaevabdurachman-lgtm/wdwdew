export const runtime="nodejs";
export async function POST(req:Request){
 const base=process.env.AI_SERVER_URL;
 if(!base)return Response.json({error:"AI_SERVER_URL missing"},{status:503});
 const r=await fetch(base.replace(/\/$/,"")+"/ai/vision",{method:"POST",headers:{"content-type":"application/json"},body:await req.text()});
 return new Response(await r.text(),{status:r.status,headers:{"content-type":"application/json"}});
}
