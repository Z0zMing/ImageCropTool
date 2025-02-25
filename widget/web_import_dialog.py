from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QGridLayout, QWidget, 
    QScrollArea, QFrame, QMessageBox, QSplitter
)
from PySide6.QtCore import Qt, Signal, QSize, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineUrlRequestInterceptor
import os
import json
import requests
from io import BytesIO

class WebSite:
    def __init__(self, name, icon, url, search_api=None):
        self.name = name
        self.icon = icon
        self.url = url
        self.search_api = search_api

class ImageUrlInterceptor(QWebEngineUrlRequestInterceptor):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked_images = []
        
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        # Check if this is an image request
        if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            self.clicked_images.append(url)

class WebImportDialog(QDialog):
    image_selected = Signal(QPixmap)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Image from Web")
        self.setMinimumSize(1000, 700)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Load websites config
        self.websites = self.load_websites_config()
        
        # Create UI
        self.init_ui()
        
        # Apply styles
        self.apply_styles()
        
        # Create web interceptor
        self.interceptor = ImageUrlInterceptor(self)
        # Create a QWebEngineProfile for the web view
        self.profile = QWebEngineProfile("WebImportDialogProfile", self)
        self.profile.setUrlRequestInterceptor(self.interceptor)
    
    def load_websites_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'websites.json')
        websites = []
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    websites_data = json.load(f)
                    
                    for site_data in websites_data:
                        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), site_data['icon'])
                        websites.append(WebSite(
                            site_data['name'], 
                            icon_path, 
                            site_data['url'],
                            site_data.get('search_api')
                        ))
            else:
                QMessageBox.warning(self, "Warning", "Websites configuration file not found.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load websites: {str(e)}")
            
        return websites
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        sites_label = QLabel("Select a website:")
        sites_layout = QGridLayout()
        
        row, col = 0, 0
        for i, website in enumerate(self.websites):
            btn = QPushButton()
            btn.setToolTip(website.name)
            btn.setIcon(QIcon(website.icon))
            btn.setIconSize(QSize(48, 48))
            btn.setFixedSize(70, 70)
            btn.clicked.connect(lambda checked, site=website: self.open_website(site))
            
            sites_layout.addWidget(btn, row, col)
            col += 1
            if col > 3:  # 4 buttons per row
                col = 0
                row += 1
        
        top_layout.addWidget(sites_label)
        top_layout.addLayout(sites_layout)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search images...")
        self.search_input.returnPressed.connect(self.search_images)
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_images)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        top_layout.addLayout(search_layout)
        
        self.web_view = QWebEngineView()
        self.web_view.loadFinished.connect(self.page_loaded)
        self.web_view.page().profile().downloadRequested.connect(self.handle_download)
        
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(top_widget)
        splitter.addWidget(self.web_view)
        splitter.setSizes([100, 500])
        
        main_layout.addWidget(splitter)
        
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        
        main_layout.addLayout(button_layout)
        
        self.status_label = QLabel("Select a website to browse images")
        main_layout.addWidget(self.status_label)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #555555;
            }
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px;
                border-radius: 3px;
            }
        """)
    
    def open_website(self, website):
        self.status_label.setText(f"Loading {website.name}...")
        self.current_website = website
        self.web_view.load(QUrl(website.url))
    
    def page_loaded(self):
        self.status_label.setText(f"Browsing {self.current_website.name}. Click on an image to select it.")
        
        js_code = """
        document.addEventListener('click', function(e) {
            if (e.target.tagName === 'IMG') {
                // Send image URL back to Python
                window.location.href = e.target.src;
                e.preventDefault();
                return false;
            }
        }, true);
        """
        
        self.web_view.page().runJavaScript(js_code)
    
    def search_images(self):
        query = self.search_input.text().strip()
        if not query or not hasattr(self, 'current_website'):
            return
            
        if self.current_website.search_api:
            search_url = self.current_website.search_api.replace('{query}', query)
            self.web_view.load(QUrl(search_url))
            self.status_label.setText(f"Searching for '{query}' on {self.current_website.name}")
        else:
            search_url = f"{self.current_website.url}/search?q={query}"
            self.web_view.load(QUrl(search_url))
            self.status_label.setText(f"Searching for '{query}' on {self.current_website.name}")
    
    def handle_download(self, download):
        if self.interceptor.clicked_images:
            image_url = self.interceptor.clicked_images[-1]
            self.download_and_select_image(image_url)
            self.interceptor.clicked_images.clear()
            
    def download_and_select_image(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            img_data = BytesIO(response.content)
            pixmap = QPixmap()
            
            if pixmap.loadFromData(response.content):
                self.status_label.setText(f"Image downloaded: {url}")
                self.image_selected.emit(pixmap)
                self.accept()
            else:
                self.status_label.setText(f"Failed to load image from: {url}")
                
        except Exception as e:
            self.status_label.setText(f"Error downloading image: {str(e)}")
            QMessageBox.warning(self, "Download Error", str(e))
