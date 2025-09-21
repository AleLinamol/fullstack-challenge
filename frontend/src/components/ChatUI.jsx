import React, { useState, useEffect, useRef } from 'react';
import { mockSendMessage } from '../../mocks/chatMock';
import ChatUsersList from './ChatUsersList';
import ChatInput from './ChatInput';
import styles from './ChatUI.module.css';

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
    setMessages(prev => [...prev, { from: 'user', text }]);
    setLoading(true);
    try {
      const data = await mockSendMessage(text);
      if (data.error) {
        setMessages(prev => [...prev, { from: 'system', error: data.error, examples: data.examples }]);
      } else {
        setMessages(prev => [...prev, { from: 'system', data: data.result }]);
      }
    } catch {
      setMessages(prev => [...prev, { from: 'system', error: 'Error inesperado en el mock.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatContainer}>
      <h2 className={styles.title}>Chat de Usuarios (Mock)</h2>
      
      <ChatUsersList 
        messages={messages} 
        loading={loading} 
        messagesEndRef={messagesEndRef} 
      />

      <ChatInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}
