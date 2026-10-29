# Ingeniería Social: El Factor Humano

Cortometraje universitario de **7:45** para familiares y estudiantes no técnicos.
Las pantallas son utilería del set: la cámara sigue a los actores, sus manos,
las decisiones y las reacciones.

- [Presentación / utilería](index.html): **5 entornos Reveal.js**, con vistas internas.
- [Documento de rodaje](guion.html): **6 columnas y 13 bloques**, de 00:00 a 07:45.
- [Demo Reveal.js](reveal-demo.html): conservada con su biblioteca local.

## Los cinco entornos

| Lámina | Uso | Vistas |
|---|---|---|
| 1 | Hook y phishing/smishing | Correo, SMS |
| 2 | Golpe de título | Escudo digital SVG |
| 3 | Sitios espejo | Navegador y advertencia |
| 4 | Redes y accesos | Wi-Fi/popup, Doble candado/códigos |
| 5 | Huella y cierre | Red social/boleto, Tres pilares, Créditos |

## Preparar una toma

Abre el guion: sus enlaces preparan la vista exacta con los controles ocultos.
También puedes elegir una vista en la presentación y pulsar **Modo rodaje**.
**R** en computadora o el círculo tenue inferior izquierdo en móvil permiten
volver a los controles. Los botones propios de la maqueta siguen funcionando.

Ejemplos de rutas relativas:

- `index.html?rodaje=1&vista=sms#/mensajes`
- `index.html?rodaje=1&vista=wifi#/red-accesos`
- `index.html?rodaje=1&vista=accesos#/red-accesos`
- `index.html?rodaje=1&vista=creditos#/huella-cierre`

En móvil, la vista de accesos en modo rodaje muestra directamente la app de
códigos; en laptop conserva la comparativa de contraseñas. La vista SMS móvil
se presenta como una app, sin dibujar un segundo teléfono dentro del dispositivo.
El resto de las interfaces se reorganiza con texto legible y desplazamiento vertical.

**Pausar pulsos** o `pausa=1` congela el pulso de las alertas para repetir tomas.
El autenticador sigue activo y cambia su código de demostración cada 30 segundos.
Los códigos son ficticios y no corresponden a ninguna cuenta.
El boleto aparece censurado por defecto; un botón revela o tapa los datos ficticios.

## Abrir y editar

Cada HTML incluye su CSS y sus interacciones. Reveal.js 6.0.2 y Tailwind CSS se
cargan desde CDN: requieren conexión, sin npm ni empaquetadores. Para notas del
expositor, sirve la raíz y pulsa `S`:

```bash
python3 -m http.server 8000
```

Visita `http://localhost:8000/` y `http://localhost:8000/guion.html`.
Conserva la correspondencia entre las notas del expositor y las filas del guion.
Las rutas relativas permiten publicar desde la raíz en GitHub Pages.

## Equipo

| Integrante | Código | Rol |
|---|---|---|
| Jaime Fernando Berrios Ortiz | bo0310042024 | El Atacante / Ingeniero Social |
| Genesis Abigail Saravia Carpio | sc0139042023 | Defensora (Hook y Redes) |
| Jefferson Jared Bonilla Meléndez | bm0749042022 | Defensor (Phishing y SMS) |
| Rosmeri Estefani González Pérez | gp0382042023 | Defensora (Navegador) |
| Florentín Alexander Treminio Herrera | th0988042023 | Defensor (Wi-Fi y 2FA) |

**Diseño de Sistemas de Seguridad de Redes - UNAB / Universidad Dr. Andrés Bello.**

## Verificación y rodaje

Las pruebas de navegador no validan la cámara física. Quedan pendientes ensayo de
lectura y montaje, foco, reflejos, moiré, bandas, exposición y sonido con el equipo real.
El guion incluye notas de continuidad y fuentes FTC, CISA, OWASP y Sony.

No se ha hecho commit ni despliegue. La demo y los archivos institucionales se
conservan; los logos no aparecen en las interfaces. Los directorios `css/` y `js/`
contienen recursos anteriores que estos HTML ya no cargan.
Consulta `LICENSE`, `vendor/reveal.js/LICENSE` y
`assets/iconos/fontawesome/LICENSE.txt`.
