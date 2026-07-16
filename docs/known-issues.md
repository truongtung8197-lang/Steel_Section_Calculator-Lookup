# Known Issues & Lỗi đã biết

> Cập nhật lần cuối: Version 1.3.2

---

## 1. File steel_db.json không được sử dụng

- **Mô tả:** File `steel_db.json` được tạo bởi `xlsx_to_json.py` nhưng `main.py` đọc trực tiếp từ Excel
- **Ảnh hưởng:**
  - Tốn thời gian đọc Excel mỗi lần khởi động
  - Có thể gây lỗi nếu Excel đang mở bởi ứng dụng khác

## 2. Xử lý lỗi Excel chưa robust

- **Vị trí:** `main.py`
- **Mô tả:**
  - Chỉ catch exception chung và in ra console
  - Không thông báo rõ ràng cho người dùng nếu file Excel bị lỗi
  - Không validate cấu trúc sheet trước khi đọc
- **Ảnh hưởng:** Người dùng không biết lỗi xảy ra nếu Excel bị hỏng

## 3. Không có unit test

- **Mô tả:** Chưa có test suite để kiểm tra các công thức tính toán
- **Ảnh hưởng:** Khó phát hiện lỗi khi sửa đổi code

## 4. Giao diện chưa responsive tốt

- **Mô tả:**
  - Kích thước cửa sổ cố định (1150x750)
  - Splitter ratios cố định có thể không phù hợp với mọi màn hình
- **Ảnh hưởng:** Trải nghiệm người dùng trên màn hình nhỏ hoặc lớn

## 5. Lỗi tiềm ẩn với QDoubleValidator

- **Vị trí:** `main.py`
- **Mô tả:** Validator chỉ cho phép số dương từ 0.001 đến 999999.0, có thể gây lỗi nếu người dùng nhập giá trị lớn hơn
- **Ảnh hưởng:** Không thể tính toán cho kích thước lớn (>999999 mm)

## 6. GUI không responsive khi resize cửa sổ

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
