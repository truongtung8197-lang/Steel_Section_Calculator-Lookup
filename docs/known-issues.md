# Known Issues & Loi da biet

> Cap nhat lan cuoi: Version 1.5

---

## Da giai quyet (Resolved)

### 1. File steel_db.json khong duoc su dung
- **Trang thai v1.5:** ✅ Da giai quyet. `DataManager.load_data()` uu tien doc JSON, chi fallback sang Excel khi JSON loi/thieu, roi luu lai JSON.

### 2. Xu ly loi Excel chua robust
- **Trang thai v1.5:** ✅ Da cai thien. `data_manager.py` validate 4 sheet bat buoc, `skip_headers()` bo qua header, `clean_weight()` xu ly `---`/rong, try/except quanh load, fallback `[]`. Lookup tab hien canh bao neu Excel chua load.

### 3. Khong co unit test
- **Trang thai v1.5:** ⚠ Chua co. Van nam trong TODO (ngan han).

### 4. Giao dien chua responsive tot
- **Trang thai v1.5:** ✅ Da cai thien dang ke. `calc_tab.py` co `resizeEvent` + `_update_input_font()` scale font 9-13pt; dung `QSplitter` voi `setStretchFactor`; `left_widget.setMinimumWidth(320)` tranh input qua nho. Van con: minimum size cua MainWindow la 1000x680.

### 5. Loi tiem an voi QDoubleValidator
- **Trang thai v1.5:** ⚠ Van con. Validator gioi han 0.001 - 999999.0, nen khong tinh duoc kich thuoc > 999999 mm. Hien tai chap nhan vi du an chua can.

### 6. GUI khong responsive khi resize
- **Trang thai v1.5:** ✅ Da giai quyet (xem muc 4). Font tu dong scale, splitter linh hoat, PNG co `resizeEvent` trong `ImageBox` render lai.

---

## Chua giai quyet (Open)

### A. Thieu unit test
- Chua co test suite kiem tra cong thuc tinh toan (`core/geometry.py`) va validator.
- **Ke hoach:** Them `tests/test_geometry.py`, `tests/test_validators.py`.

### B. QDoubleValidator gioi han kich thuoc lon
- Chi nhan 0.001 - 999999.0 mm. Kich thuoc rat lon se bi tu choi.
- **Ke hoach:** Mo rong range hoac bo validator, tu validate trong `calculate()`.

### C. Chi co 1 stylesheet (light mode)
- `gui/styles.py` chi dinh nghia light mode. Chua co dark mode.
- **Ke hoach:** Them dark mode toggle (xem roadmap).

### D. Excel phai mo khoa khi dang chay
- Neu `alias.xlsx` dang mo boi Excel, `openpyxl` voi `data_only=True` van doc duoc (read-only), nhung neu JSON da ton tai thi khong doc Excel. Rui ro thap.

### E. About dialog hien sai version
- `gui/dialogs.py` `show_about()` hien "v1.0" (chua cap nhat len 1.5). Can sua hardcode string.
- **Ke hoach:** Keo version tu constant chung thay vi hardcode.

### F. metadata.saved_at fix cung "2024-07-16"
- Trong `data_manager.py`, truong `saved_at` la chuoi fix cung, chua dung ngay ghi thuc te.
- **Ke hoach:** Dung `datetime.now()` khi luu JSON.
