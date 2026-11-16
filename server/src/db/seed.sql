-- Seed Data for CampusPulse

-- Departments
INSERT OR IGNORE INTO departments (department_id, name, code, head_email) VALUES
(1, 'Computer Science & Engineering', 'CSE', 'hod.cse@campus.edu'),
(2, 'Computer Science & Design', 'CSD', 'hod.csd@campus.edu'),
(3, 'Electronics & Communication', 'ECE', 'hod.ece@campus.edu'),
(4, 'Mechanical Engineering', 'MECH', 'hod.mech@campus.edu'),
(5, 'Estate & Facility Management', 'EFM', 'director.estate@campus.edu');

-- Users
INSERT OR IGNORE INTO users (user_id, full_name, email, role, department_id) VALUES
(1, 'Eshan Jogwar', 'eshan.csd22@campus.edu', 'student', 2),
(2, 'Aarav Sharma', 'aarav.cse22@campus.edu', 'student', 1),
(3, 'Dr. Santosh Sahu', 'santosh.sahu@campus.edu', 'faculty', 2),
(4, 'Ramesh Kumar (Estate Supervisor)', 'ramesh.estate@campus.edu', 'facility_manager', 5),
(5, 'Sunil Verma (Chief Maintenance Admin)', 'admin.maintenance@campus.edu', 'admin', 5);

-- Facilities with coordinates representing a typical campus layout
INSERT OR IGNORE INTO facilities (facility_id, building_name, floor_number, room_number, facility_type, latitude, longitude, status) VALUES
(1, 'CSD Department Block', 3, 'Lab 302 (UI/UX Studio)', 'lab', 18.5204, 73.8567, 'operational'),
(2, 'CSD Department Block', 2, 'Room 204 (Smart Classroom)', 'classroom', 18.5205, 73.8568, 'maintenance_required'),
(3, 'Main Academic Complex', 1, 'Auditorium 1', 'classroom', 18.5210, 73.8572, 'operational'),
(4, 'Library Building', 2, 'Digital Resource Center', 'library', 18.5215, 73.8560, 'operational'),
(5, 'Boys Hostel Block A', 1, 'Common Room & Washroom', 'washroom', 18.5220, 73.8550, 'maintenance_required'),
(6, 'Girls Hostel Block B', 2, 'Floor 2 Study Lounge', 'hostel', 18.5225, 73.8555, 'operational'),
(7, 'Indoor Sports Complex', 0, 'Badminton Court 1', 'sports', 18.5195, 73.8580, 'under_repair'),
(8, 'Central Cafeteria', 1, 'Dining Hall B', 'cafeteria', 18.5200, 73.8562, 'operational');

-- Sample Initial Tickets (Mix of resolved and open for realistic KPI & Charts)
INSERT OR IGNORE INTO tickets (ticket_id, ticket_uuid, title, description, category, urgency_level, status, facility_id, created_by, assigned_to, created_at, resolved_at) VALUES
(1, 'c9b4a1f2-7e3d-4c8a-9f1b-2d3e4f5a6b7c', 'Flickering Ceiling Projector', 'Ceiling projector HDMI input cuts out every 5 minutes during lectures.', 'it_network', 'high', 'resolved', 2, 3, 4, datetime('now', '-5 days'), datetime('now', '-4 days', '+3 hours')),
(2, 'd8e5b2a1-8f4e-5d9b-0a2c-3e4f5a6b7c8d', 'Water Leakage in Main Washroom Sink', 'Continuous dripping from pipe underneath sink #2, causing water pooling on floor.', 'plumbing', 'high', 'resolved', 5, 1, 4, datetime('now', '-4 days'), datetime('now', '-3 days', '+6 hours')),
(3, 'e7f6c3b2-9a5f-6e0c-1b3d-4f5a6b7c8d9e', 'AC Unit Error Code E4', 'Split AC unit in Digital Resource Center blowing room temperature air and showing E4.', 'electrical', 'medium', 'resolved', 4, 2, 4, datetime('now', '-3 days'), datetime('now', '-2 days', '+12 hours')),
(4, 'f6a7d4c3-0b6a-7f1d-2c4e-5a6b7c8d9e0f', 'Loose Desk Planking in Row 4', 'Two wooden desk joints are detached, exposing sharp screws.', 'furniture', 'medium', 'in_progress', 1, 1, 4, datetime('now', '-2 days'), NULL),
(5, 'a5b8e5d4-1c7b-8a2e-3d5f-6b7c8d9e0f1a', 'Ethernet Jack Disconnected at Pod 6', 'No network signal at workstation LAN drop #6.', 'it_network', 'low', 'assigned', 1, 3, 4, datetime('now', '-1 days'), NULL),
(6, 'b4c9f6e5-2d8c-9b3f-4e6a-7c8d9e0f1a2b', 'Broken Glass Window on Fire Exit', 'Window pane shattered due to high winds, safety hazard.', 'safety', 'critical', 'submitted', 7, 2, NULL, datetime('now', '-4 hours'), NULL);

-- Audit Logs for tickets
INSERT OR IGNORE INTO ticket_audit_logs (ticket_id, changed_by, old_status, new_status, remarks, timestamp) VALUES
(1, 3, 'submitted', 'assigned', 'Assigned to Ramesh Kumar (Estate)', datetime('now', '-5 days', '+1 hour')),
(1, 4, 'assigned', 'resolved', 'Replaced faulty 15m HDMI cable and ceiling mount adapter.', datetime('now', '-4 days', '+3 hours')),
(2, 4, 'submitted', 'resolved', 'Tightened intake coupling and replaced degraded gasket.', datetime('now', '-3 days', '+6 hours')),
(3, 4, 'submitted', 'resolved', 'Cleaned indoor filters and recharged coolant.', datetime('now', '-2 days', '+12 hours')),
(4, 4, 'submitted', 'in_progress', 'Carpentry crew scheduled for evening work.', datetime('now', '-1 days', '+2 hours')),
(5, 4, 'submitted', 'assigned', 'IT technician assigned to inspect patch panel.', datetime('now', '-18 hours'));
