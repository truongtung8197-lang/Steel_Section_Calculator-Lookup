# Changelog, Thống kê & Ghi chú phát triển

> Cập nhật lần cuối: Version 1.3.2

---

## Thống kê

### Số lượng code

| File | Dòng code |
|------|-----------|
| main.py | 950+ dòng |
| xlsx_to_json.py | 258 dòng |
| **Tổng** | **~1200 dòng** |

### Số lượng loại thép hỗ trợ

- **Tính toán:** 8 loại (5 loại hỗ trợ góc bo)
- **Tra cứu:** 4 thư viện

### Dependencies

- Python 3.x
- PySide6 (Qt for Python)
- openpyxl
- PyInstaller (để đóng gói .exe)

---

## Lịch sử thay đổi

### Version 1.0 (Initial Release)

- ✅ Bộ tính toán thủ công 8 loại thép cơ bản
- ✅ Tính năng tra cứu 4 thư viện thép từ Excel
- ✅ Giao diện Qt cơ bản
- ✅ Hỗ trợ đóng gói thành .exe
- ✅ Hình vẽ kỹ thuật tham khảo

### Version 1.1 - Updated 2024-07-16

- ✅ Menu Help với About dialog và User Guide chi tiết
- ✅ Unit conversion system (mm/cm/inch) với auto-convert
- ✅ Validation chi tiết với error messages thân thiện theo từng loại thép
- ✅ Logging system ghi ra file app.log
- ✅ Tooltip và hướng dẫn sử dụng toàn diện
- ✅ Quantity field để tính tổng khối lượng
- ✅ Giao diện Qt với stylesheet đẹp mắt, modern design

### Version 1.2 - Updated 2024-07-16

- ✅ **JSON Caching System**: Tự động lưu và đọc data từ steel_db.json
  - Tăng tốc độ khởi động (không cần đọc Excel mỗi lần)
  - Giảm phụ thuộc vào Excel file
  - Fallback mechanism nếu JSON bị lỗi
- ✅ **Unit Conversion Enhancement**: Thêm đơn vị mét (m)
  - Hỗ trợ đầy đủ: mm, cm, m, inch
  - Tự động convert giá trị khi thay đổi đơn vị
  - Áp dụng cho tất cả các trường nhập liệu

### Version 1.3 (Current) - Updated 2024-07-16

- ✅ **Rounded Corner Calculations (Góc bo)**
  - Thêm trường r1 (Corner Radius) với giá trị mặc định 0
  - Hỗ trợ 5 loại thép: I/H Beam, U Channel, Angle, RHS/SHS, T-Section
  - Công thức tính toán diện tích mặt cắt có góc bo:
    - I/H: A = 2BT_f + (H-2T_f)T_w + (π-2)r₁²
    - U/C: A = 2BT_f + (H-2T_f)T_w + 2(π-2)r₁²
    - Angle: A = t(a+b-t) + (π/4-1/2)r₁²
    - RHS/SHS: A = WH - (W-2t)(H-2t) - (4-π)(R_o²-R_i²)
    - T-Section: A = BT_f + (H-T_f)T_w + 2(π-2)r₁²
  - Validation r1 theo từng loại thép
  - Unit conversion cho r1 (mm/cm/inch)
- ✅ **Silent Data Loading**
  - Bỏ QMessageBox thông báo load data
  - Chỉ log ra console/file app.log
  - Khởi động nhanh hơn, không cần click OK
- ✅ **Bug Fixes v1.3.1**
  - Fix lỗi corner radius không cập nhật khối lượng (field name mismatch "Corner Radius" → "r1")
  - Fix padding input fields: tăng padding từ 8px 12px → 10px 14px để text không bị che mất
  - Fix window resize: bỏ Qt.WindowMinimizeButtonHint flag (đã mặc định có sẵn)
  - Fix missing **main** block: thêm entry point để tool có thể chạy được
- ✅ **Known Issues v1.3.2**
  - GUI không responsive khi resize: input fields quá nhỏ khi thu nhỏ cửa sổ
  - Font size không tự động scale theo window size
  - Cần thêm cơ chế responsive scaling trong medium term

---

## TODO List

### Ngắn hạn (1-2 tuần)

- [x] ~~Sử dụng steel_db.json thay vì đọc Excel trực tiếp~~ → ✅ Hoàn thành v1.2
- [ ] Thêm unit test cho các công thức tính toán
- [x] ~~Cải thiện error handling và logging~~ → ✅ Hoàn thành
- [x] ~~Thêm tooltip và hướng dẫn sử dụng~~ → ✅ Hoàn thành
- [x] ~~Hỗ trợ đổi đơn vị~~ → ✅ Hoàn thành (bao gồm m)
- [x] ~~Cải thiện validation~~ → ✅ Hoàn thành
- [x] ~~Thêm tính năng góc bo (rounded corners)~~ → ✅ Hoàn thành v1.3

### Trung hạn (1-2 tháng)

- [ ] Thêm unit test cho calculations
- [ ] Cải thiện error handling Excel
- [ ] **Fix GUI responsive resize:**
  - Cửa sổ thu nhỏ được nhưng input fields quá nhỏ không đọc được
  - Font size không tự động scale theo window size
  - Cần thêm cơ chế responsive scaling cho layout

### Dài hạn (3-6 tháng)

- [ ] Thêm tính năng xuất báo cáo
- [ ] Lưu lịch sử tính toán
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Thêm loại thép mới

---

## Ghi chú phát triển

### Cách chạy tool

**Chạy từ source code:**

```bash
python main.py
```

**Đóng gói thành .exe:**

```bash
pyinstaller main.spec
```

**Convert Excel sang JSON:**

```bash
python xlsx_to_json.py
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
