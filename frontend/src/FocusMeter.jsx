import React, { useEffect, useState } from 'react';
import './FocusMeter.css';

function FocusMeter({ focusScore, isFocused, sessionDuration }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(focusScore);
    }, 100);
    return () => clearTimeout(timer);
  }, [focusScore]);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    }
    return `${minutes}m ${secs}s`;
  };

  const getScoreColor = () => {
    if (animatedScore >= 80) return '#10b981';
    if (animatedScore >= 50) return '#f59e0b';
    return '#ef4444';
  };

  const getScoreLabel = () => {
    if (animatedScore >= 80) return 'Excellent Focus';
    if (animatedScore >= 50) return 'Good Focus';
    return 'Needs Improvement';
  };

  return (
    <div className="focus-meter-container">
      <div className="focus-meter-header">
        <h2>Focus Meter</h2>
        <div className={`focus-status ${isFocused ? 'focused' : 'distracted'}`}>
          <span className="status-icon">{isFocused ? '👁️' : '👀'}</span>
          <span>{isFocused ? 'Focused' : 'Distracted'}</span>
        </div>
      </div>

      <div className="focus-score-display">
        <div className="score-circle">
          <svg className="score-ring" viewBox="0 0 200 200">
            <circle
              className="score-ring-background"
              cx="100"
              cy="100"
              r="80"
            />
            <circle
              className="score-ring-progress"
              cx="100"
              cy="100"
              r="80"
              style={{
                strokeDasharray: `${2 * Math.PI * 80}`,
                strokeDashoffset: `${2 * Math.PI * 80 * (1 - animatedScore / 100)}`,
                stroke: getScoreColor(),
              }}
            />
          </svg>
          <div className="score-text">
            <span className="score-value">{Math.round(animatedScore)}</span>
            <span className="score-label">%</span>
          </div>
        </div>
        <p className="score-description">{getScoreLabel()}</p>
      </div>

      <div className="focus-stats">
        <div className="stat-item">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <div className="stat-label">Session Duration</div>
            <div className="stat-value">{formatTime(sessionDuration)}</div>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <div className="stat-label">Focus Status</div>
            <div className={`stat-value ${isFocused ? 'focused' : 'distracted'}`}>
              {isFocused ? 'On Track' : 'Off Track'}
            </div>
          </div>
        </div>
      </div>

      <div className="focus-tips">
        <h3>💡 Focus Tips</h3>
        <ul>
          <li>Keep your eyes on the screen</li>
          <li>Take regular breaks with Pomodoro</li>
          <li>Stay hydrated and maintain good posture</li>
          <li>Minimize distractions in your environment</li>
        </ul>
      </div>
    </div>
  );
}

export default FocusMeter;

