document.addEventListener('DOMContentLoaded', () => {
  const banner = document.querySelector('.ecoscore-banner');
  if (!banner) return;

  const score = parseFloat(banner.dataset.score) || 0;
  const circle = banner.querySelector('.score-circle');
  const numEl = banner.querySelector('.score-num');

  let color = '#dc2626';
  if (score >= 80) color = '#16a34a';
  else if (score >= 60) color = '#65a30d';
  else if (score >= 40) color = '#f59e0b';

  circle.style.background = `conic-gradient(${color} ${score * 3.6}deg, #e5e7eb 0deg)`;

  let cur = 0;
  const step = score / 30;
  const timer = setInterval(() => {
    cur += step;
    if (cur >= score) { cur = score; clearInterval(timer); }
    numEl.textContent = cur.toFixed(1);
  }, 20);
});