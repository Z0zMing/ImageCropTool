from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class PreviewDialog(QDialog):
    """Dialog for previewing the cropped image"""

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        scaled_pixmap = pixmap.scaled(780, 580, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        preview_label.setPixmap(scaled_pixmap)
        layout.addWidget(preview_label)

        self.setLayout(layout)
