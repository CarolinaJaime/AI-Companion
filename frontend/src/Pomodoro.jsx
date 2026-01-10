import React, { useEffect, useState } from 'react';
import './Pomodoro.css';

function Pomodoro({ state, onStart, onStop, onReset }) {
  const [displayTime, setDisplayTime] = useState(state.timeRemaining || 25 * 60);

  useEffect(() => {
    setDisplayTime(state.timeRemaining);
  }, [state.timeRemaining]);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  };

  const getProgress = () => {
    const totalTime = state.isBreak ? 5 * 60 : 25 * 60;
    return ((totalTime - state.timeRemaining) / totalTime) * 100;
  };

  const getPhaseLabel = () => {
    if (!state.isRunning) return 'Ready to Start';
    return state.isBreak ? 'Break Time' : 'Focus Time';
  };

  const getPhaseEmoji = () => {
    if (!state.isRunning) return '🎯';
    return state.isBreak ? '☕' : '📚';
  };

  return (
    <div className="pomodoro-container">
      <div className="pomodoro-header">
        <h2>🍅 Pomodoro Timer</h2>
        <div className="pomodoro-cycle">
          Cycle #{state.cycle || 0}
        </div>
      </div>

      <div className="pomodoro-display">
        <div className="pomodoro-phase">
          <span className="phase-emoji">{getPhaseEmoji()}</span>
          <span className="phase-label">{getPhaseLabel()}</span>
        </div>

        <div className="pomodoro-timer">
          <div className="timer-circle">
            <svg className="timer-ring" viewBox="0 0 200 200">
              <circle
                className="timer-ring-background"
                cx="100"
                cy="100"
                r="85"
              />
              <circle
                className={`timer-ring-progress ${state.isBreak ? 'break' : 'work'}`}
                cx="100"
                cy="100"
                r="85"
                style={{
                  strokeDasharray: `${2 * Math.PI * 85}`,
                  strokeDashoffset: `${2 * Math.PI * 85 * (1 - getProgress() / 100)}`,
                }}
              />
            </svg>
            <div className="timer-text">
              <span className="timer-value">{formatTime(displayTime)}</span>
            </div>
          </div>
        </div>

        <div className="pomodoro-controls">
          {!state.isRunning ? (
            <button
              className="pomodoro-btn start-btn"
              onClick={onStart}
            >
              ▶️ Start
            </button>
          ) : (
            <>
              <button
                className="pomodoro-btn stop-btn"
                onClick={onStop}
              >
                ⏸️ Pause
              </button>
              <button
                className="pomodoro-btn reset-btn"
                onClick={onReset}
              >
                🔄 Reset
              </button>
            </>
          )}
        </div>
      </div>

      <div className="pomodoro-info">
        <div className="info-item">
          <span className="info-label">Work Session:</span>
          <span className="info-value">25 minutes</span>
        </div>
        <div className="info-item">
          <span className="info-label">Break:</span>
          <span className="info-value">5 minutes</span>
        </div>
        <div className="info-item">
          <span className="info-label">Status:</span>
          <span className={`info-value ${state.isRunning ? 'active' : 'inactive'}`}>
            {state.isRunning ? 'Active' : 'Inactive'}
          </span>
        </div>
      </div>

      <div className="pomodoro-tips">
        <h3>📝 Pomodoro Technique</h3>
        <ul>
          <li>Work for 25 minutes</li>
          <li>Take a 5-minute break</li>
          <li>After 4 cycles, take a longer break</li>
          <li>Stay focused during work sessions</li>
        </ul>
      </div>
    </div>
  );
}

export default Pomodoro;

