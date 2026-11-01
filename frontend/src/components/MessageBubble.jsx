/**
 * MessageBubble.jsx – Chat Bubble component matching the reference UI.
 * Features sender avatar, purple user bubble, bot card, speech output, and status checkmarks.
 */
import React, { useState } from 'react';

function formatTime(date) {
  if (!(date instanceof Date) || isNaN(date)) return '';
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function MessageBubble({ message }) {
  const { role, text, timestamp, category, confidence } = message;
  const isBot = role === 'bot';
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Text to Speech playback
  const handleSpeak = () => {
    if (!window.speechSynthesis) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    // Detect if text has Hindi characters
    if (/[\u0900-\u097F]/.test(text)) {
      utterance.lang = 'hi-IN';
    } else {
      utterance.lang = 'en-IN';
    }

    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className={`message-row ${isBot ? 'message-row--bot' : 'message-row--user'}`}>
      {/* Bot Avatar */}
      {isBot && (
        <div className="avatar-bubble avatar-bubble--bot" title="ABES Help Desk">
          🏛️
        </div>
      )}

      <div className="message-content-group">
        {/* Sender Name & Timestamp for Bot */}
        {isBot && (
          <div className="message-header-info">
            <span className="sender-name">ABES Help Desk</span>
            <span className="message-time">{formatTime(timestamp)}</span>
            <span className="read-receipt" title="Verified response">✓✓</span>
          </div>
        )}

        {/* Message Bubble Body */}
        <div className={`message-bubble ${isBot ? 'bubble--bot' : 'bubble--user'}`}>
          <div className="bubble-text">{text}</div>

          {/* Action Row for Bot: TTS Speaker Button */}
          {isBot && window.speechSynthesis && (
            <div className="bubble-footer">
              <button
                className={`speak-btn ${isSpeaking ? 'speaking' : ''}`}
                onClick={handleSpeak}
                title={isSpeaking ? 'Stop speaking' : 'Listen to answer'}
                aria-label="Text to speech"
              >
                {isSpeaking ? '🔊 Stop' : '🔈 Listen'}
              </button>
            </div>
          )}
        </div>

        {/* User Timestamp */}
        {!isBot && (
          <div className="message-header-info user-info">
            <span className="message-time">{formatTime(timestamp)}</span>
            <span className="read-receipt user-receipt">✓✓</span>
          </div>
        )}
      </div>

      {/* User Avatar */}
      {!isBot && (
        <div className="avatar-bubble avatar-bubble--user" title="You">
          👤
        </div>
      )}
    </div>
  );
}
