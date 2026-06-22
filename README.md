# testgen-chatbot

Ứng dụng Streamlit multi-agent để sinh, chạy và rà soát mã kiểm thử từ yêu cầu, tài liệu, source code và test code đầu vào.

## Cấu trúc

```text
app.py                  # launcher cho streamlit run app.py
src/testgen/            # source ứng dụng chính
src/testgen/agents/     # requirement, planning, generator, reviewer, pytest executor
src/testgen/rag/        # document loading, chunking, vector store, retriever
prompts/                # prompt template có thể chỉnh mà không đụng package
tests/                  # pytest regression tests
outputs/                # file xuất và lịch sử chạy
.runtime/               # ChromaDB runtime, tự sinh và bị ignore
```

## Cài đặt

1. Cài Python 3.10+ và Ollama.
2. Kéo model local:

```bash
ollama pull qwen2.5:7b
ollama pull llama3.1:8b
ollama pull qwen2.5-coder:7b
ollama pull deepseek-coder:6.7b
ollama pull nomic-embed-text
```

3. Cài thư viện:

```bash
pip install -r requirements.txt
```

4. Tạo cấu hình local nếu cần:

```bash
cp .env.example .env
```

5. Chạy ứng dụng:

```bash
streamlit run app.py
```

## Cấu hình model

Model mặc định nằm trong `src/testgen/core/config.py` và có thể override bằng biến môi trường hoặc chọn lại trong sidebar.

- Requirement: `qwen2.5:7b`
- Test Planning: `llama3.1:8b`
- Code Generator: `qwen2.5-coder:7b`
- Code Review: `deepseek-coder:6.7b`
- Embedding: `nomic-embed-text`

OpenRouter chỉ xử lý chat/completion. Nếu bật RAG mà không dùng Gemini embedding, hệ thống vẫn cần Ollama embedding local với `nomic-embed-text`.

Không commit API key thật. Với Streamlit, ưu tiên nhập Gemini/OpenRouter key trong sidebar. Run history chỉ lưu metadata đã sanitize, không lưu API key.

## Demo nhanh

Bộ demo hoàn chỉnh nằm ở `examples/demo/`.

- Source mẫu: `examples/demo/sample_source.py`
- Requirement mẫu: `examples/demo/requirements.md`
- Hướng dẫn từng bước: `examples/demo/streamlit_demo_guide.md`
- Output/report mẫu: `examples/demo/sample_outputs/`

Chạy demo:

```bash
streamlit run app.py
```

Nếu muốn phần retry theo coverage hiện rõ khi thuyết trình, đặt ngưỡng coverage demo trước khi chạy:

```powershell
$env:PYTEST_COVERAGE_THRESHOLD = "95"
streamlit run app.py
```

README trong `examples/demo/` ghi sẵn model khuyến nghị cho local Ollama và OpenRouter, các bước nạp source/requirement, cách chỉ ra AST, retry, coverage, review report và diagnostics.

## Hướng dẫn cấu hình & Chạy kiểm thử cho từng Framework

TestGen hỗ trợ sinh và chạy mã tự động cho nhiều framework khác nhau. Dưới đây là yêu cầu môi trường local bắt buộc để hệ thống có thể thực thi (Run Executor) thành công:

### 1. Pytest (Python)
- **Môi trường:** Python 3.10+
- **Cài đặt:** `pip install pytest pytest-cov`
- **Hoạt động:** TestGen tự động phân tích coverage và chạy test thông qua môi trường Python hiện tại.

### 2. JUnit 5 (Java)
- **Môi trường:** Java JDK 11+ và Maven.
- **Cài đặt:** Dự án của bạn phải có sẵn `pom.xml` cấu hình JUnit 5 và plugin JaCoCo (nếu muốn lấy điểm coverage).
- **Hoạt động:** TestGen sẽ tự động tạo thư mục maven ảo, copy source code và chạy lệnh `mvn test`.

### 3. Jest (JavaScript)
- **Môi trường:** Node.js (v14+) và `npm`.
- **Cài đặt:** Cần cài đặt Jest trong thư mục gốc hoặc chạy lệnh `npm install --save-dev jest jest-environment-jsdom`.
- **Hoạt động:** TestGen sẽ gọi `npx jest` hoặc `npm test` để thu thập coverage và parse JSON kết quả.

