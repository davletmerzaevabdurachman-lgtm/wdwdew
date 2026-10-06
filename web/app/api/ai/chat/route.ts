import { NextRequest } from "next/server";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const base = process.env.AI_SERVER_URL;
  if (!base) return Response.json({ error: "AI_SERVER_URL is not configured." }, { status: 503 });
  const body = await req.text();
  const upstream = await fetch(`${base.replace(/\/$/,"")}/ai/chat`, {
    method:"POST",
    headers:{"content-type":"application/json"},
    body
  });
  if (!upstream.ok || !upstream.body) {
    return new Response(await upstream.text(), {status:upstream.status,headers:{"content-type":"application/json"}});
  }
  return new Response(upstream.body,{status:200,headers:{"content-type":"application/x-ndjson; charset=utf-8","cache-control":"no-cache"}});
}
