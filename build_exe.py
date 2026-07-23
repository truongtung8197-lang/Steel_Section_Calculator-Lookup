#!/usr/bin/env python3
"""
Build script để đóng gói ứng dụng Steel Section Calculator thành file .exe
Sử dụng PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

# Đường dẫn thư mục gốc của dự án
BASE_DIR = Path(__file__).parent.absolute()

# Cấu hình build
APP_NAME = "SteelCalculator"
ENTRY_POINT = "main.py"

# Lưu ý: Không đóng gói file dữ liệu vào .exe
# Người dùng cần đặt alias.xlsx và steel_db.json cùng thư mục với .exe
DATA_FILES = []

# Các module ẩn cần import (tránh lỗi missing module)
HIDDEN_IMPORTS = [
    "PySide6",
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
    "PySide6.QtPrintSupport",
    "openpyxl",
    "openpyxl.cell",
    "openpyxl.styles",
    "core",
    "core.constants",
    "core.geometry",
    "core.steel_types",
    "data",
    "data.data_manager",
    "gui",
    "gui.dialogs",
    "gui.styles",
    "gui.tabs",
    "gui.tabs.calc_tab",
    "gui.tabs.lookup_tab",
    "gui.widgets",
    "gui.widgets.dynamic_shapes",
    "gui.widgets.dynamic_shapes.base_shape",
]

# Qt plugins cần thiết
QT_PLUGINS = [
    "platforms",
    "styles",
]


def build_exe():
    """Thực hiện build file .exe với PyInstaller"""

    print("=" * 60)
    print(f"Building {APP_NAME}.exe...")
    print("=" * 60)

    # Tạo thư mục dist nếu chưa có
    dist_dir = BASE_DIR / "dist"
    dist_dir.mkdir(exist_ok=True)

    # Build PyInstaller command
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        APP_NAME,
        "--onefile",  # Đóng gói thành 1 file .exe
        "--windowed",  # Không hiển thị console
        "--clean",  # Xóa cache trước khi build
        "--noconfirm",  # Không hỏi xác nhận ghi đè
        ENTRY_POINT,
    ]

    # Không include file dữ liệu vào .exe
    # Người dùng cần copy alias.xlsx và steel_db.json vào thư mục dist/ sau khi build
    print(
        "[INFO] Data files (alias.xlsx, steel_db.json) must be placed in the same folder as the .exe"
    )

    # Thêm hidden imports
    for module in HIDDEN_IMPORTS:
        cmd.extend(["--hidden-import", module])

    # Thêm Qt plugins
    for plugin in QT_PLUGINS:
        cmd.extend(["--collect-all", f"PySide6.{plugin}"])

    # Thư mục output
    cmd.extend(["--distpath", str(dist_dir)])
    cmd.extend(["--workpath", str(BASE_DIR / "build")])
    cmd.extend(["--specpath", str(BASE_DIR)])

    print("\n[BUILD] Command:")
    print(" ".join(cmd))
    print("\n[BUILD] Starting build process...\n")

    # Chạy PyInstaller
    try:
        result = subprocess.run(
            cmd, cwd=BASE_DIR, check=True, capture_output=False, text=True
        )

        print("\n" + "=" * 60)
        print(f"[SUCCESS] Build completed successfully!")
        print(f"[OUTPUT] {dist_dir / (APP_NAME + '.exe')}")
        print("=" * 60)

        return True

    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print(f"[ERROR] Build failed with exit code {e.returncode}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
