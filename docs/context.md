# Steel Management & Calculator Pro - Tổng quan mã nguồn

## Công nghệ & Thư viện sử dụng
- **Ngôn ngữ**: Python 3.14.x
- **Giao diện người dùng**: PySide6 (Qt)
- **Xử lý dữ liệu Excel**: openpyxl

## Kiến trúc tính năng chính

### 1. Bộ tính toán thủ công (Manual Calculator)
Tính toán khối lượng thép lý thuyết theo thời gian thực cho 8 loại hình dạng mặt cắt:
- **Thép tấm (Plate)**: Chiều dài × Chiều rộng × Độ dày
- **Thép hình I/H (I Beam / H Beam)**
- **Thép hình U (PFC / U Channel)**
- **Thép góc (Angle / L Section)**
- **Thép hộp (RHS / SHS)**
- **Thép ống (CHS / Pipe)**
- **Thép tròn đặc (Rod / Round Bar)**
- **Thép chữ T (T Section)**

**Đặc điểm vận hành:**
- **Giao diện động**: Các trường nhập liệu tự động thay đổi (rebuild) phù hợp với hình dạng thép được chọn.
- **Bản vẽ kỹ thuật động (Dynamic Shapes)**: Tự động vẽ mặt cắt hình học bằng QPainter. Khi thiếu thông số, hệ thống hiển thị hình mẫu kèm ký hiệu (Sample mode); khi nhập đủ, hệ thống chuyển sang chế độ hiển thị thông số thực.
- **Xử lý bo góc ($r_1$)**: Hỗ trợ tính toán và hiển thị cung bo tròn mịn cho 5 loại mặt cắt: I/H, U/C, Angle, RHS/SHS, T-Section.
- **Tính năng bổ trợ**: Hỗ trợ đổi đơn vị nhanh (mm/cm/m/inch), nhập số lượng (Quantity) để tính tổng khối lượng, sao chép nhanh kết quả vào bộ nhớ tạm (Clipboard), và tự động co giãn font chữ khi thay đổi kích thước cửa sổ.

### 2. Tra cứu biên dạng thép (Steel Section Lookup)
Hệ thống tra cứu dữ liệu từ file bộ nhớ đệm `steel_db.json` hoặc đọc trực tiếp từ file dữ liệu gốc `alias.xlsx` khi không có bộ nhớ đệm.

**Cơ sở dữ liệu hỗ trợ:**
- **Thép I/H (Sheet "I lib")** & **Thép U (Sheet "U lib")**: Tra cứu tên, khối lượng nguyên bản, biên dạng thay thế tương đương.
- **Thép Shape VN (Sheet "HINH_VN")** & **Thép ống/hộp định hình (Sheet "Ong,Hop")**: Tra cứu tên, khối lượng chuẩn và ghi chú đi kèm.

---

## 📐 Công thức hình học chuẩn hóa

- Mật độ khối lượng của thép quy ước: $7.85 \times 10^{-6} \text{ kg/mm}^3$ (Tương đương $7850 \text{ kg/m}^3$).
- Công thức khối lượng tổng quát: 
$$\text{Khối lượng (kg)} = \text{Diện tích mặt cắt (mm}^2\text{)} \times \text{Chiều dài (m)} \times 0.00785$$

### 1. Diện tích mặt cắt không có góc bo ($A$)
- **Thép tấm (Plate)**: $A = \text{Width} \times \text{Thickness}$
- **Thép I/H**: $A = 2B \cdot T_f + (H - 2T_f)T_w$
- **Thép U/C**: $A = 2B \cdot T_f + (H - 2T_f)T_w$
- **Thép góc V/L**: $A = t(a + b - t)$
- **Thép hộp (RHS/SHS)**: $A = W \cdot H - (W - 2t)(H - 2t)$
- **Thép ống tròn (CHS)**: $A = \frac{\pi}{4}[OD^2 - (OD - 2t)^2]$
- **Thép tròn đặc (Rod)**: $A = \frac{\pi \cdot D^2}{4}$
- **Thép chữ T**: $A = B \cdot T_f + (H - T_f)T_w$

### 2. Diện tích mặt cắt có tính đến góc bo ($A_{fillet}$)
- **Thép I/H**: $A_{fillet} = A + (4 - \pi)r_1^2$ *(Cộng thêm diện tích 4 góc bo nội)*
- **Thép U/C**: $A_{fillet} = A + (2 - \frac{\pi}{2})r_1^2$ *(Cộng thêm diện tích 2 góc bo nội)*
- **Thép góc V/L**: $A_{fillet} = A + (1 - \frac{\pi}{4})r_1^2$ *(Cộng thêm diện tích 1 góc bo nội)*
- **Thép hộp (RHS/SHS)**: $A_{fillet} = W \cdot H - (W - 2t)(H - 2t) - (4 - \pi)(R_o^2 - R_i^2)$  
  *(Trong đó bán kính trong $R_i = r_1$, bán kính ngoài $R_o = r_1 + t$)*
- **Thép chữ T**: $A_{fillet} = A + (2 - \frac{\pi}{2})r_1^2$ *(Cộng thêm diện tích 2 góc bo nội)*

---

## 📂 Cấu trúc thư mục dự án
```text
Steel_Section_Calculator-Lookup/
|-- main.py                    # Điểm khởi chạy ứng dụng
|-- alias.xlsx                 # Cơ sở dữ liệu cấu kiện dạng Excel
|-- steel_db.json              # Bộ nhớ đệm dữ liệu (Tự động sinh)
|-- requirements.txt           # Danh sách thư viện phụ thuộc
|-- core/                      # Logic tính toán và hằng số hệ thống
|-- data/                      # Quản lý đọc/ghi và chuyển đổi dữ liệu
|-- gui/                       # Giao diện người dùng và đồ họa cấu kiện
|   |-- widgets/
|   |   |-- dynamic_shapes/    # Các thành phần vẽ mặt cắt động bằng QPainter
|-- docs/                      # Tài liệu dự án (progress.md, context.md, known-issues.md)