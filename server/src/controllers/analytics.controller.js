const db = require('../db/connection');

// GET /api/v1/analytics/kpis - Primary executive dashboard KPIs
exports.getKpis = (req, res, next) => {
  try {
    const kpiStmt = db.prepare(`
      SELECT 
        COUNT(ticket_id) AS total_tickets,
        SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved_tickets,
        SUM(CASE WHEN status IN ('submitted', 'assigned', 'in_progress') THEN 1 ELSE 0 END) AS active_tickets,
        SUM(CASE WHEN urgency_level = 'critical' AND status != 'resolved' THEN 1 ELSE 0 END) AS critical_active,
        ROUND(AVG(CASE WHEN status = 'resolved' AND resolved_at IS NOT NULL 
                  THEN (unixepoch(resolved_at) - unixepoch(created_at)) / 3600.0 
                  ELSE NULL END), 1) AS mttr_hours
      FROM tickets
    `);
    const kpis = kpiStmt.get();

    // SLA Calculation: Target SLA is 48 hours for general, 12 hours for critical
    const slaStmt = db.prepare(`
      SELECT 
        COUNT(ticket_id) as total_resolved,
        SUM(CASE WHEN (unixepoch(resolved_at) - unixepoch(created_at)) / 3600.0 <= 48 THEN 1 ELSE 0 END) as within_sla
      FROM tickets
      WHERE status = 'resolved' AND resolved_at IS NOT NULL
    `);
    const sla = slaStmt.get();
    const slaComplianceRate = sla.total_resolved > 0 
      ? Math.round((sla.within_sla / sla.total_resolved) * 100) 
      : 100;

    res.status(200).json({
      success: true,
      data: {
        total_tickets: kpis.total_tickets || 0,
        resolved_tickets: kpis.resolved_tickets || 0,
        active_tickets: kpis.active_tickets || 0,
        critical_active: kpis.critical_active || 0,
        mttr_hours: kpis.mttr_hours || 0,
        sla_compliance_rate: slaComplianceRate
      }
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/analytics/category-breakdown - Chart 1: Categories
exports.getCategoryBreakdown = (req, res, next) => {
  try {
    const stmt = db.prepare(`
      SELECT 
        category,
        COUNT(ticket_id) AS count,
        SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved_count,
        SUM(CASE WHEN status != 'resolved' THEN 1 ELSE 0 END) AS pending_count
      FROM tickets
      GROUP BY category
      ORDER BY count DESC
    `);
    const breakdown = stmt.all();

    res.status(200).json({ success: true, data: breakdown });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/analytics/building-breakdown - Chart 2: Departments & Buildings
exports.getBuildingBreakdown = (req, res, next) => {
  try {
    const stmt = db.prepare(`
      SELECT 
        f.building_name,
        COUNT(t.ticket_id) AS total_tickets,
        SUM(CASE WHEN t.status IN ('submitted', 'assigned', 'in_progress') THEN 1 ELSE 0 END) AS open_tickets,
        SUM(CASE WHEN t.status = 'resolved' THEN 1 ELSE 0 END) AS resolved_tickets
      FROM facilities f
      LEFT JOIN tickets t ON f.facility_id = t.facility_id
      GROUP BY f.building_name
      ORDER BY total_tickets DESC
    `);
    const buildingStats = stmt.all();

    res.status(200).json({ success: true, data: buildingStats });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/analytics/time-series - Chart 3: Incident velocity over time
exports.getTimeSeries = (req, res, next) => {
  try {
    const stmt = db.prepare(`
      SELECT 
        date(created_at) AS report_date,
        COUNT(ticket_id) AS reported_count,
        SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved_count
      FROM tickets
      GROUP BY date(created_at)
      ORDER BY report_date ASC
      LIMIT 30
    `);
    const timeSeries = stmt.all();

    res.status(200).json({ success: true, data: timeSeries });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/analytics/hotspots - Geospatial map pins
exports.getHotspots = (req, res, next) => {
  try {
    const stmt = db.prepare('SELECT * FROM vw_campus_hotspots ORDER BY open_tickets DESC');
    const hotspots = stmt.all();

    res.status(200).json({ success: true, data: hotspots });
  } catch (error) {
    next(error);
  }
};
