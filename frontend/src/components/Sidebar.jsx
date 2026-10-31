/**
 * Sidebar.jsx – Left Navigation Sidebar (ABES Student Help Desk)
 * Matches the reference dark sidebar layout.
 */
import React from 'react';
import '../styles/App.css';

export default function Sidebar({
  isOpen,
  onClose,
  darkMode,
  onToggleDarkMode,
  language,
  onToggleLanguage,
}) {
  return (
    <>
      {/* Mobile overlay backdrop */}
      <div
        className={`sidebar-overlay ${isOpen ? 'open' : ''}`}
        onClick={onClose}
        aria-hidden="true"
      />

      <aside className={`nav-sidebar ${isOpen ? 'open' : ''}`} aria-label="Navigation">
        {/* Profile Card */}
        <div className="nav-profile">
          <div className="nav-profile__avatar-wrap">
            <div className="nav-profile__avatar">
              🎓
            </div>
            <span className="nav-profile__badge" title="Verified College Help Desk">✓</span>
          </div>

          <div className="nav-profile__name">ABES Engineering College</div>
          <div className="nav-profile__role">Student Support Help Desk</div>

          <div className="nav-profile__meta">
            <div className="meta-item">
              <span className="meta-icon">📞</span>
              <div className="meta-info">
                <span className="meta-val">+91 120 7135112</span>
                <span className="meta-lbl">Toll-Free Help Desk</span>
              </div>
            </div>

            <div className="meta-item">
              <span className="meta-icon">✉️</span>
              <div className="meta-info">
                <span className="meta-val">helpdesk@abes.ac.in</span>
                <span className="meta-lbl">Official Support</span>
              </div>
            </div>

            <div className="meta-item">
              <span className="meta-icon">🏛️</span>
              <div className="meta-info">
                <span className="meta-val">AKTU Code: 032</span>
                <span className="meta-lbl">Affiliated with AKTU</span>
              </div>
            </div>
          </div>
        </div>

        {/* Menu Navigation */}
        <div className="nav-menu">
          <a
            href="https://www.abes.ac.in"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-menu__item"
          >
            <span className="menu-icon">🌐</span>
            <span>ABES Official Website</span>
          </a>

          <a
            href="https://erp.abes.ac.in"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-menu__item"
          >
            <span className="menu-icon">💻</span>
            <span>Student ERP Portal</span>
          </a>

          <a
            href="https://aktu.ac.in"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-menu__item"
          >
            <span className="menu-icon">📜</span>
            <span>AKTU Exam Circulars</span>
          </a>

          {/* Language Switch */}
          <button
            className="nav-menu__item nav-menu__action"
            onClick={onToggleLanguage}
            title="Toggle Language"
          >
            <span className="menu-icon">🗣️</span>
            <span>Language: <strong>{language === 'hi' ? 'हिंदी (Hindi)' : 'English'}</strong></span>
          </button>

          {/* Dark Mode Switch */}
          <div className="nav-menu__item nav-menu__toggle">
            <div className="toggle-label">
              <span className="menu-icon">{darkMode ? '🌙' : '☀️'}</span>
              <span>Dark Mode</span>
            </div>
            <label className="switch">
              <input
                type="checkbox"
                checked={darkMode}
                onChange={onToggleDarkMode}
                aria-label="Toggle Dark Mode"
              />
              <span className="slider round"></span>
            </label>
          </div>
        </div>

        {/* Bottom Banner Card */}
        <div className="nav-bottom-card">
          <div className="bottom-card__tag">ABES ACADEMICS</div>
          <div className="bottom-card__title">24x7 Student Help Desk</div>
          <div className="bottom-card__desc">
            Instant answers for admissions, fees, exams, hostel, scholarships & placements.
          </div>
          <a
            href="https://www.abes.ac.in/admissions"
            target="_blank"
            rel="noopener noreferrer"
            className="bottom-card__btn"
          >
            Apply for Admission →
          </a>
        </div>
      </aside>
    </>
  );
}
