from PySide6.QtCore import Qt, QRect, QSize, QPoint, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPixmap, QTransform, QCursor
from PySide6.QtWidgets import QLabel, QMessageBox
from widget.message_box import StyleMessageBox


class Canvas(QLabel):
    """Widget for displaying and interacting with the image"""

    selection_size_changed = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.rect = QRect(0, 0, 0, 0)
        self.dragging = False
        self.scale_factor = 1.0
        self.offset = QPoint(0, 0)
        self.original_pixmap = None
        self.displayed_pixmap = None
        self.display_scale = 1.0
        self.original_size = None
        self.rotation = 0
        self.setMinimumSize(400, 300)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("QLabel { background-color: #2c2c2c; }")
        self.resize_margin = 10
        self.resizing = False
        self.resize_edge = None
        self.last_pos = None
        self.last_rect = None
        self.show_selection = False

        self.setMouseTracking(True)

    def set_image(self, pixmap):
        """Set and initialize the image to be displayed"""
        self.original_pixmap = pixmap
        self.original_size = (pixmap.width(), pixmap.height())
        print(f"Original image size: {pixmap.width()}x{pixmap.height()}")
        self.pixmap = pixmap
        self.show_selection = False
        self.update_display()

    def update_display(self):
        """Update the displayed image and selection box after resize or load"""
        if self.pixmap:
            parent = self.parent()
            if parent:
                available_width = self.width()
                available_height = self.height()

                self.display_scale = min(
                    available_width / self.pixmap.width(),
                    available_height / self.pixmap.height(),
                )

                scaled_width = int(self.pixmap.width() * self.display_scale)
                scaled_height = int(self.pixmap.height() * self.display_scale)

                scaled_pixmap = self.pixmap.scaled(
                    scaled_width,
                    scaled_height,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )

                self.displayed_pixmap = scaled_pixmap
                self.setPixmap(scaled_pixmap)

                self.rect = QRect(
                    (self.width() - scaled_width) // 2,
                    (self.height() - scaled_height) // 2,
                    scaled_width,
                    scaled_height,
                )

    def set_selection_size(self, target_width, target_height):
        """Set the size of the selection rectangle based on target dimensions"""
        if not self.original_pixmap:
            return False

        orig_width, orig_height = (
            self.original_pixmap.width(),
            self.original_pixmap.height(),
        )

        if target_width > orig_width or target_height > orig_height:
            StyleMessageBox.warning(
                self,
                "Invalid Size",
                f"Requested size ({target_width}x{target_height}) exceeds original image size ({orig_width}x{orig_height}).\n"
                f"Please enter a size smaller than the original image.",
            )
            return False

        display_rect_width = int(target_width * self.display_scale)
        display_rect_height = int(target_height * self.display_scale)

        display_rect_width = min(display_rect_width, self.displayed_pixmap.width())
        display_rect_height = min(display_rect_height, self.displayed_pixmap.height())

        image_x = (self.width() - self.displayed_pixmap.width()) // 2
        image_y = (self.height() - self.displayed_pixmap.height()) // 2

        x = image_x + (self.displayed_pixmap.width() - display_rect_width) // 2
        y = image_y + (self.displayed_pixmap.height() - display_rect_height) // 2

        self.rect.setRect(x, y, display_rect_width, display_rect_height)
        self.show_selection = True
        self.update()
        return True

    def get_crop_rect(self):
        """Calculate the crop rectangle in original image coordinates"""
        if not self.original_pixmap or not self.displayed_pixmap:
            return None

        image_x = (self.width() - self.displayed_pixmap.width()) // 2
        image_y = (self.height() - self.displayed_pixmap.height()) // 2

        relative_x = self.rect.x() - image_x
        relative_y = self.rect.y() - image_y

        original_x = int(relative_x / self.display_scale)
        original_y = int(relative_y / self.display_scale)
        original_width = int(self.rect.width() / self.display_scale)
        original_height = int(self.rect.height() / self.display_scale)

        original_x = max(
            0, min(original_x, self.original_pixmap.width() - original_width)
        )
        original_y = max(
            0, min(original_y, self.original_pixmap.height() - original_height)
        )

        return QRect(original_x, original_y, original_width, original_height)

    def get_cropped_image(self):
        """Return the cropped portion of the original image"""
        if not self.original_pixmap:
            return None

        crop_rect = self.get_crop_rect()
        if crop_rect:
            return self.original_pixmap.copy(crop_rect)
        return None

    def rotate_image(self, degrees, record=True):
        """Rotate the image by specified degrees"""
        if not self.original_pixmap:
            return False

        self.rotation = (self.rotation + degrees) % 360
        transform = QTransform().rotate(degrees)

        self.original_pixmap = self.original_pixmap.transformed(
            transform, Qt.SmoothTransformation
        )
        self.original_size = (
            self.original_pixmap.width(),
            self.original_pixmap.height(),
        )
        self.pixmap = self.original_pixmap
        self.update_display()
        return True

    def paintEvent(self, event):
        """Draw the selection rectangle overlay"""
        super().paintEvent(event)
        if self.pixmap and self.show_selection:
            painter = QPainter(self)
            painter.setPen(QPen(QColor(0, 120, 215), 2))
            painter.setBrush(QColor(0, 120, 215, 30))
            painter.drawRect(self.rect)

    def get_resize_edge(self, pos):
        if not self.rect:
            return None

        left = abs(pos.x() - self.rect.left()) <= self.resize_margin
        right = abs(pos.x() - self.rect.right()) <= self.resize_margin
        top = abs(pos.y() - self.rect.top()) <= self.resize_margin
        bottom = abs(pos.y() - self.rect.bottom()) <= self.resize_margin

        if top and left:
            return "top_left"
        if top and right:
            return "top_right"
        if bottom and left:
            return "bottom_left"
        if bottom and right:
            return "bottom_right"
        if left:
            return "left"
        if right:
            return "right"
        if top:
            return "top"
        if bottom:
            return "bottom"
        return None

    def mousePressEvent(self, event):
        if not self.pixmap or not self.show_selection:
            return

        edge = self.get_resize_edge(event.pos())
        if edge:
            self.resizing = True
            self.resize_edge = edge
            self.last_pos = event.pos()
        elif self.rect.contains(event.pos()):
            self.dragging = True
            self.offset = event.pos() - self.rect.topLeft()
            self.setCursor(Qt.SizeAllCursor)

    def mouseMoveEvent(self, event):
        if not self.displayed_pixmap or not self.show_selection:
            return

        edge = self.get_resize_edge(event.pos())
        if edge:
            cursors = {
                "left": Qt.SizeHorCursor,
                "right": Qt.SizeHorCursor,
                "top": Qt.SizeVerCursor,
                "bottom": Qt.SizeVerCursor,
                "top_left": Qt.SizeFDiagCursor,
                "bottom_right": Qt.SizeFDiagCursor,
                "top_right": Qt.SizeBDiagCursor,
                "bottom_left": Qt.SizeBDiagCursor,
            }
            self.setCursor(cursors[edge])
        elif self.rect.contains(event.pos()):
            self.setCursor(Qt.SizeAllCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.resizing and self.last_pos:
            dx = event.pos().x() - self.last_pos.x()
            dy = event.pos().y() - self.last_pos.y()

            new_rect = QRect(self.rect)
            image_x = (self.width() - self.displayed_pixmap.width()) // 2
            image_y = (self.height() - self.displayed_pixmap.height()) // 2

            if self.resize_edge in ["left", "top_left", "bottom_left"]:
                new_rect.setLeft(min(max(image_x, new_rect.left() + dx),
                                   new_rect.right() - self.resize_margin))
            if self.resize_edge in ["right", "top_right", "bottom_right"]:
                new_rect.setRight(min(max(new_rect.left() + self.resize_margin,
                                        new_rect.right() + dx),
                                    image_x + self.displayed_pixmap.width()))
            if self.resize_edge in ["top", "top_left", "top_right"]:
                new_rect.setTop(min(max(image_y, new_rect.top() + dy),
                                  new_rect.bottom() - self.resize_margin))
            if self.resize_edge in ["bottom", "bottom_left", "bottom_right"]:
                new_rect.setBottom(min(max(new_rect.top() + self.resize_margin,
                                         new_rect.bottom() + dy),
                                     image_y + self.displayed_pixmap.height()))

            self.rect = new_rect
            self.last_pos = event.pos()
            crop_rect = self.get_crop_rect()
            if crop_rect:
                self.selection_size_changed.emit(crop_rect.width(), crop_rect.height())
            self.update()

        elif self.dragging:
            new_pos = event.pos() - self.offset
            image_x = (self.width() - self.displayed_pixmap.width()) // 2
            image_y = (self.height() - self.displayed_pixmap.height()) // 2

            new_x = max(image_x,
                       min(new_pos.x(),
                           image_x + self.displayed_pixmap.width() - self.rect.width()))
            new_y = max(image_y,
                       min(new_pos.y(),
                           image_y + self.displayed_pixmap.height() - self.rect.height()))

            self.rect.moveTopLeft(QPoint(new_x, new_y))
            self.update()

    def mouseReleaseEvent(self, event):
        if self.resizing:
            crop_rect = self.get_crop_rect()
            if crop_rect:
                self.selection_size_changed.emit(crop_rect.width(), crop_rect.height())

        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.last_pos = None

    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        if self.pixmap:
            self.update_display()
