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

export function useChat() {
  const [messages, setMessages] = useState([]);
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
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isLoading, error, submit, clearChat };
}
