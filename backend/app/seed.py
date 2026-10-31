"""
seed.py – Loads faqs.json into the SQLite database on startup.
Only inserts records when the table is empty (idempotent).
"""
import json
import os
import logging
from sqlalchemy.orm import Session
from app.models import FAQ

logger = logging.getLogger(__name__)

# Resolve path relative to this file
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "faqs.json")


def seed_faqs(db: Session, force: bool = False) -> None:
    """Insert FAQ records from faqs.json if the table is empty or count mismatches."""
    faq_path = os.path.abspath(DATA_FILE)
    if not os.path.exists(faq_path):
        logger.error("FAQ data file not found at %s", faq_path)
        return

    with open(faq_path, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    existing_count = db.query(FAQ).count()
    if existing_count == len(faq_data) and not force:
        logger.info("FAQ table already up-to-date with %d records. Skipping.", existing_count)
        return

    # Delete existing FAQs to re-seed cleanly
    db.query(FAQ).delete()
    records = []
    for item in faq_data:
        records.append(
            FAQ(
                id=item["id"],
                category=item["category"],
                intent=item["intent"],
                questions=item["questions"],
                answer=item.get("answer", item.get("answer_en", "")),
                answer_en=item.get("answer_en"),
                answer_hi=item.get("answer_hi"),
            )
        )

    db.bulk_save_objects(records)
    db.commit()
    logger.info("Seeded %d FAQ records for ABES Help Desk.", len(records))
