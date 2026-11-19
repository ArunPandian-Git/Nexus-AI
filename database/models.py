from pathlib import Path

models_code = '''
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Integer,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


# ==========================================
# 1. USER MODEL
# ==========================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    username: Mapped[str] = mapped_column(
        String(100), unique=True, index=True
    )

    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================================
# 2. CONVERSATION MODEL
# ==========================================

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    title: Mapped[str] = mapped_column(
        String(255), default="New Conversation"
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    user = relationship(
        "User",
        back_populates="conversations"
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


# ==========================================
# 3. MESSAGE MODEL
# ==========================================

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"), index=True
    )

    role: Mapped[str] = mapped_column(
        String(50)
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages"
    )


# ==========================================
# 4. DOCUMENT MODEL
# ==========================================

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    filename: Mapped[str] = mapped_column(
        String(255)
    )

    file_path: Mapped[str] = mapped_column(
        String(1000)
    )

    file_type: Mapped[str] = mapped_column(
        String(50)
    )

    file_size: Mapped[int] = mapped_column(
        Integer, default=0
    )

    processing_status: Mapped[str] = mapped_column(
        String(50), default="uploaded"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )


# ==========================================
# 5. AGENT ACTIVITY MODEL
# ==========================================

class AgentActivity(Base):
    __tablename__ = "agent_activities"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    agent_name: Mapped[str] = mapped_column(
        String(100)
    )

    task_description: Mapped[str] = mapped_column(
        Text
    )

    status: Mapped[str] = mapped_column(
        String(50), default="pending"
    )

    execution_time: Mapped[int] = mapped_column(
        Integer, default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
'''

path = Path("/content/database/models.py")
path.write_text(models_code, encoding="utf-8")

print("SUCCESS: Enterprise database models created!")
print("File:", path)
