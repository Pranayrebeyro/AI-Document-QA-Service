import chromadb
from google import genai
from google.genai import types

from app.config.settings import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# ChromaDB Client
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


def get_embedding(text: str):
    """
    Generate embedding using Gemini Embedding model.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values


def store_chunks(document_id: str, chunks: list):
    embeddings = []

    for chunk in chunks:
        embeddings.append(get_embedding(chunk))

    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": document_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_chunks(document_id: str, question: str, top_k: int = 3):
    query_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "document_id": document_id
        }
    )

    if (
        "documents" not in results
        or not results["documents"]
        or not results["documents"][0]
    ):
        return []

    return results["documents"][0]


def delete_document(document_id: str):
    collection.delete(
        where={
            "document_id": document_id
        }
    )


def list_documents():
    data = collection.get()

    if "metadatas" not in data:
        return []

    documents = set()

    for metadata in data["metadatas"]:
        documents.add(metadata["document_id"])

    return list(documents)


def get_collection_count():
    return collection.count()