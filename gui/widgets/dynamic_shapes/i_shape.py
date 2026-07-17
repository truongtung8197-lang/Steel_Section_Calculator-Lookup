import math
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _i_shape_points(h, b, tw, tf, r1):
    """Tính outline điểm mặt cắt thép I/H theo công thức hình học.

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Cánh trên (top flange) ở y=h, cánh dưới (bottom flange) ở y=0.
    """
    h = float(h)
    b = float(b)
    tw = float(tw)
    tf = float(tf)
    r1 = float(r1)

    if h <= 0 or b <= 0 or tw <= 0 or tf <= 0:
        raise ValueError("Invalid dimensions for I-shape")

    if tw >= b or 2 * tf >= h:
        raise ValueError("Dimensions violate I-shape constraints")

    if r1 < 0:
        raise ValueError("Corner radius must be non-negative")

    x_web_left = (b - tw) / 2.0
    x_web_right = (b + tw) / 2.0
    max_r = min(x_web_left, (h - 2 * tf) / 2.0)
    if r1 > max_r:
        r1 = max_r

    pts = []

    # --- Đi từ trái sang phải dọc theo cánh trên (top flange) ---
    # Góc trên-trái ngoài
    pts.append(QPointF(0.0, h))
    # Góc trên-phải ngoài
    pts.append(QPointF(b, h))
    # Cạnh trong cánh trên - phải
    pts.append(QPointF(b, h - tf))

    # Arc 1: Trên-Phải (flange → web)
    # Tâm: (x_web_right+r1, h-tf-r1)
    # Start: (x_web_right+r1, h-tf)   → vector (0, r1)   → góc 90°
    # End:   (x_web_right, h-tf-r1)   → vector (-r1, 0)  → góc 180°
    # Sweep: 90° CCW (từ 90° đến 180°)
    if r1 > 1e-9:
        cx = x_web_right + r1
        cy = h - tf - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(90.0 + 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))
    else:
        pts.append(QPointF(x_web_right, h - tf))

    # --- Đi xuống dọc theo bụng (web) bên phải ---
    # Arc 2: Dưới-Phải (web → flange)
    # Tâm: (x_web_right+r1, tf+r1)
    # Start: (x_web_right, tf+r1)     → vector (-r1, 0)  → góc 180°
    # End:   (x_web_right+r1, tf)     → vector (0, -r1)  → góc 270°
    # Sweep: 90° CCW (từ 180° đến 270°)
    if r1 > 1e-9:
        cx = x_web_right + r1
        cy = tf + r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(180.0 + 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))
    else:
        pts.append(QPointF(x_web_right, tf))

    # --- Đi từ phải sang trái dọc theo cánh dưới (bottom flange) ---
    # Cạnh trong cánh dưới - phải
    pts.append(QPointF(b, tf))
    # Góc dưới-phải ngoài
    pts.append(QPointF(b, 0.0))
    # Góc dưới-trái ngoài
    pts.append(QPointF(0.0, 0.0))
    # Cạnh trong cánh dưới - trái
    pts.append(QPointF(0.0, tf))

    # Arc 3: Dưới-Trái (flange → web)
    # Tâm: (x_web_left-r1, tf+r1)
    # Start: (x_web_left-r1, tf)      → vector (0, -r1)  → góc 270°
    # End:   (x_web_left, tf+r1)      → vector (r1, 0)   → góc 0° (360°)
    # Sweep: 90° CCW (từ 270° đến 360°)
    if r1 > 1e-9:
        cx = x_web_left - r1
        cy = tf + r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(270.0 + 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))
    else:
        pts.append(QPointF(x_web_left, tf))

    # --- Đi lên dọc theo bụng (web) bên trái ---
    # Arc 4: Trên-Trái (web → flange)
    # Tâm: (x_web_left-r1, h-tf-r1)
    # Start: (x_web_left, h-tf-r1)    → vector (r1, 0)   → góc 0°
    # End:   (x_web_left-r1, h-tf)    → vector (0, r1)   → góc 90°
    # Sweep: 90° CCW (từ 0° đến 90°)
    if r1 > 1e-9:
        cx = x_web_left - r1
        cy = h - tf - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(0.0 + 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))
    else:
        pts.append(QPointF(x_web_left, h - tf))

    # Cạnh trong cánh trên - trái
    pts.append(QPointF(0.0, h - tf))

    return pts


class DynamicIShape(DynamicShapeWidget):
    def _get_outline_points(self, dims, r1):
        h = dims.get("H", 0)
        b = dims.get("B", 0)
        tw = dims.get("Tw", 0)
        tf = dims.get("Tf", 0)
        return _i_shape_points(h, b, tw, tf, r1)

    def _get_dimension_specs(self, dims):
        h = float(dims.get("H", 0))
        b = float(dims.get("B", 0))
        tw = float(dims.get("Tw", 0))
        tf = float(dims.get("Tf", 0))

        x_web_left = (b - tw) / 2.0
        x_web_right = (b + tw) / 2.0

        return [
            ((0.0, 0.0), (0.0, h), f"H = {h:.0f} mm", "left"),
            ((b, 0.0), (b, tf), f"Tf = {tf:.0f} mm", "right"),
            ((x_web_left, h / 2), (x_web_right, h / 2), f"Tw = {tw:.0f} mm", "top"),
            ((0.0, 0.0), (b, 0.0), f"B = {b:.0f} mm", "bottom"),
        ]