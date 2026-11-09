

import chromadb
from backend.config import settings


class ChromaStore:
    def __init__(self):
        path = settings.path(settings.CHROMA_PERSIST_DIRECTORY)
        path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(path=str(path))

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )

    def upsert(self, chunks, embeddings):
        if not chunks:
            return 0

        ids = [chunk["id"] for chunk in chunks]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "Duplicate chunk IDs found in ingestion batch"
            )

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match"
            )

        self.collection.upsert(
            ids=ids,
            documents=[chunk["text"] for chunk in chunks],
            metadatas=[chunk["metadata"] for chunk in chunks],
            embeddings=embeddings
        )

        return len(chunks)

    def delete_obsolete_chunks(self, document_ids, new_chunk_ids):
        if not document_ids:
            return 0

        existing = self.collection.get(
            where={
                "document_id": {
                    "$in": list(set(document_ids))
                }
            },
            include=["metadatas"]
        )

        new_ids = set(new_chunk_ids)

        obsolete_ids = [
            chunk_id
            for chunk_id in existing["ids"]
            if chunk_id not in new_ids
        ]

        if obsolete_ids:
            self.collection.delete(ids=obsolete_ids)

        return len(obsolete_ids)

    def query(self, embedding, n_results=10):
        count = self.collection.count()

        if not count:
            return []

        res = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(n_results, count),
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        return [
            {
                "id": res["ids"][0][i],
                "text": text,
                "metadata": res["metadatas"][0][i],
                "distance": res["distances"][0][i]
            }
            for i, text in enumerate(res["documents"][0])
        ]

    def count(self):
        return self.collection.count()

