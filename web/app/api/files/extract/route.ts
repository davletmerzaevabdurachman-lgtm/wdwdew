export const runtime="nodejs";
export async function POST(req:Request){
 const base=process.env.AI_SERVER_URL;
 if(!base)return Response.json({error:"AI_SERVER_URL missing"},{status:503});
 const form=await req.formData();
 const r=await fetch(base.replace(/\/$/,"")+"/files/extract",{method:"POST",body:form});
 return new Response(await r.text(),{status:r.status,headers:{"content-type":"application/json"}});
}
