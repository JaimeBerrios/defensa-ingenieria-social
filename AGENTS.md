# Instrucciones para Codex

## Mensajes de commit

Cuando el usuario autorice commits, usa Conventional Commits 1.0.0:
`tipo(alcance opcional): descripción`. Consulta `docs/mantenimiento/commits.md`.
Usa los tipos en minúsculas y descripciones breves en español. Esta norma aplica
a commits nuevos; no reescribas el historial publicado para adaptarlo.

## Propósito y archivos

Este repositorio es una plantilla local para tres entregables académicos UNAB:
`pdf/presentacion.pdf`, `pdf/reporte.pdf` y `web/presentacion/index.html`. GitHub aloja las ramas; no compila.
**Por defecto, prepara, genera y compila exclusivamente el reporte.**
Solo prepara o actualiza `documentos/presentacion.tex`, `pdf/presentacion.pdf` y
`web/presentacion/index.html` cuando el usuario solicite explícitamente la presentación.
Para incluirla, ejecuta `python compilar.py --con-presentacion`.
Lee `datos/datos.md` antes de editar y revisa el estado de Git para respetar el trabajo
existente. Trabaja en la rama actual. Si el usuario pide una rama nueva, créala
con un nombre descriptivo; no cambies de rama ni publiques cambios por rutina.

- `datos/datos.md`: fuente compartida de datos y consigna en español.
- `datos/referencias.json`: referencias redactadas en APA 7 y formas de cita compartidas.
- `herramientas/contenido.py`: comprobación de láminas y generación de citas/bibliografías.
- `documentos/presentacion.tex`, `documentos/reporte.tex` y `web/presentacion/index.html`: contenido editable de cada entregable.
- `plantilla/latex/*.sty`, `web/presentacion/css/unab.css` y `web/presentacion/js/presentacion.js`: diseño reutilizable; modificar solo si hace falta ajustar
  la presentación visual o si el usuario lo solicita.
- `assets/institucional/`: logos obligatorios, variantes y acreditación.
- `assets/contenido/imagenes/`: imágenes y gráficos del trabajo.
- `vendor/reveal.js/`: biblioteca externa con su versión y licencia; no personalizar aquí.
- `assets/fuentes/firma.otf`: fuente personal original, usada por el reporte y en la firma web del index.
- `compilar.py`: único punto de entrada para compilar los dos documentos y sincronizar datos web.

## Edición

Conserva los encabezados y las etiquetas de datos generales de `datos/datos.md`, y las
columnas Nombre/Código. El script escapa caracteres especiales y genera
`.build/datos.tex`; no edites ese archivo ni dupliques estos valores en los `.tex`.
Solo con `--con-presentacion` o `--solo-presentacion`, también actualiza los elementos `span[data-campo]` y `tbody#integrantes` del HTML;
conserva esos marcadores y edita sus valores en datos/datos.md. La firma no se exporta al HTML.
Conserva también los marcadores `data-cita` y `referencias:inicio` / `referencias:fin`.
Las citas se editan en datos/referencias.json; usa `\cita`, `\citatexto` o `\citas` (múltiples) en LaTeX.
No edites las bibliografías generadas en .build/. Revisa el formato APA 7 según
el tipo de fuente: el script centraliza textos, no valida todas las reglas APA.
Ejecuta `python compilar.py --verificar` para validar el reporte y recursos institucionales. Usa
`python compilar.py --con-presentacion --verificar` para detectar diferencias de títulos,
expositores, cantidad de láminas o claves de citas antes de compilar.
Usa `--modo-entrega` (o `--entrega`) para validar estrictamente que no queden datos, integrantes ni referencias de ejemplo antes de entregar.
Usa `--solo-presentacion` cuando únicamente se requiera iterar sobre las láminas (PDF y web).
Usa `--limpiar` para eliminar temporales de `.build/` y `--probar` para correr la suite de pruebas.
Los apartados de tema, indicaciones y fuentes requieren interpretación y redacción;
no se convierten automáticamente en contenido académico.

Usa los datos y fuentes proporcionados. No inventes integrantes, códigos, nombres
de docentes, resultados ni referencias. Si falta información esencial, pregunta;
puedes avanzar con las partes independientes. En un borrador identifica lo pendiente.
Sustituye los textos de ejemplo cuando prepares un trabajo real y adapta las
secciones a la consigna. Cuando se solicite la presentación, mantén su coherencia
con el reporte; no actualices diapositivas por rutina al trabajar solo en el reporte.

