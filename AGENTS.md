# Instrucciones para Codex

## Alcance

Este repositorio contiene una campaña web: presentación Reveal.js y guion técnico.
El contenido, CSS e interacciones actuales están incluidos en `index.html` y
`guion.html`. Los directorios `css/` y `js/` conservan recursos previos sin cargar. `reveal-demo.html` conserva la demo y debe mantenerse.
No restaures el sistema LaTeX/PDF ni su compilador salvo petición expresa.

Revisa Git antes de editar y respeta el trabajo existente. Trabaja en la rama
actual; no hagas commit, push ni cambies de rama sin solicitud del usuario.

## Contenido y diseño

Edita datos, integrantes, citas y notas directamente en los HTML. Mantén la
correspondencia entre los cinco entornos y los bloques de `guion.html` (montaje de 07:45). Usa las vistas de cada entorno
para preparar la utilería; no agregues láminas por cada toma. La campaña
carga Reveal.js 6.0.2 desde cdnjs y Tailwind CSS vía CDN; la demo conserva la
biblioteca local.
No inventes nombres, códigos, resultados ni referencias. Conserva los marcadores
HTML de datos, citas y bibliografía para futuras ediciones.
Usa Grupo como término colectivo y `data-expositor="grupo"` para el equipo.
Conserva los archivos de logos en `assets/institucional/`, pero no muestres
logos universitarios en las interfaces actuales. El escudo digital SVG propio
de la lámina 2 sí forma parte del diseño solicitado. Mantén el lienzo 16:9 en computadora, el reflujo nativo en móvil, el azul
`#173864` como acento y la correspondencia de tiempos y expositores.
No agregues firma a las diapositivas ni reduzcas indiscriminadamente las letras.

La biblioteca está en `vendor/reveal.js/`: conserva su licencia y no personalices
sus archivos. Los iconos Font Awesome Free están en `assets/iconos/fontawesome/`;
conserva su licencia. No elimines la demo ni sus recursos.

## Verificación

Después de mover o editar recursos, revisa los enlaces locales de los HTML,
las rutas CSS y la sintaxis JavaScript. Si hay navegador disponible, comprueba
la presentación y la demo, navegación, notas, interacciones y consola. Identifica las
comprobaciones manuales o de navegador que queden pendientes.
No se requiere compilar documentos ni generar PDF.

## Commits

Cuando el usuario autorice commits, usa Conventional Commits 1.0.0:
`tipo(alcance opcional): descripción`, tipos en minúsculas y descripción breve
en español. Consulta `docs/mantenimiento/commits.md`. No reescribas historial.
