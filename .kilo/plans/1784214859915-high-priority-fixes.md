# High Priority Fixes - Implementation Plan

*Plan ID:* 1784214859915-high-priority-fixes
*Target:* v1.5 improvements
*Scope:* 3 ưu tiên cao từ `docs/progress.md`

---

## Goals

1. **Remove hardcoded version** in About dialog by centralizing `APP_VERSION` in `core/constants.py`.
2. **Fix hardcoded `saved_at`** in `data/data_manager.py` by using dynamic datetime.
3. **Add Unit Test suite** (`tests/`) covering `core/geometry.py` and `data/data_manager.py` using `pytest`.

---

## Task 1: Centralize Version & Fix saved_at

### 1.1 Add `APP_VERSION` to `core/constants.py`

- **File:** `core/constants.py`
- **Change:** Thêm dòng `APP_VERSION = "1.5"` sau các hằng số hiện có (gần `DENSITY_FACTOR` hoặc cuối trước logging).
- **Note:** Không hardcode ở chỗ khác.

### 1.2 Update About dialog

- **File:** `gui/dialogs.py`
- **Change:**
  - Import: `from core.constants import APP_VERSION`
  - Thay dòng `"Steel Management & Calculator Pro v1.0\n\n"` bằng f-string sử dụng `APP_VERSION`.
  - Cập nhật phần "Year" thành năm hiện tại hoặc dynamic nếu cần (tuỳ chọn, ưu tiên làm sau nếu muốn, nhưng năm 2024 đã sai so với 2026). Đề xuất: thay `Year: 2024` bằng `Year: 2026` hoặc dùng `datetime.now().year`. Để tránh hardcode mới, dùng `datetime.now().year`.

### 1.3 Fix saved_at in `data/data_manager.py`

- **File:** `data/data_manager.py`
- **Change:**
  - Import `from datetime import datetime` ở đầu file.
  - Trong `_save_to_json`, thay `"saved_at": "2024-07-16"` bằng `"saved_at": datetime.now().strftime("%Y-%m-%d")`.
- **Edge case:** Đảm bảo timezone không ảnh hưởng (dùng local time là đủ).

---

## Task 2: Unit Test Suite

### 2.1 Add pytest dependency

- **File:** `requirements.txt`
- **Change:** Thêm `pytest>=8.0` vào cuối file.

### 2.2 Create test structure

- **New files:**
  - `tests/__init__.py` (empty, để pytest nhận diện package)
  - `tests/test_geometry.py`
  - `tests/test_data_manager.py`

### 2.3 `tests/test_geometry.py`

- **Import:** `pytest`, `math`, và các hàm từ `core.geometry`.
- **Coverage - area functions (no corner radius):**
  - `area_plate`: test với Width=100, Thickness=5 → expect 500.
  - `area_ishape`: test với H=200, B=100, Tw=6, Tf=10, r1=0 → expect `2*100*10 + (200-20)*6 = 2000 + 1080 = 3080`.
  - `area_channel`: cùng giá trị H/B/Tw/Tf → expect 3080.
  - `area_angle`: Leg A=100, Leg B=50, Thickness=5 → expect `5*(100+50-5) = 725`.
  - `area_rhs_shs`: Width=100, Height=50, Thickness=5, r1=0 → expect `100*50 - 90*40 = 5000 - 3600 = 1400`.
  - `area_chs`: OD=50, Thickness=5 → expect `pi/4*(2500 - 1600) = pi/4*900 = 706.858...`
  - `area_rod`: Diameter=20 → expect `pi*400/4 = 314.159...`
  - `area_tsection`: H=200, B=100, Tw=6, Tf=10 → expect `100*10 + 190*6 = 1000 + 1140 = 2140`.
- **Coverage - area with corner radius:**
  - `area_ishape` với r1=5 → expect `3080 + (4-pi)*25`.
  - `area_channel` với r1=5 → expect `3080 + (2 - pi/2)*25`.
  - `area_angle` với r1=5 → expect `725 + (1 - pi/4)*25`.
  - `area_rhs_shs` với r1=5, t=5 → expect `1400 - (4-pi)*((10^2)-(5^2)) = 1400 - (4-pi)*75`.
  - `area_tsection` với r1=5 → expect `2140 + (2 - pi/2)*25`.
- **Coverage - check functions:**
  - Valid inputs should NOT raise.
  - Invalid inputs (zero/negative dimensions) should raise `ValueError`.
  - Invalid relationships (e.g., Tw >= B for I-shape) should raise `ValueError`.
  - Invalid radius (r1 < 0 or r1 > allowed max) should raise `ValueError`.
  - RHS/SHS: `2*t >= Width` or `2*t >= Height` should raise.
  - CHS/Rod: invalid thickness or diameter should raise.

### 2.4 `tests/test_data_manager.py`

- **Mock strategy:** Không cần file Excel/JSON thật. Dùng `unittest.mock.patch` và `tmp_path`.
- **Test cases:**
  - `load_data` khi JSON hợp lệ → trả về profiles từ JSON, không đọc Excel.
  - `load_data` khi JSON lỗi/corrupt → fallback sang `_load_excel_data`, rồi `_save_to_json`.
  - `_save_to_json` tạo file JSON đúng cấu trúc, `saved_at` là ngày hiện tại (dùng regex hoặc parse JSON và assert `saved_at` khớp `datetime.now().strftime("%Y-%m-%d")`).
  - `_load_excel_data` khi file Excel không tồn tại → trả về `[]`.
  - `_load_excel_data` với workbook mock đủ sheets → parse đúng số records và cấu trúc dict.
- **Fixtures:** Tạo mock workbook với 4 sheets bắt buộc, mỗi sheet có vài dòng dữ liệu mẫu.

---

## Task 3: Validation & Verification

### 3.1 Automated checks

- Chạy `pytest` từ thư mục gốc, đảm bảo tất cả test pass.
- Chạy `python -m py_compile core/constants.py core/geometry.py data/data_manager.py gui/dialogs.py` để kiểm tra syntax cơ bản (tuỳ chọn, pytest sẽ catch lỗi import).

### 3.2 Manual spot checks

- Chạy app, mở About dialog → verify version hiển thị `1.5`.
- Xóa `steel_db.json`, chạy Lookup tab → xác nhận file JSON được tạo lại với `saved_at` là ngày hôm nay.

---

## Risks & Mitigations

- **Risk:** Test geometry có thể bị sai do tính toán thủ công.
  - *Mitigation:* Dùng giá trị số nguyên đơn giản, hoặc dùng `pytest.approx` cho số thập phân (CHS, corner radius).
- **Risk:** `_load_excel_data` phức tạp, mock có thể bỏ sót logic.
  - *Mitigation:* Tập trung test `load_data` (integration) và `_save_to_json` (unit), `_load_excel_data` chỉ test 1-2 case cơ bản.
- **Risk:** `APP_VERSION` có thể cần dùng ở nhiều chỗ khác trong tương lai.
  - *Mitigation:* Đặt ở `core/constants.py` là đúng theo nguyên tắc tập trung cấu hình.

---

## Dependencies

- Task 1 và Task 2 độc lập, có thể song song.
- Không thay đổi cấu trúc thư mục hiện có ngoài việc thêm `tests/` và `requirements.txt`.
