import { NextResponse } from "next/server";
export const runtime = "nodejs";
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
      signal: AbortSignal.timeout(25000), cache: "no-store",
    });
    if (response.status >= 500) throw new Error("Upstream unavailable");
    const data: unknown = await response.json();
    if (!data || typeof data !== "object") throw new Error("Invalid upstream response");
    return NextResponse.json(data, { status: response.status });
  } catch {
    return NextResponse.json({ error: "No pudimos conectar con el servicio. Inténtalo nuevamente en unos instantes." }, { status: 502 });
  }
}
