import os


class Settings:
    VECTORDB_PATH = os.getenv("VECTORDB_URL", "")
    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    POSTGRES_DB = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://rag_user:rag_pass@localhost/rag_db",
    )
    SECRET = os.getenv("SECRET_KEY", "Test123456789")


settings = Settings()
