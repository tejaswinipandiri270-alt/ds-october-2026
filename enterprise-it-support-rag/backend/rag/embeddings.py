from functools import lru_cache
from sentence_transformers import SentenceTransformer
from backend.config import settings

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(settings.EMBEDDING_MODEL)

def embed_texts(texts):
    if not texts:
        return []
    vectors = get_embedding_model().encode(texts, normalize_embeddings=True,
        convert_to_numpy=True, show_progress_bar=False)
    return vectors.tolist()
