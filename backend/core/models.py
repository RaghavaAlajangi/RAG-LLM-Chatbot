import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Literal

from pydantic import BaseModel
from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class RoleType(PyEnum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatSummary(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageIn(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class NewChatRequest(BaseModel):
    title: str
    messages: List[MessageIn]


class MessageUpdate(BaseModel):
    role: RoleType
    content: str


class UpdateChatRequest(BaseModel):
    messages: List[MessageUpdate]


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    title: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="history", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    history_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("chat_histories.id", ondelete="CASCADE")
    )
    role: Mapped[RoleType] = mapped_column(Enum(RoleType), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    history: Mapped["ChatHistory"] = relationship(
        "ChatHistory", back_populates="messages"
    )
