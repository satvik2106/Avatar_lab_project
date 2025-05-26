const express = require('express');
const router = express.Router();
const { handleAudioUpload } = require('../controllers/audioController');

router.post('/', handleAudioUpload);

module.exports = router;
