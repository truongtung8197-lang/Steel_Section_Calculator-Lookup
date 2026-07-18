"""Định nghĩa tọa độ mặt cắt 2D cho từng loại thép.

Mỗi hàm trả về một QPainterPath là đường bao mặt cắt,
có tâm tại (0, 0) để dễ scale và dịch chuyển sau này.
"""

import math
from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPainterPath


def get_angle_path(params: dict) -> QPainterPath:
    """Tạo QPainterPath cho mặt cắt thép góc chữ L (Angle / L Section).

    Parameters
    ----------
    params : dict
        Với các keys:
        - "Leg A" (float): Chiều dài cạnh đứng (mm)
        - "Leg B" (float): Chiều dài cạnh ngang (mm)
        - "Thickness" (float): Độ dày thép (mm)
        - "r1" (float, optional): Bán kính bo góc trong (mm). Mặc định 0.

    Returns
    -------
    QPainterPath
        Đường bao mặt cắt, tâm tại (0,0).
        Nếu r1 > 0, góc trong được bo tròn bằng arc.
    """
    a = params["Leg A"]
    b = params["Leg B"]
    t = params["Thickness"]
    r1 = params.get("r1", 0.0) or 0.0

    # Giới hạn r1 không vượt quá kích thước cho phép
    max_r1 = min(a, b) / 2.0
    r1 = max(0.0, min(r1, max_r1))

    path = QPainterPath()

    # --- Đường bao ngoài (outer contour) ---
    # Đi từ dưới-trái, theo chiều kim đồng hồ:
    # (0,0) → (B,0) → (B,t) → (t,t) → (t,A) → (0,A) → về (0,0)

    # Các điểm chính của L (chưa bo góc):
    # P0: (0, 0)         - góc dưới-trái (cạnh ngang)
    # P1: (B, 0)         - góc dưới-phải (cạnh ngang)
    # P2: (B, t)         - góc trên-phải (cạnh ngang) - điểm gấp
    # P3: (t, t)         - góc trong (điểm bo r1)
    # P4: (t, A)         - góc trên (cạnh đứng)
    # P5: (0, A)         - góc trên-trái (cạnh đứng)

    if r1 > 0 and r1 < t:
        # --- CÓ bo góc trong ---
        # Chia đường bao thành các đoạn, góc trong tại (t, t) được bo
        # Đoạn từ P0 → P1 (đáy)
        path.moveTo(0.0, 0.0)
        path.lineTo(b, 0.0)

        # Đoạn từ P1 → P2 (cạnh phải cánh ngang)
        path.lineTo(b, t)

        # Bo góc trong tại (t, t): từ (b, t) → (t, t) → (t, a)
        # Vẽ cung tròn góc 90°, bán kính r1
        # Tâm cung: (t + r1, t + r1)
        # Góc bắt đầu: 270° (từ hướng 3 giờ, ngược chiều kim đồng hồ)
        cx = t + r1
        cy = t + r1
        # Điểm bắt đầu cung: (cx + r1, cy) = (t + 2*r1, t + r1)
        # Nhưng ta muốn cung từ (t, t+r1) đến (t+r1, t)
        # Dùng arcTo với góc 270° → 360° (tức -90° → 0° trong Qt)
        # Điểm bắt đầu thực tế: (t, t + r1), điều này yêu cầu lineTo trước
        # Đi từ (b, t) → (t + r1, t) → bo cung → (t, t + r1) → (t, a)
        # Thực tế: từ P2 (b, t) → điểm bắt đầu cung (t + r1, t)
        if t + r1 < b:
            path.lineTo(t + r1, t)
        else:
            path.lineTo(t, t)

        # Vẽ cung bo góc trong 90° (từ 0° đến 90°, tức quadrant thứ nhất)
        # Qt: góc 0° = 3 giờ (phải), đi ngược chiều kim đồng hồ
        # Ta muốn cung từ (t+r1, t) [hướng 0°] đến (t, t+r1) [hướng 270°]
        # Trong Qt, arcTo(rect, startAngle, spanAngle) với góc đo bằng 1/16 độ
        rect = QRectF(t, t, 2 * r1, 2 * r1)
        path.arcTo(rect, 0.0, -90.0)  # Từ 0° đến -90° (theo chiều kim đồng hồ)

        # Đoạn từ điểm cuối cung (t, t + r1) lên P4 (t, a)
        path.lineTo(t, a)

        # Đoạn từ P4 → P5 (cạnh trái)
        path.lineTo(0.0, a)

        # Đóng path về (0,0)
        path.closeSubpath()

    else:
        # --- KHÔNG bo góc (r1 = 0) ---
        path.moveTo(0.0, 0.0)
        path.lineTo(b, 0.0)
        path.lineTo(b, t)
        path.lineTo(t, t)
        path.lineTo(t, a)
        path.lineTo(0.0, a)
        path.closeSubpath()

    # --- Dịch tâm về (0,0) ---
    # Tính bounding box hiện tại
    # Dịch sao cho tâm hình học nằm tại (0,0)
    cx = b / 2.0
    cy = a / 2.0
    path.translate(-cx, -cy)

    return path


def _get_bounding_rect(path: QPainterPath) -> QRectF:
    """Tính bounding rect của path (tiện cho debug)."""
    return path.boundingRect()
