from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal

class ToolTipsButton(QPushButton):
    """Button with tooltip message"""
    tooltip_message = Signal(str)

    def __init__(self, text, tooltip_text, parent=None):
        super().__init__(text, parent)
        self._tooltip_text = tooltip_text

    def enterEvent(self, event):
        self.tooltip_message.emit(self._tooltip_text)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.tooltip_message.emit("")
        super().leaveEvent(event)