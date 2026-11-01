"""
nlp.py – TF-IDF vectorizer + cosine similarity intent matcher.

Design
------
• On startup (or first use) all FAQ questions are loaded from the DB,
  flattened into a list, and vectorised with TF-IDF.
• Each incoming user query is preprocessed (lowercase, strip punctuation,
  remove English stop-words) and then compared to the corpus via cosine
  similarity.
• The FAQ whose best-matching question scores >= threshold is returned;
  otherwise a graceful fallback is produced.
"""
import re
import logging
from typing import Optional
from datetime import datetime, timezone, timedelta

# IST Timezone (Asia/Kolkata: UTC+5:30)
_IST = timezone(timedelta(hours=5, minutes=30))

def get_time_greeting() -> str:
    """Get greeting according to Indian time (Asia/Kolkata)."""
    try:
        from zoneinfo import ZoneInfo
        current_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    except Exception:
        current_time = datetime.now(_IST)

    hour = current_time.hour

    if 5 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 17:
        return "Good Afternoon!"
    elif 17 <= hour < 21:
        return "Good Evening!"
    else:
        return "Good Night!"


def detect_greeting(message: str) -> Optional[str]:
    """
    Detect user's greeting case-insensitively with any punctuation/emoji.
    Exact responses matching the specified greeting catalog:
    - Hi / Hello / Hii -> Hi! How can I help you today?
    - Hey / Heyy -> Hey! How can I assist you?
    - Namaste / Namaskar -> Namaste! Aap academics, attendance, fees, exams ya kisi bhi college-related query mein help le sakte hain. Main aapki kya sahayata kar sakta hoon?
    - नमस्ते / प्रणाम -> नमस्ते! आप पढ़ाई, अटेंडेंस, फीस, परीक्षा, हॉस्टल या कॉलेज से जुड़े किसी भी सवाल में मदद ले सकते हैं। मैं आपकी क्या सहायता कर सकता हूँ?
    - Good morning -> Good Morning! How can I help you?
    - Good afternoon -> Good Afternoon! How can I assist you?
    - Good evening -> Good Evening! How can I help you?
    - Good night -> Good Night! Take care!
    """
    clean_msg = message.lower().strip()
    # Strip non-alphanumeric and non-Devanagari characters (punctuation, emojis, etc.)
    clean_text = re.sub(r"[^\w\s\u0900-\u097f]", " ", clean_msg)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()

    greetings_map = {
        # Hi / Hello / Hii
        "hi": "Hi! How can I help you today?",
        "hii": "Hi! How can I help you today?",
        "hiii": "Hi! How can I help you today?",
        "hello": "Hi! How can I help you today?",
        "helloo": "Hi! How can I help you today?",
        "hlo": "Hi! How can I help you today?",
        "hlw": "Hi! How can I help you today?",

        # Hey / Heyy
        "hey": "Hey! How can I assist you?",
        "heyy": "Hey! How can I assist you?",
        "heyyy": "Hey! How can I assist you?",

        # Namaste / Namaskar
        "namaste": "Namaste! Aap academics, attendance, fees, exams ya kisi bhi college-related query mein help le sakte hain. Main aapki kya sahayata kar sakta hoon?",
        "namaskar": "Namaste! Aap academics, attendance, fees, exams ya kisi bhi college-related query mein help le sakte hain. Main aapki kya sahayata kar sakta hoon?",
        "namastey": "Namaste! Aap academics, attendance, fees, exams ya kisi bhi college-related query mein help le sakte hain. Main aapki kya sahayata kar sakta hoon?",
        "pranam": "Namaste! Aap academics, attendance, fees, exams ya kisi bhi college-related query mein help le sakte hain. Main aapki kya sahayata kar sakta hoon?",

        # नमस्ते / प्रणाम
        "नमस्ते": "नमस्ते! आप पढ़ाई, अटेंडेंस, फीस, परीक्षा, हॉस्टल या कॉलेज से जुड़े किसी भी सवाल में मदद ले सकते हैं। मैं आपकी क्या सहायता कर सकता हूँ?",
        "नमस्कार": "नमस्ते! आप पढ़ाई, अटेंडेंस, फीस, परीक्षा, हॉस्टल या कॉलेज से जुड़े किसी भी सवाल में मदद ले सकते हैं। मैं आपकी क्या सहायता कर सकता हूँ?",
        "प्रणाम": "नमस्ते! आप पढ़ाई, अटेंडेंस, फीस, परीक्षा, हॉस्टल या कॉलेज से जुड़े किसी भी सवाल में मदद ले सकते हैं। मैं आपकी क्या सहायता कर सकता हूँ?",

        # Good morning
        "good morning": "Good Morning! How can I help you?",
        "goodmorning": "Good Morning! How can I help you?",
        "gm": "Good Morning! How can I help you?",
        "सुप्रभात": "Good Morning! How can I help you?",

        # Good afternoon
        "good afternoon": "Good Afternoon! How can I assist you?",
        "goodafternoon": "Good Afternoon! How can I assist you?",
        "ga": "Good Afternoon! How can I assist you?",
        "शुभ दोपहर": "Good Afternoon! How can I assist you?",

        # Good evening
        "good evening": "Good Evening! How can I help you?",
        "goodevening": "Good Evening! How can I help you?",
        "ge": "Good Evening! How can I help you?",
        "शुभ संध्या": "Good Evening! How can I help you?",

        # Good night
        "good night": "Good Night! Take care!",
        "goodnight": "Good Night! Take care!",
        "gn": "Good Night! Take care!",
        "शुभ रात्रि": "Good Night! Take care!",
    }

    # 1. Exact match on cleaned text
    if clean_text in greetings_map:
        return greetings_map[clean_text]

    # 2. Check multi-word phrase greetings first
    for g_phrase in ["good morning", "good afternoon", "good evening", "good night", "शुभ दोपहर", "शुभ संध्या", "शुभ रात्रि"]:
        if g_phrase in clean_text:
            return greetings_map[g_phrase]

    # 3. Check individual words
    words = clean_text.split()
    for w in words:
        if w in greetings_map:
            return greetings_map[w]

    return None

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.models import FAQ
from app.config import SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)

# ── NLTK stop-words (downloaded lazily) ──────────────────────────────────────
try:
    from nltk.corpus import stopwords
    import nltk

    try:
        _STOP_WORDS = set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        _STOP_WORDS = set(stopwords.words("english"))
except Exception:  # pragma: no cover
    logger.warning("NLTK stopwords unavailable; proceeding without them.")
    _STOP_WORDS = set()

# ── Conversational fillers and carrier words ────────────────────────────────
CARRIER_WORDS = {
    "abes", "engineering", "college", "university", "institute", "institution",
    "tell", "know", "want", "need", "give", "show", "provide", "please", "plz",
    "info", "information", "detail", "details", "regarding", "related", "sir", "madam",
    "kya", "hai", "hain", "batao", "bataiye", "chahiye", "kare", "karein", "hoga", "hogi", "karte",
    "बताओ", "बताइए", "दीजिए", "चाहिए", "बारे", "कॉलेज", "यूनिवर्सिटी", "प्लीज", "सर", "मैडम", "जानकारी", "कृपया"
}

# ── Module-level state (populated on first call or explicit init) ─────────────
_vectorizer: Optional[TfidfVectorizer] = None
_tfidf_matrix = None          # sparse matrix – shape (n_questions, n_features)
_faq_index: list[dict] = []   # parallel list: each entry maps to a row in matrix


# ─────────────────────────────────────────────────────────────────────────────
# Text pre-processing
# ─────────────────────────────────────────────────────────────────────────────

