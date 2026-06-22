import pytest
import os
import stat
from unittest.mock import patch, MagicMock

from testgen.rag import vector_store

def test_validate_collection_name_invalid():
    with pytest.raises(ValueError):
        vector_store._validate_collection_name("")
    with pytest.raises(ValueError):
        vector_store._validate_collection_name("ab")
    with pytest.raises(ValueError):
        vector_store._validate_collection_name("a!b")

def test_create_or_reset_collection_delete_exc(monkeypatch):
    client = MagicMock()
    client.delete_collection.side_effect = Exception("not found")
    monkeypatch.setattr(vector_store, "_get_client", lambda: client)
    vector_store.create_or_reset_collection("valid_name")
    client.create_collection.assert_called_once()

@patch("pathlib.Path.exists", return_value=False)
def test_delete_collection_path_not_exists(mock_exists):
    assert vector_store.delete_collection("valid_name") is True

@patch("pathlib.Path.exists", return_value=True)
def test_delete_collection_exc(mock_exists, monkeypatch):
    client = MagicMock()
    client.delete_collection.side_effect = Exception("error")
    monkeypatch.setattr(vector_store, "_get_client", lambda: client)
    assert vector_store.delete_collection("valid_name") is False

@patch("pathlib.Path.exists", return_value=False)
def test_get_collection_path_not_exists(mock_exists):
    assert vector_store.get_collection("valid_name") is None

@patch("pathlib.Path.exists", return_value=True)
def test_get_collection_exc(mock_exists, monkeypatch):
    client = MagicMock()
    client.get_collection.side_effect = Exception("error")
    monkeypatch.setattr(vector_store, "_get_client", lambda: client)
    assert vector_store.get_collection("valid_name") is None

def test_delete_readonly(monkeypatch):
    calls = []
    monkeypatch.setattr(os, "chmod", lambda p, mode: calls.append((p, mode)))
    def fake_func(p): calls.append(p)
    vector_store._delete_readonly(fake_func, "path", None)
    assert calls == [("path", stat.S_IWRITE), "path"]

def test_list_collection_names_exc():
    client = MagicMock()
    client.list_collections.side_effect = Exception("error")
    assert vector_store._list_collection_names(client) == []

def test_list_collection_names_str():
    client = MagicMock()
    client.list_collections.return_value = ["  col1  ", "col2"]
    assert vector_store._list_collection_names(client) == ["col1", "col2"]

def test_release_client_resources():
    client = MagicMock()
    client.close.side_effect = Exception("error")
    client.stop.side_effect = Exception("error")
    client._system.stop.side_effect = Exception("error")
    
    # Should not raise
    vector_store._release_client_resources(client)

def test_clear_vector_store_delete_error(monkeypatch):
    client = MagicMock()
    client.get_collection.return_value = "exists"
    client.delete_collection.side_effect = Exception("cannot delete")
    monkeypatch.setattr(vector_store, "_get_client", lambda: client)
    
    res, purged = vector_store.clear_vector_store(["col1"], purge_disk=False)
    assert res["col1"] is False
    assert purged is False

def test_clear_vector_store_purge_disk(monkeypatch):
    client = MagicMock()
    client.get_collection.return_value = "exists"
    client.list_collections.return_value = ["leftover"]
    mock_get_client = MagicMock(return_value=client)
    monkeypatch.setattr(vector_store, "_get_client", mock_get_client)
    
    with patch("testgen.rag.vector_store.CHROMA_PATH") as mock_path, \
         patch("testgen.rag.vector_store.rmtree", side_effect=Exception("error")):
        mock_path.exists.return_value = True
        res, purged = vector_store.clear_vector_store(["col1"], purge_disk=True)
        assert purged is False

def test_clear_vector_store_purge_disk_rmtree_success(monkeypatch):
    client = MagicMock()
    mock_get_client = MagicMock(return_value=client)
    monkeypatch.setattr(vector_store, "_get_client", mock_get_client)
    
    with patch("testgen.rag.vector_store.CHROMA_PATH") as mock_path, \
         patch("testgen.rag.vector_store.rmtree"):
        
        mock_path.exists.side_effect = [True, False, False, False]
        res, purged = vector_store.clear_vector_store([], purge_disk=True)
        assert purged is True

def test_add_chunks_no_metadata():
    col = MagicMock()
    vector_store.add_chunks(col, ["chunk1", "  "], metadatas=None, embedder=lambda x: [1.0], batch_size=1)
    col.add.assert_called_once()
    args = col.add.call_args[1]
    assert args["documents"] == ["chunk1"]
    assert args["metadatas"] == [{"chunk_index": 0}]

def test_add_chunks_empty_collection():
    assert vector_store.add_chunks(None, ["chunk1"]) is None
