# Kế hoạch chi tiết vẽ mặt cắt thép hình động (Dùng Shapely để bo góc)

## 0. Dependency & chuẩn bị

```bash
pip install shapely PySide6
```

Thống nhất trước khi code:

- **Đơn vị**: mm, số thực (float).
- **Gốc toạ độ**: đặt tại **tâm hình học của bounding box** (không phải centroid vật lý) cho mọi profile — để việc scale-to-fit ở bước sau đơn giản, đồng nhất.
- **Chiều trục**: x sang phải, y hướng lên (toạ độ "thật"), sẽ lật khi vẽ ra Qt (Qt y hướng xuống).
- **Quy ước bo góc**: r1 áp dụng cho các góc được liệt kê cụ thể theo từng profile ở bảng dưới, không mặc định bo tất cả góc.

---

## 1. Kiến trúc tổng thể

```
params (dict)
   │
   ▼
[shapes.py] build_raw_polygon()      -> Shapely Polygon KHÔNG bo góc (góc vuông)
   │
   ▼
[fillet.py] apply_fillets()          -> Shapely Polygon ĐÃ bo góc (có thể có hole)
   │
   ▼
[path_utils.py] polygon_to_qpainterpath() -> QPainterPath
   │
   ▼
[section_view.py] SectionView.paintEvent() -> scale-to-fit, vẽ, vẽ dimension
```

Mỗi bước là hàm thuần tuý (pure function), dễ unit test độc lập.

---

## 2. Bước xây polygon thô (`shapes.py`)

Viết 1 hàm cho mỗi profile, trả về **list toạ độ (x, y)** theo chiều kim đồng hồ hoặc ngược kim đồng hồ nhất quán (chọn CCW cho exterior để hợp chuẩn Shapely). Với hình có lỗ (RHS/SHS/CHS) trả về thêm outer + inner riêng.

### Bảng thông số & cách dựng

| Profile | Params | Cách dựng polygon thô | Góc cần bo r1 |
|---|---|---|---|
| **Tấm** | W (rộng), t (dày) | Hình chữ nhật đơn giản `box(-W/2,-t/2, W/2,t/2)` | Không |
| **Tròn đặc** | D | `Point(0,0).buffer(D/2)` — không cần polygon thô, dùng thẳng buffer tạo hình tròn xấp xỉ đa giác | Không |
| **CHS** | D (ngoài), t | Outer = circle bán kính D/2; Inner = circle bán kính D/2 - t (nếu ≤0 thì báo lỗi validate) | Không |
| **RHS/SHS** | H, B (SHS: B=H), t, r1 (bán kính **ngoài**) | Outer: rounded rect qua buffer trực tiếp (xem mục 3.2); Inner: rounded rect với r_in = max(r1 - t, 0) | 4 góc ngoài + 4 góc trong |
| **L / V** | A, B (V: A=B), t, r1 (góc trong), r2 (mũi ngoài, optional = 0) | Polygon 6 điểm hình chữ L: `(0,0),(B,0),(B,t),(t,A),(0,A)`... rồi dịch gốc về giữa bbox | 1 góc lõm trong (giao bụng-cánh), 2 góc ngoài mũi cạnh (r2, có thể =0) |
| **T** | H, B, tw, tf, r1 | Polygon 8 điểm: cánh ngang trên + bụng đứng dưới, đối xứng qua trục đứng | 2 góc lõm nơi bụng nối cánh |
| **C** | H, B, tw, tf, r1 | Polygon 12 điểm: giống I nhưng cánh chỉ mở về 1 phía (dạng chữ C/U) | 4 góc lõm bụng-cánh (2 trên, 2 dưới) |
| **I / H** | H, B, tw, tf, r1 | Polygon 12 điểm đối xứng 2 trục, tâm tại (0,0): cánh trên, bụng, cánh dưới | 4 góc lõm bụng-cánh |

**Ví dụ cụ thể polygon thô của I/H** (điểm đi CCW, gốc ở tâm):

