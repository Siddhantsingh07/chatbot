/**
 * api.js – All backend API calls in one place.
 * The base URL is read from the VITE_API_URL env variable (falls back to
 * the Vite dev-server proxy so you never hard-code the backend host).
 */

const BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Internal helper – throws a descriptive Error on HTTP errors.
 */
async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`;
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`API ${res.status}: ${text || res.statusText}`);
  }

  return res.json();
}

// ── Chat ─────────────────────────────────────────────────────────────────────

/**
 * POST /api/chat
 * @param {string} message
 * @returns {{ reply, intent, category, confidence }}
 */
export async function sendMessage(message) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

// ── FAQs ─────────────────────────────────────────────────────────────────────

/**
 * GET /api/faqs?category=...
 * @param {string|null} category
 * @returns {{ faqs: FAQ[], total: number }}
 */
export async function fetchFAQs(category = null) {
  const qs = category ? `?category=${encodeURIComponent(category)}` : '';
  return request(`/api/faqs${qs}`);
}

// ── Categories ───────────────────────────────────────────────────────────────

/**
 * GET /api/categories
 * @returns {{ categories: string[] }}
 */
export async function fetchCategories() {
  return request('/api/categories');
}

// ── History ──────────────────────────────────────────────────────────────────

/**
 * GET /api/history?limit=...
 * @param {number} limit
 * @returns {{ history: HistoryItem[], total: number }}
 */
export async function fetchHistory(limit = 50) {
  return request(`/api/history?limit=${limit}`);
}

// ── Health ───────────────────────────────────────────────────────────────────

/**
 * GET /api/health
 * @returns {{ status, message, faq_count, version }}
 */
export async function fetchHealth() {
  return request('/api/health');
}
