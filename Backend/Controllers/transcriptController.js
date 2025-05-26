exports.handleTranscript = (req, res) => {
    const { transcript } = req.body;
  
    if (!transcript) {
      return res.status(400).json({ message: 'Transcript is required.' });
    }
  
    // Simulate processing
    console.log('Received transcript:', transcript);
  
    res.status(200).json({ message: 'Transcript received.', data: transcript });
  };
  