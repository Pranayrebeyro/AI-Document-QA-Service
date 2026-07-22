from google import genai

from app.config.settings import (
    GEMINI_API_KEY,
    LLM_MODEL,
)

# -------------------------
# Gemini Client
# -------------------------

client = genai.Client(api_key=GEMINI_API_KEY)


# -------------------------
# Generate Answer
# -------------------------

def generate_answer(context: str, question: str):

    prompt = f"""
You are an AI Document Question Answering Assistant.

Your job is to answer ONLY using the provided document context.

Rules:
1. Do NOT use your own knowledge.
2. If the answer is present in the context, answer clearly.
3. If the answer is not found, reply exactly:
"I couldn't find that information in the uploaded document."

==========================
DOCUMENT CONTEXT
==========================

{context}

==========================
QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
    )

    if hasattr(response, "text") and response.text:
        return response.text.strip()

    return "I couldn't find that information in the uploaded document."