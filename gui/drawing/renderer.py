"""QPainter-based renderer cho bản vẽ mặt cắt thép động."""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen

from gui.drawing.dimension import (
    DIM_COLOR,
    TEXT_COLOR,
    draw_horizontal_dimension,
    draw_vertical_dimension,
)
from gui.drawing.section_geometry import get_angle_path


# Màu sắc
BG_COLOR = QColor("#ffffff")
SECTION_FILL = QColor("#e0f2fe")  # Xanh nhạt
SECTION_STROKE = QColor("#0284c7")  # Xanh đậm
SECTION_STROKE_WIDTH = 2.0
PADDING_RATIO = 0.1  # 10% padding từ viền widget
DIM_OFFSET_RATIO = 0.08  # 8% chiều rộng widget cho dimension offset


class DynamicRenderer:
    """Render bản vẽ mặt cắt thép dùng QPainter.

    Nhận loại thép + tham số kích thước, tự động scale và vẽ
    mặt cắt kèm dimension lines.
    """

    def __init__(self):
        self.section_type: str = ""
        self.params: dict = {}

    def set_section(self, section_type: str, params: dict):
        """Thiết lập loại thép và tham số kích thước."""
        self.section_type = section_type
        self.params = params

    def render(self, painter: QPainter, width: float, height: float):
        """Render bản vẽ vào painter với kích thước widget cho trước."""
        if not self.section_type or not self.params:
            self._draw_placeholder(painter, width, height, "No section selected")
            return

        # Chọn hàm lấy path theo loại thép
        path = self._get_path()
        if path is None:
            self._draw_placeholder(
                painter, width, height, f"Unknown section: {self.section_type}"
            )
            return

        # Tính bounding box của path (tọa độ gốc chưa scale)
        bbox = path.boundingRect()
        if bbox.isEmpty() or bbox.width() < 0.001 or bbox.height() < 0.001:
            self._draw_placeholder(painter, width, height, "Invalid parameters")
            return

        # --- Tính tỷ lệ scale ---
        padding = min(width, height) * PADDING_RATIO
        draw_w = width - 2 * padding
        draw_h = height - 2 * padding

        # Bỏ thêm khoảng cho dimension lines (phía dưới và bên trái)
        dim_offset = min(width, height) * DIM_OFFSET_RATIO
        draw_w -= dim_offset * 0.5
        draw_h -= dim_offset * 0.5

        scale_x = draw_w / bbox.width() if bbox.width() > 0 else 1.0
        scale_y = draw_h / bbox.height() if bbox.height() > 0 else 1.0
        scale = min(scale_x, scale_y)

        # --- Tính translation để căn giữa ---
        scaled_w = bbox.width() * scale
        scaled_h = bbox.height() * scale
        offset_x = (width - scaled_w) / 2.0
        offset_y = (height - scaled_h) / 2.0

        # --- Vẽ nền ---
        painter.fillRect(0, 0, int(width), int(height), BG_COLOR)

        # --- Vẽ mặt cắt ---
        painter.save()
        painter.translate(offset_x, offset_y)
        painter.scale(scale, scale)

        # Vẽ fill
        painter.fillPath(path, QBrush(SECTION_FILL))
        # Vẽ stroke
        pen = QPen(SECTION_STROKE, SECTION_STROKE_WIDTH / scale)
        painter.setPen(pen)
        painter.drawPath(path)

        painter.restore()

        # --- Vẽ dimension lines (sau khi scale) ---
        self._draw_dimensions(
            painter, bbox, scale, offset_x, offset_y, dim_offset, width, height
        )

    def _get_path(self) -> QPainterPath:
        """Lấy QPainterPath theo loại thép."""
        # TODO: mở rộng khi thêm các type khác
        mapping = {
            "angle": get_angle_path,
        }
        func = mapping.get(self.section_type)
        if func:
            return func(self.params)
        return None

    def _draw_dimensions(
        self,
        painter: QPainter,
        bbox: QRectF,
        scale: float,
        offset_x: float,
        offset_y: float,
        dim_offset: float,
        widget_w: float,
        widget_h: float,
    ):
        """Vẽ dimension lines cho mặt cắt."""
        # Lấy các tham số chính
        if self.section_type == "angle":
            self._draw_angle_dimensions(
                painter, bbox, scale, offset_x, offset_y, dim_offset
            )

    def _draw_angle_dimensions(
        self,
        painter: QPainter,
        bbox: QRectF,
        scale: float,
        offset_x: float,
        offset_y: float,
        dim_offset: float,
    ):
        """Vẽ dimension cho thép góc L."""
        a = self.params.get("Leg A", 0)
        b = self.params.get("Leg B", 0)
        t = self.params.get("Thickness", 0)
        r1 = self.params.get("r1", 0) or 0

        # Tọa độ gốc (chưa scale) của các điểm
        # Như đã định nghĩa trong section_geometry, tâm tại (0,0)
        # Nên tọa độ các điểm là:
        # P0: (-b/2, -a/2) - góc dưới-trái
        # P1: (b/2, -a/2)  - góc dưới-phải
        # P2: (b/2, t - a/2) - góc gấp dưới-phải
        # P4: (t - b/2, a/2) - góc trên (cạnh đứng)
        # P5: (-b/2, a/2)  - góc trên-trái

        cx = -b / 2.0
        cy = -a / 2.0

        # Hàm chuyển tọa độ gốc → widget
        def to_widget(px, py):
            return (
                px * scale + offset_x,
                py * scale + offset_y,
            )

        # --- Dimension cho Leg B (cạnh ngang, đáy) ---
        y_bot = cy  # y của cạnh đáy
        x_left = cx
        x_right = cx + b
        w_x1, w_y1 = to_widget(x_left, y_bot)
        w_x2, _ = to_widget(x_right, y_bot)

        # Dimension bên dưới đáy
        draw_horizontal_dimension(
            painter,
            w_x1,
            w_x2,
            w_y1,
            f"{b:.1f}",
            offset=dim_offset + 10,
            unit="mm",
            color=DIM_COLOR,
        )

        # --- Dimension cho Leg A (cạnh đứng, trái) ---
        x_left_edge = cx  # x của cạnh trái
        y_top = cy + a
        y_bottom = cy
        _, w_y_bot = to_widget(x_left_edge, y_bottom)
        w_x_left_edge, w_y_top = to_widget(x_left_edge, y_top)

        # Dimension bên trái cạnh đứng
        draw_vertical_dimension(
            painter,
            w_x_left_edge,
            w_y_bot,
            w_y_top,
            f"{a:.1f}",
            offset=dim_offset + 10,
            unit="mm",
            color=DIM_COLOR,
        )

        # --- Dimension cho Thickness (cạnh ngang bên phải) ---
        y_thick = cy + t  # y của cạnh trên cánh ngang
        x_thick_left = cx + b - t
        x_thick_right = cx + b
        wt_x1, wt_y = to_widget(x_thick_left, y_thick)
        wt_x2, _ = to_widget(x_thick_right, y_thick)

        # Dimension phía trên cạnh ngang
        draw_horizontal_dimension(
            painter,
            wt_x1,
            wt_x2,
            wt_y - 5,  # hơi dịch lên trên
            f"{t:.1f}",
            offset=15,
            unit="mm",
            color=DIM_COLOR,
        )

        # --- Dimension cho r1 nếu có ---
        if r1 > 0:
            # Vẽ đường chú thích góc bo tại vị trí góc trong
            # Tọa độ góc trong: (t - b/2 + r1, t - a/2 + r1)
            corner_x = cx + t + r1 / 2
            corner_y = cy + t + r1 / 2
            w_cx, w_cy = to_widget(corner_x, corner_y)

            pen = QPen(DIM_COLOR, 1.5)
            painter.setPen(pen)
            font = QFont("Consolas", 10)
            painter.setFont(font)
            painter.setPen(TEXT_COLOR)
            painter.drawText(QPointF(w_cx - 15, w_cy - 10), f"r₁={r1:.0f}")

    def _draw_placeholder(
        self,
        painter: QPainter,
        width: float,
        height: float,
        message: str = "",
    ):
        """Vẽ placeholder khi chưa có dữ liệu."""
        painter.fillRect(0, 0, int(width), int(height), BG_COLOR)
        if message:
            font = QFont("Consolas", 12)
            painter.setFont(font)
            painter.setPen(QColor("#94a3b8"))
            painter.drawText(
                QPointF(20, height / 2.0),
                f"⚠️ {message}",
            )
