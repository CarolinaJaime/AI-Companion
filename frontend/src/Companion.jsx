// Companion component for the AI-powered study companion
import React, { useState, useEffect, useRef } from 'react';
import './Companion.css';

// Companion component props
function Companion({ message, focusScore, isFocused, isBreak }) {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const synthRef = useRef(null); // Reference to the Web Speech API

  useEffect(() => {
    // Initialize the Web Speech API
    synthRef.current = window.speechSynthesis;
    
    // Cleanup the Web Speech API
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  // Speak the message using Web Speech API (text-to-speech)
  useEffect(() => {
    if (message && synthRef.current && message.trim()) {
      const utterance = new SpeechSynthesisUtterance(message);
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      utterance.volume = 0.8;
      
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      
      synthRef.current.speak(utterance);
    }
  }, [message]);

  // Get the companion's emotion based on the focus score and whether they are focused
  const getCompanionEmotion = () => {
    // Show sleeping state during breaks
    if (isBreak) return 'sleeping';
    if (focusScore >= 80) return 'happy';
    if (focusScore >= 50) return 'neutral';
    if (isFocused) return 'encouraging'; 
    return 'concerned'; // Default emotion if no other condition is met
  };

  const emotion = getCompanionEmotion();

  return (
    <div className="companion-container-simple">
      <div className="companion-avatar-simple">
        <div className={`companion-face ${emotion}`}>
          <span className="companion-emoji">
            {emotion === 'sleeping' && '😴'}
            {emotion === 'happy' && '😊'}
            {emotion === 'neutral' && '😐'}
            {emotion === 'encouraging' && '💪'}
            {emotion === 'concerned' && '🤔'}
          </span>
        </div>
        {isSpeaking && <div className="speaking-indicator">🔊</div>}
      </div>
    </div>
  );
}

export default Companion;



