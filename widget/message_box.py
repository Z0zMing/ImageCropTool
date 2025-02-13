from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class StyleMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)

        self.setStyleSheet("""
            QMessageBox {
                background-color: #2c2c2c;
                border: 1px solid #3c3c3c;
                border-radius: 5px;
            }
            QMessageBox QLabel {
                color: white;
                font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
                font-size: 20px;
                font-weight: 500;
                padding: 10px;
            }
            QMessageBox QPushButton {
                background-color: #3b3b3b;
                border: none;
                border-radius: 3px;
                color: white;
                font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
                font-size: 20px;
                font-weight: 500;
                min-width: 70px;
                padding: 6px 12px;
            }
            QMessageBox QPushButton:hover {
                background-color: #4b4b4b;
            }
            QMessageBox QPushButton:pressed {
                background-color: #2b2b2b;
            }
        """)

    @staticmethod
    def warning(parent, title, text):
        msg = StyleMessageBox(parent)
        warning_icon = QIcon("icons/warning.svg")
        msg.setIconPixmap(warning_icon.pixmap(QSize(50, 50))) 
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec()

    @staticmethod
    def information(parent, title, text):
        msg = StyleMessageBox(parent)
        info_icon = QIcon("icons/information.svg")
        msg.setIconPixmap(info_icon.pixmap(QSize(50, 50))) 
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        return msg.exec()
