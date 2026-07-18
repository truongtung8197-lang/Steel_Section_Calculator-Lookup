"""Dynamic Plate widget."""

from PySide6.QtCore import QPointF

from gui.widgets.dynamic_shapes.base_shape import DynamicShapeWidget


def _plate_shape_points(length, width):
    """Tính outline điểm mặt cắt thép Plate.

    Tọa độ model: góc dưới-trái ở (0,0), X sang phải, Y lên trên.
    Hình chữ nhật đơn giản: length × width (không dùng thickness).
    """
    length = float(length)
    width = float(width)

    if length <= 0 or width <= 0:
        raise ValueError("Invalid dimensions for Plate")

    return [
        QPointF(0.0, 0.0),
        QPointF(length, 0.0),
        QPointF(length, width),
        QPointF(0.0, width),
    ]


class DynamicPlateShape(DynamicShapeWidget):
    def _get_sample_dims(self):
        """Trả về dimensions mẫu cho Plate."""
        return {"Length": 100, "Width": 50}

    def _get_outline_points(self, dims, r1):
        length = float(dims.get("Length", 0))
        width = float(dims.get("Width", 0))
        return _plate_shape_points(length, width)

    def _get_dimension_specs(self, dims, is_sample=False):
        length = float(dims.get("Length", 0))
        width = float(dims.get("Width", 0))

        if is_sample:
            return [
                ((0.0, 0.0), (0.0, width), "W", "left"),
                ((0.0, 0.0), (length, 0.0), "L", "bottom"),
            ]
        else:
            return [
                ((0.0, 0.0), (0.0, width), f"W = {width:.0f} mm", "left"),
                ((0.0, 0.0), (length, 0.0), f"L = {length:.0f} mm", "bottom"),
            ]
