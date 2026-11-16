const crypto = require('crypto');
const db = require('../db/connection');

// GET /api/v1/tickets - Retrieve tickets with optional filtering
exports.getTickets = (req, res, next) => {
  try {
    const { status, category, urgency, facility_id, search } = req.query;
    
    let query = `
      SELECT 
        t.ticket_id,
        t.ticket_uuid,
        t.title,
        t.description,
        t.category,
        t.urgency_level,
        t.status,
        t.image_url,
        t.created_at,
        t.resolved_at,
        f.facility_id,
        f.building_name,
        f.floor_number,
        f.room_number,
        f.facility_type,
        u_creator.full_name AS created_by_name,
        u_creator.email AS created_by_email,
        u_assignee.full_name AS assigned_to_name
      FROM tickets t
      JOIN facilities f ON t.facility_id = f.facility_id
      JOIN users u_creator ON t.created_by = u_creator.user_id
      LEFT JOIN users u_assignee ON t.assigned_to = u_assignee.user_id
      WHERE 1=1
    `;
    const params = [];

    if (status && status !== 'all') {
      query += ` AND t.status = ?`;
      params.push(status);
    }
    if (category && category !== 'all') {
      query += ` AND t.category = ?`;
      params.push(category);
    }
    if (urgency && urgency !== 'all') {
      query += ` AND t.urgency_level = ?`;
      params.push(urgency);
    }
    if (facility_id) {
      query += ` AND t.facility_id = ?`;
      params.push(facility_id);
    }
    if (search && search.trim() !== '') {
      query += ` AND (t.title LIKE ? OR t.description LIKE ? OR f.building_name LIKE ? OR t.ticket_uuid LIKE ?)`;
      const searchPattern = `%${search.trim()}%`;
      params.push(searchPattern, searchPattern, searchPattern, searchPattern);
    }

    query += ` ORDER BY t.created_at DESC`;

    const stmt = db.prepare(query);
    const tickets = stmt.all(...params);

    res.status(200).json({
      success: true,
      count: tickets.length,
      data: tickets
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/tickets/:uuid - Retrieve specific ticket with audit trail
exports.getTicketByUuid = (req, res, next) => {
  try {
    const { uuid } = req.params;

    const ticketStmt = db.prepare(`
      SELECT 
        t.*,
        f.building_name,
        f.floor_number,
        f.room_number,
        f.facility_type,
        f.latitude,
        f.longitude,
        u_creator.full_name AS created_by_name,
        u_creator.email AS created_by_email,
        u_assignee.full_name AS assigned_to_name
      FROM tickets t
      JOIN facilities f ON t.facility_id = f.facility_id
      JOIN users u_creator ON t.created_by = u_creator.user_id
      LEFT JOIN users u_assignee ON t.assigned_to = u_assignee.user_id
      WHERE t.ticket_uuid = ?
    `);

    const ticket = ticketStmt.get(uuid);

    if (!ticket) {
      return res.status(404).json({
        success: false,
        message: `Ticket with UUID ${uuid} not found.`
      });
    }

    // Retrieve audit timeline
    const auditStmt = db.prepare(`
      SELECT 
        a.log_id,
        a.old_status,
        a.new_status,
        a.remarks,
        a.timestamp,
        u.full_name AS changed_by_name
      FROM ticket_audit_logs a
      JOIN users u ON a.changed_by = u.user_id
      WHERE a.ticket_id = ?
      ORDER BY a.timestamp ASC
    `);
    const timeline = auditStmt.all(ticket.ticket_id);

    res.status(200).json({
      success: true,
      data: {
        ...ticket,
        timeline
      }
    });
  } catch (error) {
    next(error);
  }
};

// POST /api/v1/tickets - Create a new ticket
exports.createTicket = (req, res, next) => {
  try {
    const { title, description, category, urgency_level, facility_id, created_by, image_url } = req.body;

    // Boundary & Input Validation
    if (!title || typeof title !== 'string' || title.trim().length === 0) {
      return res.status(400).json({ success: false, message: 'Title is required and cannot be empty.' });
    }
    if (title.length > 200) {
      return res.status(400).json({ success: false, message: 'Title cannot exceed 200 characters.' });
    }
    if (!description || typeof description !== 'string' || description.trim().length < 10) {
      return res.status(400).json({ success: false, message: 'Description must be at least 10 characters long.' });
    }
    if (!category) {
      return res.status(400).json({ success: false, message: 'Category is required.' });
    }
    if (!urgency_level) {
      return res.status(400).json({ success: false, message: 'Urgency level is required.' });
    }
    if (!facility_id) {
      return res.status(400).json({ success: false, message: 'Facility selection is required.' });
    }

    const ticketUuid = crypto.randomUUID();
    const creatorId = created_by || 1; // Default to student demo user if unauthenticated

    // Execute atomic creation + initial audit log entry
    const createTransaction = db.transaction(() => {
      const insertTicket = db.prepare(`
        INSERT INTO tickets (ticket_uuid, title, description, category, urgency_level, status, facility_id, created_by, image_url)
        VALUES (?, ?, ?, ?, ?, 'submitted', ?, ?, ?)
      `);
      const result = insertTicket.run(
        ticketUuid,
        title.trim(),
        description.trim(),
        category,
        urgency_level,
        facility_id,
        creatorId,
        image_url || null
      );

      const ticketId = result.lastInsertRowid;

      const insertAudit = db.prepare(`
        INSERT INTO ticket_audit_logs (ticket_id, changed_by, old_status, new_status, remarks)
        VALUES (?, ?, NULL, 'submitted', 'Submitted by student.')
      `);
      insertAudit.run(ticketId, creatorId);

      return ticketId;
    });

    const newTicketId = createTransaction();

    res.status(201).json({
      success: true,
      message: 'Request submitted successfully.',
      ticket_id: newTicketId,
      ticket_uuid: ticketUuid
    });
  } catch (error) {
    next(error);
  }
};

// PATCH /api/v1/tickets/:uuid/status - Update status and technician assignment
exports.updateTicketStatus = (req, res, next) => {
  try {
    const { uuid } = req.params;
    const { status, assigned_to, remarks, changed_by } = req.body;

    const validStatuses = ['submitted', 'assigned', 'in_progress', 'resolved', 'closed', 'rejected'];
    if (!status || !validStatuses.includes(status)) {
      return res.status(400).json({
        success: false,
        message: `Invalid status. Must be one of: ${validStatuses.join(', ')}`
      });
    }

    const currentTicket = db.prepare('SELECT ticket_id, status FROM tickets WHERE ticket_uuid = ?').get(uuid);
    if (!currentTicket) {
      return res.status(404).json({ success: false, message: `Ticket with UUID ${uuid} not found.` });
    }

    const modifierId = changed_by || 4; // Default to facility supervisor

    // Perform atomic transaction
    const updateTransaction = db.transaction(() => {
      let resolvedAtSql = status === 'resolved' ? 'CURRENT_TIMESTAMP' : 'NULL';
      if (status !== 'resolved') {
        resolvedAtSql = 'resolved_at'; // preserve existing if not changing to resolved
      }

      const updateStmt = db.prepare(`
        UPDATE tickets
        SET 
          status = ?,
          assigned_to = COALESCE(?, assigned_to),
          resolved_at = CASE WHEN ? = 'resolved' THEN CURRENT_TIMESTAMP ELSE resolved_at END
        WHERE ticket_id = ?
      `);
      updateStmt.run(status, assigned_to || null, status, currentTicket.ticket_id);

      const auditStmt = db.prepare(`
        INSERT INTO ticket_audit_logs (ticket_id, changed_by, old_status, new_status, remarks)
        VALUES (?, ?, ?, ?, ?)
      `);
      auditStmt.run(
        currentTicket.ticket_id,
        modifierId,
        currentTicket.status,
        status,
        remarks || `Status transitioned to ${status}`
      );
    });

    updateTransaction();

    res.status(200).json({
      success: true,
      message: `Ticket ${uuid} status successfully updated to ${status}.`
    });
  } catch (error) {
    next(error);
  }
};
