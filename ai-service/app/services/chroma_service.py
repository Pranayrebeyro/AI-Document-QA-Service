import chromadb
from google import genai

from app.config.settings import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    CHROMA_DB_PATH,
    COLLECTION_NAME,
)

# ---------------------------------------
# Gemini Client
# ---------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------------------------------
# ChromaDB Client
# ---------------------------------------

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DB_PATH
)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)

# ---------------------------------------
# Generate Embedding
# ---------------------------------------

def get_embedding(text: str):

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    embedding = response.embeddings[0].values

    print(f"Generated embedding size : {len(embedding)}")

    return embedding


# ---------------------------------------
# Store Chunks
# ---------------------------------------

def store_chunks(document_id: str, chunks: list):

    print("\n" + "=" * 70)
    print("STORING DOCUMENT")
    print("=" * 70)

    try:
        collection.delete(
            where={
                "document_id": document_id
            }
        )
    except Exception:
        pass

    embeddings = []

    for index, chunk in enumerate(chunks):

        print(f"Embedding Chunk {index + 1}/{len(chunks)}")

        embeddings.append(
            get_embedding(chunk)
        )

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

    print("\nDOCUMENT STORED SUCCESSFULLY")
    print("Document ID :", document_id)
    print("Chunks :", len(chunks))
    print("Collection Count :", collection.count())

    print("\nStored Document IDs")

    data = collection.get()

    if data["metadatas"]:

        for meta in data["metadatas"]:
            print(meta)

    print("=" * 70 + "\n")


# ---------------------------------------
# Search Chunks
# ---------------------------------------

def search_chunks(document_id: str, question: str, top_k: int = 5):

    print("\n" + "=" * 70)
    print("SEARCHING DOCUMENT")
    print("=" * 70)

    print("Question :", question)
    print("Document ID :", document_id)

    query_embedding = get_embedding(question)

    print("\nCollection Count :", collection.count())

    print("\nTrying metadata search...\n")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={
            "document_id": document_id
        }
    )

    print("Metadata Search Result")
    print(results)

    if (
        "documents" in results
        and len(results["documents"]) > 0
        and len(results["documents"][0]) > 0
    ):

        print("Metadata search successful.")

        return results["documents"][0]

    print("\nMetadata search failed.")
    print("Trying global search...\n")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    print("Global Search Result")
    print(results)

    if (
        "documents" not in results
        or len(results["documents"]) == 0
        or len(results["documents"][0]) == 0
    ):

        print("No documents found in ChromaDB.")

        return []

    print("Global search successful.")

    return results["documents"][0]


# ---------------------------------------
# Delete Document
# ---------------------------------------

def delete_document(document_id):

    collection.delete(
        where={
            "document_id": document_id
        }
    )


# ---------------------------------------
# List Documents
# ---------------------------------------

def list_documents():

    data = collection.get()

    if "metadatas" not in data:
        return []

    documents = set()

    for metadata in data["metadatas"]:
        documents.add(
            metadata["document_id"]
        )

    return list(documents)


# ---------------------------------------
# Collection Count
# ---------------------------------------

def get_collection_count():

    return collection.count()