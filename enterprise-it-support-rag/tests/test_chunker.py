import pytest
from backend.rag.chunker import chunk_text

def test_empty_text():
    assert chunk_text("   ") == []

def test_multiple_chunks():
    result = chunk_text(" ".join(["support"] * 250), 100, 20)
    assert len(result) > 1 and all(result)

def test_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("hello", 10, 10)
