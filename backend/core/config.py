import os


class Settings:
    # Vector DB params
    VECTORDB_HOST = os.getenv("VECTORDB_HOST", "localhost")
    VECTORDB_PORT = os.getenv("VECTORDB_PORT", "8000")
    VECTORDB_COLLECTION = os.getenv("VECTORDB_COLLECTION", "guck_lab")
    VECTORDB_TOPK = os.getenv("VECTORDB_TOPK", 5)

    # LLM api key from gwdg
    GWDG_API_KEY = os.getenv("GWDG_API_KEY")
    GWDG_ENDPOINT = os.getenv("GWDG_ENDPOINT")

    # Embedding model params
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
    POSTGRES_DB = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://rag_user:rag_pass@localhost/rag_db",
    )

    SECRET = os.getenv("SECRET_KEY", "Test123456789")


settings = Settings()