```python
def build_raw_I(H, B, tw, tf, r1):
    hw, hh = B/2, H/2
    hweb = tw/2
    pts = [
        (-hw, hh), (hw, hh), (hw, hh-tf), (hweb, hh-tf),
        (hweb, -hh+tf), (hw, -hh+tf), (hw, -hh), (-hw, -hh),
        (-hw, -hh+tf), (-hweb, -hh+tf), (-hweb, hh-tf), (-hw, hh-tf),
    ]
    return Polygon(pts)
```

Đây chính là polygon "chưa bo góc". 4 góc lõm cần bo là các điểm `(hweb, hh-tf)`, `(hweb, -hh+tf)`, `(-hweb, -hh+tf)`, `(-hweb, hh-tf)` (chỗ bụng gặp cánh).

Tương tự viết `build_raw_C`, `build_raw_T`, `build_raw_L` theo cùng cách liệt kê điểm thủ công — đây là phần lao động chính, cần vẽ tay trên giấy trước khi code để không sai toạ độ.

---

## 3. Bước bo góc (`fillet.py`)

Đây là phần lõi của Hướng A. Có **2 kỹ thuật buffer** tuỳ loại góc:

### 3.1. Bo góc LỒI (convex) — dùng phép "Opening"

```python
def fillet_convex(polygon: Polygon, r: float) -> Polygon:
    if r <= 0:
        return polygon
    return polygon.buffer(-r, join_style=1, resolution=16).buffer(r, join_style=1, resolution=16)
```

`join_style=1` = round. Co vào rồi phồng ra đúng bán kính r → các góc lồi bị "bào tròn", cạnh thẳng không đổi.

### 3.2. Bo góc LÕM (concave) — dùng phép "Closing"

```python
def fillet_concave(polygon: Polygon, r: float) -> Polygon:
    if r <= 0:
        return polygon
    return polygon.buffer(r, join_style=1, resolution=16).buffer(-r, join_style=1, resolution=16)
```

Phồng ra trước rồi co vào → góc lõm được bo, góc lồi hầu như không đổi (nếu r nhỏ hơn cạnh liên quan).

### 3.3. Vấn đề: mỗi polygon có CẢ góc lồi lẫn góc lõm cần bo khác bán kính (VD: RHS ngoài toàn lồi, RHS trong toàn lồi nhưng bán kính khác; I/H toàn lõm bo r1, không có góc lồi cần bo)

→ Giải pháp: **áp dụng closing/opening toàn cục nếu tất cả góc cần bo trong 1 polygon là cùng 1 loại (lồi hoặc lõm) và cùng bán kính** (đúng cho I/H, T, C, RHS-outer, RHS-inner — mỗi cái chỉ có 1 loại góc cần bo).

Riêng **L/V** có cả góc lõm (r1) lẫn góc lồi mũi cạnh (r2, thường nhỏ hoặc =0) → xử lý 2 bước tuần tự:

```python
poly = fillet_concave(raw_L_polygon, r1)   # bo góc trong trước
if r2 > 0:
    poly = fillet_convex(poly, r2)          # rồi bo 2 mũi ngoài
```

Vì closing/opening chỉ ảnh hưởng góc có bán kính cong nhỏ hơn r đang áp, áp lần lượt không phá hỏng góc đã bo trước (miễn r1, r2 đủ nhỏ so với kích thước biên dạng — nên thêm validate).

### 3.4. Validate bắt buộc trước khi buffer (tránh polygon tự cắt/méo)

- `r1 < min(tw, tf)/2`-ish tuỳ hình — mỗi profile cần điều kiện riêng, liệt kê rõ trong `models/params.py`.
- Sau khi buffer xong, luôn kiểm tra `result_polygon.is_valid` và `not result_polygon.is_empty`; nếu fail, fallback trả về polygon thô (không bo) + log cảnh báo, tránh app crash khi người dùng nhập r1 quá lớn.

### 3.5. Hình có lỗ (RHS/SHS)

