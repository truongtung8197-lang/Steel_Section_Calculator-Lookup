# Tiến độ phát triển & Lộ trình (Progress & Roadmap)

*Cập nhật lần cuối: 17/07/2026 (Version 1.6)*

---

## ✅ Đã hoàn thành (v1.0 → v1.6)

- [x] Kiến trúc module hóa: core/, data/, gui/, docs/
- [x] 8 loại thép với công thức diện tích mặt cắt (có/và không có góc bo r₁)
- [x] Tab Manual Calculator — rebuild_inputs động, validation, unit conversion
- [x] Tab Steel Section Lookup — tra cứu profile từ Excel/JSON
- [x] ImageBox hiển thị ảnh PNG tĩnh cho từng loại thép
- [x] Font tự động scale theo resizeEvent (9–13pt)
- [x] Menu Help: About + User Guide
- [x] Fallback IO an toàn (JSON → Excel, try-except)
- [x] Logging vào app.log
- [x] Fix lỗi hardcode version (APP_VERSION trong constants.py)
- [x] Fix lỗi ngày saved_at cố định (dùng datetime.now())
- [x] Tạo tests/ với test_geometry.py và test_data_manager.py

---

## 🗺️ To do list — Version 1.7

### Mục tiêu
Loại bỏ hoàn toàn ảnh PNG tĩnh, thay bằng các widget vẽ động (QPainter) hiển thị mặt cắt ngang của thép theo đúng thông số người dùng nhập.

### Kế hoạch triển khai (từng bước)

| Bước | Loại thép | File PNG cũ | Class dynamic mới | Ghi chú |
|:----:|:-----------|:-------------|:------------------|:--------|
| 1 | Angle / L | L.PNG | DynamicLShape | Đang làm |
| 2 | I Beam / H Beam | I.PNG | DynamicIShape | Kế tiếp |
| 3 | PFC / U Channel | U.PNG | DynamicUShape | |
| 4 | RHS / SHS | RHS.PNG | DynamicRHSShape | |
| 5 | T Section | T.PNG | DynamicTShape | |
| 6 | CHS / Pipe | CHS.PNG | DynamicCHSShape | |
| 7 | Rod / Round Bar | ROD.PNG | DynamicRodShape | |
| 8 | Plate | PL.PNG | DynamicPlateShape | |

### Yêu cầu kỹ thuật cho mỗi dynamic shape

1. Kế thừa QWidget — vẽ bằng paintEvent() với QPainter
2. Nhận thông số đầu vào — dict các kích thước (mm), có hoặc không có r₁
3. Tự động scale — vừa khung hình, giữ tỷ lệ, căn giữa
4. Hiển thị kích thước — vẽ đường kích thước (dimension lines) và nhãn số
5. Góc bo (r₁) — nếu r₁ > 0, vẽ cung tròn ở góc bo tương ứng
6. Cập nhật real-time — gọi update() khi thông số thay đổi
7. Resize responsive — tự động vẽ lại khi widget thay đổi kích thước
8. Fallback — nếu thiếu thông số, hiển thị thông báo thay vì crash
