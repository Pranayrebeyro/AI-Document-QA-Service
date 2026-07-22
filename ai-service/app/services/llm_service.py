import os

import google.generativeai as genai
from app.config.settings import GEMINI_API_KEY

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


def generate_answer(context, question):

    prompt = f"""
You are an AI document assistant.

Answer ONLY from the given context.

If the answer is not available in the context, reply:
"I couldn't find that information in the uploaded document."

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text