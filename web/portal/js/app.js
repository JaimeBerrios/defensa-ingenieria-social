const installs = [
  ['Python 3.9+', 'Requerido', 'Ejecuta compilar.py sin paquetes adicionales de pip.'],
  ['Tectonic', 'Automático', 'El script descarga la versión fija y la reutiliza fuera del repositorio.'],
  ['VS Code', 'Opcional', 'Edita los archivos y compila con Ctrl + Shift + B.'],
  ['Git', 'Versiones', 'Conserva el trabajo existente; crea otra rama solo cuando comiences un proyecto que lo necesite.']
];
const fileGroups = [
  ['Archivos que editas', [
    ['datos/datos.md', 'Datos y consigna', 'Metadatos e integrantes: una sola fuente para las portadas.'],
    ['datos/referencias.json', 'Referencias', 'Fuentes confirmadas y formas de cita compartidas en APA 7.'],
    ['documentos/reporte.tex', 'Contenido del reporte', 'Redacta aquí el trabajo académico.'],
    ['documentos/presentacion.tex', 'Diapositivas PDF', 'Prepara las láminas cuando se solicite una exposición.'],
    ['web/presentacion/index.html', 'Diapositivas web', 'Contenido y notas de las diapositivas.'],
    ['web/presentacion/css/ y js/', 'Diseño web', 'Estilos e interacciones locales; conserva los marcadores.']
  ]],
  ['Herramientas y recursos', [
    ['compilar.py', 'Compilación', 'Genera el reporte por defecto; usa --con-presentacion para incluir las diapositivas.'],
    ['plantilla/latex/', 'Diseño LaTeX', 'Estilos institucionales reutilizables.'],
    ['assets/', 'Recursos', 'Logos, fuentes, iconos y contenido del trabajo.'],
    ['herramientas/ y vendor/', 'Mantenimiento', 'Validación, descarga de iconos y dependencias locales con sus licencias.']
  ]],
  ['Entregables', [
    ['pdf/reporte.pdf', 'Reporte', 'Documento principal en tamaño carta.'],
    ['pdf/presentacion.pdf', 'Presentación PDF', 'Diapositivas 16:9 para exponer.'],
    ['web/presentacion/index.html', 'Presentación web', 'Versión interactiva que funciona sin conexión.']
  ]]
];
const workflow = [
  ['1', 'Revisa tu rama', 'Conserva el trabajo actual. Crea una rama descriptiva únicamente si necesitas comenzar otro proyecto.'],
  ['2', 'Completa los datos', 'Edita datos/datos.md y registra las fuentes en datos/referencias.json.'],
  ['3', 'Redacta el reporte', 'Actualiza documentos/reporte.tex. La presentación se prepara cuando también necesitas exponer.'],
  ['4', 'Agrega evidencias', 'Guarda las imágenes, gráficos y evidencias en assets/contenido/.'],
  ['5', 'Valida y compila', 'Ejecuta los comandos desde la raíz y revisa los registros de .build/.'],
  ['6', 'Revisa la entrega', 'Abre el PDF generado y comprueba portada, citas, tablas y firma final.']
];

function renderCards(container, items) {
  items.forEach(([title, label, description]) => {
    const column = document.createElement('div');
    column.className = 'col-md-6';
    const card = document.createElement('article');
    card.className = 'info-card';
    [['span', label], ['h3', title], ['p', description]].forEach(([tag, text]) => {
      const node = document.createElement(tag);
      node.textContent = text;
      card.append(node);
    });
    column.append(card);
    container.append(column);
  });
}
renderCards(document.querySelector('#installGrid'), installs);
renderCards(document.querySelector('#workflowGrid'), workflow);
const fileGrid = document.querySelector('#fileGrid');
fileGroups.forEach(([title, items]) => {
  const section = document.createElement('div');
  section.className = 'col-12';
  const heading = document.createElement('h3');
  heading.className = 'grupo-archivos';
  heading.textContent = title;
  const row = document.createElement('div');
  row.className = 'row g-3';
  renderCards(row, items);
  section.append(heading, row);
  fileGrid.append(section);
});
document.querySelector('#currentYear').textContent = new Date().getFullYear();

const root = document.documentElement;
const themeToggle = document.querySelector('#themeToggle');
const systemTheme = matchMedia('(prefers-color-scheme: dark)');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const status = document.querySelector('#portalStatus');
const announce = message => { status.textContent = message; };
let savedTheme = null;
try { savedTheme = localStorage.getItem('theme'); } catch { /* Preferencias no esenciales. */ }
if (!['dark', 'light'].includes(savedTheme)) savedTheme = null;

