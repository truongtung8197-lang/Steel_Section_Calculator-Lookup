"""Dynamic CHS/Pipe (Circular Hollow Section) widget."""

import math

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _circle_points(cx, cy, r, steps):
    """Sinh các điểm trên đường tròn, đi theo chiều KIM ĐỒNG HỒ."""
    pts = []
    for i in range(steps):
        frac = i / steps
        theta = math.radians(360.0 * frac)
        pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))
    return pts


def _chs_shape_points(od, t):
    """Tính outer và inner circle points cho CHS."""
    od = float(od)
    t = float(t)
    if od <= 0 or t <= 0:
        raise ValueError("Invalid dimensions for CHS")
    if 2 * t >= od:
        raise ValueError("Thickness too large for CHS")

    r_outer = od / 2.0
    r_inner = r_outer - t
    cx = r_outer
    cy = r_outer

    steps = max(24, int(math.ceil(r_outer / 1.5)))
    outer_pts = _circle_points(cx, cy, r_outer, steps)
    inner_pts = _circle_points(cx, cy, r_inner, steps)

    return outer_pts, inner_pts


class DynamicCHSShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho CHS/Pipe."""
        return {"OD": 50, "Thickness": 5}

    def _get_outline_points(self, dims, r1):
        od = float(dims.get("OD", 0))
        return [
            QPointF(0.0, 0.0),
            QPointF(od, 0.0),
            QPointF(od, od),
            QPointF(0.0, od),
        ]

    def _get_dimension_specs(self, dims, is_sample=False):
        od = float(dims.get("OD", 0))
        t = float(dims.get("Thickness", 0))
        
        if is_sample:
            return [
                ((0.0, od / 2), (od, od / 2), "OD", "bottom"),
                # Dim for thickness at 12 o'clock position (top of circle)
                ((od / 2, od), (od / 2, od - t), "t", "top"),
            ]
        else:
            return [
                ((0.0, od / 2), (od, od / 2), f"OD = {od:.0f} mm", "bottom"),
                # Dim for thickness at 12 o'clock position (top of circle)
                ((od / 2, od), (od / 2, od - t), f"t = {t:.0f} mm", "top"),
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

        od = float(dims_to_use.get("OD", 0))
        t = float(dims_to_use.get("Thickness", 0))

        if od <= 0 or t <= 0:
            if is_sample:
                with QPainter(self) as painter:
                    self._draw_fallback(painter, "Lỗi tính toán hình học")
            else:
                with QPainter(self) as painter:
                    self._draw_fallback(painter, "Dữ liệu không hợp lệ")
            return

        try:
            outer_pts, inner_pts = _chs_shape_points(od, t)
        except Exception:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Lỗi tính toán hình học")
            return

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

            for spec in self._get_dimension_specs(dims_to_use, is_sample=is_sample):
                if len(spec) < 4:
                    continue
                p1, p2, label, direction = spec
                wp1 = to_widget(QPointF(*p1))
                wp2 = to_widget(QPointF(*p2))
                self._draw_dimension_line(painter, wp1, wp2, label, direction)