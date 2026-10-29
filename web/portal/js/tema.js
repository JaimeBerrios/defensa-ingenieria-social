// Se ejecuta antes de los estilos para evitar un destello del tema incorrecto.
(() => {
  let saved = null;
  try { saved = localStorage.getItem('theme'); } catch { /* Almacenamiento opcional. */ }
  const theme = ['light', 'dark'].includes(saved) ? saved
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  document.documentElement.classList.add(theme);
  document.documentElement.dataset.theme = theme;
  document.documentElement.dataset.bsTheme = theme;
})();