def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) characters."""
    return any("\u0900" <= ch <= "\u097F" for ch in text)


def preprocess(text: str) -> str:
    """
    Lowercase, remove punctuation, collapse whitespace, remove stop-words and
    carrier filler words while fully preserving Devanagari (Hindi) script & matras.
    """
    text = text.lower()
    # Normalize common Hindi variant characters (chandrabindu -> anusvara, chandra-O -> O matra, strip nukta)
    text = text.replace("\u0901", "\u0902")
    text = text.replace("\u0949", "\u094b")
    text = text.replace("\u093c", "")
    # Preserve alphanumeric and full Devanagari range \u0900-\u097F (consonants + matras)
    text = re.sub(r"[^\w\s\u0900-\u097f]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = [w for w in text.split() if len(w) > 0]
    tokens = [w for w in words if w not in _STOP_WORDS and w not in CARRIER_WORDS and len(w) > 1]
    # If all tokens were filtered out (e.g. "who are you", "hi"), relax carrier words
    if not tokens:
        tokens = [w for w in words if w not in _STOP_WORDS and len(w) > 1]
    if not tokens:
        tokens = [w for w in words if len(w) > 0]
    return " ".join(tokens)


# ─────────────────────────────────────────────────────────────────────────────
# Vectoriser initialisation
# ─────────────────────────────────────────────────────────────────────────────

def build_vectorizer(db: Session) -> None:
    """
    Load every FAQ + its questions from the DB, pre-process them,
    and fit the TF-IDF vectorizer.  Call once at startup.
    """
    global _vectorizer, _tfidf_matrix, _faq_index

    faqs = db.query(FAQ).all()
    if not faqs:
        logger.warning("No FAQs in DB – vectorizer not built.")
        return

    corpus: list[str] = []   # processed question strings
    index: list[dict] = []   # metadata for each question

    for faq in faqs:
        questions = faq.questions if isinstance(faq.questions, list) else []
        cat_clean = faq.category.replace("_", " ")
        intent_clean = faq.intent.replace("_", " ")

        for q in questions:
            corpus.append(preprocess(q))
            index.append(
                {
                    "faq_id": faq.id,
                    "category": faq.category,
                    "intent": faq.intent,
                    "answer": faq.answer,
                    "answer_en": faq.answer_en or faq.answer,
                    "answer_hi": faq.answer_hi or faq.answer,
                    "orig_question": q,
                }
            )

        # Also register category + intent representation for direct subject queries
        corpus.append(preprocess(f"{cat_clean} {intent_clean}"))
        index.append(
            {
                "faq_id": faq.id,
                "category": faq.category,
                "intent": faq.intent,
                "answer": faq.answer,
                "answer_en": faq.answer_en or faq.answer,
                "answer_hi": faq.answer_hi or faq.answer,
                "orig_question": f"Topic: {cat_clean} - {intent_clean}",
            }
        )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
        token_pattern=r"(?u)\b[\w\u0900-\u097f]{2,}\b",
    )
    matrix = vectorizer.fit_transform(corpus)

    _vectorizer = vectorizer
    _tfidf_matrix = matrix
    _faq_index = index

    logger.info(
        "TF-IDF vectorizer built: %d questions from %d FAQs.",
        len(corpus),
        len(faqs),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Intent matching
# ─────────────────────────────────────────────────────────────────────────────

def match_intent(user_query: str, db: Session) -> dict:
    """
    Match *user_query* against greeting rules and FAQ corpus.

    Returns a dict:
        reply      – answer string (in Hindi if query is Hindi, else English)
        intent     – matched intent name (or None)
        category   – matched category (or None)
        confidence – cosine similarity score (or None)
    """
    # 1. Direct greeting check
    greeting_reply = detect_greeting(user_query)
    if greeting_reply:
        logger.info("Direct greeting matched for query: '%s'", user_query)
        return {
            "reply": greeting_reply,
            "intent": "greeting",
            "category": "small_talk",
            "confidence": 1.0,
        }

    # Lazy init: build vectorizer if not yet done
    if _vectorizer is None:
        build_vectorizer(db)

    hindi_query = is_devanagari(user_query)

    if _vectorizer is None or _tfidf_matrix is None:
        return _fallback(db, hindi=hindi_query)

    processed_query = preprocess(user_query)
    if not processed_query.strip():
        return _fallback(db, hindi=hindi_query)

    query_vec = _vectorizer.transform([processed_query])
    scores = cosine_similarity(query_vec, _tfidf_matrix).flatten()

    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])

    if best_score >= SIMILARITY_THRESHOLD:
        meta = _faq_index[best_idx]
        logger.debug(
            "Match found: intent=%s, score=%.3f", meta["intent"], best_score
        )
        # Select appropriate language
        if hindi_query and meta.get("answer_hi"):
            selected_answer = meta["answer_hi"]
        elif not hindi_query and meta.get("answer_en"):
            selected_answer = meta["answer_en"]
        else:
            selected_answer = meta.get("answer_en") or meta["answer"]

        return {
            "reply": selected_answer,
            "intent": meta["intent"],
            "category": meta["category"],
            "confidence": round(best_score, 4),
        }

    logger.debug("No match above threshold %.2f (best=%.3f)", SIMILARITY_THRESHOLD, best_score)
    return _fallback(db, hindi=hindi_query)


# ─────────────────────────────────────────────────────────────────────────────
# Fallback response
# ─────────────────────────────────────────────────────────────────────────────

def _fallback(db: Session, hindi: bool = False) -> dict:
    """Return a helpful fallback when no intent is matched."""
    from sqlalchemy import distinct
    categories = [
        row[0]
        for row in db.query(distinct(FAQ.category)).order_by(FAQ.category).all()
    ]

    if categories:
        cat_list = ", ".join(c.replace("_", " ").title() for c in categories)
        if hindi:
            reply = (
                "नमस्ते! मुझे ABES हेल्प डेस्क नॉलेज बेस में इस सवाल का सटीक उत्तर नहीं मिला। "
                "आप मुझसे निम्नलिखित विषयों पर पूछ सकते हैं:\n\n"
                f"📚 {cat_list}\n\n"
                "सुझाव: आप अपना सवाल दोबारा लिख सकते हैं, अंग्रेज़ी/हिंदी में पूछ सकते हैं, या 🎙️ वॉयस सर्च का उपयोग कर सकते हैं।\n"
                "सहायता के लिए ABES हेल्प डेस्क से helpdesk@abes.ac.in या 0120-7135112 पर संपर्क करें।"
            )
        else:
            reply = (
                "I'm sorry, I couldn't find a specific match in the ABES Help Desk knowledge base. "
                "You can ask me about the following topics:\n\n"
                f"📚 {cat_list}\n\n"
                "Tip: You can rephrase, type in Hindi/English, or use the 🎙️ Voice Search button. "
                "For urgent queries, reach the ABES Help Desk at helpdesk@abes.ac.in or 0120-7135112."
            )
    else:
        if hindi:
            reply = (
                "मुझे आपका सवाल समझ नहीं आया। "
                "कृपया ABES स्टूडेंट हेल्प डेस्क से helpdesk@abes.ac.in पर संपर्क करें।"
            )
        else:
            reply = (
                "I'm sorry, I couldn't understand your question. "
                "Please contact the ABES Student Help Desk at helpdesk@abes.ac.in."
            )

    return {
        "reply": reply,
        "intent": None,
        "category": None,
        "confidence": None,
    }
