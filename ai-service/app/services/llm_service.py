import google.generativeai as genai
from app.config.settings import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


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