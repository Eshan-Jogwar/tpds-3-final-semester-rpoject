const express = require('express');
const router = express.Router();
const facilitiesController = require('../controllers/facilities.controller');

router.get('/', facilitiesController.getFacilities);
router.get('/:id', facilitiesController.getFacilityById);

module.exports = router;
