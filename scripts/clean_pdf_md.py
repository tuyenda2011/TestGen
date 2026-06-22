import re
from pathlib import Path

def clean_md_file(file_path):
    print(f"Cleaning: {file_path.name}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_len = len(content)

    # Các mẫu regex cần xóa
    patterns = [
        re.compile(r"^## --- Trang \d+ ---$", re.MULTILINE),
        re.compile(r"^\(continues on next page\)$", re.MULTILINE),
        re.compile(r"^pytest Documentation, Release [\d\.]+$", re.MULTILINE),
        re.compile(r"^JUnit 5 User Guide$", re.MULTILINE),
        re.compile(r"^Table of Contents$", re.MULTILINE),
        re.compile(r"^\d+\s*CONTENTS$", re.MULTILINE),
        re.compile(r"^CONTENTS\s*\d+$", re.MULTILINE),
        re.compile(r"^\d+$", re.MULTILINE), # Các trang số độc lập
    ]

    for p in patterns:
        content = p.sub("", content)

    # Nối các đoạn code bị gãy (```python \n \n ...)
    # Xóa các dòng trống thừa mứa
    content = re.sub(r"\n{3,}", "\n\n", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f" -> Done. Size reduced from {original_len} to {len(content)} chars.\n")

if __name__ == "__main__":
    docs_dir = Path(r"D:\Chatbot\docs\rag_seed_pdfs")
    
    # Chỉ dọn các file có hậu tố _core.md sinh ra từ PDF
    files_to_clean = [
        "coveragepy_official_core.md",
        "junit5_user_guide_official_core.md",
        "pytest_cov_official_core.md",
        "pytest_official_core.md"
    ]
    
    for f_name in files_to_clean:
        f_path = docs_dir / f_name
        if f_path.exists():
            clean_md_file(f_path)
        else:
            print(f"Không tìm thấy {f_name}")
