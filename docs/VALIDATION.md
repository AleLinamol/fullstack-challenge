# Registro de validación

Validación y publicación: 6 de noviembre de 2026 (Argentina).

## Direcciones públicas

- Aplicación: https://jahi-chat.vercel.app
- Backend: https://jahi-chat-backend.onrender.com

## Comprobaciones locales

- Compilación de producción de Next.js 16.4.5 y TypeScript: correctos.
- ESLint: sin errores ni advertencias.
- Agent: 11 pruebas aprobadas, incluidos acceso no autorizado y ausencia de clave.
- Orchestrator: 20 pruebas aprobadas, incluida indisponibilidad temporal del Agent como HTTP 503. Advertencia heredada de Pydantic sobre `Field(example=...)`.
- Playwright: 8 pruebas aprobadas en escritorio y móvil. Incluyen integración real con ambos servicios, listas vacías, errores, recuperación durante el arranque y ausencia de reintentos en errores permanentes.
- Arranque conjunto mediante `deploy/start.py`: correcto. `/health` comprueba ambos servicios.
- Se corrigieron dos pruebas antiguas del Agent para reflejar el contrato existente de listas y listas vacías; ese contrato no cambió.

Reproducir la integración después de instalar dependencias y compilar el frontend:

```sh
# PowerShell
$env:COMBINED="1"
python scripts/verify_integration.py
```

En Linux/macOS: `COMBINED=1 python scripts/verify_integration.py`. Requiere puertos 8000, 8001 y 3000 disponibles y un navegador Playwright instalado.

## Construcción y publicación

- Render construyó correctamente `deploy/Dockerfile` en Linux y publicó ambos procesos en una instancia Free. Backend en revisión `e04f117`; Agent solo escucha en loopback.
- El primer build de Vercel detectó dos módulos omitidos de Git por una regla heredada `lib/`. Se corrigió `.gitignore` y se incluyeron `frontend/src/lib/chat.ts` y `send-chat.ts`.
- Vercel compiló y publicó correctamente la revisión `011a42a` desde un checkout remoto limpio. Se fijó Node.js 24.x.
- Producción usa `deploy-next`, sin modificar `main`. No se contrató ningún servicio pago.

## Pruebas públicas

Backend: seis comprobaciones HTTP correctas: `/health`, `usuario 2`, `buscar ana`, `lista 3`, `usuario 999` y `hola`.

Frontend: siete comprobaciones HTTP correctas sin cookies ni autenticación: página inicial HTTP 200, las cinco consultas anteriores mediante `/api/chat`, y rechazo de una consulta vacía con HTTP 400. El enlace público funciona sin cuenta de Vercel.

En el navegador se probaron ID, búsqueda, listado, lista vacía y mensaje no reconocido contra los servicios reales. Se revisaron capturas de escritorio y el diseño a 390 píxeles de ancho, sin desbordamiento horizontal. No se esperó un ciclo completo de suspensión de Render; la recuperación de arranque se comprobó mediante pruebas automatizadas de respuestas temporales.

## Límites vigentes

El backend puede tardar en despertar después de inactividad. No hay autenticación de usuarios finales ni persistencia: es una demo con datos estáticos. Los límites de los planes gratuitos se detallan en [DEPLOYMENT.md](DEPLOYMENT.md).
