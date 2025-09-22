import React, { useState, useEffect, useRef } from "react";
// import { mockSendMessage } from '../../mocks/chatMock'; // Ya no se usa esta línea
import ChatUsersList from "./ChatUsersList";
import ChatInput from "./ChatInput";
import styles from "./ChatUI.module.css";

export default function ChatUI() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Se reemplaza mockSendMessage por una llamada POST al orchestrator
  const sendMessage = async (text) => {
    setMessages((prev) => [...prev, { from: "user", text }]);
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }), // Ajusta el cuerpo según la API del orchestrator
      });

      if (!response.ok) {
        throw new Error(`Error en la respuesta: ${response.statusText}`);
      }

      const data = await response.json();

      if (data.error) {
        setMessages((prev) => [
          ...prev,
          { from: "system", error: data.error, examples: data.examples },
        ]);

      } else {
        setMessages((prev) => [...prev, { from: "system", data: data.result }]);
      }

    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { from: "system", error: `Error inesperado: ${error.message}` },
      ]);

    } finally {
      setLoading(false);
    }

  };

  return (
    <div className={styles.chatContainer}>
      <h2 className={styles.title}>Chat de Usuarios (Orchestrator)</h2>

      <ChatUsersList
        messages={messages}
        loading={loading}
        messagesEndRef={messagesEndRef}
      />
      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
