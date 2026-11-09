from backend.rag.hybrid_retriever import reciprocal_rank_fusion

def test_rrf_combines_results():
    a = [{"id":"a","text":"alpha"}, {"id":"b","text":"beta"}]
    b = [{"id":"b","text":"beta"}, {"id":"c","text":"gamma"}]
    result = reciprocal_rank_fusion(a, b, 3)
    assert {x["id"] for x in result} == {"a", "b", "c"}
