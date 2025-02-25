from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent

class PreviewDialog(QDialog):
    """Dialog for previewing the cropped image"""

    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Preview")
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.setStyleSheet("""
            QDialog {
                background-color: #2c2c2c;
                border: 1px solid #3c3c3c;
            }
            QLabel {
                color: white;
                font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
                font-size: 20px;
                font-weight: 500;
                padding: 10px;
            }
        """)



        layout = QVBoxLayout()
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        scaled_pixmap = pixmap.scaled(780, 580, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        preview_label.setPixmap(scaled_pixmap)
        layout.addWidget(preview_label)

        self.setLayout(layout)
        self._dragging = False
        self._offset = QPoint()


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._offset = event.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            self.move(self.pos() + event.pos() - self._offset)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)