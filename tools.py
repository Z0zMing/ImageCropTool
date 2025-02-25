import sys, os
from PySide6.QtWidgets import (
    QWidget,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QComboBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QPixmap, QTransform, QKeySequence, QIcon, QFont

from widget.canvas import Canvas
from widget.preview_dialog import PreviewDialog
from widget.ToolTips import ToolTipsButton
from widget.styles import Styles
from widget.message_box import StyleMessageBox
from widget.web_import_dialog import WebImportDialog

import time
import json


class ImageCropper(QWidget):
    """Main window for image cropping application"""

    def __init__(self):
        super().__init__()
        self.setObjectName("mainWidget")
        self.setWindowTitle("Image Cropper")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setMinimumSize(1600, 900)
        
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("titleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 0, 0)
        title_layout.setSpacing(0)
        
        self.title_label = QLabel("Image Cropper")
        self.title_label.setStyleSheet(Styles.TITLE_LABEL)
        title_layout.addWidget(self.title_label)
        
        title_layout.addStretch()
        
        self.min_button = QPushButton("", self)
        self.min_button.setObjectName("minButton")
        self.min_button.setIcon(QIcon("icons/minimize.svg"))
        self.min_button.setIconSize(QSize(16, 16))
        self.close_button = QPushButton("", self)
        self.close_button.setObjectName("closeButton")
        self.close_button.setIcon(QIcon("icons/close.svg"))
        self.close_button.setIconSize(QSize(16, 16))
        
        self.min_button.setFixedSize(45, 35)
        self.close_button.setFixedSize(45, 35)
        
        self.min_button.setStyleSheet(Styles.WINDOW_BUTTON)
        self.close_button.setStyleSheet(Styles.WINDOW_BUTTON)
        
        title_layout.addWidget(self.min_button)
        title_layout.addWidget(self.close_button)
        
        self.min_button.clicked.connect(self.showMinimized)
        self.close_button.clicked.connect(self.close)
        
        main_container = QWidget(self)
        main_container.setObjectName("mainContainer")
        main_container.setContentsMargins(10, 10, 10, 10)

        self.canvas = Canvas(self)
        self.canvas.selection_size_changed.connect(self.update_resolution_input)

        self.tooltipLabel = QLabel("", self)
        self.tooltipLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        self.upLoadButton = ToolTipsButton(
            "", "Click to upload image", self
        )
        self.upLoadButton.setIcon(QIcon("icons/upload-image.svg"))
        self.upLoadButton.setIconSize(QSize(24, 24))
        self.upLoadButton.setFixedSize(40, 40)

        self.webImportButton = ToolTipsButton(
            "", "Import image from web", self
        )
        self.webImportButton.setIcon(QIcon("icons/web-import.svg"))
        self.webImportButton.setIconSize(QSize(24, 24))
        self.webImportButton.setFixedSize(40, 40)

        self.resolution_group = QHBoxLayout()

        self.resolution_combo = QComboBox(self)
        self.resolution_combo.addItem("select preset resolution")
        self.resolution_combo.addItem("720p (1280x720)")
        self.resolution_combo.addItem("1K (1920x1080)")
        self.resolution_combo.addItem("2K (2560x1440)")

        self.resolution_input = QLineEdit(self)
        self.resolution_input.setPlaceholderText(
            "Enter custom resolution (e.g. 1920x1080)"
        )
        self.resolution_input.returnPressed.connect(self.get_resolution)

        self.cropButton = ToolTipsButton(
            "", "Crop the image according to the set solution", self
        )
        self.cropButton.setIcon(QIcon("icons/crop-simple.svg"))
        self.cropButton.setIconSize(QSize(24, 24))
        self.cropButton.setFixedSize(40, 40)

        self.rotateLeftButton = ToolTipsButton("", "Rotate image left", self)
        self.rotateLeftButton.setIcon(QIcon("icons/rotate-left.svg"))
        self.rotateLeftButton.setIconSize(QSize(24, 24))
        self.rotateLeftButton.setFixedSize(40, 40)

        self.rotateRightButton = ToolTipsButton("", "Rotate image right", self)
        self.rotateRightButton.setIcon(QIcon("icons/rotate-right.svg"))
        self.rotateRightButton.setIconSize(QSize(24, 24))
        self.rotateRightButton.setFixedSize(40, 40)

        self.previewButton = ToolTipsButton(
            "", "Preview of the image after Crop", self
        )
        self.previewButton.setIcon(QIcon("icons/open-preview.svg"))
        self.previewButton.setIconSize(QSize(24, 24))
        self.previewButton.setFixedSize(40, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upLoadButton)
        button_layout.addWidget(self.webImportButton)
        button_layout.addWidget(self.resolution_combo)
        button_layout.addWidget(self.resolution_input)
        button_layout.addWidget(self.cropButton)
        button_layout.addWidget(self.rotateLeftButton)
        button_layout.addWidget(self.rotateRightButton)
        button_layout.addWidget(self.previewButton)

        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.canvas, 1)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.tooltipLabel)
        bottom_layout.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        )
        main_layout.addLayout(bottom_layout)
        
        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)
        window_layout.addWidget(self.title_bar)
        window_layout.addWidget(main_container)

        self.load_shortcut_config()
        self.upLoadButton.clicked.connect(self.load_image)
        self.webImportButton.clicked.connect(self.import_from_web)
        self.resolution_combo.currentIndexChanged.connect(self.on_combo_changed)
        self.rotateLeftButton.clicked.connect(lambda: self.rotate_image(-90))
        self.rotateRightButton.clicked.connect(lambda: self.rotate_image(90))
        self.previewButton.clicked.connect(self.preview_crop)
        self.cropButton.clicked.connect(self.crop_image)

        self.upLoadButton.tooltip_message.connect(self.set_tooltip_text)
        self.webImportButton.tooltip_message.connect(self.set_tooltip_text)
        self.cropButton.tooltip_message.connect(self.set_tooltip_text)
        self.rotateLeftButton.tooltip_message.connect(self.set_tooltip_text)
        self.rotateRightButton.tooltip_message.connect(self.set_tooltip_text)
        self.previewButton.tooltip_message.connect(self.set_tooltip_text)
        

        self.current_resolution_width = None
        self.current_resolution_height = None

        self.setStyleSheet(Styles.MAIN_WIDGET)
        self.upLoadButton.setStyleSheet(Styles.UPLOAD_BUTTON)
        self.webImportButton.setStyleSheet(Styles.UPLOAD_BUTTON)  # Using same style as upload button
        self.cropButton.setStyleSheet(Styles.CROP_BUTTON)
        self.rotateLeftButton.setStyleSheet(Styles.ROTATE_LEFT_BUTTON)
        self.rotateRightButton.setStyleSheet(Styles.ROTATE_RIGHT_BUTTON)
        self.previewButton.setStyleSheet(Styles.PREVIEW_BUTTON)
        self.resolution_input.setStyleSheet(Styles.RESOLUTION_INPUT)
        self.resolution_combo.setStyleSheet(Styles.RESOLUTION_COMBO)
        self.tooltipLabel.setStyleSheet(Styles.TOOLTIP_LABEL)

        self.disable_controls()

    def disable_controls(self):
        """Disable all controls except upload button"""
        self.cropButton.setEnabled(False)
        self.rotateLeftButton.setEnabled(False)
        self.rotateRightButton.setEnabled(False)
        self.previewButton.setEnabled(False)
        self.resolution_combo.setEnabled(False)
        self.resolution_input.setEnabled(False)

    def enable_controls(self):
        """Enable all controls"""
        self.cropButton.setEnabled(True)
        self.rotateLeftButton.setEnabled(True)
        self.rotateRightButton.setEnabled(True)
        self.previewButton.setEnabled(True)
        self.resolution_combo.setEnabled(True)
        self.resolution_input.setEnabled(True)

    def set_default_shortcuts(self):
        """Set the default shortcuts for the buttons"""
        self.upLoadButton.setShortcut("Ctrl+O")
        self.cropButton.setShortcut("Ctrl+Return")
        self.rotateLeftButton.setShortcut("Ctrl+Left")
        self.rotateRightButton.setShortcut("Ctrl+Right")
        self.previewButton.setShortcut("Ctrl+P")

    def load_shortcut_config(self):
        """Load the shortcut configuration from file"""
        try:
            with open("config.json", "r") as file:
                config = json.load(file)
            self.upLoadButton.setShortcut(
                QKeySequence(config.get("load_image", "Ctrl+O"))
            )
            self.cropButton.setShortcut(
                QKeySequence(config.get("crop_image", "Ctrl+Return"))
            )
            self.rotateLeftButton.setShortcut(
                QKeySequence(config.get("rotate_left", "Ctrl+Left"))
            )
            self.rotateRightButton.setShortcut(
                QKeySequence(config.get("rotate_right", "Ctrl+Right"))
            )
            self.previewButton.setShortcut(
                QKeySequence(config.get("preview_crop", "Ctrl+P"))
            )
        except FileNotFoundError:
            self.set_default_shortcuts()
        except json.JSONDecodeError:
            self.set_default_shortcuts()
        except Exception as e:
            self.set_default_shortcuts()

    def set_tooltip_text(self, message):
        """set the tooltip text"""
        self.tooltipLabel.setText(message)

    def on_combo_changed(self, index):
        """Handle resolution preset selection from dropdown"""
        if index == 0:
            return

        resolutions = {
            1: "1280x720",  # 720p
            2: "1920x1080",  # 1K
            3: "2560x1440",  # 2K
        }

        if index in resolutions:
            self.resolution_input.setText(resolutions[index])
            self.get_resolution()

    def load_image(self):
        """Load and display an image from file system"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image files (*.jpg *.png *.jpeg)"
        )
        if file_path:
            pixmap = QPixmap(file_path)
            self.canvas.set_image(pixmap)
            self.enable_controls()

    def import_from_web(self):
        """Import image from web dialog"""
        try:
            dialog = WebImportDialog(self)
            dialog.image_selected.connect(self.set_imported_image)
            dialog.exec()
        except Exception as e:
            StyleMessageBox.critical(self, "Error", f"Error opening web import: {str(e)}")

    def set_imported_image(self, pixmap):
        """Process the image imported from the web"""
        if not pixmap.isNull():
            self.canvas.load_pixmap(pixmap)
            self.enable_controls()
        else:
            StyleMessageBox.warning(self, "Warning", "Selected image could not be loaded.")

    def get_resolution(self):
        """Process the input resolution and apply it to the selection box"""
        resolution = self.resolution_input.text()
        is_from_combo = False
        for index, value in {1: "1280x720", 2: "1920x1080", 3: "2560x1440"}.items():
            if value == resolution and self.resolution_combo.currentIndex() == index:
                is_from_combo = True
                break

        if not resolution:
            StyleMessageBox.warning(
                self,
                "No Resolution",
                "Please either select a preset resolution or enter a custom one."
            )
            return

        try:
            width, height = map(int, resolution.split("x"))
            if self.canvas.set_selection_size(width, height):
                self.current_resolution_width = width
                self.current_resolution_height = height
                cropped_image = self.canvas.get_cropped_image()
                if cropped_image:
                    print(
                        f"Cropped image size: {cropped_image.width()}x{cropped_image.height()}"
                    )
                if not is_from_combo:
                    self.resolution_combo.setCurrentIndex(0)
            else:
                pass
        except ValueError:
            StyleMessageBox.warning(
                self,
                "Invalid Format",
                "Please enter the resolution in format: widthxheight (e.g. 1920x1080)"
            )
            return

    def rotate_image(self, degrees):
        """Rotate the image by specified degrees"""
        if self.canvas.rotate_image(degrees):
            if self.current_resolution_height and self.current_resolution_width:
                current_image_width = self.canvas.original_pixmap.width()
                current_image_height = self.canvas.original_pixmap.height()

                if (
                    self.current_resolution_height <= current_image_height
                    and self.current_resolution_width <= current_image_width
                ):
                    self.canvas.set_selection_size(
                        self.current_resolution_width, self.current_resolution_height
                    )
                else:
                    StyleMessageBox.warning(
                        self,
                        "Invalid Resolution After Rotation",
                        "The previously set resolution is invalid after rotation. Please set a new resolution.\n"
                    )
                    self.resolution_combo.setCurrentIndex(0)
                    self.resolution_input.clear()
                    self.current_resolution_width = None
                    self.current_resolution_height = None

    def preview_crop(self):
        """Show preview of the cropped image"""
        cropped = self.canvas.get_cropped_image()
        if cropped:
            preview = PreviewDialog(cropped, self)
            preview.exec_()

    def crop_image(self):
        """Combined function for handling crop operations"""
        if not self.canvas.original_pixmap:
            return

        if not self.current_resolution_width or not self.current_resolution_height:
            resolution = self.resolution_input.text()
            if not resolution:
                StyleMessageBox.warning(
                    self,
                    "No Resolution",
                    "Please either select a preset resolution or enter a custom one."
                )
                return

            try:
                width, height = map(int, resolution.split("x"))
                if not self.canvas.set_selection_size(width, height):
                    return
                self.current_resolution_width = width
                self.current_resolution_height = height
            except ValueError:
                StyleMessageBox.warning(
                    self,
                    "Invalid Format",
                    "Please enter the resolution in format: widthxheight (e.g. 1920x1080)"
                )
                return

        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)

        cropped = self.canvas.get_cropped_image()
        if cropped:
            filename = f"crop_{int(time.time())}.png"
            filepath = os.path.join(output_dir, filename)
            cropped.save(filepath)
            StyleMessageBox.information(self, "Success", f"Image saved as {filename}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragging') and self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def update_resolution_input(self, width, height):
        """Update resolution input when selection size changes"""
        self.resolution_input.setText(f"{width}x{height}")
        self.resolution_combo.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setFont(QFont("Microsoft YaHei"))
    window = ImageCropper()
    window.show()
    sys.exit(app.exec())