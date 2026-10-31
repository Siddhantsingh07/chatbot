/**
 * Header.jsx – Top bar of the Chat UI
 * Features category story bubbles, active Help Desk contact header & action buttons.
 */
import React from 'react';
import '../styles/Header.css';

const CATEGORY_STORY_ICONS = [
  { cat: 'admissions', icon: '🎓', label: 'Admissions' },
  { cat: 'fees', icon: '💰', label: 'Fees' },
  { cat: 'scholarships', icon: '🏆', label: 'Scholarships' },
  { cat: 'exams', icon: '📝', label: 'Exams' },
  { cat: 'timetable', icon: '📅', label: 'Timetable' },
  { cat: 'hostel', icon: '🏠', label: 'Hostel' },
  { cat: 'placements', icon: '💼', label: 'Placements' },
  { cat: 'library', icon: '📚', label: 'Library' },
  { cat: 'campus', icon: '🏫', label: 'Campus' },
  { cat: 'documents', icon: '📄', label: 'Documents' },
  { cat: 'contact', icon: '📞', label: 'Contact' },
];

export default function Header({
  onClear,
  messageCount,
  isOnline,
  geminiActive,
  onCategoryClick,
  onMenuToggle,
  onRightToggle,
}) {
  return (
    <header className="chat-header">
      {/* Top Story Avatars row */}
      <div className="header__stories">
        <button
          className="header__menu-btn"
          onClick={onMenuToggle}
          aria-label="Toggle menu"
          title="Menu"
        >
          ☰
        </button>

        <div className="stories-scroll">
          {CATEGORY_STORY_ICONS.map((item) => (
            <button
              key={item.cat}
              className="story-bubble"
              onClick={() => onCategoryClick(item.cat)}
              title={`Ask about ${item.label}`}
            >
              <div className="story-circle">{item.icon}</div>
              <span className="story-label">{item.label}</span>
            </button>
          ))}
        </div>

        <button
          className="header__topics-btn"
          onClick={onRightToggle}
          aria-label="Toggle topics panel"
          title="Topics & Helplines"
        >
          📋
        </button>
      </div>

      {/* Main Contact Bar */}
      <div className="header__main-bar">
        <div className="agent-info">
          <div className="agent-avatar-wrap">
            <div className="agent-avatar">🏛️</div>
            <span className="agent-online-dot" />
          </div>

          <div className="agent-text">
            <div className="agent-title-row">
              <span className="agent-name">ABES Student Support Help Desk</span>
              {geminiActive && (
                <span className="gemini-pill" title="Enhanced with Google Gemini AI">
                  ✨ Gemini AI
                </span>
              )}
            </div>
            <div className="agent-status">
              <span className="status-indicator">●</span>
              <span>Online · Virtual Desk (AKTU Code: 032)</span>
            </div>
          </div>
        </div>

        {/* Action icons on right */}
        <div className="header__actions">
          <a
            href="tel:01207135112"
            className="action-btn"
            title="Call ABES Help Desk (0120-7135112)"
          >
            📞
          </a>

          <a
            href="https://www.abes.ac.in"
            target="_blank"
            rel="noopener noreferrer"
            className="action-btn"
            title="Visit abes.ac.in"
          >
            🌐
          </a>

          {messageCount > 0 && (
            <button
              className="action-btn clear-btn"
              onClick={onClear}
              title="Clear conversation"
            >
              🗑️
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
