# Steel Management & Calculator Pro

**Phiên bản:** 1.3.2  
**Công nghệ:** Python 3.x, PySide6 (Qt), openpyxl

---

File này đã được tách thành các tài liệu nhỏ hơn để dễ quản lý. Vui lòng tham khảo các file sau:

| File | Nội dung |
|------|----------|
| 📘 `docs/overview.md` | Tổng quan tool, chức năng, cấu trúc thư mục, công thức tính, cấu hình |
| ⚠️ `docs/known-issues.md` | Các lỗi đã biết, hạn chế hiện tại |
| 🗺️ `docs/roadmap.md` | Kế hoạch phát triển, cải tiến dự kiến (ưu tiên cao/thấp) |
| 📋 `docs/changelog.md` | Lịch sử thay đổi, thống kê, TODO list, ghi chú phát triển |

---

## Cấu trúc thư mục hiện tại

```
APP STEEL LOOKUP/
├── main.py                    # File chính
├── main.spec                  # PyInstaller config
├── alias.xlsx                 # Excel database
├── steel_db.json              # JSON cache
├── xlsx_to_json.py            # Excel → JSON script
├── STEEL TYPE png/            # Hình vẽ kỹ thuật
├── docs/                      # Tài liệu
│   ├── overview.md
│   ├── known-issues.md
│   ├── roadmap.md
│   └── changelog.md
└── progress.md                # File index này
