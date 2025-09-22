import React, { useState, useEffect, useRef } from "react";
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

  const sendMessage = async (text) => {
    setMessages((prev) => [...prev, { from: "user", text }]);
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }), 
      });

      // Siempre parseamos el JSON, incluso si no es ok (para leer errores del backend)
      let data;
      try {
        data = await response.json();
        // Log para debug: mira la consola para ver qué devuelve exactamente
        console.log("Respuesta del backend:", data);
        console.log("Status code:", response.status);
      } catch (parseError) {
        // Si no se puede parsear JSON (respuesta inválida), tratamos como error genérico
        console.error("Error parseando JSON:", parseError);
        throw new Error(`Respuesta inválida del servidor: ${response.status} ${response.statusText}`);
      }

      // Manejo de errores: chequea múltiples formatos comunes (error, detail, message)
      let errorMessage = data.error || data.detail || data.message || null;

      // Limpieza específica para JSON-RPC: remueve el prefijo "JSON-RPC Error -XXXXX: "
      if (errorMessage && typeof errorMessage === 'string' && errorMessage.startsWith('JSON-RPC Error')) {
        // Extrae solo el mensaje después del prefijo
        errorMessage = errorMessage.split('JSON-RPC Error')[1]?.trim().replace(/^-?\d+:\s*/, '') || errorMessage;
        console.log("Mensaje de error limpio:", errorMessage);
      }

      if (errorMessage) {
        // Es un error: muestra como burbuja de error
        setMessages((prev) => [
          ...prev,
          { 
            from: "system", 
            error: errorMessage, 
            examples: data.examples || data.suggestions || null
          },
        ]);
      } else if (data.result !== undefined) {
        // Éxito: usa data.result para UserCards
        // NUEVO: Si hay data.message, agrégalo como texto informativo (no error)
        const systemMessage = {
          from: "system",
          data: data.result  // Para mostrar UserCards (vacía o no)
        };
        if (data.message) {
          systemMessage.text = data.message;  // Muestra el mensaje como texto normal
        }
        setMessages((prev) => [...prev, systemMessage]);
      } else {
        // Respuesta inesperada
        console.warn("Respuesta inesperada del backend:", data);
        setMessages((prev) => [
          ...prev,
          { from: "system", error: "Respuesta inesperada del servidor. Verifica los logs." },
        ]);
      }

    } catch (error) {
      // Errores de red o parseo: mensaje genérico
      console.error("Error en fetch:", error);
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
      <h1 className={styles.title}>- Fullstack Challenge-</h1>
       <h2 className={styles.subtitle}>Chat de Usuarios</h2>

      <ChatUsersList
        messages={messages}
        loading={loading}
        messagesEndRef={messagesEndRef}
      />
      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