```python
def build_RHS(H, B, t, r1):
    outer_raw = box(-B/2, -H/2, B/2, H/2)
    outer = fillet_convex(outer_raw, r1)
    r_in = max(r1 - t, 0)
    inner_raw = box(-B/2+t, -H/2+t, B/2-t, H/2-t)
    inner = fillet_convex(inner_raw, r_in)
    return Polygon(outer.exterior, [inner.exterior])  # outer với 1 lỗ = inner
```

Lưu ý: nếu `r1=0` dùng thẳng `box()` không cần buffer, tránh gọi buffer thừa khi r=0.

---

## 4. Chuyển Shapely Polygon → QPainterPath (`path_utils.py`)

```python
from PySide6.QtGui import QPainterPath
from PySide6.QtCore import QPointF

def ring_to_path(path: QPainterPath, coords, is_first: bool):
    pts = list(coords)
    path.moveTo(QPointF(*pts[0]))
    for x, y in pts[1:]:
        path.lineTo(QPointF(x, y))
    path.closeSubpath()

def polygon_to_qpainterpath(polygon) -> QPainterPath:
    path = QPainterPath()
    path.setFillRule(Qt.OddEvenFill)   # bắt buộc để hình có lỗ (RHS/CHS) hiển thị đúng
    ring_to_path(path, polygon.exterior.coords, True)
    for interior in polygon.interiors:
        ring_to_path(path, interior.coords, False)
    return path
```

Vì buffer() của shapely trả về polygon xấp xỉ cung tròn bằng nhiều đoạn thẳng ngắn (số đoạn phụ thuộc `resolution`), **không cần** dùng `arcTo` — chỉ cần `lineTo` nối các điểm là đủ mượt (resolution=16 mỗi 1/4 cung là đủ đẹp ở kích thước UI thông thường; có thể tăng lên 24-32 nếu hình bo góc lớn cần mượt hơn khi zoom).

---

## 5. Widget vẽ (`section_view.py`)

```python
class SectionView(QWidget):
    def __init__(self):
        super().__init__()
        self.shape_type = None
        self.params = {}
        self.setMinimumSize(200, 200)

    def set_params(self, shape_type: str, params: dict):
        self.shape_type = shape_type
        self.params = params
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if not self.shape_type:
            return
        try:
            polygon = build_shape(self.shape_type, self.params)  # gọi shapes.py + fillet.py
            path = polygon_to_qpainterpath(polygon)
        except Exception as e:
            self._draw_error(painter, str(e))
            return

        bbox = path.boundingRect()
        margin = 60  # px chừa cho dimension
        avail_w = max(self.width() - 2*margin, 10)
        avail_h = max(self.height() - 2*margin, 10)
        scale = min(avail_w / bbox.width(), avail_h / bbox.height())

        transform = QTransform()
        transform.translate(self.width()/2, self.height()/2)
        transform.scale(scale, -scale)   # lật trục y
        transform.translate(-bbox.center().x(), -bbox.center().y())

        painter.setTransform(transform)
        pen = QPen(Qt.black); pen.setWidth(0)  # cosmetic pen — luôn 1px thật, không bị scale
        painter.setPen(pen)
        painter.setBrush(QColor("#B0B3B8"))
        painter.drawPath(path)

        painter.resetTransform()
        draw_dimensions(painter, self.shape_type, self.params, transform)
```

`resizeEvent` mặc định của Qt đã tự trigger `paintEvent`, không cần override thêm — kéo giãn cửa sổ là hình tự scale lại.

---

## 6. Vẽ dimension line (`dimension.py`)

Data-driven: mỗi profile khai báo danh sách "đoạn cần đo" bằng toạ độ thật (2 điểm + hướng offset), hàm vẽ dùng chung:

```python
def get_dimension_specs(shape_type, params):
    # trả về list of dict: {p1:(x,y), p2:(x,y), offset_dir:(dx,dy), label:str}
    ...

def draw_dimensions(painter, shape_type, params, transform):
    specs = get_dimension_specs(shape_type, params)
    for spec in specs:
        p1_px = transform.map(QPointF(*spec['p1']))
        p2_px = transform.map(QPointF(*spec['p2']))
        draw_single_dimension(painter, p1_px, p2_px, spec['label'], spec['offset_px'])
```

