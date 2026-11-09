from backend.rag.document_loader import load_documents


def test_load_all_documents():
    documents = load_documents("data/documents")

    assert len(documents) == 10

    for document in documents:
        assert document["filename"]
        assert document["sections"]
        assert document["sections"][0]["text"].strip()

    print(f"\nSuccessfully loaded {len(documents)} documents")


def test_supported_file_types():
    documents = load_documents("data/documents")

    supported_types = {".txt", ".pdf", ".docx"}

    for document in documents:
        assert document["file_type"] in supported_types