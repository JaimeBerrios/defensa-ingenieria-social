# Vistas previas del portal

Capturas reales de la primera página de los PDF de ejemplo. Se muestran en index.html.
Actualízalas si cambias la portada o los datos, después de compilar:

```bash
pdftoppm -f 1 -singlefile -scale-to 850 -png pdf/reporte.pdf assets/contenido/vistas-previas/reporte
pdftoppm -f 1 -singlefile -scale-to 850 -png pdf/presentacion.pdf assets/contenido/vistas-previas/presentacion
```

No representan el estado de compilación en vivo. Los PDF de pdf/ son los entregables.
