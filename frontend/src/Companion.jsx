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

// Returns the CSS filter for a puffle based on hue and firstClick
const getPuffleFilter = (id, hue, firstClick) => {
  if (firstClick) return 'none'; // no filter on first click
  if (id === 'black') {
    return `brightness(1) saturate(1)`; // preserve true black
  }
  return `hue-rotate(${hue}deg) saturate(1.2)`;
};

function Customization({ onClose }) {
  const [step, setStep] = useState('choose'); // 'choose' | 'color'
  const [selected, setSelected] = useState(null);
  const [hue, setHue] = useState(0);
  const [firstClick, setFirstClick] = useState(true); // show original color first

  const choosePuffle = (p) => {
    setSelected(p);
    setHue(0);       // slider starts at 0
    setStep('color'); 
    setFirstClick(true); // show original image first
  };

  const handleSliderChange = (value) => {
    setHue(value);
    setFirstClick(false); // once slider moves, filter is applied
  };

  return (
    <div className="customization-page">
      <header className="customization-header">
        <h2>{step === 'choose' ? 'Choose Your Puffle!' : `Choose Your Puffle's Color`}</h2>
        <button onClick={() => onClose && onClose()}>Close</button>
      </header>

      <div className={`customization-body ${step === 'choose' ? 'chooser' : 'color'}`}>
        {step === 'choose' && (
          <div className="chooser-grid">
            {PUFFLES.map((p) => (
              <button key={p.id} className="puffle-button" onClick={() => choosePuffle(p)}>
                <img
                  src={p.file}
                  alt={p.label}
                  className="puffle-thumb"
                  style={{ filter: 'none' }} // show original color in chooser
                />
                <div className="puffle-label">{p.label}</div>
              </button>
            ))}
          </div>
        )}

        {step === 'color' && selected && (
          <div className="color-pane">
            <div className="image-center">
              <img
                src={selected.file}
                alt={selected.label}
                className="big-puffle"
                style={{ filter: getPuffleFilter(selected.id, hue, firstClick) }}
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
              />
              <div className="color-actions">
                <button onClick={() => setStep('choose')}>Back</button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Customization;
