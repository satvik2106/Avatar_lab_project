const path = require('path');
const fs = require('fs');

exports.handleAudioUpload = (req, res) => {
  if (!req.files || !req.files.audio) {
    return res.status(400).json({ message: 'No audio file uploaded.' });
  }

  const audio = req.files.audio;
  const uploadPath = path.join(__dirname, '..', 'uploads', 'audio', audio.name);

  audio.mv(uploadPath, (err) => {
    if (err) {
      return res.status(500).json({ message: 'Error saving file.' });
    }

    res.status(200).json({
      message: 'Audio uploaded successfully.',
      filePath: `/uploads/audio/${audio.name}`
    });
  });
};
