# Preparación del despliegue público

Estado: configuración preparada localmente. No se publicaron cambios ni se creó infraestructura.

## Topología

- Frontend: servicio Node compatible con Next.js (por ejemplo Vercel), directorio raíz `frontend`, instalación `pnpm install --frozen-lockfile`, build `pnpm build` y arranque `pnpm start` si el proveedor lo solicita.
- Agent y Orchestrator: dos servicios Docker independientes usando sus respectivas carpetas `backend/agent` y `backend/orchestrator` como contexto de construcción. Los Dockerfiles respetan `PORT` del proveedor.
- Preferir red privada entre backends. Si el Agent es público, usar HTTPS y una clave aleatoria larga. No exponer la clave al navegador.

## Orden y variables

1. Crear Agent y configurar un secreto `AGENT_KEY`.
2. Crear Orchestrator con el mismo `AGENT_KEY` y `AGENT_URL` apuntando al endpoint `/rpc` del Agent.
3. Crear frontend y configurar `ORCHESTRATOR_URL` con el origen del Orchestrator, sin `/chat` final.
4. Reiniciar los servicios después de cambiar variables. No es necesario ampliar CORS: las peticiones al Orchestrator se hacen desde el servidor Next.
5. Verificar en la URL pública búsqueda, listado, usuario inexistente, error de intención, móvil y recuperación si el backend se suspende.

No hay un plan o proveedor contratado. Revisar disponibilidad, costos, suspensión por inactividad y límites vigentes antes de crear los servicios. Si un plan suspende los backends, el primer acceso puede requerir reintentar.

## Autorización pendiente

Antes de hacer push, abrir PR o desplegar: revisar el diff y resultados de pruebas, elegir el proveedor/cuenta y autorizar explícitamente la publicación y la creación de servicios. Los tres servicios son necesarios para una demo real; no sustituir silenciosamente FastAPI por respuestas simuladas.

## Reversión

Conservar la revisión actual del repositorio antes de publicar. Si la verificación pública falla, volver el frontend y los backends a esa revisión y a sus variables anteriores; no borrar servicios hasta confirmar recuperación.
