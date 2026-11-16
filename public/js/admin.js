// CampusPulse Operations Board JavaScript (Admin & Facility Supervisors)

document.addEventListener('DOMContentLoaded', () => {
  const ticketsTableBody = document.getElementById('ticketsTableBody');
  const ticketsCount = document.getElementById('ticketsCount');
  const filterSearch = document.getElementById('filterSearch');
  const filterStatus = document.getElementById('filterStatus');
  const filterCategory = document.getElementById('filterCategory');
  const filterUrgency = document.getElementById('filterUrgency');
  const btnRefreshTickets = document.getElementById('btnRefreshTickets');

  // Modal Elements
  const triageModalEl = document.getElementById('triageModal');
  const triageModal = new bootstrap.Modal(triageModalEl);
  const triageModalTitle = document.getElementById('triageModalTitle');
  const triageModalLoc = document.getElementById('triageModalLoc');
  const newStatusSelect = document.getElementById('newStatusSelect');
  const remarksInput = document.getElementById('remarksInput');
  const btnSaveStatus = document.getElementById('btnSaveStatus');

  // Toast
  const toastEl = document.getElementById('adminToast');
  const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
  const toastMessage = document.getElementById('adminToastMessage');

  let activeTicketUuid = null;
  let cachedTickets = [];

  // Fetch tickets with query params
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
        renderTicketsTable(cachedTickets);
      }
    } catch (err) {
      console.error('Failed to load tickets:', err);
      ticketsTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4">Error loading tickets from backend.</td></tr>`;
    }
  }

  // Render Table Rows
  function renderTicketsTable(tickets) {
    ticketsCount.textContent = tickets.length;
    if (tickets.length === 0) {
      ticketsTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">No tickets match the selected filters.</td></tr>`;
      return;
    }

    ticketsTableBody.innerHTML = '';
    tickets.forEach(t => {
      const tr = document.createElement('tr');

      const urgencyBadge = `
        <span class="badge bg-${t.urgency_level === 'critical' ? 'dark' : t.urgency_level === 'high' ? 'danger' : t.urgency_level === 'medium' ? 'warning text-dark' : 'success'} text-uppercase">
          ${t.urgency_level}
        </span>
      `;

      const statusBadge = `
        <span class="badge-status badge-${t.status}">
          ${t.status.replace('_', ' ')}
        </span>
      `;

      tr.innerHTML = `
        <td>
          <div class="fw-bold text-dark">${escapeHtml(t.title)}</div>
          <div class="small text-muted"><span class="badge bg-light text-secondary border me-1">${t.category}</span> ${t.ticket_uuid.substring(0, 8)}...</div>
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

    // Attach click listeners to triage buttons
    document.querySelectorAll('.btn-triage').forEach(btn => {
      btn.addEventListener('click', () => {
        const uuid = btn.getAttribute('data-uuid');
        openTriageModal(uuid);
      });
    });
  }

  // Open Triage Modal
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

  // Save Status Update (PATCH)
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
          changed_by: 4 // Facility Manager ID
        })
      });
      const data = await res.json();

      if (res.ok && data.success) {
        triageModal.hide();
        showToast(data.message, 'success');
        fetchTickets(); // Refresh table
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

  // Initial load
  fetchTickets();
});
