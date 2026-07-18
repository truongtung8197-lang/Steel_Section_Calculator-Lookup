"""Dynamic T-Section widget."""

import math
from PySide6.QtCore import QPointF
from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget

def _t_shape_points(h, b, tw, tf, r1):
    """Tính outline điểm mặt cắt thép T-Section.

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Flange ở trên (y = h-tf đến y = h), web ở dưới (y = 0 đến y = h-tf).
    Outline đi theo chiều KIM ĐỒNG HỒ (clockwise).
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

    # Giới hạn bán kính bo góc tối đa để không phá vỡ cấu trúc hình học
    max_r = min((b - tw) / 2.0, (h - tf))
    if r1 > max_r:
        r1 = max_r

    x_web_left = (b - tw) / 2.0
    x_web_right = (b + tw) / 2.0
    y_web_top = h - tf  # Mặt dưới của flange
    pts = []

    # === VẼ THEO CHIỀU KIM ĐỒNG HỒ (CLOCKWISE) ===

    # 1. Đáy bên trái của bụng (Web)
    pts.append(QPointF(x_web_left, 0.0))
    
    # 2. Đáy bên phải của bụng (Web)
    pts.append(QPointF(x_web_right, 0.0))
    
    # 3. Đường đứng bên phải bụng tiến lên điểm bắt đầu Arc 1
    if r1 > 1e-9:
        pts.append(QPointF(x_web_right, y_web_top - r1))
    else:
        pts.append(QPointF(x_web_right, y_web_top))

    # Arc 1: Bo góc phải (Web → Flange)
    # Tâm: (x_web_right + r1, y_web_top - r1)
    # Góc chạy từ 180° -> 90° (Giảm dần theo chiều kim đồng hồ)
    if r1 > 1e-9:
        cx = x_web_right + r1
        cy = y_web_top - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(steps + 1):
            frac = i / steps
            theta = math.radians(180.0 - 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 4. Cạnh dưới của Flange phải, đi ra rìa phải ngoài cùng
    pts.append(QPointF(b, y_web_top))
    
    # 5. Cạnh đứng ngoài cùng bên phải Flange (Đi lên)
    pts.append(QPointF(b, h))
    
    # 6. Cạnh đỉnh trên cùng của Flange (Từ phải sang trái)
    pts.append(QPointF(0.0, h))
    
    # 7. Cạnh đứng ngoài cùng bên trái Flange (Đi xuống mặt đáy flange)
    pts.append(QPointF(0.0, y_web_top))
    
    # 8. Cạnh dưới của Flange trái tiến vào điểm bắt đầu Arc 2
    if r1 > 1e-9:
        pts.append(QPointF(x_web_left - r1, y_web_top))
    else:
        pts.append(QPointF(x_web_left, y_web_top))

    # Arc 2: Bo góc trái (Flange → Web)
    # Tâm: (x_web_left - r1, y_web_top - r1)
    # Góc chạy từ 270° -> 180° (Giảm dần theo chiều kim đồng hồ)
    if r1 > 1e-9:
        cx = x_web_left - r1
        cy = y_web_top - r1
        steps = max(8, int(math.ceil(r1 / 1.5)))
        for i in range(steps + 1):
            frac = i / steps
            theta = math.radians(270.0 - 90.0 * frac)
            pts.append(QPointF(cx + r1 * math.cos(theta), cy + r1 * math.sin(theta)))

    # 9. Đường đứng bên trái bụng đi xuống đáy để khép kín hình
    if r1 > 1e-9:
        pts.append(QPointF(x_web_left, y_web_top - r1))

    return pts


class DynamicTShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho T Section."""
        return {"H": 200, "B": 100, "Tw": 6, "Tf": 10}

    def _get_outline_points(self, dims, r1):
        h = dims.get("H", 0)
        b = dims.get("B", 0)
        tw = dims.get("Tw", 0)
        tf = dims.get("Tf", 0)
        return _t_shape_points(h, b, tw, tf, r1)

    def _get_dimension_specs(self, dims, is_sample=False):
        h = float(dims.get("H", 0))
        b = float(dims.get("B", 0))
        tw = float(dims.get("Tw", 0))
        tf = float(dims.get("Tf", 0))

        x_web_left = (b - tw) / 2.0
        x_web_right = (b + tw) / 2.0

        if is_sample:
            return [
                ((0.0, 0.0), (0.0, h), "H", "left"),
                ((0.0, h), (b, h), "B", "top"),
                ((x_web_left, h / 2), (x_web_right, h / 2), "Tw", "left"),
                ((b, h), (b, h - tf), "Tf", "right"),
            ]
        else:
            return [
                ((0.0, 0.0), (0.0, h), f"H = {h:.0f} mm", "left"),
                ((0.0, h), (b, h), f"B = {b:.0f} mm", "top"),
                ((x_web_left, h / 2), (x_web_right, h / 2), f"Tw = {tw:.0f} mm", "left"),
                ((b, h), (b, h - tf), f"Tf = {tf:.0f} mm", "right"),
            ]