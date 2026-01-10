import React, { useState, useEffect } from 'react';
import './App.css';
import Companion from './Companion';
import FocusMeter from './FocusMeter';
import Pomodoro from './Pomodoro';
import wsService from '../services/websocket';

function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [focusData, setFocusData] = useState({
    isFocused: false,
    focusScore: 0,
    sessionDuration: 0,
  });
  const [companionMessage, setCompanionMessage] = useState('');
  const [pomodoroState, setPomodoroState] = useState({
    isRunning: false,
    isBreak: false,
    timeRemaining: 25 * 60,
    cycle: 0,
  });

  useEffect(() => {
    // Connect WebSocket
    wsService.connect();

    // Set up event listeners
    const handleConnected = () => setIsConnected(true);
    const handleDisconnected = () => setIsConnected(false);
    
    const handleMessage = (data) => {
      // Handle focus detection updates
      if (data.focus !== undefined) {
        setFocusData(prev => ({
          ...prev,
          isFocused: data.focus,
          focusScore: data.focus_score || prev.focusScore,
        }));
      }

      // Handle focus score updates
      if (data.focus_score !== undefined) {
        setFocusData(prev => ({
          ...prev,
          focusScore: data.focus_score,
        }));
      }

      // Handle session duration
      if (data.session_duration !== undefined) {
        setFocusData(prev => ({
          ...prev,
          sessionDuration: data.session_duration,
        }));
      }

      // Handle AI companion messages
      if (data.message) {
        setCompanionMessage(data.message);
      }

      // Handle Pomodoro updates
      if (data.pomodoro) {
        setPomodoroState(prev => ({
          ...prev,
          ...data.pomodoro,
        }));
      }
    };

    wsService.on('connected', handleConnected);
    wsService.on('disconnected', handleDisconnected);
    wsService.on('message', handleMessage);
    wsService.on('focus_update', handleMessage);
    wsService.on('pomodoro_update', handleMessage);
    wsService.on('ai_message', handleMessage);

    // Cleanup
    return () => {
      wsService.off('connected', handleConnected);
      wsService.off('disconnected', handleDisconnected);
      wsService.off('message', handleMessage);
      wsService.off('focus_update', handleMessage);
      wsService.off('pomodoro_update', handleMessage);
      wsService.off('ai_message', handleMessage);
    };
  }, []);

  const handleStartPomodoro = () => {
    wsService.send({ action: 'start_pomodoro' });
  };

  const handleStopPomodoro = () => {
    wsService.send({ action: 'stop_pomodoro' });
  };

  const handleResetPomodoro = () => {
    wsService.send({ action: 'reset_pomodoro' });
  };

  return (
    <div className="app">
      <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
        <span className="status-dot"></span>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      <header className="app-header">
        <h1>🐾 Puffle</h1>
        <p>Your AI-Powered Study Companion</p>
      </header>

      <div className="app-content">
        <div className="app-main">
          <Companion 
            message={companionMessage}
            focusScore={focusData.focusScore}
            isFocused={focusData.isFocused}
          />
          <FocusMeter 
            focusScore={focusData.focusScore}
            isFocused={focusData.isFocused}
            sessionDuration={focusData.sessionDuration}
          />
        </div>

        <div className="app-sidebar">
          <Pomodoro
            state={pomodoroState}
            onStart={handleStartPomodoro}
            onStop={handleStopPomodoro}
            onReset={handleResetPomodoro}
          />
        </div>
      </div>
    </div>
  );
}

export default App;

