# Steel Management & Calculator Pro - Tong quan

**Phien ban:** 1.6  
**Cong nghe:** Python 3.14.x, PySide6 6.11.1 (Qt), openpyxl 3.1.5  
**Muc dich:** Cong cu tinh toan khoi luong thep ly thuyet va tra cuu profile thep chuan tu file Excel

---

## Chuc nang chinh

### 1. Tab "Manual Calculator" (Bo tinh toan thu cong)

Tinh khoi luong thep ly thuyet cho 8 loai hinh cat thep (dinh nghia trong `core/steel_types.py`):

- **Plate** (Tam): Dai x Rong x Day
- **I Beam / H Beam** (Dam I/H)
- **PFC / U Channel** (Thep hinh U)
- **Angle / L Section** (Thep goc)
- **RHS / SHS** (Thep hop)
- **CHS / Pipe** (Thep ong)
- **Rod / Round Bar** (Thep tron)
- **T Section** (Thep chu T)

**Dac diem (thuc te code v1.6):**

- Chon loai thep tu dropdown; form input duoc build dong (`rebuild_inputs` trong `calc_tab.py`)
- Tu dong hien thi hinh ve ky thuat tu `STEEL TYPE png/` qua `ImageBox` widget
- Tinh khoi luong theo kg/m (mac dinh Length=1m) hoac kg (Plate / nhieu quantity)
- Ho tro nhap Quantity de tinh tong khoi luong
- Nut "Copy Value" sao chep ket qua vao clipboard
- Nut "Clear" xoa trang cac truong
- Validation dau vao voi `_validation_msg()` hien thi loi mau do
- Ho tro doi don vi dong (mm/cm/m/inch) voi `on_unit_changed()` tu dong convert
- Ho tro tinh toan goc bo (r1) cho 5 loai: I/H, U/C, Angle, RHS/SHS, T-Section
- Font input tu dong scale (9-13pt) theo chieu rong cua so qua `resizeEvent`
- Menu Help (About + User Guide) trong `gui/dialogs.py`
- Logging vao `app.log`

### 2. Tab "Steel Section Lookup" (Tra cuu profile thep)

Tra cuu thong tin profile thep tu `steel_db.json` (cache) hoac `alias.xlsx` (fallback).
Ho tro 4 thu vien (dinh nghia trong `data/data_manager.py`):

- **I Beam / H Beam** (Sheet: "I lib"): cot D, E, F, N, O
- **PFC / U Channel** (Sheet: "U lib"): cot D, E, F, N, O
- **Shape VN** (Sheet: "HINH_VN"): cot D, B, C
- **Pipe / Tube** (Sheet: "Ong,Hop"): cot D, B, C

**Dac diem:**

- Tim kiem theo ten profile, ho tro nhieu tu khoa (space-separated)
- Hien thi chi tiet profile da chon (Original/Substitute section + weight)
- Nut "Copy" cho tung truong
- Giao dien 2 panel: danh sach trai, chi tiet phai (QSplitter)
- Dropdown chon thu vien dong
- Canh bao ro rang neu Excel chua load duoc

---

## Cau truc thu muc (v1.6)

```
Steel_Section_Calculator-Lookup/
|-- main.py                    # Entry point (49 dong)
|-- alias.xlsx                 # Excel database
|-- steel_db.json              # JSON cache (tu dong tao)
|-- requirements.txt           # PySide6==6.11.1, openpyxl==3.1.5
|-- core/                      # Business logic
|   |-- constants.py           # DENSITY_FACTOR, UNIT_CONVERSION, paths, logging
|   |-- geometry.py            # 8 cap area_*/check_* functions
|   |-- steel_types.py         # SteelType dataclass + STEEL_TYPES list (8 loai)
|-- data/                      # Data management
|   |-- data_manager.py        # Load/save JSON, load Excel voi skip_headers
|-- gui/                       # UI components
|   |-- styles.py              # Stylesheet (light mode)
|   |-- dialogs.py             # show_about, show_help
|   |-- widgets/
|   |   |-- image_box.py       # ImageBox widget (QLabel + QPixmap)
|   |-- tabs/
|   |   |-- calc_tab.py        # CalculatorTab (315 dong)
|   |   |-- lookup_tab.py      # LookupTab (162 dong)
|-- docs/                      # Tai lieu
|   |-- progress.md
|   |-- context.md
|   |-- known-issues.md
|-- STEEL TYPE png/            # Hinh ve ky thuat (8 file PNG)
```

---

## 📐 Công thức tính toán chuẩn hóa

* **Mật độ khối lượng của thép:** $7.85 \times 10^{-6} \text{ kg/mm}^3$ (tương đương $7850 \text{ kg/m}^3$).
* **Công thức tính khối lượng tổng quát:**
  $$\text{Weight (kg)} = \text{Area (mm}^2\text{)} \times \text{Length (m)} \times 0.00785$$
  *(Trong đó: chiều dài nhập vào bằng mét được nhân với 1000 để quy đổi sang mm trước khi tính toán)*

