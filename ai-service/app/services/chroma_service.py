import chromadb
from google import genai

from app.config.settings import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

# -------------------------
# Gemini Client
# -------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

# -------------------------
# ChromaDB Client
# -------------------------

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)

# -------------------------
# Generate Embedding
# -------------------------

def get_embedding(text: str):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


# -------------------------
# Store Chunks
# -------------------------

def store_chunks(document_id: str, chunks: list):

    print("\n========== STORING DOCUMENT ==========")

    try:
        collection.delete(where={"document_id": document_id})
    except Exception:
        pass

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

    print("Document ID :", document_id)
    print("Chunks Stored :", len(chunks))
    print("Collection Count :", collection.count())
    print("=====================================\n")


# -------------------------
# Search Chunks
# -------------------------

def search_chunks(document_id: str, question: str, top_k: int = 5):

    print("\n========== SEARCH ==========")
    print("Question :", question)
    print("Document ID :", document_id)

    query_embedding = get_embedding(question)

    print("Query Embedding Length :", len(query_embedding))

    print("\nSearching WITHOUT metadata filter...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print("\nRaw Chroma Result")
    print(results)

    documents = results.get("documents", [])

    if not documents:
        print("No documents found.")
        return []

    if len(documents[0]) == 0:
        print("No matching chunks.")
        return []

    print("\nRetrieved Chunks :", len(documents[0]))

    return documents[0]


# -------------------------
# Delete Document
# -------------------------

def delete_document(document_id):

    collection.delete(
        where={
            "document_id": document_id
        }
    )


# -------------------------
# List Documents
# -------------------------

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


# -------------------------
# Collection Count
# -------------------------

def get_collection_count():

    return collection.count()