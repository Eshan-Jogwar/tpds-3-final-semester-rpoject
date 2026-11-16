const express = require('express');
const router = express.Router();
const ticketsController = require('../controllers/tickets.controller');

router.get('/', ticketsController.getTickets);
router.post('/', ticketsController.createTicket);
router.get('/:uuid', ticketsController.getTicketByUuid);
router.patch('/:uuid/status', ticketsController.updateTicketStatus);

module.exports = router;
