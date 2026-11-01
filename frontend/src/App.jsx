/**
 * App.jsx – Root Component for ABES Student Support Help Desk.
 * Manages 3-column layout matching the modern reference chat interface.
 */
import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from './components/Sidebar';
import RightSidebar from './components/RightSidebar';
import Header from './components/Header';
import ChatWindow from './components/ChatWindow';
import ChatInput from './components/ChatInput';
import { useChat } from './hooks/useChat';
import { useCategories } from './hooks/useCategories';
import { fetchHealth } from './services/api';

import './styles/global.css';
import './styles/App.css';

const CATEGORY_DEFAULT_QUERIES = {
  admissions: {
    en: 'What is the admission process and eligibility criteria?',
    hi: 'एडमिशन प्रक्रिया और पात्रता क्या है?',
  },
  fees: {
    en: 'What is the fee structure and how can I pay the fees?',
    hi: 'कॉलेज फीस स्ट्रक्चर क्या है और फीस कैसे जमा करें?',
  },
  scholarships: {
    en: 'What scholarships are available and how to apply?',
    hi: 'कौन-कौन सी स्कॉलरशिप उपलब्ध हैं और आवेदन कैसे करें?',
  },
  exams: {
    en: 'When are the exams and what is the schedule?',
    hi: 'परीक्षाएं कब हैं और टाइमटेबल क्या है?',
  },
  timetable: {
    en: 'Where can I find my class timetable?',
    hi: 'क्लास का टाइमटेबल कहाँ मिलेगा?',
  },
  hostel: {
    en: 'What are the hostel facilities, availability, and fees?',
    hi: 'हॉस्टल की सुविधा, उपलब्धता और फीस क्या है?',
  },
  placements: {
    en: 'Tell me about college placements and average package',
    hi: 'कॉलेज प्लेसमेंट और औसत पैकेज के बारे में बताइए',
  },
  library: {
    en: 'What are the library timings and book borrowing rules?',
    hi: 'लाइब्रेरी का समय और किताबें जारी करवाने के नियम क्या हैं?',
  },
  campus: {
    en: 'What facilities are available on campus?',
    hi: 'कैंपस में कौन-कौन सी सुविधाएं उपलब्ध हैं?',
  },
  documents: {
    en: 'How to get a bonafide certificate, transcript, or ID card?',
    hi: 'बोनाफाइड सर्टिफिकेट या मार्कशीट कैसे प्राप्त करें?',
  },
  contact: {
    en: 'What is the helpline number and email ID of the college?',
    hi: 'कॉलेज का हेल्पलाइन नंबर और ईमेल आईडी क्या है?',
  },
  attendance: {
    en: 'What is the minimum attendance requirement?',
    hi: 'कॉलेज में कितने प्रतिशत अटेंडेंस अनिवार्य है?',
  },
  academics: {
    en: 'Where can I get the syllabus and academic calendar?',
    hi: 'सिलेबस और एकेडमिक कैलेंडर कहाँ मिलेगा?',
  },
};

export default function App() {
  const [language, setLanguage] = useState('en'); // 'en' or 'hi'
  const { messages, isLoading, error, submit, clearChat } = useChat(language);
  const { categories } = useCategories();

  const [leftSidebarOpen, setLeftSidebarOpen] = useState(false);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [isOnline, setIsOnline] = useState(null);
  const [geminiActive, setGeminiActive] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [activeCategory, setActiveCategory] = useState(null);

  // Apply dark mode to <body>
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
  }, [darkMode]);

  // Poll backend health
  useEffect(() => {
    let cancelled = false;
    const checkHealth = async () => {
      try {
        const data = await fetchHealth();
        if (!cancelled) {
          setIsOnline(true);
          setGeminiActive(Boolean(data?.gemini_active));
        }
      } catch {
        if (!cancelled) {
          setIsOnline(false);
          setGeminiActive(false);
        }
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30_000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const handleCategoryClick = useCallback(
    (cat) => {
      setActiveCategory(cat);
      const categoryConfig = CATEGORY_DEFAULT_QUERIES[cat];
      const query = categoryConfig ? (categoryConfig[language] || categoryConfig.en) : `What are the details regarding ${cat}?`;
      submit(query);
      setLeftSidebarOpen(false);
      setRightSidebarOpen(false);
    },
    [submit, language]
  );

  const handleStarterClick = useCallback(
    (query) => {
      submit(query);
    },
    [submit]
  );

  return (
    <div className="app-layout">
      {/* 1. Left Profile & Navigation Sidebar */}
      <Sidebar
        isOpen={leftSidebarOpen}
        onClose={() => setLeftSidebarOpen(false)}
        darkMode={darkMode}
        onToggleDarkMode={() => setDarkMode((prev) => !prev)}
        language={language}
        onToggleLanguage={() => setLanguage((prev) => (prev === 'en' ? 'hi' : 'en'))}
      />

      {/* 2. Center Chat Workspace */}
      <main className="main-chat-workspace">
        <Header
          onClear={clearChat}
          messageCount={messages.length}
          isOnline={isOnline}
          geminiActive={geminiActive}
          onCategoryClick={handleCategoryClick}
          onMenuToggle={() => setLeftSidebarOpen((prev) => !prev)}
          onRightToggle={() => setRightSidebarOpen((prev) => !prev)}
        />

        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          error={error}
          onStarterClick={handleStarterClick}
        />

        <ChatInput
          onSubmit={submit}
          isLoading={isLoading}
          categories={categories}
        />
      </main>

      {/* 3. Right Topics & Helpline Sidebar */}
      <div className={`right-sidebar-wrap ${rightSidebarOpen ? 'open' : ''}`}>
        <div
          className={`sidebar-overlay ${rightSidebarOpen ? 'open' : ''}`}
          onClick={() => setRightSidebarOpen(false)}
          aria-hidden="true"
        />
        <RightSidebar
          categories={categories}
          activeCategory={activeCategory}
          onSelectCategory={handleCategoryClick}
        />
      </div>
    </div>
  );
}
