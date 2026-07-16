# Changelog, Thống kê & Ghi chú phát triển

> Cập nhật lần cuối: Version 1.5

---

## Thống kê

### Số lượng code (thực tế, đo bằng số dòng)

| File | Dòng code |
|------|-----------|
| main.py (entry) | 49 dòng |
| core/constants.py | 31 dòng |
| core/geometry.py | 127 dòng |
| core/steel_types.py | 112 dòng |
| data/data_manager.py | 144 dòng |
| gui/dialogs.py | 56 dòng |
| gui/styles.py | 159 dòng |
| gui/tabs/calc_tab.py | 366 dòng |
| gui/tabs/lookup_tab.py | 197 dòng |
| gui/widgets/image_box.py | 51 dòng |
| **Tổng (không tính __init__.py rỗng)** | **~1.292 dòng** |

### Số lượng loại thép hỗ trợ

- **Tính toán:** 8 loại (5 loại hỗ trợ góc bo: I/H, U/C, Angle, RHS/SHS, T-Section)
- **Tra cứu:** 4 thư viện (I lib, U lib, HINH_VN, Ong,Hop)

### Dependencies

- Python 3.14.x
- PySide6==6.11.1 (Qt for Python)
- openpyxl==3.1.5

---

## Lịch sử thay đổi

### Version 1.5 (Current)

- ✅ **Cải thiện GUI responsive** (giải quyết known-issue cũ): thêm `resizeEvent` + `_update_input_font()` trong `calc_tab.py` tự động scale font input (9–13pt) theo chiều rộng cửa sổ; dùng `QSplitter` với `setStretchFactor`; `left_widget.setMinimumWidth(320)`.
- ✅ **Cải thiện error handling Excel** (giải quyết known-issue cũ): `DataManager` validate các sheet bắt buộc (`I lib`, `U lib`, `HINH_VN`, `Ong,Hop`), `skip_headers()` tự động bỏ qua header rows, `clean_weight()` xử lý giá trị rỗng / `---`, try/except quanh load, fallback về `[]` nếu lỗi.
- ✅ **JSON caching đã hoạt động đúng** (giải quyết known-issue cũ): `load_data()` ưu tiên đọc `steel_db.json`, fallback sang Excel rồi lưu lại JSON; Lookup tab hiển cảnh báo rõ ràng nếu Excel chưa load được.
- ✅ **Cập nhật dependencies & docs** cho khớp với code thực tế (V1.5).

### Version 1.4

- ✅ **Tái cấu trúc toàn bộ codebase**: tách `main.py` (~1200 dòng) thành 12 file module hóa; xóa file rác; cấu trúc `core/` `data/` `gui/` `docs/`.
- Cải thiện Excel loading: skip header rows tự động; load được 964 records từ 4 thư viện thép.

### Version 1.3

- ✅ **Rounded Corner Calculations (Góc bo)**: thêm trường r1 (Corner Radius) mặc định 0, hỗ trợ 5 loại thép.
- ✅ **Silent Data Loading**; Bug Fixes v1.3.1.

### Version 1.2

- ✅ **JSON Caching System**; Unit Conversion Enhancement (thêm đơn vị m).

### Version 1.1

- ✅ Menu Help (About + User Guide); Unit conversion (mm/cm/inch); Validation; Logging; tooltip; Quantity.

### Version 1.0 (Initial Release)

- ✅ Bộ tính toán thủ công 8 loại thép; Tra cứu 4 thư viện; Giao diện Qt; Đóng gói .exe; Hình vẽ kỹ thuật.

---

## TODO List

### Ngắn hạn (1-2 tuần)

- [ ] Thêm unit test cho các công thức tính toán (tests/test_geometry.py, ...)

### Trung hạn (1-2 tháng)

- [ ] Dark mode support (hiện chỉ có 1 stylesheet light trong `styles.py`)
- [ ] Cải thiện error handling Excel (validate cấu trúc cột cụ thể hơn)

### Dài hạn (3-6 tháng)

- [ ] Xuất báo cáo (Excel/PDF)
- [ ] Lưu lịch sử tính toán
- [ ] Multi-language support (EN/VI)
- [ ] Thêm loại thép mới (Built-up, Custom section)

---

## Ghi chú phát triển

### Cách chạy tool

```bash
pip install -r requirements.txt
python main.py
```

### Đóng gói thành .exe

```bash
pyinstaller --onefile --windowed --add-data "STEEL TYPE png;STEEL TYPE png" --add-data "alias.xlsx;." --add-data "steel_db.json;." main.py
```

### Cấu trúc file JSON (steel_db.json)

```json
{
  "profiles": [
    { "type": "ih", "D": "...", "E": "...", "F": "...", "N": "...", "O": "..." },
    { "type": "hinh_vn", "D": "...", "B": "...", "C": "..." }
  ],
  "metadata": {
    "total_records": 964,
    "source": "alias.xlsx",
    "saved_at": "2024-07-16"
  }
}
```
