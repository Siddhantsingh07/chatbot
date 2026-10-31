import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'backend')
from app.database import SessionLocal, Base, engine
from app.seed import seed_faqs
from app.nlp import build_vectorizer, match_intent

Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_faqs(db, force=True)
build_vectorizer(db)

test_queries = [
    'hi',
    'hello',
    'नमस्ते',
    'admission process',
    'admission kaise le sakte hai',
    'fees kitni hai',
    'hostel rules',
    'highest placement package',
    'library timings',
    'who are you'
]

for q in test_queries:
    res = match_intent(q, db)
    intent = res.get('intent')
    cat = res.get('category')
    conf = res.get('confidence')
    print(f"Q: {q:<30} -> Intent: {intent:<25} Cat: {cat:<15} Conf: {conf}")
