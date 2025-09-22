# _Fullstack Challenge_

# Chat UI - Frontend

Este componente corresponde a la interfaz de usuario del sistema. Está desarrollado con **React + Vite** y consume los endpoints expuestos por los demás servicios (`agent` y `orchestrator`).

---

## Instalación y ejecución

Clonar el repositorio y acceder a la carpeta del frontend:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Ejecutar en modo desarrollo:

```bash
npm run dev
```

La aplicación quedará disponible en:  
 [http://localhost:5173](http://localhost:5173)

---

##  Estructura principal

```
frontend/
├── mocks/                        # Carpeta con datos simulados (mock) para pruebas
├── node_modules/                 # Dependencias instaladas por npm
├── public/                       # Archivos estáticos accesibles directamente
│   └── bg.jpg                    # Imagen de fondo usada en el chat
├── src/                          # Código fuente principal
│   ├── assets/                   # Carpeta opcional para otros recursos (imágenes, íconos, etc.)
│   ├── components/               # Componentes React del chat
│   │   ├── ChatInput.jsx         # Componente para el input de mensajes + botón de enviar
│   │   ├── ChatInput.module.css  # Estilos del input y botón (CSS Modules)
│   │   ├── ChatUI.jsx            # Componente principal del chat (estructura general)
│   │   ├── ChatUI.module.css     # Estilos principales del chat (contenedor, responsive, etc.)
│   │   ├── ChatUserCard.jsx      # Componente que muestra información de un usuario (tarjeta)
│   │   ├── ChatUserCard.module.css # Estilos de las tarjetas de usuario
│   │   ├── ChatUsersList.jsx     # Lista de usuarios renderizada dentro del chat
│   │   └── ChatUsersList.module.css # Estilos de la lista de usuarios
│   ├── App.jsx                   # Componente raíz de la aplicación, renderiza el ChatUI
│   │
│   └── index.css                 # Estilos globales de la aplicación
└── 

```

---

##  Interfaz

El frontend implementa una **UI de chat** que permite la interacción con el sistema:  

- Visualización de mensajes enviados y recibidos.  
- Diferenciación entre **mensajes de usuario**, **mensajes del sistema** y **errores**.  
- Entrada de texto y botón de envío.  
- Diseño responsive, adaptado para escritorio, tablets y móviles.  

---

##  Configuración

El frontend se conecta al servicio backend a través de una URL configurable.  
Por defecto, esta se encuentra en el archivo:

```
src/config.js
```

Ejemplo:

```js
export const API_URL = "http://localhost:8000/chat";
```

---

## Build

Para generar la versión de producción:

```bash
npm run build
```

Esto creará la carpeta `dist/` lista para ser servida por un servidor estático.  
