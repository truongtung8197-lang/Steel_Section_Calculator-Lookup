"""Dialog About và User Guide."""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from core.constants import APP_VERSION


def show_about(parent):
    QMessageBox.about(
        parent,
        "About Steel Management & Calculator Pro",
        f"Steel Management & Calculator Pro v{APP_VERSION}\n\n"
        "A tool for calculating steel weight and looking up standard steel sections.\n\n"
        "Technology: Python 3.x, PySide6, openpyxl\n"
        "Developer: Development Team\n"
        f"Year: {datetime.now().year}",
    )


def show_help(parent):
    help_text = """
    <h2>Steel Management & Calculator Pro - User Guide</h2>

    <h3>Tab 1: Manual Calculator</h3>
    <ol>
        <li><b>Select Steel Type:</b> Choose the type of steel section from the dropdown</li>
        <li><b>Enter Dimensions:</b> Input the section dimensions in the form fields</li>
        <li><b>Quantity:</b> Enter the quantity (default is 1)</li>
        <li><b>Result:</b> The calculated weight will appear automatically</li>
        <li><b>Copy:</b> Click "Copy Value" to copy the result to clipboard</li>
        <li><b>Clear:</b> Click "Clear" to reset all input fields</li>
    </ol>

    <h3>Tab 2: Steel Section Lookup</h3>
    <ol>
        <li><b>Select Steel Library:</b> Choose the steel library/database</li>
        <li><b>Search:</b> Enter keywords to search for sections (e.g., "WC 500" or "500")</li>
        <li><b>Select Profile:</b> Click on a profile from the list to view details</li>
        <li><b>Copy:</b> Click "Copy" buttons to copy individual values</li>
    </ol>

    <h3>Tips:</h3>
    <ul>
        <li>All dimensions are in millimeters (mm) unless otherwise specified</li>
        <li>Length for beams/channels is in meters (m)</li>
        <li>You can search with multiple keywords separated by spaces</li>
        <li>Hover over input fields for tooltips and guidance</li>
    </ul>

    <h3>Steel Density:</h3>
    <p>Standard steel density: 7850 kg/m³ (7.85e-6 kg/mm³)</p>
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle("User Guide")
    msg_box.setTextFormat(Qt.RichText)
    msg_box.setText(help_text)
    msg_box.exec()