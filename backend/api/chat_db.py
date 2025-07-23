from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.db import get_async_session
from ..core.models import (
    ChatHistory,
    ChatMessage,
    ChatSummary,
    MessageIn,
    NewChatRequest,
    RoleType,
    UpdateChatRequest,
)
from ..core.users import current_active_user

router = APIRouter(prefix="/chat_db")


@router.post("/new_chat")
async def new_chat(
    request: NewChatRequest,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    chat_id = uuid4()
    new_history = ChatHistory(
        id=chat_id,
        user_id=user.id,
        title=request.title,
        created_at=datetime.utcnow(),
    )
    session.add(new_history)

    for msg in request.messages:
        session.add(
            ChatMessage(
                history_id=chat_id,
                role=RoleType(msg.role),
                content=msg.content,
            )
        )

    await session.commit()
    return {"chat_id": str(chat_id), "message": "Chat saved successfully"}


@router.delete("/remove_chat/{chat_id}")
async def remove_chat(
    chat_id: UUID4,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.get(ChatHistory, chat_id)
    if result is None or result.user_id != user.id:
        raise HTTPException(
            status_code=404, detail="Chat not found or access denied"
        )

    await session.delete(result)
    await session.commit()
    return {"message": "Chat deleted successfully"}


@router.get("/fetch_chat/{chat_id}", response_model=List[MessageIn])
async def fetch_chat(
    chat_id: UUID4,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.get(ChatHistory, chat_id)
    if result is None or result.user_id != user.id:
        raise HTTPException(
            status_code=404, detail="Chat not found or access denied"
        )

    query = await session.execute(
        ChatMessage.__table__.select().where(ChatMessage.history_id == chat_id)
    )
    messages = query.fetchall()

    return [{"role": m.role.value, "content": m.content} for m in messages]


@router.patch("/update_chat/{chat_id}")
async def update_chat_history(
    chat_id: UUID4,
    update: UpdateChatRequest,
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # 1. Fetch chat history
    result = await session.execute(
        select(ChatHistory).where(
            ChatHistory.id == chat_id, ChatHistory.user_id == user.id
        )
    )
    chat = result.scalar_one_or_none()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # 2. Add new messages
    for msg in update.messages:
        session.add(
            ChatMessage(
                history_id=chat_id,
                role=msg.role,
                content=msg.content,
                timestamp=datetime.utcnow(),
            )
        )

    await session.commit()
    return {"message": "Chat updated successfully"}


@router.get("/list_chats", response_model=list[ChatSummary])
async def list_user_chats(
    user=Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    stmt = (
        select(ChatHistory)
        .where(ChatHistory.user_id == user.id)
        .order_by(ChatHistory.created_at.desc())
    )
    result = await session.execute(stmt)
    chats = result.scalars().all()
    return chats
