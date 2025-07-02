from functools import lru_cache
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..core.users import current_active_user
from ..langchain_utils.chain import get_rag_chain, openai_client

router = APIRouter(prefix="/rag")


class QueryRequest(BaseModel):
    prompt: str
    model: str


@lru_cache(maxsize=100)
@router.get("/models", response_model=List[str])
def list_models():
    models = openai_client.models.list()
    model_names = [m.id for m in models]
    return model_names


@router.post("/chat")
async def chat_api(request: QueryRequest, user=Depends(current_active_user)):
    model_name = request.model
    prompt = request.prompt
    chain = get_rag_chain(model_name)
    result = chain.invoke({"input": prompt})
    answer = result["answer"]

    docs = [doc.metadata for doc in result["context"]]
    return {"answer": answer, "relevant_docs": docs}
