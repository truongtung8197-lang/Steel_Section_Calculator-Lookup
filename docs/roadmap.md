# Roadmap & Cai thien du kien

> Cap nhat lan cuoi: Version 1.5

---

## Da hoan thanh (Done - kiem chung tu code thuc te)

### 1. Validation & error messages
- ✅ Hoan thanh. `calc_tab.py` co `_validation_msg()` tra ve thong bao chi tiet tung loai thep, hien thi mau do.

### 2. Unit conversion system
- ✅ Hoan thanh. `UNIT_CONVERSION = {mm:1, cm:10, m:1000, inch:25.4}`; `on_unit_changed()` tu convert. Constants trong `core/constants.py`.

### 3. Help system & tooltip
- ✅ Hoan thanh. `gui/dialogs.py` co `show_about`, `show_help` (RichText). Tooltip tren tat ca input/button.

### 4. Logging system
- ✅ Hoan thanh. `core/constants.py` config logging ra `app.log`, level INFO.

### 5. Error handling
- ✅ Hoan thanh (phan lon). Try/except trong `data_manager.py`, `calculate()`; Lookup hien canh bao.

### 6. JSON caching thay vi doc Excel truc tiep
- ✅ Hoan thanh (v1.2 + cai thien v1.5). `load_data()` uu tien JSON, fallback Excel, luu lai JSON.

### 7. Validation messages
- ✅ Hoan thanh. Xem muc 1.

### 8. Tinh nang goc bo (rounded corners)
- ✅ Hoan thanh (v1.3). Truong r1 mac dinh 0, ho tro 5 loai (I/H, U/C, Angle, RHS/SHS, T). Validation r1 trong `geometry.py`.

### 9. Tai cau truc code (Technical Debt)
- ✅ Hoan thanh (v1.4). Tach thanh `core/`, `data/`, `gui/` (tabs, widgets), `docs/`. Moi file don nhiem.

---

## Uu tien cao (High Priority - chua lam)

### 10. Them unit test
- **Ly do:** Bao ve cac cong thuc `core/geometry.py` va validator truoc khi sua code.
- **Cach thuc:** Tao thu muc `tests/` voi `test_geometry.py`, `test_validators.py`, `test_data_manager.py`. Chay bang `pytest`.

### 11. Sua About dialog hien sai version
- **Ly do:** `show_about()` dang hardcode "v1.0", khong khop thuc te (1.5).
- **Cach thuc:** Dinh nghia `APP_VERSION` trong `core/constants.py`, import vao `dialogs.py`.

### 12. Sua metadata.saved_at fix cung
- **Ly do:** `data_manager.py` luu `saved_at="2024-07-16"` cung dinh, sai ngay thuc te.
- **Cach thuc:** Dung `datetime.now().strftime(...)` khi ghi JSON.

---

## Uu tien thap (Low Priority - chua lam)

### 13. Dark mode support
- **Ly do:** Giam moi mat khi dung lau.
- **Cach thuc:** Them stylesheet dark trong `gui/styles.py`, toggle trong menu.

### 14. Xuat bao cao (Excel/PDF)
- **Ly do:** Luu tru ket qua tinh toan / danh sach da tra cuu.

### 15. Luu lich su tinh toan
- **Ly do:** Tien loi tra cuu lai. Luu vao file JSON/sqlite.

### 16. Multi-language support (EN/VI)
- **Ly do:** Ho tro nguoi dung quoc te. Tach text ra resource.

### 17. Them loai thep moi
- **Co the them:** Built-up sections, Custom section (user tu nhap dien tich).
- **Cach thuc:** Mo rong `STEEL_TYPES` trong `core/steel_types.py` + them `area_*`/`check_*` trong `geometry.py`.

---

## Cau truc de xuat them (tests/)

```
tests/
|-- test_geometry.py      # Kiem tra 8 cong thuc area_*
|-- test_validators.py    # Kiem tra check_* raise dung ValueError
|-- test_data_manager.py  # Kiem tra load JSON / fallback Excel
```
