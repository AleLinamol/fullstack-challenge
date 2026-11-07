# Despliegue gratuito: Vercel + Render

## Configuración preparada

Frontend Next.js en Vercel Hobby. Agent y Orchestrator conservan sus aplicaciones independientes y corren como dos procesos en una sola instancia Render Free. Esto comparte el arranque y utiliza horas de una instancia; no mantiene dos servicios despiertos consumiendo el cupo compartido por separado.

El Agent escucha exclusivamente en `127.0.0.1:8001`; el Orchestrator escucha en el puerto público asignado por Render. `deploy/start.py` supervisa los procesos y detiene ambos si uno falla. Los Dockerfiles individuales siguen disponibles para desplegarlos por separado.

## Render

1. Conectar la cuenta GitHub y crear un Blueprint desde este repositorio, usando la rama `migration/next-typescript-tailwind` y `render.yaml`.
2. Revisar que el único servicio, `jahi-chat-backend`, tenga plan **Free** y costo de cómputo **$0**. No seleccionar servicios pagos ni agregar una base de datos.
3. El Blueprint genera `AGENT_KEY`; no copiar esa clave al frontend. `AGENT_URL` se establece internamente en loopback al iniciar.
4. Render construye `deploy/Dockerfile` desde la raíz del repositorio y comprueba `/health`, que también verifica el Agent.
5. Guardar la URL HTTPS del backend. Los despliegues automáticos están desactivados para controlar futuras publicaciones. Si el proveedor requiere otro nombre por disponibilidad, se puede cambiar sin modificar los contratos.

## Vercel

1. Usar cuenta personal **Hobby**, importar el mismo repositorio y seleccionar la rama `deploy-next` para la demo.
2. Directorio raíz: `frontend`. Framework: Next.js. Instalación: `pnpm install --frozen-lockfile`; compilación: `pnpm build`. El repositorio fija pnpm 11.25.0.
3. Configurar `ORCHESTRATOR_URL` con el origen HTTPS de Render, sin `/chat` final. Aplicar al entorno que se despliegue (Preview o Production).
4. Desplegar y verificar la dirección gratuita `vercel.app`. No se necesita dominio propio.
5. Si el proyecto se vincula antes de fusionar la PR, revisar que la vista previa use `deploy-next`. Cambiar la rama de producción a `main` solamente después de fusionar los cambios y confirmar cuál es la rama principal del repositorio.

## Arranque después de inactividad

Render Free suspende la instancia después de 15 minutos sin tráfico. El navegador vuelve a enviar solamente consultas marcadas como temporalmente no disponibles, hasta 15 intentos. Cada petición tiene un máximo de 10 segundos hacia Render y cada reintento espera 2 segundos: el intento completo puede tardar unos 3 minutos. La interfaz avisa durante la espera y libera el formulario si no se recupera. Consultar usuarios es una operación de lectura; no aplicar este patrón automáticamente a operaciones con efectos secundarios.

Cada función Next tiene `maxDuration = 15`, sin mantener una invocación abierta durante todo el despertar. No se usan pings periódicos para evitar la suspensión.

## Límites y costo

Render concede 750 horas de instancia gratuitas por espacio de trabajo al mes, compartidas con otros servicios que ya existan. Hay además límites de transferencia y compilaciones. Vercel Hobby se destina a proyectos personales no comerciales. Mantener ambos planes gratuitos y revisar el consumo; no se contrató ningún servicio pago.

Fuentes oficiales verificadas:
- https://render.com/docs/free
- https://render.com/docs/blueprint-spec
- https://vercel.com/docs/plans
- https://vercel.com/docs/functions/configuring-functions/duration

## Validación pública pendiente

Probar `/health`, consulta por ID, búsqueda, listado, usuario inexistente, mensaje no reconocido y recuperación después de inactividad desde escritorio y móvil. No declarar un despliegue terminado hasta verificar ambas URLs. Si falla, volver a la revisión anterior desde el proveedor sin borrar los servicios.


## Instancia creada

Backend activo en https://jahi-chat-backend.onrender.com, servicio `jahi-chat-backend`, plan Free, región Oregon. Creado mediante importación pública del repositorio con los mismos valores del Blueprint: rama de migración, `deploy/Dockerfile`, contexto raíz, comprobación `/health` y despliegue automático desactivado. La clave se generó en Render y no se guarda en el repositorio. Para Vercel, usar `ORCHESTRATOR_URL=https://jahi-chat-backend.onrender.com`.


## Frontend publicado

- Demo: https://jahi-chat.vercel.app
- Cuenta: AleLinamol, Vercel Hobby.
- Proyecto: `jahi-chat`; raíz `frontend`; framework Next.js; Node.js 24.x.
- Rama de producción: `deploy-next`, creada desde la migración para evitar el problema del importador con nombres de rama que contienen `/`.
- Revisión publicada: `011a42a`. Despliegue: `dpl_D1E1hbHNpuoiwSbdz3RAnrnvJCBD`.
- `ORCHESTRATOR_URL` configurada para Production y Preview.
- GitHub está vinculado y los pushes a `deploy-next` generan despliegues de producción. Los cambios en otras ramas generan vistas previas.
- La rama `main` no se modificó ni se fusionó automáticamente. Antes de cambiar la rama de producción a `main`, fusionar la PR y verificar esa revisión.
- La documentación posterior se publica en la rama de migración; no se vuelve a desplegar producción por cambios solamente documentales de esta tarea.
