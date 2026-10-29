# Guía de uso

Antes de comenzar, consulta el [tutorial de clonación por HTTPS o SSH y trabajo
con ramas](clonacion-y-ramas.md) si necesitas descargar la plantilla o incorporarte
a la rama de tu equipo.

1. Completa `datos/datos.md` y registra fuentes reales en `datos/referencias.json`.
2. Edita `documentos/reporte.tex`. El contenido de las indicaciones no se redacta automáticamente.
3. Ejecuta `python3 compilar.py --verificar` y `python3 compilar.py` desde la raíz.
4. Revisa `.build/reporte.log` y abre `pdf/reporte.pdf`.
5. Solo si necesitas exposición, edita `documentos/presentacion.tex` y
   `web/presentacion/index.html`, y ejecuta `python3 compilar.py --con-presentacion`.
6. Abre `index.html` para acceder al portal y los entregables.

Antes de enviar el trabajo, completa la [lista de entrega](lista-de-entrega.md).

`--sin-red` usa el motor y los paquetes previamente descargados. `--modo-entrega --verificar`
rechaza metadatos y referencias de ejemplo; no reemplaza la revisión académica ni visual.
`--probar` ejecuta las pruebas. `--solo-presentacion` conserva el reporte anterior.
`--limpiar` elimina exclusivamente los temporales de `.build/`.

El portal usa Bootstrap y Font Awesome locales, con versiones y licencias en vendor/.
El portal y la presentación institucional pueden abrirse sin conexión. Los enlaces a redes
sociales y sitios externos requieren internet.
La presentación institucional usa recursos locales y funciona sin conexión. La demo en
`ejemplos/` conserva referencias externas de la demostración original.
