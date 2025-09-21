# _Fullstack Challenge_

# Orchestrator - Backend FastAPI Service

## Descripción

**Orchestrator** es un servicio backend implementado con FastAPI que expone un endpoint `/chat`.  
Este servicio interpreta mensajes en lenguaje natural mediante un parser de intenciones y se comunica con un agente externo vía JSON-RPC para obtener datos de usuarios.  

---

## Características principales

- Endpoint REST en `/chat` (método POST).
- Parser de intención que interpreta comandos:
  - `usuario <id>` → obtiene un usuario por ID.
  - `buscar <query>` → busca usuarios por nombre o email.
  - `lista <n>`, `últimos <n>`, `show <n>` → lista los últimos N usuarios.
- Comunicación con un agente externo vía JSON-RPC sobre HTTP.
- Autenticación mediante header `X-Agent-Key` al comunicarse con el agente.
- Manejo de errores claros y respuestas limpias hacia el frontend.
- Incluye tests unitarios del parser y de la integración con el agente (mock HTTP).

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

3. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (puedes ajustar los valores):

```bash
AGENT_KEY=challenge-token-123
AGENT_URL=http://localhost:8001/rpc
```

---

## Estructura del proyecto

```
orchestrator/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app y endpoint /chat
│   ├── config.py           # Configuración y variables de entorno
│   ├── errors.py           # Manejo de errores y excepciones
│   ├── intent_parser.py    # Parser regex para interpretar mensajes
│   ├── jsonrpc_client.py   # Cliente HTTP JSON-RPC para comunicarse con el Agent
│   └── mocks/
│       └── agent_mock.py   # Mock del Agent para pruebas locales
├── tests/
│   ├── test_main.py        # Tests del endpoint /chat
│   ├── test_intent_parser.py # Tests unitarios del parser de intención
│   └── test_jsonrpc_client.py # Tests de la comunicación JSON-RPC (mock)
├── .env                    # Variables de entorno (ignorar en git)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```

---

## Cómo ejecutar el servidor

Desde la raíz del proyecto, ejecuta:

```bash
uvicorn app.main:app --reload --port 8000
```

El servidor quedará disponible en: [http://localhost:8000](http://localhost:8000)

---

## Cómo usar el endpoint `/chat`

- **URL**: `http://localhost:8000/chat`
- **Método**: POST  
- **Headers**:
  - `Content-Type: application/json`

### Ejemplo de petición

```json
{
  "message": "usuario 2"
}
```

---

## Ejemplo de respuesta exitosa

```json
{
    "result": {
        "id": 2,
        "name": "Bruno Díaz",
        "email": "bruno@elogia.tech",
        "role": "viewer",
        "createdAt": "2025-06-10T15:30:00Z"
    },
    "error": null,
    "examples": null
}
```

---

## Manejo de errores

El servicio responde con mensajes de error en formato JSON:

- **Intención desconocida**:  
  ```json
  { "error": "No entiendo. Ejemplos: 'usuario 2', 'buscar ana', 'lista 3'" }
  ```
- **Error de comunicación con el Agent**: status HTTP y detalle de error.
- **Errores JSON-RPC** propagados desde el Agent:
  - `-32601`: Método no encontrado.
  - `-32602`: Parámetros inválidos.

---

## Tests Unitarios

El proyecto incluye tests unitarios y de integración en la carpeta `tests/`.

---

### Estructura de tests

```
tests/
 ├── test_main.py            # Tests del endpoint /chat
 ├── test_intent_parser.py   # Tests del parser
 └── test_jsonrpc_client.py  # Tests de integración con mock HTTP
```

---

### Requisitos para ejecutar tests

- Tener instalado `pytest` y `respx`:

```bash
pip install pytest respx
```

- Estar en la raíz del proyecto `orchestrator/`.

---

### Cómo ejecutar los tests

```bash
pytest tests/
```

---

### Qué verifican los tests

- **test_intent_parser.py**: reconoce patrones de usuario, búsqueda y listado.  
- **test_jsonrpc_client.py**: valida la comunicación con el Agent usando mock HTTP.  
- **test_main.py**: asegura que `/chat` responda correctamente en escenarios válidos y de error.  
