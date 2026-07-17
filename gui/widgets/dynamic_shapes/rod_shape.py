"""Dynamic Rod/Round Bar widget."""

import math

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _rod_shape_points(d):
    """Tính circle points cho Rod."""
    d = float(d)
    if d <= 0:
        raise ValueError("Invalid diameter for Rod")

    r = d / 2.0
    cx = r
    cy = r
    steps = max(24, int(math.ceil(r / 1.5)))

    pts = []
    for i in range(steps):
        frac = i / steps
        theta = math.radians(360.0 * frac)
        pts.append(QPointF(cx + r * math.cos(theta), cy + r * math.sin(theta)))
    return pts


class DynamicRodShape(DynamicShapeWidget):
    def _get_outline_points(self, dims, r1):
        d = float(dims.get("Diameter", 0))
        return [
            QPointF(0.0, 0.0),
            QPointF(d, 0.0),
            QPointF(d, d),
            QPointF(0.0, d),
        ]

    def _get_dimension_specs(self, dims):
        d = float(dims.get("Diameter", 0))
        return [
            ((0.0, d / 2), (d, d / 2), f"D = {d:.0f} mm", "bottom"),
        ]

    def paintEvent(self, event):
        if not self._dims:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Nhap du thong so de xem hinh")
            return

        d = float(self._dims.get("Diameter", 0))
        if d <= 0:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Du lieu khong hop le")
            return

        try:
            pts = _rod_shape_points(d)
        except Exception:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Loi tinh toan hinh hoc")
            return

        w_w, h_w = self.width(), self.height()
        margin = 60
        avail_w = w_w - margin * 2
        avail_h = h_w - margin * 2
        if avail_w <= 0 or avail_h <= 0:
            with QPainter(self) as painter:
                self._draw_fallback(painter, "Cua so qua nho")
            return

        xs = [p.x() for p in pts]
        ys = [p.y() for p in pts]
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
        poly = [to_widget(p) for p in pts]
        path.moveTo(poly[0])
        for p in poly[1:]:
            path.lineTo(p)
        path.closeSubpath()

        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QPen(QColor("#0f172a"), 2))
            painter.setBrush(QBrush(QColor("#e0f2fe")))
            painter.drawPath(path)

            for spec in self._get_dimension_specs(self._dims):
                if len(spec) < 4:
                    continue
                p1, p2, label, direction = spec
                wp1 = to_widget(QPointF(*p1))
                wp2 = to_widget(QPointF(*p2))
                self._draw_dimension_line(painter, wp1, wp2, label, direction)