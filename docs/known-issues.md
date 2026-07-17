# Danh sach loi (Known Issues) & Bai hoc kinh nghiem

*Cap nhat lan cuoi: 17/07/2026 (Version 1.8)*

---

## Cac loi da giai quyet (Resolved)

1. **File steel_db.json khong duoc su dung hieu qua**
   * Mo ta: Ung dung luon doc file Excel truc tiep gay cham.
   * Giai phap v1.5: DataManager.load_data() uu tien doc JSON cache, chi fallback sang Excel khi JSON loi/thieu, sau do tu cap nhat lai JSON.

2. **Xu ly loi Excel thieu an toan (Robustness)**
   * Mo ta: Loi cau truc file Excel de gay crash ung dung.
   * Giai phap v1.5: data_manager.py tu dong kiem tra 5 sheet bat buoc, dung skip_headers() bo qua dong tieu de, clean_weight() xu ly cac ky tu la (---, o trong), boc khoi lenh trong try/except va fallback ve danh sach rong [] kem canh bao tren giao dien.

3. **Giao dien co gian (Responsive) chua tot**
   * Mo ta: Font chu va khung nhap lieu bi vo, tran vien hoac qua nho khi thay doi kich thuoc cua so.
   * Giai phap v1.5: Su dung QSplitter voi ty le gian no setStretchFactor, dat chieu rong toi thieu cho khung nhap lieu left_widget.setMinimumWidth(320). Viet de resizeEvent() de goi _update_input_font() tu dong scale font chu dong tu 9pt den 13pt.

---

## Cac loi chua giai quyet (Open Issues)

### A. Thieu he thong Unit Test (Uu tien cao)
* Hien trang: Chua co test suite tu dong kiem tra tinh chinh xac cua cac cong thuc hinh hoc (core/geometry.py) va cac ham kiem tra du lieu dau vao.
* Ke hoach: Tao thu muc tests/ chua test_geometry.py va test_validators.py chay bang pytest.

### B. Gioi han nhap lieu cua QDoubleValidator (Uu tien trung binh)
* Hien trang: Validator gioi han nhap lieu tu 0.001 den 999999.0 mm, khien ung dung khong xu ly duoc kich thuoc lon hon hoac bang 1000 m.
* Ke hoach: Mo rong dai kiem tra hoac chuyen sang tu viet ham kiem tra gia tri (custom validation) trong su kien tinh toan thay vi phu thuoc hoan toan vao validator cua Qt.

### C. Giao dien chi ho tro Light Mode (Uu tien thap)
* Hien trang: File gui/styles.py chi dinh nghia duy nhat mot bang ma mau sang.
* Ke hoach: Phat trien them giao dien toi (Dark Mode) va co che chuyen doi truc tiep tren menu bar.

### D. Xung dot chiem dung file Excel (Uu tien thap)
* Hien trang: Neu nguoi dung dang mo file alias.xlsx bang Microsoft Excel, thu vien openpyxl co the bi loi quyen truy cap (Permission Error) khi co doc ghi.
* Ke hoach: Toi uu hoa co che mo file o che do chi doc (read-only) khi load du lieu tho.

### E. Giao dien About hien thi sai phien ban (Uu tien cao) - Resolved
* Giai phap v1.6: Dua bien APP_VERSION = "1.6" vao core/constants.py va import vao gui/dialogs.py. Nam cung duoc thay bang datetime.now().year.

### F. Ngay cap nhat du lieu saved_at bi co dinh (Uu tien cao) - Resolved
* Giai phap v1.6: Su dung thu vien datetime de tu dong ghi nhan thoi gian thuc khi xuat cache JSON: datetime.now().strftime("%Y-%m-%d").

---

## Bai hoc kinh nghiem cho AI Agent (Lessons Learned)

* **LL-1 (Cau truc Module):** Tuyet doi khong gop code nguoc tro lai thanh mot file duy nhat. Giu vung kien truc module doc lap (core/ xu ly toan hoc, data/ xu ly IO, gui/ xu ly hien thi).
* **LL-2 (An toan du lieu - Fallback IO):** Moi thao tac doc/ghi file ben ngoai (JSON, Excel, hinh anh) bat buoc phai nam trong khoi lenh try-except. Phai luon co phuong an fallback (tra ve danh sach rong, su dung du lieu mac dinh) de tranh ung dung bi crash dot ngot.
* **LL-3 (Xu ly du lieu dau vao som):** Cac ham kiem tra tinh hop le (check_*) phai duoc dat ngay tai layer tinh toan toan hoc (geometry.py), thuc hien truoc khi tinh dien tich de co lap loi logic.
* **LL-4 (Khong hardcode thong tin cau hinh):** Khong hardcode cac chuoi phien ban, ngay thang, duong dan file hoac hang so toan hoc o cac file giao dien. Toan bo phai duoc quan ly tap trung tai core/constants.py.
* **LL-5 (Thiet ke giao dien linh hoat):** Tranh su dung kich thuoc co dinh (fixed size) cho widget. Luon uu tien dung QSplitter, QLayout va lang nghe su kien resizeEvent de tinh toan lai.
* **LL-6 (Ve QPainter cho hinh hoc ky thuat):**
  * Fill dung: Dung QPainterPath + drawPath() voi setBrush() de to mau dac khap kin.
  * Text khong de duong dim: Luon xoa nen phia sau text bang painter.fillRect(rect, QBrush(QColor("#ffffff"))) truoc khi drawText(), kem padding 4-6px.
  * Arrowhead chuan: Dung drawPolygon() tam giac dac (setPen(Qt.NoPen) + setBrush()), khong ve mui ten bang 2 net line.
  * Dimension margin theo pixel: Cong margin SAU khi da chuyen sang toa do widget (dim_margin_px = 20-30px co dinh).
  * Extension lines: Ve duong giong (p1->a, p2->b) bang DashLine roi ra ngoai hinh truoc khi ve duong dim chinh.
  * Font size co dinh theo widget: Font size cho dimension text lay theo self.width() (clamp 9-11pt).
* **LL-7 (Khong dung QPainterPath.arcTo() cho arc fillet):**
  * Dung math.cos/math.sin voi discrete points (steps = max(8, ceil(r1/1.5))) de sinh cac diem tren cung tron.
  * arcTo() de sai huong sweep tren he toa do Y-flip cua Qt (Y xuong duoi).
  * Cach nay da duoc kiem chung thanh cong o DynamicLShape va DynamicIShape.
