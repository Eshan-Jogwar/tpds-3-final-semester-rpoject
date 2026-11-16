const express = require('express');
const router = express.Router();
const db = require('../db/connection');

router.get('/', (req, res, next) => {
  try {
    const departments = db.prepare('SELECT * FROM departments ORDER BY name ASC').all();
    res.status(200).json({ success: true, data: departments });
  } catch (error) {
    next(error);
  }
});

module.exports = router;
