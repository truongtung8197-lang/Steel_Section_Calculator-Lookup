# 🧮 Phần Mềm Tính Khối Lượng & Tra Cứu Thép Định Hình

## ✨ Các tính năng chính

### 1. Bộ tính toán thủ công (Manual Calculator)

* **Hỗ trợ đầy đủ 8 loại thép phổ dụng:** Thép tấm (Plate), Thép I/H, Thép U (PFC), Thép V/L (Angle), Thép hộp (RHS/SHS), Thép ống tròn (CHS), Thép tròn đặc (Rod) và Thép chữ T (T-Section).
* **Giao diện nhập liệu thông minh:** Biểu mẫu tự động thay đổi các trường nhập dữ liệu (Chiều cao, rộng, dày...) tương ứng ngay khi bạn chọn loại hình dáng thép, giúp tối ưu không gian hiển thị.
* **Bản vẽ kỹ thuật động (Dynamic Shapes):** Hình vẽ mặt cắt tự động co giãn trực quan theo thời gian thực.
  * *Chế độ hiển thị mẫu (Sample Mode):* Hiển thị ký hiệu hình học (H, B, Tw, Tf...) khi chưa nhập đủ thông số.
  * *Chế độ kích thước thực (Normal Mode):* Tự động điền thông số thực tế trực tiếp lên bản vẽ ngay khi nhập đủ dữ liệu.
* **Tính toán bo góc ($r_1$) chuyên sâu:** Hỗ trợ tính chính xác phần diện tích/khối lượng hao hụt hoặc cộng thêm do các góc bo tròn nội/ngoại đối với các dòng thép hình phức tạp.
* **Chuyển đổi đơn vị linh hoạt:** Hỗ trợ nhập kích thước theo nhiều hệ đo lường (`mm`, `cm`, `m`, `inch`) và tự động quy đổi đồng bộ.

### 2. Tra cứu barem thép tiêu chuẩn (Steel Section Lookup)

* **Tìm kiếm thông minh:** Bộ lọc đa từ khóa hỗ trợ tìm kiếm nhanh theo tên ký hiệu thanh thép (ví dụ: `I200`, `H150`, `U100`).
* **Thư viện dữ liệu phong phú:** Tra cứu tức thì từ 4 kho dữ liệu chuẩn: Thép hình I/H, Thép hình U, Thép tiêu chuẩn Việt Nam (Shape VN), ống và hộp định hình sẵn.
* **Gợi ý vật liệu thay thế:** Hiển thị song song thông tin biên dạng nguyên bản và biên dạng thay thế tương đương giúp tối ưu hóa công tác tìm kiếm vật liệu trong đấu thầu.

---

## 🚀 Hướng dẫn sử dụng nhanh

### 🔹 Cách tính khối lượng thép bất kỳ

1. Tại tab **Manual Calculator**, chọn loại hình dáng thép cần tính từ danh sách thả xuống.
2. Lựa chọn đơn vị đo lường phù hợp (Mặc định hệ thống là `mm`).
3. Tiến hành nhập các thông số hình học hiển thị trên form (Phần mềm sẽ tự động hiển thị hình vẽ minh họa tương ứng).
4. Nhập thêm **Chiều dài (Length)** và **Số lượng (Quantity)** để tính tổng khối lượng tổng thể.
5. Nhấp nút **Copy Value** để sao chép nhanh kết quả khối lượng vào bộ nhớ tạm để paste sang Excel, Word. Nhấp **Clear** để làm sạch các trường dữ liệu cho lượt tính tiếp theo.

### 🔹 Cách tra cứu barem thép từ thư viện

1. Chuyển sang tab **Steel Section Lookup**.
2. Lựa chọn bảng Thư viện thép cần tra cứu tại ô danh sách thả xuống.
3. Nhập ký hiệu thép vào ô tìm kiếm, danh sách kết quả phù hợp sẽ lọc tự động ở panel bên trái.
4. Nhấp chọn vào mã thép cụ thể, toàn bộ thông số hình học chi tiết, trọng lượng tiêu chuẩn ($kg/m$) và vật liệu thay thế tương đương sẽ hiển thị đầy đủ ở bảng bên phải.

---

## 🛠️ Yêu cầu hệ thống & Cài đặt (Dành cho Kỹ thuật viên)

Ứng dụng được phát triển trên nền tảng Python hiện đại, đảm bảo tính gọn nhẹ và hiệu năng cao.

### Yêu cầu môi trường

* Python 3.14.x
* PySide6 == 6.11.1 (Thư viện đồ họa Qt)
* openpyxl == 3.1.5 (Bộ đọc/ghi file Excel dữ liệu)

### Các bước cài đặt mã nguồn

1. Tải toàn bộ thư mục dự án về máy tính.
2. Cài đặt các thư viện phụ thuộc bắt buộc thông qua Terminal/Command Prompt:

   ```bash
   pip install -r requirements.txt
3. Khởi chạy ứng dụng:

    ```
    python main.py
    ```

⚠️ Lưu ý quan trọng: Để tính năng tra cứu hoạt động ổn định, tuyệt đối không di chuyển hoặc đổi tên file dữ liệu gốc alias.xlsx ra khỏi thư mục chứa file chạy chính (main.py). Hệ thống sẽ tự động khởi tạo file bộ nhớ đệm steel_db.json trong lần chạy đầu tiên để tăng tốc độ truy xuất cho những lần sau.

---
