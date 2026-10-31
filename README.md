# 🎓 UniAssist – AI-Powered University Student Support Chatbot

A full-stack chatbot that answers university student queries using TF-IDF intent matching.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite, plain CSS |
| Backend | Python 3.11+ FastAPI |
| Database | SQLite via SQLAlchemy |
| NLP | scikit-learn TF-IDF + cosine similarity |

## Quick Start

### 1. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

## API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Send a message → get AI reply |
| GET | /api/faqs | List FAQs (optional ?category=) |
| GET | /api/categories | List FAQ categories |
| GET | /api/history | Recent chat history |
| GET | /api/health | Health check |

Interactive Swagger docs: http://localhost:8000/docs
