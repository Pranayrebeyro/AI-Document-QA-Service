from fastapi import APIRouter
from pydantic import BaseModel

from app.services.pdf_service import extract_text_from_pdf
from app.utils.chunker import split_text
from app.services.chroma_service import (
    store_chunks,
    search_chunks,
)
from app.services.llm_service import generate_answer

router = APIRouter()


# -------------------------
# Request Models
# -------------------------

class ProcessRequest(BaseModel):
    documentId: str
    pdfPath: str


class AskRequest(BaseModel):
    documentId: str
    question: str


# -------------------------
# Health Check
# -------------------------

@router.get("/health")
def health():
    return {
        "success": True,
        "message": "Python AI Service Running 🚀"
    }


# -------------------------
# Process PDF
# -------------------------

@router.post("/process")
def process_document(request: ProcessRequest):

    try:

        text = extract_text_from_pdf(request.pdfPath)

        chunks = split_text(text)

        store_chunks(
            document_id=request.documentId,
            chunks=chunks
        )

        return {
            "success": True,
            "message": "Document indexed successfully",
            "chunks": len(chunks)
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


# -------------------------
# Ask Question
# -------------------------

@router.post("/ask")
def ask_question(request: AskRequest):
    try:
        chunks = search_chunks(
            document_id=request.documentId,
            question=request.question
        )

        if not chunks:
            return {
                "success": False,
                "answer": "No relevant information found."
            }

        context = "\n\n".join(chunks)

        answer = generate_answer(
            context=context,
            question=request.question
        )

        return {
            "success": True,
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }