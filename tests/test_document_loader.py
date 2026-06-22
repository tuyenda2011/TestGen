import pytest
from pathlib import Path
from io import BytesIO

from testgen.rag import document_loader

class DummyFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def getvalue(self):
        return self.data

class DummyReadFile:
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def read(self):
        return self.data

def test_read_file_bytes():
    assert document_loader._read_file_bytes(None) == b""
    assert document_loader._read_file_bytes(b"hello") == b"hello"
    assert document_loader._read_file_bytes(DummyFile("1.txt", "hello")) == b"hello"
    assert document_loader._read_file_bytes(DummyFile("2.txt", b"world")) == b"world"
    assert document_loader._read_file_bytes(DummyReadFile("3.txt", "hello")) == b"hello"
    assert document_loader._read_file_bytes(DummyReadFile("4.txt", b"world")) == b"world"
    with pytest.raises(TypeError):
        document_loader._read_file_bytes(123)

def test_as_files():
    assert document_loader._as_files(None) == []
    assert document_loader._as_files([1, 2]) == [1, 2]
    assert document_loader._as_files(1) == [1]

def test_load_txt():
    assert document_loader.load_txt(b"hello") == "hello"

def test_load_pdf():
    assert document_loader.load_pdf(b"") == ""
    # We can mock pypdf.PdfReader to test PDF loading
    from unittest.mock import patch, MagicMock
    with patch("testgen.rag.document_loader.PdfReader") as mock_reader:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "pdf text "
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_reader.return_value = mock_pdf
        assert document_loader.load_pdf(b"dummy") == "pdf text"

def test_load_uploaded_file():
    assert document_loader.load_uploaded_file(None) == ""
    assert document_loader.load_uploaded_file(DummyFile("test.txt", "hello")) == "hello"
    assert document_loader.load_uploaded_file(DummyFile("test.md", "markdown")) == "markdown"
    
    with pytest.raises(ValueError, match="Loại tệp không được hỗ trợ"):
        document_loader.load_uploaded_file(DummyFile("test.csv", "a,b,c"))

def test_load_text_uploaded_file_entries():
    res = document_loader.load_text_uploaded_file_entries(DummyFile("test.txt", "hello"))
    assert res == [("test.txt", "hello")]

def test_load_uploaded_files():
    res = document_loader.load_uploaded_files([DummyFile("1.txt", "hello"), DummyFile("2.txt", "")])
    assert "Tài liệu: 1.txt\n\nhello" in res

def test_safe_stem():
    assert document_loader._safe_stem("a!@#b") == "a_b"
    assert document_loader._safe_stem("!") == "uploaded_file"

def test_persist_uploaded_doc_files(tmp_path):
    res = document_loader.persist_uploaded_doc_files([
        DummyFile("valid.txt", b"ok"), 
        DummyFile("invalid.csv", b"bad"), 
        DummyFile("empty.txt", b"")
    ], tmp_path)
    assert len(res) == 1
    assert res[0].name == "valid.txt"
    assert res[0].read_text() == "ok"

def test_delete_legacy_hashed_duplicates(tmp_path):
    f1 = tmp_path / "doc_1234567890ab.txt"
    f1.touch()
    f2 = tmp_path / "doc_other.txt"
    f2.touch()
    document_loader._delete_legacy_hashed_duplicates(tmp_path, "doc", ".txt")
    assert not f1.exists()
    assert f2.exists()

def test_delete_saved_doc_file(tmp_path):
    f1 = tmp_path / "valid.txt"
    f1.touch()
    assert document_loader.delete_saved_doc_file(tmp_path, "valid.txt") is True
    assert not f1.exists()
    
    # invalid extension
    f2 = tmp_path / "bad.csv"
    f2.touch()
    assert document_loader.delete_saved_doc_file(tmp_path, "bad.csv") is False
    
    # not exist
    assert document_loader.delete_saved_doc_file(tmp_path, "valid.txt") is False

def test_list_saved_doc_files(tmp_path):
    assert document_loader.list_saved_doc_files(tmp_path / "non_existent") == []
    
    f1 = tmp_path / "a.txt"
    f1.touch()
    f2 = tmp_path / "b.md"
    f2.touch()
    f3 = tmp_path / "c.csv"
    f3.touch()
    
    res = document_loader.list_saved_doc_files(tmp_path)
    assert len(res) == 2
    assert res[0].name == "a.txt"
    assert res[1].name == "b.md"

def test_load_saved_doc_entries(tmp_path):
    f1 = tmp_path / "a.txt"
    f1.write_text("hello txt")
    f2 = tmp_path / "b.md"
    f2.write_text("hello md")
    
    res = document_loader.load_saved_doc_entries(tmp_path)
    assert len(res) == 2
    assert res[0] == ("a.txt", "hello txt")
    assert res[1] == ("b.md", "hello md")
    
    f3 = tmp_path / "c.pdf"
    f3.write_bytes(b"dummy pdf bytes")
    # without mocking PdfReader, it might raise PdfStreamError which is caught and ignored
    res2 = document_loader.load_saved_doc_entries(tmp_path)
    assert len(res2) == 2  # c.pdf ignored because of Exception
