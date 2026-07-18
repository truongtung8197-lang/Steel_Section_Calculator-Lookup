# 🚀 Lộ trình Version 2.0 — Dynamic Technical Drawing

*Mục tiêu: Thay thế hoàn toàn file PNG tĩnh bằng hình vẽ động cập nhật theo thông số người dùng*

---

## 🧩 Kiến trúc tổng thể

```
gui/drawing/                       # Thư mục mới cho dynamic drawing
├── __init__.py
├── renderer.py                    # Công cụ vẽ chính (QPainter)
├── section_geometry.py            # Dữ liệu tọa độ mặt cắt cho từng loại thép
└── dimension.py                   # Vẽ dimension line + chú thích kích thước

gui/widgets/
├── image_box.py                   # GIỮ LẠI (rename sau) →  dynamic_drawing_widget.py (SỬA)
└── (các file khác giữ nguyên)

core/
├── geometry.py                    # GIỮ NGUYÊN (công thức tính diện tích)
├── steel_types.py                 # SỬA: thêm trường section_type thay vì image_file
└── (các file khác giữ nguyên)
```

---

## 📋 Checklist chi tiết

### Giai đoạn 1: Nền tảng vẽ (Prioritet: Cao nhất)

- [ ] **1.1** Tạo `gui/drawing/` với `__init__.py`
- [ ] **1.2** Viết `section_geometry.py` — định nghĩa tọa độ 2D mặt cắt cho từng loại thép
  - Plate (hình chữ nhật đơn giản), I/H (chữ I), U/C (chữ U), Angle (chữ L), RHS/SHS (hình hộp rỗng), CHS (hình tròn rỗng), Rod (hình tròn đặc), T (chữ T)
  - Mỗi loại thép là 1 hàm nhận các tham số kích thước, trả về danh sách `QPointF` (polygon path)
- [ ] **1.3** Viết `dimension.py` — vẽ dimension line (mũi tên 2 đầu + text kích thước)
  - `draw_dimension_horizontal(painter, x1, x2, y, value, unit)`
  - `draw_dimension_vertical(painter, x, y1, y2, value, unit)`
  - `draw_dimension_angled(painter, ...)` cho các cạnh xiên (nếu cần)
- [ ] **1.4** Viết `renderer.py` — class `DynamicRenderer` dùng `QPainter`
  - Nhận: loại thép (key), dict tham số kích thước, kích thước widget
  - Vẽ: mặt cắt tỷ lệ → dimension lines → chú thích kích thước
  - Tự động scale/tỉ lệ để vừa widget
  - `render(painter, width, height) -> None`

### Giai đoạn 2: Tích hợp vào GUI (Prioritet: Cao)

- [ ] **2.1** Sửa `gui/widgets/image_box.py` → `DynamicDrawingWidget`
  - Kế thừa `QWidget` thay vì `QLabel`
  - Override `paintEvent` → gọi `DynamicRenderer.render()`
  - Có property `steel_type` + `params` để trigger repaint
  - Giữ giao diện tương thích ngược (method: `set_image()` → redirect)
- [ ] **2.2** Sửa `core/steel_types.py`
  - Thêm trường `section_type: str` (key mapping đến hàm vẽ)
  - Có thể bỏ trường `image_file` hoặc để lại cho tương thích
- [ ] **2.3** Sửa `gui/tabs/calc_tab.py`
  - `rebuild_inputs()`: sau khi tạo input, gọi `drawing_widget.set_params(values)`
  - Kết nối signal `textChanged` của mỗi input → `drawing_widget.update()`
  - Bỏ dòng `self.image_box.set_image(img_path)`

### Giai đoạn 3: Chi tiết hóa bản vẽ (Prioritet: Trung bình)

- [ ] **3.1** Thêm hiển thị giá trị số trên hình vẽ (gần cạnh tương ứng)
- [ ] **3.2** Thêm hatch pattern cho phần diện tích thép (tùy chọn)
- [ ] **3.3** Thêm chú thích "r1" cho góc bo khi r1 > 0
- [ ] **3.4** Màu sắc: nền trắng, đường viền xanh đậm, chữ đen, dimension line đỏ/xanh

### Giai đoạn 4: Hoàn thiện & Tối ưu (Prioritet: Thấp)

- [ ] **4.1** Cache pixmap để tránh repaint lại mỗi lần resize (dùng double-buffer)
- [ ] **4.2** Anti-aliasing cho đường vẽ (đã có sẵn trong QPainter)
- [ ] **4.3** Kiểm tra tỷ lệ hiển thị hợp lý (nếu kích thước quá chênh lệch)
- [ ] **4.4** Xóa thư mục `STEEL TYPE png/` và các file PNG cũ
- [ ] **4.5** Cập nhật docs/progress.md + docs/known-issues.md

---

## 🎨 Chi tiết từng loại mặt cắt

### 1. Plate (Thép tấm)

```
┌──────────────────────┐  ← Width (mm)
│                      │  ↑
│     ████████████     │ Thickness (mm)
│                      │  ↓
└──────────────────────┘
```

- Vẽ: hình chữ nhật đặc
- Dimension: Width (ngang), Thickness (dọc)

