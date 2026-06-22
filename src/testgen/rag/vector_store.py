from __future__ import annotations

from functools import lru_cache
import gc
import os
import re
from shutil import rmtree
import stat
import time
from typing import Callable, Any

import chromadb
from chromadb.config import Settings

from testgen.core.config import CHROMA_PATH
from testgen.core.llm import get_embedding, get_embedding_batch
from testgen.core.logger import get_logger

logger = get_logger(__name__)

_COLLECTION_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,510}[A-Za-z0-9]$")


def _validate_collection_name(collection_name: str) -> str:
    cleaned = (collection_name or "").strip()
    if not _COLLECTION_NAME_PATTERN.fullmatch(cleaned):
        raise ValueError(
            "Chroma collection name must be 3-512 characters, use only letters, numbers, '.', '_' or '-', "
            "and start/end with a letter or number."
        )
    return cleaned


@lru_cache(maxsize=1)
def _get_client() -> Any:
    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(CHROMA_PATH),
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )


def create_or_reset_collection(collection_name: str):
    collection_name = _validate_collection_name(collection_name)
    client = _get_client()
    try:
        client.delete_collection(name=collection_name)
    except Exception:
        pass
    return client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})


def delete_collection(collection_name: str) -> bool:
    collection_name = _validate_collection_name(collection_name)
    if not CHROMA_PATH.exists():
        return True
    client = _get_client()
    try:
        client.delete_collection(name=collection_name)
        return True
    except Exception as exc:
        logger.warning(f"Lỗi khi xóa collection {collection_name}: {exc}")
        return False


def get_collection(collection_name: str):
    collection_name = _validate_collection_name(collection_name)
    if not CHROMA_PATH.exists():
        return None
    client = _get_client()
    try:
        return client.get_collection(name=collection_name)
    except Exception as exc:
        msg = str(exc)
        if "does not exist" in msg:
            logger.info(f"Collection {collection_name} chưa tồn tại (điều này bình thường khi app mới chạy lần đầu).")
        else:
            logger.warning(f"Lỗi khi lấy collection {collection_name}: {exc}")
        return None


def _delete_readonly(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _list_collection_names(client: Any) -> list[str]:
    try:
        collections = client.list_collections()
    except Exception as exc:
        logger.warning(f"Lỗi khi liệt kê collections: {exc}")
        return []

    names: list[str] = []
    for item in collections:
        if isinstance(item, str):
            name = item.strip()
        else:
            name = str(getattr(item, "name", "")).strip()
        if name:
            names.append(name)
    return names


def _release_client_resources(client: Any) -> None:
    # Best-effort cleanup across Chroma versions.
    for method_name in ("close", "stop"):
        method = getattr(client, method_name, None)
        if callable(method):
            try:
                method()
            except Exception:
                pass

    system = getattr(client, "_system", None)
    if system is not None:
        stop = getattr(system, "stop", None)
        if callable(stop):
            try:
                stop()
            except Exception:
                pass

    # Some versions keep global client/system maps.
    try:
        from chromadb.api import shared_system_client as shared_client  # type: ignore

        shared_class = getattr(shared_client, "SharedSystemClient", None)
        cache_map = getattr(shared_class, "_identifier_to_system", None) if shared_class is not None else None
        if isinstance(cache_map, dict):
            cache_map.clear()
    except Exception:
        pass


def clear_vector_store(collection_names: list[str], purge_disk: bool = False) -> tuple[dict[str, bool], bool]:
    client = _get_client()
    results: dict[str, bool] = {}

    normalized_names = []
    for name in collection_names:
        cleaned = (name or "").strip()
        if cleaned:
            normalized_names.append(_validate_collection_name(cleaned))

    for name in normalized_names:
        if not (name or "").strip():
            continue
        try:
            # If collection is missing, treat as already cleared.
            client.get_collection(name=name)
        except Exception:
            results[name] = True
            continue

        try:
            client.delete_collection(name=name)
            results[name] = True
        except Exception as exc:
            logger.warning(f"Lỗi khi xóa collection {name} trong clear_vector_store: {exc}")
            results[name] = False

    if not purge_disk:
        return results, False

    disk_purged = False
    # Try to remove any remaining collections before deleting files.
    for leftover_name in _list_collection_names(client):
        try:
            client.delete_collection(name=leftover_name)
        except Exception:
            pass

    # Try full reset first (if supported by this Chroma build).
    reset = getattr(client, "reset", None)
    if callable(reset):
        try:
            reset()
        except Exception:
            pass

    try:
        _release_client_resources(client)
        del client
    except Exception:
        pass

    try:
        gc.collect()
        _get_client.cache_clear()
        for _ in range(5):
            if not CHROMA_PATH.exists():
                disk_purged = True
                break
            try:
                rmtree(CHROMA_PATH, onerror=_delete_readonly)
                disk_purged = not CHROMA_PATH.exists()
                if disk_purged:
                    break
            except Exception:
                time.sleep(0.15)
    except Exception:
        disk_purged = False

    if disk_purged:
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)

    return results, disk_purged


EmbeddingFn = Callable[[str], list[float]]
EmbeddingBatchFn = Callable[[list[str]], list[list[float]]]

def add_chunks(
    collection,
    chunks: list[str],
    metadatas: list[dict[str, Any]] | None = None,
    embedder: EmbeddingFn | None = None,
    batch_embedder: EmbeddingBatchFn | None = None,
    batch_size: int = 32,
) -> None:
    if collection is None or not chunks:
        return

    batch_embed = batch_embedder or get_embedding_batch
    size = max(int(batch_size or 1), 1)
    ids: list[str] = []
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadata_batch: list[dict[str, Any]] = []

    def flush() -> None:
        if not ids:
            return
        
        # Batch Embed
        try:
            batch_embeddings = batch_embed(documents)
            embeddings.extend(batch_embeddings)
        except Exception as e:
            logger.warning(f"Batch embedding failed, falling back to sequential: {e}")
            # Fallback to sequential if batch fails
            embed = embedder or get_embedding
            for doc in documents:
                embeddings.append(embed(doc))
        
        collection.add(
            ids=list(ids),
            documents=list(documents),
            embeddings=list(embeddings),
            metadatas=list(metadata_batch),
        )
        ids.clear()
        documents.clear()
        embeddings.clear()
        metadata_batch.clear()

    for index, chunk in enumerate(chunks):
        if not chunk or not chunk.strip():
            continue
        cleaned = chunk.strip()
        ids.append(f"chunk-{index}")
        documents.append(cleaned)
        
        metadata = dict(metadatas[index]) if metadatas and index < len(metadatas) else {}
        metadata["chunk_index"] = int(metadata.get("chunk_index", index) or index)
        metadata_batch.append(metadata)
        
        if len(ids) >= size:
            flush()

    if ids:
        flush()
