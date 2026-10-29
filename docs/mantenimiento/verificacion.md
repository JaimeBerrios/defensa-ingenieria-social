# Verificación de la plantilla

Revisión local del 16 de octubre de 2026. El proyecto conserva intencionalmente
los datos, integrantes y referencias de ejemplo para reutilizarlo.

## Correcciones

- Se retiró el bloque XMP incompatible de `isotipo-azul.png` y el perfil ICC
  no admitido por el motor PDF de `acreditacion.png`. Los bloques de píxeles
  comprimidos de ambos PNG permanecen idénticos; no se alteraron dimensiones,
  proporciones ni transparencia. El motor ya descartaba ese perfil al compilar.
- En Beamer, microtype aplica solamente los parches compatibles de listas,
  índice y ecuaciones; las notas al pie las gestiona Beamer.
- Se regeneraron ambos PDF y las vistas previas del portal.

## Comprobaciones ejecutadas

- `python3 compilar.py --probar`: 29 pruebas correctas.
- `python3 -m herramientas.validacion`: enlaces y recursos locales correctos.
- `python3 compilar.py --con-presentacion --verificar`: coinciden los títulos,
  los expositores y las nueve láminas.
- `python3 compilar.py --con-presentacion --sin-red`: ambos PDF compilados
  con los recursos existentes, sin descargar dependencias.
- Inspección de las ocho páginas del reporte y nueve de la presentación:
  logos, tablas, pies y firma sin cortes visibles.
- Firefox sin interfaz, con apertura local: tema del sistema, cambio de tema,
  persistencia, imágenes, comandos de Windows/Linux/macOS, copia y menú móvil.
- Vistas de 320, 390 y 768 píxeles mediante iframe: sin desbordamiento horizontal;
  navegación móvil comprobada a 390 píxeles.
- Presentación web: avance y retroceso por fragmentos, índice, comparativa y
  reinicio de portada y fragmentos correctos.

## Límites conocidos

El reporte compila sin advertencias tipográficas. La presentación conserva
avisos del motor sobre el mapa Unicode de los iconos Font Awesome y sustituciones
de tamaños de fuente de hasta 1,25 puntos. No se observaron iconos ausentes,
caracteres perdidos ni desbordamientos. El mapa afecta la extracción de los
iconos como texto; su dibujo se conserva. Esta revisión no equivale a pruebas
en todos los navegadores o sistemas operativos.

El modo entrega debe rechazar esta plantilla mientras mantenga ejemplos.
Para entregar un trabajo real hay que completar sus datos, contenido y fuentes.
La revisión no incluye commit ni publicación de la reorganización existente.
