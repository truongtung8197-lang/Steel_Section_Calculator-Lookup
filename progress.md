# Steel Management & Calculator Pro - Progress Documentation

## 📋 Tổng quan Tool

**Tên tool:** Steel Management & Calculator Pro  
**Phiên bản:** 1.3.2
**Công nghệ:** Python 3.x, PySide6 (Qt), openpyxl  
**Mục đích:** Công cụ tính toán khối lượng thép lý thuyết và tra cứu profile thép chuẩn từ file Excel

### Chức năng chính

#### 1. Tab "Manual Calculator" (Bộ tính toán thủ công)

- Tính khối lượng thép lý thuyết cho 8 loại hình cắt thép:
  - **Plate** (Tấm): Tính theo chiều dài × rộng × dày
  - **I Beam / H Beam** (Dầm I/H): Tính diện tích mặt cắt theo công thức hình học
  - **PFC / U Channel** (Thép hình U): Tính diện tích mặt cắt theo công thức hình học
  - **Angle / L Section** (Thép góc): Tính diện tích mặt cắt theo công thức hình học
  - **RHS / SHS** (Thép hộp): Tính diện tích mặt cắt theo công thức hình học
  - **CHS / Pipe** (Thép ống): Tính diện tích mặt cắt theo công thức hình học
  - **Rod / Round Bar** (Thép tròn): Tính diện tích mặt cắt theo công thức hình học
  - **T Section** (Thép chữ T): Tính diện tích mặt cắt theo công thức hình học

- **Đặc điểm:**
  - Tự động hiển thị hình vẽ kỹ thuật tham khảo cho từng loại thép
  - Tính khối lượng theo đơn vị kg/m hoặc kg tùy theo loại thép
  - Hỗ trợ nhập số lượng (Quantity) để tính tổng khối lượng
  - Nút "Copy Value" để sao chép kết quả tính toán
  - Nút "Clear" để xóa trắng các trường nhập liệu
  - Validation đầu vào với thông báo lỗi chi tiết theo từng loại thép
  - Hỗ trợ đổi đơn vị động (mm/cm/m/inch) với tự động convert giá trị
  - **Hỗ trợ tính toán với góc bo (r1)** cho I/H, U/C, Angle, RHS/SHS, T-Section
  - Menu Help với About dialog và User Guide chi tiết
  - Logging system ghi lại hoạt động vào file app.log

#### 2. Tab "Steel Section Lookup" (Tra cứu profile thép)

- Tra cứu thông tin profile thép từ file Excel `alias.xlsx`
- Hỗ trợ 4 thư viện thép:
  - **I Beam / H Beam** (Sheet: "I lib"): 5 cột D, E, F, N, O
  - **PFC / U Channel** (Sheet: "U lib"): 5 cột D, E, F, N, O
  - **Shape VN** (Sheet: "HINH_VN"): 3 cột A, B, C
  - **Pipe / Tube** (Sheet: "Ong,Hop"): 3 cột A, B, C

- **Đặc điểm:**
  - Tìm kiếm theo tên profile (hỗ trợ tìm kiếm từ khóa nhiều từ)
  - Hiển thị chi tiết thông tin profile đã chọn
  - Nút "Copy" cho từng trường thông tin để sao chép nhanh
  - Hiển thị khối lượng theo kg/m
  - Giao diện phân chia 2 panel: danh sách kết quả bên trái, chi tiết bên phải
  - Dropdown chọn thư viện thép động (I Beam, U Channel, Shape VN, Pipe/Tube)

### Cấu trúc File

```bash
APP STEEL LOOKUP/
├── main.py                    # File chính - Giao diện và logic
├── main.spec                  # File cấu hình PyInstaller (đóng gói .exe)
├── alias.xlsx                 # File Excel chứa database thép
├── steel_db.json              # File JSON cache (tự động tạo bởi tool)
├── xlsx_to_json.py            # Script convert Excel → JSON
├── SVG.py                     # Module xử lý SVG (chưa sử dụng)
├── U.svg                      # File SVG (chưa sử dụng)
├── build/                     # Thư mục build PyInstaller
├── STEEL TYPE png/            # Thư mục chứa hình vẽ kỹ thuật
│   ├── CHS.png
│   ├── I.png
│   ├── L.png
│   ├── PL.png
│   ├── RHS.png
│   ├── ROD.png
│   ├── T.png
│   └── U.png
└── progress.md                # File documentation
```

### Công thức tính toán

**Mật độ thép:** 7.85e-6 kg/mm³ (7850 kg/m³)

**Công thức diện tích mặt cắt (không góc bo):**

- **Plate:** A = Length × Width × Thickness
- **I Beam:** A = 2 × B × Tf + (H - 2 × Tf) × Tw
- **U Channel:** A = 2 × B × Tf + (H - 2 × Tf) × Tw
- **Angle:** A = t × (a + b - t)
- **RHS/SHS:** A = W × H - (W - 2t) × (H - 2t)
- **CHS:** A = π/4 × (OD² - (OD - 2t)²)
- **Rod:** A = π × D² / 4
- **T Section:** A = B × Tf + (H - Tf) × Tw