function applyTheme(theme) {
  root.classList.toggle('dark', theme === 'dark');
  root.classList.toggle('light', theme === 'light');
  root.dataset.theme = theme;
  root.dataset.bsTheme = theme;
  themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
  themeToggle.title = themeToggle.getAttribute('aria-label');
  themeToggle.querySelector('i').className = theme === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
}
applyTheme(root.dataset.theme);
function changeTheme(update) {
  if (document.startViewTransition && !reducedMotion.matches) document.startViewTransition(update);
  else update();
}
themeToggle.addEventListener('click', () => changeTheme(() => {
  savedTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('theme', savedTheme); } catch { /* El tema sigue funcionando sin persistencia. */ }
  applyTheme(savedTheme);
}));
systemTheme.addEventListener('change', event => {
  if (!savedTheme) applyTheme(event.matches ? 'dark' : 'light');
});

// Los comandos se mantienen como texto seleccionable incluso si falla el portapapeles.
const commandSystem = document.querySelector('#commandSystem');
const commandTemplates = new Map();
document.querySelectorAll('code').forEach(code => {
  if (/^python(?:3)?\b/.test(code.textContent.trim())) {
    commandTemplates.set(code, code.textContent.trim().replace(/^python3?\b/, '{python}'));
  }
});
function updateCommands() {
  const python = commandSystem.value === 'windows' ? 'python' : 'python3';
  commandTemplates.forEach((template, code) => { code.textContent = template.replace('{python}', python); });
  document.querySelectorAll('.copy-command').forEach(button => {
    button.textContent = 'Copiar';
    button.setAttribute('aria-label', 'Copiar comando: ' + button.previousElementSibling.textContent);
  });
}
commandSystem.value = /Win/i.test(navigator.platform) ? 'windows' : 'unix';
commandSystem.addEventListener('change', () => {
  updateCommands();
  announce('Comandos para ' + (commandSystem.value === 'windows' ? 'Windows.' : 'Linux o macOS.'));
});
async function copyCommand(code, button) {
  const text = code.textContent;
  let copied = false;
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      copied = true;
    }
  } catch { /* Respaldo para apertura local y permisos restringidos. */ }
  if (!copied) {
    const input = document.createElement('textarea');
    input.value = text;
    input.setAttribute('readonly', '');
    input.className = 'clipboard-fallback';
    document.body.append(input);
    input.select();
    try { copied = document.execCommand('copy'); } catch { copied = false; }
    input.remove();
    button.focus();
  }
  if (copied) {
    button.textContent = 'Copiado';
    announce('Comando copiado.');
    window.setTimeout(() => { button.textContent = 'Copiar'; }, 2000);
  } else {
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(code);
    selection.removeAllRanges();
    selection.addRange(range);
    announce('No se pudo copiar automáticamente. El comando está seleccionado; usa Ctrl+C o Cmd+C.');
  }
}
document.querySelectorAll('.code-panel code').forEach(code => {
  const row = document.createElement('div');
  row.className = 'command-row';
  code.before(row);
  row.append(code);
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-command';
  button.textContent = 'Copiar';
  button.addEventListener('click', () => copyCommand(code, button));
  row.append(button);
});
updateCommands();

const nav = document.querySelector('.navbar');
const menu = document.querySelector('#mainNav');
const links = [...document.querySelectorAll('#mainNav .nav-link')];
const sections = [...document.querySelectorAll('main > header[id], main > section[id]')];
function updateNavigation() {
  const margin = parseFloat(getComputedStyle(sections[0]).scrollMarginTop) || 96;
  const edge = Math.max(nav.getBoundingClientRect().height + 24, margin + 4);
  let current = sections[0].id;
  sections.forEach(section => { if (section.getBoundingClientRect().top <= edge) current = section.id; });
  links.forEach(link => {
    const active = link.hash === '#' + current;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
let pendingScroll = false;
window.addEventListener('scroll', () => {
  if (!pendingScroll) requestAnimationFrame(() => { updateNavigation(); pendingScroll = false; });
  pendingScroll = true;
}, { passive: true });
links.forEach(link => link.addEventListener('click', () => {
  if (window.bootstrap && window.matchMedia('(max-width: 991.98px)').matches && menu.classList.contains('show')) {
    const collapse = bootstrap.Collapse.getOrCreateInstance(menu, { toggle: false });
    menu.addEventListener('hidden.bs.collapse', () => {
      const destination = document.querySelector(link.hash);
      destination.scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth' });
      destination.setAttribute('tabindex', '-1');
      destination.focus({ preventScroll: true });
    }, { once: true });
    collapse.hide();
  }
}));
window.addEventListener('resize', updateNavigation);
updateNavigation();
