"""Standalone test cho bản vẽ động thép góc L (Angle / L Section).

Chạy script này để xem trực quan hình vẽ mặt cắt thép L
với các tham số có thể thay đổi bằng slider.

Usage:
    python tests/test_drawing_angle.py
"""

import sys
import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QFont, QColor, QPen
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# Thêm thư mục gốc vào path để import được các module
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from gui.drawing.renderer import DynamicRenderer
from gui.drawing.section_geometry import get_angle_path
from gui.drawing.dimension import (
    draw_horizontal_dimension,
    draw_vertical_dimension,
    DIM_COLOR,
)


class DrawingWidget(QWidget):
    """Widget vẽ mặt cắt thép L, cập nhật theo tham số."""

    def __init__(self, renderer: DynamicRenderer):
        super().__init__()
        self.renderer = renderer
        self.setMinimumSize(500, 450)
        self.setStyleSheet("background: white; border: 1px solid #e2e8f0;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.renderer.render(painter, self.width(), self.height())
        painter.end()


class ControlPanel(QWidget):
    """Panel điều khiển tham số cho thép L."""

    def __init__(self, on_change):
        super().__init__()
        self.on_change = on_change
        self._setup_ui()
        self.setMaximumWidth(280)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tiêu đề
        title = QLabel("⚙️ Angle / L Section Parameters")
        title.setStyleSheet("font: bold 14px; color: #1e293b; padding-bottom: 5px;")
        layout.addWidget(title)

        # Leg A
        self.leg_a_spin = self._create_spin_group(layout, "Leg A (mm):", 10, 500, 100)
        # Leg B
        self.leg_b_spin = self._create_spin_group(layout, "Leg B (mm):", 10, 500, 80)
        # Thickness
        self.thick_spin = self._create_spin_group(
            layout, "Thickness t (mm):", 1, 100, 10
        )
        # r1 corner radius
        self.r1_spin = self._create_spin_group(layout, "Corner r₁ (mm):", 0, 50, 0)

        # Separator
        layout.addSpacing(10)
        sep = QLabel("━" * 30)
        sep.setStyleSheet("color: #cbd5e1;")
        layout.addWidget(sep)

        # Nút Pre-set samples
        presets_title = QLabel("📐 Sample Profiles:")
        presets_title.setStyleSheet("font: bold 12px; color: #475569;")
        layout.addWidget(presets_title)

        btn_style = """
            QPushButton {
                background: #f1f5f9; border: 1px solid #cbd5e1;
                border-radius: 6px; padding: 6px 12px;
                text-align: left; font: 10px;
            }
            QPushButton:hover { background: #e2e8f0; }
        """

        samples = [
            ("L100x100x10 (r₁=0)", 100, 100, 10, 0),
            ("L100x100x10 (r₁=8)", 100, 100, 10, 8),
            ("L150x90x12 (r₁=10)", 150, 90, 12, 10),
            ("L200x100x14 (r₁=12)", 200, 100, 14, 12),
            ("L80x40x6 (r₁=0)", 80, 40, 6, 0),
        ]

        for label, a, b, t, r1 in samples:
            btn = QPushButton(label)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(
                lambda checked, a=a, b=b, t=t, r1=r1: self._set_preset(a, b, t, r1)
            )
            layout.addWidget(btn)

        layout.addStretch()

        # Thông tin
        info = QLabel("💡 Adjust sliders to see\nthe drawing update in real-time.")
        info.setStyleSheet("color: #94a3b8; font: 9px;")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

    def _create_spin_group(
        self, layout, label: str, min_v: int, max_v: int, default: int
    ):
        """Tạo 1 row: label + spinbox + slider."""
        row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet("font: 10px; color: #334155;")
        lbl.setMinimumWidth(100)

        spin = QSpinBox()
        spin.setRange(min_v, max_v)
        spin.setValue(default)
        spin.setSuffix(" mm")
        spin.setStyleSheet("font: 10px;")
        spin.setFixedWidth(90)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_v, max_v)
        slider.setValue(default)
        slider.setStyleSheet("""
            QSlider::groove:horizontal { height: 4px; background: #cbd5e1; border-radius: 2px; }
            QSlider::handle:horizontal { background: #0284c7; width: 14px; height: 14px;
                                          margin: -5px 0; border-radius: 7px; }
        """)

        # Kết nối spin ↔ slider
        spin.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(spin.setValue)

        # Kết nối thay đổi → callback
        def on_value_changed(val):
            self.on_change()

        spin.valueChanged.connect(on_value_changed)

        row.addWidget(lbl)
        row.addWidget(spin)
        row.addWidget(slider, 1)
        layout.addLayout(row)

        return spin

    def _set_preset(self, a, b, t, r1):
        """Set preset sample values."""
        self.leg_a_spin.setValue(a)
        self.leg_b_spin.setValue(b)
        self.thick_spin.setValue(t)
        self.r1_spin.setValue(r1)

    def get_params(self) -> dict:
        """Lấy tham số hiện tại."""
        return {
            "Leg A": float(self.leg_a_spin.value()),
            "Leg B": float(self.leg_b_spin.value()),
            "Thickness": float(self.thick_spin.value()),
            "r1": float(self.r1_spin.value()),
        }


class MainDialog(QDialog):
    """Dialog chính test thép L."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Dynamic Drawing Test — Angle / L Section [v2.0]")
        self.setMinimumSize(900, 600)

        # Renderer
        self.renderer = DynamicRenderer()

        # Layout chính
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Drawing widget (trái)
        self.drawing_widget = DrawingWidget(self.renderer)

        # Control panel (phải)
        self.control = ControlPanel(self._on_params_changed)
        self.control.setStyleSheet("background: #f8fafc; border-radius: 8px;")

        main_layout.addWidget(self.drawing_widget, 1)
        main_layout.addWidget(self.control)

        # Render lần đầu
        self._on_params_changed()

    def _on_params_changed(self):
        """Cập nhật renderer và vẽ lại."""
        params = self.control.get_params()
        self.renderer.set_section("angle", params)
        self.drawing_widget.update()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    dialog = MainDialog()
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
