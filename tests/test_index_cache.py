import pytest
from unittest.mock import MagicMock
from testgen.rag import index_cache

def test_build_labeled_chunks():
    sections = [("doc1", "text1"), ("doc2", "a"*200)]
    chunks = index_cache.build_labeled_chunks(sections, "Prefix", 100, 10)
    assert len(chunks) >= 3
    assert "# Prefix: doc1" in chunks[0]
    assert "# Prefix: doc2 (phần 1)" in chunks[1]

def test_build_sections_signature():
    sig = index_cache.build_sections_signature(
        collection_name="col",
        sections=[("a", "b")],
        section_prefix="pfx",
        backend="gemini",
        chunk_size=10,
        chunk_overlap=1
    )
    assert len(sig) == 64  # sha256

def test_call_add_chunks_with_metadata():
    col = MagicMock()
    mock_add = MagicMock()
    # Define a fake function with 3 parameters to simulate signature
    def fake_fn(a, b, c): pass
    # Using patch or just overriding signature check. Inspect signature might fail on mock, let's use a real function
    index_cache._call_add_chunks(fake_fn, col, ["chunk"], [{"m": 1}])
    # But fake_fn does nothing. We can just mock the whole thing or pass a lambda
    
    lst = []
    def fake_add_3(c, ch, m): lst.append((c, ch, m))
    index_cache._call_add_chunks(fake_add_3, "col", ["chunk"], [{"m": 1}])
    assert lst == [("col", ["chunk"], [{"m": 1}])]
    
    lst2 = []
    def fake_add_2(c, ch): lst2.append((c, ch))
    index_cache._call_add_chunks(fake_add_2, "col", ["chunk"], [{"m": 1}])
    assert lst2 == [("col", ["chunk"])]

def test_call_add_chunks_inspect_fails():
    # If inspect fails, it falls back to 2 parameters
    lst = []
    def fake_add(*args, **kwargs): lst.append(args)
    # Built-in functions usually raise ValueError on inspect
    import builtins
    index_cache._call_add_chunks(builtins.print, "col", ["chunk"], [{"m": 1}])

def test_prepare_indexed_collection_reused():
    mock_get = MagicMock(return_value="collection")
    mock_create = MagicMock()
    mock_add = MagicMock()
    
    sections = [("a", "b")]
    sig = index_cache.build_sections_signature(
        collection_name="col", sections=sections, section_prefix="pfx", 
        backend="gemini", chunk_size=100, chunk_overlap=10
    )
    
    res = index_cache.prepare_indexed_collection(
        collection_name="col", sections=sections, section_prefix="pfx",
        backend="gemini", chunk_size=100, chunk_overlap=10,
        previous_signature=sig, get_collection_fn=mock_get,
        create_or_reset_collection_fn=mock_create, add_chunks_fn=mock_add
    )
    assert res.reused is True
    assert res.collection == "collection"
    mock_create.assert_not_called()

def test_prepare_indexed_collection_new():
    mock_get = MagicMock(return_value=None)
    mock_create = MagicMock(return_value="new_collection")
    mock_add = MagicMock()
    
    sections = [("a", "b")]
    
    res = index_cache.prepare_indexed_collection(
        collection_name="col", sections=sections, section_prefix="pfx",
        backend="gemini", chunk_size=100, chunk_overlap=10,
        previous_signature="different", get_collection_fn=mock_get,
        create_or_reset_collection_fn=mock_create, add_chunks_fn=mock_add
    )
    assert res.reused is False
    assert res.collection == "new_collection"
    mock_create.assert_called_once()
    mock_add.assert_called_once()
