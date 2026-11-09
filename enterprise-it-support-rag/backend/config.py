from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    APP_NAME: str = "Enterprise IT Support RAG Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_TIMEOUT: int = 120
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_PERSIST_DIRECTORY: str = "data/vector_db"
    CHROMA_COLLECTION: str = "it_support_knowledge"
    DOCUMENT_DIRECTORY: str = "data/documents"
    UPLOAD_DIRECTORY: str = "data/uploads"
    FEEDBACK_FILE: str = "data/feedback/feedback.jsonl"
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 120
    TOP_K: int = 5
    VECTOR_CANDIDATES: int = 12
    BM25_CANDIDATES: int = 12
    RRF_K: int = 60
    MAX_UPLOAD_MB: int = 15
    CORS_ORIGINS: str = "http://localhost:8501,http://127.0.0.1:8501"
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", env_file_encoding="utf-8", extra="ignore")
    def path(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else ROOT_DIR / p
    @property
    def cors_origin_list(self):
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
