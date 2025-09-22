# _Fullstack Challenge_

Este proyecto corresponde a un **challenge fullstack** que integra dos servicios backend (Agent y Orchestrator) y un frontend en React (Chat UI).  
El objetivo es demostrar habilidades en desarrollo de APIs, comunicación entre servicios y construcción de interfaces de usuario.

---

## 🧩 Arquitectura general

```
[Frontend Chat UI]  →  [Orchestrator (FastAPI)]  →  [Agent (FastAPI JSON-RPC)]
```

- **Agent**: servicio JSON-RPC para consulta de usuarios desde un dataset estático.  
- **Orchestrator**: servicio REST que interpreta lenguaje natural y consulta al Agent.  
- **Chat UI**: interfaz de chat en React que consume el Orchestrator.  

📖 Documentación detallada:  
- [Agent README](./agent/README.md)  
- [Orchestrator README](./orchestrator/README.md)  
- [Frontend README](./frontend/README.md)  

---

## ⚙️ Requisitos generales

- Python 3.8+  
- Node.js 18+  
- npm o yarn  
- uvicorn, FastAPI, pytest, respx  

---

## 🚀 Instalación y ejecución

### 1. Agent (backend JSON-RPC)

```bash
cd agent
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Servicio disponible en: [http://localhost:8001/rpc](http://localhost:8001/rpc)

Ejemplo con curl en Linux:

```bash
curl -X POST http://localhost:8001/rpc   -H "Content-Type: application/json"   -H "X-Agent-Key: challenge-token-123"   -d '{
    "jsonrpc": "2.0",
    "method": "search_users",
    "params": { "query": "ana" },
    "id": 1
  }'
```

Ejemplo con curl en Windows:

```bash
$body = @'
{
    "jsonrpc": "2.0",
    "method": "search_users",
    "params": { "query": "ana" },
    "id": 1
}
'@

Invoke-WebRequest -Uri "http://localhost:8001/rpc" -Method POST -Headers @{ "Content-Type" = "application/json"; "X-Agent-Key" = "challenge-token-123" } -Body $body
```

---

### 2. Orchestrator (backend FastAPI)

```bash
cd orchestrator
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Servicio disponible en: [http://localhost:8000/chat](http://localhost:8000/chat)

Ejemplo con curl en Linux:

```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d '{ "message": "usuario 2" }'
```

Ejemplo con curl en Windows:

```bash
Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "usuario 2"}'
```
 
---

### 3. Chat UI (frontend React)

```bash
cd frontend
npm install
npm run dev
```

Interfaz disponible en: [http://localhost:5173](http://localhost:5173)

---

## 📂 Estructura del proyecto

```
fullstack-challenge/
├── agent/          # Backend JSON-RPC (usuarios)
├── orchestrator/   # Backend REST (intérprete de mensajes)
├── frontend/       # Chat UI en React
└── README.md       # Documentación general (este archivo)
```

---

## ✅ Tests

- **Agent**: `pytest tests/`  
- **Orchestrator**: `pytest tests/` (requiere `respx`)  

---

## ✨ Funcionalidades destacadas

- **Agent**: búsqueda y listado de usuarios vía JSON-RPC.  
- **Orchestrator**: parser de lenguaje natural → llamadas al Agent.  
- **Chat UI**: interfaz tipo chat responsive para interactuar con el sistema.  
