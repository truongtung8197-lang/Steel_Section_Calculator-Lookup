# Steel Management & Calculator Pro - Tổng quan

**Phiên bản:** 1.4  
**Công nghệ:** Python 3.x, PySide6 (Qt), openpyxl  
**Mục đích:** Công cụ tính toán khối lượng thép lý thuyết và tra cứu profile thép chuẩn từ file Excel

---

## Chức năng chính

### 1. Tab "Manual Calculator" (Bộ tính toán thủ công)

Tính khối lượng thép lý thuyết cho 8 loại hình cắt thép:

- **Plate** (Tấm): Tính theo chiều dài × rộng × dày
- **I Beam / H Beam** (Dầm I/H): Tính diện tích mặt cắt theo công thức hình học
- **PFC / U Channel** (Thép hình U): Tính diện tích mặt cắt theo công thức hình học
- **Angle / L Section** (Thép góc): Tính diện tích mặt cắt theo công thức hình học
- **RHS / SHS** (Thép hộp): Tính diện tích mặt cắt theo công thức hình học
- **CHS / Pipe** (Thép ống): Tính diện tích mặt cắt theo công thức hình học
- **Rod / Round Bar** (Thép tròn): Tính diện tích mặt cắt theo công thức hình học
- **T Section** (Thép chữ T): Tính diện tích mặt cắt theo công thức hình học

**Đặc điểm:**

- Tự động hiển thị hình vẽ kỹ thuật tham khảo cho từng loại thép
- Tính khối lượng theo đơn vị kg/m hoặc kg tùy theo loại thép
- Hỗ trợ nhập số lượng (Quantity) để tính tổng khối lượng
- Nút "Copy Value" để sao chép kết quả tính toán
- Nút "Clear" để xóa trắng các trường nhập liệu
- Validation đầu vào với thông báo lỗi chi tiết theo từng loại thép
- Hỗ trợ đổi đơn vị động (mm/cm/m/inch) với tự động convert giá trị
- **Hỗ trợ tính toán với góc bo (r1)** cho I/H, U/C, Angle, RHS/SHS, T-Section
- Menu Help với About dialog và User Guide chi tiết
- Logging system ghi lại hoạt động vào file app.log

### 2. Tab "Steel Section Lookup" (Tra cứu profile thép)

Tra cứu thông tin profile thép từ file Excel `alias.xlsx`
Hỗ trợ 4 thư viện thép:

- **I Beam / H Beam** (Sheet: "I lib"): 5 cột D, E, F, N, O
- **PFC / U Channel** (Sheet: "U lib"): 5 cột D, E, F, N, O
- **Shape VN** (Sheet: "HINH_VN"): 3 cột A, B, C
- **Pipe / Tube** (Sheet: "Ong,Hop"): 3 cột A, B, C

**Đặc điểm:**

- Tìm kiếm theo tên profile (hỗ trợ tìm kiếm từ khóa nhiều từ)
- Hiển thị chi tiết thông tin profile đã chọn
- Nút "Copy" cho từng trường thông tin để sao chép nhanh
- Hiển thị khối lượng theo kg/m
- Giao diện phân chia 2 panel: danh sách kết quả bên trái, chi tiết bên phải
- Dropdown chọn thư viện thép động (I Beam, U Channel, Shape VN, Pipe/Tube)

---

## Cấu trúc thư mục (v1.4)

```
APP STEEL LOOKUP/
├── main.py                    # Entry point (~40 dòng)
├── alias.xlsx                 # Excel database
├── steel_db.json              # JSON cache (auto-generated)
├── core/                      # Business logic thuần
│   ├── __init__.py
│   ├── constants.py           # DENSITY_FACTOR, UNIT_CONVERSION, paths, logging
│   ├── geometry.py            # 8 cặp area_*/check_* functions
│   └── steel_types.py         # SteelType dataclass + STEEL_TYPES list
├── data/                      # Data management
│   ├── __init__.py
│   └── data_manager.py        # Load/save JSON, load Excel với skip_headers
├── gui/                       # Tất cả UI components
│   ├── __init__.py
│   ├── styles.py              # Stylesheet riêng
│   ├── dialogs.py             # show_about, show_help
│   ├── widgets/
│   │   ├── __init__.py
│   │   └── image_box.py       # ImageBox widget
│   └── tabs/
│       ├── __init__.py
│       ├── calc_tab.py        # CalculatorTab
│       └── lookup_tab.py      # LookupTab
├── docs/                      # Tài liệu
│   ├── overview.md
│   ├── known-issues.md
│   ├── roadmap.md
│   └── changelog.md
└── STEEL TYPE png/            # Hình vẽ kỹ thuật
    ├── CHS.png
    ├── I.png
    ├── L.png
    ├── PL.png
    ├── RHS.png
    ├── ROD.png
    ├── T.png
    └── U.png
```

---

## Công thức tính toán

**Mật độ thép:** 7.85e-6 kg/mm³ (7850 kg/m³)

### Công thức diện tích mặt cắt (không góc bo)

| Loại thép | Công thức |
|-----------|-----------|
| Plate | A = Length × Width × Thickness |
| I Beam | A = 2 × B × Tf + (H - 2 × Tf) × Tw |
| U Channel | A = 2 × B × Tf + (H - 2 × Tf) × Tw |
| Angle | A = t × (a + b - t) |
| RHS/SHS | A = W × H - (W - 2t) × (H - 2t) |
| CHS | A = π/4 × (OD² - (OD - 2t)²) |
| Rod | A = π × D² / 4 |
| T Section | A = B × Tf + (H - Tf) × Tw |

### Công thức diện tích mặt cắt (có góc bo r1)

| Loại thép | Công thức |
|-----------|-----------|
| I Beam | A = 2BT_f + (H-2T_f)T_w + (π-2)r₁² |
| U Channel | A = 2BT_f + (H-2T_f)T_w + 2(π-2)r₁² |
| Angle | A = t(a+b-t) + (π/4-1/2)r₁² |
| RHS/SHS | A = WH - (W-2t)(H-2t) - (4-π)(R_o²-R_i²) |
| T Section | A = BT_f + (H-T_f)T_w + 2(π-2)r₁² |

**Khối lượng:** Weight = Area × Length × Density

---

## Cấu hình đường dẫn

- Tool tự động phát hiện đường dẫn base directory khi chạy từ:
  - File .exe đã đóng gói (PyInstaller)
  - File .py source code
- Các đường dẫn quan trọng:
  - `BASE_DIR`: Thư mục chứa file thực thi
  - `PNG_DIR`: Thư mục chứa hình vẽ kỹ thuật
  - `EXCEL_PATH`: Đường dẫn file alias.xlsx
  - `JSON_PATH`: Đường dẫn file steel_db.json (cache)

---

## Cấu trúc Excel (alias.xlsx)

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

---

## Cấu trúc JSON (steel_db.json)

```json
{
  "profiles": [...],
  "metadata": {
    "total_records": 123,
    "source": "alias.xlsx",
    "saved_at": "2024-07-16"
  }
}
```

Mỗi record có các trường:

- **Type 1 (ih, channel):** type, D, E, F, N, O
- **Type 2 (hinh_vn, ong_hop):** type, D, B, C
