# Steel Management & Calculator Pro - Progress Documentation

## 📋 Tổng quan Tool

**Tên tool:** Steel Management & Calculator Pro  
**Phiên bản:** 1.0  
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
  - Validation đầu vào: chỉ cho phép nhập số dương

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

### Cấu trúc File

```
APP STEEL LOOKUP/
├── main.py                    # File chính - Giao diện và logic
├── main.spec                  # File cấu hình PyInstaller (đóng gói .exe)
├── alias.xlsx                 # File Excel chứa database thép
├── steel_db.json              # File JSON export từ Excel (tạo bởi xlsx_to_json.py)
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
└── progress.md                # File documentation (đang tạo)
```

### Công thức tính toán

**Mật độ thép:** 7.85e-6 kg/mm³ (7850 kg/m³)

**Công thức diện tích mặt cắt:**
- **Plate:** A = Length × Width × Thickness
- **I Beam:** A = 2 × B × Tf + (H - 2 × Tf) × Tw
- **U Channel:** A = 2 × B × Tf + (H - 2 × Tf) × Tw
- **Angle:** A = t × (a + b - t)
- **RHS/SHS:** A = W × H - (W - 2t) × (H - 2t)
- **CHS:** A = π/4 × (OD² - (OD - 2t)²)
- **Rod:** A = π × D² / 4
- **T Section:** A = B × Tf + (H - Tf) × Tw

**Khối lượng:** Weight = Area × Length × Density

### Cấu hình đường dẫn

- Tool tự động phát hiện đường dẫn base directory khi chạy từ:
  - File .exe đã đóng gói (PyInstaller)
  - File .py source code
- Các đường dẫn quan trọng:
  - `BASE_DIR`: Thư mục chứa file thực thi
  - `PNG_DIR`: Thư mục chứa hình vẽ kỹ thuật
  - `EXCEL_PATH`: Đường dẫn file alias.xlsx

---

## ⚠️ Các lỗi đã biết

### 1. Validation chưa hoàn chỉnh
- **Vị trí:** `main.py` dòng 66, 72, 78, 84, 90, 96
- **Mô tả:** Các hàm `check_*` chỉ validate điều kiện cơ bản, chưa validate:
  - Giá trị âm hoặc bằng 0 (trừ Length có validator riêng)
  - Thứ tự logic giữa các kích thước (ví dụ: Tw phải nhỏ hơn B)
- **Ảnh hưởng:** Có thể tính ra kết quả không chính xác nếu người dùng nhập sai logic

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

### 4. File steel_db.json không được sử dụng
- **Mô tả:** File `steel_db.json` được tạo bởi `xlsx_to_json.py` nhưng `main.py` đọc trực tiếp từ Excel
- **Ảnh hưởng:** 
  - Tốn thời gian đọc Excel mỗi lần khởi động
  - Có thể gây lỗi nếu Excel đang mở bởi ứng dụng khác

### 5. Giao diện chưa responsive tốt
- **Mô tả:** 
  - Kích thước cửa sổ cố định (1150x750)
  - Splitter ratios cố định có thể không phù hợp với mọi màn hình
- **Ảnh hưởng:** Trải nghiệm người dùng trên màn hình nhỏ hoặc lớn

### 6. Thiếu tooltip và hướng dẫn
- **Mô tả:** 
  - Không có tooltip giải thích các trường nhập liệu
  - Không có hướng dẫn sử dụng
- **Ảnh hưởng:** Người dùng mới có thể không biết cách sử dụng

### 7. Không hỗ trợ đổi đơn vị
- **Mô tả:** Tất cả đầu vào đều dùng mm và m, không có tùy chọn đổi đơn vị
- **Ảnh hưởng:** Người dùng phải tự convert đơn vị nếu có data ở inch hoặc feet

### 8. Lỗi tiềm ẩn với QDoubleValidator
- **Vị trí:** `main.py` dòng 267-268
- **Mô tả:** Validator chỉ cho phép số dương từ 0.001 đến 999999.0, có thể gây lỗi nếu người dùng nhập giá trị lớn hơn
- **Ảnh hưởng:** Không thể tính toán cho kích thước lớn (>999999 mm)

---

## 🚀 Các cải tiến dự kiến

### Ưu tiên Cao (High Priority)

#### 1. Sử dụng steel_db.json thay vì đọc Excel trực tiếp
- **Lý do:** Tăng tốc độ khởi động, giảm phụ thuộc vào Excel
- **Cách thực hiện:**
  - Kiểm tra file JSON có tồn tại và mới hơn Excel không
  - Nếu có, đọc từ JSON
  - Nếu không, đọc từ Excel và tạo JSON mới
- **Lợi ích:** 
  - Khởi động nhanh hơn
  - Không bị lỗi nếu Excel đang mở
  - Có thể cache data

#### 2. Thêm unit test cho các công thức tính toán
- **Lý do:** Đảm bảo tính chính xác của công thức
- **Cách thực hiện:**
  - Tạo file `test_calculations.py`
  - Test các công thức với giá trị known
  - Test các edge cases (kích thước nhỏ, lớn)
- **Lợi ích:** Dễ dàng refactor và mở rộng mà không sợ break functionality

