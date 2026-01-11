import React, { useState } from 'react';
import './Customization.css';

const PUFFLES = [
  { id: 'black', label: 'Black Puffle', file: '/images/Black_Puffle.png' },
  { id: 'blue', label: 'Blue Puffle', file: '/images/bluepuffle.png' },
  { id: 'brown', label: 'Brown Puffle', file: '/images/Brown_puffle.png' },
  { id: 'purple', label: 'Purple Puffle', file: '/images/Purple_Puffle.png' },
  { id: 'white', label: 'White Puffle', file: '/images/White_Puffle.png' },
  { id: 'red', label: 'Red Puffle', file: '/images/Red_puffle.png' },
  { id: 'pink', label: 'Pink Puffle', file: '/images/Pink_Puffle.png' },
  { id: 'orange', label: 'Orange Puffle', file: '/images/orange_puffle.png' }
];

// Returns CSS filter for puffle
const getPuffleFilter = (id, hue, firstClick) => {
  if (firstClick) return 'none'; // show original color on first click
  if (id === 'black') {
    return `brightness(1) sepia(1) hue-rotate(${hue}deg) saturate(2)`; // black can change hue
  }
  return `hue-rotate(${hue}deg) saturate(1.2)`;
};

function Customization({ onClose }) {
  const [step, setStep] = useState('choose'); // 'choose' | 'color'
  const [selected, setSelected] = useState(null);
  const [hue, setHue] = useState(0);
  const [firstClick, setFirstClick] = useState(true); // show original color first
  const [savedPuffle, setSavedPuffle] = useState(null); // store saved puffle

  const choosePuffle = (p) => {
    setSelected(p);
    setHue(0);
    setStep('color');
    setFirstClick(true);
  };

  const handleSliderChange = (value) => {
    setHue(value);
    setFirstClick(false);
  };

  const handleSave = () => {
    // Save selected puffle and hue
    setSavedPuffle({ ...selected, hue });
    setStep('choose'); // return to chooser
  };

  return (
    <div className="customization-page">
      <header className="customization-header">
        <h2>{step === 'choose' ? 'Choose Your Puffle!' : `Customize Your Puffle`}</h2>
        <button onClick={() => onClose && onClose()}>Close</button>
      </header>

      <div className={`customization-body ${step === 'choose' ? 'chooser' : 'color'}`}>
        {/* CHOOSER GRID */}
        {step === 'choose' && (
          <div className="chooser-grid">
            {PUFFLES.map((p) => (
              <button key={p.id} className="puffle-button" onClick={() => choosePuffle(p)}>
                <img
                  src={p.file}
                  alt={p.label}
                  className="puffle-thumb"
                  style={{ filter: 'none' }} // show original color
                />
                <div className="puffle-label">{p.label}</div>
              </button>
            ))}
          </div>
        )}

        {/* COLOR CUSTOMIZATION */}
        {step === 'color' && selected && (
          <div className="color-pane">
            <div className="image-center">
              <img
                src={selected.file}
                alt={selected.label}
                className="big-puffle"
                style={{ width: '380px', height: '380px', objectFit: 'contain', filter: getPuffleFilter(selected.id, hue, firstClick) }}
              />
            </div>

            <div className="slider-area simple-slider">
              <div className="color-display">
                <div className="swatch" style={{ background: `hsl(${hue},100%,50%)` }} />
                <div className="color-label">Hue: {hue}°</div>
              </div>

              <input
                type="range"
                min="0"
                max="360"
                value={hue}
                onChange={(e) => handleSliderChange(parseInt(e.target.value, 10))}
                className="hue-slider"
                style={{ width: '380px' }}
              />

              <div className="color-actions" style={{ display: 'flex', gap: '12px', marginTop: '12px' }}>
                <button onClick={() => setStep('choose')}>Back</button>
                <button onClick={handleSave}>Save</button>
              </div>
            </div>
          </div>
        )}

        {/* SHOW SAVED PUFFLE */}
        {savedPuffle && step === 'choose' && (
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <h4>Saved Puffle:</h4>
            <img
              src={savedPuffle.file}
              alt={savedPuffle.label}
              style={{
                width: '120px',
                height: '120px',
                objectFit: 'contain',
                filter: getPuffleFilter(savedPuffle.id, savedPuffle.hue, false)
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default Customization;
