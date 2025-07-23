from functools import lru_cache
from typing import List, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..core.users import current_active_user
from ..langchain_utils.chain import get_rag_chain, openai_client
from ..langchain_utils.prompts import get_prompt

router = APIRouter(prefix="/rag")


class Message(BaseModel):
    """User message."""

    role: Literal["user", "assistant"]
    content: str


class QueryRequest(BaseModel):
    """User query request."""

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
    # 1. Separate the latest user message
    latest_user_message = request.chat_history[-1].content

    # 2.Trim the chat history (exclude the last message)
    chat_history = [m.model_dump() for m in request.chat_history[:-1]]

    # 3. Prepare the chain
    model_name = request.model
    prompt = get_prompt()
    chain = get_rag_chain(model_name, prompt)

    # 4. Call the chain
    result = chain.invoke(
        {
            "input": latest_user_message,
            "chat_history": chat_history,
        }
    )
    # 5. Process the result
    answer = result["answer"]
    docs = [doc.metadata for doc in result.get("context", [])]

    source_names = set(
        doc.get("source") or doc.get("title") or "Unknown" for doc in docs
    )

    if source_names:
        source_block = "### Source documents:\n" + "\n".join(
            f"- {name}" for name in source_names
        )
        answer += "\n\n" + source_block

    return {
        "answer": answer,
        "relevant_docs": docs,
    }
