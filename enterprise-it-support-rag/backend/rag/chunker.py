
import hashlib


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> list[str]:
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")

    clean = " ".join(text.split())
    chunks, start = [], 0

    while start < len(clean):
        end = min(start + chunk_size, len(clean))

        if end < len(clean):
            boundary = clean.rfind(" ", start, end)
            if boundary > start + int(chunk_size * 0.6):
                end = boundary

        piece = clean[start:end].strip()

        if piece:
            chunks.append(piece)

        if end >= len(clean):
            break

        start = max(end - overlap, start + 1)

    return chunks


def chunk_documents(documents, chunk_size, overlap):
    output = []

    for doc in documents:
        for section in doc["sections"]:
            page = section["page"] or 0

            for idx, chunk in enumerate(
                chunk_text(section["text"], chunk_size, overlap)
            ):
                # Include filename and file type to distinguish different files.
                unique_key = (
                    f'{doc["filename"]}|'
                    f'{doc["file_type"]}|'
                    f'{doc["document_id"]}|'
                    f'{page}|{idx}'
                )

                chunk_id = hashlib.sha256(
                    unique_key.encode("utf-8")
                ).hexdigest()

                output.append({
                    "id": chunk_id,
                    "text": chunk,
                    "metadata": {
                        "document_id": doc["document_id"],
                        "filename": doc["filename"],
                        "file_type": doc["file_type"],
                        "source": doc["source"],
                        "page": page,
                        "chunk_index": idx
                    }
                })

    return output
