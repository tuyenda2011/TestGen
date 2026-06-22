import os
import sys
from pathlib import Path

# Thêm src vào PYTHONPATH để có thể import các module của testgen
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from testgen.rag.document_loader import load_pdf_pages
from testgen.rag.pdf_sources import get_source_rules, filter_pdf_pages

def main():
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    docs_dir = ROOT_DIR / "docs" / "rag_seed_pdfs"
    if not docs_dir.exists():
        print(f"Error: {docs_dir} không tồn tại.")
        return

    pdf_files = list(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print("Không tìm thấy file .pdf nào trong thư mục.")
        return

    for pdf_file in pdf_files:
        print(f"\nĐang xử lý: {pdf_file.name}...")
        
        # 1. Đọc PDF thành các trang
        with open(pdf_file, "rb") as f:
            pages = load_pdf_pages(f, source_name=pdf_file.name)
        if not pages:
            print("  -> Không đọc được text hoặc file rỗng.")
            continue
            
        print(f"  -> Đọc được {len(pages)} trang. Đang lọc rác...")
        
        # 2. Lấy rules và lọc rác
        rules = get_source_rules(pdf_file.name)
        rules["source_name"] = pdf_file.name
        kept_pages, kept_count, dropped_count = filter_pdf_pages(pages, rules)
        
        if kept_count == 0:
            print("  -> Bị lọc bỏ 100%. Không sinh file core.")
            continue
            
        # 3. Ghi ra file Markdown
        out_name = f"{pdf_file.stem}_core.md"
        out_path = docs_dir / out_name
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# TÀI LIỆU CỐT LÕI (Rút gọn từ {pdf_file.name})\n\n")
            f.write(f"> **Tổng quan**: Giữ lại {kept_count} trang, lọc bỏ {dropped_count} trang dư thừa (changelog, index, license...).\n\n")
            
            for p in kept_pages:
                f.write(f"\n\n## --- Trang {p.get('page', '?')} ---\n\n")
                f.write(str(p.get("text", "")))
                
        print(f"  -> HOÀN THÀNH. Đã lưu cốt lõi vào: {out_name} ({kept_count}/{len(pages)} trang)")

if __name__ == "__main__":
    main()
