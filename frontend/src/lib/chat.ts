export type User = { id: number; name: string; email: string; role: string; createdAt: string };
export type Reply = { text?: string; error?: string; users?: User[]; examples?: string[] };
function isUser(value: unknown): value is User {
  if (!value || typeof value !== "object") return false;
  const user = value as Record<string, unknown>;
  return typeof user.id === "number" && ["name", "email", "role", "createdAt"].every(key => typeof user[key] === "string");
}
export function parseReply(value: unknown, ok: boolean): Reply {
  if (!value || typeof value !== "object") return { error: "Respuesta inválida del servidor." };
  const data = value as Record<string, unknown>;
  const examples = Array.isArray(data.examples) ? data.examples.filter((x): x is string => typeof x === "string") : undefined;
  const error = data.error || (!ok ? data.detail || data.message : undefined);
  if (error || !ok) return { error: typeof error === "string" ? error.replace(/^JSON-RPC Error\s+-?\d+:\s*/, "") : "No pudimos procesar tu consulta.", examples };
  if (data.result !== undefined && data.result !== null) {
    const users = Array.isArray(data.result) ? data.result : [data.result];
    if (!users.every(isUser)) return { error: "Respuesta inválida del servidor." };
    return { users, text: typeof data.message === "string" ? data.message : undefined };
  }
  return { error: "Respuesta inesperada del servidor." };
}
