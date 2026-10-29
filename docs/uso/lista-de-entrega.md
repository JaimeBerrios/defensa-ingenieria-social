# Lista de revisión antes de entregar

Por defecto entrega únicamente el reporte. Marca cada punto después de revisarlo.

- [ ] Completé los datos, integrantes y códigos en `datos/datos.md`, sin ejemplos.
- [ ] El reporte responde a la consigna y a las secciones solicitadas por el docente.
- [ ] Las afirmaciones, resultados y evidencias tienen respaldo; identifiqué lo pendiente.
- [ ] Registré fuentes reales en `datos/referencias.json` y revisé citas y APA 7.
- [ ] Ejecuté `python3 compilar.py --modo-entrega --verificar` sin pendientes.
- [ ] Ejecuté `python3 compilar.py --modo-entrega` y terminó correctamente.
- [ ] Revisé `.build/reporte.log`: sin referencias indefinidas, caracteres faltantes ni desbordamientos visibles.
- [ ] Abrí el PDF recién generado: portada, logos, tablas, numeración y firma final correctos.
- [ ] Confirmé que el archivo que entregaré es `pdf/reporte.pdf` y corresponde a la última compilación.

## Solo si también se solicita presentación

- [ ] Actualicé `documentos/presentacion.tex` y `web/presentacion/index.html` de forma coherente con el reporte.
- [ ] Ejecuté `python3 compilar.py --con-presentacion --modo-entrega --verificar`.
- [ ] Compilé con `python3 compilar.py --con-presentacion --modo-entrega` y revisé ambos registros.
- [ ] Revisé las diapositivas PDF y web: texto legible, expositores, citas, navegación y recursos sin cortes ni enlaces rotos.
- [ ] Incluí `pdf/presentacion.pdf` y la versión web con sus recursos locales, según la consigna.

En Windows puedes usar `python` en lugar de `python3`. La validación automática
de GitHub no sustituye esta revisión académica y visual.
