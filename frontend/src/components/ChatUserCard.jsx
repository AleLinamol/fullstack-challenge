import React from 'react';
import styles from './ChatUserCard.module.css';

function UserCards({ users }) {
  if (!users) return null;
  const usersArray = Array.isArray(users) ? users : [users];
  if (usersArray.length === 0) {
    return <div>No se encontraron usuarios.</div>;
  }
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
      {usersArray.map(user => (
        <div 
          key={user.id} 
          style={{ border: '1px solid #ccc', borderRadius: '8px', padding: '10px', width: '220px' }}
        >
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

export default function MessageBubble({ message }) {
  const isUser   = message.from === 'user';
  const isError  = !!message.error;

  let className = styles.messageBubble;
  if (isError) className += ` ${styles.error}`;
  else className += isUser ? ` ${styles.user}` : ` ${styles.system}`;

  return (
    <div className={className}>
      {isError ? (
        <>
          <div><strong>Error:</strong> {message.error}</div>
          {message.examples && (
            <div className={styles.messageErrorExamples}>
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
