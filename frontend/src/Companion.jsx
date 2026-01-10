import React, { useState, useEffect, useRef } from 'react';
import './Companion.css';

function Companion({ message, focusScore, isFocused }) {
  const [messages, setMessages] = useState([]);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const messagesEndRef = useRef(null);
  const synthRef = useRef(null);

  useEffect(() => {
    synthRef.current = window.speechSynthesis;
    return () => {
      if (synthRef.current) {
        synthRef.current.cancel();
      }
    };
  }, []);

  useEffect(() => {
    if (message) {
      setMessages(prev => [...prev, { text: message, timestamp: Date.now() }]);
      
      // Speak the message using Web Speech API
      if (synthRef.current && message.trim()) {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        utterance.volume = 0.8;
        
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);
        
        synthRef.current.speak(utterance);
      }
    }
  }, [message]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const getCompanionEmotion = () => {
    if (focusScore >= 80) return 'happy';
    if (focusScore >= 50) return 'neutral';
    if (isFocused) return 'encouraging';
    return 'concerned';
  };

  const emotion = getCompanionEmotion();

  return (
    <div className="companion-container">
      <div className="companion-header">
        <div className="companion-avatar">
          <div className={`companion-face ${emotion}`}>
            <span className="companion-emoji">
              {emotion === 'happy' && '😊'}
              {emotion === 'neutral' && '😐'}
              {emotion === 'encouraging' && '💪'}
              {emotion === 'concerned' && '🤔'}
            </span>
          </div>
          {isSpeaking && <div className="speaking-indicator">🔊</div>}
        </div>
        <h2>Puffle</h2>
        <p className="companion-status">
          {isFocused ? 'You\'re focused! Keep it up!' : 'Let\'s get back on track!'}
        </p>
      </div>

      <div className="companion-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>👋 Hi! I'm Puffle, your study companion.</p>
            <p>I'll help you stay focused and motivated during your study sessions!</p>
          </div>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className="message-bubble">
              <p>{msg.text}</p>
              <span className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

export default Companion;

