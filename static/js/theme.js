(function () {
  'use strict';

  const html = document.documentElement;
  const btn = document.getElementById('themeToggle');

  if (!btn) {
    console.warn('[EcoSort] Theme toggle button not found');
    return;
  }

  btn.addEventListener('click', () => {
    const current = html.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('ecosort-theme', next);
    console.log('[EcoSort] Theme →', next);
  });
})();