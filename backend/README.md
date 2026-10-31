# University Chatbot – Backend

## Setup & Run

### 1. Create a virtual environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Copy `.env.example` to `.env` and adjust if needed.

### 4. Start the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Send a message, get AI reply |
| GET | /api/faqs | List all FAQs (optional ?category=) |
| GET | /api/categories | List all categories |
| GET | /api/history | Recent chat history |
| GET | /api/health | Health check |
