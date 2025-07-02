from pathlib import Path

from langchain.embeddings import HuggingFaceEmbeddings

model_dir = Path(__file__).parents[2] / "llm_models" / "embedding"


embedder = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True, "batch_size": 16},
    cache_folder=str(model_dir),
    multi_process=False,
)


def get_embedder():
    return embedder
