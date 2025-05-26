const express = require('express');
const cors = require('cors');
const fileUpload = require('express-fileupload');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(fileUpload({
  limits: { fileSize: 50 * 1024 * 1024 }, // 50MB max file size
  useTempFiles: true,
  tempFileDir: './tmp/'
}));
app.use('/uploads', express.static('uploads'));
app.use('/outputs', express.static('outputs'));

// Create necessary directories if they don't exist
const dirs = ['./uploads', './outputs', './assets', './tmp'];
dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created directory: ${dir}`);
  }
});

// Log environment configuration
console.log('Environment Configuration:');
console.log(`- TTS API URL: ${process.env.TTS_API_URL || 'http://localhost:8000'}`);
console.log(`- LatentSync API URL: ${process.env.LATENTSYNC_API_URL || 'http://localhost:6900'}`);
console.log(`- Server Port: ${process.env.PORT || 5000}`);
console.log(`- Environment: ${process.env.NODE_ENV || 'development'}`);

// ✅ Root route for checking backend status
app.get('/', (req, res) => {
  res.json({
    status: 'API is running',
    services: {
      tts: process.env.TTS_API_URL || 'http://localhost:8000',
      latentsync: process.env.LATENTSYNC_API_URL || 'http://localhost:6900'
    }
  });
});

// Routes
const ttsRoutes = require('./routes/ttsRoutes');
app.use('/api', ttsRoutes);

app.use('/api/upload/audio', require('./routes/audioRoutes'));
app.use('/api/transcript', require('./routes/transcriptRoutes'));
app.use('/api/templates', require('./routes/templateRoutes'));

const latentsyncRoutes = require('./routes/latentsyncRoutes');
app.use('/api/latentsync', latentsyncRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err.stack);
  res.status(500).json({
    error: 'Server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An unexpected error occurred'
  });
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`API available at http://localhost:${PORT}`);
});
