/**
 * RightSidebar.jsx – Right Panel (Topics, FAQs & Campus Helplines)
 * Matches the right column of the reference chat UI.
 */
import React, { useState, useMemo } from 'react';
import '../styles/App.css';

const CATEGORY_DETAILS = {
  admissions:   { icon: '🎓', label: 'Admissions & Cutoffs', desc: 'B.Tech, MCA, MBA eligibility, JEE/CUET' },
  fees:         { icon: '💰', label: 'Fee Structure', desc: 'Tuition fees, payment dates, installments' },
  scholarships: { icon: '🏆', label: 'Scholarships & Aid', desc: 'UP scholarship, merit waiver, EWS scheme' },
  exams:        { icon: '📝', label: 'Exams & Results', desc: 'AKTU schedule, internal tests, backlogs' },
  timetable:    { icon: '📅', label: 'Class Timetable', desc: 'Lecture slots, academic calendar 2026' },
  hostel:       { icon: '🏠', label: 'Hostel & Mess', desc: 'AC/Non-AC rooms, mess menu, curfew rules' },
  library:      { icon: '📚', label: 'Central Library', desc: 'Timings, IEEE access, book issue rules' },
  placements:   { icon: '💼', label: 'Placements & CTC', desc: 'Recruiters, packages (Highest 42 LPA)' },
  documents:    { icon: '📄', label: 'Certificates & Bonafide', desc: 'Degree, migration, transcript requests' },
  campus:       { icon: '🏫', label: 'Campus & Facilities', desc: 'Sports, canteen, dress code, tech fest' },
  contact:      { icon: '📞', label: 'Helpline & Offices', desc: 'Director, Dean, Registrar, HOD contacts' },
  small_talk:   { icon: '💬', label: 'General Help Desk', desc: 'Greetings, capabilities, guidance' },
};

const CAMPUS_HELPLINES = [
  { dept: 'Admissions Office', phone: '+91 9999889341', time: '9 AM - 5 PM' },
  { dept: 'Registrar & Exam Cell', phone: '0120-7135112', time: '9 AM - 4 PM' },
  { dept: 'Chief Hostel Warden', phone: '+91 9876543210', time: '24x7 Emergency' },
  { dept: 'Training & Placements', phone: '0120-7135115', time: '10 AM - 5 PM' },
];

export default function RightSidebar({
  categories = [],
  activeCategory,
  onSelectCategory,
  onSelectTopic,
}) {
  const [search, setSearch] = useState('');

  const filteredCategories = useMemo(() => {
    if (!search.trim()) return categories;
    const q = search.toLowerCase();
    return categories.filter((cat) => {
      const details = CATEGORY_DETAILS[cat] || { label: cat, desc: '' };
      return (
        cat.toLowerCase().includes(q) ||
        details.label.toLowerCase().includes(q) ||
        details.desc.toLowerCase().includes(q)
      );
    });
  }, [categories, search]);

  return (
    <aside className="topics-sidebar" aria-label="Quick Topics & Helplines">
      {/* Search Bar */}
      <div className="topics-search">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          placeholder="Search topics / FAQs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          aria-label="Search FAQs"
        />
        {search && (
          <button className="search-clear" onClick={() => setSearch('')}>
            ✕
          </button>
        )}
      </div>

      {/* Topics Section */}
      <div className="sidebar-section-header">
        <span>Help Desk Topics</span>
        <span className="count-pill">{filteredCategories.length}</span>
      </div>

      <div className="topics-list" role="list">
        {filteredCategories.map((cat) => {
          const info = CATEGORY_DETAILS[cat] || {
            icon: '📌',
            label: cat,
            desc: `Questions about ${cat}`,
          };
          const isActive = activeCategory === cat;

          return (
            <div
              key={cat}
              className={`topic-card ${isActive ? 'active' : ''}`}
              role="listitem"
              onClick={() => onSelectCategory(cat)}
            >
              <div className="topic-card__avatar">{info.icon}</div>
              <div className="topic-card__info">
                <div className="topic-card__title">{info.label}</div>
                <div className="topic-card__desc">{info.desc}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Emergency & Campus Helplines */}
      <div className="sidebar-section-header" style={{ marginTop: '16px' }}>
        <span>Direct Helplines</span>
      </div>

      <div className="helplines-list">
        {CAMPUS_HELPLINES.map((item) => (
          <div key={item.dept} className="helpline-card">
            <div className="helpline-icon">📞</div>
            <div className="helpline-info">
              <div className="helpline-dept">{item.dept}</div>
              <div className="helpline-num">{item.phone}</div>
            </div>
            <div className="helpline-time">{item.time}</div>
          </div>
        ))}
      </div>
    </aside>
  );
}
