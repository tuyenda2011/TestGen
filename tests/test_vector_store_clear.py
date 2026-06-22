from __future__ import annotations

import pytest
from testgen.rag import vector_store

class _FakeClient:
    def __init__(self, collections=None):
        self.collections = set(collections or [])

    def delete_collection(self, name):
        if name not in self.collections:
            raise ValueError("not found")
        self.collections.remove(name)

    def create_collection(self, name, metadata=None):
        self.collections.add(name)
        return {"name": name}

    def get_collection(self, name):
        if name not in self.collections:
            raise ValueError("not found")
        return {"name": name}


def _patch_client(monkeypatch, client):
    def fake_get_client():
        return client

    fake_get_client.cache_clear = lambda: None  # type: ignore[attr-defined]
    monkeypatch.setattr(vector_store, "_get_client", fake_get_client)


def test_validate_collection_name_valid():
    assert vector_store._validate_collection_name("valid_name-123") == "valid_name-123"


def test_validate_collection_name_invalid():
    with pytest.raises(ValueError):
        vector_store._validate_collection_name("a")  # too short
    with pytest.raises(ValueError):
        vector_store._validate_collection_name("invalid!name")


def test_create_or_reset_collection(monkeypatch):
    client = _FakeClient()
    _patch_client(monkeypatch, client)
    
    col = vector_store.create_or_reset_collection("my_collection")
    assert col["name"] == "my_collection"
    assert "my_collection" in client.collections

    # Test reset
    col2 = vector_store.create_or_reset_collection("my_collection")
    assert col2["name"] == "my_collection"


def test_delete_collection(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_store, "CHROMA_PATH", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    
    client = _FakeClient(["my_col"])
    _patch_client(monkeypatch, client)

    assert vector_store.delete_collection("my_col") is True
    assert "my_col" not in client.collections
    assert vector_store.delete_collection("missing_col") is False


def test_delete_collection_no_path(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_store, "CHROMA_PATH", tmp_path / "missing")
    assert vector_store.delete_collection("my_col") is True


def test_get_collection(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_store, "CHROMA_PATH", tmp_path)
    tmp_path.mkdir(exist_ok=True)
    
    client = _FakeClient(["my_col"])
    _patch_client(monkeypatch, client)

    col = vector_store.get_collection("my_col")
    assert col is not None
    assert col["name"] == "my_col"
    
    assert vector_store.get_collection("missing_col") is None


def test_get_collection_no_path(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_store, "CHROMA_PATH", tmp_path / "missing")
    assert vector_store.get_collection("my_col") is None


def test_list_collection_names(monkeypatch):
    class ListClient:
        def list_collections(self):
            return ["col1", type("Col", (), {"name": "col2"})()]
            
    assert vector_store._list_collection_names(ListClient()) == ["col1", "col2"]


def test_list_collection_names_error(monkeypatch):
    class BadClient:
        def list_collections(self):
            raise ValueError("error")
            
    assert vector_store._list_collection_names(BadClient()) == []


def test_release_client_resources():
    class ResClient:
        called = []
        def close(self):
            self.called.append("close")
        
        class System:
            def stop(self):
                ResClient.called.append("stop")
        _system = System()

    client = ResClient()
    vector_store._release_client_resources(client)
    assert "close" in client.called
    assert "stop" in client.called


def test_clear_vector_store_purges_collections_and_disk(tmp_path, monkeypatch):
    chroma_path = tmp_path / "chroma"
    chroma_path.mkdir(parents=True, exist_ok=True)
    (chroma_path / "old.bin").write_bytes(b"legacy")

    monkeypatch.setattr(vector_store, "CHROMA_PATH", chroma_path)
    client = _FakeClient({"docs", "source"})
    _patch_client(monkeypatch, client)

    results, disk_purged = vector_store.clear_vector_store(["docs", "source"], purge_disk=True)

    assert results == {"docs": True, "source": True}
    assert disk_purged is True
    assert client.collections == set()
    assert chroma_path.exists()
    assert not (chroma_path / "old.bin").exists()


def test_clear_vector_store_missing_and_failed_collection(monkeypatch, tmp_path):
    monkeypatch.setattr(vector_store, "CHROMA_PATH", tmp_path / "chroma")
    
    class FailClient(_FakeClient):
        def delete_collection(self, name):
            if name == "docs":
                raise RuntimeError("delete failed")
            super().delete_collection(name)

    client = FailClient({"docs"})
    _patch_client(monkeypatch, client)

    results, disk_purged = vector_store.clear_vector_store(["docs", "source"], purge_disk=False)

    assert results["docs"] is False
    assert results["source"] is True
    assert disk_purged is False


def test_add_chunks_batches_non_empty_documents():
    class FakeCollection:
        def __init__(self):
            self.calls = []

        def add(self, *, ids, documents, embeddings, metadatas):
            self.calls.append(
                {
                    "ids": ids,
                    "documents": documents,
                    "embeddings": embeddings,
                    "metadatas": metadatas,
                }
            )

    collection = FakeCollection()

    vector_store.add_chunks(
        collection,
        [" first ", "", "second", "   ", "third"],
        embedder=lambda text: [float(len(text))],
        batch_size=2,
    )

    assert len(collection.calls) == 2
    assert collection.calls[0]["ids"] == ["chunk-0", "chunk-2"]
    assert collection.calls[0]["documents"] == ["first", "second"]
    assert collection.calls[0]["embeddings"] == [[5.0], [6.0]]
    assert collection.calls[1]["ids"] == ["chunk-4"]
    assert collection.calls[1]["metadatas"] == [{"chunk_index": 4}]
