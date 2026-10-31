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

# ── Module-level state (populated on first call or explicit init) ─────────────
_vectorizer: Optional[TfidfVectorizer] = None
_tfidf_matrix = None          # sparse matrix – shape (n_questions, n_features)
_faq_index: list[dict] = []   # parallel list: each entry maps to a row in matrix


# ─────────────────────────────────────────────────────────────────────────────
# Text pre-processing
# ─────────────────────────────────────────────────────────────────────────────

def preprocess(text: str) -> str:
    """Lowercase, remove punctuation, collapse whitespace, remove stop-words."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)   # strip punctuation
    text = re.sub(r"\s+", " ", text).strip()
    words = [w for w in text.split() if len(w) > 0]
    tokens = [w for w in words if w not in _STOP_WORDS and len(w) > 1]
    # If all tokens were filtered out (e.g. "who are you", "hi"), keep original words
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
        for q in questions:
            corpus.append(preprocess(q))
            index.append(
                {
                    "faq_id": faq.id,
                    "category": faq.category,
                    "intent": faq.intent,
                    "answer": faq.answer,
                }
            )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
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
    Match *user_query* against the FAQ corpus.

    Returns a dict:
        reply      – answer string
        intent     – matched intent name (or None)
        category   – matched category (or None)
        confidence – cosine similarity score (or None)
    """
    # Lazy init: build vectorizer if not yet done
    if _vectorizer is None:
        build_vectorizer(db)

    if _vectorizer is None or _tfidf_matrix is None:
        return _fallback(db)

    processed_query = preprocess(user_query)
    if not processed_query.strip():
        return _fallback(db)

    query_vec = _vectorizer.transform([processed_query])
    scores = cosine_similarity(query_vec, _tfidf_matrix).flatten()

    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])

    if best_score >= SIMILARITY_THRESHOLD:
        meta = _faq_index[best_idx]
        logger.debug(
            "Match found: intent=%s, score=%.3f", meta["intent"], best_score
        )
        return {
            "reply": meta["answer"],
            "intent": meta["intent"],
            "category": meta["category"],
            "confidence": round(best_score, 4),
        }

    logger.debug("No match above threshold %.2f (best=%.3f)", SIMILARITY_THRESHOLD, best_score)
    return _fallback(db)


# ─────────────────────────────────────────────────────────────────────────────
# Fallback response
# ─────────────────────────────────────────────────────────────────────────────

def _fallback(db: Session) -> dict:
    """Return a helpful fallback when no intent is matched."""
    from sqlalchemy import distinct
    categories = [
        row[0]
        for row in db.query(distinct(FAQ.category)).order_by(FAQ.category).all()
    ]

    if categories:
        cat_list = ", ".join(c.replace("_", " ").title() for c in categories)
        reply = (
            "I'm sorry, I couldn't find a specific match in the ABES Help Desk knowledge base. "
            "You can ask me about the following topics:\n\n"
            f"📚 {cat_list}\n\n"
            "Tip: You can rephrase, type in Hindi/English, or use the 🎙️ Voice Search button. "
            "For urgent queries, reach the ABES Help Desk at helpdesk@abes.ac.in or 0120-7135112."
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
