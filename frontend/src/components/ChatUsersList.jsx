import React from 'react';
import MessageBubble from './ChatUserCard';
import styles from './ChatUsersList.module.css';

export default function ChatUsersList({ messages, loading, messagesEndRef }) {
  return (
    <div className={styles.messagesContainer}>
      {messages.map((msg, idx) => (
        <MessageBubble key={idx} message={msg} />
      ))}
      {loading && <div>Cargando...</div>}
      <div ref={messagesEndRef} />
    </div>
  );
}
