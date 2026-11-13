
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):

    # Application
    APP_NAME: str = "Enterprise IT Support RAG Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = False
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_KEY: str = ""
    model_config = SettingsConfigDict(
    env_file=ROOT_DIR / ".env",
    env_file_encoding="utf-8",
    extra="ignore"
)
     # Langfuse monitoring
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_BASE_URL: str = "https://cloud.langfuse.com"

    # Ollama - Keep existing local LLM support
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_TIMEOUT: int = 120

    # Azure AI Search
    AZURE_SEARCH_ENABLED: bool = False
    AZURE_SEARCH_ENDPOINT: str = "https://secureit-rag-search.search.windows.net"
    AZURE_SEARCH_API_KEY: str = ""
    AZURE_SEARCH_ADMIN_KEY: str = ""
    AZURE_SEARCH_INDEX_NAME: str = "rag-1794563417722"

    # Azure Blob Storage
    AZURE_STORAGE_ACCOUNT_NAME: str = ""
    AZURE_STORAGE_CONTAINER_NAME: str = "security-documents"
    AZURE_STORAGE_CONNECTION_STRING: str = ""

    # Microsoft Foundry
    FOUNDRY_ENABLED: bool = False
    FOUNDRY_ENDPOINT: str = ""
    FOUNDRY_API_KEY: str = ""
    # LLM provider selection
    LLM_PROVIDER: str = "ollama"

    # Foundry model deployments
    FOUNDRY_CHAT_DEPLOYMENT: str = "gpt-5-mini"
    FOUNDRY_EMBEDDING_DEPLOYMENT: str = "text-embedding-3-small"

    # Local embedding model - Keep existing support
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "data/vector_db"
    CHROMA_COLLECTION: str = "it_support_knowledge"

    # Documents
    DOCUMENT_DIRECTORY: str = "data/documents"
    UPLOAD_DIRECTORY: str = "data/uploads"
    FEEDBACK_FILE: str = "data/feedback/feedback.jsonl"

    # RAG configuration
    CHUNK_SIZE: int = 700
    CHUNK_OVERLAP: int = 120
    TOP_K: int = 5
    VECTOR_CANDIDATES: int = 12
    BM25_CANDIDATES: int = 12
    RRF_K: int = 60

    # Upload
    MAX_UPLOAD_MB: int = 15

    # CORS
    CORS_ORIGINS: str = (
        "http://localhost:8501,"
        "http://127.0.0.1:8501"
    )

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def path(self, value: str) -> Path:
        p = Path(value)
        return p if p.is_absolute() else ROOT_DIR / p

    @property
    def cors_origin_list(self):
        return [
            x.strip()
            for x in self.CORS_ORIGINS.split(",")
            if x.strip()
        ]


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

