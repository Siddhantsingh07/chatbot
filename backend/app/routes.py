"""
routes.py – All API route handlers.
"""
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FAQ, ChatHistory
from app.nlp import match_intent
from app.schemas import (
    ChatRequest,
    ChatResponse,
    FAQListResponse,
    FAQSchema,
    CategoriesResponse,
    HistoryResponse,
    HistoryItem,
    HealthResponse,
)
from app.config import MAX_HISTORY_RECORDS
from app.gemini_service import is_gemini_available, generate_gemini_reply

router = APIRouter(prefix="/api")
logger = logging.getLogger(__name__)


# ─── POST /api/chat ──────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Accept a user message, run TF-IDF intent matching with database retrieval,
    optionally augment with Google Gemini LLM, store the exchange, and return
    the bot reply with metadata.
    """
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=422, detail="Message cannot be empty.")

    # 1. Run local FAQ intent matching (includes time-based greeting detection)
    result = match_intent(user_message, db)

    # 2. If Gemini is configured and message is not a direct greeting, generate conversational grounded response
    if is_gemini_available() and result.get("intent") != "greeting":
        try:
            categories_rows = db.query(distinct(FAQ.category)).all()
            all_categories = [r[0] for r in categories_rows]

            matched_faq = None
            if result.get("intent"):
                matched_faq = {
                    "intent": result.get("intent"),
                    "category": result.get("category"),
                    "answer": result.get("reply"),
                    "confidence": result.get("confidence"),
                }

            gemini_reply = generate_gemini_reply(
                user_query=user_message,
                matched_faq=matched_faq,
                available_categories=all_categories,
            )

            if gemini_reply:
                result["reply"] = gemini_reply
                if not result.get("intent"):
                    result["intent"] = "gemini_generative"
                    result["category"] = "general"
        except Exception as e:
            logger.warning("Error running Gemini generation: %s", e)

    # 3. Persist to chat history
    record = ChatHistory(
        user_message=user_message,
        bot_reply=result["reply"],
        intent=result.get("intent"),
        category=result.get("category"),
        confidence=result.get("confidence"),
        timestamp=datetime.now(timezone.utc),
    )
    db.add(record)
    db.commit()

    return ChatResponse(
        reply=result["reply"],
        intent=result.get("intent"),
        category=result.get("category"),
        confidence=result.get("confidence"),
    )


# ─── GET /api/faqs ───────────────────────────────────────────────────────────

@router.get("/faqs", response_model=FAQListResponse)
def list_faqs(
    category: Optional[str] = Query(None, description="Filter by category slug"),
    db: Session = Depends(get_db),
):
    """Return all FAQs, optionally filtered by category."""
    query = db.query(FAQ)
    if category:
        query = query.filter(func.lower(FAQ.category) == category.lower())

    faqs = query.order_by(FAQ.category, FAQ.id).all()
    return FAQListResponse(
        faqs=[FAQSchema.model_validate(f) for f in faqs],
        total=len(faqs),
    )


# ─── GET /api/categories ─────────────────────────────────────────────────────

@router.get("/categories", response_model=CategoriesResponse)
def list_categories(db: Session = Depends(get_db)):
    """Return a distinct, sorted list of FAQ categories."""
    rows = (
        db.query(distinct(FAQ.category))
        .order_by(FAQ.category)
        .all()
    )
    categories = [row[0] for row in rows]
    return CategoriesResponse(categories=categories)


# ─── GET /api/history ────────────────────────────────────────────────────────

@router.get("/history", response_model=HistoryResponse)
def get_history(
    limit: int = Query(MAX_HISTORY_RECORDS, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Return recent chat history, newest first."""
    records = (
        db.query(ChatHistory)
        .order_by(ChatHistory.timestamp.desc())
        .limit(limit)
        .all()
    )
    return HistoryResponse(
        history=[HistoryItem.model_validate(r) for r in records],
        total=len(records),
    )


# ─── GET /api/greeting ───────────────────────────────────────────────────────

@router.get("/greeting")
def get_greeting():
    """Return dynamic time-based greeting for initial session display."""
    from app.nlp import get_time_greeting
    time_greeting = get_time_greeting()
    return {
        "time_greeting": time_greeting,
        "welcome_en": f"{time_greeting} Welcome to ABES Student Support Help Desk. How can I help you today?",
        "welcome_hi": f"{time_greeting} ABES स्टूडेंट सपोर्ट हेल्प डेस्क में आपका स्वागत है। मैं आपकी क्या सहायता कर सकता हूँ?",
    }


# ─── GET /api/health ─────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Simple liveness / readiness check."""
    faq_count = db.query(FAQ).count()
    return HealthResponse(
        status="ok",
        message="University Chatbot API is running.",
        faq_count=faq_count,
        version="1.0.0",
        gemini_active=is_gemini_available(),
    )
