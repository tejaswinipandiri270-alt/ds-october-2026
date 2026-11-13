
from backend.config import settings
from backend.rag.azure_search_retriever import AzureSearchRetriever


class RAGPipeline:

    def __init__(self):

        self.bm25_ready = False

        if settings.AZURE_SEARCH_ENABLED:

            print("Initializing Azure AI Search pipeline...")

            self.store = None
            self.retriever = None
            self.reranker = None

            self.azure_retriever = AzureSearchRetriever()

        else:

            print("Initializing local RAG pipeline...")

            from backend.rag.vector_store import ChromaStore
            from backend.rag.hybrid_retriever import HybridRetriever
            from backend.rag.reranker import CrossEncoderReranker

            self.store = ChromaStore()
            self.retriever = HybridRetriever(self.store)
            self.reranker = CrossEncoderReranker()

            self.azure_retriever = None

    def ingest_directory(self, directory=None):

        if self.azure_retriever is not None:
            raise RuntimeError(
                "Azure mode uses Blob Storage and Azure AI Search "
                "for document ingestion. Local ingestion is disabled."
            )

        from backend.rag.document_loader import load_documents
        from backend.rag.chunker import chunk_documents
        from backend.rag.embeddings import embed_texts

        docs = load_documents(
            settings.path(directory or settings.DOCUMENT_DIRECTORY)
        )

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

        vectors = embed_texts(
            [chunk["text"] for chunk in chunks]
        )

        document_ids = list({
            doc["document_id"] for doc in docs
        })

        new_chunk_ids = [
            chunk["id"] for chunk in chunks
        ]

        count = self.store.upsert(chunks, vectors)

        removed = self.store.delete_obsolete_chunks(
            document_ids,
            new_chunk_ids
        )

        self.retriever.rebuild_bm25(chunks)
        self.bm25_ready = True

        return {
            "documents": len(docs),
            "chunks": count,
            "removed_old_chunks": removed
        }

    def retrieve(self, question, top_k=None):

        if self.azure_retriever is not None:

            print("Using Azure AI Search Hybrid Retrieval...")

            response = self.azure_retriever.hybrid_search(
                question,
                top_k=settings.VECTOR_CANDIDATES
            )

            candidates = response["results"]

            # Azure Search already performs hybrid retrieval.
            # Do not load the local Cross-Encoder here.
            return candidates[:(top_k or settings.TOP_K)]

        print("Using Local ChromaDB + BM25 Retrieval...")

        if not self.store.count():
            raise RuntimeError(
                "Knowledge base is empty. Run ingestion first."
            )

        if not self.bm25_ready:

            from backend.rag.document_loader import load_documents
            from backend.rag.chunker import chunk_documents

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

        candidates = self.retriever.retrieve(
            question,
            top_k=settings.VECTOR_CANDIDATES
        )

        return self.reranker.rerank(
            query=question,
            documents=candidates,
            top_k=top_k or settings.TOP_K
        )

