# Validación automática

El flujo [validacion.yml](../../.github/workflows/validacion.yml) se ejecuta en
GitHub Actions con cada push y Pull Request. También permite iniciarlo manualmente
desde la pestaña **Actions** cuando esté disponible en la rama predeterminada.

Comprueba en Python 3.9 y 3.13:

1. La suite de pruebas (`python compilar.py --probar`).
2. Enlaces Markdown y recursos locales (`python -m herramientas.validacion`).
3. Datos, citas y coherencia de los documentos (`python compilar.py --con-presentacion --verificar`).

No compila PDF, no descarga Tectonic, no publica archivos y no necesita paquetes
pip. Los avisos de datos de ejemplo son esperados en esta plantilla: el flujo
no usa `--modo-entrega`, porque ese modo corresponde a un trabajo personalizado.
GitHub prepara Python y las acciones necesarias en sus propios ejecutores.

La comprobación de enlaces se limita a destinos locales; no consulta la
disponibilidad de sitios externos ni evalúa el contenido académico.

Para repetir las comprobaciones en tu equipo ejecuta los mismos tres comandos
desde la raíz. Un resultado local correcto no acredita una ejecución remota:
consulta el resultado en Actions después de publicar el flujo.

Referencia: [documentación oficial de GitHub Actions para Python](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
