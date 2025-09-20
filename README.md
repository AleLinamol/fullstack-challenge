# Fullstack-challenge

# Agent - Backend JSON-RPC Service

## Descripción

**Agent** es un servicio backend implementado con FastAPI que expone un endpoint JSON-RPC para consultar datos de usuarios. Los datos se cargan desde un archivo estático `seed.json`. El servicio valida un header personalizado para autorizar las peticiones y soporta métodos para obtener usuarios por ID, buscar usuarios por nombre y listar todos los usuarios.

---

## Características principales

- Endpoint JSON-RPC 2.0 en `/rpc` (método POST).
- Autenticación mediante header `X-Agent-Key`.
- Métodos soportados:
  - `get_user`: obtener usuario por ID.
  - `search_users`: buscar usuarios por nombre (búsqueda parcial, case insensitive).
  - `list_users`: listar todos los usuarios.
- Manejo de errores JSON-RPC estándar.
- Modularizado para facilitar mantenimiento y extensión.

---

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

---

## Instalación

1. Clona el repositorio o descarga el código.

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

3. Crea un archivo `.env` en la raíz del proyecto con la siguiente variable (puedes cambiar el valor):

```bash
AGENT_KEY=challenge-token-123
```

---

## Estructura del proyecto

```
agent/
 ├── app/
 │    ├── main.py           # Servidor FastAPI y endpoint /rpc
 │    ├── config.py         # Configuración y variables de entorno
 │    ├── data_loader.py    # Carga y consulta de datos de usuarios
 │    ├── errors.py         # Manejo de errores JSON-RPC
 │    ├── rpc_handlers.py   # Implementación de métodos JSON-RPC
 │    ├── seed.json         # Datos estáticos de usuarios
 │    └── __init__.py       # Paquete Python vacío
 ├── requirements.txt       # Dependencias del proyecto
 └── README.md              # Este archivo
```

---

## Cómo ejecutar el servidor

Desde la raíz del proyecto, ejecuta:

```bash
uvicorn app.main:app --reload --port 8001
```

El servidor quedará disponible en: [http://localhost:8001](http://localhost:8001)

---

## Cómo usar el endpoint /rpc

- **URL**: `http://localhost:8001/rpc`
- **Método**: POST  
- **Headers**:
  - `Content-Type: application/json`
  - `X-Agent-Key: <valor de AGENT_KEY en .env>`

### Ejemplo de petición

```json
{
  "jsonrpc": "2.0",
  "method": "search_users",
  "params": { "query": "ana" },
  "id": 1
}
```

---

## Métodos disponibles

### `get_user`
- **Parámetros**: `{ "id": <int> }`
- **Descripción**: Obtiene un usuario por su ID.

### `search_users`
- **Parámetros**: `{ "query": "<string>" }`
- **Descripción**: Busca usuarios cuyo nombre contiene la cadena (case insensitive).

### `list_users`
- **Parámetros**: No requiere
- **Descripción**: Devuelve la lista completa de usuarios.

---

## Ejemplo de respuesta exitosa

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": [
        {
            "id": 1,
            "name": "Ana López",
            "email": "ana@elogia.tech",
            "role": "admin",
            "createdAt": "2025-05-01T10:00:00Z"
        }
    ]
}
```

---

## Manejo de errores

El servicio responde con errores JSON-RPC estándar, por ejemplo:

- **Código -32600**: Petición inválida.
- **Código -32601**: Método no encontrado.
- **Código -32602**: Parámetros inválidos.
- **Código -32700**: Error de parseo JSON.

---

## Notas adicionales

- Puedes modificar el archivo `seed.json` para cambiar los datos de usuarios.
- El proyecto está modularizado para facilitar la extensión y mantenimiento.
