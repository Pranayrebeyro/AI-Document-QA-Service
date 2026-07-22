import chromadb
from sentence_transformers import SentenceTransformer
from app.config.settings import EMBEDDING_MODEL

# Initialize ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Create or load collection
collection = client.get_or_create_collection(
    name="documents"
)

# Load embedding model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


def store_chunks(document_id: str, chunks: list):
    """
    Generate embeddings for chunks and store them in ChromaDB.
    """

    embeddings = embedding_model.encode(chunks).tolist()

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


def search_chunks(document_id, question, top_k=3):

    query_embedding = embedding_model.encode(question).tolist()

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


def delete_document(document_id: str):
    """
    Delete all chunks of a document.
    """

    collection.delete(
        where={
            "document_id": document_id
        }
    )


def list_documents():
    """
    List all stored document IDs.
    """

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


def get_collection_count():
    """
    Return total number of chunks stored.
    """

    return collection.count()