"""QLabel tùy chỉnh để hiển thị hình vẽ kỹ thuật tham khảo."""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImageBox(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(300, 300)
        self.setStyleSheet(
            "background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 10px;"
        )
        self._current_path = None
        self._png_dir = ""

    def set_png_dir(self, png_dir: str):
        self._png_dir = png_dir

    def set_image(self, path: str):
        self._current_path = path
        self._render()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._render()

    def _render(self):
        if not self._current_path or not os.path.exists(self._current_path):
            self.setText(
                "ℹ️ Technical Drawing Image Not Found\nPlace your PNGs in "
                + self._png_dir
            )
            self.setPixmap(QPixmap())
            return
        pix = QPixmap(self._current_path)
        if pix.isNull():
            self.setText("⚠️ Failed to load image template.")
            self.setPixmap(QPixmap())
            return

        w = pix.size().width()
        h = pix.size().height()
        if w > 0 and h > 0:
            scaled = pix.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(scaled)
            self.setText("")