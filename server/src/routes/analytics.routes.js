const express = require('express');
const router = express.Router();
const analyticsController = require('../controllers/analytics.controller');

router.get('/kpis', analyticsController.getKpis);
router.get('/categories', analyticsController.getCategoryBreakdown);
router.get('/buildings', analyticsController.getBuildingBreakdown);
router.get('/time-series', analyticsController.getTimeSeries);
router.get('/hotspots', analyticsController.getHotspots);

module.exports = router;
