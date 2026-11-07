# Registro de validación

Validación local: 6 de noviembre de 2026 (Argentina).

## Resultados

- Next.js 16.4.5: compilación de producción correcta, incluida comprobación TypeScript.
- ESLint: sin errores ni advertencias después de corregir la navegación con Link.
- TypeScript: `tsc --noEmit` sin errores.
- Agent: **11 pruebas aprobadas**, incluidos acceso no autorizado y ausencia de clave.
- Orchestrator: **19 pruebas aprobadas**. Advertencia preexistente de Pydantic sobre `Field(example=...)`.
- Playwright/Chromium: **4 pruebas aprobadas** en escritorio y móvil. Dos verifican respuestas simuladas para escenarios de error; dos consultan realmente Next.js → Orchestrator → Agent.
- Integración real: consultas `usuario 2`, `buscar ana`, `lista 3` y rechazo de entrada vacía por el proxy.
- Revisión visual de capturas en escritorio y móvil. Sin desbordamiento horizontal en los escenarios automatizados.
- `git diff --check`: correcto.

Se actualizaron dos pruebas antiguas del Agent que esperaban un objeto/None; la implementación existente entrega listas y listas vacías. No se modificó ese contrato para hacer pasar las pruebas.

## Reproducir integración

Instalar dependencias Python en `.venv`, instalar frontend y navegador, compilar frontend y ejecutar desde la raíz:

```sh
python scripts/verify_integration.py
```

El script inicia ambos backends con una clave exclusiva de prueba y usa el frontend de producción mediante Playwright. Libera sus procesos de backend al terminar. Requiere puertos 8000, 8001 y 3000 disponibles; no reutilizar un frontend ajeno durante esta verificación.

## Pendiente de infraestructura pública

No se construyeron imágenes Docker ni se verificó un proveedor remoto. Las configuraciones de despliegue necesitan validación en el proveedor elegido. No se hizo push, PR ni despliegue. La demo pública y sus costos requieren autorización y elección de cuenta.


## Actualización para alojamiento gratuito

- Compilación de producción y TypeScript: correctos.
- ESLint: correcto.
- Orchestrator: **20 pruebas aprobadas**, incluida indisponibilidad temporal del Agent como HTTP 503.
- Playwright: **8 pruebas aprobadas** en escritorio y móvil, incluidas recuperación tras arranque y ausencia de reintentos en errores permanentes.
- Arranque conjunto mediante `deploy/start.py`: correcto; `/health` comprueba ambos servicios y las consultas reales atravesaron toda la cadena.
- Reproducción: PowerShell `$env:COMBINED="1"; python scripts/verify_integration.py`; Linux/macOS `COMBINED=1 python scripts/verify_integration.py`.
- La construcción Docker no se pudo ejecutar porque Docker Desktop no tenía un motor activo. La imagen se verificará en el primer build de Render.
- Aún no se crearon servicios públicos; faltan las conexiones a las cuentas de Vercel y Render.


## Backend público en Render Free

Desplegado el 6 de noviembre de 2026 desde `e04f117`.

- URL: https://jahi-chat-backend.onrender.com
- Salud: `/health` devolvió `{"status":"ok"}`.
- Consultas reales verificadas: `usuario 2`, `buscar ana`, `lista 3`, `usuario 999` y `hola`.
- Seis comprobaciones HTTP correctas; la construcción Docker y el arranque público fueron exitosos en Render.
- Agent permanece en loopback; solamente Orchestrator recibe tráfico público.
- Frontend público pendiente de importación y despliegue en Vercel.
