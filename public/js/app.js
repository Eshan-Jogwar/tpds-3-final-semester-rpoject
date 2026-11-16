// CampusPulse Client-Side Application Logic (Student & Faculty Portal)
// Enhanced Edition v2.0 with Drag-and-Drop, Dark Mode, and 2-Column Sidebar

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
  const btnResetForm = document.getElementById('btnResetForm');

  // Drag-and-Drop Elements
  const dropzoneContainer = document.getElementById('dropzoneContainer');
  const fileInput = document.getElementById('fileInput');
  const dropzonePrompt = document.getElementById('dropzonePrompt');
  const dropzonePreview = document.getElementById('dropzonePreview');
  const previewImg = document.getElementById('previewImg');
  const removePhotoBtn = document.getElementById('removePhotoBtn');

  // Theme Toggle Elements
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');

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

  let facilitiesList = [];

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
    if (theme === 'dark') {
      themeIcon.className = 'bi bi-sun-fill text-warning';
    } else {
      themeIcon.className = 'bi bi-moon-stars';
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
  // 2. Drag & Drop File Upload Controller (Phase 2)
  // ==========================================
  if (dropzoneContainer && fileInput) {
    dropzoneContainer.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzoneContainer.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzoneContainer.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzoneContainer.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzoneContainer.classList.remove('dragover');
      });
    });

    dropzoneContainer.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        handleImageFile(files[0]);
      }
    });

    fileInput.addEventListener('change', () => {
      if (fileInput.files && fileInput.files.length > 0) {
        handleImageFile(fileInput.files[0]);
      }
    });

    removePhotoBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      resetDropzone();
    });
  }

  function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
      showToast('Please upload a valid image file (PNG, JPG, WebP).', 'warning');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      showToast('Image size exceeds 5MB limit.', 'warning');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const base64Data = e.target.result;
      previewImg.src = base64Data;
      ticketImage.value = base64Data;
      dropzonePrompt.classList.add('d-none');
      dropzonePreview.classList.remove('d-none');
    };
    reader.readAsDataURL(file);
  }

  function resetDropzone() {
    fileInput.value = '';
    ticketImage.value = '';
    previewImg.src = '';
    dropzonePreview.classList.add('d-none');
    dropzonePrompt.classList.remove('d-none');
  }

  if (btnResetForm) {
    btnResetForm.addEventListener('click', () => {
      resetDropzone();
      titleCounter.textContent = '0';
      descCounter.textContent = '0';
      grievanceForm.classList.remove('was-validated');
    });
  }

  // ==========================================
  // 3. Facilities Initialization
  // ==========================================
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
            <span class="badge bg-secondary-subtle text-secondary border text-uppercase" style="font-size: 0.65rem;">Floor ${f.floor_number}</span>
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

  // ==========================================
  // 4. Form Counters & Validation
  // ==========================================
  ticketTitle.addEventListener('input', () => {
    titleCounter.textContent = ticketTitle.value.length;
  });

  ticketDescription.addEventListener('input', () => {
    descCounter.textContent = ticketDescription.value.length;
  });

  btnPreviewSubmit.addEventListener('click', () => {
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
      showToast('Please fill in all required fields.', 'danger');
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

  // Submit Ticket
  btnConfirmSubmit.addEventListener('click', async () => {
    confirmationModal.hide();

    const payload = {
      title: ticketTitle.value.trim(),
      description: ticketDescription.value.trim(),
      category: ticketCategory.value,
      urgency_level: document.querySelector('input[name="urgencyRadio"]:checked')?.value || 'medium',
      facility_id: parseInt(ticketFacility.value, 10),
      image_url: ticketImage.value || null,
      created_by: 1
    };

    try {
      const res = await fetch('/api/v1/tickets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (res.ok && data.success) {
        showToast(`Request submitted. Ticket ID: ${data.ticket_uuid}`, 'success');
        grievanceForm.reset();
        grievanceForm.classList.remove('was-validated');
        resetDropzone();
        titleCounter.textContent = '0';
        descCounter.textContent = '0';

        setTimeout(() => {
          const trackTabTrigger = new bootstrap.Tab(document.getElementById('track-tab'));
          trackTabTrigger.show();
          searchUuidInput.value = data.ticket_uuid;
          trackTicket(data.ticket_uuid);
        }, 1000);

        loadFacilities();
      } else {
        showToast(data.message || 'Could not submit request.', 'danger');
      }
    } catch (err) {
      console.error('Error submitting ticket:', err);
      showToast('Network error submitting request.', 'danger');
    }
  });

  // ==========================================
  // 5. Track Ticket By UUID
  // ==========================================
  async function trackTicket(uuid) {
    if (!uuid || uuid.trim().length === 0) {
      showToast('Please enter a ticket ID.', 'warning');
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
        document.getElementById('resLocation').textContent = `${ticket.building_name}, ${ticket.room_number}`;
        document.getElementById('resCategory').textContent = ticket.category.toUpperCase();
        document.getElementById('resDescription').textContent = ticket.description;
        document.getElementById('resDate').textContent = new Date(ticket.created_at).toLocaleString();

        const statusBadge = document.getElementById('resStatusBadge');
        statusBadge.textContent = ticket.status.replace('_', ' ');
        statusBadge.className = `badge-status badge-${ticket.status} mb-2 d-inline-block`;

        const urgencyBadge = document.getElementById('resUrgencyBadge');
        urgencyBadge.textContent = ticket.urgency_level.toUpperCase();
        urgencyBadge.className = `badge bg-${ticket.urgency_level === 'critical' ? 'dark' : ticket.urgency_level === 'high' ? 'danger' : ticket.urgency_level === 'medium' ? 'warning text-dark' : 'success'}`;

        const photoContainer = document.getElementById('resPhotoContainer');
        const photoImg = document.getElementById('resPhotoImg');
        if (ticket.image_url) {
          photoImg.src = ticket.image_url;
          photoContainer.classList.remove('d-none');
        } else {
          photoContainer.classList.add('d-none');
        }

        const timeline = document.getElementById('resTimeline');
        timeline.innerHTML = '';
        if (ticket.timeline && ticket.timeline.length > 0) {
          ticket.timeline.forEach(log => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.innerHTML = `
              <div class="timeline-marker"></div>
              <div class="d-flex justify-content-between align-items-center">
                <strong class="small text-uppercase">${log.new_status.replace('_', ' ')}</strong>
                <span class="text-muted" style="font-size: 0.75rem;">${new Date(log.timestamp).toLocaleString()}</span>
              </div>
              <p class="small text-secondary mb-1">${log.remarks || 'Status updated.'}</p>
              <small class="text-muted">By: ${log.changed_by_name}</small>
            `;
            timeline.appendChild(item);
          });
        } else {
          timeline.innerHTML = '<p class="text-muted small">No history logged yet.</p>';
        }

      } else {
        trackResultCard.classList.add('d-none');
        showToast(data.message || 'Ticket not found.', 'danger');
      }
    } catch (err) {
      console.error('Error tracking ticket:', err);
      showToast('Could not load ticket details.', 'danger');
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

  function showToast(msg, variant = 'success') {
    toastEl.className = `toast align-items-center text-white bg-${variant} border-0`;
    toastMessage.textContent = msg;
    toast.show();
  }

  loadFacilities();
});
