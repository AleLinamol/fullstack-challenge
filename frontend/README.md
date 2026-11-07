# Frontend

Next.js App Router + React + TypeScript estricto + Tailwind CSS 4.

- `src/app/page.tsx`: entrada de la página.
- `src/components/Chat.tsx`: conversación interactiva, formulario accesible, ejemplos y tarjetas responsive.
- `src/lib/chat.ts`: tipos y validación de respuestas externas.
- `src/app/api/chat/route.ts`: proxy de servidor con validación, timeout y errores controlados.

Configurar `ORCHESTRATOR_URL` en `.env` antes de iniciar. La variable se lee en el servidor; no requiere `NEXT_PUBLIC_`. El navegador solo llama a `/api/chat`, evitando CORS y direcciones locales incrustadas en producción.

Ver instalación, comandos y pruebas en el [README principal](../README.md).
