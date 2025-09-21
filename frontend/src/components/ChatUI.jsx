import React, { useState } from 'react';
import { mockSendMessage } from '../../mocks/chatMock';
import './ChatUI.css';

function MessageBubble({ message }) {
  const isUser   = message.from === 'user';
  const isError = !!message.error;
  let className = 'message-bubble ';
  if (isError) className += 'error';
  else className += isUser  ? 'user' : 'system';
  return (
    <div className={className}>
      {isError ? (
        <>
          <div><strong>Error:</strong> {message.error}</div>
          {message.examples && (
            <div className="message-error-examples">
              Ejemplos: {message.examples.join(', ')}
            </div>
          )}
        </>
      ) : message.data ? (
        Array.isArray(message.data) ? (
          <UserCards users={message.data} />
        ) : (
          <UserCards users={[message.data]} />
        )
      ) : (
        <div>{message.text}</div>
      )}
    </div>
  );
}

function UserCards({ users }) {
  if (!users) return null;
  const usersArray = Array.isArray(users) ? users : [users];
  if (usersArray.length === 0) {
    return <div>No se encontraron usuarios.</div>;
  }
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
      {usersArray.map(user => (
        <div key={user.id} style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '10px', width: '220px' }}>
          <div><strong>ID:</strong> {user.id}</div>
          <div><strong>Nombre:</strong> {user.name}</div>
          <div><strong>Email:</strong> {user.email}</div>
          <div><strong>Rol:</strong> {user.role}</div>
          <div><small>Creado: {new Date(user.createdAt).toLocaleDateString()}</small></div>
        </div>
      ))}
    </div>
  );
}

function MessageInput({ onSend, disabled }) {
  const [text, setText] = React.useState('');
  const handleSend = () => {
    if (text.trim()) {
      onSend(text.trim());
      setText('');
    }
  };
  return (
    <div className="message-input-container">
      <input
        type="text"
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleSend()}
        disabled={disabled}
        placeholder="Escribe un mensaje..."
        className="message-input"
      />
      <button
        onClick={handleSend}
        disabled={disabled}
        className="send-button"
      >
        Enviar
      </button>
    </div>
  );
}


export default function ChatUI() {
    const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
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
    <div className="chat-container">
      <h2>Chat de Usuarios (Mock)</h2>
      <div className="messages-container">
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        {loading && <div>Cargando...</div>}
      </div>
      <MessageInput onSend={sendMessage} disabled={loading} />
    </div>
  );
}