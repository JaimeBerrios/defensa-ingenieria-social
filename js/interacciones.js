// Configuración local: recorrido lineal y transiciones discretas.
Reveal.configure({ navigationMode: "linear", transition: "fade", transitionSpeed: "fast" });
const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)");
function ajustarMovimiento() {
  Reveal.configure({
    transition: movimientoReducido.matches ? "none" : "fade",
    backgroundTransition: movimientoReducido.matches ? "none" : "fade",
    autoAnimate: !movimientoReducido.matches,
    fragments: true
  });
  document.querySelectorAll(".slides > section").forEach(function (slide) {
    slide.dataset.transition = movimientoReducido.matches ? "none" : "fade";
  });
}
ajustarMovimiento();
movimientoReducido.addEventListener("change", ajustarMovimiento);

const herramientas = document.querySelector(".herramientas");
function cerrarPaneles() {
  herramientas.querySelectorAll("details").forEach(function (panel) { panel.open = false; });
}
function actualizarIndice() {
  const actual = Reveal.getCurrentSlide();
  if (!actual) return;
  const etapa = ["reflexion", "conceptos"].includes(actual.id) ? "contexto"
    : ["desarrollo", "aplicaciones", "comparativa"].includes(actual.id) ? "desarrollo" : "cierre";
  document.querySelector(".ruta-exposicion").hidden = actual.id === "portada";
  document.querySelectorAll(".ruta-exposicion a").forEach(function (enlace) {
    if (enlace.dataset.etapa === etapa) enlace.setAttribute("aria-current", "step");
    else enlace.removeAttribute("aria-current");
  });
  herramientas.querySelectorAll("nav a").forEach(function (enlace) {
    if (enlace.hash === "#/" + actual.id) enlace.setAttribute("aria-current", "step");
    else enlace.removeAttribute("aria-current");
  });
}
document.querySelectorAll(".herramientas nav a, .ruta-exposicion a").forEach(function (enlace) {
  enlace.addEventListener("click", function (evento) {
    evento.preventDefault();
    const destino = document.getElementById(enlace.hash.slice(2));
    const posicion = Array.from(document.querySelectorAll(".slides > section")).indexOf(destino);
    if (posicion >= 0) Reveal.slide(posicion, 0, -1);
    cerrarPaneles();
    document.querySelector("#indice-presentacion summary").focus();
  });
});
herramientas.querySelectorAll("details").forEach(function (panel) {
  panel.addEventListener("toggle", function () {
    if (panel.open) herramientas.querySelectorAll("details").forEach(function (otro) {
      if (otro !== panel) otro.open = false;
    });
  });
});
function alternarHerramientas() {
  cerrarPaneles();
  const ocultas = document.body.classList.toggle("modo-exposicion");
  if (ocultas) document.activeElement.blur();
  else document.querySelector("#indice-presentacion summary").focus();
}
document.getElementById("iniciar-exposicion").addEventListener("click", alternarHerramientas);
Reveal.addKeyBinding({ keyCode: 72, key: "H", description: "Mostrar u ocultar herramientas" }, alternarHerramientas);
document.addEventListener("keydown", function (evento) {
  if (evento.key === "Escape" && herramientas.querySelector("details[open]")) {
    evento.preventDefault();
    evento.stopImmediatePropagation();
    const panel = herramientas.querySelector("details[open]");
    cerrarPaneles();
    panel.querySelector("summary").focus();
  }
}, true);

const estadoHerramientas = document.querySelector(".estado-herramientas");
const botonPantalla = document.getElementById("pantalla-completa");
function actualizarPantalla() {
  const activa = Boolean(document.fullscreenElement);
  botonPantalla.setAttribute("aria-pressed", String(activa));
  botonPantalla.setAttribute("aria-label", activa ? "Salir de pantalla completa" : "Entrar en pantalla completa");
  botonPantalla.querySelector("span").textContent = activa ? "Salir de pantalla completa" : "Pantalla completa";
}
botonPantalla.addEventListener("click", async function () {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
    cerrarPaneles();
  } catch (error) {
    document.getElementById("ayuda-presentacion").open = true;
    estadoHerramientas.textContent = "El navegador no permitió pantalla completa. Prueba la tecla F.";
  }
});
document.addEventListener("fullscreenchange", actualizarPantalla);
actualizarPantalla();
document.getElementById("reiniciar-presentacion").addEventListener("click", function () {
  Reveal.togglePause(false);
  Reveal.toggleOverview(false);
  document.querySelectorAll(".slides .fragment").forEach(function (fragmento) {
    fragmento.classList.remove("visible", "current-fragment");
  });
  Reveal.sync();
  Reveal.slide(0, 0, -1);
  document.body.classList.remove("modo-exposicion");
  estadoHerramientas.textContent = "Presentación reiniciada.";
  cerrarPaneles();
  document.querySelector("#indice-presentacion summary").focus();
});

Reveal.on("ready", actualizarIndice);
Reveal.on("slidechanged", function () { cerrarPaneles(); actualizarIndice(); });
Reveal.on("fullscreen", function () { cerrarPaneles(); });
if (Reveal.isReady()) actualizarIndice();
