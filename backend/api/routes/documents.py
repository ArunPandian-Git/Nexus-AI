from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

router = APIRouter(
    prefix="/documents",
    tags=["Document Intelligence"]
)

STORAGE_DIR = Path("/content/storage/documents")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf", ".txt", ".docx", ".csv", ".xlsx"
}

MAX_FILE_SIZE = 20 * 1024 * 1024


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty files are not allowed."
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 20 MB limit."
        )

    document_id = str(uuid.uuid4())

    safe_name = f"{document_id}{extension}"
    destination = STORAGE_DIR / safe_name

    destination.write_bytes(content)

    return {
        "application": "NEXUS AI",
        "document_id": document_id,
        "filename": file.filename,
        "stored_filename": safe_name,
        "size_bytes": len(content),
        "status": "uploaded"
    }
