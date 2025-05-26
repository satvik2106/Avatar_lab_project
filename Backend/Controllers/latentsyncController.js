const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

const lipsync = async (req, res) => {
  try {
    if (!req.files || !req.files.video || !req.files.audio) {
      return res.status(400).json({ error: 'Video and audio files are required' });
    }

    const videoFile = req.files.video;
    const audioFile = req.files.audio;

    console.log(`Processing lipsync request with video: ${videoFile.name}, audio: ${audioFile.name}`);

    const form = new FormData();
    form.append('video', videoFile.data, videoFile.name);
    form.append('audio', audioFile.data, audioFile.name);

    // Use environment variable for API URL with fallback
    const latentSyncApiUrl = process.env.LATENTSYNC_API_URL || 'http://localhost:6900';
    console.log(`Connecting to LatentSync API at: ${latentSyncApiUrl}`);

    const response = await axios.post(
      `${latentSyncApiUrl}/api/lipsync`,
      form,
      {
        headers: {
          ...form.getHeaders(),
        },
        responseType: 'arraybuffer',
        timeout: 300000, // 5 minute timeout for long processing
      }
    );

    // Create outputs directory if it doesn't exist
    const outputDir = path.join(__dirname, '../outputs');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Save with unique filename
    const outputFilePath = path.join(outputDir, `lipsync_${Date.now()}.mp4`);
    fs.writeFileSync(outputFilePath, response.data);

    console.log(`Lipsync video generated and saved to: ${outputFilePath}`);
    res.download(outputFilePath);
  } catch (error) {
    console.error('LatentSync API error:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data.toString());
    }
    res.status(500).json({ error: 'Lip sync generation failed' });
  }
};

module.exports = { lipsync };
