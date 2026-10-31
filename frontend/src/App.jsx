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

export default function App() {
  const { messages, isLoading, error, submit, clearChat } = useChat();
  const { categories } = useCategories();

  const [leftSidebarOpen, setLeftSidebarOpen] = useState(false);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [isOnline, setIsOnline] = useState(null);
  const [geminiActive, setGeminiActive] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState('en'); // 'en' or 'hi'
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
      submit(`Tell me about ${cat} at ABES Engineering College`);
      setLeftSidebarOpen(false);
      setRightSidebarOpen(false);
    },
    [submit]
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
