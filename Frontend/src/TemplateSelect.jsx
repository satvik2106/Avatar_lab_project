import React, { useRef, useState } from 'react';
import { useHistory } from 'react-router-dom';
import './TemplateSelect.css';
import ParticleBackgroundSimple from './ParticleBackgroundSimple';

const templates = [
  {
    id: 'template1',
    name: 'Person A',
    imageUrl: '/assets/demo1_video.mp4',
    audioUrl: '/assets/demo1.wav',
    posterUrl: '/assets/poster1.jpg'
  },
  {
    id: 'template2',
    name: 'Person B',
    imageUrl: '/assets/demo2_video.mp4',
    audioUrl: '/assets/demo2.wav',
    posterUrl: '/assets/poster2.jpg'
  },
  {
    id: 'template3',
    name: 'Person C',
    imageUrl: '/assets/demo3.mp4',
    audioUrl: '/assets/demo3.wav',
    posterUrl: '/assets/poster3.jpg'
  },
  {
    id: 'template4',
    name: 'Person D',
    imageUrl: '/assets/spokesman.mp4',
    audioUrl: '/assets/bark_output_2.wav',
    posterUrl: '/assets/poster4.jpg'
  },
  {
    id: 'template5',
    name: 'Person E',
    imageUrl: '/assets/woman-talking-podcast.mp4',
    audioUrl: '/assets/bark_output_0.wav',
    posterUrl: '/assets/poster4.jpg'
  },
  {
    id: 'template6',
    name: 'Person F',
    imageUrl: '/assets/doctor-speaking.mp4',
    audioUrl: '/assets/small-e-girl-speak.wav',
    posterUrl: '/assets/poster4.jpg'
  },
];

const TemplateSelect = () => {
  const [selectedTemplateId, setSelectedTemplateId] = useState(null);
  const [hoveredTemplateId, setHoveredTemplateId] = useState(null);
  const history = useHistory();

  const audioRefs = useRef({});

  const handleMouseEnter = (templateId) => {
    setHoveredTemplateId(templateId);
    const audio = audioRefs.current[templateId];
    if (audio) {
      audio.currentTime = 0;
      audio.play().catch(err => console.log("Audio play error:", err));
    }
  };

  const handleMouseLeave = (templateId) => {
    setHoveredTemplateId(null);
    const audio = audioRefs.current[templateId];
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }
  };

  const selectedTemplate = templates.find((t) => t.id === selectedTemplateId);

  const handleConfirm = () => {
    if (!selectedTemplate) {
      alert('Please select a template before continuing.');
      return;
    }

    history.push('/enter-transcript', {
      videoTemplate: selectedTemplate,
      audioTemplate: selectedTemplate,
    });
  };

  return (
    <div className="template-select-page dark">
      <ParticleBackgroundSimple />

      <div className="background-overlay"></div>

      <div style={{
        position: 'relative',
        zIndex: 1,
        width: '100%',
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px 0'
      }}>
        <h2 className="page-title">Select Avatar Template</h2>

        <div className="template-grid">
          {templates.map((template) => (
            <div
              key={template.id}
              className={`template-card glassmorphism ${selectedTemplateId === template.id ? 'selected' : ''}`}
              onClick={() => setSelectedTemplateId(template.id)}
              onMouseEnter={() => handleMouseEnter(template.id)}
              onMouseLeave={() => handleMouseLeave(template.id)}
              role="button"
              tabIndex={0}
              aria-pressed={selectedTemplateId === template.id}
              onKeyPress={(e) => {
                if (e.key === 'Enter' || e.key === ' ') setSelectedTemplateId(template.id);
              }}
            >
              <div className="card-media-wrapper">
                {hoveredTemplateId === template.id ? (
                  <video
                    src={template.imageUrl}
                    muted
                    loop
                    autoPlay
                    playsInline
                    preload="metadata"
                    className="template-video-preview"
                    poster={template.posterUrl}
                  />
                ) : (
                  <img
                    src={template.posterUrl}
                    alt={`Poster of ${template.name}`}
                    className="template-image-preview"
                  />
                )}
                <div className="media-overlay"></div>
              </div>

              {/* Hidden audio used for hover */}
              <audio
                ref={(el) => (audioRefs.current[template.id] = el)}
                src={template.audioUrl}
                preload="auto"
              />

              <div className="template-info">
                <p>{template.name}</p>
                <audio controls key={template.audioUrl} preload="metadata">
                  <source
                    src={template.audioUrl}
                    type={`audio/${template.audioUrl.split('.').pop()}`}
                  />
                  Your browser does not support the audio element.
                </audio>
              </div>
            </div>
          ))}
        </div>

        <button
          className="confirm-btn"
          onClick={handleConfirm}
          disabled={!selectedTemplateId}
        >
          <span>Confirm Selection & Proceed</span>
        </button>
      </div>
    </div>
  );
};

export default TemplateSelect;
