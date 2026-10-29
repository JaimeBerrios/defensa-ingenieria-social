/* Las simulaciones no envían datos ni abren dominios externos. */
(() => {
  const feedback = document.getElementById('alert-feedback');
  document.getElementById('alert-button').addEventListener('click', () => {
    feedback.textContent = 'Simulación: detente. Verifica por la aplicación o el canal oficial antes de actuar.';
  });
  if (!window.Reveal) {
    document.getElementById('load-error').hidden = false;
    return;
  }
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function updateSpeaker(event) {
    const slide = event.currentSlide || Reveal.getCurrentSlide();
    const name = slide.dataset.expositor === 'grupo' ? 'Grupo · 5 integrantes' : slide.dataset.expositor;
    document.getElementById('speaker').textContent = `${name} / ${slide.dataset.tiempo}`;
  }
  Reveal.on('ready', updateSpeaker);
  Reveal.on('slidechanged', updateSpeaker);
  Reveal.initialize({
    width: 1280, height: 720, margin: 0.08,
    hash: true, slideNumber: true, controls: true, progress: true,
    transition: reduced ? 'none' : 'fade',
    plugins: window.RevealNotes ? [RevealNotes] : []
  }).catch(() => { document.getElementById('load-error').hidden = false; });
})();
