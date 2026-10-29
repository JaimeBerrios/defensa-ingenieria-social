# Personalización

## Datos y contenido

Edita metadatos en `datos/datos.md` y citas en `datos/referencias.json`.
La etiqueta colectiva es **Grupo**; no alternar con Equipo. En diapositivas usa
`data-expositor="grupo"` para el valor compartido y un nombre propio para una persona.
En LaTeX usa `\expositor{\Grupo}` para el colectivo.

## Diseño web

- `web/presentacion/css/unab.css`: tema institucional compartido.
- `web/presentacion/css/presentacion.css`: composiciones de la plantilla actual.
- `web/presentacion/js/presentacion.js`: configuración de Reveal y pie del expositor.
- `web/presentacion/js/interacciones.js`: índice, ruta, accesibilidad y herramientas.
- `web/presentacion/index.html`: contenido, notas y marcadores de sincronización.

Conserva azul `#173864`, logos, formato 16:9, notas y marcadores de citas y datos.
No reduzcas todo el texto para encajar contenido: reorganiza o divide las láminas.

## Font Awesome

Está permitido descargar iconos oficiales adicionales de **Font Awesome Free** cuando
aporten claridad al contenido. No hace falta limitarse a la selección inicial.
Usa iconos Free, conserva versión y licencia y respeta los permisos técnicos de red.
No cambies automáticamente a una versión nueva ni descargues recursos Pro sin licencia.

```bash
python3 -m herramientas.iconos --descargar microscope shield-halved --sincronizar
# Solo actualizar la biblioteca desde SVG ya guardados, sin conexión:
python3 -m herramientas.iconos --sincronizar
```

Los originales se guardan en `assets/iconos/fontawesome/solid/` y la licencia en
`assets/iconos/fontawesome/LICENSE.txt`. La versión fijada es 6.7.2.
Para mostrar un icono ya sincronizado:

```html
<svg class="icono-fa" aria-hidden="true" focusable="false">
  <use href="#fa-microscope"></use>
</svg>
```

Mantén texto visible en botones y títulos. Los iconos decorativos se ocultan a lectores
de pantalla. La biblioteca SVG se incorpora al HTML para permitir abrirlo con `file://`
sin solicitudes externas; los originales siguen centralizados para mantenimiento.

Después de cambiar rutas ejecuta `python3 -m herramientas.validacion`.
Después de cambiar contenido valida y compila los entregables seleccionados con `compilar.py`.


## Portal principal

`index.html` usa estilos en `web/portal/css/styles.css`, interacciones en
`web/portal/js/app.js` y el tema inicial en `web/portal/js/tema.js`.
Bootstrap y las fuentes de Font Awesome se cargan localmente desde `vendor/`,
conservando sus versiones y licencias. No sustituyas estos enlaces por CDN si
quieres mantener el funcionamiento sin conexión.

Los comandos se adaptan al selector de sistema y se copian desde su texto visible.
El tema sigue al sistema hasta que el usuario elige uno con el botón de sol/luna
de la navegación. Las transiciones respetan movimiento reducido.
Los datos de las tarjetas están en `app.js`; evita añadir rutas antiguas o una
instrucción de cambiar de rama automáticamente.
