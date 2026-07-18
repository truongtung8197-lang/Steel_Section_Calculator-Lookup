# Tiến độ phát triển & Lộ trình (Progress & Roadmap)

## To-do list

### 🏗️ Kiến trúc & Hệ thống cốt lõi
- [x] Triển khai kiến trúc mô đun hóa chuẩn: `core/`, `data/`, `gui/`, `docs/`
- [x] Định nghĩa công thức diện tích mặt cắt cho 8 loại thép (hỗ trợ cả trường hợp có và không có góc bo $r_1$)
- [x] Xây dựng cơ chế fallback dữ liệu an toàn (JSON cache $\rightarrow$ Excel database, xử lý qua try-except)
- [x] Tích hợp hệ thống ghi nhật ký hoạt động vào file `app.log`
- [x] Sửa lỗi hardcode phiên bản (quản lý tập trung qua `APP_VERSION` trong `constants.py`)
- [x] Sửa lỗi thời gian `saved_at` cố định (chuyển sang cập nhật tự động bằng `datetime.now()`)
- [x] Thiết lập thư mục `tests/` với các bộ kiểm thử `test_geometry.py` và `test_data_manager.py`

### 💻 Giao diện & Tính năng người dùng
- [x] Tab Manual Calculator: Thiết lập các trường nhập liệu tự động thay đổi (rebuild_inputs), kiểm tra dữ liệu đầu vào và chuyển đổi đơn vị đo
- [x] Tab Steel Section Lookup: Hỗ trợ tra cứu thông tin biên dạng thép linh hoạt từ cơ sở dữ liệu Excel/JSON
- [x] Tích hợp tính năng tự động co giãn font chữ (9-13pt) dựa trên sự kiện thay đổi kích thước cửa sổ (`resizeEvent`)
- [x] Xây dựng Menu Help: Hiển thị hộp thoại About và tài liệu User Guide cho người dùng
- [x] Tối ưu hóa thứ tự hiển thị các trường nhập liệu trên giao diện: Di chuyển trường Chiều dài (`Length`) xuống sau bán kính bo góc ($r_1$)

### 🎨 Số hóa bản vẽ mặt cắt (Dynamic Shapes)
- [x] Loại bỏ hoàn toàn sự phụ thuộc vào ảnh PNG tĩnh, thay bằng các thành phần vẽ động (`QPainter`) phản hồi theo thời gian thực
- [x] Xây dựng lớp cơ sở `DynamicShapeWidget` để quản lý các thuộc tính vẽ chung
- [x] Hỗ trợ chế độ hiển thị mẫu (`Sample mode`): Vẽ hình minh họa kèm ký hiệu biên dạng (H, B, Tw, Tf...) khi người dùng chưa nhập đủ thông số
- [x] Sửa lỗi đồ họa hiển thị (Rendering bugs): 
  - Chuyển cơ chế đổ màu vùng thép sang dùng `QPainterPath` kết hợp `drawPath()`
  - Xóa nền chữ đo kích thước (`fillRect`) dựa theo kích thước thực của văn bản (`QFontMetrics`)
  - Chuyển mũi tên kích thước sang dạng đa giác đặc (`drawPolygon`) để tránh bị đứt nét
  - Thiết lập lề đo kích thước (`Dimension margin`) dựa trên pixel cố định sau khi quy đổi tọa độ widget
- [x] Hoàn thiện hiển thị hình học động cho cả 8 loại cấu kiện:
  - [x] **Thép góc (Angle / L)**: `DynamicLShape`
  - [x] **Thép hình U (PFC / U Channel)**: `DynamicUShape` (Sử dụng phương pháp tính điểm thủ công)
  - [x] **Thép hộp (RHS / SHS)**: `DynamicRHSShape` (Vẽ mặt cắt rỗng bao gồm cả biên trong và biên ngoài)
  - [x] **Thép ống (CHS / Pipe)**: `DynamicCHSShape` (Mặt cắt rỗng hình tròn)
  - [x] **Thép tròn (Rod / Round Bar)**: `DynamicRodShape` (Hình tròn đặc)
  - [x] **Thép tấm (Plate)**: `DynamicPlateShape` (Hình chữ nhật)
  - [x] **Thép hình I/H (I Beam / H Beam)**: `DynamicIShape` (Sửa lỗi hướng quét cung bo từ $90^\circ \rightarrow -90^\circ$ và bổ sung tham số `direction` bị thiếu)
  - [ ] **Thép chữ T (T Section)**: `DynamicTShape` (Đang sửa lỗi vạt góc ở cánh bên trái và đảo lại hướng bo góc lượn)

### 📝 Tài liệu kỹ thuật
- [x] Cập nhật các file tài liệu hướng dẫn và tiến độ trong thư mục `docs/` (`context.md`, `progress.md`, `known-issues.md`)