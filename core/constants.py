"""Constants and configuration - độc lập, không phụ thuộc thư viện ngoài."""

import logging
import os
import sys

# Mật độ thép (kg/mm³)
DENSITY_FACTOR = 7.85e-6  # tương đương 7850 kg/m³

# Hệ số chuyển đổi đơn vị (về mm)
UNIT_CONVERSION = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "inch": 25.4}

# Tự động lấy đường dẫn thư mục chứa file .py hoặc .exe
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cấu hình logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Đường dẫn tài nguyên
PNG_DIR = os.path.join(BASE_DIR, "STEEL TYPE png")
EXCEL_PATH = os.path.join(BASE_DIR, "alias.xlsx")
JSON_PATH = os.path.join(BASE_DIR, "steel_db.json")

APP_VERSION = "1.6"