from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

def load_document(file_path: Path) -> dict:
    ext = file_path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")
    if ext == ".txt":
        sections = [{"text": file_path.read_text(encoding="utf-8", errors="replace"), "page": None}]
    elif ext == ".pdf":
        import pymupdf
        sections = []
        with pymupdf.open(file_path) as pdf:
            for number, page in enumerate(pdf, start=1):
                text = page.get_text("text")
                if text.strip():
                    sections.append({"text": text, "page": number})
    else:
        from docx import Document
        doc = Document(file_path)
        text = "\\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        sections = [{"text": text, "page": None}]
    if not any(s["text"].strip() for s in sections):
        raise ValueError(f"No readable text found in {file_path.name}")
    return {"document_id": file_path.stem, "filename": file_path.name,
            "file_type": ext, "sections": sections, "source": file_path.name}

def load_documents(directory):
    folder = Path(directory)
    if not folder.exists():
        raise FileNotFoundError(f"Document directory does not exist: {folder}")
    return [load_document(p) for p in sorted(folder.rglob("*"))
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS]
