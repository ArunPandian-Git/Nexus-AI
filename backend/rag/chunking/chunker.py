%%writefile /content/backend/rag/chunking/chunker.py

import re
from typing import List, Dict

from backend.rag.chunking.text_cleaner import clean_text


class DocumentChunker:

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
        min_chunk_size: int = 50
    ):

        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive")

        if chunk_overlap < 0:
            raise ValueError("Chunk overlap cannot be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "Chunk overlap must be smaller than chunk size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    def split_text(self, text: str) -> List[str]:

        text = clean_text(text)

        if not text:
            return []

        # Split text into paragraphs
        paragraphs = re.split(r"\n\s*\n", text)

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:
                continue

            # Handle paragraphs larger than chunk size
            if len(paragraph) > self.chunk_size:

                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""

                start = 0

                while start < len(paragraph):

                    end = start + self.chunk_size

                    piece = paragraph[start:end].strip()

                    if piece:
                        chunks.append(piece)

                    if end >= len(paragraph):
                        break

                    start = end - self.chunk_overlap

                continue

            candidate = (
                current_chunk + "\n\n" + paragraph
                if current_chunk
                else paragraph
            )

            if len(candidate) <= self.chunk_size:

                current_chunk = candidate

            else:

                if current_chunk:
                    chunks.append(current_chunk)

                overlap_text = (
                    current_chunk[-self.chunk_overlap:]
                    if self.chunk_overlap > 0
                    else ""
                )

                current_chunk = (
                    overlap_text + "\n\n" + paragraph
                    if overlap_text
                    else paragraph
                )

        if current_chunk:
            chunks.append(current_chunk)

        # Assign chunk IDs and metadata
        return [
            chunk
            for chunk in chunks
            if len(chunk.strip()) >= self.min_chunk_size
        ]

    def create_chunks(
        self,
        text: str,
        document_id: str,
        filename: str
    ) -> List[Dict]:

        text_chunks = self.split_text(text)

        results = []

        for index, chunk in enumerate(text_chunks):

            results.append({
                "chunk_id": f"{document_id}_{index + 1}",
                "document_id": document_id,
                "filename": filename,
                "chunk_index": index,
                "content": chunk,
                "character_count": len(chunk)
            })

        return results
