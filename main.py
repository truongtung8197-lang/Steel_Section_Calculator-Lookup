"""Steel Management & Calculator Pro - Entry Point."""

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QTabWidget

from core.constants import EXCEL_PATH, JSON_PATH, logger
from data.data_manager import DataManager
from gui.dialogs import show_about, show_help
from gui.styles import apply_styles
from gui.tabs.calc_tab import CalculatorTab
from gui.tabs.lookup_tab import LookupTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steel Management & Calculator Pro")
        self.resize(1150, 750)
        self.setMinimumSize(1000, 680)

        # Load data
        data_mgr = DataManager(EXCEL_PATH, JSON_PATH, logger)
        self.excel_data = data_mgr.load_data()

        # Setup UI
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._create_menu_bar()
        self._init_tabs()
        apply_styles(self)

        logger.info("Application started successfully")

    def _create_menu_bar(self):
        menubar = self.menuBar()

        help_menu = menubar.addMenu("&Help")

        about_action = help_menu.addAction("&About")
        about_action.triggered.connect(lambda: show_about(self))

        help_action = help_menu.addAction("&User Guide")
        help_action.triggered.connect(lambda: show_help(self))

    def _init_tabs(self):
        calc_tab = CalculatorTab()
        lookup_tab = LookupTab(self.excel_data)
        self.tabs.addTab(calc_tab, "Manual Calculator")
        self.tabs.addTab(lookup_tab, "Steel Section Lookup")


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    try:
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Application crashed: {e}", exc_info=True)
        raise