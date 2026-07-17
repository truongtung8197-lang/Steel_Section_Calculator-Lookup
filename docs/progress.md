# Tien do phat trien & Lo trinh (Progress & Roadmap)

*Cap nhat lan cuoi: 17/07/2026 (Version 1.8)*

---

## Da hoan thanh (v1.0 -> v1.8)

- [x] Kien truc module hoa: core/, data/, gui/, docs/
- [x] 8 loai thep voi cong thuc dien tich mat cat (co/va khong co goc bo r1)
- [x] Tab Manual Calculator - rebuild_inputs dong, validation, unit conversion
- [x] Tab Steel Section Lookup - tra cuu profile tu Excel/JSON
- [x] ImageBox hien thi anh PNG tinh cho tung loai thep
- [x] Font tu dong scale theo resizeEvent (9-13pt)
- [x] Menu Help: About + User Guide
- [x] Fallback IO an toan (JSON -> Excel, try-except)
- [x] Logging vao app.log
- [x] Fix loi hardcode version (APP_VERSION trong constants.py)
- [x] Fix loi ngay saved_at co dinh (dung datetime.now())
- [x] Tao tests/ voi test_geometry.py va test_data_manager.py
- [x] Dynamic shape v1.7 Buoc 1: Angle/L - DynamicLShape + DynamicShapeWidget base class, QStackedWidget trong calc_tab.py
- [x] Sua rendering bugs DynamicShapeWidget: fill QPainterPath, text clear background, solid arrow polygon, pixel-based dim margin, extension lines, widget-based font size
- [x] Sua 2 bugs DynamicIShape: arc sweep direction (90 -> -90) va thieu direction param trong _draw_dimension_line
- [x] Viet lai DynamicIShape dung manual point calculation (math.cos/sin) thay vi QPainterPath.arcTo() de tranh loi sweep direction

---

## To do list - Version 1.7

### Muc tieu
Loai bo hoan toan anh PNG tinh, thay bang cac widget ve dong (QPainter) hien thi mat cat ngang cua thep theo dung thong so nguoi dung nhap.

### Ke hoach trien khai (tung buoc)

| Buoc | Loai thep | File PNG cu | Class dynamic moi | Ghi chu |
|:----:|:-----------|:-------------|:------------------|:--------|
| 1 | Angle / L | L.PNG | DynamicLShape | Da xong - gui/widgets/dynamic_shapes/l_shape.py, base_shape.py |
| 2 | I Beam / H Beam | I.PNG | DynamicIShape | Da xong - gui/widgets/dynamic_shapes/i_shape.py, dung manual point calculation |
| 3 | PFC / U Channel | U.PNG | DynamicUShape | Da xong - gui/widgets/dynamic_shapes/u_shape.py, dung manual point calculation |
| 4 | RHS / SHS | RHS.PNG | DynamicRHSShape | Da xong - gui/widgets/dynamic_shapes/rhs_shape.py, dung manual point calculation, ve mat cat rong (outer+inner) |
| 5 | T Section | T.PNG | DynamicTShape | Da xong - gui/widgets/dynamic_shapes/t_shape.py |
| 6 | CHS / Pipe | CHS.PNG | DynamicCHSShape | Da xong - gui/widgets/dynamic_shapes/chs_shape.py, mat cat rong (outer+inner tron) |
| 7 | Rod / Round Bar | ROD.PNG | DynamicRodShape | Da xong - gui/widgets/dynamic_shapes/rod_shape.py, hinh tron dac |
| 8 | Plate | PL.PNG | DynamicPlateShape | Da xong - gui/widgets/dynamic_shapes/plate_shape.py, hinh chu nhat |

### Yeu cau ky thuat cho moi dynamic shape

1. Ke thua QWidget - ve bang paintEvent() voi QPainter
2. Nhan thong so dau vao - dict cac kich thuoc (mm), co hoac khong co r1
3. Tu dong scale - vua khung hinh, giu ty le, can giua
4. Hien thi kich thuoc - ve duong kich thuoc (dimension lines) va nhan so
5. Goc bo (r1) - neu r1 > 0, ve cung tron o goc bo tuong ung (dung math.cos/sin, khong dung arcTo)
6. Cap nhat real-time - goi update() khi thong so thay doi
7. Resize responsive - tu dong ve lai khi widget thay doi kich thuoc
8. Fallback - neu thieu thong so, hien thi thong bao thay vi crash

## history Lich su thay doi (Changelog)

### v1.8 (Ban phat hanh hien tai)

