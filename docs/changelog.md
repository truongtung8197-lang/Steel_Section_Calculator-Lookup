# Changelog, Thống kê & Ghi chú phát triển

> Cập nhật lần cuối: Version 1.4

---

## Thống kê

### Số lượng code

| File | Dòng code |
|------|-----------|
| main.py (entry) | ~40 dòng |
| core/ (3 files) | ~250 dòng |
| data/data_manager.py | ~140 dòng |
| gui/ (5 files) | ~550 dòng |
| **Tổng** | **~980 dòng** |

### Số lượng loại thép hỗ trợ

- **Tính toán:** 8 loại (5 loại hỗ trợ góc bo)
- **Tra cứu:** 4 thư viện

### Dependencies

- Python 3.x
- PySide6 (Qt for Python)
- openpyxl

---

## Lịch sử thay đổi

### Version 1.4 (Current)

- ✅ **Tái cấu trúc toàn bộ codebase**
  - Tách `main.py` (~1200 dòng) → 12 file module hóa
  - Tách `progress.md` (456 dòng) → 4 file docs nhỏ
  - Xóa file rác: SVG.py, U.svg, main.spec, build/, xlsx_to_json.py, app.log
  - Cấu trúc mới: `core/` (business), `data/` (data), `gui/` (UI), `docs/` (tài liệu)
  - Cải thiện Excel loading: skip header rows tự động
  - Tất cả import hoạt động, load được 964 records từ 4 thư viện thép

### Version 1.3

- ✅ **Rounded Corner Calculations (Góc bo)**
  - Thêm trường r1 (Corner Radius) với giá trị mặc định 0
  - Hỗ trợ 5 loại thép: I/H Beam, U Channel, Angle, RHS/SHS, T-Section
- ✅ **Silent Data Loading** — Bỏ QMessageBox thông báo load data
- ✅ **Bug Fixes v1.3.1** — Fix corner radius, padding, window resize, entry point

### Version 1.2

- ✅ **JSON Caching System** — Tự động lưu và đọc data từ steel_db.json
- ✅ **Unit Conversion Enhancement** — Thêm đơn vị mét (m)

### Version 1.1

- ✅ Menu Help với About dialog và User Guide chi tiết
- ✅ Unit conversion system (mm/cm/inch) với auto-convert
- ✅ Validation chi tiết với error messages
- ✅ Logging system, tooltip, Quantity field

### Version 1.0 (Initial Release)

- ✅ Bộ tính toán thủ công 8 loại thép cơ bản
- ✅ Tính năng tra cứu 4 thư viện thép từ Excel
- ✅ Giao diện Qt cơ bản, hỗ trợ đóng gói .exe
- ✅ Hình vẽ kỹ thuật tham khảo

---

## TODO List

### Ngắn hạn (1-2 tuần)

- [ ] Thêm unit test cho các công thức tính toán

### Trung hạn (1-2 tháng)

- [ ] Fix GUI responsive resize (font scale, input fields quá nhỏ khi thu nhỏ)
- [ ] Cải thiện error handling Excel

### Dài hạn (3-6 tháng)

- [ ] Thêm tính năng xuất báo cáo
- [ ] Lưu lịch sử tính toán
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Thêm loại thép mới

---

## Ghi chú phát triển

### Cách chạy tool

```bash
python main.py
```

### Đóng gói thành .exe

```bash
pyinstaller --onefile --windowed --add-data "STEEL TYPE png;STEEL TYPE png" --add-data "alias.xlsx;." main.py
```

### Cấu trúc file JSON (steel_db.json)

```json
{
  "profiles": [...],
  "metadata": {
    "total_records": 123,
    "source": "alias.xlsx",
    "saved_at": "2024-07-16"
  }
}
