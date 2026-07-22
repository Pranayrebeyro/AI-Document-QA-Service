from google import genai
from app.config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text