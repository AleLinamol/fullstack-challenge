import { NextResponse } from "next/server";
export const runtime = "nodejs";
export const maxDuration = 15;
export async function POST(request: Request) {
  let body: unknown;
  try { body = await request.json(); } catch {
    return NextResponse.json({ error: "El mensaje debe ser JSON válido." }, { status: 400 });
  }
  if (!body || typeof body !== "object" || !("message" in body) || typeof body.message !== "string" || !body.message.trim() || body.message.length > 500) {
    return NextResponse.json({ error: "Escribe un mensaje de entre 1 y 500 caracteres." }, { status: 400 });
  }
  const base = process.env.ORCHESTRATOR_URL;
  if (!base) return NextResponse.json({ error: "El servicio de chat todavía no está configurado." }, { status: 503 });
  try {
    const response = await fetch(`${base.replace(/\/$/, "")}/chat`, {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: body.message.trim() }),
      signal: AbortSignal.timeout(10000), cache: "no-store",
    });
    if ([502, 503, 504].includes(response.status)) throw new Error("Upstream starting");
    if (response.status >= 500) return NextResponse.json({ error: "El servicio no pudo procesar la consulta." }, { status: 502 });
    const data: unknown = await response.json();
    if (!data || typeof data !== "object") throw new Error("Invalid upstream response");
    return NextResponse.json(data, { status: response.status });
  } catch {
    return NextResponse.json({ code: "SERVICE_WARMING_UP", error: "El servicio está iniciándose. Reintentando…" }, { status: 503, headers: { "Retry-After": "2" } });
  }
}
