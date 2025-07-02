from functools import lru_cache
from typing import List, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..core.users import current_active_user
from ..langchain_utils.chain import get_rag_chain, openai_client

router = APIRouter(prefix="/rag")


class Message(BaseModel):
    """User message."""

    role: Literal["user", "assistant"]
    content: str


class QueryRequest(BaseModel):
    """User query request."""

    prompt: str
    model: str
    chat_history: List[Message] = []


@lru_cache(maxsize=100)
@router.get("/models", response_model=List[str])
def list_models():
    """API endpoint to list available models."""
    models = openai_client.models.list()
    model_names = [m.id for m in models]
    return model_names


@router.post("/chat")
async def chat_api(request: QueryRequest, user=Depends(current_active_user)):
    """API endpoint for chat with given LLM."""
    model_name = request.model
    prompt = request.prompt
    chat_history = [m.model_dump() for m in request.chat_history]

    chain = get_rag_chain(model_name)
    result = chain.invoke({"input": prompt, "chat_history": chat_history})

    answer = result["answer"]

    docs = [doc.metadata for doc in result["context"]]
    return {"answer": answer, "relevant_docs": docs}
