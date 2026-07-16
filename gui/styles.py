"""Stylesheet cho toàn bộ ứng dụng."""


def apply_styles(window):
    """Áp dụng stylesheet cho MainWindow."""
    window.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 11pt;
            color: #1e293b;
            background-color: #f8fafc;
        }
        QTabWidget::pane {
            border: 1px solid #e2e8f0;
            background: #f8fafc;
            border-radius: 8px;
        }
        QTabBar::tab {
            background: #e2e8f0;
            color: #475569;
            padding: 10px 20px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: 500;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background: #ffffff;
            color: #0f172a;
            border: 1px solid #e2e8f0;
            border-bottom-color: #f8fafc;
            font-weight: 600;
        }
        QGroupBox {
            font-weight: 600;
            font-size: 11.5pt;
            color: #0f172a;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            margin-top: 5px;
            padding: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            background-color: #f8fafc;
        }
        QLineEdit, QComboBox, QListWidget {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 6px 8px;
            color: #334155;
        }
        QLineEdit { min-height: 22px; }
        QComboBox { min-height: 22px; }
        QListWidget { padding: 5px; background: #ffffff; }
        QListWidget::item {
            padding: 10px 12px;
            border-radius: 6px;
            margin-bottom: 2px;
        }
        QListWidget::item:hover { background: #f1f5f9; color: #0f172a; }
        QListWidget::item:selected { background: #0284c7; color: white; }
        QLineEdit:focus, QComboBox:focus {
            border: 2px solid #3b82f6;
            background: #ffffff;
        }
        QPushButton#ClearButton {
            background: #f1f5f9;
            color: #64748b;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 8px 14px;
            font-weight: 500;
        }
        QPushButton#ClearButton:hover { background: #e2e8f0; color: #334155; }

        QPushButton#RowCopyButton {
            background: #ffffff;
            color: #0284c7;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: 600;
        }
        QPushButton#RowCopyButton:hover {
            background: #f1f5f9;
            border-color: #0284c7;
        }

        QWidget#ResultCard {
            background-color: #e0f2fe;
            border: 1px solid #bae6fd;
            border-radius: 12px;
            padding: 18px;
        }
        QPushButton#CalcCopyButton {
            background: #ffffff;
            color: #0284c7;
            border: 1px solid #bae6fd;
            border-radius: 8px;
            padding: 8px 20px;
            font-weight: 600;
            margin-top: 5px;
        }
        QPushButton#CalcCopyButton:hover {
            background: #f0f9ff;
            border-color: #0284c7;
        }
        QWidget#LookupCard {
            background-color: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 15px;
        }
        QLabel#ResultTitle {
            color: #64748b;
            font-size: 8.5pt;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        QLabel#ResultLabel {
            font-size: 26pt;
            font-weight: 800;
            color: #0284c7;
        }
        QLabel#LookupSectionName {
            font-size: 18pt;
            font-weight: 800;
            color: #0f172a;
            border-bottom: 2px solid #cbd5e1;
            padding-bottom: 8px;
            margin-bottom: 5px;
        }
        QLabel#LookupValue {
            font-size: 12pt;
            font-weight: 700;
            color: #0369a1;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QLabel { background: transparent; }
        QScrollBar:vertical {
            border: none;
            background: #f8fafc;
            width: 10px;
            margin: 15px 0 15px 0;
        }
        QScrollBar::handle:vertical {
            background: #cbd5e1;
            min-height: 20px;
            border-radius: 5px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0px;
        }
    """)