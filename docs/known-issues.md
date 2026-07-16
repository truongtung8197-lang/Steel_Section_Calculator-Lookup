# Danh sách lỗi (Known Issues) & Bài học kinh nghiệm

*Cập nhật lần cuối: 16/07/2026 (Version 1.6)*

File này ghi nhận các vấn đề phát sinh, trạng thái xử lý và các bài học kỹ thuật cốt lõi để AI Agent tuân thủ trong quá trình phát triển dự án.

---

## ✅ Các lỗi đã giải quyết (Resolved)

1. **File `steel_db.json` không được sử dụng hiệu quả**
   * *Mô tả:* Ứng dụng luôn đọc file Excel trực tiếp gây chậm.
   * *Giải pháp v1.5:* `DataManager.load_data()` ưu tiên đọc JSON cache, chỉ fallback sang Excel khi JSON lỗi/thiếu, sau đó tự cập nhật lại JSON.

2. **Xử lý lỗi Excel thiếu an toàn (Robustness)**
   * *Mô tả:* Lỗi cấu trúc file Excel dễ gây crash ứng dụng.
   * *Giải pháp v1.5:* `data_manager.py` tự động kiểm tra 5 sheet bắt buộc, dùng `skip_headers()` bỏ qua dòng tiêu đề, `clean_weight()` xử lý các ký tự lạ (`---`, ô trống), bọc khối lệnh trong `try/except` và fallback về danh sách rỗng `[]` kèm cảnh báo trên giao diện.

3. **Giao diện co giãn (Responsive) chưa tốt**
   * *Mô tả:* Font chữ và khung nhập liệu bị vỡ, tràn viền hoặc quá nhỏ khi thay đổi kích thước cửa sổ.
   * *Giải pháp v1.5:* Sử dụng `QSplitter` với tỷ lệ giãn nở `setStretchFactor`, đặt chiều rộng tối thiểu cho khung nhập liệu `left_widget.setMinimumWidth(320)`. Viết đè `resizeEvent()` để gọi `_update_input_font()` tự động scale font chữ động từ 9pt đến 13pt. Khung vẽ kỹ thuật `ImageBox` tự động render lại hình ảnh theo kích thước mới.

---

## ❌ Các lỗi chưa giải quyết (Open Issues)

### A. Thiếu hệ thống Unit Test (Ưu tiên cao)

* *Hiện trạng:* Chưa có test suite tự động kiểm tra tính chính xác của các công thức hình học (`core/geometry.py`) và các hàm kiểm tra dữ liệu đầu vào.
* *Kế hoạch:* Tạo thư mục `tests/` chứa `test_geometry.py` và `test_validators.py` chạy bằng `pytest`.

### B. Giới hạn nhập liệu của QDoubleValidator (Ưu tiên trung bình)

* *Hiện trạng:* Validator giới hạn nhập liệu từ `0.001` đến `999999.0` mm, khiến ứng dụng không xử lý được kích thước lớn hơn hoặc bằng $1000$ m.
* *Kế hoạch:* Mở rộng dải kiểm tra hoặc chuyển sang tự viết hàm kiểm tra giá trị (custom validation) trong sự kiện tính toán thay vì phụ thuộc hoàn toàn vào validator của Qt.

### C. Giao diện chỉ hỗ trợ Light Mode (Ưu tiên thấp)

* *Hiện trạng:* File `gui/styles.py` chỉ định nghĩa duy nhất một bảng mã màu sáng.
* *Kế hoạch:* Phát triển thêm giao diện tối (Dark Mode) và cơ chế chuyển đổi trực tiếp trên menu bar.

### D. Xung đột chiếm dụng file Excel (Ưu tiên thấp)

* *Hiện trạng:* Nếu người dùng đang mở file `alias.xlsx` bằng Microsoft Excel, thư viện `openpyxl` có thể bị lỗi quyền truy cập (Permission Error) khi cố đọc ghi.
* *Kế hoạch:* Tối ưu hóa cơ chế mở file ở chế độ chỉ đọc (read-only) khi load dữ liệu thô.

### E. Giao diện About hiển thị sai phiên bản (Ưu tiên cao)

* *Hiện trạng:* Hàm `show_about()` trong `gui/dialogs.py` đang bị hardcode chuỗi `"v1.0"`, không tự động cập nhật khi ứng dụng lên v1.6.
* *Giải pháp v1.6:* Đưa biến `APP_VERSION = "1.6"` vào `core/constants.py` và import vào `gui/dialogs.py`. Năm cũng được thay bằng `datetime.now().year`.
* *Trạng thái:* **Resolved**

### F. Ngày cập nhật dữ liệu `saved_at` bị cố định (Ưu tiên cao)

* *Hiện trạng:* File `data_manager.py` lưu siêu dữ liệu JSON với ngày ghi cố định là `"2024-07-16"`.
* *Giải pháp v1.6:* Sử dụng thư viện `datetime` để tự động ghi nhận thời gian thực khi xuất cache JSON: `datetime.now().strftime("%Y-%m-%d")`.
* *Trạng thái:* **Resolved**

---

## 🧠 Bài học kinh nghiệm cho AI Agent (Lessons Learned)

> **⚠️ NGUYÊN TẮC BẮT BUỘC ĐỐI VỚI AI AGENT KHI ĐỌC/GHI CODE DỰ ÁN NÀY:**

* **LL-1 (Cấu trúc Module):** Tuyệt đối không gộp code ngược trở lại thành một file duy nhất. Giữ vững kiến trúc module độc lập (`core/` xử lý toán học, `data/` xử lý IO, `gui/` xử lý hiển thị). Khi cập nhật tính năng mới, chỉ tác động đúng file chịu trách nhiệm.
* **LL-2 (An toàn dữ liệu - Fallback IO):** Mọi thao tác đọc/ghi file bên ngoài (JSON, Excel, hình ảnh) **bắt buộc** phải nằm trong khối lệnh `try-except`. Phải luôn có phương án fallback (trả về danh sách rỗng, sử dụng dữ liệu mặc định) để tránh ứng dụng bị crash đột ngột.
* **LL-3 (Xử lý dữ liệu đầu vào sớm):** Các hàm kiểm tra tính hợp lệ (`check_*`) phải được đặt ngay tại layer tính toán toán học (`geometry.py`), thực hiện trước khi tính diện tích để cô lập lỗi logic (ví dụ: bề dày bụng thép không được lớn hơn chiều rộng cánh).
* **LL-4 (Không hardcode thông tin cấu hình):** Không hardcode các chuỗi phiên bản, ngày tháng, đường dẫn file hoặc hằng số toán học ở các file giao diện. Toàn bộ phải được quản lý tập trung tại `core/constants.py`.
* **LL-5 (Thiết kế giao diện linh hoạt):** Tránh sử dụng kích thước cố định (fixed size) cho widget. Luôn ưu tiên dùng `QSplitter`, `QLayout` và lắng nghe sự kiện `resizeEvent` để tính
