from __future__ import annotations

from io import BytesIO, StringIO
from pathlib import Path
import pytest

from testgen.rag import document_loader
from testgen.rag.document_loader import (
    delete_saved_doc_file,
    load_saved_doc_entries,
    load_text_uploaded_file_entries,
    load_uploaded_files,
    persist_uploaded_doc_files,
)


class UploadedBuffer(BytesIO):
    def __init__(self, name: str, data: bytes) -> None:
        super().__init__(data)
        self.name = name


def test_read_file_bytes_handles_none():
    assert document_loader._read_file_bytes(None) == b""


def test_read_file_bytes_handles_bytes():
    assert document_loader._read_file_bytes(b"data") == b"data"


def test_read_file_bytes_handles_stringio():
    sio = StringIO("text data")
    assert document_loader._read_file_bytes(sio) == b"text data"


def test_read_file_bytes_handles_custom_read_method():
    class CustomReader:
        def read(self):
            return "string text"
    assert document_loader._read_file_bytes(CustomReader()) == b"string text"


def test_read_file_bytes_raises_on_invalid():
    with pytest.raises(TypeError):
        document_loader._read_file_bytes(123)


def test_as_files():
    assert document_loader._as_files(None) == []
    assert document_loader._as_files([1, 2]) == [1, 2]
    assert document_loader._as_files(1) == [1]


def test_entry_name():
    assert document_loader._entry_name(UploadedBuffer("test.txt", b"")) == "test.txt"
    class NoName: pass
    assert document_loader._entry_name(NoName()) == "uploaded-file"


def test_decode_text():
    assert document_loader._decode_text(b"") == ""
    assert document_loader._decode_text(b"\xef\xbb\xbfhello") == "hello"  # BOM stripped


def test_load_pdf_returns_empty_for_empty_file():
    assert document_loader.load_pdf(b"") == ""


def test_load_uploaded_file_handles_none():
    assert document_loader.load_uploaded_file(None) == ""


def test_load_uploaded_file_raises_for_unsupported_type():
    with pytest.raises(ValueError, match="Loại tệp không được hỗ trợ"):
        document_loader.load_uploaded_file(UploadedBuffer("test.png", b"data"))


def test_load_uploaded_files_combines_multiple_documents():
    files = [
        UploadedBuffer("a.txt", "Yeu cau A".encode("utf-8")),
        UploadedBuffer("b.txt", "Yeu cau B".encode("utf-8")),
    ]

    text = load_uploaded_files(files)

    assert "# Tài liệu: a.txt" in text
    assert "# Tài liệu: b.txt" in text
    assert "Yeu cau A" in text
    assert "Yeu cau B" in text


def test_load_uploaded_file_accepts_markdown():
    text = document_loader.load_uploaded_file(
        UploadedBuffer("requirements.md", "# Checkout\n\n- Must total order".encode("utf-8"))
    )

    assert "# Checkout" in text
    assert "Must total order" in text


def test_load_text_uploaded_file_entries_reads_source_code_files():
    files = [
        UploadedBuffer("app.py", b"print('hello')"),
        UploadedBuffer("tests.spec.js", b"const x = 1;"),
    ]

    entries = load_text_uploaded_file_entries(files)

    assert entries == [
        ("app.py", "print('hello')"),
        ("tests.spec.js", "const x = 1;"),
    ]


def test_persist_uploaded_doc_files_and_load_saved_entries(tmp_path: Path):
    files = [
        UploadedBuffer("Spec A.pdf", b"%PDF-1.4 fake-content"),
        UploadedBuffer("req.txt", "hello docs".encode("utf-8")),
        UploadedBuffer("guide.md", "# Guide\nhello markdown".encode("utf-8")),
        UploadedBuffer("image.png", b"image data"), # should be skipped
    ]

    persisted_paths = persist_uploaded_doc_files(files, tmp_path)
    assert len(persisted_paths) == 3
    assert all(path.exists() for path in persisted_paths)

    entries = load_saved_doc_entries(tmp_path)
    assert any(name.endswith(".txt") and "hello docs" in text for name, text in entries)
    assert any(name.endswith(".md") and "hello markdown" in text for name, text in entries)


def test_persist_uploaded_doc_files_overwrites_duplicate_name(tmp_path: Path):
    first = [UploadedBuffer("req.txt", "old docs".encode("utf-8"))]
    second = [UploadedBuffer("req.txt", "new docs".encode("utf-8"))]

    first_paths = persist_uploaded_doc_files(first, tmp_path)
    second_paths = persist_uploaded_doc_files(second, tmp_path)

    assert first_paths == second_paths
    assert first_paths[0].name == "req.txt"
    assert first_paths[0].read_text(encoding="utf-8") == "new docs"


def test_persist_uploaded_doc_files_removes_legacy_hashed_duplicate(tmp_path: Path):
    legacy_path = tmp_path / "req_abcdef123456.txt"
    legacy_path.write_text("old docs", encoding="utf-8")

    persisted_paths = persist_uploaded_doc_files([UploadedBuffer("req.txt", b"new docs")], tmp_path)

    assert persisted_paths[0].name == "req.txt"
    assert persisted_paths[0].read_text(encoding="utf-8") == "new docs"
    assert not legacy_path.exists()


def test_delete_saved_doc_file_removes_only_supported_doc(tmp_path: Path):
    persisted_paths = persist_uploaded_doc_files([UploadedBuffer("req.txt", b"docs")], tmp_path)
    assert persisted_paths[0].exists()

    assert delete_saved_doc_file(tmp_path, "req.txt") is True
    assert not persisted_paths[0].exists()
    assert delete_saved_doc_file(tmp_path, "missing.txt") is False


def test_delete_saved_doc_file_rejects_unsupported_extensions(tmp_path: Path):
    img = tmp_path / "img.png"
    img.write_text("data")
    assert delete_saved_doc_file(tmp_path, "img.png") is False


def test_delete_saved_doc_file_rejects_paths_outside_storage_dir(tmp_path: Path):
    out_path = tmp_path.parent / "out.txt"
    out_path.write_text("out")
    try:
        # Pass a relative path that points outside
        assert delete_saved_doc_file(tmp_path, "../out.txt") is False
    finally:
        out_path.unlink(missing_ok=True)
