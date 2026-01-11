// Main App component
import React, { useState, useEffect } from 'react';
import './App.css';
import Onboarding from './Onboarding';
import Customization from './Customization';
import Companion from './Companion';
import Pomodoro from './Pomodoro';
import wsService from './services/websocket';

// State management
function App() {
  const [isOnboarding, setIsOnboarding] = useState(true);
  const [isCustomizing, setIsCustomizing] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [sessionData, setSessionData] = useState(null);
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
  const [currentTask, setCurrentTask] = useState('');

  useEffect(() => {
    // Connect WebSocket only after onboarding
    if (!isOnboarding) {
      wsService.connect();

      // Update connection status
      const handleConnected = () => setIsConnected(true);
      const handleDisconnected = () => setIsConnected(false);
      
      // Handle WebSocket messages
      const handleMessage = (data) => {
        console.log('Received message:', data);
        
        // Handle focus detection updates
        if (data.focus !== undefined) {
          setFocusData(prev => ({
            ...prev, // Preserve existing state
            isFocused: data.focus,
            focusScore: data.focus_score || prev.focusScore, // Fallback to previous score if not provided
          }));
        }

        // Handle focus score updates (alternative path)
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

        // Handle current task updates
        if (data.current_task) {
          setCurrentTask(data.current_task);
        }
      };

      // Register event listeners
      wsService.on('connected', handleConnected);
      wsService.on('disconnected', handleDisconnected);
      wsService.on('message', handleMessage);
      wsService.on('focus_update', handleMessage);
      wsService.on('pomodoro_update', handleMessage);
      wsService.on('ai_message', handleMessage);

      // Cleanup event listeners
      return () => {
        wsService.off('connected', handleConnected);
        wsService.off('disconnected', handleDisconnected);
        wsService.off('message', handleMessage);
        wsService.off('focus_update', handleMessage);
        wsService.off('pomodoro_update', handleMessage);
        wsService.off('ai_message', handleMessage);
      };
    }
  }, [isOnboarding]);

  const handleOnboardingComplete = (data) => {
    setSessionData(data);
    setCurrentTask(data.currentTask || '');
    setIsOnboarding(false);
  };

  // Pomodoro control handlers
  const handleStartPomodoro = () => {
    wsService.send({ action: 'start_pomodoro' });
  };

  // Stop Pomodoro
  const handleStopPomodoro = () => {
    wsService.send({ action: 'stop_pomodoro' });
  };

  // Reset Pomodoro
  const handleResetPomodoro = () => {
    wsService.send({ action: 'reset_pomodoro' });
  };

  // Show onboarding first
  if (isOnboarding) {
    if (isCustomizing) {
      return <Customization onClose={() => setIsCustomizing(false)} />;
    }
    return <Onboarding onComplete={handleOnboardingComplete} onCustomize={() => setIsCustomizing(true)} />;
  }

  // Render the main app UI
  return (
    <div className="app">
      <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
        <span className="status-dot"></span>
        {isConnected ? 'Connected' : 'Disconnected'}
      </div>

      <header className="app-header">
        <h2 className="current-task-title">{currentTask || 'Ready to start!'}</h2>
      </header>

      <div className="app-content-simple">
        <div className="app-left">
          <Companion 
            message={companionMessage}
            focusScore={focusData.focusScore}
            isFocused={focusData.isFocused}
            isBreak={pomodoroState.isBreak}
          />
        </div>

        <div className="app-right">
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



