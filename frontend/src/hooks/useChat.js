/**
 * useChat.js – Custom hook that manages all chat state.
 *
 * Responsibilities:
 *  - Maintain the message list (user + bot bubbles)
 *  - Call the backend /api/chat endpoint
 *  - Track loading / error state
 *  - Expose helpers consumed by UI components
 */

import { useState, useCallback, useRef } from 'react';
import { sendMessage } from '../services/api';

/** Unique ID generator for React keys */
let _id = 0;
function uid() { return ++_id; }

function makeUserBubble(text) {
  return { id: uid(), role: 'user', text, timestamp: new Date() };
}

function makeBotBubble(text, meta = {}) {
  return {
    id: uid(),
    role: 'bot',
    text,
    intent: meta.intent ?? null,
    category: meta.category ?? null,
    confidence: meta.confidence ?? null,
    timestamp: new Date(),
  };
}

export function getIndiaTimeGreeting(language = 'en') {
  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const istDate = new Date(utc + 3600000 * 5.5);
  const hour = istDate.getHours();

  if (hour >= 5 && hour < 12) {
    return language === 'hi' ? 'Good Morning! सुप्रभात!' : 'Good Morning!';
  } else if (hour >= 12 && hour < 17) {
    return language === 'hi' ? 'Good Afternoon! शुभ दोपहर!' : 'Good Afternoon!';
  } else if (hour >= 17 && hour < 21) {
    return language === 'hi' ? 'Good Evening! शुभ संध्या!' : 'Good Evening!';
  } else {
    return language === 'hi' ? 'Good Night! शुभ रात्रि!' : 'Good Night!';
  }
}

export function makeInitialGreeting(language = 'en') {
  const greeting = getIndiaTimeGreeting(language);
  const text =
    language === 'hi'
      ? `${greeting} ABES स्टूडेंट सपोर्ट हेल्प डेस्क में आपका स्वागत है। मैं आपकी क्या सहायता कर सकता हूँ?`
      : `${greeting} Welcome to ABES Student Support Help Desk. How can I help you today?`;

  return {
    id: uid(),
    role: 'bot',
    text,
    intent: 'initial_welcome',
    category: 'small_talk',
    confidence: 1.0,
    timestamp: new Date(),
  };
}

export function useChat(language = 'en') {
  const [messages, setMessages] = useState(() => [makeInitialGreeting(language)]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const abortRef = useRef(null);

  const appendMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, msg]);
  }, []);

  const submit = useCallback(async (text) => {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    setError(null);
    appendMessage(makeUserBubble(trimmed));
    setIsLoading(true);

    try {
      const data = await sendMessage(trimmed);
      appendMessage(makeBotBubble(data.reply, data));
    } catch (err) {
      const errMsg =
        err.message?.includes('Failed to fetch')
          ? 'Cannot reach the server. Please make sure the backend is running.'
          : `Something went wrong: ${err.message}`;
      setError(errMsg);
      appendMessage(
        makeBotBubble(
          '⚠️ Sorry, I encountered an error. Please try again in a moment.',
        ),
      );
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, appendMessage]);

  const clearChat = useCallback(() => {
    setMessages([makeInitialGreeting(language)]);
    setError(null);
  }, [language]);

  return { messages, isLoading, error, submit, clearChat };
}
