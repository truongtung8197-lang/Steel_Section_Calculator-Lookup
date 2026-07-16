# Roadmap & Cải tiến dự kiến

> Cập nhật lần cuối: Version 1.3.2

---

## Ưu tiên Cao (High Priority)

### 1. Cải thiện validation và error messages

- **Lý do:** Đã có validation chi tiết với thông báo lỗi thân thiện
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Thêm hàm `get_validation_error_message()` với thông báo chi tiết cho từng loại thép
  - Validation logic phù hợp với từng loại hình cắt
  - Hiển thị thông báo lỗi màu đỏ trên giao diện

### 2. Thêm unit conversion system

- **Lý do:** Đã hỗ trợ đổi đơn vị mm/cm/m/inch
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Thêm dropdown đơn vị cho từng trường nhập liệu
  - Tự động convert giá trị khi thay đổi đơn vị
  - Hàm `on_unit_changed()` xử lý conversion logic
  - Constants: `UNIT_CONVERSION = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "inch": 25.4}`

### 3. Thêm Help system và tooltip

- **Lý do:** Đã có menu Help với About và User Guide
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Menu "Help" với "About" dialog hiển thị thông tin phiên bản
  - "User Guide" chi tiết với hướng dẫn sử dụng từng tab
  - Tooltip cho tất cả các trường nhập liệu và nút bấm
  - RichText format cho User Guide

### 4. Thêm logging system

- **Lý do:** Đã có logging module ghi ra file
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Logging configuration với file `app.log`
  - Log level: INFO
  - Format: timestamp - level - message
  - Log các hoạt động: khởi động, tính toán, lỗi, validation

### 5. Cải thiện error handling

- **Lý do:** Đã có error handling tốt hơn
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Try-catch blocks cho các operation chính
  - Message boxes rõ ràng cho người dùng
  - Logging đầy đủ cho debugging
  - Validation trước khi tính toán

### 6. Sử dụng steel_db.json thay vì đọc Excel trực tiếp

- **Lý do:** Tăng tốc độ khởi động, giảm phụ thuộc vào Excel
- **Trạng thái:** ✅ Hoàn thành (Version 1.2)
- **Chi tiết:**
  - Tự động lưu data ra JSON sau khi đọc Excel
  - Lần khởi động sau đọc từ JSON (nhanh hơn)
  - Fallback mechanism nếu JSON bị lỗi
  - Hàm `load_data()` và `save_to_json()`

### 7. Cải thiện validation messages

- **Lý do:** Thông báo lỗi rõ ràng, thân thiện
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Hàm `get_validation_error_message()` với messages chi tiết
  - Hiển thị lỗi theo từng loại thép cụ thể
  - Màu sắc rõ ràng: đỏ cho lỗi, xanh cho kết quả

### 8. Thêm tính năng góc bo (rounded corners)

- **Lý do:** Tính toán chính xác hơn cho thép có góc bo
- **Trạng thái:** ✅ Hoàn thành (Version 1.3)
- **Chi tiết:**
  - Thêm trường nhập liệu r1 (Corner Radius) với giá trị mặc định 0
  - Hỗ trợ 5 loại thép: I/H Beam, U Channel, Angle, RHS/SHS, T-Section
  - Công thức tính toán diện tích mặt cắt có góc bo theo tiêu chuẩn
  - Validation r1: I/U: 0 ≤ r1 ≤ min((B-Tw)/2, (H-2·Tf)/2); T: 0 ≤ r1 ≤ min((B-Tw)/2, (H-Tf)/2); Angle: 0 ≤ r1 ≤ min(LegA, LegB)/2; SHS/RHS: T ≤ r1 ≤ min(B, H)/2. Tất cả kích thước > 0.
  - Tự động convert đơn vị cho r1 (mm/cm/inch)

---

## Ưu tiên Thấp (Low Priority)

### 9. Thêm tính năng xuất báo cáo

- **Lý do:** Tiện lợi cho người dùng cần lưu trữ
- **Cách thực hiện:**
  - Export kết quả tính toán ra Excel/PDF
  - Export danh sách profile đã tra cứu

### 10. Thêm tính năng lưu lịch sử tính toán

- **Lý do:** Tiện lợi cho người dùng cần tra cứu lại
- **Cách thực hiện:**
  - Lưu các phép tính gần đây vào file
  - Hiển thị dropdown chọn lại các phép tính cũ

### 11. Dark mode support

- **Lý do:** Giảm mỏi mắt khi sử dụng lâu
- **Cách thực hiện:**
  - Thêm toggle dark/light mode
  - Tạo stylesheet riêng cho dark mode

### 12. Multi-language support

- **Lý do:** Hỗ trợ người dùng quốc tế
- **Cách thực hiện:**
  - Tách text ra file resource
  - Hỗ trợ tiếng Anh và tiếng Việt

### 13. Thêm loại thép mới

- **Lý do:** Mở rộng tính năng
- **Có thể thêm:**
  - Steel Plate với các kích thước chuẩn
  - Built-up sections
  - Custom section (cho phép người dùng tự nhập diện tích)

---

## Tái cấu trúc code (Technical Debt)

### 14. Tách main.py thành nhiều module

- **Lý do:** File hiện tại ~1200 dòng, khó bảo trì
- **Cấu trúc đề xuất:**

  ```
  steel_app/
  ├── main.py                    # Entry point (~20 dòng)
  ├── core/
  │   ├── constants.py           # DENSITY_FACTOR, UNIT_CONVERSION, paths
  │   ├── steel_types.py         # SteelType dataclass + STEEL_TYPES list
  │   └── geometry.py            # Hàm area_*, check_* cho từng loại
  ├── data/
  │   └── excel_loader.py        # Load Excel, save/load JSON
  ├── gui/
  │   ├── styles.py              # Stylesheet riêng
  │   ├── widgets/
  │   │   └── image_box.py       # ImageBox class
  │   ├── tabs/
  │   │   ├── calculator_tab.py  # Tab 1
  │   │   └── lookup_tab.py      # Tab 2
  │   └── dialogs/
  │       ├── about_dialog.py
  │       └── help_dialog.py
  └── tests/
      ├── test_geometry.py
      ├── test_validators.py
      └── test_excel_loader.py
  ```

- **Lợi ích:**
  - Dễ bảo trì, mỗi file chỉ giữ 1 nhiệm vụ
  - Dễ mở rộng, thêm loại thép mới không cần sửa file chính
  - Dễ test, có thể import riêng business logic
  - Dễ phân công công việc cho nhiều người
  - Dễ tái sử dụng code cho CLI tool, API backend
