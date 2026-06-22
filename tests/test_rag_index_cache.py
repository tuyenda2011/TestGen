from __future__ import annotations

from testgen.rag.index_cache import build_sections_signature, prepare_indexed_collection


def test_sections_signature_changes_when_input_changes():
    first = build_sections_signature(
        collection_name="docs",
        sections=[("a.txt", "hello")],
        section_prefix="Tài liệu",
        backend="ollama",
        chunk_size=100,
        chunk_overlap=10,
    )
    second = build_sections_signature(
        collection_name="docs",
        sections=[("a.txt", "hello changed")],
        section_prefix="Tài liệu",
        backend="ollama",
        chunk_size=100,
        chunk_overlap=10,
    )

    assert first != second


def test_prepare_indexed_collection_reuses_matching_signature():
    calls = {"created": 0, "added": 0, "got": 0}
    existing_collection = {"name": "docs"}
    previous_signature = build_sections_signature(
        collection_name="docs",
        sections=[("a.txt", "hello")],
        section_prefix="Tài liệu",
        backend="ollama",
        chunk_size=100,
        chunk_overlap=10,
    )

    result = prepare_indexed_collection(
        collection_name="docs",
        sections=[("a.txt", "hello")],
        section_prefix="Tài liệu",
        backend="ollama",
        chunk_size=100,
        chunk_overlap=10,
        previous_signature=previous_signature,
        get_collection_fn=lambda name: calls.__setitem__("got", calls["got"] + 1) or existing_collection,
        create_or_reset_collection_fn=lambda name: calls.__setitem__("created", calls["created"] + 1) or {"new": name},
        add_chunks_fn=lambda collection, chunks: calls.__setitem__("added", calls["added"] + len(chunks)),
    )

    assert result.reused is True
    assert result.collection == existing_collection
    assert calls == {"created": 0, "added": 0, "got": 1}


def test_prepare_indexed_collection_reindexes_changed_input():
    calls = {"created": 0, "added": 0}

    result = prepare_indexed_collection(
        collection_name="docs",
        sections=[("a.txt", "hello changed")],
        section_prefix="Tài liệu",
        backend="ollama",
        chunk_size=100,
        chunk_overlap=10,
        previous_signature="old-signature",
        get_collection_fn=lambda name: None,
        create_or_reset_collection_fn=lambda name: calls.__setitem__("created", calls["created"] + 1) or {"new": name},
        add_chunks_fn=lambda collection, chunks: calls.__setitem__("added", calls["added"] + len(chunks)),
    )

    assert result.reused is False
    assert calls == {"created": 1, "added": 1}
