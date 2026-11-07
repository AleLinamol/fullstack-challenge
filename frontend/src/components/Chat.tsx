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
    <main className="mx-auto flex min-h-dvh max-w-4xl flex-col px-4 py-6 sm:px-8 sm:py-12">
      <header className="mb-6 flex items-center justify-between gap-4">
        <Link href="/" className="text-lg font-bold tracking-tight">jahi<span className="text-violet-400">.</span></Link>
        <span className="rounded-full border border-slate-700 px-3 py-1 text-xs text-slate-300">Fullstack Challenge</span>
      </header>
      <section className="flex min-h-[75dvh] flex-1 flex-col overflow-hidden rounded-3xl border border-slate-700 bg-slate-900 shadow-2xl" aria-labelledby="chat-title">
        <div className="border-b border-slate-700 p-6 sm:p-8">
          <p className="mb-2 text-xs font-semibold tracking-[0.2em] text-violet-300 uppercase">Directorio de usuarios</p>
          <h1 id="chat-title" className="text-3xl font-semibold tracking-tight">Una consulta, una conversación.</h1>
          <p className="mt-3 max-w-xl text-sm leading-6 text-slate-300">Busca por nombre, consulta un usuario por su ID o pide una lista. Los datos de este directorio son de demostración.</p>
          <div className="mt-5 flex flex-wrap gap-2">{examples.map(example => <button key={example} disabled={loading} onClick={() => void send(example)} className="rounded-full border border-violet-400/40 px-3 py-2 text-sm text-violet-200 transition hover:bg-violet-400/10 disabled:opacity-40">{example}</button>)}</div>
        </div>
        <div role="log" aria-label="Conversación" aria-live="polite" aria-relevant="additions" aria-busy={loading} className="flex max-h-[55dvh] min-h-64 flex-1 flex-col gap-4 overflow-y-auto p-4 sm:p-8">
          {messages.length === 0 && <div className="my-auto py-8 text-center text-slate-400"><p className="text-lg text-slate-200">¿A quién buscas hoy?</p><p className="mt-2 text-sm">Elige un ejemplo o escribe tu consulta abajo.</p></div>}
          {messages.map(message => <article key={message.id} className={`max-w-full rounded-2xl p-4 ${message.from === "user" ? "ml-auto bg-violet-600 text-white" : message.error ? "border border-rose-400/40 bg-rose-950/30 text-rose-200" : "mr-auto w-full bg-slate-800"}`}>
            <p className="mb-2 text-xs font-semibold opacity-70">{message.from === "user" ? "Tú" : "Asistente"}</p>
            {message.text && <p className="break-words text-sm leading-6">{message.text}</p>}
            {message.error && <p className="text-sm">{message.error}</p>}
            {message.examples && <p className="mt-2 text-xs">Prueba con: {message.examples.join(" · ")}</p>}
            {message.users && (message.users.length === 0 ? <p>No se encontraron usuarios.</p> : <div className="grid gap-3 sm:grid-cols-2">{message.users.map(user => <div key={user.id} className="min-w-0 rounded-xl border border-slate-600 bg-slate-900/60 p-4">
              <div className="flex items-center justify-between gap-3"><span className="text-xs text-violet-300">ID {user.id}</span><span className="rounded-full bg-slate-700 px-2 py-1 text-xs">{user.role}</span></div>
              <h2 className="mt-3 font-semibold">{user.name}</h2><p className="mt-1 break-all text-sm text-slate-300">{user.email}</p>
              <p className="mt-3 text-xs text-slate-400">Creado: {Number.isNaN(Date.parse(user.createdAt)) ? "Fecha no disponible" : new Intl.DateTimeFormat("es-AR", { timeZone: "UTC" }).format(new Date(user.createdAt))}</p>
            </div>)}</div>)}
          </article>)}
          {loading && <p role="status" className="animate-pulse text-sm text-violet-200">{waking ? "El servicio está iniciándose. La primera consulta puede tardar hasta 3 minutos…" : "Consultando el directorio…"}</p>}
          <div ref={end} />
        </div>
        <form onSubmit={submit} className="mt-auto flex gap-2 border-t border-slate-700 p-4 sm:p-6">
          <label htmlFor="message" className="sr-only">Tu consulta</label>
          <input ref={input} id="message" value={text} onChange={event => setText(event.target.value)} maxLength={500} readOnly={loading} placeholder="Por ejemplo: buscar ana" autoComplete="off" className="min-w-0 flex-1 rounded-xl border border-slate-600 bg-slate-950 px-4 py-3 text-sm placeholder:text-slate-500" />
          <button disabled={loading || !text.trim()} type="submit" className="rounded-xl bg-violet-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-violet-400 disabled:cursor-not-allowed disabled:opacity-40">Enviar</button>
        </form>
      </section>
      <footer className="pt-5 text-center text-xs text-slate-400">Next.js · TypeScript · Tailwind CSS · FastAPI</footer>
    </main>
  );
}
