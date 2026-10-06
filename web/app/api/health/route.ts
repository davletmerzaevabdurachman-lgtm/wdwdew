export const dynamic="force-dynamic";
export async function GET(){
  const base=process.env.AI_SERVER_URL;
  if(!base) return Response.json({ok:false,error:"AI_SERVER_URL missing"},{status:503});
  try{
    const r=await fetch(base.replace(/\/$/,"")+"/health",{cache:"no-store"});
    return Response.json(await r.json(),{status:r.status});
  }catch(e){return Response.json({ok:false,error:"AI server unreachable"},{status:503});}
}
