const usersMock = [
  {
    id: 1,
    name: "Ana Pérez",
    email: "ana@example.com",
    role: "admin",
    createdAt: "2024-01-15T10:00:00Z"
  },
  {
    id: 2,
    name: "Bruno Díaz",
    email: "bruno@elogia.tech",
    role: "viewer",
    createdAt: "2025-06-10T15:30:00Z"
  },
  {
    id: 3,
    name: "Carlos Gómez",
    email: "carlos@example.com",
    role: "editor",
    createdAt: "2024-03-22T14:30:00Z"
  },
  {
    id: 4,
    name: "Diana López",
    email: "diana.lopez@example.com",
    role: "viewer",
    createdAt: "2024-05-05T09:15:00Z"
  }
];

export async function mockSendMessage(text) {
  // Simular retardo para imitar llamada a backend
  await new Promise(resolve => setTimeout(resolve, 800));

  const lowerText = text.toLowerCase().trim();

  if (lowerText.startsWith('usuario ')) {
    // Obtener usuario por id
    const idStr = lowerText.split(' ')[1];
    const id = parseInt(idStr, 10);
    const user = usersMock.find(u => u.id === id);
    if (user) {
      return { result: user, error: null, examples: null };
    } else {
      return {
        result: null,
        error: `No se encontró usuario con id ${id}.`,
        examples: ["usuario 1", "usuario 2", "usuario 3"]
      };
    }
  } else if (lowerText.startsWith('buscar ')) {
    // Buscar usuarios por nombre o email
    const query = lowerText.slice(7).trim();
    const foundUsers = usersMock.filter(u =>
      u.name.toLowerCase().includes(query) || u.email.toLowerCase().includes(query)
    );
    if (foundUsers.length > 0) {
      return { result: foundUsers, error: null, examples: null };
    } else {
      return {
        result: null,
        error: `No se encontraron usuarios que coincidan con "${query}".`,
        examples: ["buscar ana", "buscar bruno", "buscar example.com"]
      };
    }
  } else if (lowerText.startsWith('listar')) {
    // Listar usuarios con parámetro opcional para cantidad
    const parts = lowerText.split(' ');
    let count = null;
    if (parts.length > 1) {
      const n = parseInt(parts[1], 10);
      if (!isNaN(n) && n > 0) count = n;
    }
    const result = count ? usersMock.slice(0, count) : usersMock;
    return { result, error: null, examples: null };
  } else if (lowerText === 'lista') {
    // Compatibilidad con "lista" para listar todos
    return { result: usersMock, error: null, examples: null };
  } else {
    // Error intención no reconocida
    return {
      result: null,
      error: "Intención no reconocida.",
      examples: [
        "usuario 2",
        "buscar ana",
        "listar",
        "listar 3"
      ]
    };
  }
}