Conserva ambos logos, sus proporciones y el azul institucional `#173864`.
Mantén diapositivas 16:9, textos breves y un pie con el expositor correspondiente.
No reduzcas indiscriminadamente el tamaño de letra para hacer caber contenido:
divide láminas o reorganiza la portada si hay muchos integrantes o títulos largos.
El reporte usa tamaño carta y firma tipográfica al final de todo su contenido,
incluidos los anexos. El texto de firma procede de `datos/datos.md`; no agregar firma
a las diapositivas. Cuando prepares la presentación, asegúrate de reflejar los cambios
tanto en `documentos/presentacion.tex` como en `web/presentacion/index.html`.

## Compilación y entrega obligatorias

Después de editar contenido o diseño, ejecuta `python3 compilar.py` desde la raíz
(en Windows, `python compilar.py`). El script descarga una versión fija de
Tectonic si falta en la carpeta de datos del usuario y la reutiliza en futuras
ramas y clones. No instales una copia por proyecto ni guardes el compilador en Git.
La primera ejecución y los paquetes nuevos necesitan red. Respeta los permisos
del entorno y solicita la autorización técnica necesaria si el sandbox bloquea
red o escritura fuera del repositorio; no eludas esas restricciones.

1. Compila el reporte con el script; incluye la presentación únicamente si fue solicitada.
2. Revisa `.build/reporte.log` y, si se compiló la presentación, `.build/presentacion.log`: resuelve referencias
   indefinidas, caracteres faltantes y desbordamientos visibles.
3. Inspecciona los PDF recién generados: logos completos, portada legible, tablas y pies sin cortes,
   numeración coherente y firma al final del reporte. Si hay herramientas de
   renderizado, guarda las capturas temporales en `.build/` o fuera del repositorio.
4. Entrega el reporte y un resumen breve de cambios y verificaciones. Solo si se
   solicitó la presentación, entrega también su PDF y el HTML web actualizados.

No declares la tarea terminada con PDF antiguos ni sustituyas LaTeX por una impresión PDF desde HTML.
Si la compilación queda bloqueada, explica el error y distingue los PDF anteriores de los nuevos. El script conserva los anteriores si uno falla.
`--sin-red` permite comprobar que el motor y los paquetes se reutilizan sin descargas.
El entregable predeterminado es `pdf/reporte.pdf`. Si se solicita la presentación,
se añaden `pdf/presentacion.pdf` y `web/presentacion/index.html`. Conserva las fuentes
editables y los entregables anteriores no seleccionados. No hagas commit ni push salvo que se solicite.


## Organización e iconos

Respeta la distribución documentada en `docs/estructura.md`. `compilar.py` y el portal
`index.html` permanecen en la raíz. La implementación Python está en `herramientas/`.
No crees copias editables en las rutas antiguas ni guardes temporales fuera de `.build/`.
LaTeX resuelve recursos desde `documentos/`: usa `../assets/`, `../plantilla/latex/`
y `../.build/`. La presentación se edita en `web/presentacion/index.html`, sus estilos
en `web/presentacion/css/` y sus interacciones en `web/presentacion/js/`.

Usa **Grupo** como término colectivo, con el valor de `datos/datos.md`. En HTML usa
`data-expositor="grupo"`; en LaTeX, `\expositor{\Grupo}`. Para una persona concreta usa
su nombre y conserva la correspondencia entre PDF y web.

Está autorizado descargar iconos adicionales de **Font Awesome Free** cuando hagan falta
para el contenido. Usa fuentes oficiales, conserva versión y licencia, guarda los SVG en
`assets/iconos/fontawesome/solid/` y mantén el funcionamiento sin conexión. La herramienta
`python3 -m herramientas.iconos --descargar NOMBRE --sincronizar` descarga desde la versión
fijada y actualiza la biblioteca SVG incorporada al HTML. Respeta las autorizaciones técnicas
de red del entorno; no uses iconos Pro sin una licencia aportada por el usuario.
Consulta `docs/uso/personalizacion.md`. No descargues la biblioteca completa si basta una selección.

Después de mover recursos ejecuta `python3 -m herramientas.validacion`, las pruebas y la
compilación de los entregables afectados. Revisa enlaces, consola y documentos renderizados.
