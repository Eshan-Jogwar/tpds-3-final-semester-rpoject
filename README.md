# CampusPulse: Intelligent Campus Facility, Resource & Grievance Management Platform

[![Node.js](https://img.shields.io/badge/Node.js-v18%2B-green.svg)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-5.x-blue.svg)](https://expressjs.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203%20(On--Disk)-lightblue.svg)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Front--End-Bootstrap%205-purple.svg)](https://getbootstrap.com/)
[![Docker](https://img.shields.io/badge/Container-Docker%20%26%20Compose-2496ED.svg)](https://www.docker.com/)

> **Course**: TPDS-III (Tools and Practices in Data Science / Product Development Studio)  
> **Class**: 5th Semester B.Tech CSD (Computer Science & Design)  
> **Project Code**: `TPDS-III-CSD-2026`

---

## 📌 Executive Summary

**CampusPulse** is an end-to-end, full-stack, data-driven campus infrastructure management and grievance intelligence platform. It replaces archaic paper logbooks and disconnected messaging groups with an automated, transparent, and auditable system.

The platform provides:
1. **Student & Faculty Portal**: Frictionless grievance lodging with photo attachment, room selection, urgency classification, and 36-character UUID tracking.
2. **Operations & Triage Console**: Real-time management board for facility supervisors to assign technicians, transition incident states, and maintain transparent audit histories.
3. **Executive BI & Analytics Dashboard**: Live metrics for campus administration tracking Mean Time to Resolution (MTTR), SLA compliance percentages, category distributions, and geospatial campus fault density.

---

## 🗺️ The Four-Module Mapping Table (Syllabus Alignment)

| Syllabus Module | Syllabus Concepts | Applied Project Feature | Code Artifact Path |
|---|---|---|---|
| **Module 1: Dashboard Designing** | - Open-source dashboard tools<br>- Live data connections<br>- Chart grammars (Donut, Bar, Time-series)<br>- Geospatial campus mapping<br>- Deployment & export | - Executive BI Analytics Portal<br>- SLA Compliance & MTTR gauges<br>- Category distribution & velocity charts<br>- Interactive campus hotspot layout<br>- CSV / Tableau data export | `/public/analytics.html`<br>`/public/js/analytics.js`<br>`/server/src/controllers/analytics.controller.js`<br>`/server/src/db/schema.sql` (views) |
| **Module 2: Front-End Development** | - Responsive mobile-first UI<br>- UI design patterns<br>- UI controls (select, range, radio, buttons)<br>- Modal dialogs & feedback toasts<br>- Bootstrap 5 responsive framework | - Student grievance lodging portal<br>- Facility status directory<br>- Submission confirmation modal<br>- Live status update toast alerts<br>- Responsive viewports (320px–1920px) | `/public/index.html`<br>`/public/admin.html`<br>`/public/css/styles.css`<br>`/public/js/app.js`<br>`/public/js/admin.js` |
| **Module 3: Back-End Development** | - Web server & HTTP lifecycle<br>- REST API design (GET, POST, PATCH)<br>- Relational SQL database (SQLite on disk)<br>- 3NF schema, PRAGMAs, views, indexes<br>- Node.js & Express.js framework | - RESTful API microservices<br>- Express middleware (CORS, JSON, errors)<br>- 3NF SQLite database (`campuspulse.db`)<br>- Parameterized queries & transactions<br>- PRAGMA WAL & foreign key enforcement | `/server/src/app.js`<br>`/server/src/server.js`<br>`/server/src/db/connection.js`<br>`/server/src/db/schema.sql`<br>`/server/src/controllers/` |
| **Module 4: GIT & Deployment** | - Git version control & commit management<br>- Branching strategy (`main`, `feature/*`)<br>- Multi-stage Docker containerization<br>- Docker Compose orchestration<br>- Cloud deployment readiness | - Structured GitHub repository<br>- Multi-stage `Dockerfile`<br>- `docker-compose.yml` with persistent disk volume<br>- Automated test suite (`npm test`) | `/.git/`<br>`/.gitignore`<br>`/Dockerfile`<br>`/docker-compose.yml`<br>`/tests/api.test.js` |

---

## 🏗️ System Architecture

```
[ Client Tier: Module 2 ]
   ├── Student Portal (index.html)  --> Lodges tickets, tracks UUID, views facilities
   ├── Operations Board (admin.html) --> Triages issues, assigns technicians, updates statuses
   └── Executive BI (analytics.html) --> Chart.js, KPI gauges, interactive campus hotspot map
             │
             ▼ (HTTP REST JSON via Fetch API)
[ Server Tier: Module 3 ]
   └── Node.js & Express.js API Engine
         ├── Middleware (CORS, JSON BodyParser, Error Handler)
         ├── Controllers (Tickets, Facilities, Analytics, Departments)
         └── Prepared Parameterized Queries
             │
             ▼ (In-Process Synchronous better-sqlite3 Driver)
[ Relational Storage Tier: Module 3 ]
   └── On-Disk SQLite Database (/data/campuspulse.db)
         ├── PRAGMA foreign_keys = ON;
         ├── PRAGMA journal_mode = WAL;
         ├── 5 Normalized 3NF Tables (departments, users, facilities, tickets, audit_logs)
         └── 2 Analytical Views (vw_department_sla_metrics, vw_campus_hotspots)
```

---

## ⚡ Quick Start & Execution

### 1. Local Run (Node.js)

```bash
# 1. Clone repository
git clone https://github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git
cd tpds-3-final-semester-rpoject

# 2. Install dependencies
npm install

# 3. Start the application (automatically initializes SQLite schema & seed data)
npm start

# Access in browser:
# - Student Portal:    http://localhost:5000/index.html
# - Operations Board:  http://localhost:5000/admin.html
# - BI Dashboard:      http://localhost:5000/analytics.html
# - API Healthcheck:   http://localhost:5000/api/v1/health
```

### 2. Run with Docker & Docker Compose (Module 4)

```bash
# Build and run containerized application
docker-compose up --build -d

# Check running status
docker-compose ps

# Stop container
docker-compose down
```

### 3. Run Automated Empirical Tests (Guideline 7)

```bash
npm test
```

---

## 📊 Database Requirements & Design (SQLite on Disk)

To satisfy **Module 3 ("SQL and its types, and SQL Server")**, the system utilizes an on-disk serverless SQLite architecture with the following mandatory safeguards:

1. **Foreign Key Enforcement**: Enabled via `PRAGMA foreign_keys = ON;` on connection to ensure referential integrity.
2. **Concurrency & Locking Control**: Configured with `PRAGMA journal_mode = WAL;` (Write-Ahead Logging) and `PRAGMA busy_timeout = 5000;`, enabling concurrent reads during writes.
3. **Transaction Atomicity (TCL)**: All status updates and audit logs are executed inside an atomic `db.transaction()` block.
4. **B-Tree Indexes**: Created on `facility_id`, `status`, `category`, and `created_at` for $O(\log N)$ query speed.
5. **Analytical Views**: `vw_department_sla_metrics` calculates MTTR using SQLite's `unixepoch()` date math.

---

## 🧪 Empirical Test Suite (Guideline 7 Compliance)

| Test ID | Test Category | Condition / Input | Expected Result | Measured Result |
|---|---|---|---|---|
| **TC-01** | System Health | `GET /api/v1/health` | HTTP 200, SQLite healthy | Pass (200 OK) |
| **TC-02** | Normal Input | Valid ticket submission | HTTP 201, UUID returned | Pass (201 Created) |
| **TC-03** | Data Retrieval | `GET /api/v1/tickets/:uuid` | HTTP 200, full audit trail | Pass (200 OK) |
| **TC-04** | Boundary Check | Description &lt; 10 characters | HTTP 400 Bad Request | Pass (400 Intercepted) |
| **TC-05** | Boundary Check | Title &gt; 200 characters | HTTP 400 Bad Request | Pass (400 Intercepted) |
| **TC-06** | Malformed Input | Missing required category | HTTP 400 Bad Request | Pass (400 Intercepted) |
| **TC-07** | Transaction Atomicity | Status transition to resolved | HTTP 200, audit log logged | Pass (Atomic Write) |
| **TC-08** | Analytics Engine | `GET /api/v1/analytics/kpis` | HTTP 200, MTTR & SLA calc | Pass (Computed Metrics) |

---

## 👥 Authors & Academic Attribution

* **Team Lead**: Eshan Jogwar (Roll No. CSD-XXXX) — Backend, Database & Docker
* **Course Guide**: Dr. Santosh Kumar Sahu
* **Institution**: 5th Semester CSD, TPDS-III Capstone Project
