const express = require('express');
const cors = require('cors');
const path = require('path');

const ticketsRoutes = require('./routes/tickets.routes');
const facilitiesRoutes = require('./routes/facilities.routes');
const analyticsRoutes = require('./routes/analytics.routes');
const departmentsRoutes = require('./routes/departments.routes');
const errorHandler = require('./middleware/errorHandler');

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve Static Frontend (Public Web UI)
app.use(express.static(path.join(__dirname, '../../public')));

// API Health Check
app.get('/api/v1/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    service: 'CampusPulse API',
    database: 'SQLite (On-Disk, Serverless)',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use('/api/v1/tickets', ticketsRoutes);
app.use('/api/v1/facilities', facilitiesRoutes);
app.use('/api/v1/analytics', analyticsRoutes);
app.use('/api/v1/departments', departmentsRoutes);

// 404 Handler for undefined API routes
app.use('/api', (req, res) => {
  res.status(404).json({
    success: false,
    message: `API endpoint ${req.originalUrl} not found.`
  });
});

// Fallback to index.html for client-side navigation
app.use((req, res) => {
  res.sendFile(path.join(__dirname, '../../public/index.html'));
});

// Error handling middleware
app.use(errorHandler);

module.exports = app;