---

### 1. Công thức diện tích mặt cắt $A \text{ (mm}^2\text{)}$ - KHÔNG CÓ GÓC BO

| Loại thép | Công thức diện tích mặt cắt ($A$) | Ghi chú biến số |
| :--- | :--- | :--- |
| **Plate** (Thép tấm) | $A = \text{Width} \times \text{Thickness}$ | Chiều rộng (Width), Độ dày (Thickness) |
| **I Beam** (Thép I/H) | $A = 2B \cdot T_f + (H - 2T_f)T_w$ | Chiều cao ($H$), Rộng cánh ($B$), Dày bụng ($T_w$), Dày cánh ($T_f$) |
| **U Channel** (Thép U/C) | $A = 2B \cdot T_f + (H - 2T_f)T_w$ | Chiều cao ($H$), Rộng cánh ($B$), Dày bụng ($T_w$), Dày cánh ($T_f$) |
| **Angle** (Thép góc V/L) | $A = t(a + b - t)$ | Chiều dài 2 cánh ($a, b$), Độ dày ($t$) |
| **RHS/SHS** (Thép hộp) | $A = W \cdot H - (W - 2t)(H - 2t)$ | Chiều rộng ($W$), Chiều cao ($H$), Độ dày ($t$) |
| **CHS** (Thép ống tròn) | $A = \frac{\pi}{4} [OD^2 - (OD - 2t)^2]$ | Đường kính ngoài ($OD$), Độ dày ($t$) |
| **Rod** (Thép tròn đặc) | $A = \frac{\pi \cdot D^2}{4}$ | Đường kính ($D$) |
| **T Section** (Thép chữ T) | $A = B \cdot T_f + (H - T_f)T_w$ | Rộng cánh ($B$), Chiều cao ($H$), Dày cánh ($T_f$), Dày bụng ($T_w$) |

---

### 2. Công thức diện tích mặt cắt $A \text{ (mm}^2\text{)}$ - CÓ GÓC BO ($r_1$)

| Loại thép | Công thức diện tích mặt cắt ($A$) | Giải thích hiệu chỉnh góc bo |
| :--- | :--- | :--- |
| **I Beam** (Thép I/H) | $A = 2B \cdot T_f + (H - 2T_f)T_w + (4 - \pi)r_1^2$ | Cộng thêm diện tích của 4 góc bo nội |
| **U Channel** (Thép U/C) | $A = 2B \cdot T_f + (H - 2T_f)T_w + (2 - \frac{\pi}{2})r_1^2$ | Cộng thêm diện tích của 2 góc bo nội |
| **Angle** (Thép góc V/L) | $A = t(a + b - t) + (1 - \frac{\pi}{4})r_1^2$ | Cộng thêm diện tích của 1 góc bo nội |
| **RHS/SHS** (Thép hộp)* | $A = W \cdot H - (W - 2t)(H - 2t) - (4 - \pi)(R_o^2 - R_i^2)$ | Trừ bớt diện tích hao hụt do bo tròn 4 góc bên ngoài và bên trong. Quy ước: Bán kính trong $R_i = r_1$; Bán kính ngoài $R_o = r_1 + t$. |
| **T Section** (Thép chữ T) | $A = B \cdot T_f + (H - T_f)T_w + (2 - \frac{\pi}{2})r_1^2$ | Cộng thêm diện tích của 2 góc bo nội |

---

## Cau hinh duong dan

- `BASE_DIR`: tu dong phat hien (file .py hoac .exe qua `sys.frozen`)
- `PNG_DIR`: thu muc hinh ve ky thuat
- `EXCEL_PATH`: duong dan alias.xlsx
- `JSON_PATH`: duong dan steel_db.json (cache)

---

## Cau truc Excel (alias.xlsx)

**Sheet "I lib" va "U lib":**

- Cot D: Ten profile
- Cot E: Ten section goc
- Cot F: Khoi luong kg/m (original)
- Cot N: Ten section thay the
- Cot O: Khoi luong kg/m (substitute)

**Sheet "HINH_VN" va "Ong,Hop":**

- Cot A: Ten profile
- Cot B: Khoi luong kg/m
- Cot C: Ghi chu

---

## Cau truc JSON (steel_db.json)

```json
{
  "profiles": [
    { "type": "ih", "D": "...", "E": "...", "F": "...", "N": "...", "O": "..." },
    { "type": "hinh_vn", "D": "...", "B": "...", "C": "..." }
  ],
  "metadata": { "total_records": 964, "source": "alias.xlsx", "saved_at": "2024-07-16" }
}
```

Moi record:

- **Type 1 (ih, channel):** type, D, E, F, N, O
- **Type 2 (hinh_vn, ong_hop):** type, D, B, C
