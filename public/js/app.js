// CampusPulse Client-Side Application Logic (Student & Faculty Portal)

document.addEventListener('DOMContentLoaded', () => {
  // Elements
  const grievanceForm = document.getElementById('grievanceForm');
  const ticketTitle = document.getElementById('ticketTitle');
  const titleCounter = document.getElementById('titleCounter');
  const ticketDescription = document.getElementById('ticketDescription');
  const descCounter = document.getElementById('descCounter');
  const ticketCategory = document.getElementById('ticketCategory');
  const ticketFacility = document.getElementById('ticketFacility');
  const ticketImage = document.getElementById('ticketImage');
  const btnPreviewSubmit = document.getElementById('btnPreviewSubmit');
  const btnConfirmSubmit = document.getElementById('btnConfirmSubmit');

  // Modal & Toast Instances
  const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
  const toastEl = document.getElementById('liveToast');
  const toast = new bootstrap.Toast(toastEl, { delay: 6000 });
  const toastMessage = document.getElementById('toastMessage');

  // Tracking Elements
  const btnTrackTicket = document.getElementById('btnTrackTicket');
  const searchUuidInput = document.getElementById('searchUuidInput');
  const trackResultCard = document.getElementById('trackResultCard');
  const sampleUuidBtns = document.querySelectorAll('.sample-uuid-btn');

  // Facilities Grid Element
  const facilitiesGrid = document.getElementById('facilitiesGrid');
  const btnRefreshFacilities = document.getElementById('btnRefreshFacilities');

  // Global cached facilities
  let facilitiesList = [];

  // 1. Initialize Facilities Dropdown
  async function loadFacilities() {
    try {
      const res = await fetch('/api/v1/facilities');
      const data = await res.json();
      if (data.success) {
        facilitiesList = data.data;
        ticketFacility.innerHTML = '<option value="" selected disabled>Select affected facility...</option>';
        facilitiesList.forEach(fac => {
          const opt = document.createElement('option');
          opt.value = fac.facility_id;
          opt.textContent = `${fac.building_name} — ${fac.room_number} (${fac.facility_type})`;
          ticketFacility.appendChild(opt);
        });
        renderFacilitiesGrid(facilitiesList);
      }
    } catch (err) {
      console.error('Failed to load facilities:', err);
    }
  }

  // Render Facility Grid
  function renderFacilitiesGrid(list) {
    if (!facilitiesGrid) return;
    facilitiesGrid.innerHTML = '';
    list.forEach(f => {
      const col = document.createElement('div');
      col.className = 'col-md-6 col-lg-3';
      const statusBadge = f.status === 'operational' 
        ? '<span class="badge bg-success-subtle text-success border border-success-subtle">Operational</span>' 
        : '<span class="badge bg-warning-subtle text-warning border border-warning-subtle">Maintenance Req.</span>';

      col.innerHTML = `
        <div class="custom-card p-3 h-100">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <span class="badge bg-light text-secondary border text-uppercase" style="font-size: 0.65rem;">Floor ${f.floor_number}</span>
            ${statusBadge}
          </div>
          <h5 class="h6 fw-bold mb-1">${f.building_name}</h5>
          <p class="small text-muted mb-2">${f.room_number}</p>
          <div class="d-flex justify-content-between align-items-center pt-2 border-top mt-auto small">
            <span class="text-secondary"><i class="bi bi-tag me-1"></i>${f.facility_type}</span>
            <span class="badge ${f.active_tickets > 0 ? 'bg-danger' : 'bg-secondary'} rounded-pill">${f.active_tickets || 0} active</span>
          </div>
        </div>
      `;
      facilitiesGrid.appendChild(col);
    });
  }

  // 2. Character Counters
  ticketTitle.addEventListener('input', () => {
    titleCounter.textContent = ticketTitle.value.length;
  });

  ticketDescription.addEventListener('input', () => {
    descCounter.textContent = ticketDescription.value.length;
  });

  // 3. Form Preview in Modal
  btnPreviewSubmit.addEventListener('click', () => {
    // Basic HTML5 validation trigger
    if (!grievanceForm.checkValidity()) {
      grievanceForm.classList.add('was-validated');
      return;
    }

    const title = ticketTitle.value.trim();
    const desc = ticketDescription.value.trim();
    const category = ticketCategory.value;
    const facilityId = ticketFacility.value;
    const urgency = document.querySelector('input[name="urgencyRadio"]:checked')?.value || 'medium';

    if (title.length < 3 || desc.length < 10 || !category || !facilityId) {
      showToast('Please fill all required fields properly.', 'danger');
      return;
    }

    const selectedFacility = facilitiesList.find(f => f.facility_id == facilityId);

    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalCategory').textContent = category.toUpperCase();
    document.getElementById('modalLocation').textContent = selectedFacility ? `${selectedFacility.building_name} (${selectedFacility.room_number})` : '-';
    
    const modalUrgency = document.getElementById('modalUrgency');
    modalUrgency.textContent = urgency.toUpperCase();
    modalUrgency.className = `badge bg-${urgency === 'critical' ? 'dark' : urgency === 'high' ? 'danger' : urgency === 'medium' ? 'warning text-dark' : 'success'}`;

    confirmationModal.show();
  });

  // 4. Confirm & Lodge Ticket (POST)
  btnConfirmSubmit.addEventListener('click', async () => {
    confirmationModal.hide();

    const payload = {
      title: ticketTitle.value.trim(),
      description: ticketDescription.value.trim(),
      category: ticketCategory.value,
      urgency_level: document.querySelector('input[name="urgencyRadio"]:checked')?.value || 'medium',
      facility_id: parseInt(ticketFacility.value, 10),
      image_url: ticketImage.value.trim() || null,
      created_by: 1 // Default demo student
    };

    try {
      const res = await fetch('/api/v1/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showToast(`Grievance lodged! UUID: ${data.ticket_uuid}`, 'success');
        grievanceForm.reset();
        grievanceForm.classList.remove('was-validated');
        titleCounter.textContent = '0';
        descCounter.textContent = '0';

        // Auto-switch to tracking tab and track this ticket
        setTimeout(() => {
          const trackTabTrigger = new bootstrap.Tab(document.getElementById('track-tab'));
          trackTabTrigger.show();
          searchUuidInput.value = data.ticket_uuid;
          trackTicket(data.ticket_uuid);
        }, 1200);

        // Refresh facility metrics
        loadFacilities();
      } else {
        showToast(data.message || 'Failed to submit grievance.', 'danger');
      }
    } catch (err) {
      console.error('Error lodging ticket:', err);
      showToast('Network error while lodging ticket.', 'danger');
    }
  });

  // 5. Track Ticket By UUID
  async function trackTicket(uuid) {
    if (!uuid || uuid.trim().length === 0) {
      showToast('Please enter a ticket UUID to track.', 'warning');
      return;
    }

    try {
      const res = await fetch(`/api/v1/tickets/${encodeURIComponent(uuid.trim())}`);
      const data = await res.json();

      if (res.ok && data.success) {
        const ticket = data.data;
        trackResultCard.classList.remove('d-none');

        document.getElementById('resTitle').textContent = ticket.title;
        document.getElementById('resUuid').textContent = ticket.ticket_uuid;
        document.getElementById('resLocation').textContent = `${ticket.building_name} — ${ticket.room_number}`;
        document.getElementById('resCategory').textContent = ticket.category.toUpperCase();
        document.getElementById('resDescription').textContent = ticket.description;
        document.getElementById('resDate').textContent = new Date(ticket.created_at).toLocaleString();

        // Status Badge
        const statusBadge = document.getElementById('resStatusBadge');
        statusBadge.textContent = ticket.status.replace('_', ' ');
        statusBadge.className = `badge-status badge-${ticket.status} mb-2 d-inline-block`;

        // Urgency Badge
        const urgencyBadge = document.getElementById('resUrgencyBadge');
        urgencyBadge.textContent = ticket.urgency_level.toUpperCase();
        urgencyBadge.className = `badge bg-${ticket.urgency_level === 'critical' ? 'dark' : ticket.urgency_level === 'high' ? 'danger' : ticket.urgency_level === 'medium' ? 'warning text-dark' : 'success'}`;

        // Timeline Render
        const timeline = document.getElementById('resTimeline');
        timeline.innerHTML = '';
        if (ticket.timeline && ticket.timeline.length > 0) {
          ticket.timeline.forEach(log => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
              <div class="timeline-marker"></div>
              <div class="d-flex justify-content-between align-items-center">
                <strong class="small text-dark text-uppercase">${log.new_status.replace('_', ' ')}</strong>
                <span class="text-muted" style="font-size: 0.75rem;">${new Date(log.timestamp).toLocaleString()}</span>
              </div>
              <p class="small text-secondary mb-1">${log.remarks || 'Status updated.'}</p>
              <small class="text-muted">By: ${log.changed_by_name}</small>
            `;
            timeline.appendChild(item);
          });
        } else {
          timeline.innerHTML = '<p class="text-muted small">No audit logs available for this ticket.</p>';
        }

      } else {
        trackResultCard.classList.add('d-none');
        showToast(data.message || 'Ticket not found.', 'danger');
      }
    } catch (err) {
      console.error('Error tracking ticket:', err);
      showToast('Failed to retrieve ticket information.', 'danger');
    }
  }

  btnTrackTicket.addEventListener('click', () => {
    trackTicket(searchUuidInput.value);
  });

  sampleUuidBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const uuid = btn.getAttribute('data-uuid');
      searchUuidInput.value = uuid;
      trackTicket(uuid);
    });
  });

  if (btnRefreshFacilities) {
    btnRefreshFacilities.addEventListener('click', loadFacilities);
  }

  // Toast Helper
  function showToast(msg, variant = 'success') {
    toastEl.className = `toast align-items-center text-white bg-${variant} border-0`;
    toastMessage.textContent = msg;
    toast.show();
  }

  // Initial Load
  loadFacilities();
});
