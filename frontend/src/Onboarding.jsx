import React, { useState, useEffect } from 'react';
import './Onboarding.css';

function Onboarding({ onComplete }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    subject: '',
    duration: '',
    audioType: '',
    studyGuide: null,
    pomodoroSessions: [],
    playlist: null,
  });

  const durations = [
    { value: 30, label: '30 minutes' },
    { value: 60, label: '1 hour' },
    { value: 90, label: '1 hour 30 minutes' },
    { value: 120, label: '2 hours' },
    { value: 150, label: '2 hours 30 minutes' },
    { value: 180, label: '3 hours' },
  ];

  const [durationIndex, setDurationIndex] = useState(0);

  const audioTypes = [
    { value: 'lofi', label: 'Lo-Fi Hip Hop', icon: '🎵' },
    { value: 'nature', label: 'Nature Sounds', icon: '🌿' },
    { value: 'classical', label: 'Classical Music', icon: '🎻' },
    { value: 'ambient', label: 'Ambient', icon: '🌊' },
    { value: 'binaural', label: 'Binaural Beats', icon: '🔊' },
    { value: 'silence', label: 'Silence', icon: '🔇' },
  ];

  const handleNext = () => {
    if (step === 3) {
      // Generate study guide and pomodoro sessions after audio selection
      generateStudyPlan();
      setStep(4);
    } else if (step === 4) {
      // After step 4, submit and go to main study view
      handleSubmit();
    } else if (step < 4) {
      setStep(step + 1);
    }
  };

  const handleDurationPrev = () => {
    setDurationIndex((prev) => {
      const newIndex = prev === 0 ? durations.length - 1 : prev - 1;
      updateFormData('duration', durations[newIndex].value.toString());
      return newIndex;
    });
  };

  const handleDurationNext = () => {
    setDurationIndex((prev) => {
      const newIndex = prev === durations.length - 1 ? 0 : prev + 1;
      updateFormData('duration', durations[newIndex].value.toString());
      return newIndex;
    });
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const generateStudyPlan = () => {
    // Calculate number of pomodoro sessions (25 min each)
    const totalMinutes = parseInt(formData.duration);
    const pomodoroCount = Math.ceil(totalMinutes / 25);
    
    // Generate tasks for each pomodoro session
    const sessions = Array.from({ length: pomodoroCount }, (_, i) => ({
      id: i + 1,
      task: `Task ${i + 1}: Study ${formData.subject}`,
      duration: i === pomodoroCount - 1 ? totalMinutes % 25 || 25 : 25,
      completed: false,
    }));

    const studyGuide = {
      subject: formData.subject,
      totalDuration: totalMinutes,
      sessions: sessions,
    };

    setFormData(prev => ({
      ...prev,
      studyGuide,
      pomodoroSessions: sessions,
    }));
  };

  const handleSubmit = async () => {
    // Send data to backend with ElevenLabs playlist setup
    try {
      const response = await fetch('http://localhost:8000/api/session/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subject: formData.subject,
          duration: parseInt(formData.duration),
          audio_type: formData.audioType,
          study_guide: formData.studyGuide,
          pomodoro_sessions: formData.pomodoroSessions,
          playlist_provider: 'elevenlabs',
        }),
      });

      if (response.ok) {
        const data = await response.json();
        onComplete({
          ...formData,
          currentTask: formData.pomodoroSessions[0]?.task || '',
          currentSessionIndex: 0,
          sessionId: data.session_id,
        });
      } else {
        console.error('Failed to start session');
        // Still complete onboarding even if backend fails (for testing)
        onComplete({
          ...formData,
          currentTask: formData.pomodoroSessions[0]?.task || '',
          currentSessionIndex: 0,
        });
      }
    } catch (error) {
      console.error('Error starting session:', error);
      // Still complete onboarding even if backend fails (for testing)
      onComplete({
        ...formData,
        currentTask: formData.pomodoroSessions[0]?.task || '',
        currentSessionIndex: 0,
      });
    }
  };

  // Initialize duration when component mounts or when step changes to 2
  useEffect(() => {
    if (step === 2) {
      if (formData.duration) {
        const initialIndex = durations.findIndex(d => d.value.toString() === formData.duration);
        if (initialIndex >= 0) {
          setDurationIndex(initialIndex);
        }
      } else {
        setDurationIndex(0);
        updateFormData('duration', durations[0].value.toString());
      }
    }
  }, [step]);

  const updateFormData = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="onboarding-container">
      <div className="onboarding-card">
        <div className="onboarding-header">
          <h1>🐾 Welcome to Puffle!</h1>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
          <p className="step-indicator">Step {step} of 4</p>
        </div>

        <div className="onboarding-content">
          {/* Step 1: What are you studying? */}
          {step === 1 && (
            <div className="onboarding-step">
              <h2>What are you studying today?</h2>
              <p className="step-description">Enter the subject or topic you want to focus on</p>
              <input
                type="text"
                className="onboarding-input"
                placeholder="e.g., Machine Learning, Calculus, History..."
                value={formData.subject}
                onChange={(e) => updateFormData('subject', e.target.value)}
                autoFocus
              />
            </div>
          )}

          {/* Step 2: Duration */}
          {step === 2 && (
            <div className="onboarding-step">
              <h2>How long do you want to study?</h2>
              <p className="step-description">Select your study session duration</p>
              <div className="duration-carousel">
                <button 
                  className="carousel-btn carousel-btn-prev"
                  onClick={handleDurationPrev}
                  aria-label="Previous duration"
                >
                  ←
                </button>
                <div className="duration-carousel-content">
                  <div className="duration-display">
                    {durations[durationIndex].label}
                  </div>
                </div>
                <button 
                  className="carousel-btn carousel-btn-next"
                  onClick={handleDurationNext}
                  aria-label="Next duration"
                >
                  →
                </button>
              </div>
              <div className="carousel-dots">
                {durations.map((_, index) => (
                  <button
                    key={index}
                    className={`carousel-dot ${index === durationIndex ? 'active' : ''}`}
                    onClick={() => {
                      setDurationIndex(index);
                      updateFormData('duration', durations[index].value.toString());
                    }}
                    aria-label={`Select ${durations[index].label}`}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Step 3: Audio Type */}
          {step === 3 && (
            <div className="onboarding-step">
              <h2>What kind of audio would you like?</h2>
              <p className="step-description">Choose background audio for your study session</p>
              <div className="audio-grid">
                {audioTypes.map((audio) => (
                  <button
                    key={audio.value}
                    className={`audio-option ${formData.audioType === audio.value ? 'selected' : ''}`}
                    onClick={() => updateFormData('audioType', audio.value)}
                  >
                    <span className="audio-icon">{audio.icon}</span>
                    <span className="audio-label">{audio.label}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Step 4: Study Guide Preview */}
          {step === 4 && formData.studyGuide && (
            <div className="onboarding-step">
              <h2>Your Study Plan</h2>
              <p className="step-description">Review your personalized study guide and pomodoro sessions</p>
              <div className="study-guide">
                <div className="study-guide-header">
                  <h3>{formData.studyGuide.subject}</h3>
                  <p>Total Duration: {formData.studyGuide.totalDuration} minutes</p>
                </div>
                <div className="sessions-list">
                  <h4>Pomodoro Sessions:</h4>
                  {formData.studyGuide.sessions.map((session) => (
                    <div key={session.id} className="session-item">
                      <span className="session-number">Session {session.id}</span>
                      <span className="session-task">{session.task}</span>
                      <span className="session-duration">{session.duration} min</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="onboarding-actions">
          {step > 1 && (
            <button className="btn-secondary" onClick={handleBack}>
              ← Back
            </button>
          )}
          {step < 4 && (
            <button 
              className="btn-primary" 
              onClick={handleNext}
              disabled={
                (step === 1 && !formData.subject.trim()) ||
                (step === 2 && !formData.duration) ||
                (step === 3 && !formData.audioType)
              }
            >
              Next →
            </button>
          )}
          {step === 4 && (
            <button 
              className="btn-primary submit-btn" 
              onClick={handleNext}
            >
              🚀 Start Study Session
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Onboarding;