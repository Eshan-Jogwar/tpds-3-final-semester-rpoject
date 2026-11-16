# Campus: Campus Facility Maintenance and Asset Intelligence Platform

[![Node.js](https://img.shields.io/badge/Node.js-v20%2B-green.svg)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-5.x-blue.svg)](https://expressjs.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite%203%20(WAL)-lightblue.svg)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Front--End-Bootstrap%205.3-purple.svg)](https://getbootstrap.com/)
[![Docker](https://img.shields.io/badge/Container-Docker%20%26%20Compose-2496ED.svg)](https://www.docker.com/)

> **Course**: Tools and Practices in Data Science III (TPDS-III)  
> **Class**: 5th Semester B.Tech in Computer Science and Design (CSD)  
> **Repository**: [https://github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git](https://github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git)

---

## Overview

Campus is a 3-tier web platform for facility incident management, department dispatch, SLA compliance tracking, and spatial hotspot detection across university infrastructure. It replaces unmonitored messaging threads and paper logs with an immutable audit ledger and real-time operational telemetry.

### Core Modules

1. **Student & Faculty Incident Portal**: 30-second ticket filing with photo uploads, category classification, room dropdowns, and interactive 2D SVG blueprint selection.
2. **Technician Work Orders Queue**: Filterable operational board with single-click bulk status transitions, priority flags, and dynamic SLA breach countdown timers.
3. **Executive Analytics Dashboard**: Real-time administrative metrics tracking Mean Time to Resolution (MTTR), department SLA compliance percentages, trade expenditure distributions, and campus fault hotspots.

---

## Curriculum Syllabus Mapping (Modules 1–4)

| Syllabus Module | Core Competencies | Applied System Implementation | Source Path |
|---|---|---|---|
| **Module 1: Dashboard Designing** | Open-source dashboard tools, live database querying, chart grammars (doughnut, velocity lines), spatial campus layout, CSV exports | Executive analytics dashboard, SLA compliance tables, MTTR gauges, 7-day rolling resolution trends, interactive 2D SVG hotspot blueprint | `/public/analytics.html`<br>`/public/js/analytics.js`<br>`/server/src/controllers/analytics.controller.js` |
| **Module 2: Front-End Development** | Responsive mobile-first interfaces, UI controls, modal dialogs, status toasts, accessibility, Bootstrap 5 | Student incident portal, facility directory, technician work queue, photo dropzone, responsive viewports (320px–1920px) | `/public/index.html`<br>`/public/admin.html`<br>`/public/css/styles.css`<br>`/public/js/app.js` |
| **Module 3: Back-End Development** | HTTP server lifecycle, REST API design, relational SQLite schema in 3NF, PRAGMA optimizations, views, indexes, Express.js | Express 5 REST API, async route exception handling, 3NF SQLite database (`data/campuspulse.db`), WAL concurrency, audit ledger | `/server/src/app.js`<br>`/server/src/server.js`<br>`/server/src/db/connection.js`<br>`/server/src/db/schema.sql` |
| **Module 4: Version Control & DevOps** | Git commit conventions, feature branching, Docker containerization, Docker Compose orchestration, automated tests | Multi-stage `Dockerfile`, `docker-compose.yml`, root `Makefile`, persistent disk volume, automated Jest/Supertest suite | `/.git/`<br>`/Dockerfile`<br>`/docker-compose.yml`<br>`/Makefile`<br>`/tests/api.test.js` |

---

## System Architecture

```
[ Tier 1: Presentation Layer ]
   ├── Student Portal (index.html)     -> Ticket submission, room dropdowns, 2D SVG blueprint
   ├── Work Orders Queue (admin.html)   -> Triage queue, bulk status transitions, SLA badges
   └── Executive Dashboard (analytics.html) -> Chart.js charts, KPI cards, spatial hotspot telemetry
             │
             ▼  HTTP/1.1 REST (JSON)
[ Tier 2: Application Layer (Node.js 20 LTS + Express 5) ]
   ├── Middleware: CORS, JSON parser, input validation, central error handler
   ├── Controllers: /api/v1/tickets, /api/v1/facilities, /api/v1/departments, /api/v1/analytics
   └── Service Logic: SLA deadline calculation, deterministic state machine, audit writer
             │
             ▼  In-Process IPC (better-sqlite3)
[ Tier 3: Persistence Layer (SQLite 3.45 on Disk) ]
   ├── PRAGMA journal_mode = WAL; (Non-blocking concurrent reads during active writes)
   ├── PRAGMA foreign_keys = ON;  (Referential integrity enforcement)
   ├── PRAGMA busy_timeout = 5000; (Lock collision mitigation)
   ├── 5 Tables in 3NF: departments, users, facilities, tickets, ticket_audit_logs
   └── 2 Analytical Views: vw_department_sla_metrics, vw_campus_hotspots
```

---

## Quick Start

### 1. Docker (Recommended Single-Command Setup)

```bash
# Build container and launch services in background
make up

# Alternatively, using docker compose directly:
docker compose up --build -d
```

Access services:
* **Student Incident Portal:** [http://localhost:5000/index.html](http://localhost:5000/index.html)
* **Technician Work Orders:** [http://localhost:5000/admin.html](http://localhost:5000/admin.html)
* **Executive Analytics:** [http://localhost:5000/analytics.html](http://localhost:5000/analytics.html)
* **API Healthcheck:** [http://localhost:5000/api/v1/health](http://localhost:5000/api/v1/health)

Useful `make` commands:
```bash
make status  # Check container state
make test    # Run endpoint verification curl assertions
make logs    # Stream container logs
make down    # Stop container
```

### 2. Local Node.js Execution

```bash
# 1. Install dependencies
npm install

# 2. Run database migration and launch server
npm start

# 3. Run automated test suite
npm test
```

---

## Database Design (SQLite On-Disk, 3NF)

To fulfill **Module 3 ("SQL and its types, and SQL Server")**, the persistence layer implements an embedded on-disk SQLite architecture with the following constraints:

1. **Foreign Key Enforcement**: Connection opens with `PRAGMA foreign_keys = ON;`.
2. **Concurrency & Locking Control**: Connection sets `PRAGMA journal_mode = WAL;` and `PRAGMA busy_timeout = 5000;`. Readers do not block writers, and writers do not block readers.
3. **Transaction Atomicity**: State changes and corresponding entries in `ticket_audit_logs` execute within a single atomic `db.transaction()` block.
4. **B-Tree Query Indexing**:
   * `idx_tickets_status_priority` ON `tickets(status, priority)`
   * `idx_tickets_facility` ON `tickets(facility_id)`
   * `idx_tickets_department` ON `tickets(department_id)`
   * `idx_audit_ticket` ON `ticket_audit_logs(ticket_id)`
5. **Analytical Views**:
   * `vw_department_sla_metrics`: Computes total tickets, resolved count, SLA breach count, compliance rate, and average resolution time in hours using native SQLite date functions.
   * `vw_campus_hotspots`: Groups unresolved tickets by facility and calculates priority-weighted incident scores.

---

## Automated Test Verification

The test suite validates integration behavior across REST routes, constraints, and analytical views using Jest and Supertest (`tests/api.test.js`).

| Test ID | Test Category | Target Endpoint | Assertion | Result |
|---|---|---|---|---|
| **TC-01** | System Health | `GET /api/v1/health` | HTTP 200, status "healthy", SQLite check passed | Pass |
| **TC-02** | Ticket Insertion | `POST /api/v1/tickets` | HTTP 201, UUID ticket number and SLA deadline assigned | Pass |
| **TC-03** | Record Retrieval | `GET /api/v1/tickets/:id` | HTTP 200, full record with location and department joins | Pass |
| **TC-04** | Input Boundary | `POST /api/v1/tickets` (title < 5 chars) | HTTP 400 Bad Request, validation error returned | Pass |
| **TC-05** | Input Boundary | `POST /api/v1/tickets` (invalid facility ID) | HTTP 400 Bad Request, foreign key rejection | Pass |
| **TC-06** | State Machine | `PATCH /api/v1/tickets/:id/status` (`open` -> `in_progress`) | HTTP 200, state transition recorded in audit ledger | Pass |
| **TC-07** | Atomic Audit Log | `PATCH /api/v1/tickets/:id/status` (`in_progress` -> `resolved`) | HTTP 200, resolution timestamp and audit row created | Pass |
| **TC-08** | Analytics Engine | `GET /api/v1/analytics/kpis` | HTTP 200, MTTR, SLA compliance, and volume aggregates | Pass |

---

## Authors & Course Context

* **Developer**: Eshan Jogwar (Roll No: CSD-501)
* **Program**: B.Tech in Computer Science and Design (CSD), 5th Semester
* **Laboratory**: Tools and Practices in Data Science III (TPDS-III)
* **Institution**: Department of Computer Science and Design
