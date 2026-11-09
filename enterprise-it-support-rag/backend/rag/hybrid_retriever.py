import re
from rank_bm25 import BM25Okapi
from backend.config import settings
from backend.rag.embeddings import embed_texts

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_'-]+", text.lower())

def reciprocal_rank_fusion(vector_hits, lexical_hits, top_k=5, rrf_k=60):
    scores, records = {}, {}
    for hits in (vector_hits, lexical_hits):
        for rank, hit in enumerate(hits, 1):
            key = hit["id"]
            scores[key] = scores.get(key, 0.0) + 1.0 / (rrf_k + rank)
            records[key] = hit
    return [dict(records[k], retrieval_score=scores[k])
            for k in sorted(scores, key=scores.get, reverse=True)[:top_k]]

class HybridRetriever:
    def __init__(self, store):
        self.store, self.bm25, self.chunks = store, None, []
    def rebuild_bm25(self, chunks):
        self.chunks = chunks
        corpus = [tokenize(c["text"]) for c in chunks]
        self.bm25 = BM25Okapi(corpus) if corpus else None
    def retrieve(self, query, top_k=None):
        top_k = top_k or settings.TOP_K
        vector = self.store.query(embed_texts([query])[0], settings.VECTOR_CANDIDATES)
        lexical = []
        if self.bm25:
            scores = self.bm25.get_scores(tokenize(query))
            for idx in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:settings.BM25_CANDIDATES]:
                if scores[idx] > 0:
                    lexical.append(self.chunks[idx])
        return reciprocal_rank_fusion(vector, lexical, top_k, settings.RRF_K)
