import { parseReply, type Reply } from "./chat";
const MAX_ATTEMPTS = 15;
export async function sendChat(message: string, onWaking: () => void): Promise<Reply> {
  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    try {
      const response = await fetch("/api/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }), signal: AbortSignal.timeout(15000),
      });
      const data: unknown = await response.json();
      const warming = response.status === 503 && data !== null && typeof data === "object" && "code" in data && data.code === "SERVICE_WARMING_UP";
      if (!warming) return parseReply(data, response.ok);
      if (attempt === MAX_ATTEMPTS - 1) break;
      onWaking();
      await new Promise(resolve => setTimeout(resolve, 2000));
    } catch {
      return { error: "No pudimos completar la consulta. Revisa tu conexión e inténtalo nuevamente." };
    }
  }
  return { error: "El servicio sigue sin responder. Espera un momento y vuelve a enviar tu consulta." };
}
