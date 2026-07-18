"""Dynamic L-shape (Angle) widget."""

import math

from PySide6.QtCore import QPointF

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _l_shape_points(a, b, t, r1):
    """Tính outline điểm mặt cắt thép góc L (Angle) theo công thức hình học.

    Tọa độ: góc ngoài ở (0,0), cánh A dài `a` theo +x, cánh B dài `b` theo +y,
    độ dày `t`. Góc bo `r1` nằm ở góc trong (t, t).
    """
    a = float(a)
    b = float(b)
    t = float(t)
    r1 = float(r1)

    if a <= 0 or b <= 0 or t <= 0:
        raise ValueError("Invalid dimensions for L-shape")

    if 2 * t >= a or 2 * t >= b:
        raise ValueError("Thickness too large for L-shape")

    if r1 < 0:
        raise ValueError("Corner radius must be non-negative")

    max_r1 = min(a - t, b - t) if (a > t and b > t) else 0.0
    if r1 > max_r1:
        raise ValueError("Corner radius too large")

    pts = []
    pts.append(QPointF(0.0, 0.0))
    pts.append(QPointF(a, 0.0))
    pts.append(QPointF(a, t))

    if r1 > 1e-9:
        cx = t + r1
        cy = t + r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        start_angle = math.radians(270.0)
        end_angle = math.radians(180.0)
        for i in range(steps + 1):
            frac = i / steps
            theta = start_angle + (end_angle - start_angle) * frac
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))
    else:
        pts.append(QPointF(t, t))

    pts.append(QPointF(t, b))
    pts.append(QPointF(0.0, b))
    return pts


class DynamicLShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho Angle/L Section."""
        return {"Leg A": 100, "Leg B": 50, "Thickness": 5}

    def _get_outline_points(self, dims, r1):
        a = dims.get("Leg A", 0)
        b = dims.get("Leg B", 0)
        t = dims.get("Thickness", 0)
        return _l_shape_points(a, b, t, r1)

    def _get_dimension_specs(self, dims, is_sample=False):
        a = dims.get("Leg A", 0)
        b = dims.get("Leg B", 0)
        t = dims.get("Thickness", 0)
        
        if is_sample:
            return [
                ((0.0, 0.0), (0.0, b), "Leg B", "left"),
                ((0.0, 0.0), (a, 0.0), "Leg A", "bottom"),
                ((a, 0.0), (a, t), "t", "right"),
            ]
        else:
            return [
                ((0.0, 0.0), (0.0, b), f"b = {b:.0f} mm", "left"),
                ((0.0, 0.0), (a, 0.0), f"a = {a:.0f} mm", "bottom"),
                ((a, 0.0), (a, t), f"t = {t:.0f} mm", "right"),
            ]