* **Dynamic Shape Rendering fixes:** Sua 4 bug rendering trong DynamicShapeWidget (base_shape.py): fill than thep doi sang QPainterPath + drawPath() de mau #e0f2fe do dac; text dimension co clear background bang fillRect() trang + padding; arrowhead doi sang drawPolygon() tam giac dac; dim margin dung pixel co dinh + extension lines thay vi margin theo model space; font size dimension co dinh theo widget (9-11pt), khong scale theo gia tri mm.
* **DynamicIShape bugfixes:** Sua 2 bugs trong DynamicIShape (i_shape.py): (1) arc sweep direction tu 90 -> -90 de ve goc bo dung huong tren he toa do Y-flip cua Qt; (2) them tham so direction con thieu trong loi goi _draw_dimension_line() de DIM hien thi tro lai.
* **DynamicIShape rewrite:**
* **DynamicUShape (Buoc 3):**
* **DynamicRHSShape (Buoc 4):**
* **Hoan thanh dynamic shape cho 8 loai thep:** Loai bo hoan toan phu thuoc vao anh PNG tinh cho dynamic shapes.
* **DynamicPlateShape (Buoc 8):** Them gui/widgets/dynamic_shapes/plate_shape.py voi DynamicPlateShape. Tich hop vao calc_tab.py.
* **DynamicRodShape (Buoc 7):** Them gui/widgets/dynamic_shapes/rod_shape.py voi DynamicRodShape. Tich hop vao calc_tab.py.
* **DynamicCHSShape (Buoc 6):** Them gui/widgets/dynamic_shapes/chs_shape.py voi DynamicCHSShape. Tich hop vao calc_tab.py.
* **DynamicTShape (Buoc 5):** Them gui/widgets/dynamic_shapes/t_shape.py voi DynamicTShape. Tich hop vao calc_tab.py. Them gui/widgets/dynamic_shapes/rhs_shape.py voi DynamicRHSShape. Tich hop vao calc_tab.py. Them gui/widgets/dynamic_shapes/u_shape.py voi DynamicUShape. Tich hop vao calc_tab.py. Viet lai hoan toan _i_shape_points() dung manual point calculation (math.cos/math.sin) thay vi QPainterPath.arcTo() de tranh loi sweep direction. Bo paintEvent() override, de base class xu ly.
* **Tai lieu:** Cap nhat docs/known-issues.md them LL-7 (khong dung arcTo cho arc fillet). Cap nhat docs/plan.md va docs/progress.md.

### v1.7

* **Dynamic Shape Buoc 1 (Angle/L):** Them gui/widgets/dynamic_shapes/ voi DynamicShapeWidget base class va DynamicLShape. Tich hop QStackedWidget vao calc_tab.py de chuyen doi giua ImageBox PNG cu va DynamicLShape khi chon Angle.
* **Unit Test:** Bo sung tests/test_dynamic_l_shape.py kiem tra ham thuan _l_shape_points() voi cac case r1=0, r1>0, invalid dims.

### v1.6

* **Unit Tests:** Bo sung test suite tu dong (tests/) voi 38 test cases kiem tra 8 cong thuc area_* + 8 ham check_* trong core/geometry.py va cac ham load/save/fallback trong data/data_manager.py. Chay bang pytest.
* **Sua loi Version:** Thay hardcode v1.0 trong About dialog bang hang so tap trung APP_VERSION o core/constants.py, nam hien thi tu dong lay datetime.now().year.
* **Sua loi Metadata saved_at:** Thay gia tri co dinh 2024-07-16 bang thoi gian thuc datetime.now().strftime("%Y-%m-%d") khi xuat cache JSON.
* **Tai lieu:** Cap nhat docs/progress.md, docs/known-issues.md va docs/context.md khop phien ban v1.6.

## Rui ro can luu y khi giao cho agent

- Neu agent khong tach _get_outline_points() ra khoi paintEvent(), code se kho test va kho tai dung cho buoc 2-8 - nhac agent lam dung Phase 1/2 truoc khi dung Phase 3.
- **Rendering bugs da gap o buoc 1 (ghi nho cho buoc 2-8):** (1) Fill phai dung QPainterPath + drawPath(), khong dung drawLine() loop. (2) Text phai clear background bang fillRect() + QFontMetrics do kich thuoc that. (3) Arrowhead phai dung drawPolygon() dac, khong dung line-based de tranh ke thua DashLine. (4) Dimension margin phai la pixel co dinh SAU khi da sang widget space, khong phai mm model space. (5) Extension lines giup tach biet dim line khoi bien hinh.
- **KHONG DUNG QPainterPath.arcTo() cho arc fillet.** Dung math.cos/math.sin voi discrete points (giong L-shape) de tranh loi sweep direction tren he toa do Y-flip cua Qt.
- Toan goc bo (Phase 2b) la phan de sai nhat - yeu cau agent tu verify bang in ra toa do + ve thu voi r1=0 truoc khi them r1>0.
