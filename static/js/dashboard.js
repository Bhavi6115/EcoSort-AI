(function () {
  'use strict';

  let materialTotals = {};
  let history = [];

  const dataEl = document.getElementById('dashboard-data');
  if (dataEl) {
    try {
      const parsed = JSON.parse(dataEl.textContent);
      materialTotals = parsed.materialTotals || {};
      history = parsed.history || [];
    } catch (e) {
      console.error('[EcoSort] JSON parse failed:', e);
    }
  }

  if (typeof Chart === 'undefined') {
    console.error('[EcoSort] Chart.js not loaded');
    return;
  }

  const COLORS = {
    cardboard: '#b4783c',
    paper:     '#2563eb',
    plastic:   '#dc2626',
    glass:     '#16a34a',
    metal:     '#eab308',
    trash:     '#111827',
  };

  // Material Distribution
  const matCanvas = document.getElementById('materialChart');
  if (matCanvas) {
    const labels = Object.keys(materialTotals);
    const values = Object.values(materialTotals);

    if (labels.length === 0) {
      new Chart(matCanvas, {
        type: 'doughnut',
        data: { labels: ['No data yet'], datasets: [{ data: [1], backgroundColor: ['#e5e7eb'], borderWidth: 0 }] },
        options: { responsive: true, maintainAspectRatio: false, cutout: '62%', plugins: { legend: { display: false }, tooltip: { enabled: false } } },
      });
    } else {
      new Chart(matCanvas, {
        type: 'doughnut',
        data: {
          labels: labels.map(l => l.charAt(0).toUpperCase() + l.slice(1)),
          datasets: [{
            data: values,
            backgroundColor: labels.map(k => COLORS[k] || '#999'),
            borderWidth: 3,
            borderColor: '#fff',
            hoverOffset: 6,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '62%',
          plugins: {
            legend: { position: 'bottom', labels: { padding: 14, usePointStyle: true, pointStyle: 'circle' } },
          },
        },
      });
    }
  }

  // EcoScore Trend
  const trendCanvas = document.getElementById('trendChart');
  if (trendCanvas) {
    let labels = [];
    let scores = [];

    if (history.length > 0) {
      labels = history.map(h => (h.timestamp || '').replace('T', ' ').slice(5, 16));
      scores = history.map(h => h.eco_score ?? 0);
    }

    if (labels.length === 0) {
      new Chart(trendCanvas, {
        type: 'line',
        data: { labels: ['No data'], datasets: [{ data: [0], borderColor: '#e5e7eb' }] },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(0,0,0,.05)' } },
            x: { grid: { display: false }, ticks: { color: '#9ca3af' } },
          },
        },
      });
    } else {
      new Chart(trendCanvas, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'EcoScore',
            data: scores,
            borderColor: '#059669',
            borderWidth: 3,
            backgroundColor: (ctx) => {
              const chart = ctx.chart;
              const { ctx: c, chartArea } = chart;
              if (!chartArea) return 'rgba(5,150,105,.1)';
              const grad = c.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
              grad.addColorStop(0, 'rgba(5, 150, 105, 0.35)');
              grad.addColorStop(1, 'rgba(5, 150, 105, 0.02)');
              return grad;
            },
            fill: true,
            tension: 0.35,
            pointRadius: 6,
            pointHoverRadius: 9,
            pointBackgroundColor: '#059669',
            pointBorderColor: '#fff',
            pointBorderWidth: 3,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true, max: 100, grid: { color: 'rgba(0,0,0,.05)' }, ticks: { color: '#6b7280', stepSize: 20 } },
            x: { grid: { display: false }, ticks: { color: '#6b7280' } },
          },
          plugins: { legend: { display: false } },
        },
      });
    }
  }
})();