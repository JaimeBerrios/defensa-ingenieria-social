# Organización del repositorio

| Carpeta | Qué contiene |
|---|---|
| `datos/` | Única fuente de metadatos, integrantes, consigna y bibliografía. |
| `documentos/` | Contenido LaTeX, fragmentos y anexos editables. |
| `plantilla/latex/` | Estilos reutilizables; no guardar contenido de un trabajo aquí. |
| `web/portal/` | CSS y JavaScript del portal de la raíz. |
| `web/presentacion/` | Diapositivas HTML, tema, estilos propios e interacciones. |
| `assets/institucional/` | Logos y acreditación originales; conservar proporciones. |
| `assets/fuentes/` | Fuentes locales, incluida la firma original. |
| `assets/iconos/fontawesome/` | SVG oficiales y licencia de la selección de iconos. |
| `assets/contenido/` | Imágenes, gráficos y evidencias del trabajo. |
| `herramientas/` | Implementación Python; `compilar.py` sigue siendo la entrada única. |
| `vendor/` | Reveal.js, Bootstrap y Font Awesome locales con versión y licencia, sin personalizaciones. |
| `ejemplos/` | Demos que no forman parte de la entrega académica. |
| `docs/` | Índice de documentación y mapa de estructura. |
| `docs/uso/` | Clonación, preparación de trabajos y personalización. |
| `docs/mantenimiento/` | Registros técnicos de verificación de la plantilla. |
| `pdf/` | Entregables PDF generados y versionados. |
| `tests/` | Comprobaciones automatizadas. |
| `.github/workflows/` | Validación automática de pruebas, enlaces y coherencia, sin compilar PDF. |
| `.build/` | Datos, referencias, registros y capturas temporales; fuera de Git. |

El portal `index.html` permanece en la raíz. Su presentación está en
`web/presentacion/index.html`; no hay otra copia editable en `reveal.js/`.

Las rutas de LaTeX se resuelven desde `documentos/`: usa `../assets/`,
`../plantilla/latex/` y `../.build/`. El compilador fija la raíz del repositorio
para sus datos y salidas, aunque se invoque desde otro directorio.
Las rutas HTML y CSS se resuelven desde el archivo que las contiene.

Para añadir una sección extensa usa `\input{secciones/nombre.tex}` desde el documento.
No dupliques archivos para conservar rutas antiguas: actualiza sus consumidores y pruebas.

## Criterios para añadir archivos

- Contenido específico de un trabajo: `datos/`, `documentos/` y `assets/contenido/`.
- Diseño reutilizable: `plantilla/latex/`, `web/portal/` o `web/presentacion/`, según su destino.
- Automatización Python: módulos en `herramientas/`; `compilar.py` conserva la entrada pública.
- Bibliotecas externas: `vendor/`, con versión y licencia; no mezclar con código propio.
- Nuevas comprobaciones: `tests/`, agrupadas por responsabilidad.
- Capturas de revisión, registros y archivos intermedios: `.build/`, ignorado por Git.
- Entregables finales: `pdf/`; no guardar allí fuentes ni capturas temporales.

La raíz conserva los dos puntos de entrada, el README, las instrucciones para
agentes y la configuración del repositorio. No necesita una carpeta `src/`:
la implementación ya está separada de los documentos académicos.

Las carpetas `.agents/`, `.codex/`, `.aws/`, `.venv/` y los archivos `.env`
son configuración local y están excluidos de Git. No copies credenciales en
datos académicos, documentación ni recursos del portal.

Consulta el [índice de documentación](README.md) para elegir la guía adecuada.
