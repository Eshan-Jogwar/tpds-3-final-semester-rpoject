// CampusPulse Operations Board JavaScript (Admin & Facility Supervisors)
// Enhanced Edition v2.0 with Column Sorting, Multi-select Bulk Actions & Dark Mode

document.addEventListener('DOMContentLoaded', () => {
  const ticketsTableBody = document.getElementById('ticketsTableBody');
  const ticketsCount = document.getElementById('ticketsCount');
  const filterSearch = document.getElementById('filterSearch');
  const filterStatus = document.getElementById('filterStatus');
  const filterCategory = document.getElementById('filterCategory');
  const filterUrgency = document.getElementById('filterUrgency');
  const btnRefreshTickets = document.getElementById('btnRefreshTickets');

  // Theme Elements
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');

  // Modal Elements
  const triageModalEl = document.getElementById('triageModal');
  const triageModal = new bootstrap.Modal(triageModalEl);
  const triageModalTitle = document.getElementById('triageModalTitle');
  const triageModalLoc = document.getElementById('triageModalLoc');
  const newStatusSelect = document.getElementById('newStatusSelect');
  const remarksInput = document.getElementById('remarksInput');
  const btnSaveStatus = document.getElementById('btnSaveStatus');

  // Bulk Actions Elements
  const selectAllCheckbox = document.getElementById('selectAllCheckbox');
  const bulkActionsBar = document.getElementById('bulkActionsBar');
  const selectedCountBadge = document.getElementById('selectedCountBadge');
  const bulkInProgressBtn = document.getElementById('bulkInProgressBtn');
  const bulkResolvedBtn = document.getElementById('bulkResolvedBtn');
  const bulkClearBtn = document.getElementById('bulkClearBtn');

  // Toast
  const toastEl = document.getElementById('adminToast');
  const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
  const toastMessage = document.getElementById('adminToastMessage');

  let activeTicketUuid = null;
  let cachedTickets = [];
  let selectedUuids = new Set();

  // Sorting state
  let currentSort = {
    column: 'created_at',
    ascending: false
  };

  // ==========================================
  // 1. Theme Controller
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
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });
  }
  initTheme();

  // ==========================================
  // 2. Fetch Tickets
  // ==========================================
  async function fetchTickets() {
    try {
      const search = filterSearch.value.trim();
      const status = filterStatus.value;
      const category = filterCategory.value;
      const urgency = filterUrgency.value;

      const params = new URLSearchParams();
      if (search) params.append('search', search);
      if (status !== 'all') params.append('status', status);
      if (category !== 'all') params.append('category', category);
      if (urgency !== 'all') params.append('urgency', urgency);

      const res = await fetch(`/api/v1/tickets?${params.toString()}`);
      const data = await res.json();

      if (data.success) {
        cachedTickets = data.data;
        sortAndRenderTickets();
      }
    } catch (err) {
      console.error('Failed to load tickets:', err);
      ticketsTableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger py-4">Error loading tickets from backend.</td></tr>`;
    }
  }

  // ==========================================
  // 3. Sorting Engine (Phase 4)
  // ==========================================
  function sortAndRenderTickets() {
    const { column, ascending } = currentSort;

    cachedTickets.sort((a, b) => {
      let valA = a[column];
      let valB = b[column];

      if (column === 'urgency_level') {
        const order = { critical: 4, high: 3, medium: 2, low: 1 };
        valA = order[valA] || 0;
        valB = order[valB] || 0;
      } else if (typeof valA === 'string') {
        valA = valA.toLowerCase();
        valB = (valB || '').toLowerCase();
      }

      if (valA < valB) return ascending ? -1 : 1;
      if (valA > valB) return ascending ? 1 : -1;
      return 0;
    });

    renderTicketsTable(cachedTickets);
  }

  document.querySelectorAll('th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.getAttribute('data-sort');
      if (currentSort.column === col) {
        currentSort.ascending = !currentSort.ascending;
      } else {
        currentSort.column = col;
        currentSort.ascending = true;
      }

      // Update header indicators
      document.querySelectorAll('th.sortable i').forEach(icon => {
        icon.className = 'bi bi-arrow-down-up ms-1';
      });
      const currentIcon = th.querySelector('i');
      if (currentIcon) {
        currentIcon.className = currentSort.ascending ? 'bi bi-arrow-up ms-1 text-primary' : 'bi bi-arrow-down ms-1 text-primary';
      }

      sortAndRenderTickets();
    });
  });

  // ==========================================
  // 4. Render Table Rows with Selection
  // ==========================================
  function renderTicketsTable(tickets) {
    ticketsCount.textContent = tickets.length;
    if (tickets.length === 0) {
      ticketsTableBody.innerHTML = `<tr><td colspan="8" class="text-center text-muted py-4">No tickets match the selected filters.</td></tr>`;
      updateBulkActionsBar();
      return;
    }

    ticketsTableBody.innerHTML = '';
    tickets.forEach(t => {
      const tr = document.createElement('tr');
      const isChecked = selectedUuids.has(t.ticket_uuid);

      const urgencyBadge = `
        <span class="badge bg-${t.urgency_level === 'critical' ? 'dark' : t.urgency_level === 'high' ? 'danger' : t.urgency_level === 'medium' ? 'warning text-dark' : 'success'} text-uppercase" style="letter-spacing: 0.3px;">
          ${t.urgency_level}
        </span>
      `;

      // Notice badge-status has white-space: nowrap in CSS
      const statusBadge = `
        <span class="badge-status badge-${t.status}">
          ${t.status.replace('_', ' ')}
        </span>
      `;

      tr.innerHTML = `
        <td class="text-center">
          <input type="checkbox" class="form-check-input ticket-row-cb" data-uuid="${t.ticket_uuid}" ${isChecked ? 'checked' : ''}>
        </td>
        <td>
          <div class="fw-bold">${escapeHtml(t.title)}</div>
          <div class="small text-muted"><span class="badge bg-secondary-subtle text-secondary border me-1">${t.category}</span> ${t.ticket_uuid.substring(0, 8)}...</div>
        </td>
        <td>
          <div class="small fw-semibold">${t.building_name}</div>
          <div class="small text-muted">${t.room_number}</div>
        </td>
        <td>${urgencyBadge}</td>
        <td>${statusBadge}</td>
        <td>
          <div class="small fw-semibold">${t.created_by_name}</div>
          <div class="small text-muted" style="font-size: 0.75rem;">${t.created_by_email}</div>
        </td>
        <td><small class="text-muted">${new Date(t.created_at).toLocaleDateString()}</small></td>
        <td class="text-end">
          <button class="btn btn-outline-primary btn-sm py-1 px-2 btn-triage" data-uuid="${t.ticket_uuid}">
            <i class="bi bi-pencil-square me-1"></i> Triage
          </button>
        </td>
      `;

      ticketsTableBody.appendChild(tr);
    });

    // Row Checkbox Listeners
    document.querySelectorAll('.ticket-row-cb').forEach(cb => {
      cb.addEventListener('change', (e) => {
        const uuid = e.target.getAttribute('data-uuid');
        if (e.target.checked) {
          selectedUuids.add(uuid);
        } else {
          selectedUuids.delete(uuid);
        }
        updateBulkActionsBar();
      });
    });

    // Triage Button Listeners
    document.querySelectorAll('.btn-triage').forEach(btn => {
      btn.addEventListener('click', () => {
        const uuid = btn.getAttribute('data-uuid');
        openTriageModal(uuid);
      });
    });

    updateBulkActionsBar();
  }

  // ==========================================
  // 5. Bulk Actions Engine (Phase 4)
  // ==========================================
  function updateBulkActionsBar() {
    const count = selectedUuids.size;
    selectedCountBadge.textContent = count;
    if (count > 0) {
      bulkActionsBar.classList.remove('d-none');
    } else {
      bulkActionsBar.classList.add('d-none');
    }

    if (selectAllCheckbox) {
      selectAllCheckbox.checked = count > 0 && count === cachedTickets.length;
    }
  }

  selectAllCheckbox.addEventListener('change', (e) => {
    if (e.target.checked) {
      cachedTickets.forEach(t => selectedUuids.add(t.ticket_uuid));
    } else {
      selectedUuids.clear();
    }
    document.querySelectorAll('.ticket-row-cb').forEach(cb => cb.checked = e.target.checked);
    updateBulkActionsBar();
  });

  bulkClearBtn.addEventListener('click', () => {
    selectedUuids.clear();
    document.querySelectorAll('.ticket-row-cb').forEach(cb => cb.checked = false);
    updateBulkActionsBar();
  });

  async function executeBulkStatusUpdate(newStatus, defaultRemark) {
    if (selectedUuids.size === 0) return;
    const count = selectedUuids.size;

    let successCount = 0;
    for (const uuid of Array.from(selectedUuids)) {
      try {
        const res = await fetch(`/api/v1/tickets/${uuid}/status`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            status: newStatus,
            remarks: defaultRemark,
            changed_by: 4
          })
        });
        if (res.ok) successCount++;
      } catch (err) {
        console.error('Failed to update ticket:', uuid, err);
      }
    }

    selectedUuids.clear();
    showToast(`Bulk updated ${successCount} of ${count} tickets to ${newStatus}.`, 'success');
    fetchTickets();
  }

  bulkInProgressBtn.addEventListener('click', () => {
    executeBulkStatusUpdate('in_progress', 'Bulk dispatched by facility supervisor.');
  });

  bulkResolvedBtn.addEventListener('click', () => {
    executeBulkStatusUpdate('resolved', 'Bulk verified and resolved by facility team.');
  });

  // ==========================================
  // 6. Single Triage Modal
  // ==========================================
  function openTriageModal(uuid) {
    const ticket = cachedTickets.find(t => t.ticket_uuid === uuid);
    if (!ticket) return;

    activeTicketUuid = uuid;
    triageModalTitle.textContent = ticket.title;
    triageModalLoc.textContent = `${ticket.building_name} (${ticket.room_number})`;
    newStatusSelect.value = ticket.status;
    remarksInput.value = '';

    triageModal.show();
  }

  btnSaveStatus.addEventListener('click', async () => {
    if (!activeTicketUuid) return;

    const newStatus = newStatusSelect.value;
    const remarks = remarksInput.value.trim();

    if (!remarks) {
      remarksInput.focus();
      remarksInput.classList.add('is-invalid');
      return;
    }
    remarksInput.classList.remove('is-invalid');

    try {
      const res = await fetch(`/api/v1/tickets/${activeTicketUuid}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          status: newStatus,
          remarks,
          changed_by: 4
        })
      });
      const data = await res.json();

      if (res.ok && data.success) {
        triageModal.hide();
        showToast(data.message, 'success');
        fetchTickets();
      } else {
        showToast(data.message || 'Failed to update ticket.', 'danger');
      }
    } catch (err) {
      console.error('Error updating status:', err);
      showToast('Network error updating status.', 'danger');
    }
  });

  // Filter Listeners
  let debounceTimeout;
  filterSearch.addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(fetchTickets, 300);
  });
  filterStatus.addEventListener('change', fetchTickets);
  filterCategory.addEventListener('change', fetchTickets);
  filterUrgency.addEventListener('change', fetchTickets);
  btnRefreshTickets.addEventListener('click', fetchTickets);

  function showToast(msg, variant = 'success') {
    toastEl.className = `toast align-items-center text-white bg-${variant} border-0`;
    toastMessage.textContent = msg;
    toast.show();
  }

  function escapeHtml(str) {
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  }

  fetchTickets();
});
