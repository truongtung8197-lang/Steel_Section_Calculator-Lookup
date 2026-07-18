"""Tab 1: Manual Calculator - Bộ tính toán thủ công."""

import os
from typing import Dict, List

from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from core.constants import PNG_DIR, UNIT_CONVERSION, logger
from core.steel_types import STEEL_TYPES
from gui.widgets.dynamic_shapes.chs_shape import DynamicCHSShape
from gui.widgets.dynamic_shapes.i_shape import DynamicIShape
from gui.widgets.dynamic_shapes.l_shape import DynamicLShape
from gui.widgets.dynamic_shapes.plate_shape import DynamicPlateShape
from gui.widgets.dynamic_shapes.rhs_shape import DynamicRHSShape
from gui.widgets.dynamic_shapes.rod_shape import DynamicRodShape
from gui.widgets.dynamic_shapes.t_shape import DynamicTShape
from gui.widgets.dynamic_shapes.u_shape import DynamicUShape
from gui.widgets.image_box import ImageBox

DYNAMIC_SHAPE_MAP = {
    "angle": DynamicLShape,
    "ih": DynamicIShape,
    "channel": DynamicUShape,
    "rhs_shs": DynamicRHSShape,
    "tsection": DynamicTShape,
    "chs": DynamicCHSShape,
    "rod": DynamicRodShape,
    "plate": DynamicPlateShape,
}
DYNAMIC_SHAPE_KEYS = set(DYNAMIC_SHAPE_MAP.keys())


class CalculatorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inputs: List[QLineEdit] = []
        self.unit_combos: Dict[str, QComboBox] = {}
        self.current_raw_weight = None
        self._setup_ui()

    def _setup_ui(self):
        main_splitter = QSplitter(Qt.Horizontal, self)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(15)

        # Type combo + Clear button
        self.type_combo = QComboBox()
        self.type_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.type_combo.setToolTip("Select the type of steel section to calculate")
        for s in STEEL_TYPES:
            self.type_combo.addItem(s.name, s.key)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("ClearButton")
        self.clear_btn.setToolTip("Clear all input fields and reset to default values")

        type_header = QHBoxLayout()
        type_header.addWidget(self.type_combo)
        type_header.addWidget(self.clear_btn)

        type_box = QGroupBox("1. Select Steel Type")
        type_vbox = QVBoxLayout(type_box)
        type_vbox.addLayout(type_header)

        # Form inputs
        self.form_host = QWidget()
        self.form_layout = QFormLayout(self.form_host)
        self.form_layout.setLabelAlignment(Qt.AlignLeft)
        self.form_layout.setFormAlignment(Qt.AlignTop)
        self.form_layout.setVerticalSpacing(12)
        self.form_layout.setHorizontalSpacing(20)

        self.image_box = ImageBox()
        self.image_box.set_png_dir(PNG_DIR)

        self.image_stack = QStackedWidget()
        self.image_stack.addWidget(self.image_box)  # 0 = static PNG

        self._dynamic_widgets = {}
        for key, widget_cls in DYNAMIC_SHAPE_MAP.items():
            widget = widget_cls()
            self.image_stack.addWidget(widget)
            self._dynamic_widgets[key] = widget

        input_box = QGroupBox("2. Section Dimensions")
        input_box.setToolTip("Enter the geometric dimensions of the steel section")
        input_vbox = QVBoxLayout(input_box)
        input_vbox.addWidget(self.form_host)

        # Result card
        self.result_card = QWidget()
        self.result_card.setObjectName("ResultCard")
        card_layout = QVBoxLayout(self.result_card)

        self.result_title = QLabel("CALCULATED THEORETICAL WEIGHT")
        self.result_title.setObjectName("ResultTitle")
        self.result_title.setAlignment(Qt.AlignCenter)

        self.result_label = QLabel("0.00 kg/m")
        self.result_label.setObjectName("ResultLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.calc_copy_btn = QPushButton("Copy Value")
        self.calc_copy_btn.setObjectName("CalcCopyButton")
        self.calc_copy_btn.setToolTip("Copy the calculated weight to clipboard")
        self.calc_copy_btn.clicked.connect(self.copy_calc_result)

        card_layout.addWidget(self.result_title)
        card_layout.addWidget(self.result_label)
        card_layout.addWidget(self.calc_copy_btn, alignment=Qt.AlignCenter)

        left_layout.addWidget(type_box)
        left_layout.addWidget(input_box)
        left_layout.addWidget(self.result_card)
        left_layout.addStretch(1)

        # Right panel: image
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(20, 20, 20, 20)
        img_box = QGroupBox("Cross-Section Dimension Reference")
        img_box.setToolTip(
            "Technical drawing showing dimension labels for the selected steel type"
        )
        img_vbox = QVBoxLayout(img_box)
        img_vbox.addWidget(self.image_stack)
        right_layout.addWidget(img_box)

        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setStretchFactor(0, 6)
        main_splitter.setStretchFactor(1, 4)
        left_widget.setMinimumWidth(320)

        calc_layout = QVBoxLayout(self)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.addWidget(main_splitter)

        self.type_combo.currentIndexChanged.connect(self.rebuild_inputs)
        self.clear_btn.clicked.connect(self.clear_inputs)
        self.rebuild_inputs()
        self._update_input_font(self.width())

    def _update_input_font(self, width: int):
        """Scale input font so numbers stay legible when window shrinks.

        The left panel gets ~60% of the width; derive a sensible pt size
        from that, clamped to a readable range. Applies to line edits,
        unit combos, and action buttons so nothing gets clipped.
        """
        left_width = max(width * 6 // 10, 320)
        pt = left_width / 60.0
        pt = max(9.0, min(pt, 13.0))
        font = self.font()
        font.setPointSizeF(pt)
        for edit in self.inputs:
            edit.setFont(font)
        for combo in self.unit_combos.values():
            combo.setFont(font)
        if hasattr(self, "type_combo"):
            self.type_combo.setFont(font)
        if hasattr(self, "clear_btn"):
            self.clear_btn.setFont(font)
        if hasattr(self, "calc_copy_btn"):
            self.calc_copy_btn.setFont(font)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_input_font(self.width())

    def current_type(self):
        key = self.type_combo.currentData()
        return next(s for s in STEEL_TYPES if s.key == key)

    def rebuild_inputs(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self.inputs.clear()
        self.unit_combos.clear()

        steel = self.current_type()
        validator = QDoubleValidator(0.001, 999999.0, 3, self)
        validator.setNotation(QDoubleValidator.StandardNotation)

        # Collect Length field to add it after corner radius
        length_container = None
        length_edit = None
        length_unit_combo = None
        
        for label, unit in steel.fields:
            # Skip Length for now, will add it after corner radius
            if label == "Length":
                continue
            
            container = QWidget()
            cl = QHBoxLayout(container)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(5)

            edit = QLineEdit()
            edit.setProperty("field_label", label)
            edit.setProperty("original_unit", unit)
            edit.setPlaceholderText("0.00")
            edit.setValidator(validator)
            edit.setMinimumWidth(70)
            edit.setToolTip(f"Enter {label} value")

            unit_combo = QComboBox()
            unit_combo.addItems(["mm", "cm", "m", "inch"])
            unit_combo.setCurrentText(unit if unit in ["mm", "cm", "m", "inch"] else "mm")
            unit_combo.setMaximumWidth(70)
            unit_combo.setToolTip("Select unit of measurement")
            unit_combo.currentTextChanged.connect(
                lambda text, lbl=label: self.on_unit_changed(lbl, text)
            )

            cl.addWidget(edit, 1)
            cl.addWidget(unit_combo)
            self.inputs.append(edit)
            self.unit_combos[label] = unit_combo

            edit.textChanged.connect(self.calculate)
            self.form_layout.addRow(f"<b>{label}</b>", container)

        # Corner radius
        if steel.key in ["ih", "channel", "angle", "rhs_shs", "tsection"]:
            rc = QWidget()
            rcl = QHBoxLayout(rc)
            rcl.setContentsMargins(0, 0, 0, 0)
            rcl.setSpacing(5)

            re = QLineEdit()
            re.setProperty("field_label", "r1")
            re.setProperty("original_unit", "mm")
            re.setText("0")
            re.setValidator(validator)
            re.setMinimumWidth(70)
            re.setToolTip("Corner radius (r1). Default 0 for sharp corners")
            re.textChanged.connect(self.calculate)

            ruc = QComboBox()
            ruc.addItems(["mm", "cm", "inch"])
            ruc.setCurrentText("mm")
            ruc.setMaximumWidth(70)
            ruc.setToolTip("Select unit for r1")
            ruc.currentTextChanged.connect(lambda text, lbl="r1": self.on_unit_changed(lbl, text))

            rcl.addWidget(re, 1)
            rcl.addWidget(ruc)
            self.inputs.append(re)
            self.unit_combos["r1"] = ruc
            self.form_layout.addRow("<b>r1 (Corner Radius)</b>", rc)

        # Add Length field after corner radius
        for label, unit in steel.fields:
            if label == "Length":
                container = QWidget()
                cl = QHBoxLayout(container)
                cl.setContentsMargins(0, 0, 0, 0)
                cl.setSpacing(5)

                edit = QLineEdit()
                edit.setProperty("field_label", label)
                edit.setProperty("original_unit", unit)
                edit.setPlaceholderText("0.00")
                edit.setValidator(validator)
                edit.setMinimumWidth(70)
                edit.setToolTip("Length in meters (always in m for beams)")
                
                if unit == "m":
                    edit.setText("1")

                unit_combo = QComboBox()
                unit_combo.addItems(["mm", "cm", "m", "inch"])
                unit_combo.setCurrentText(unit if unit in ["mm", "cm", "m", "inch"] else "mm")
                unit_combo.setMaximumWidth(70)
                unit_combo.setToolTip("Select unit of measurement")
                unit_combo.currentTextChanged.connect(
                    lambda text, lbl=label: self.on_unit_changed(lbl, text)
                )

                cl.addWidget(edit, 1)
                cl.addWidget(unit_combo)
                self.inputs.append(edit)
                self.unit_combos[label] = unit_combo

                edit.textChanged.connect(self.calculate)
                self.form_layout.addRow(f"<b>{label}</b>", container)
                break

        # Quantity
        qty = QLineEdit()
        qty.setProperty("field_label", "Quantity")
        qty.setPlaceholderText("1")
        qty.setText("1")
        qty.setMinimumWidth(70)
        qty.setValidator(validator)
        qty.setToolTip("Quantity of steel sections")
        qty.textChanged.connect(self.calculate)
        self.form_layout.addRow("<b>Quantity</b>", qty)
        self.inputs.append(qty)

        # Image / dynamic shape
        if steel.key in DYNAMIC_SHAPE_KEYS:
            self.image_stack.setCurrentIndex(list(DYNAMIC_SHAPE_MAP.keys()).index(steel.key) + 1)
        else:
            img_path = os.path.join(PNG_DIR, steel.image_file)
            self.image_box.set_image(img_path)
            self.image_stack.setCurrentIndex(0)
        self.type_combo.setToolTip(steel.tooltip)
        self._update_input_font(self.width())
        self.calculate()

    def on_unit_changed(self, field_label: str, new_unit: str):
        try:
            edit = None
            for inp in self.inputs:
                if inp.property("field_label") == field_label:
                    edit = inp
                    break
            if not edit or not edit.text().strip():
                return
            old_val = float(edit.text().strip())
            old_unit = edit.property("original_unit")
            if old_unit == "m":
                return
            val_mm = old_val * UNIT_CONVERSION.get(old_unit, 1.0)
            new_val = val_mm / UNIT_CONVERSION.get(new_unit, 1.0)
            edit.setText(f"{new_val:.3f}")
            edit.setProperty("original_unit", new_unit)
        except Exception as e:
            logger.error(f"Unit conversion error: {e}")

    def calculate(self):
        steel = self.current_type()
        try:
            values = {}
            for edit in self.inputs:
                label = edit.property("field_label")
                text = edit.text().strip()
                if not text:
                    raise ValueError(f"Missing {label}")
                values[label] = float(text)

            try:
                steel.validator(values)
            except ValueError:
                msg = self._validation_msg(steel.key, values)
                self.result_label.setText("Invalid Input")
                self.result_label.setStyleSheet("color: #ef4444;")
                self.current_raw_weight = None
                if steel.key in DYNAMIC_SHAPE_KEYS:
                    self._dynamic_widgets[steel.key].set_dimensions({}, 0)
                return

            if steel.key in DYNAMIC_SHAPE_KEYS:
                self._dynamic_widgets[steel.key].set_dimensions(values, values.get("r1", 0))

            qty = values.get("Quantity", 1.0)
            base = steel.calc(values)
            total = base * qty
            self.current_raw_weight = total

            if steel.key == "plate":
                suffix = "kg"
            else:
                lm = values.get("Length", 1.0)
                suffix = "kg/m" if (abs(lm - 1.0) < 1e-9 and abs(qty - 1.0) < 1e-9) else "kg"

            self.result_label.setText(f"{total:,.2f} {suffix}")
            self.result_label.setStyleSheet("color: #0284c7;")
        except (ValueError, KeyError):
            self.result_label.setText("---")
            self.result_label.setStyleSheet("color: #94a3b8;")
            self.current_raw_weight = None
            if steel.key in DYNAMIC_SHAPE_KEYS:
                self._dynamic_widgets[steel.key].set_dimensions({}, 0)

    def _validation_msg(self, key: str, v: dict) -> str:
        msgs = {
            "plate": [
                (v.get("Length", 0) <= 0, "Length must be > 0"),
                (v.get("Width", 0) <= 0, "Width must be > 0"),
                (v.get("Thickness", 0) <= 0, "Thickness must be > 0"),
            ],
            "ih": [
                (v.get("Tw", 0) >= v.get("B", 0), "Tw must be < B"),
                ((2 * v.get("Tf", 0)) >= v.get("H", 0), "2×Tf must be < H"),
            ],
            "channel": [
                (v.get("Tw", 0) >= v.get("B", 0), "Tw must be < B"),
                ((2 * v.get("Tf", 0)) >= v.get("H", 0), "2×Tf must be < H"),
            ],
            "tsection": [
                (v.get("Tw", 0) >= v.get("B", 0), "Tw must be < B"),
                (v.get("Tf", 0) >= v.get("H", 0), "Tf must be < H"),
            ],
            "angle": [
                (v.get("Thickness", 0) >= v.get("Leg A", 0), "Thickness must be < Leg A"),
                (v.get("Thickness", 0) >= v.get("Leg B", 0), "Thickness must be < Leg B"),
            ],
            "rhs_shs": [
                ((2 * v.get("Thickness", 0)) >= v.get("Width", 0), "2×Thickness must be < Width"),
                ((2 * v.get("Thickness", 0)) >= v.get("Height", 0), "2×Thickness must be < Height"),
            ],
            "chs": [
                ((2 * v.get("Thickness", 0)) >= v.get("OD", 0), "2×Thickness must be < OD"),
            ],
            "rod": [
                (v.get("Diameter", 0) <= 0, "Diameter must be > 0"),
            ],
        }
        for cond, msg in msgs.get(key, []):
            if cond:
                return msg
        return "Invalid input"

    def copy_calc_result(self):
        if self.current_raw_weight is not None:
            QApplication.clipboard().setText(f"{self.current_raw_weight:.2f}")

    def clear_inputs(self):
        self.type_combo.blockSignals(True)
        steel = self.current_type()
        for edit in self.inputs:
            lbl = edit.property("field_label")
            if lbl == "Quantity":
                edit.setText("1")
            elif lbl == "Length" and steel.key != "plate":
                edit.setText("1")
            else:
                edit.clear()
        self.type_combo.blockSignals(False)
        self.current_raw_weight = None
        self.calculate()