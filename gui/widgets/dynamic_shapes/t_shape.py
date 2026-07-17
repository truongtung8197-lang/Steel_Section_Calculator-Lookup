"""Dynamic T-Section widget."""

import math

from PySide6.QtCore import QPointF

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _t_shape_points(h, b, tw, tf, r1):
    """Tính outline điểm mặt cắt thép T-Section.

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Flange ở trên (y = h-tf đến y = h), web ở dưới (y = 0 đến y = h-tf).
    Outline đi theo chiều KIM ĐỒNG HỒ (clockwise).
    2 góc bo (fillet) ở nơi web giao với flange (góc dưới của flange).
    """
    h = float(h)
    b = float(b)
    tw = float(tw)
    tf = float(tf)
    r1 = float(r1)

    if h <= 0 or b <= 0 or tw <= 0 or tf <= 0:
        raise ValueError("Invalid dimensions for T-shape")
    if tw >= b or tf >= h:
        raise ValueError("Dimensions violate T-shape constraints")
    if r1 < 0:
        raise ValueError("Corner radius must be non-negative")

    max_r = min((b - tw) / 2.0, (h - tf))
    if r1 > max_r:
        r1 = max_r

    x_web_left = (b - tw) / 2.0
    x_web_right = (b + tw) / 2.0
    y_web_top = h - tf  # top of web = bottom of flange
    pts = []

    # === Clockwise outline ===

    # 1. Bottom-left corner of web
    pts.append(QPointF(x_web_left, 0.0))
    # 2. Bottom-right corner of web
    pts.append(QPointF(x_web_right, 0.0))
    # 3. Up right face of web to start of arc 1
    if r1 > 1e-9:
        pts.append(QPointF(x_web_right, y_web_top - r1))
    else:
        pts.append(QPointF(x_web_right, y_web_top))

    # Arc 1: Right fillet (web → flange)
    # Center: (x_web_right+r1, y_web_top-r1)
    # Start: (x_web_right, y_web_top-r1)  → vector (-r1, 0)   → model angle 180°
    # End:   (x_web_right+r1, y_web_top)  → vector (0, r1)    → model angle 90°
    # CW sweep: 180° → 90°
    if r1 > 1e-9:
        cx = x_web_right + r1
        cy = y_web_top - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(180.0 - 90.0 * frac)  # CW
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 4. Right edge of flange (up)
    pts.append(QPointF(b, y_web_top))
    pts.append(QPointF(b, h))
    # 5. Top edge (right → left)
    pts.append(QPointF(0.0, h))
    # 6. Left edge of flange (down) to start of arc 2
    if r1 > 1e-9:
        pts.append(QPointF(x_web_left - r1, y_web_top))  # Shortened by r1
    else:
        pts.append(QPointF(x_web_left, y_web_top))

    # Arc 2: Left fillet (flange → web)
    # Center: (x_web_left-r1, y_web_top-r1)
    # Start: (x_web_left-r1, y_web_top)  → vector (0, -r1)  → model angle 90°
    # End:   (x_web_left, y_web_top-r1)  → vector (r1, 0)   → model angle 0°
    # CW sweep: 90° → 0° (giảm dần)
    if r1 > 1e-9:
        cx = x_web_left - r1
        cy = y_web_top - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(90.0 - 90.0 * frac)  # CW: 90° → 0°
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 7. Down left face of web to bottom-left corner
    if r1 > 1e-9:
        pts.append(QPointF(x_web_left, y_web_top - r1))
    else:
        pts.append(QPointF(x_web_left, 0.0))
    # Back to start — closeSubpath() will connect

    return pts


class DynamicTShape(DynamicShapeWidget):
    def _get_outline_points(self, dims, r1):
        h = dims.get("H", 0)
        b = dims.get("B", 0)
        tw = dims.get("Tw", 0)
        tf = dims.get("Tf", 0)
        return _t_shape_points(h, b, tw, tf, r1)

    def _get_dimension_specs(self, dims):
        h = float(dims.get("H", 0))
        b = float(dims.get("B", 0))
        tw = float(dims.get("Tw", 0))
        tf = float(dims.get("Tf", 0))

        x_web_left = (b - tw) / 2.0
        x_web_right = (b + tw) / 2.0

        return [
            ((0.0, 0.0), (0.0, h), f"H = {h:.0f} mm", "left"),
            ((0.0, h), (b, h), f"B = {b:.0f} mm", "top"),
            ((x_web_left, h / 2), (x_web_right, h / 2), f"Tw = {tw:.0f} mm", "left"),
            ((b, h), (b, h - tf), f"Tf = {tf:.0f} mm", "right"),
        ]
