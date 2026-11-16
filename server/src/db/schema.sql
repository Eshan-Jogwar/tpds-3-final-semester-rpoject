-- ====================================================================
-- CampusPulse Database Schema (SQLite 3NF Normalized)
-- Course: TPDS-III (5th Semester CSD)
-- ====================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- 1. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    head_email TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK (role IN ('student', 'faculty', 'facility_manager', 'admin')),
    department_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(department_id) ON DELETE SET NULL
);

-- 3. Facilities Table (Campus Buildings & Rooms with Geospatial Coordinates)
CREATE TABLE IF NOT EXISTS facilities (
    facility_id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT NOT NULL,
    floor_number INTEGER NOT NULL,
    room_number TEXT NOT NULL,
    facility_type TEXT NOT NULL CHECK (facility_type IN ('classroom', 'lab', 'washroom', 'hostel', 'sports', 'library', 'cafeteria')),
    latitude REAL,
    longitude REAL,
    status TEXT DEFAULT 'operational' CHECK (status IN ('operational', 'maintenance_required', 'under_repair')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tickets Table (Incidents & Grievances)
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_uuid TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('electrical', 'plumbing', 'furniture', 'it_network', 'cleanliness', 'civil', 'safety')),
    urgency_level TEXT NOT NULL CHECK (urgency_level IN ('low', 'medium', 'high', 'critical')),
    status TEXT DEFAULT 'submitted' CHECK (status IN ('submitted', 'assigned', 'in_progress', 'resolved', 'closed', 'rejected')),
    facility_id INTEGER NOT NULL,
    created_by INTEGER NOT NULL,
    assigned_to INTEGER,
    image_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME,
    FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    FOREIGN KEY (created_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    FOREIGN KEY (assigned_to) REFERENCES users(user_id) ON DELETE SET NULL
);

-- 5. Ticket Audit Trail (Immutable Log for Transparency)
CREATE TABLE IF NOT EXISTS ticket_audit_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    changed_by INTEGER NOT NULL,
    old_status TEXT,
    new_status TEXT,
    remarks TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    FOREIGN KEY (changed_by) REFERENCES users(user_id)
);

-- 6. Performance B-Tree Indexes
CREATE INDEX IF NOT EXISTS idx_tickets_facility ON tickets(facility_id);
CREATE INDEX IF NOT EXISTS idx_tickets_status ON tickets(status);
CREATE INDEX IF NOT EXISTS idx_tickets_category ON tickets(category);
CREATE INDEX IF NOT EXISTS idx_tickets_urgency ON tickets(urgency_level);
CREATE INDEX IF NOT EXISTS idx_tickets_created_at ON tickets(created_at);
CREATE INDEX IF NOT EXISTS idx_audit_ticket ON ticket_audit_logs(ticket_id);

-- 7. Analytical Views for Module 1 Dashboard Aggregations
CREATE VIEW IF NOT EXISTS vw_department_sla_metrics AS
SELECT 
    f.building_name,
    t.category,
    t.urgency_level,
    COUNT(t.ticket_id) AS total_incidents,
    SUM(CASE WHEN t.status = 'resolved' THEN 1 ELSE 0 END) AS resolved_incidents,
    ROUND(AVG(CASE WHEN t.status = 'resolved' AND t.resolved_at IS NOT NULL 
              THEN (unixepoch(t.resolved_at) - unixepoch(t.created_at)) / 3600.0 
              ELSE NULL END), 2) AS avg_resolution_hours
FROM tickets t
JOIN facilities f ON t.facility_id = f.facility_id
GROUP BY f.building_name, t.category, t.urgency_level;

CREATE VIEW IF NOT EXISTS vw_campus_hotspots AS
SELECT 
    f.facility_id,
    f.building_name,
    f.room_number,
    f.facility_type,
    f.latitude,
    f.longitude,
    COUNT(t.ticket_id) AS total_tickets,
    SUM(CASE WHEN t.status IN ('submitted', 'assigned', 'in_progress') THEN 1 ELSE 0 END) AS open_tickets,
    SUM(CASE WHEN t.status = 'resolved' THEN 1 ELSE 0 END) AS resolved_tickets
FROM facilities f
LEFT JOIN tickets t ON f.facility_id = t.facility_id
GROUP BY f.facility_id, f.building_name, f.room_number, f.facility_type, f.latitude, f.longitude;
