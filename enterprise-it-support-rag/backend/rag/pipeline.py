
         
from backend.config import settings
from backend.rag.document_loader import load_documents
from backend.rag.chunker import chunk_documents
from backend.rag.embeddings import embed_texts
from backend.rag.vector_store import ChromaStore
from backend.rag.hybrid_retriever import HybridRetriever
from backend.rag.reranker import CrossEncoderReranker


class RAGPipeline:
    def __init__(self):
        self.store = ChromaStore()
        self.retriever = HybridRetriever(self.store)
        self.reranker = CrossEncoderReranker()
        self.bm25_ready = False

    def ingest_directory(self, directory=None):
        # Step 1: Load documents
        docs = load_documents(
            settings.path(
                directory or settings.DOCUMENT_DIRECTORY
            )
        )

        # Step 2: Split documents into chunks
        chunks = chunk_documents(
            docs,
            settings.CHUNK_SIZE,
            settings.CHUNK_OVERLAP
        )

        if not chunks:
            self.retriever.rebuild_bm25([])
            self.bm25_ready = True

            return {
                "documents": len(docs),
                "chunks": 0,
                "removed_old_chunks": 0
            }

        # Step 3: Generate embeddings
        vectors = embed_texts(
            [chunk["text"] for chunk in chunks]
        )

        # Step 4: Identify documents and chunk IDs
        document_ids = list({
            doc["document_id"] for doc in docs
        })

        new_chunk_ids = [
            chunk["id"] for chunk in chunks
        ]

        # Step 5: Insert or update new chunks
        count = self.store.upsert(
            chunks,
            vectors
        )

        # Step 6: Remove obsolete chunks
        removed = self.store.delete_obsolete_chunks(
            document_ids,
            new_chunk_ids
        )

        # Step 7: Rebuild BM25 index
        self.retriever.rebuild_bm25(chunks)
        self.bm25_ready = True

        return {
            "documents": len(docs),
            "chunks": count,
            "removed_old_chunks": removed
        }

    def retrieve(self, question, top_k=None):
        if not self.store.count():
            raise RuntimeError(
                "Knowledge base is empty. Run ingestion first."
            )

        # Build BM25 index if not already ready
        if not self.bm25_ready:
            docs = load_documents(
                settings.path(settings.DOCUMENT_DIRECTORY)
            )

            chunks = chunk_documents(
                docs,
                settings.CHUNK_SIZE,
                settings.CHUNK_OVERLAP
            )

            self.retriever.rebuild_bm25(chunks)
            self.bm25_ready = True

        # Stage 1: Hybrid retrieval
        candidates = self.retriever.retrieve(
            question,
            top_k=settings.VECTOR_CANDIDATES
        )

        # Stage 2: Cross-Encoder reranking
        final_results = self.reranker.rerank(
            query=question,
            documents=candidates,
            top_k=top_k or settings.TOP_K
        )

        return final_results
