%%writefile /content/backend/core/document_processor.py

from pathlib import Path
import csv
import fitz
from docx import Document as WordDocument
from openpyxl import load_workbook


def extract_pdf(file_path):
    text = []

    with fitz.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text()

            if page_text.strip():
                text.append(
                    f"\n--- PAGE {page_number} ---\n{page_text}"
                )

    return "\n".join(text)


def extract_docx(file_path):
    document = WordDocument(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_txt(file_path):
    return Path(file_path).read_text(
        encoding="utf-8",
        errors="replace"
    )


def extract_csv(file_path):
    rows = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        errors="replace",
        newline=""
    ) as file:

        reader = csv.reader(file)

        for row in reader:
            rows.append(" | ".join(row))

    return "\n".join(rows)


def extract_xlsx(file_path):
    workbook = load_workbook(
        file_path,
        read_only=True,
        data_only=True
    )

    content = []

    try:
        for sheet in workbook.worksheets:
            content.append(f"\n--- SHEET: {sheet.title} ---")

            for row in sheet.iter_rows(values_only=True):
                values = [
                    str(value)
                    for value in row
                    if value is not None
                ]

                if values:
                    content.append(" | ".join(values))

    finally:
        workbook.close()

    return "\n".join(content)


def extract_document(file_path):

    extension = Path(file_path).suffix.lower()

    extractors = {
        ".pdf": extract_pdf,
        ".docx": extract_docx,
        ".txt": extract_txt,
        ".csv": extract_csv,
        ".xlsx": extract_xlsx
    }

    if extension not in extractors:
        raise ValueError(
            f"Unsupported document format: {extension}"
        )

    text = extractors[extension](file_path)

    return {
        "filename": Path(file_path).name,
        "file_type": extension.replace(".", ""),
        "extracted_text": text,
        "character_count": len(text),
        "status": "processed" if text.strip() else "empty"
    }
