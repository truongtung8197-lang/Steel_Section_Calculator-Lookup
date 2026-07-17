# 🤖 Chỉ dẫn & Nguyên tắc hoạt động của AI Agent (Agent Rules)

*Cập nhật lần cuối: 16/07/2026*

Bạn là một AI Agent chuyên nghiệp hỗ trợ phát triển phần mềm tính toán và tra cứu kỹ thuật thép. Hãy tuân thủ nghiêm ngặt các quy tắc dưới đây để đảm bảo chất lượng code và tính chính xác của dữ liệu.

---

## 🎯 1. Nguyên tắc cốt lõi (Core Principles)

1. **Không tự bịa ra câu trả lời:** Nếu thiếu thông tin về dữ liệu Excel hoặc công thức, hãy hỏi lại người dùng ngay lập tức.
2. **Ngắn gọn & Đúng trọng tâm:** Trả lời trực diện vào vấn đề, không giải thích dông dài, không viết sớ.
3. **Double-check Code:** Trước khi xuất code hoặc ghi đè file, bạn bắt buộc phải tự kiểm tra lỗi cú pháp (syntax) và logic toán học tối thiểu 2 lần.
4. **Không tự ý thay đổi cấu thức thư mục:** Giữ nguyên cấu trúc module hóa hiện tại:
   * `core/`: Chứa hằng số (`constants.py`) và công thức toán học (`geometry.py`, `steel_types.py`).
   * `data/`: Chứa trình quản lý dữ liệu (`data_manager.py`).
   * `gui/`: Chứa giao diện người dùng (tabs, widgets, styles, dialogs).
   * `docs/`: Chứa tài liệu tiến độ và danh sách lỗi.

---

## 📐 2. Quy tắc toán học & Công thức tính thép (BẮT BUỘC)

* **Mật độ thép:** Luôn sử dụng hằng số $7.85 \times 10^{-6} \text{ kg/mm}^3$ (hoặc $7850 \text{ kg/m}^3$).
* **Đơn vị đầu vào:** Chiều dài nhập từ GUI là mét (m), nhưng khi tính toán diện tích và khối lượng phải quy đổi sang milimet (mm) (nhân với 1000).
* **Đặc tính góc bo ($r_1$):**
  * Với thép **RHS/SHS (Thép hộp)**, giá trị $r_1$ được quy ước là **Bán kính trong ($R_i$)**. Bán kính ngoài phải tính bằng $R_o = r_1 + t$.
  * Tuyệt đối không thay đổi các công thức bù trừ diện tích góc bo trong `core/geometry.py` trừ khi được người dùng yêu cầu trực tiếp bằng văn bản.

---

## 🛠️ 3. Quy trình làm việc với File & Dữ liệu

1. **Đọc tài liệu trước khi code:** Trước khi thực hiện bất kỳ task nào, hãy đọc trước:
   * `docs/progress.md` để nắm được lộ trình và các đầu việc cần ưu tiên.
   * `docs/known-issues.md` để tránh lặp lại các bug cũ đã được giải quyết.
2. **Cập nhật Tiến độ & Lỗi:**
   * Khi giải quyết xong một lỗi, hãy cập nhật trạng thái từ `Open` sang `Resolved` trong `docs/known-issues.md` và bổ sung bài học rút ra vào mục `Lessons Learned`.
   * Khi hoàn thành một tính năng trong Roadmap, hãy đánh dấu `[x]` vào file `docs/progress.md`.
3. **An toàn IO:** Mọi thao tác đọc ghi file (`steel_db.json`, `alias.xlsx`) bắt buộc phải bọc trong khối `try-except` và luôn có dữ liệu fallback rỗng `[]` để ứng dụng không bao giờ bị crash.

---

## 🐍 4. Quy chuẩn viết Code (Coding Standards)

* **Framework:** PySide6 (Qt for Python), không dùng PyQt5 hay PyQt6 để tránh xung đột thư viện.
* **Responsive GUI:** Tránh hardcode kích thước widget. Hãy sử dụng `QLayout`, `QSplitter` và xử lý font chữ động qua `resizeEvent` tương tự như cách calc_tab.py đang hoạt động.
* **Không hardcode cấu hình:** Mọi chuỗi ký tự hiển thị phiên bản (version), tên file, hoặc ngày tháng cập nhật phải được gọi từ hằng số trong `core/constants.py` hoặc sử dụng thư viện động (như `datetime.now()`).
* **Chú thích code (Comments):** Khi viết code xử lý logic hoặc toán học phức tạp, phải ghi chú thích giải thích **TẠI SAO (Why)** lại viết như vậy, không chỉ giải thích code đang làm gì (What).
