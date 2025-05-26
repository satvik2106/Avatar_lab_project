const axios = require('axios');
const fs = require('fs');
const path = require('path');

const generateSpeech = async (req, res) => {
  try {
    const { text, speaker_audio_path, language = 'en-us' } = req.body;

    // Validate input
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }

    // Get available speaker audio files
    const defaultSpeakerPath = path.join(__dirname, '../assets/default_speaker.wav');
    const ttsOutputsDir = path.join(__dirname, '../TTS_api/outputs');
    
    // Determine which speaker audio to use
    let speakerPath = speaker_audio_path;
    
    if (!speakerPath) {
      // Check if default speaker exists
      if (fs.existsSync(defaultSpeakerPath) && fs.statSync(defaultSpeakerPath).size > 0) {
        speakerPath = defaultSpeakerPath;
        console.log(`Using default speaker audio: ${speakerPath}`);
      } else {
        // Find any WAV file in the TTS outputs directory
        try {
          const outputFiles = fs.readdirSync(ttsOutputsDir);
          const wavFiles = outputFiles.filter(file => file.endsWith('.wav'));
          
          if (wavFiles.length > 0) {
            speakerPath = path.join(ttsOutputsDir, wavFiles[0]);
            console.log(`Using TTS output as speaker audio: ${speakerPath}`);
            
            // Also copy this file to be the default speaker for future use
            fs.copyFileSync(speakerPath, defaultSpeakerPath);
            console.log(`Copied to default speaker location: ${defaultSpeakerPath}`);
          } else {
            return res.status(500).json({
              error: 'No speaker audio available',
              message: 'Could not find any speaker audio files to use as reference'
            });
          }
        } catch (err) {
          console.error('Error finding speaker audio:', err);
          return res.status(500).json({
            error: 'Speaker audio error',
            message: 'Error finding or accessing speaker audio files'
          });
        }
      }
    }

    console.log(`Generating speech for text: "${text.substring(0, 50)}${text.length > 50 ? '...' : ''}"`);
    console.log(`Using speaker audio: ${speakerPath}`);

    // Get TTS API URL from environment variable or use default
    const ttsApiUrl = process.env.TTS_API_URL || 'http://localhost:8000';
    
    const response = await axios.post(
      `${ttsApiUrl}/api/generate_speech`,
      {
        text,
        speaker_audio_path: speakerPath,
        language
      },
      {
        responseType: 'arraybuffer',
        timeout: 60000 // 60 second timeout
      }
    );

    // Create outputs directory if it doesn't exist
    const outputDir = path.join(__dirname, '../outputs');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Save the audio file with a unique name
    const outputFilePath = path.join(outputDir, `speech_${Date.now()}.wav`);
    fs.writeFileSync(outputFilePath, response.data);

    console.log(`Speech generated and saved to: ${outputFilePath}`);
    res.download(outputFilePath); // Sends audio file to client
  } catch (error) {
    console.error('TTS API error:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    }
    res.status(500).json({
      error: 'TTS generation failed',
      message: error.message
    });
  }
};

module.exports = { generateSpeech };
