# Fullstack Challenge — Jahi

Chat de usuarios con **Next.js App Router, React, TypeScript y Tailwind CSS**. Conserva los servicios **Orchestrator y Agent en Python/FastAPI** y su contrato REST/JSON-RPC.

```text
Navegador → Next.js /api/chat → Orchestrator /chat → Agent /rpc → seed.json
```

## Ejecutar localmente

Requisitos: Node.js 20.9 o superior, pnpm 11 y Python 3.13. Ejecutar desde la raíz del repositorio:

```sh
python -m venv .venv
# Activar: Windows .venv\Scripts\Activate.ps1; Linux/macOS source .venv/bin/activate
python -m pip install -r backend/agent/requirements.txt -r backend/orchestrator/requirements.txt
```

Copiar los tres archivos `.env.example` a `.env` en sus respectivas carpetas. Usar el mismo `AGENT_KEY` en ambos servicios. Es un secreto entre servidores: nunca incluirlo en el frontend ni en Git.

En tres terminales, con el entorno Python activado donde corresponda:

```sh
cd backend/agent
uvicorn app.main:app --reload --port 8001
```

```sh
cd backend/orchestrator
uvicorn app.main:app --reload --port 8000
```

```sh
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

Abrir http://localhost:3000 y probar `usuario 2`, `buscar ana`, `lista 3`, `usuario 999` y un mensaje no reconocido.

## Verificación

Cada backend usa un paquete llamado `app`: ejecutar las suites por separado, desde cada carpeta, con `AGENT_KEY` configurado. Para Orchestrator configurar también `AGENT_URL`.

```sh
python -m pytest tests -q
```

Frontend, desde `frontend/`:

```sh
pnpm lint
pnpm typecheck
pnpm build
pnpm exec playwright install chromium
pnpm test
```

Las pruebas de navegador verifican escritorio y móvil: consultas, errores, listas vacías y recuperación. Con los servicios reales iniciados y `ORCHESTRATOR_URL` configurada, ejecutar `INTEGRATION=1 pnpm test` (PowerShell: `$env:INTEGRATION="1"; pnpm test`).

## Alojamiento gratuito

La configuración `render.yaml` prepara una instancia Render Free con ambos servicios FastAPI. El frontend se prepara para Vercel Hobby. La primera consulta espera y reintenta mientras el backend despierta. Ver la [guía de despliegue](docs/DEPLOYMENT.md). No se creó infraestructura pública.

## Documentación

- [Decisiones de migración](docs/MIGRATION.md)
- [Preparación del despliegue](docs/DEPLOYMENT.md)
- [Resultados de pruebas](docs/VALIDATION.md)
- [Frontend](frontend/README.md)
- [Agent](backend/agent/README.md)
- [Orchestrator](backend/orchestrator/README.md)
