import chromadb
from langchain_chroma import Chroma

from backend.core.config import settings

from .embedder import get_embedder


def get_vectorstore():
    embedder = get_embedder()

    chroma_client = chromadb.HttpClient(
        host=settings.VECTORDB_HOST, port=settings.VECTORDB_PORT
    )

    vectordb = Chroma(
        client=chroma_client,
        embedding_function=embedder,
        collection_name=settings.VECTORDB_COLLECTION,
        collection_metadata={"hnsw:space": "cosine"},
    )
    return vectordb


def get_retriever():
    vectordb = get_vectorstore()
    return vectordb.as_retriever(search_kwargs={"k": settings.VECTORDB_TOPK})
