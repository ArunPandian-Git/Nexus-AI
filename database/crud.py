%%writefile /content/database/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import select

from database.models import (
    User,
    Conversation,
    Message,
    Document,
    AgentActivity
)


# ==========================================
# USER OPERATIONS
# ==========================================

def create_user(db: Session, username, email, hashed_password):
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(db: Session, email):
    return db.scalar(
        select(User).where(User.email == email)
    )


# ==========================================
# CONVERSATION OPERATIONS
# ==========================================

def create_conversation(db: Session, user_id, title):
    conversation = Conversation(
        user_id=user_id,
        title=title
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_user_conversations(db: Session, user_id):
    return list(
        db.scalars(
            select(Conversation)
            .where(Conversation.user_id == user_id)
        ).all()
    )


# ==========================================
# MESSAGE OPERATIONS
# ==========================================

def create_message(db: Session, conversation_id, role, content):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_conversation_messages(db: Session, conversation_id):
    return list(
        db.scalars(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()
    )


# ==========================================
# DOCUMENT OPERATIONS
# ==========================================

def create_document(
    db: Session,
    filename,
    file_path,
    file_type,
    file_size,
    processing_status="uploaded"
):
    document = Document(
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        processing_status=processing_status
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_all_documents(db: Session):
    return list(db.scalars(select(Document)).all())


# ==========================================
# AGENT ACTIVITY OPERATIONS
# ==========================================

def create_agent_activity(
    db: Session,
    agent_name,
    task_description,
    status="completed",
    execution_time=0.0
):
    activity = AgentActivity(
        agent_name=agent_name,
        task_description=task_description,
        status=status,
        execution_time=execution_time
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_all_agent_activities(db: Session):
    return list(
        db.scalars(select(AgentActivity)).all()
    )


# ==========================================
# UPDATE OPERATIONS
# ==========================================

def update_document_status(db: Session, document_id, new_status):
    document = db.get(Document, document_id)

    if document is None:
        return None

    document.processing_status = new_status

    db.commit()
    db.refresh(document)

    return document


# ==========================================
# DELETE OPERATIONS
# ==========================================

def delete_document(db: Session, document_id):
    document = db.get(Document, document_id)

    if document is None:
        return False

    db.delete(document)
    db.commit()

    return True
