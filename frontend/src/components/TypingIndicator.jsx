/**
 * TypingIndicator.jsx – Animated typing indicator for ABES Help Desk.
 */
import React from 'react';
import '../styles/ChatWindow.css';

export default function TypingIndicator() {
  return (
    <div className="message-row message-row--bot" aria-live="polite">
      <div className="avatar-bubble avatar-bubble--bot">🏛️</div>
      <div className="typing-bubble">
        <span className="typing-label">ABES Help Desk is typing</span>
        <div className="typing-dots">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  );
}
