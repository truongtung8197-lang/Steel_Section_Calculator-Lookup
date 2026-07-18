"""Vẽ dimension line và chú thích kích thước cho bản vẽ mặt cắt thép."""

import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen


# Màu sắc dimension
DIM_COLOR = QColor("#dc2626")  # Đỏ
DIM_COLOR_ALT = QColor("#2563eb")  # Xanh dương (cho r1, góc bo)
TEXT_COLOR = QColor("#1e293b")  # Xám đậm
LINE_WIDTH = 1.5
ARROW_SIZE = 8.0  # px
TEXT_OFFSET = 4  # px
FONT_SIZE = 10


def _draw_arrowhead(
    painter: QPainter, tip: QPointF, angle: float, size: float = ARROW_SIZE
):
    """Vẽ mũi tên tại điểm tip theo hướng angle (radians)."""
    p1 = QPointF(
        tip.x() - size * math.cos(angle - math.pi / 6),
        tip.y() - size * math.sin(angle - math.pi / 6),
    )
    p2 = QPointF(
        tip.x() - size * math.cos(angle + math.pi / 6),
        tip.y() - size * math.sin(angle + math.pi / 6),
    )
    painter.drawLine(tip, p1)
    painter.drawLine(tip, p2)


def draw_horizontal_dimension(
    painter: QPainter,
    x1: float,
    x2: float,
    y: float,
    value: str,
    offset: float = 25.0,
    unit: str = "mm",
    color: QColor = DIM_COLOR,
):
    """Vẽ dimension line ngang.

    Parameters
    ----------
    painter : QPainter
    x1, x2 : float - Tọa độ x 2 đầu
    y : float - Tọa độ y của điểm đo
    value : str - Giá trị hiển thị
    offset : float - Khoảng cách từ điểm đo đến dimension line
    unit : str - Đơn vị
    color : QColor - Màu sắc
    """
    pen = QPen(color, LINE_WIDTH)
    painter.setPen(pen)

    # Extension lines (nét đứt ngắn)
    ext_pen = QPen(color, 1.0, Qt.DashLine)
    painter.setPen(ext_pen)
    painter.drawLine(QPointF(x1, y), QPointF(x1, y + offset * 0.6))
    painter.drawLine(QPointF(x2, y), QPointF(x2, y + offset * 0.6))

    # Dimension line (nét liền)
    dim_y = y + offset
    painter.setPen(pen)
    painter.drawLine(QPointF(x1, dim_y), QPointF(x2, dim_y))

    # Mũi tên 2 đầu
    _draw_arrowhead(painter, QPointF(x1, dim_y), 0.0)  # hướng phải
    _draw_arrowhead(painter, QPointF(x2, dim_y), math.pi)  # hướng trái

    # Text
    mid_x = (x1 + x2) / 2.0
    text = f"{value} {unit}"
    font = QFont("Consolas", FONT_SIZE)
    painter.setFont(font)
    painter.setPen(TEXT_COLOR)
    text_rect = painter.fontMetrics().boundingRect(text)
    text_x = mid_x - text_rect.width() / 2.0
    text_y = dim_y + TEXT_OFFSET + text_rect.height()
    painter.drawText(QPointF(text_x, text_y), text)


def draw_vertical_dimension(
    painter: QPainter,
    x: float,
    y1: float,
    y2: float,
    value: str,
    offset: float = 25.0,
    unit: str = "mm",
    color: QColor = DIM_COLOR,
):
    """Vẽ dimension line dọc.

    Parameters
    ----------
    painter : QPainter
    x : float - Tọa độ x của điểm đo
    y1, y2 : float - Tọa độ y 2 đầu
    value : str - Giá trị hiển thị
    offset : float - Khoảng cách từ điểm đo đến dimension line
    unit : str - Đơn vị
    color : QColor - Màu sắc
    """
    pen = QPen(color, LINE_WIDTH)
    painter.setPen(pen)

    # Extension lines (nét đứt)
    ext_pen = QPen(color, 1.0, Qt.DashLine)
    painter.setPen(ext_pen)
    painter.drawLine(QPointF(x, y1), QPointF(x - offset * 0.6, y1))
    painter.drawLine(QPointF(x, y2), QPointF(x - offset * 0.6, y2))

    # Dimension line (nét liền) - bên trái điểm đo
    dim_x = x - offset
    painter.setPen(pen)
    painter.drawLine(QPointF(dim_x, y1), QPointF(dim_x, y2))

    # Mũi tên 2 đầu
    _draw_arrowhead(painter, QPointF(dim_x, y1), math.pi / 2)  # hướng xuống
    _draw_arrowhead(painter, QPointF(dim_x, y2), -math.pi / 2)  # hướng lên

    # Text (xoay 90°)
    mid_y = (y1 + y2) / 2.0
    text = f"{value} {unit}"
    font = QFont("Consolas", FONT_SIZE)
    painter.setFont(font)
    painter.setPen(TEXT_COLOR)

    painter.save()
    painter.translate(dim_x - TEXT_OFFSET - 8, mid_y)
    painter.rotate(-90)
    text_rect = painter.fontMetrics().boundingRect(text)
    painter.drawText(QPointF(-text_rect.width() / 2.0, text_rect.height() / 2.0), text)
    painter.restore()
