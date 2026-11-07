# Nexo: propuesta visual

Nombre propuesto para la interfaz: **Nexo**. El nombre del repositorio, las direcciones y los servicios FastAPI se conservan.

## Diseño

Paisaje de lago y montañas al atardecer, paleta lavanda, panel translúcido con desenfoque, bordes suaves y tarjetas semitransparentes. Icono de marca y pictogramas creados directamente en SVG dentro de los componentes. El formulario conserva etiquetas accesibles, foco visible y estados de espera/error. Se respeta la preferencia de movimiento reducido.

## Imagen

- Generada con la herramienta integrada de ImageGen; no se usó la API ni un proveedor externo de fotografías.
- Archivo de la aplicación: `frontend/public/nexo-landscape.webp`.
- Dimensiones: 1672 × 941 píxeles; tamaño: 69.368 bytes.
- Se convirtió el PNG generado a WebP para reducir el peso de la página, sin cambiar la composición.

Prompt final:

> Use case: photorealistic-natural. Asset type: full-screen background image for an elegant translucent glass chat website. Create a beautiful tranquil alpine lake at dusk, layered distant mountain silhouettes, delicate wisps of mist and soft clouds, lavender and dusty rose sky transitioning to deep indigo, muted silver-blue reflections on still water. Cinematic fine art landscape photograph, sophisticated and peaceful, realistic textures. Wide landscape composition, horizon in lower middle, ample soft quiet sky, mountains toward the edges, visually calm center to sit behind a readable translucent interface. No people, buildings, lettering, UI, logos or watermark. The image should feel atmospheric and luminous, not neon or excessively dark. This is a background asset only, not a website mockup.

## Validación

Compilación de producción, TypeScript, ESLint y ocho pruebas de navegador correctos con el nuevo diseño. Se revisaron las capturas de escritorio y móvil con servicios FastAPI reales. El fondo se incluye como archivo local de la aplicación, sin dependencias de imágenes remotas.

Estado: propuesta preparada localmente para revisión visual antes de actualizar la demo pública.