`draw_single_dimension` vẽ: 2 extension line ngắn, 1 line có 2 mũi tên đầu-cuối, text label ở giữa — style CAD cơ bản. Vẽ ở toạ độ **pixel sau khi map**, không set lại transform, để text/mũi tên luôn đúng tỉ lệ dù hình bị scale nhỏ/lớn.

---

## 7. Validate & UX

`models/params.py`: 1 dataclass + hàm `validate()` cho mỗi profile, ví dụ:

```python
@dataclass
class IBeamParams:
    H: float; B: float; tw: float; tf: float; r1: float = 0
    def validate(self):
        errors = []
        if self.tf*2 >= self.H: errors.append("tf quá lớn so với H")
        if self.tw >= self.B: errors.append("tw quá lớn so với B")
        if self.r1 > min(self.tw, self.tf): errors.append("r1 quá lớn, giảm bớt")
        return errors
```

Nếu có lỗi → hiện text đỏ trong `SectionView` thay vì vẽ hình sai, không raise exception ra ngoài UI.

Ở tầng UI: debounce input bằng `QTimer.singleShot(150, refresh)` để gõ số nhanh không giật hình liên tục.

---

## 8. Cấu trúc file đề xuất

```
geometry/
  shapes.py        # build_raw_*() cho từng profile + build_shape() dispatcher
  fillet.py        # fillet_convex(), fillet_concave()
  path_utils.py     # polygon_to_qpainterpath()
widgets/
  section_view.py   # SectionView(QWidget)
  dimension.py       # get_dimension_specs(), draw_dimensions()
models/
  params.py         # dataclass + validate() từng profile
tests/
  test_shapes.py     # unit test build_raw_* với r1=0 (so khớp polygon vuông kỳ vọng)
  test_fillet.py      # test area/perimeter polygon sau bo góc nằm trong khoảng hợp lý
```

---

## 9. Thứ tự triển khai (độ khó tăng dần, để agent làm tuần tự & review từng bước)

1. `path_utils.py` + `SectionView` khung (scale-to-fit, cosmetic pen) — test bằng 1 `box()` shapely cứng, chưa nối UI thật.
2. **Tấm, Tròn đặc, CHS** — không cần fillet.py, chỉ test cơ chế `OddEvenFill` cho hình có lỗ (CHS).
3. `fillet.py` (`fillet_convex`, `fillet_concave`) — unit test riêng, không qua UI: kiểm tra polygon trước/sau buffer có diện tích, số đỉnh hợp lý.
4. **RHS/SHS** — chỉ dùng `fillet_convex`, có 2 polygon lồng (test even-odd + fillet cùng lúc).
5. **L/V** — kết hợp `fillet_concave` (r1) rồi `fillet_convex` (r2) tuần tự.
6. **T** rồi **C** — nhiều góc lõm hơn nhưng cùng kỹ thuật `fillet_concave`.
7. **I/H** — phức tạp nhất, 4 góc lõm đối xứng, làm cuối để tận dụng kinh nghiệm từ C/T.
8. `dimension.py` — data-driven dimension specs, áp cho tất cả profile đã xong.
9. Nối `set_params()` với các ô nhập trong UI thật + debounce + validate errors hiển thị.
10. Polish: màu sắc, `QWidget.grab().save()` để xuất PNG nếu cần.

---

## 10. Lưu ý bàn giao cho agent

- Yêu cầu agent viết `tests/test_shapes.py` **trước** khi ghép UI — với `r1=0`, polygon trả về phải khớp polygon vuông thủ công (so sánh toạ độ hoặc diện tích) để đảm bảo phần dựng hình học đúng trước khi thêm fillet.
- Nhấn mạnh: `resolution` của buffer ảnh hưởng độ mượt cung tròn — mặc định 16 là đủ cho hiển thị UI thông thường, có thể chỉnh nếu thấy cung tròn bị "gãy khúc" khi phóng to.
- Nhắc agent luôn bọc `build_shape()` trong try/except ở `paintEvent` để tránh crash toàn app khi người dùng nhập giá trị vô lý.
