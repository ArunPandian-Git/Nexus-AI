%%writefile /content/backend/api/routes/documents.py

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.api.dependencies import get_database
from backend.core.document_processor import extract_document
from database.crud import create_document

router = APIRouter(
    prefix="/documents",
    tags=["Document Intelligence"]
)

STORAGE_DIR = Path("/content/storage/documents")
EXTRACTED_DIR = Path("/content/storage/extracted")

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".txt", ".csv", ".xlsx"
}

MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_database)
):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported document format"
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 20 MB upload limit"
        )

    original_name = Path(file.filename).name
    unique_name = f"{uuid4().hex}{extension}"

    file_path = STORAGE_DIR / unique_name

    try:
        # Save original document
        file_path.write_bytes(content)

        # Extract document text
        result = extract_document(str(file_path))

        # Save extracted text separately
        extracted_path = EXTRACTED_DIR / f"{file_path.stem}.txt"

        extracted_path.write_text(
            result["extracted_text"],
            encoding="utf-8"
        )

        # Save metadata in database
        document = create_document(
            db=db,
            filename=original_name,
            file_path=str(file_path),
            file_type=extension.replace(".", ""),
            file_size=len(content),
            processing_status=result["status"]
        )

        return {
            "message": "Document uploaded and processed successfully",
            "document_id": document.id,
            "filename": original_name,
            "file_type": extension.replace(".", ""),
            "file_size": len(content),
            "processing_status": result["status"],
            "character_count": result["character_count"],
            "extracted_text_path": str(extracted_path)
        }

    except Exception as error:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        if isinstance(error, HTTPException):
            raise error

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(error)}"
        )

    finally:
        await file.close()


@router.get("/")
def list_documents(db: Session = Depends(get_database)):
    from database.crud import get_all_documents

    documents = get_all_documents(db)

    return {
        "total_documents": len(documents),
        "documents": [
            {
                "id": document.id,
                "filename": document.filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "processing_status": document.processing_status
            }
            for document in documents
        ]
    }
