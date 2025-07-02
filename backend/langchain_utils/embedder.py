from langchain.embeddings import HuggingFaceEmbeddings

embedder = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True, "batch_size": 16},
    cache_folder="llm_models/embeddings",
    multi_process=False,
)


def get_embedder():
    return embedder
