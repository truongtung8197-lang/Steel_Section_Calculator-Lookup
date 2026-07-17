# Plan: v1.7 Buoc 1 - DynamicLShape (Angle/L)

Da co main.py + calc_tab.py that.

## Quyet dinh kien truc quan trong: lam base class NGAY o buoc 1

Roadmap co 8 buoc lap lai cung 1 bo yeu cau ky thuat (scale-to-fit, dimension lines, arc r1, fallback...). Buoc 1 xay 1 base class dung chung + 1 class con DynamicLShape. Cac buoc 2-8 sau chi can viet class con.

```
gui/widgets/dynamic_shapes/
  __init__.py
  base_shape.py       # DynamicShapeWidget(QWidget) - logic dung chung
  l_shape.py          # DynamicLShape(DynamicShapeWidget) - rieng cho Angle
  i_shape.py          # DynamicIShape(DynamicShapeWidget) - rieng cho I/H Beam
```

## Phase 1 - base_shape.py: DynamicShapeWidget

- set_dimensions(dims: dict, r1: float = 0) - nhan dict thong so (mm) + r1, goi self.update().
- paintEvent(event) - khung chuan: neu dims rong/invalid -> goi _draw_fallback(); nguoc lai tinh scale-to-fit roi goi _get_outline_points() (phai override o class con) de ve.
- _draw_dimension_line(painter, p1, p2, label, offset) - helper ve duong kich thuoc + mui ten + text, dung chung.
- _draw_fallback(painter, message) - dung chung.
- resizeEvent(event) - goi self.update().
- Method truu tuong: _get_outline_points(dims, r1) -> list[QPointF] va _get_dimension_specs(dims) -> list[tuple].

## Phase 2 - l_shape.py: DynamicLShape

- Input dims: {"Leg A": ..., "Leg B": ..., "Thickness": ...} (mm).
- _get_outline_points(dims, r1): tinh outline hinh L. Neu r1 > 0: thay goc trong bang cung tron ban kinh r1 - dung math.cos/math.sin de tinh discrete points (khong dung QPainterPath.arcTo).
- _get_dimension_specs(dims): tra ve list cac duong kich thuoc.

### Cach tinh arc chuan (dung cho moi shape):
Dung math.cos/math.sin voi steps = max(8, ceil(r1/1.5)) de sinh discrete points tren cung tron. Khong dung QPainterPath.arcTo() vi de sai huong sweep tren he toa do Y-flip cua Qt.

## Phase 3 - Tich hop vao calc_tab.py

1. Thay self.image_box = ImageBox() bang QStackedWidget chua nhieu trang: trang 0 = ImageBox cu, cac trang sau = dynamic shape widgets.
2. Mapping DYNAMIC_SHAPE_MAP trong calc_tab.py:
   DYNAMIC_SHAPE_MAP = {"angle": DynamicLShape, "ih": DynamicIShape}
3. Trong rebuild_inputs(), switch image_stack.setCurrentIndex() theo steel.key in DYNAMIC_SHAPE_KEYS.
4. Trong calculate(), goi self._dynamic_widgets[steel.key].set_dimensions(values, values.get("r1", 0)) khi hop le, set_dimensions({}, 0) khi loi/invalid.

## Phase 4 - Test

- tests/test_dynamic_l_shape.py: test _l_shape_points() thuan logic.
- tests/test_dynamic_i_shape.py: test _i_shape_points() thuan logic.

## Phase 5 - Fallback & rollback an toan

- Neu dynamic shape loi runtime -> base class wrap trong try-except, fallback ve _draw_fallback().
- Giu nguyen ImageBox + PNG cho cac loai chua lam dynamic.

## Checklist thuc hien

- [x] Tao gui/widgets/dynamic_shapes/base_shape.py voi DynamicShapeWidget
- [x] Viet _l_shape_points(a, b, t, r1) thuan logic
- [x] Tao gui/widgets/dynamic_shapes/l_shape.py voi DynamicLShape
- [x] Viet tests/test_dynamic_l_shape.py
- [x] Xac nhan label that cua steel.fields cho Angle (Leg A/Leg B/Thickness)
- [x] Thay self.image_box bang QStackedWidget trong _setup_ui()
- [x] Sua rebuild_inputs(): switch image_stack.setCurrentIndex()
- [x] Sua calculate(): goi dynamic_widget.set_dimensions()
- [x] Test tay tren UI
- [x] Cap nhat progress.md

## Rui ro can luu y

- Khong dung QPainterPath.arcTo() cho arc fillet. Dung math.cos/math.sin voi discrete points (giong L-shape) de tranh loi sweep direction tren he toa do Y-flip cua Qt.
