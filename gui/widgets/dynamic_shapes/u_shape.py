"""Dynamic U-shape (PFC / Channel) widget."""

import math

from PySide6.QtCore import QPointF

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _u_shape_points(h, b, tw, tf, r1):
    """Tính outline điểm mặt cắt thép U (PFC / Channel).

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Outline đi theo chiều KIM ĐỒNG HỒ (clockwise).
    Web nằm bên TRÁI (x = 0 đến x = tw), flanges hướng sang PHẢI (x = 0 đến x = b).
    Chỉ có 2 góc bo (fillet) ở bên TRÁI (nơi web giao với flange).
    """
    h = float(h)
    b = float(b)
    tw = float(tw)
    tf = float(tf)
    r1 = float(r1)

    if h <= 0 or b <= 0 or tw <= 0 or tf <= 0:
        raise ValueError("Invalid dimensions for U-shape")

    if tw >= b or 2 * tf >= h:
        raise ValueError("Dimensions violate U-shape constraints")

    if r1 < 0:
        raise ValueError("Corner radius must be non-negative")

    max_r = min((b - tw), (h - 2 * tf) / 2.0)
    if r1 > max_r:
        r1 = max_r

    # Web ở bên TRÁI: x từ 0 đến tw
    # Flanges hướng sang PHẢI: x từ 0 đến b
    # Right face của web (inner face, facing the inside of the channel): x = tw
    xw = tw  # right face of web (inner face)
    pts = []

    # === Clockwise outline ===

    # 1. Bottom-left outer corner (web bottom)
    pts.append(QPointF(0.0, 0.0))
    # 2. Bottom flange: đi sang phải → góc dưới-phải ngoài
    pts.append(QPointF(b, 0.0))
    # 3. Đi lên cạnh phải của bottom flange
    pts.append(QPointF(b, tf))
    # 4. Đi sang trái dọc theo inner edge của bottom flange đến start của arc 1
    if r1 > 1e-9:
        pts.append(QPointF(xw + r1, tf))
    else:
        pts.append(QPointF(xw, tf))

    # Arc 1: Bottom-LEFT fillet (flange → web)
    # Center: (xw+r1, tf+r1) but in our case xw=tw, so center=(tw+r1, tf+r1)
    # Start: (xw+r1, tf)  → vector (0, -r1)  → model angle 270°
    # End:   (xw, tf+r1)  → vector (-r1, 0)  → model angle 180°
    # CW sweep: 270° → 180°
    if r1 > 1e-9:
        cx = xw + r1
        cy = tf + r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(270.0 - 90.0 * frac)  # CW
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 5. Đi lên dọc theo right face của web (x = xw) đến start của arc 2
    if r1 > 1e-9:
        pts.append(QPointF(xw, h - tf - r1))
    else:
        pts.append(QPointF(xw, h - tf))

    # Arc 2: Top-LEFT fillet (web → flange)
    # Center: (xw+r1, h-tf-r1) = (tw+r1, h-tf-r1)
    # Start: (xw, h-tf-r1)  → vector (-r1, 0)  → model angle 180°
    # End:   (xw+r1, h-tf)  → vector (0, r1)   → model angle 90°
    # CW sweep: 180° → 90°
    if r1 > 1e-9:
        cx = xw + r1
        cy = h - tf - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(180.0 - 90.0 * frac)  # CW
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 6. Đi sang phải dọc theo inner edge của top flange đến cạnh phải
    pts.append(QPointF(b, h - tf))
    # 7. Đi lên cạnh phải → góc trên-phải ngoài
    pts.append(QPointF(b, h))
    # 8. Top: đi sang trái → góc trên-trái ngoài (web top)
    pts.append(QPointF(0.0, h))
    # 9. Đi xuống cạnh trái (left face của web) đến inner edge của top flange
    pts.append(QPointF(0.0, h - tf))
    # 10. Đi xuống cạnh trái đến inner edge của bottom flange
    pts.append(QPointF(0.0, tf))
    # 11. Về (0,0) — closeSubpath() sẽ tự nối

    return pts


class DynamicUShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho U/C Channel."""
        return {"H": 200, "B": 100, "Tw": 6, "Tf": 10}

    def _get_outline_points(self, dims, r1):
        h = dims.get("H", 0)
        b = dims.get("B", 0)
        tw = dims.get("Tw", 0)
        tf = dims.get("Tf", 0)
        return _u_shape_points(h, b, tw, tf, r1)

    def _get_dimension_specs(self, dims, is_sample=False):
        h = float(dims.get("H", 0))
        b = float(dims.get("B", 0))
        tw = float(dims.get("Tw", 0))
        tf = float(dims.get("Tf", 0))

        if is_sample:
            return [
                ((0.0, 0.0), (0.0, h), "H", "left"),
                ((b, 0.0), (b, tf), "Tf", "right"),
                # Tw: đo từ left face (x=0) đến right face của web (x=tw)
                ((0.0, h / 2), (tw, h / 2), "Tw", "left"),
                ((0.0, 0.0), (b, 0.0), "B", "bottom"),
            ]
        else:
            return [
                ((0.0, 0.0), (0.0, h), f"H = {h:.0f} mm", "left"),
                ((b, 0.0), (b, tf), f"Tf = {tf:.0f} mm", "right"),
                # Tw: đo từ left face (x=0) đến right face của web (x=tw)
                ((0.0, h / 2), (tw, h / 2), f"Tw = {tw:.0f} mm", "left"),
                ((0.0, 0.0), (b, 0.0), f"B = {b:.0f} mm", "bottom"),
            ]
