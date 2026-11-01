/**
 * ChatWindow.jsx – Main Chat Timeline matching reference UI.
 * Auto-scrolls, shows Date divider, Starter cards in empty state, and Typing indicator.
 */
import React, { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import '../styles/ChatWindow.css';

const QUICK_STARTERS = [
  {
    icon: '🎓',
    title: 'Admissions 2026',
    desc: 'Eligibility, JEE cutoff, direct entry & counseling',
    query: 'What is the admission process for B.Tech at ABES?',
  },
  {
    icon: '💰',
    title: 'Fee Structure',
    desc: 'Tuition fees, payment modes & installment plans',
    query: 'What is the tuition fee structure for B.Tech?',
  },
  {
    icon: '💼',
    title: 'Placements & CTC',
    desc: 'Highest package 42 LPA, average package & top MNCs',
    query: 'What is the average and highest placement package at ABES?',
  },
  {
    icon: '🏠',
    title: 'Hostel & Facilities',
    desc: 'AC/Non-AC rooms, mess menu & campus rules',
    query: 'What are the hostel facilities and fee structure?',
  },
];

export default function ChatWindow({
  messages,
  isLoading,
  error,
  onStarterClick,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-window-container" role="log" aria-live="polite">
      {/* Date Divider as seen in reference UI */}
      <div className="chat-date-divider">
        <span>Today · Student Support Desk</span>
      </div>

      {/* Empty State with ABES Branding & Starter Cards */}
      {messages.length === 0 && !isLoading ? (
        <div className="empty-helpdesk-state">
          <div className="empty-badge">🏛️ ABES ENGINEERING COLLEGE</div>
          <h2 className="empty-title">Welcome to ABES Student Support Help Desk</h2>
          <p className="empty-subtitle">
            Ask any question regarding admissions, examinations, fees, hostels,
            placements, or syllabus. You can also click the <strong>🎙️ Voice Button</strong> to speak your question!
          </p>

          <div className="starters-grid">
            {QUICK_STARTERS.map((s) => (
              <button
                key={s.title}
                className="starter-card"
                onClick={() => onStarterClick && onStarterClick(s.query)}
              >
                <div className="starter-icon">{s.icon}</div>
                <div className="starter-content">
                  <div className="starter-title">{s.title}</div>
                  <div className="starter-desc">{s.desc}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="messages-stream">
          {messages.map((msg) => (
            <MessageBubble key={msg.id} message={msg} />
          ))}

          {/* Quick starter cards at the beginning of the conversation */}
          {messages.length <= 1 && !isLoading && (
            <div className="starters-container-inline">
              <div className="starters-label">⚡ Quick Topics:</div>
              <div className="starters-grid">
                {QUICK_STARTERS.map((s) => (
                  <button
                    key={s.title}
                    className="starter-card"
                    onClick={() => onStarterClick && onStarterClick(s.query)}
                  >
                    <div className="starter-icon">{s.icon}</div>
                    <div className="starter-content">
                      <div className="starter-title">{s.title}</div>
                      <div className="starter-desc">{s.desc}</div>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Typing Indicator */}
      {isLoading && <TypingIndicator />}

      {/* Error Banner */}
      {error && (
        <div className="chat-error-toast" role="alert">
          ⚠️ {error}
        </div>
      )}

      {/* Anchor for auto-scroll */}
      <div ref={bottomRef} />
    </div>
  );
}
