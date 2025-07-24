from sentence_transformers import SentenceTransformer

# Initialize the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_text(texts: list):
    # Generate embeddings for all texts in the list
    embeddings = model.encode(texts, convert_to_tensor=False, show_progress_bar=False)
    return embeddings.tolist()