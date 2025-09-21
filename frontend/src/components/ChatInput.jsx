import React, { useState } from 'react';
import styles from './ChatInput.module.css';

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState('');

  const handleSend = () => {
    if (text.trim()) {
      onSend(text.trim());
      setText('');
    }
  };

  return (
    <div className={styles.messageInputContainer}>
      <input
        type="text"
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
        disabled={disabled}
        placeholder="Escribe un mensaje..."
        className={styles.messageInput}
      />
      <button
        onClick={handleSend}
        disabled={disabled}
        className={styles.sendButton}
      >
        Enviar
      </button>
    </div>
  );
}
