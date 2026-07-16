"""Tab 2: Steel Section Lookup - Tra cứu profile thép."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from core.constants import logger


class LookupTab(QWidget):
    def __init__(self, excel_data: list, parent=None):
        super().__init__(parent)
        self.excel_data = excel_data
        self._setup_ui()

    def _setup_ui(self):
        splitter = QSplitter(Qt.Horizontal, self)

        # Left panel
        left_panel = QWidget()
        left_vbox = QVBoxLayout(left_panel)
        left_vbox.setContentsMargins(20, 20, 20, 20)
        left_vbox.setSpacing(10)

        search_box = QGroupBox("Search Section Name")
        search_layout = QVBoxLayout(search_box)
        search_layout.setSpacing(8)

        self.lookup_type_combo = QComboBox()
        self.lookup_type_combo.addItem("I Beam / H Beam", "ih")
        self.lookup_type_combo.addItem("PFC / U Channel", "channel")
        self.lookup_type_combo.addItem("Shape VN (HINH_VN)", "hinh_vn")
        self.lookup_type_combo.addItem("Pipe / Tube (Ong,Hop)", "ong_hop")
        self.lookup_type_combo.currentIndexChanged.connect(self._on_type_changed)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("e.g. 'WC 500' or '500 WC'...")

        search_layout.addWidget(QLabel("<b>Select Steel Library:</b>"))
        search_layout.addWidget(self.lookup_type_combo)
        search_layout.addWidget(QLabel("<b>Enter Search Keywords:</b>"))
        search_layout.addWidget(self.search_edit)

        list_box = QGroupBox("Matching Standard Profiles")
        list_layout = QVBoxLayout(list_box)
        self.lookup_list = QListWidget()
        list_layout.addWidget(self.lookup_list)

        left_vbox.addWidget(search_box)
        left_vbox.addWidget(list_box)

        # Right panel
        right_panel = QWidget()
        right_vbox = QVBoxLayout(right_panel)
        right_vbox.setContentsMargins(20, 20, 20, 20)

        detail_box = QGroupBox("Profile Specifications Data")
        detail_layout = QVBoxLayout(detail_box)

        self.lookup_card = QWidget()
        self.lookup_card.setObjectName("LookupCard")
        self.card_vbox = QVBoxLayout(self.lookup_card)
        self.card_vbox.setSpacing(10)
        self._reset_card()

        detail_layout.addWidget(self.lookup_card)
        right_vbox.addWidget(detail_box)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 6)

        total_layout = QVBoxLayout(self)
        total_layout.setContentsMargins(0, 0, 0, 0)
        total_layout.addWidget(splitter)

        self.search_edit.textChanged.connect(self._filter)
        self.lookup_list.itemClicked.connect(self._display_details)
        self._filter()

    def _on_type_changed(self):
        self.search_edit.clear()
        self._filter()
        self._reset_card()

    def _reset_card(self):
        self._clear_layout(self.card_vbox)
        lbl = QLabel("No Selection")
        lbl.setObjectName("LookupSectionName")
        lbl.setAlignment(Qt.AlignCenter)
        self.card_vbox.addWidget(lbl)
        self.card_vbox.addStretch(1)

    def _clear_layout(self, layout):
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
            else:
                self._clear_layout(item.layout())

    def _filter(self):
        query = self.search_edit.text().lower().strip()
        self.lookup_list.clear()

        if not query:
            item = QListWidgetItem("Enter search keywords to find profiles...")
            item.setFlags(Qt.NoItemFlags)
            self.lookup_list.addItem(item)
            return

        keywords = query.split()
        current_type = self.lookup_type_combo.currentData()

        if not self.excel_data:
            item = QListWidgetItem("⚠️ Excel data not loaded. Check file path or sheet names.")
            item.setFlags(Qt.NoItemFlags)
            self.lookup_list.addItem(item)
            return

        matches = 0
        for row in self.excel_data:
            if row["type"] != current_type:
                continue
            if all(kw in row["D"].lower() for kw in keywords):
                item = QListWidgetItem(row["D"])
                item.setData(Qt.UserRole, row)
                self.lookup_list.addItem(item)
                matches += 1

        if matches == 0:
            item = QListWidgetItem("No matching profiles found")
            item.setFlags(Qt.NoItemFlags)
            self.lookup_list.addItem(item)

    def _display_details(self, item):
        self._clear_layout(self.card_vbox)
        row = item.data(Qt.UserRole)
        if not row:
            return

        # Title
        title = QLabel(row["D"])
        title.setObjectName("LookupSectionName")
        title.setAlignment(Qt.AlignCenter)
        title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.card_vbox.addWidget(title)

        def add_row(title_text, display_text, raw_val):
            t = QLabel(f"<b>{title_text}:</b>")
            v = QLabel(display_text)
            v.setObjectName("LookupValue")
            v.setTextInteractionFlags(Qt.TextSelectableByMouse)

            btn = QPushButton("Copy")
            btn.setObjectName("RowCopyButton")
            if raw_val and raw_val != "---":
                btn.clicked.connect(lambda checked=False, val=raw_val: QApplication.clipboard().setText(val))
            else:
                btn.setEnabled(False)

            h = QHBoxLayout()
            h.addWidget(v, 1)
            h.addWidget(btn)
            self.card_vbox.addWidget(t)
            self.card_vbox.addLayout(h)

        t = row["type"]
        if t in ["ih", "channel"]:
            add_row("Original Section", row["E"], row["E"])
            fv = row["F"]
            add_row("Weight per meter", f"{fv} kg/m" if fv != "---" else "---", fv)
            add_row("Substitute Section", row["N"], row["N"])
            ov = row["O"]
            add_row("Weight per meter", f"{ov} kg/m" if ov != "---" else "---", ov)
        else:
            bv = row["B"]
            add_row("Weight per meter", f"{bv} kg/m" if bv != "---" else "---", bv)
            add_row("Note", row["C"], row["C"])

        self.card_vbox.addStretch(1)