#### 3. Cải thiện error handling và logging
- **Lý do:** Dễ debug và hỗ trợ người dùng tốt hơn
- **Cách thực hiện:**
  - Thêm logging module thay vì print
  - Log ra file `app.log`
  - Hiển thị message box rõ ràng khi có lỗi
  - Validate cấu trúc Excel trước khi đọc

### Ưu tiên Trung bình (Medium Priority)

#### 4. Thêm tooltip và hướng dẫn sử dụng
- **Lý do:** Cải thiện UX cho người dùng mới
- **Cách thực hiện:**
  - Thêm tooltip cho các trường nhập liệu
  - Thêm menu "Help" hoặc nút "?" với hướng dẫn
  - Thêm placeholder text rõ ràng hơn

#### 5. Hỗ trợ đổi đơn vị
- **Lý do:** Linh hoạt hơn cho người dùng quốc tế
- **Cách thực hiện:**
  - Thêm dropdown chọn đơn vị (mm/cm/inch)
  - Tự động convert giá trị nhập
  - Hiển thị đơn vị rõ ràng trên kết quả

#### 6. Cải thiện validation
- **Lý do:** Ngăn ngừa lỗi người dùng
- **Cách thực hiện:**
  - Thêm validation logic chi tiết hơn
  - Hiển thị message rõ ràng khi validation fail
  - Thêm range check phù hợp với từng loại thép

#### 7. Responsive design
- **Lý do:** Tương thích tốt hơn với các kích thước màn hình khác nhau
- **Cách thực hiện:**
  - Lưu và restore window size/position
  - Điều chỉnh layout tự động theo kích thước
  - Thêm minimum size hợp lý

### Ưu tiên Thấp (Low Priority)

#### 8. Thêm tính năng xuất báo cáo
- **Lý do:** Tiện lợi cho người dùng cần lưu trữ
- **Cách thực hiện:**
  - Export kết quả tính toán ra Excel/PDF
  - Export danh sách profile đã tra cứu

#### 9. Thêm tính năng lưu lịch sử tính toán
- **Lý do:** Tiện lợi cho người dùng cần tra cứu lại
- **Cách thực hiện:**
  - Lưu các phép tính gần đây vào file
  - Hiển thị dropdown chọn lại các phép tính cũ

#### 10. Dark mode support
- **Lý do:** Giảm mỏi mắt khi sử dụng lâu
- **Cách thực hiện:**
  - Thêm toggle dark/light mode
  - Tạo stylesheet riêng cho dark mode

#### 11. Multi-language support
- **Lý do:** Hỗ trợ người dùng quốc tế
- **Cách thực hiện:**
  - Tách text ra file resource
  - Hỗ trợ tiếng Anh và tiếng Việt

#### 12. Thêm loại thép mới
- **Lý do:** Mở rộng tính năng
- **Có thể thêm:**
  - Steel Plate với các kích thước chuẩn
  - Built-up sections
  - Custom section (cho phép người dùng tự nhập diện tích)

---

## 📊 Thống kê

### Số lượng code
- **main.py:** 741 dòng
- **xlsx_to_json.py:** 258 dòng
- **Tổng:** ~1000 dòng code

### Số lượng loại thép hỗ trợ
- **Tính toán:** 8 loại
- **Tra cứu:** 4 thư viện

### Dependencies
- Python 3.x
- PySide6 (Qt for Python)
- openpyxl
- PyInstaller (để đóng gói .exe)

---

## 🔄 Lịch sử thay đổi

### Version 1.0 (Current)
- ✅ Hoàn thành bộ tính toán thủ công 8 loại thép
- ✅ Hoàn thành tính năng tra cứu 4 thư viện thép
- ✅ Giao diện Qt với stylesheet đẹp mắt
- ✅ Hỗ trợ đóng gói thành .exe
- ✅ Hình vẽ kỹ thuật tham khảo
- ✅ Chức năng copy kết quả

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
  "ih": [...],
  "channel": [...],
  "hinh_vn": [...],
  "ong_hop": [...]
}
```

Mỗi record có các trường:
- **Type 1 (ih, channel):** name, original_section, weight, substitute_section, substitute_weight
- **Type 2 (hinh_vn, ong_hop):** name, weight, note

---

## 👤 Thông tin liên hệ

**Developer:** [Tên developer]  
**Ngày tạo:** 2024  
**License:** [License info]

---

## 📌 TODO List

### Ngắn hạn (1-2 tuần)
- [ ] Sử dụng steel_db.json thay vì đọc Excel trực tiếp
- [ ] Thêm unit test cho các công thức tính toán
- [ ] Cải thiện error handling và logging

### Trung hạn (1-2 tháng)
- [ ] Thêm tooltip và hướng dẫn sử dụng
- [ ] Hỗ trợ đổi đơn vị
- [ ] Cải thiện validation
- [ ] Responsive design

### Dài hạn (3-6 tháng)
- [ ] Thêm tính năng xuất báo cáo
- [ ] Lưu lịch sử tính toán
- [ ] Dark mode support
- [ ] Multi-language support
- [ ] Thêm loại thép mới

---

**Last Updated:** 2024-07-16  
**Maintained by:** Development Team