import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from config.settings import CHROMA_DB_DIR

# Initialize the embedding function with the local model
embedding_function = SentenceTransformerEmbeddingFunction(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Use persistent client with the embedding function
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
collection = chroma_client.get_or_create_collection(
    name="rag_chunks",
    embedding_function=embedding_function
)

def add_to_vectorstore(chunks):
    # Add documents in batch instead of one by one for better performance
    if chunks:
        ids = [str(i) for i in range(len(chunks))]
        collection.add(documents=chunks, ids=ids)

def query_vectorstore(query_text):
    # Use the text directly instead of pre-computed embeddings
    results = collection.query(query_texts=[query_text], n_results=3)
    return results["documents"][0] if results["documents"] else []