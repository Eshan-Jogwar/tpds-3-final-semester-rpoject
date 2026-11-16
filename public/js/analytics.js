// CampusPulse Executive BI & Dashboard JavaScript (Module 1)

document.addEventListener('DOMContentLoaded', () => {
  // Chart instances
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
  const campusHotspotGrid = document.getElementById('campusHotspotGrid');
  const btnRefreshAnalytics = document.getElementById('btnRefreshAnalytics');
  const btnExportData = document.getElementById('btnExportData');

  // 1. Fetch and Render KPIs
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

  // 2. Category Doughnut Chart
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
              borderColor: '#ffffff'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom',
                labels: { boxWidth: 12, font: { size: 11 } }
              }
            },
            cutout: '65%'
          }
        });
      }
    } catch (err) {
      console.error('Failed to load category chart:', err);
    }
  }

  // 3. Time Series Velocity Chart
  async function loadTrendChart() {
    try {
      const res = await fetch('/api/v1/analytics/time-series');
      const data = await res.json();
      if (data.success && data.data.length > 0) {
        const labels = data.data.map(d => d.report_date);
        const reported = data.data.map(d => d.reported_count);
        const resolved = data.data.map(d => d.resolved_count);

        const ctx = document.getElementById('trendChart').getContext('2d');
        if (trendChartInstance) trendChartInstance.destroy();

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
                tension: 0.3,
                fill: true,
                pointRadius: 4
              },
              {
                label: 'Resolved Issues',
                data: resolved,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.3,
                fill: true,
                pointRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: { stepSize: 1 }
              }
            },
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12 } }
            }
          }
        });
      }
    } catch (err) {
      console.error('Failed to load trend chart:', err);
    }
  }

  // 4. Building Breakdown Bar Chart
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

        buildingChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Open Faults',
                data: openTickets,
                backgroundColor: '#f59e0b'
              },
              {
                label: 'Resolved',
                data: resolvedTickets,
                backgroundColor: '#10b981'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: { stacked: true },
              y: { stacked: true, beginAtZero: true }
            },
            plugins: {
              legend: { position: 'top', labels: { boxWidth: 12 } }
            }
          }
        });
      }
    } catch (err) {
      console.error('Failed to load building chart:', err);
    }
  }

  // 5. Interactive Geospatial Campus Hotspots
  async function loadHotspots() {
    try {
      const res = await fetch('/api/v1/analytics/hotspots');
      const data = await res.json();
      if (data.success) {
        campusHotspotGrid.innerHTML = '';
        data.data.forEach(h => {
          const col = document.createElement('div');
          col.className = 'col-6 col-md-4';
          
          let alertColor = 'success';
          if (h.open_tickets > 2) alertColor = 'danger';
          else if (h.open_tickets > 0) alertColor = 'warning';

          col.innerHTML = `
            <div class="p-2 bg-white rounded border building-hotspot" title="Coordinates: ${h.latitude}, ${h.longitude}">
              <div class="d-flex justify-content-between align-items-center mb-1">
                <span class="badge bg-${alertColor}-subtle text-${alertColor} border border-${alertColor}-subtle" style="font-size: 0.65rem;">
                  <i class="bi bi-geo-alt-fill me-1"></i>${h.facility_type}
                </span>
                <span class="badge bg-${alertColor} rounded-pill">${h.open_tickets} active</span>
              </div>
              <div class="fw-semibold text-truncate small">${h.building_name}</div>
              <div class="text-muted" style="font-size: 0.75rem;">${h.room_number}</div>
            </div>
          `;
          campusHotspotGrid.appendChild(col);
        });
      }
    } catch (err) {
      console.error('Failed to load hotspots:', err);
    }
  }

  // 6. CSV Export for Tableau / Power-BI
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
      loadHotspots();
    });
  }

  // Initial Orchestration
  loadKpis();
  loadCategoryChart();
  loadTrendChart();
  loadBuildingChart();
  loadHotspots();
});
