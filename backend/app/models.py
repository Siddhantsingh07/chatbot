"""
models.py – SQLAlchemy ORM models (database table definitions).
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from app.database import Base


class FAQ(Base):
    """Stores the structured FAQ dataset loaded from faqs.json."""
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)
    intent = Column(String(200), nullable=False)
    # Stored as a JSON list of question strings
    questions = Column(JSON, nullable=False)
    answer = Column(Text, nullable=False)
    answer_en = Column(Text, nullable=True)
    answer_hi = Column(Text, nullable=True)


class ChatHistory(Base):
    """Records every chat exchange for the history endpoint."""
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_message = Column(Text, nullable=False)
    bot_reply = Column(Text, nullable=False)
    intent = Column(String(200), nullable=True)
    category = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
