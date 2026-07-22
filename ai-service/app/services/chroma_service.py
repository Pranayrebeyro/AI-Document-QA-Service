import chromadb
from google import genai
from app.config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="documents"
)


def get_embedding(text: str):
    response = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
    )

    return response.embeddings[0].values


def store_chunks(document_id: str, chunks: list):

    embeddings = [
        get_embedding(chunk)
        for chunk in chunks
    ]

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

    if not results["documents"]:
        return []

    return results["documents"][0]


def delete_document(document_id):

    collection.delete(
        where={
            "document_id": document_id
        }
    )


def list_documents():

    data = collection.get()

    if "metadatas" not in data:
        return []

    return list(
        set(
            metadata["document_id"]
            for metadata in data["metadatas"]
        )
    )


def get_collection_count():

    return collection.count()