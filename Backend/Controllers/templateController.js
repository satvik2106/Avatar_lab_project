exports.getTemplates = (req, res) => {
    // Simulated list of templates
    const templates = [
      { id: 1, name: 'Professional', file: 'pro_avatar.png' },
      { id: 2, name: 'Casual', file: 'casual_avatar.png' },
      { id: 3, name: 'Techie', file: 'tech_avatar.png' }
    ];
  
    res.status(200).json({ templates });
  };
  