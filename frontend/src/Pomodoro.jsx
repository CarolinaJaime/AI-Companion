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
    <div className="pomodoro-container-simple">
      <div className="pomodoro-timer-circle">
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
  );
}

export default Pomodoro;



