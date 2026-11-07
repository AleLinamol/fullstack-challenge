"use client";
import { useEffect, useRef, useState, type FormEvent } from "react";
import Link from "next/link";
import { type Reply } from "../lib/chat";
import { sendChat } from "../lib/send-chat";
type Message = Reply & { id: number; from: "user" | "system" };
const examples = ["usuario 2", "buscar ana", "lista 3"];
export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [waking, setWaking] = useState(false);
  const busy = useRef(false);
  const end = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLInputElement>(null);
  const sequence = useRef(0);
  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth", block: "end" }); }, [messages, loading]);
  async function send(value: string) {
    const message = value.trim();
    if (!message || busy.current) return;
    busy.current = true;
    setLoading(true);
    setWaking(false);
    setText("");
    setMessages(prev => [...prev, { id: sequence.current++, from: "user", text: message }]);
    const reply = await sendChat(message, () => setWaking(true));
    setMessages(prev => [...prev, { ...reply, id: sequence.current++, from: "system" }]);
    busy.current = false;
    setLoading(false);
    input.current?.focus();
  }
  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); void send(text); }
  return (
    <main className="page-shell">
      <header className="site-header">
        <Link href="/" className="brand" aria-label="Nexo, inicio">
          <span className="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><path d="M10 21V11l12 10V11" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/><circle cx="10" cy="10" r="3" fill="currentColor"/><circle cx="22" cy="22" r="3" fill="currentColor"/></svg></span>
          <span>nexo<span className="brand-period">.</span></span>
        </Link>
        <span className="demo-badge"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m8 2 1.5 4.5L14 8l-4.5 1.5L8 14l-1.5-4.5L2 8l4.5-1.5L8 2Z" stroke="currentColor" strokeLinejoin="round"/></svg>Demo interactiva</span>
      </header>
      <section className="chat-panel" aria-labelledby="chat-title">
        <div className="chat-heading">
          <p className="eyebrow">Personas que conectan</p>
          <h1 id="chat-title">Encontrá a quien buscás.</h1>
          <p className="intro">Un nombre, un ID o una lista. Tu próxima conexión empieza con una consulta.</p>
          <div className="suggestions">{examples.map(example => <button key={example} disabled={loading} onClick={() => void send(example)} className="suggestion"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4 12 12 4M4 4h8v8" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round"/></svg>{example}</button>)}</div>
        </div>
        <div role="log" aria-label="Conversación" aria-live="polite" aria-relevant="additions" aria-busy={loading} className="conversation">
          {messages.length === 0 && <div className="empty-state">
            <div className="empty-symbol" aria-hidden="true"><svg viewBox="0 0 40 40" fill="none"><path d="M31 25.5a4 4 0 0 1-4 4H16l-7 5v-9a4 4 0 0 1-3-4v-12a4 4 0 0 1 4-4h17a4 4 0 0 1 4 4v16Z" stroke="currentColor" strokeWidth="1.5" strokeLinejoin="round"/><circle cx="13" cy="17" r="1.5" fill="currentColor"/><circle cx="19" cy="17" r="1.5" fill="currentColor"/><circle cx="25" cy="17" r="1.5" fill="currentColor"/></svg></div>
            <p className="empty-title">¿A quién buscás hoy?</p>
            <p className="empty-description">Probá una sugerencia o escribí tu consulta.<br/>Nosotros encontramos la conexión.</p>
          </div>}
          {messages.map(message => <article key={message.id} className={`message ${message.from === "user" ? "message-user" : message.error ? "message-error" : "message-system"}`}>
            <p className="message-author">{message.from === "user" ? "Vos" : "Nexo"}</p>
            {message.text && <p className="break-words text-sm leading-6">{message.text}</p>}
            {message.error && <p className="text-sm leading-6">{message.error}</p>}
            {message.examples && <p className="mt-2 text-xs opacity-80">Probá con: {message.examples.join(" · ")}</p>}
            {message.users && (message.users.length === 0 ? <p className="text-sm">No se encontraron usuarios.</p> : <div className="grid gap-3 sm:grid-cols-2">{message.users.map(user => <div key={user.id} className="user-card">
              <div className="mb-4 flex items-center justify-between gap-3"><span className="user-id">ID {user.id}</span><span className="role-badge">{user.role}</span></div>
              <div className="flex items-center gap-3"><span className="user-avatar" aria-hidden="true">{user.name.split(" ").map(part => part[0]).slice(0, 2).join("")}</span><h2 className="min-w-0 text-sm font-semibold">{user.name}</h2></div>
              <p className="mt-3 break-all text-sm text-white/85">{user.email}</p>
              <p className="mt-3 text-xs text-white/65">Creado: {Number.isNaN(Date.parse(user.createdAt)) ? "Fecha no disponible" : new Intl.DateTimeFormat("es-AR", { timeZone: "UTC" }).format(new Date(user.createdAt))}</p>
            </div>)}</div>)}
          </article>)}
          {loading && <p role="status" className="loading-message"><span className="loading-dot" aria-hidden="true"/>{waking ? "El servicio está iniciándose. La primera consulta puede tardar hasta 3 minutos…" : "Buscando tu conexión…"}</p>}
          <div ref={end} />
        </div>
        <div className="composer-area">
          <form onSubmit={submit} className="composer">
            <label htmlFor="message" className="sr-only">Tu consulta</label>
            <input ref={input} id="message" value={text} onChange={event => setText(event.target.value)} maxLength={500} readOnly={loading} placeholder="Escribí una consulta…" autoComplete="off" className="composer-input" />
            <button disabled={loading || !text.trim()} type="submit" className="send-button"><span>Enviar</span><svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M4 10h12m-5-5 5 5-5 5" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/></svg></button>
          </form>
          <p className="composer-hint">Un pequeño directorio. Grandes conexiones.<span>Enter para enviar ↵</span></p>
        </div>
      </section>
      <footer className="site-footer"><span>Fullstack Challenge<span className="footer-separator">/</span>Datos de demostración</span><span>Hecho para conectar.</span></footer>
    </main>
  );
}