**Công thức diện tích mặt cắt (có góc bo r1):**

- **I Beam:** A = 2BT_f + (H-2T_f)T_w + (π-2)r₁²
- **U Channel:** A = 2BT_f + (H-2T_f)T_w + 2(π-2)r₁²
- **Angle:** A = t(a+b-t) + (π/4-1/2)r₁²
- **RHS/SHS:** A = WH - (W-2t)(H-2t) - (4-π)(R_o²-R_i²)
- **T Section:** A = BT_f + (H-T_f)T_w + 2(π-2)r₁²

**Khối lượng:** Weight = Area × Length × Density

### Cấu hình đường dẫn

- Tool tự động phát hiện đường dẫn base directory khi chạy từ:
  - File .exe đã đóng gói (PyInstaller)
  - File .py source code
- Các đường dẫn quan trọng:
  - `BASE_DIR`: Thư mục chứa file thực thi
  - `PNG_DIR`: Thư mục chứa hình vẽ kỹ thuật
  - `EXCEL_PATH`: Đường dẫn file alias.xlsx
  - `JSON_PATH`: Đường dẫn file steel_db.json (cache)

---

## ⚠️ Các lỗi đã biết

### 1. File steel_db.json không được sử dụng

- **Mô tả:** File `steel_db.json` được tạo bởi `xlsx_to_json.py` nhưng `main.py` đọc trực tiếp từ Excel
- **Ảnh hưởng:**
  - Tốn thời gian đọc Excel mỗi lần khởi động
  - Có thể gây lỗi nếu Excel đang mở bởi ứng dụng khác

### 2. Xử lý lỗi Excel chưa robust

- **Vị trí:** `main.py` dòng 420-470
- **Mô tả:**
  - Chỉ catch exception chung và in ra console
  - Không thông báo rõ ràng cho người dùng nếu file Excel bị lỗi
  - Không validate cấu trúc sheet trước khi đọc
- **Ảnh hưởng:** Người dùng không biết lỗi xảy ra nếu Excel bị hỏng

### 3. Không có unit test

- **Mô tả:** Chưa có test suite để kiểm tra các công thức tính toán
- **Ảnh hưởng:** Khó phát hiện lỗi khi sửa đổi code

### 4. Giao diện chưa responsive tốt

- **Mô tả:**
  - Kích thước cửa sổ cố định (1150x750)
  - Splitter ratios cố định có thể không phù hợp với mọi màn hình
- **Ảnh hưởng:** Trải nghiệm người dùng trên màn hình nhỏ hoặc lớn

### 5. Lỗi tiềm ẩn với QDoubleValidator

- **Vị trí:** `main.py` dòng 267-268
- **Mô tả:** Validator chỉ cho phép số dương từ 0.001 đến 999999.0, có thể gây lỗi nếu người dùng nhập giá trị lớn hơn
- **Ảnh hưởng:** Không thể tính toán cho kích thước lớn (>999999 mm)

### 6. GUI không responsive khi resize cửa sổ

- **Mô tả:**
  - Cửa sổ chỉ có thể resize về 1 mức cố định (minimum size 950x650)
  - Khi thu nhỏ cửa sổ, các ô nhập liệu trở nên rất nhỏ và không thể đọc/nhập được
  - Font size không tự động scale theo kích thước cửa sổ
  - Các hình PNG tham khảo có thể gây cản trở layout khi resize
- **Nguyên nhân:**
  - Thiếu cơ chế responsive scaling
  - Minimum size quá lớn so với không gian có sẵn
  - Font size cố định (11pt) không điều chỉnh theo window size
- **Ảnh hưởng:** Trải nghiệm người dùng kém khi làm việc với cửa sổ nhỏ hoặc màn hình có độ phân giải thấp

---

## 🚀 Các cải tiến dự kiến

### Ưu tiên Cao (High Priority)

#### 1. Cải thiện validation và error messages

- **Lý do:** Đã có validation chi tiết với thông báo lỗi thân thiện
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Thêm hàm `get_validation_error_message()` với thông báo chi tiết cho từng loại thép
  - Validation logic phù hợp với từng loại hình cắt
  - Hiển thị thông báo lỗi màu đỏ trên giao diện

#### 2. Thêm unit conversion system

- **Lý do:** Đã hỗ trợ đổi đơn vị mm/cm/m/inch
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Thêm dropdown đơn vị cho từng trường nhập liệu
  - Tự động convert giá trị khi thay đổi đơn vị
  - Hàm `on_unit_changed()` xử lý conversion logic
  - Constants: `UNIT_CONVERSION = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "inch": 25.4}`

#### 3. Thêm Help system và tooltip

- **Lý do:** Đã có menu Help với About và User Guide
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Menu "Help" với "About" dialog hiển thị thông tin phiên bản
  - "User Guide" chi tiết với hướng dẫn sử dụng từng tab
  - Tooltip cho tất cả các trường nhập liệu và nút bấm
  - RichText format cho User Guide

#### 4. Thêm logging system

- **Lý do:** Đã có logging module ghi ra file
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Logging configuration với file `app.log`
  - Log level: INFO
  - Format: timestamp - level - message
  - Log các hoạt động: khởi động, tính toán, lỗi, validation

