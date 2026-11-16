// CampusPulse Executive BI & Dashboard JavaScript (Module 1)
// Enhanced Edition v2.0 with Interactive 2D SVG Campus Map, Donut Center Metric, Timeframe Slicer & Dark Mode

document.addEventListener('DOMContentLoaded', () => {
  let categoryChartInstance = null;
  let trendChartInstance = null;
  let buildingChartInstance = null;

  // DOM Elements
  const kpiTotal = document.getElementById('kpiTotal');
  const kpiResolved = document.getElementById('kpiResolved');
  const kpiActive = document.getElementById('kpiActive');
  const kpiCritical = document.getElementById('kpiCritical');
  const kpiMttr = document.getElementById('kpiMttr');
  const kpiSla = document.getElementById('kpiSla');
  const slaProgressBar = document.getElementById('slaProgressBar');
  const btnRefreshAnalytics = document.getElementById('btnRefreshAnalytics');
  const btnExportData = document.getElementById('btnExportData');

  // Theme Elements
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');

  // Timeframe Elements
  const timeframeAll = document.getElementById('timeframeAll');
  const timeframe30 = document.getElementById('timeframe30');
  const timeframe7 = document.getElementById('timeframe7');

  // Map Inspector Elements
  const inspBuildingName = document.getElementById('inspBuildingName');
  const inspStatusBadge = document.getElementById('inspStatusBadge');
  const inspDetails = document.getElementById('inspDetails');

  let cachedHotspots = [];
  let currentTimeframe = 'all';

  // ==========================================
  // 1. Dark Mode Theme Controller (Phase 5)
  // ==========================================
  function initTheme() {
    const savedTheme = localStorage.getItem('campuspulse-theme') || 
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    applyTheme(savedTheme);
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-bs-theme', theme);
    localStorage.setItem('campuspulse-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars';
    }
    // Re-render charts with theme color adjustments
    updateChartsTheme(theme);
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
  }
  initTheme();

  function updateChartsTheme(theme) {
    const textColor = theme === 'dark' ? '#94a3b8' : '#64748b';
    const gridColor = theme === 'dark' ? '#334155' : '#e2e8f0';

    [trendChartInstance, buildingChartInstance].forEach(chart => {
      if (chart && chart.options.scales) {
        if (chart.options.scales.x) {
          chart.options.scales.x.ticks.color = textColor;
          chart.options.scales.x.grid.color = gridColor;
        }
        if (chart.options.scales.y) {
          chart.options.scales.y.ticks.color = textColor;
          chart.options.scales.y.grid.color = gridColor;
        }
        chart.update();
      }
    });

    if (categoryChartInstance) {
      categoryChartInstance.update();
    }
  }

  // ==========================================
  // 2. Fetch and Render KPIs
  // ==========================================
  async function loadKpis() {
    try {
      const res = await fetch('/api/v1/analytics/kpis');
      const data = await res.json();
      if (data.success) {
        const k = data.data;
        kpiTotal.textContent = k.total_tickets;
        kpiResolved.textContent = k.resolved_tickets;
        kpiActive.textContent = k.active_tickets;
        kpiCritical.textContent = k.critical_active;
        kpiMttr.textContent = k.mttr_hours !== null ? k.mttr_hours : '0.0';
        kpiSla.textContent = k.sla_compliance_rate;
        slaProgressBar.style.width = `${k.sla_compliance_rate}%`;
      }
    } catch (err) {
      console.error('Failed to load KPIs:', err);
    }
  }

  // ==========================================
  // 3. Category Doughnut Chart with Center Metric (Phase 3)
  // ==========================================
  const centerTextPlugin = {
    id: 'centerTextPlugin',
    afterDraw(chart) {
      if (chart.config.type !== 'doughnut') return;
      const { ctx, chartArea: { top, width, height } } = chart;
      ctx.save();
      
      const total = chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
      const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
      
      ctx.font = 'bold 22px system-ui';
      ctx.fillStyle = isDark ? '#f1f5f9' : '#0f172a';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${total}`, width / 2, top + (height / 2) - 8);

      ctx.font = '500 11px system-ui';
      ctx.fillStyle = isDark ? '#94a3b8' : '#64748b';
      ctx.fillText('INCIDENTS', width / 2, top + (height / 2) + 12);
      ctx.restore();
    }
  };

  async function loadCategoryChart() {
    try {
      const res = await fetch('/api/v1/analytics/categories');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        const labels = data.data.map(d => d.category.toUpperCase());
        const counts = data.data.map(d => d.count);

        const ctx = document.getElementById('categoryChart').getContext('2d');
        if (categoryChartInstance) categoryChartInstance.destroy();

        categoryChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels,
            datasets: [{
              data: counts,
              backgroundColor: [
                '#3b82f6', // IT
                '#f59e0b', // Electrical
                '#06b6d4', // Plumbing
                '#8b5cf6', // Furniture
                '#10b981', // Cleanliness
                '#64748b', // Civil
                '#ef4444'  // Safety
              ],
              borderWidth: 2,
              borderColor: document.documentElement.getAttribute('data-bs-theme') === 'dark' ? '#1e293b' : '#ffffff'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: {
                  boxWidth: 12,
                  font: { size: 11 },
                  color: document.documentElement.getAttribute('data-bs-theme') === 'dark' ? '#94a3b8' : '#64748b'
                }
              }
            },
            cutout: '72%'
          },
          plugins: [centerTextPlugin]
        });
      }
    } catch (err) {
      console.error('Failed to load category chart:', err);
    }
  }

  // ==========================================
  // 4. Time Series Trend Chart with Segmented Filter
  // ==========================================
  async function loadTrendChart() {
    try {
      const res = await fetch('/api/v1/analytics/time-series');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        let filteredData = data.data;
        if (currentTimeframe === '7') {
          filteredData = filteredData.slice(-7);
        } else if (currentTimeframe === '30') {
          filteredData = filteredData.slice(-30);
        }

        const labels = filteredData.map(d => d.report_date);
        const reported = filteredData.map(d => d.reported_count);
        const resolved = filteredData.map(d => d.resolved_count);

        const ctx = document.getElementById('trendChart').getContext('2d');
        if (trendChartInstance) trendChartInstance.destroy();

        const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';
        const gridColor = isDark ? '#334155' : '#e2e8f0';

        trendChartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels,
            datasets: [
              {
                label: 'Reported Grievances',
                data: reported,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                tension: 0.35,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
              },
              {
                label: 'Resolved Issues',
                data: resolved,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.35,
                fill: true,
                pointRadius: 4,
                pointHoverRadius: 6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                ticks: { color: textColor },
                grid: { color: gridColor }
              },
              y: {
                beginAtZero: true,
                ticks: { stepSize: 1, color: textColor },
                grid: { color: gridColor }
              }
            },
            plugins: {
              legend: {
                position: 'top',
                labels: { boxWidth: 12, color: textColor }
              }
            }
          }
        });
      }
    } catch (err) {
      console.error('Failed to load trend chart:', err);
    }
  }

  // Timeframe Buttons Listener (Phase 3)
  [timeframeAll, timeframe30, timeframe7].forEach(radio => {
    if (radio) {
      radio.addEventListener('change', () => {
        if (timeframe7.checked) currentTimeframe = '7';
        else if (timeframe30.checked) currentTimeframe = '30';
        else currentTimeframe = 'all';
        loadTrendChart();
      });
    }
  });

  // ==========================================
  // 5. Building Breakdown Bar Chart
  // ==========================================
  async function loadBuildingChart() {
    try {
      const res = await fetch('/api/v1/analytics/buildings');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        const labels = data.data.map(d => d.building_name);
        const openTickets = data.data.map(d => d.open_tickets);
        const resolvedTickets = data.data.map(d => d.resolved_tickets);

        const ctx = document.getElementById('buildingChart').getContext('2d');
        if (buildingChartInstance) buildingChartInstance.destroy();

        const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        const textColor = isDark ? '#94a3b8' : '#64748b';
        const gridColor = isDark ? '#334155' : '#e2e8f0';

        buildingChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Open Faults',
                data: openTickets,
                backgroundColor: '#f59e0b',
                borderRadius: 4
              },
              {
                label: 'Resolved',
                data: resolvedTickets,
                backgroundColor: '#10b981',
                borderRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { stacked: true, ticks: { color: textColor }, grid: { color: gridColor } },
              y: { stacked: true, beginAtZero: true, ticks: { color: textColor }, grid: { color: gridColor } }
            },
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12, color: textColor } }
            }
          }
        });
      }
    } catch (err) {
      console.error('Failed to load building chart:', err);
    }
  }

  // ==========================================
  // 6. Interactive 2D SVG Campus Blueprint (Phase 3)
  // ==========================================
  async function loadHotspotsAndMap() {
    try {
      const res = await fetch('/api/v1/analytics/hotspots');
      const data = await res.json();
      if (data.success) {
        cachedHotspots = data.data;

        // Group by building name
        const buildingCounts = {};
        cachedHotspots.forEach(h => {
          if (!buildingCounts[h.building_name]) buildingCounts[h.building_name] = 0;
          buildingCounts[h.building_name] += h.open_tickets;
        });

        // Update SVG Pin Counters
        const pinCsd = document.getElementById('pin-csd');
        const pinAcad = document.getElementById('pin-acad');
        const pinLib = document.getElementById('pin-lib');
        const pinHostel = document.getElementById('pin-hostel');
        const pinSports = document.getElementById('pin-sports');
        const pinCafe = document.getElementById('pin-cafe');

        if (pinCsd) pinCsd.textContent = buildingCounts['CSD Department Block'] || 0;
        if (pinAcad) pinAcad.textContent = buildingCounts['Main Academic Complex'] || 0;
        if (pinLib) pinLib.textContent = buildingCounts['Library Building'] || 0;
        if (pinHostel) pinHostel.textContent = (buildingCounts['Boys Hostel Block A'] || 0) + (buildingCounts['Girls Hostel Block B'] || 0);
        if (pinSports) pinSports.textContent = buildingCounts['Indoor Sports Complex'] || 0;
        if (pinCafe) pinCafe.textContent = buildingCounts['Central Cafeteria'] || 0;

        // Attach interactive click listeners to SVG building groups
        document.querySelectorAll('.building-group').forEach(group => {
          group.addEventListener('click', () => {
            const bName = group.getAttribute('data-bname');
            selectBuildingOnMap(bName);
          });
        });

        // Pre-select CSD Block by default
        selectBuildingOnMap('CSD Department Block');
      }
    } catch (err) {
      console.error('Failed to load hotspots for map:', err);
    }
  }

  function selectBuildingOnMap(buildingName) {
    // Highlight SVG building
    document.querySelectorAll('.map-building-path').forEach(p => p.classList.remove('active-building'));
    const selectedGroup = document.querySelector(`.building-group[data-bname="${buildingName}"]`);
    if (selectedGroup) {
      const path = selectedGroup.querySelector('.map-building-path');
      if (path) path.classList.add('active-building');
    }

    // Inspect building details
    const buildingRooms = cachedHotspots.filter(h => h.building_name === buildingName || (buildingName.includes('Hostel') && h.building_name.includes('Hostel')));
    const totalOpen = buildingRooms.reduce((sum, r) => sum + r.open_tickets, 0);

    inspBuildingName.textContent = buildingName;
    if (totalOpen > 0) {
      inspStatusBadge.textContent = `${totalOpen} Active Fault${totalOpen > 1 ? 's' : ''}`;
      inspStatusBadge.className = totalOpen > 2 ? 'badge bg-danger' : 'badge bg-warning text-dark';
    } else {
      inspStatusBadge.textContent = 'All Systems Operational';
      inspStatusBadge.className = 'badge bg-success';
    }

    if (buildingRooms.length > 0) {
      const roomDetails = buildingRooms.map(r => 
        `<strong>${r.room_number}</strong> (${r.facility_type}): <span class="${r.open_tickets > 0 ? 'text-danger fw-bold' : 'text-success'}">${r.open_tickets} active</span>`
      ).join(' &bull; ');
      inspDetails.innerHTML = roomDetails;
    } else {
      inspDetails.textContent = 'Zero reported maintenance issues in this facility block.';
    }
  }

  // ==========================================
  // 7. CSV Export for Tableau / Power-BI
  // ==========================================
  btnExportData.addEventListener('click', async () => {
    try {
      const res = await fetch('/api/v1/tickets');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        const headers = ['ticket_uuid', 'title', 'category', 'urgency_level', 'status', 'building_name', 'room_number', 'created_at', 'resolved_at'];
        const csvRows = [headers.join(',')];

        data.data.forEach(row => {
          const values = headers.map(header => {
            const val = row[header] === null || row[header] === undefined ? '' : String(row[header]).replace(/"/g, '""');
            return `"${val}"`;
          });
          csvRows.push(values.join(','));
        });

        const csvString = csvRows.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.setAttribute('href', url);
        link.setAttribute('download', `campuspulse_export_${new Date().toISOString().slice(0, 10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    } catch (err) {
      console.error('Failed to export CSV:', err);
      alert('Failed to generate export file.');
    }
  });

  if (btnRefreshAnalytics) {
    btnRefreshAnalytics.addEventListener('click', () => {
      loadKpis();
      loadCategoryChart();
      loadTrendChart();
      loadBuildingChart();
      loadHotspotsAndMap();
    });
  }

  // Orchestrate Initial Load
  loadKpis();
  loadCategoryChart();
  loadTrendChart();
  loadBuildingChart();
  loadHotspotsAndMap();
});
