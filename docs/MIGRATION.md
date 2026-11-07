# Migración de Vite a Next.js

## Qué cambió

- Vite y sus entradas JavaScript fueron reemplazados por Next.js App Router.
- Componentes y contratos convertidos a TypeScript estricto; las respuestas HTTP se validan antes de renderizarlas.
- Los módulos CSS fueron reemplazados por utilidades Tailwind 4 con PostCSS según la guía oficial: https://tailwindcss.com/docs/installation/framework-guides/nextjs
- La interacción usa un componente cliente; layout y página permanecen como componentes de servidor.
- El navegador llama a una ruta de servidor de Next.js; `ORCHESTRATOR_URL` sustituye la URL local fija. Agent y Orchestrator siguen siendo servicios independientes.
- Se corrigió el tratamiento de `error: null`, resultados vacíos, errores de validación estructurados y mensajes informativos junto a resultados.
- El formulario bloquea solicitudes simultáneas, admite Enter, limita consultas a 500 caracteres y expone estados accesibles de carga.
- Se corrigió el fallo de arranque del Orchestrator sin `AGENT_KEY` y el Agent ahora rechaza solicitudes cuando su clave no está configurada.

## Cómo explicarlo en una entrevista

El chat conserva React para la interacción. Next.js aporta el enrutamiento y un punto de acceso del mismo origen que el navegador. TypeScript describe los datos durante el desarrollo y la validación en ejecución comprueba las respuestas externas. Tailwind permite aplicar diseño responsive sin módulos CSS separados. La lógica de búsqueda y el protocolo JSON-RPC permanecen en Python.

## Límites

Es una demostración con datos estáticos, sin autenticación de usuarios finales, persistencia ni LLM. El proxy no convierte automáticamente el servicio público en una API privada. Antes de habilitar tráfico amplio, configurar límites de solicitudes en el proveedor y revisar los datos de demostración. No afirmar un despliegue público hasta tener la URL y verificarla.

## Fuentes y comprobaciones

- Next.js App Router: https://nextjs.org/docs/app/getting-started/installation
- [Resultados de validación local](VALIDATION.md)
