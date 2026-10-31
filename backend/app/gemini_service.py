"""
gemini_service.py – Google Gemini LLM integration for conversational student support.

Features:
- Grounded generation (RAG): Combines official university FAQ context with Gemini.
- Graceful degradation: If GEMINI_API_KEY is missing or the API call fails,
  the app falls back seamlessly to the local TF-IDF model.
- Supports conversational fluency, Hindi/Hinglish questions, and polite guidance.
"""
import logging
from typing import Optional, List, Dict
from app.config import GEMINI_API_KEY, GEMINI_MODEL, USE_GEMINI

logger = logging.getLogger(__name__)

_client = None

def get_gemini_client():
    """Lazily initializes and returns the Gemini GenAI client."""
    global _client
    if not USE_GEMINI or not GEMINI_API_KEY:
        return None

    if _client is None:
        try:
            from google import genai
            _client = genai.Client(api_key=GEMINI_API_KEY)
            logger.info("Gemini client initialized with model: %s", GEMINI_MODEL)
        except Exception as e:
            logger.error("Failed to initialize Google GenAI client: %s", e)
            _client = None

    return _client


def is_gemini_available() -> bool:
    """Returns True if Gemini is configured and enabled."""
    return USE_GEMINI and bool(GEMINI_API_KEY.strip())


def generate_gemini_reply(
    user_query: str,
    matched_faq: Optional[Dict] = None,
    available_categories: Optional[List[str]] = None,
) -> Optional[str]:
    """
    Generate an AI response using Google Gemini grounded with university context.

    Parameters:
    - user_query: The student's input message.
    - matched_faq: Dict containing {category, intent, answer, confidence} if TF-IDF matched.
    - available_categories: List of university categories for guidance.

    Returns:
    - AI-generated reply string, or None if Gemini is disabled / failed.
    """
    client = get_gemini_client()
    if not client:
        return None

    try:
        categories_str = ", ".join(available_categories or [])
        
        # Build grounding context
        if matched_faq and matched_faq.get("answer"):
            context_block = (
                f"OFFICIAL ABES ENGINEERING COLLEGE KNOWLEDGE BASE:\n"
                f"Topic/Category: {matched_faq.get('category', 'General')}\n"
                f"Verified Answer: {matched_faq.get('answer')}\n"
            )
        else:
            context_block = (
                f"OFFICIAL ABES ENGINEERING COLLEGE TOPICS:\n"
                f"The college handles: {categories_str}.\n"
                f"Help Desk Contact: helpdesk@abes.ac.in | info@abes.ac.in | Phone: 0120-7135112\n"
                f"Location: 19th KM Stone, NH-09, Ghaziabad, UP - 201009\n"
            )

        prompt = f"""You are the official "ABES Student Support Help Desk" assistant for ABES Engineering College, Ghaziabad (affiliated with AKTU).

{context_block}

STUDENT'S MESSAGE:
"{user_query}"

INSTRUCTIONS:
1. You represent the ABES Engineering College Student Help Desk. Always be polite, professional, and helpful.
2. If official ABES information is provided above, use it as the primary factual source for your answer.
3. If the student greets you (e.g. "hi", "hello", "namaste"), greet them warmly and let them know you are the ABES Student Support Help Desk ready to help with admissions, fees, exams, hostel, timetable, campus life, and placements.
4. If the question is in Hindi or Hinglish, reply naturally in the same language while maintaining factual accuracy.
5. Keep answers well-structured and concise. Use bullet points where appropriate.
6. If the question is completely unrelated to college matters, politely clarify your role as ABES Help Desk and suggest college topics ({categories_str}).
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        if response and response.text:
            return response.text.strip()

    except Exception as e:
        logger.warning("Gemini generation failed (falling back to TF-IDF): %s", e)

    return None
