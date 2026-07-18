"""Dynamic RHS/SHS (Rectangular/Square Hollow Section) widget."""

import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _rounded_rect_points(w, h, r, steps):
    """Sinh các điểm cho hình chữ nhật bo tròn 4 góc.

    Đi theo chiều KIM ĐỒNG HỒ (clockwise).
    Tất cả arc đều CCW (góc tăng dần) trong model space.
    """
    pts = []

    if r > 1e-9:
        # Bottom-left arc: 180° → 270° CCW
        cx, cy = r, r
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(180.0 + 90.0 * frac)
            pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))
    else:
        pts.append(QPointF(0.0, 0.0))

    # Bottom edge (left → right)
    pts.append(QPointF(w - r, 0.0))

    if r > 1e-9:
        # Bottom-right arc: 270° → 360° CCW
        cx, cy = w - r, r
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(270.0 + 90.0 * frac)
            pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))

    # Right edge (bottom → top)
    pts.append(QPointF(w, h - r))

    if r > 1e-9:
        # Top-right arc: 0° → 90° CCW
        cx, cy = w - r, h - r
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(0.0 + 90.0 * frac)
            pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))

    # Top edge (right → left)
    pts.append(QPointF(r, h))

    if r > 1e-9:
        # Top-left arc: 90° → 180° CCW
        cx, cy = r, h - r
        for i in range(1, steps + 1):
            frac = i / steps
            theta = math.radians(90.0 + 90.0 * frac)
            pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))

    # Left edge (top → bottom)
    pts.append(QPointF(0.0, r))

    return pts


def _rhs_shape_points(w, h, t, r1):
    """Tính outline điểm mặt cắt thép hộp RHS/SHS.

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Trả về 2 list điểm: outer (CW) và inner (CCW) để tạo lỗ rỗng.
    """
    w = float(w)
    h = float(h)
    t = float(t)
    r1 = float(r1)

    if w <= 0 or h <= 0 or t <= 0:
        raise ValueError("Invalid dimensions for RHS/SHS")
    if 2 * t >= w or 2 * t >= h:
        raise ValueError("Thickness too large for RHS/SHS")
    if r1 < 0:
        raise ValueError("Corner radius must be non-negative")

    # Outer radius Ro = r1 + t, inner radius Ri = r1
    # Khi r1 = 0: cả trong và ngoài đều vuông góc (không bo)
    if r1 > 1e-9:
        ro = r1 + t
        ri = r1
    else:
        ro = 0.0
        ri = 0.0

    # Clamp outer radius
    max_ro = min(w, h) / 2.0
    if ro > max_ro:
        ro = max_ro

    # Clamp inner radius
    inner_w = w - 2 * t
    inner_h = h - 2 * t
    if inner_w > 0 and inner_h > 0:
        max_ri = min(inner_w, inner_h) / 2.0
        if ri > max_ri:
            ri = max_ri
    else:
        ri = 0

    steps_outer = max(8, int(math.ceil(ro / 1.5))) if ro > 1e-9 else 0
    steps_inner = max(8, int(math.ceil(ri / 1.5))) if ri > 1e-9 else 0

    outer_pts = _rounded_rect_points(w, h, ro, steps_outer)

    # Inner rectangle: (w-2t) × (h-2t), offset by (t, t)
    if inner_w > 0 and inner_h > 0:
        inner_pts = _rounded_rect_points(inner_w, inner_h, ri, steps_inner)
        # Offset inner points
        inner_pts = [QPointF(p.x() + t, p.y() + t) for p in inner_pts]
    else:
        inner_pts = []

    return outer_pts, inner_pts


class DynamicRHSShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho RHS/SHS."""
        return {"Width": 100, "Height": 50, "Thickness": 5}

    def _get_outline_points(self, dims, r1):
        """Trả về outer boundary để base class tính bounding box."""
        w = float(dims.get("Width", 0))
        h = float(dims.get("Height", 0))
        return [
            QPointF(0.0, 0.0),
            QPointF(w, 0.0),
            QPointF(w, h),
            QPointF(0.0, h),
        ]

    def _get_dimension_specs(self, dims, is_sample=False):
        w = float(dims.get("Width", 0))
        h = float(dims.get("Height", 0))
        t = float(dims.get("Thickness", 0))

        if is_sample:
            return [
                ((0.0, 0.0), (0.0, h), "H", "left"),
                ((0.0, 0.0), (w, 0.0), "W", "bottom"),
                ((w, 0.0), (w, t), "t", "right"),
            ]
        else:
            return [
                ((0.0, 0.0), (0.0, h), f"H = {h:.0f} mm", "left"),
                ((0.0, 0.0), (w, 0.0), f"W = {w:.0f} mm", "bottom"),
                ((w, 0.0), (w, t), f"t = {t:.0f} mm", "right"),
            ]

    def paintEvent(self, event):
        """Override paintEvent để vẽ mặt cắt rỗng (outer + inner path)."""
        # Determine if we're in sample mode
        is_sample = self._is_sample_mode()
        
        # Use sample dimensions if in sample mode
        dims_to_use = self._dims
        r1_to_use = self._r1
        
        if is_sample:
            sample_dims = self._get_sample_dims()
            if not sample_dims:
                with QPainter(self) as painter:
                    self._draw_fallback(painter, "Nhập đủ thông số để xem hình")
                return
            dims_to_use = sample_dims
            r1_to_use = 0.0  # Always use r1=0 for sample mode

        w = float(dims_to_use.get("Width", 0))
        h = float(dims_to_use.get("Height", 0))
        t = float(dims_to_use.get("Thickness", 0))
        r = float(r1_to_use)

        if w <= 0 or h <= 0 or t <= 0:
            if is_sample:
                with QPainter(self) as painter:
                    self._draw_fallback(painter, "Lỗi tính toán hình học")
            else:
                with QPainter(self) as painter:
                    self._draw_fallback(painter, "Dữ liệu không hợp lệ")
            return

        try:
            outer_pts, inner_pts = _rhs_shape_points(w, h, t, r)
        except Exception:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Lỗi tính toán hình học")
            return

        if not outer_pts or len(outer_pts) < 3:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Dữ liệu không hợp lệ")
            return

        # Scale và center (giống base class)
        w_w, h_w = self.width(), self.height()
        margin = 60
        avail_w = w_w - margin * 2
        avail_h = h_w - margin * 2
        if avail_w <= 0 or avail_h <= 0:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Cửa sổ quá nhỏ")
            return

        xs = [p.x() for p in outer_pts]
        ys = [p.y() for p in outer_pts]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        data_w = max_x - min_x if max_x > min_x else 1.0
        data_h = max_y - min_y if max_y > min_y else 1.0

        scale = min(avail_w / data_w, avail_h / data_h)
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        widget_cx = w_w / 2.0
        widget_cy = h_w / 2.0

        def to_widget(p):
            return QPointF(
                widget_cx + (p.x() - cx) * scale,
                widget_cy - (p.y() - cy) * scale,
            )

        # Build path: outer CW + inner CCW → tạo lỗ rỗng (OddEvenFill)
        path = QPainterPath()

        poly_outer = [to_widget(p) for p in outer_pts]
        path.moveTo(poly_outer[0])
        for p in poly_outer[1:]:
            path.lineTo(p)
        path.closeSubpath()

        if inner_pts:
            poly_inner = [to_widget(p) for p in inner_pts]
            path.moveTo(poly_inner[0])
            for p in poly_inner[1:]:
                path.lineTo(p)
            path.closeSubpath()

        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor("#0f172a"), 2))
            painter.setBrush(QBrush(QColor("#e0f2fe")))
            painter.drawPath(path)

            # Vẽ DIM
            for spec in self._get_dimension_specs(dims_to_use, is_sample=is_sample):
                if len(spec) < 4:
                    continue
                p1, p2, label, direction = spec
                wp1 = to_widget(QPointF(*p1))
                wp2 = to_widget(QPointF(*p2))
                self._draw_dimension_line(painter, wp1, wp2, label, direction)
