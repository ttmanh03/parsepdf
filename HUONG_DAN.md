# Hướng dẫn sử dụng: Chuyển PDF sang Markdown bằng AI

Tool này dùng GPT-4o để đọc file PDF (kể cả PDF scan, bảng biểu phức tạp) và chuyển thành file Markdown có cấu trúc rõ ràng.

---

## Yêu cầu

- Python **3.10** trở lên
- Git
- Tài khoản OpenAI có API key (có credit)

---

## Cài đặt lần đầu

### Bước 1 — Clone repo về máy

```bash
git clone https://github.com/TEN_USER/markitdown.git
cd markitdown
```

> Thay `TEN_USER` bằng username GitHub của người chia sẻ repo này.

### Bước 2 — Tạo môi trường ảo Python

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo:

- **Windows:**
  ```powershell
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

> Sau khi kích hoạt, terminal sẽ hiện `(.venv)` ở đầu dòng.

### Bước 3 — Cài thư viện

```bash
pip install -e "packages/markitdown[pdf]"
pip install openai python-dotenv
```

### Bước 4 — Tạo file `.env`

Tạo file tên `.env` ngay tại thư mục gốc của repo (cùng chỗ với file `pdf_convert_llm.py`):

```
OPENAI_API_KEY=sk-...your-key-here...
```

> Lấy API key tại: https://platform.openai.com/api-keys

---

## Cách dùng

### Chuyển 1 file PDF

```bash
python pdf_convert_llm.py duong/dan/den/file.pdf
```

Kết quả sẽ được lưu tự động vào thư mục `ketqua/` với tên tương ứng.

**Ví dụ:**

```bash
python pdf_convert_llm.py bao_cao_tai_chinh.pdf
# => Lưu ra: ketqua/bao_cao_tai_chinh.md
```

### Chuyển nhiều file PDF cùng lúc

**Windows (PowerShell):**
```powershell
Get-ChildItem *.pdf | ForEach-Object { python pdf_convert_llm.py $_.FullName }
```

**macOS / Linux:**
```bash
for f in *.pdf; do python pdf_convert_llm.py "$f"; done
```

---

## Lưu ý

- Mỗi trang PDF gửi lên GPT-4o sẽ tốn token — file dài sẽ tốn tiền hơn.
- File output là Markdown (`.md`), mở bằng VS Code, Obsidian, Typora, hoặc bất kỳ text editor nào.
- Nếu PDF chỉ có văn bản thuần (không bảng biểu, không scan), tool vẫn chạy được và nhanh hơn vì không gọi GPT-4o cho những trang đó.

---

## Lỗi thường gặp

| Lỗi | Cách sửa |
|-----|----------|
| `ModuleNotFoundError: openai` | Chạy lại `pip install openai python-dotenv` |
| `KeyError: OPENAI_API_KEY` | Kiểm tra file `.env` đã tạo đúng chưa, đúng thư mục chưa |
| `AuthenticationError` | API key sai hoặc hết hạn — kiểm tra lại trên OpenAI |
| `pdfplumber` không cài | Chạy lại `pip install -e "packages/markitdown[pdf]"` |