### 4. Selenium (Python - E2E Testing)
- **Môi trường:** Python 3.10+
- **Cài đặt:** `pip install pytest selenium`
- **Lưu ý:** Nếu tệp kiểm thử gọi vào UI của web local, bạn phải đảm bảo web app đang chạy ở dưới nền. Mặc định TestGen sinh mã dùng `webdriver.Edge()` nên máy cần có trình duyệt MS Edge.

### 5. Playwright (Python - E2E Testing)
- **Môi trường:** Python 3.10+
- **Cài đặt:** 
  - `pip install pytest-playwright`
  - Chạy lệnh `playwright install` trên Terminal để tải các trình duyệt.
- **Lưu ý:** Tương tự Selenium, web app mục tiêu phải đang ở trạng thái chạy (nếu test nội bộ).

### 6. Postman / Newman (API Testing)
- **Môi trường:** Node.js
- **Cài đặt:** Cài đặt Newman global bằng lệnh: `npm install -g newman`
- **Lưu ý:** Newman đóng vai trò là client gửi request. Ứng dụng API server của bạn **bắt buộc phải đang chạy** (ví dụ: đang bật ở `http://localhost:8000`) để Newman có thể gọi và kiểm tra HTTP status code hoặc schema.
- **Chạy Demo API Server Local:** Để thử nghiệm sinh test Postman, bạn có thể bật API Server mẫu tích hợp sẵn bằng lệnh:
  ```bash
  python examples/demo/postman/local_api_server/order_pricing_api_server.py
  ```
  Khi thấy thông báo `Postman demo API listening on http://localhost:8000`, bạn có thể yên tâm dùng TestGen để sinh và chạy tệp kiểm thử Postman cho API này.

## Kiểm thử

```bash
python -m pytest -q
```

Trên máy Windows đang dùng conda env `chatbot`:

```powershell
cmd /c "call D:\Miniconda\Scripts\activate.bat chatbot && python -m pytest -q"
```

CI cơ bản nằm ở `.github/workflows/tests.yml` và chạy `python -m pytest -q`.

## Benchmark

Kiểm kê bộ nguồn benchmark cố định và xuất `BENCHMARK_REPORT.md`:

```bash
python benchmark.py
```

Chạy benchmark qua pipeline thật:

```bash
python benchmark.py --execute --mode OpenRouter --api-key <OPENROUTER_API_KEY>
```

## Luồng chính

1. Nạp tài liệu hoặc source code.
2. Chunk và index vào ChromaDB, kèm metadata source/section/line range.
3. Requirement Agent trích xuất JSON yêu cầu.
4. Test Planning Agent tạo test plan và tự repair JSON schema khi model trả sai dạng phổ biến.
5. Function Prompt Builder dựng prompt động theo hàm/class/branch/exception từ AST.
6. Code Generator Agent gọi LLM sinh test code theo framework.
7. Pytest Executor kiểm tra `pytest --collect-only`, sau đó chạy test sinh ra và đo coverage.
8. Nếu test pass nhưng coverage thiếu, hệ thống retry theo function chứa missing lines và chạy combined coverage.
9. Pytest Executor phân loại lỗi execution (`syntax_error`, `wrong_expected_value`, `low_coverage`, ...).
10. Code Review Agent tạo báo cáo.
11. Formatter lưu code, Excel, PDF, combined coverage report và raw coverage JSON vào `outputs/runs`.

ChromaDB được lưu ở `.runtime/chroma` và có thể xóa an toàn khi cần tạo lại index.

## Khắc phục sự cố (Troubleshooting)

### Lỗi hiển thị Tiếng Việt trên Windows (UnicodeEncodeError)
Khi AI sinh mã kiểm thử với các comment giải thích bằng tiếng Việt, plugin `inline-snapshot` của pytest có thể bị crash khi in ra màn hình Console mặc định của Windows do lỗi mã hóa (`UnicodeEncodeError: 'charmap' codec can't encode character...`), khiến hệ thống báo lỗi `pytest pass=False` (dù code test chạy thành công 100%).

**Cách khắc phục:** Thiết lập biến môi trường để ép Windows Terminal sử dụng mã UTF-8 trước khi khởi chạy ứng dụng.

Nếu dùng **PowerShell** (Mặc định trong VSCode):
```powershell
$env:PYTHONIOENCODING="utf-8"
streamlit run app.py
```

Nếu dùng **Command Prompt (cmd)**:
```cmd
set PYTHONIOENCODING=utf-8
streamlit run app.py
```

*(Mẹo: Bạn có thể cấu hình `PYTHONIOENCODING=utf-8` vào file `.env` hoặc System Environment Variables của Windows để áp dụng vĩnh viễn).*
