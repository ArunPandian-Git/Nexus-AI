%%writefile /content/database/chunk_crud.py

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database.chunk_models import DocumentChunk


def save_document_chunks(
    db: Session,
    document_id: int,
    chunks: list
):

    try:

        # Remove previously stored chunks for this document
        db.execute(
            delete(DocumentChunk).where(
                DocumentChunk.document_id == document_id
            )
        )

        saved_chunks = []

        for chunk in chunks:

            record = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk["chunk_index"],
                chunk_id=chunk["chunk_id"],
                content=chunk["content"],
                character_count=chunk["character_count"]
            )

            db.add(record)
            saved_chunks.append(record)

        db.commit()

        return len(saved_chunks)

    except Exception:
        db.rollback()
        raise


def get_document_chunks(
    db: Session,
    document_id: int
):

    return list(
        db.scalars(
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        ).all()
    )


def get_all_chunks(db: Session):

    return list(
        db.scalars(
            select(DocumentChunk)
            .order_by(DocumentChunk.id)
        ).all()
    )


def delete_document_chunks(
    db: Session,
    document_id: int
):

    result = db.execute(
        delete(DocumentChunk).where(
            DocumentChunk.document_id == document_id
        )
    )

    db.commit()

    return result.rowcount
