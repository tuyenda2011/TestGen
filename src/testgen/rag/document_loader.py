from __future__ import annotations

from testgen.core.logger import get_logger
logger = get_logger(__name__)

from io import BytesIO
from pathlib import Path
import re
import logging
from typing import Any, Callable

from pypdf import PdfReader

# P0.1.1: Tắt cảnh báo từ pypdf (như lỗi "Got invalid hex string" do có emoji)
logging.getLogger("pypdf").setLevel(logging.ERROR)

from testgen.core.constants import CODE_FILE_TYPES

_DOC_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}
_SAFE_NAME_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def _read_file_bytes(file_obj: Any) -> bytes:
    if file_obj is None:
        return b""
    if isinstance(file_obj, (bytes, bytearray)):
        return bytes(file_obj)
    if hasattr(file_obj, "getvalue"):
        data = file_obj.getvalue()
        if isinstance(data, str):
            return data.encode("utf-8")
        return bytes(data)
    if hasattr(file_obj, "read"):
        data = file_obj.read()
        if isinstance(data, str):
            return data.encode("utf-8")
        return bytes(data)
    raise TypeError("Đối tượng tệp không được hỗ trợ.")


def _as_files(uploaded_files: Any) -> list[Any]:
    if not uploaded_files:
        return []
    if isinstance(uploaded_files, (list, tuple)):
        return list(uploaded_files)
    return [uploaded_files]


def _entry_name(uploaded_file: Any) -> str:
    return getattr(uploaded_file, "name", "uploaded-file")


def _decode_text(data: bytes) -> str:
    if not data:
        return ""
    return data.decode("utf-8-sig", errors="replace")


def load_txt(file) -> str:
    return _decode_text(_read_file_bytes(file))


def _clean_pdf_text(text: str) -> str:
    if not text:
        return ""
    # Thay thế null bytes và các ký tự không in được có thể gây rác DB
    cleaned = text.replace("\x00", "")
    # Xóa các chuỗi surrogate unicode rác do parse PDF bị lỗi hex
    cleaned = re.sub(r'[\ud800-\udfff]', '', cleaned)
    return cleaned.strip()


def load_pdf(file) -> str:
    data = _read_file_bytes(file)
    if not data:
        return ""

    reader = PdfReader(BytesIO(data))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        stripped = _clean_pdf_text(text)
        if stripped:
            pages.append(stripped)
    return "\n\n".join(pages)

def load_pdf_pages(file, *, source_name: str = "") -> list[dict[str, object]]:
    data = _read_file_bytes(file)
    if not data:
        return []

    reader = PdfReader(BytesIO(data))
    pages: list[dict[str, object]] = []
    
    if not source_name:
        source_name = getattr(file, "name", "")
        
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        stripped = _clean_pdf_text(text)
        if stripped:
            pages.append({
                "page": i,
                "text": stripped,
                "source_name": source_name,
            })
    return pages


def load_uploaded_file(uploaded_file) -> str | list[dict[str, object]]:
    if uploaded_file is None:
        return ""

    name = _entry_name(uploaded_file)
    suffix = Path(name).suffix.lower()
    
    if suffix in _DOC_EXTENSIONS and suffix != ".pdf":
        return load_txt(uploaded_file)
    if suffix == ".pdf":
        from testgen.rag.pdf_sources import get_source_rules, filter_pdf_pages
        pages = load_pdf_pages(uploaded_file, source_name=name)
        rules = get_source_rules(name)
        rules["source_name"] = name
        kept_pages, _, _ = filter_pdf_pages(pages, rules)
        return kept_pages
    raise ValueError(f"Loại tệp không được hỗ trợ: {suffix}. Chỉ chấp nhận các định dạng text và pdf.")


def load_text_uploaded_file(uploaded_file) -> str:
    return _decode_text(_read_file_bytes(uploaded_file))


def _load_entries(uploaded_files, loader: Callable[[Any], Any]) -> list[tuple[str, Any]]:
    entries: list[tuple[str, Any]] = []
    for uploaded_file in _as_files(uploaded_files):
        content = loader(uploaded_file)
        if isinstance(content, str):
            content = content.strip()
            if not content:
                continue
        elif not content:
            continue
        entries.append((_entry_name(uploaded_file), content))
    return entries


def load_uploaded_file_entries(uploaded_files) -> list[tuple[str, str]]:
    return _load_entries(uploaded_files, load_uploaded_file)


def load_text_uploaded_file_entries(uploaded_files) -> list[tuple[str, str]]:
    return _load_entries(uploaded_files, load_text_uploaded_file)


def load_uploaded_files(uploaded_files) -> str:
    entries = load_uploaded_file_entries(uploaded_files)
    if not entries:
        return ""
    return "\n\n---\n\n".join(f"# Tài liệu: {name}\n\n{text}" for name, text in entries)


def _safe_stem(name: str) -> str:
    cleaned = _SAFE_NAME_PATTERN.sub("_", name).strip("._")
    return cleaned or "uploaded_file"


def _delete_legacy_hashed_duplicates(storage_dir: Path, stem: str, suffix: str) -> None:
    pattern = re.compile(rf"^{re.escape(stem)}_[0-9a-f]{{12}}{re.escape(suffix)}$", re.IGNORECASE)
    for existing_path in storage_dir.iterdir():
        if existing_path.is_file() and pattern.match(existing_path.name):
            existing_path.unlink()


def persist_uploaded_doc_files(uploaded_files, storage_dir: Path) -> list[Path]:
    files = _as_files(uploaded_files)
    if not files:
        return []

    storage_dir.mkdir(parents=True, exist_ok=True)
    persisted: list[Path] = []

    for uploaded_file in files:
        file_name = Path(_entry_name(uploaded_file))
        suffix = file_name.suffix.lower()
        if suffix not in _DOC_EXTENSIONS:
            continue

        data = _read_file_bytes(uploaded_file)
        if not data:
            continue

        safe_stem = _safe_stem(file_name.stem)
        target_path = storage_dir / f"{safe_stem}{suffix}"

        _delete_legacy_hashed_duplicates(storage_dir, safe_stem, suffix)
        target_path.write_bytes(data)
        persisted.append(target_path)

    return persisted


def delete_saved_doc_file(storage_dir: Path, file_name: str | Path) -> bool:
    storage_dir.mkdir(parents=True, exist_ok=True)
    target_path = storage_dir / Path(file_name).name
    if target_path.suffix.lower() not in _DOC_EXTENSIONS:
        return False
    if not target_path.exists() or not target_path.is_file():
        return False

    storage_root = storage_dir.resolve()
    resolved_target = target_path.resolve()
    if resolved_target.parent != storage_root:
        return False

    resolved_target.unlink()
    return True


def list_saved_doc_files(storage_dir: Path) -> list[Path]:
    if not storage_dir.exists() or not storage_dir.is_dir():
        return []
    files = [path for path in storage_dir.iterdir() if path.is_file() and path.suffix.lower() in _DOC_EXTENSIONS]
    return sorted(files, key=lambda item: item.name.lower())


def _read_saved_doc_text(file_path: Path) -> str:
    if file_path.suffix.lower() != ".pdf":
        return file_path.read_text(encoding="utf-8-sig", errors="replace")
    return load_pdf(file_path.read_bytes())


def load_saved_doc_entries(storage_dir: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for file_path in list_saved_doc_files(storage_dir):
        try:
            text = _read_saved_doc_text(file_path)
        except Exception:
            continue
        stripped = text.strip()
        if not stripped:
            continue
        entries.append((file_path.name, stripped))
    return entries

