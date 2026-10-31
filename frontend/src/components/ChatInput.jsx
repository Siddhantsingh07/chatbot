/**
 * ChatInput.jsx – Text input bar with Web Speech Voice Search & Quick Chips.
 * Matches the reference design with paperclip, send arrow, and circular purple voice button.
 */
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useVoiceInput } from '../hooks/useVoiceInput';
import '../styles/ChatInput.css';

const QUICK_CHIP_QUESTIONS = {
  admissions:   'What is the admission process for B.Tech at ABES?',
  fees:         'What is the tuition fee structure?',
  scholarships: 'What scholarships are available at ABES?',
  exams:        'When are the semester exams held?',
  timetable:    'Where can I check the class timetable?',
  hostel:       'What are the hostel and mess facilities?',
  placements:   'What is the average and highest placement package?',
  library:      'What are the central library timings?',
  documents:    'How do I apply for a bonafide or migration certificate?',
  campus:       'What are the campus dress code and rules?',
  contact:      'How do I contact the Director or Registrar office?',
};

export default function ChatInput({ onSubmit, isLoading, categories = [] }) {
  const [value, setValue] = useState('');
  const [showChips, setShowChips] = useState(false);
  const [voiceLang, setVoiceLang] = useState('en-IN'); // 'en-IN' or 'hi-IN'
  const textareaRef = useRef(null);

  // Voice Search Hook
  const {
    isListening,
    isSupported,
    error: voiceError,
    toggleListening,
  } = useVoiceInput({
    lang: voiceLang,
    onTranscript: (transcript) => {
      setValue(transcript);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
        textareaRef.current.style.height = `${Math.min(
          textareaRef.current.scrollHeight,
          150
        )}px`;
      }
    },
  });

  // Auto-resize textarea
  const handleChange = (e) => {
    setValue(e.target.value);
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = 'auto';
      ta.style.height = `${Math.min(ta.scrollHeight, 150)}px`;
    }
  };

  const handleSend = useCallback(() => {
    const trimmed = value.trim();
    if (!trimmed || isLoading) return;
    onSubmit(trimmed);
    setValue('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  }, [value, isLoading, onSubmit]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleChipClick = (cat) => {
    const q = QUICK_CHIP_QUESTIONS[cat] || `Tell me about ${cat}`;
    onSubmit(q);
    setShowChips(false);
  };

  const canSend = value.trim().length > 0 && !isLoading;

  return (
    <div className="chat-input-wrapper">
      {/* Voice Recording / Listening Banner */}
      {isListening && (
        <div className="voice-active-banner">
          <div className="voice-pulse-circle">
            <span className="pulse-ring"></span>
            🎙️
          </div>
          <div className="voice-active-text">
            <strong>Listening...</strong> Speak your query in {voiceLang === 'hi-IN' ? 'Hindi' : 'English'}
          </div>
          <div className="voice-controls">
            <button
              className="voice-lang-btn"
              onClick={() => setVoiceLang((prev) => (prev === 'en-IN' ? 'hi-IN' : 'en-IN'))}
              title="Switch Voice Language"
            >
              Lang: {voiceLang === 'hi-IN' ? 'हिन्दी' : 'EN'}
            </button>
            <button className="voice-stop-btn" onClick={toggleListening}>
              Done ⏹
            </button>
          </div>
        </div>
      )}

      {/* Voice Error Notification */}
      {voiceError && (
        <div className="voice-error-banner">
          ⚠️ {voiceError}
        </div>
      )}

      {/* Quick Suggestion Chips Popover (via paperclip) */}
      {showChips && categories.length > 0 && (
        <div className="quick-chips-popover">
          <div className="popover-header">
            <span>Quick Query Suggestions</span>
            <button className="popover-close" onClick={() => setShowChips(false)}>
              ✕
            </button>
          </div>
          <div className="chips-grid">
            {categories.map((cat) => (
              <button
                key={cat}
                className="chip-btn"
                onClick={() => handleChipClick(cat)}
                disabled={isLoading}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Input Row matching reference layout */}
      <div className={`input-container ${isListening ? 'listening' : ''}`}>
        {/* Attachment / Quick Chips Button */}
        <button
          className={`input-btn attach-btn ${showChips ? 'active' : ''}`}
          onClick={() => setShowChips((prev) => !prev)}
          title="Quick Suggestions / FAQ Topics"
          aria-label="Quick Topics"
        >
          📎
        </button>

        {/* Text Area */}
        <textarea
          ref={textareaRef}
          className="chat-textarea"
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={
            isListening
              ? "Listening... speak now..."
              : "Type a message or click 🎙️ for voice search..."
          }
          rows={1}
          disabled={isLoading}
          aria-label="Message input"
        />

        {/* Send Button (Purple Paper Airplane) */}
        <button
          className="input-btn send-btn"
          onClick={handleSend}
          disabled={!canSend}
          title="Send (Enter)"
          aria-label="Send message"
        >
          <svg
            className="send-icon"
            viewBox="0 0 24 24"
            width="20"
            height="20"
            fill="currentColor"
          >
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        </button>

        {/* Voice Search Microphone Button (Circular Purple Icon on right) */}
        <button
          className={`voice-mic-btn ${isListening ? 'active' : ''}`}
          onClick={toggleListening}
          disabled={!isSupported || isLoading}
          title={
            !isSupported
              ? "Voice recognition not supported in this browser"
              : isListening
              ? "Stop listening"
              : "Voice Search (Speak in English or Hindi)"
          }
          aria-label="Voice search microphone"
        >
          🎙️
        </button>
      </div>

      <div className="input-hint">
        Press <kbd>Enter</kbd> to send · Click <kbd>🎙️</kbd> for Voice Search · Powered by ABES Help Desk
      </div>
    </div>
  );
}
