import chromadb
from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL

# -----------------------------
# ChromaDB Client
# -----------------------------

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

# -----------------------------
# Lazy Load Embedding Model
# -----------------------------

embedding_model = None


def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        print("Loading embedding model...")
        embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    return embedding_model


# -----------------------------
# Store Chunks
# -----------------------------

def store_chunks(document_id: str, chunks: list):

    model = get_embedding_model()

    embeddings = model.encode(chunks).tolist()

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


# -----------------------------
# Search Chunks
# -----------------------------

def search_chunks(document_id: str, question: str, top_k: int = 3):

    model = get_embedding_model()

    query_embedding = model.encode(question).tolist()

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


# -----------------------------
# Delete Document
# -----------------------------

def delete_document(document_id: str):

    collection.delete(
        where={
            "document_id": document_id
        }
    )


# -----------------------------
# List Documents
# -----------------------------

def list_documents():

    data = collection.get()

    if "metadatas" not in data:
        return []

    document_ids = list(
        set(
            metadata["document_id"]
            for metadata in data["metadatas"]
        )
    )

    return document_ids


# -----------------------------
# Collection Count
# -----------------------------

def get_collection_count():

    return collection.count()