#### 5. Cải thiện error handling

- **Lý do:** Đã có error handling tốt hơn
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Try-catch blocks cho các operation chính
  - Message boxes rõ ràng cho người dùng
  - Logging đầy đủ cho debugging
  - Validation trước khi tính toán

#### 6. Sử dụng steel_db.json thay vì đọc Excel trực tiếp

- **Lý do:** Tăng tốc độ khởi động, giảm phụ thuộc vào Excel
- **Trạng thái:** ✅ Hoàn thành (Version 1.2)
- **Chi tiết:**
  - Tự động lưu data ra JSON sau khi đọc Excel
  - Lần khởi động sau đọc từ JSON (nhanh hơn)
  - Fallback mechanism nếu JSON bị lỗi
  - Hàm `load_data()` và `save_to_json()`

#### 7. Cải thiện validation messages

- **Lý do:** Thông báo lỗi rõ ràng, thân thiện
- **Trạng thái:** ✅ Hoàn thành
- **Chi tiết:**
  - Hàm `get_validation_error_message()` với messages chi tiết
  - Hiển thị lỗi theo từng loại thép cụ thể
  - Màu sắc rõ ràng: đỏ cho lỗi, xanh cho kết quả

#### 8. Thêm tính năng góc bo (rounded corners)

- **Lý do:** Tính toán chính xác hơn cho thép có góc bo
- **Trạng thái:** ✅ Hoàn thành (Version 1.3)
- **Chi tiết:**
  - Thêm trường nhập liệu r1 (Corner Radius) với giá trị mặc định 0
  - Hỗ trợ 5 loại thép: I/H Beam, U Channel, Angle, RHS/SHS, T-Section
  - Công thức tính toán diện tích mặt cắt có góc bo theo tiêu chuẩn
  - Validation r1: 0 ≤ r1 ≤ min(Tw, Tf)/2 hoặc r1 ≤ Thickness
  - Tự động convert đơn vị cho r1 (mm/cm/inch)

### Ưu tiên Thấp (Low Priority)

#### 9. Thêm tính năng xuất báo cáo

- **Lý do:** Tiện lợi cho người dùng cần lưu trữ
- **Cách thực hiện:**
  - Export kết quả tính toán ra Excel/PDF
  - Export danh sách profile đã tra cứu

#### 10. Thêm tính năng lưu lịch sử tính toán

- **Lý do:** Tiện lợi cho người dùng cần tra cứu lại
- **Cách thực hiện:**
  - Lưu các phép tính gần đây vào file
  - Hiển thị dropdown chọn lại các phép tính cũ

#### 11. Dark mode support

- **Lý do:** Giảm mỏi mắt khi sử dụng lâu
- **Cách thực hiện:**
  - Thêm toggle dark/light mode
  - Tạo stylesheet riêng cho dark mode

#### 12. Multi-language support

- **Lý do:** Hỗ trợ người dùng quốc tế
- **Cách thực hiện:**
  - Tách text ra file resource
  - Hỗ trợ tiếng Anh và tiếng Việt

#### 13. Thêm loại thép mới

- **Lý do:** Mở rộng tính năng
- **Có thể thêm:**
  - Steel Plate với các kích thước chuẩn
  - Built-up sections
  - Custom section (cho phép người dùng tự nhập diện tích)

---

## 📊 Thống kê

### Số lượng code

- **main.py:** 950+ dòng
- **xlsx_to_json.py:** 258 dòng
- **Tổng:** ~1200 dòng code

### Số lượng loại thép hỗ trợ

- **Tính toán:** 8 loại (5 loại hỗ trợ góc bo)
- **Tra cứu:** 4 thư viện

### Dependencies

- Python 3.x
- PySide6 (Qt for Python)
- openpyxl
- PyInstaller (để đóng gói .exe)

---

## 🔄 Lịch sử thay đổi

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

## 📝 Ghi chú phát triển

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

### Cấu trúc Excel (alias.xlsx)

**Sheet "I lib" và "U lib":**

- Cột D: Tên profile
- Cột E: Tên section gốc
- Cột F: Khối lượng kg/m (original)
- Cột N: Tên section thay thế
- Cột O: Khối lượng kg/m (substitute)

**Sheet "HINH_VN" và "Ong,Hop":**

- Cột A: Tên profile
- Cột B: Khối lượng kg/m
- Cột C: Ghi chú

### Cấu trúc JSON (steel_db.json)

```json
{
  "profiles": [...],
  "metadata": {
    "total_records": 123,
    "source": "alias.xlsx",
    "saved_at": "2024-07-16"
  }
}
```

Mỗi record có các trường:

- **Type 1 (ih, channel):** type, D, E, F, N, O
- **Type 2 (hinh_vn, ong_hop):** type, D, B, C

---

## 👤 Thông tin liên hệ

**Developer:** [Tên developer]  
**Ngày tạo:** 2024  
**License:** [License info]

---

## 📌 TODO List

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

**Last Updated:** 2024-07-16  
**Version:** 1.3.2  
**Maintained by:** Development Team
