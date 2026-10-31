"""
schemas.py – Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ─── Chat ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    intent: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None


# ─── FAQ ─────────────────────────────────────────────────────────────────────

class FAQSchema(BaseModel):
    id: int
    category: str
    intent: str
    questions: List[str]
    answer: str
    answer_en: Optional[str] = None
    answer_hi: Optional[str] = None

    model_config = {"from_attributes": True}


class FAQListResponse(BaseModel):
    faqs: List[FAQSchema]
    total: int


# ─── Categories ──────────────────────────────────────────────────────────────

class CategoriesResponse(BaseModel):
    categories: List[str]


# ─── History ─────────────────────────────────────────────────────────────────

class HistoryItem(BaseModel):
    id: int
    user_message: str
    bot_reply: str
    intent: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: datetime

    model_config = {"from_attributes": True}


class HistoryResponse(BaseModel):
    history: List[HistoryItem]
    total: int


# ─── Health ──────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    message: str
    faq_count: int
    version: str
    gemini_active: bool = False