### 2. I Beam / H Beam

```
       ← B →
    ┌────────┐  ──
    │        │   ↑ Tf
    └───┬─── ┘  ──
   ┌────┤        ← Tw (bụng)
   │    │
   └─── ┴───┐  ──
    │        │   ↑ Tf  (H)
    └────────┘  ──
```

- Vẽ: polygon hình chữ I
- Dimension: H (cao tổng), B (rộng cánh), Tw (dày bụng), Tf (dày cánh), r1 (góc bo)

### 3. PFC / U Channel

```
       ← B →
    ┌────────┐  ──
    │        │   ↑ Tf
    │        │       (H)
    │        │   ↓ Tf
    └────┬───┘  ──
         ← Tw (bụng)
```

- Vẽ: polygon hình chữ U
- Dimension: H, B, Tw, Tf, r1

### 4. Angle / L Section

```
    a (Leg A)
    ↑
    ├─────────┐
    │         │
    │         │ ← t (Thickness)
    └─────────┘
    ← b (Leg B) →
```

- Vẽ: polygon hình chữ L
- Dimension: Leg A (a), Leg B (b), Thickness (t), r1

### 5. RHS / SHS (Thép hộp)

```
    ← W →
    ┌──────────┐ ── R_o (bán kính ngoài)
   ╱│          │╲  ↑
  │ │          │ │ t (Thickness)
   ╲│          │╱  ↓    (H)
    └──────────┘ ── R_i (bán kính trong)
```

- Vẽ: 2 hình chữ nhật lồng nhau (ngoài - trong)
- Dimension: W (rộng), H (cao), t (dày), r1 (R_i)

### 6. CHS / Pipe (Thép ống)

```
      ╭─────╮
     ╱│     │╲  ← OD (đường kính ngoài)
    │ │     │ │
     ╲│  ░  │╱  ← ID = OD - 2t
      ╰─────╯
```

- Vẽ: 2 hình tròn đồng tâm
- Dimension: OD, t (dày thành)

### 7. Rod / Round Bar (Thép tròn)

```
      ╭─────╮
     ╱       ╲
    │    ░    │ ← D (đường kính)
     ╲       ╱
      ╰─────╯
```

- Vẽ: 1 hình tròn đặc
- Dimension: D

### 8. T Section (Thép chữ T)

```
    ← B →
    ┌────────┐  ──
    │        │   ↑ Tf
    └───┬────┘  ──
        │
        │ ← Tw (bụng)  (H)
        │
        │
```

- Vẽ: polygon hình chữ T
- Dimension: H, B, Tw, Tf, r1

---

## 📐 Nguyên tắc toán học cho vẽ

1. **Scale tự động**: Tìm bounding box của mặt cắt, scale để vừa với widget (có padding ~10%)
2. **Tỷ lệ giữ nguyên**: Dùng `Qt.KeepAspectRatio`
3. **Tọa độ tương đối**: Trung tâm mặt cắt tại (0,0), scale sau
4. **Dimension line**: Cách cạnh 10-20px, text ở giữa
5. **Mũi tên**: 45° arrowhead, dài 8px

---

## 🛠️ Công nghệ sử dụng

- **QPainter** — API vẽ 2D (line, polygon, arc, text)
- **QPen, QBrush** — Định kiểu đường vẽ và tô màu
- **QFont** — Text cho dimension labels
- **QTransform** — Scale/tỉ lệ tọa độ
- **Anti-aliasing**: `painter.setRenderHint(QPainter.Antialiasing)`
- **Font**: `QFont("Consolas", 9)` cho giá trị số

---

## ⚠️ Rủi ro & Giải pháp

| Rủi ro | Giải pháp |
|:---|:---|
| Tỉ lệ hiển thị không hợp lý (vd: cánh I quá mỏng) | Scale tối thiểu 3px cho mỗi kích thước |
| Dimension text chồng lấn | Kiểm tra va chạm text, dời text ra xa nếu cần |
| Hiệu năng lag khi gõ liên tục | Debounce 100ms trước khi repaint |
| R1 bo góc khó vẽ bằng tay | Dùng `QPainterPath.arcTo()` cho góc bo |

---

## 🔄 Luồng dữ liệu mới

```
User nhập kích thước
        │
        ▼
textChanged signal
        │
        ▼
calc_tab.py → gọi calculate()
        │
        ▼
DynamicDrawingWidget.set_params(values)
        │
        ▼
DynamicDrawingWidget.update() (trigger paintEvent)
        │
        ▼
paintEvent:
  DynamicRenderer.render(painter, w, h)
    ├── section_geometry.get_polygon(steel_type, values) → QPainterPath
    ├── dimension.draw_dimensions(painter, polygon, values)
    └── draw_labels(painter, values)
```

---

## 📅 Thứ tự ưu tiên thực hiện

1. **Giai đoạn 1** (Nền tảng) → Làm trước
2. **Giai đoạn 2** (Tích hợp) → Ngay sau GĐ1
3. **Giai đoạn 3** (Chi tiết hóa) → Khi GĐ1+2 ổn định
4. **Giai đoạn 4** (Hoàn thiện) → Cuối cùng
