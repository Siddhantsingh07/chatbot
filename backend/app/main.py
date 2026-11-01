"""
main.py – FastAPI application entry point.
"""
import logging
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.database import engine, SessionLocal, Base
from app.models import FAQ, ChatHistory          # noqa: F401 – needed for Base.metadata
from app.seed import seed_faqs
from app.nlp import build_vectorizer
from app.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s – %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=== ABES Student Support Help Desk API – Starting up ===")

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created / verified.")

    db = SessionLocal()
    try:
        seed_faqs(db)

        # Fail early with a clear message if the FAQ table is empty
        if db.query(FAQ).count() == 0:
            raise RuntimeError(
                "No FAQs found in the database. Check that faqs.json exists, "
                "is valid JSON, and that seed_faqs() loads it correctly."
            )

        build_vectorizer(db)
    finally:
        db.close()

    logger.info("Startup complete. Ready to serve requests.")
    yield
    logger.info("=== ABES Student Support Help Desk API – Shutting down ===")


app = FastAPI(
    title="ABES Student Support Help Desk API",
    description=(
        "AI-powered Help Desk for ABES Engineering College students using "
        "TF-IDF intent matching and Google Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Browsers reject credentials combined with a wildcard origin,
# so only enable credentials when explicit origins are configured.
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials="*" not in CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the University Chatbot API",
        "docs": "/docs",
        "health": "/api/health",
    }