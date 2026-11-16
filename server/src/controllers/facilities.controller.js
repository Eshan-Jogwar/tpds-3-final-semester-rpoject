const db = require('../db/connection');

// GET /api/v1/facilities - List campus facilities with ticket metrics
exports.getFacilities = (req, res, next) => {
  try {
    const stmt = db.prepare(`
      SELECT 
        f.facility_id,
        f.building_name,
        f.floor_number,
        f.room_number,
        f.facility_type,
        f.latitude,
        f.longitude,
        f.status,
        COUNT(t.ticket_id) AS total_tickets,
        SUM(CASE WHEN t.status IN ('submitted', 'assigned', 'in_progress') THEN 1 ELSE 0 END) AS active_tickets
      FROM facilities f
      LEFT JOIN tickets t ON f.facility_id = t.facility_id
      GROUP BY f.facility_id
      ORDER BY f.building_name, f.floor_number, f.room_number
    `);
    const facilities = stmt.all();

    res.status(200).json({
      success: true,
      count: facilities.length,
      data: facilities
    });
  } catch (error) {
    next(error);
  }
};

// GET /api/v1/facilities/:id - Details of specific facility
exports.getFacilityById = (req, res, next) => {
  try {
    const { id } = req.params;
    const stmt = db.prepare('SELECT * FROM facilities WHERE facility_id = ?');
    const facility = stmt.get(id);

    if (!facility) {
      return res.status(404).json({ success: false, message: 'Facility not found' });
    }

    res.status(200).json({ success: true, data: facility });
  } catch (error) {
    next(error);
  }
};
