"""Base class cho dynamic shape widgets."""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QFont,
    QBrush,
    QFontMetrics,
    QPainterPath,
)
from PySide6.QtWidgets import QWidget


class DynamicShapeWidget(QWidget):
    """Base widget vẽ mặt cắt thép động bằng QPainter."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dims = {}
        self._r1 = 0.0
        self.setMinimumSize(300, 300)

    def set_dimensions(self, dims: dict, r1: float = 0.0):
        self._dims = dims if dims else {}
        self._r1 = float(r1)
        self.update()

    def _get_outline_points(self, dims, r1):
        raise NotImplementedError

    def _get_dimension_specs(self, dims):
        return []

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self._dims:
            self._draw_fallback(painter, "Nhập đủ thông số để xem hình")
            return

        try:
            points = self._get_outline_points(self._dims, self._r1)
        except Exception:
            self._draw_fallback(painter, "Lỗi tính toán hình học")
            return

        if not points or len(points) < 3:
            self._draw_fallback(painter, "Dữ liệu không hợp lệ")
            return

        w = self.width()
        h = self.height()
        margin = 60
        avail_w = w - margin * 2
        avail_h = h - margin * 2
        if avail_w <= 0 or avail_h <= 0:
            self._draw_fallback(painter, "Cửa sổ quá nhỏ")
            return

        xs = [p.x() for p in points]
        ys = [p.y() for p in points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        data_w = max_x - min_x if max_x > min_x else 1.0
        data_h = max_y - min_y if max_y > min_y else 1.0

        scale = min(avail_w / data_w, avail_h / data_h)
        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0
        widget_cx = w / 2.0
        widget_cy = h / 2.0

        def to_widget(p: QPointF) -> QPointF:
            return QPointF(
                widget_cx + (p.x() - cx) * scale,
                widget_cy - (p.y() - cy) * scale,
            )

        poly = [to_widget(p) for p in points]
        path = QPainterPath()
        if poly:
            path.moveTo(poly[0])
            for p in poly[1:]:
                path.lineTo(p)
            path.closeSubpath()

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

    def _draw_dimension_line(self, painter, p1, p2, label, direction):
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        length = (dx * dx + dy * dy) ** 0.5
        if length < 1e-6:
            return

        ux = dx / length
        uy = dy / length
        nx = -uy
        ny = ux

        offset_dist = 30.0
        if direction == "left" and nx > 0:
            nx, ny = -nx, -ny
        if direction == "bottom" and ny < 0:
            nx, ny = -nx, -ny
        if direction == "top" and ny > 0:
            nx, ny = -nx, -ny
        if direction == "right" and nx < 0:
            nx, ny = -nx, -ny

        a = QPointF(p1.x() + nx * offset_dist, p1.y() + ny * offset_dist)
        b = QPointF(p2.x() + nx * offset_dist, p2.y() + ny * offset_dist)

        painter.setPen(QPen(QColor("#94a3b8"), 1, Qt.DashLine))
        painter.drawLine(p1, a)
        painter.drawLine(p2, b)

        painter.setPen(QPen(QColor("#475569"), 1))
        painter.drawLine(a, b)

        arrow_size = 6.0
        self._draw_solid_arrow(painter, a, ux, uy, arrow_size)
        self._draw_solid_arrow(painter, b, -ux, -uy, arrow_size)

        mx = (a.x() + b.x()) / 2.0
        my = (a.y() + b.y()) / 2.0

        font = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font)
        fm = QFontMetrics(font)
        tw = fm.horizontalAdvance(str(label))
        th = fm.height()

        painter.save()
        if abs(dx) < 1e-3:
            painter.translate(mx, my)
            painter.rotate(-90)
            rect = QRectF(-tw / 2 - 4, -th / 2, tw + 8, th)
            painter.fillRect(rect, QBrush(QColor("#ffffff")))
            painter.setPen(QColor("#0f172a"))
            painter.drawText(rect, Qt.AlignCenter, str(label))
        else:
            rect = QRectF(mx - tw / 2 - 4, my - th / 2, tw + 8, th)
            painter.fillRect(rect, QBrush(QColor("#ffffff")))
            painter.setPen(QColor("#0f172a"))
            painter.drawText(rect, Qt.AlignCenter, str(label))
        painter.restore()

    def _draw_solid_arrow(self, painter, tip, ux, uy, size):
        nx = -uy
        ny = ux
        p1 = QPointF(
            tip.x() - ux * size + nx * (size * 0.4),
            tip.y() - uy * size + ny * (size * 0.4),
        )
        p2 = QPointF(
            tip.x() - ux * size - nx * (size * 0.4),
            tip.y() - uy * size - ny * (size * 0.4),
        )

        painter.save()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor("#475569")))
        painter.drawPolygon([tip, p1, p2])
        painter.restore()

    def _draw_fallback(self, painter, message="Nhập đủ thông số để xem hình"):
        painter.fillRect(self.rect(), QColor("#f8fafc"))
        painter.setPen(QPen(QColor("#64748b")))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(self.rect(), Qt.AlignCenter, message)
