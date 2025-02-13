class Styles:
    MAIN_WIDGET = """
        QWidget#mainWidget {
            background-color: #2c2c2c;
            border: 1px solid #3c3c3c;
            border-radius: 40px;
        }
        
        QWidget {
            background-color: #2c2c2c;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            font-weight: 900;
            color: #ffffff;
        }

        QVBoxLayout, QHBoxLayout {
            padding: 10px;
            margin: 5px;
            spacing: 5px;
            background-color: transparent;
        }
    """

    UPLOAD_BUTTON = """
        QPushButton {
            background-color: #3b3b3b;
            border: none;
            border-radius: 5px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #4b4b4b;
        }
        QPushButton:pressed {
            background-color: #2b2b2b;
        }
        QPushButton:disabled {
            background-color: #2b2b2b;
            opacity: 0.5;
        }
    """

    CROP_BUTTON = UPLOAD_BUTTON
    ROTATE_LEFT_BUTTON = UPLOAD_BUTTON
    ROTATE_RIGHT_BUTTON = UPLOAD_BUTTON
    PREVIEW_BUTTON = UPLOAD_BUTTON

    HISTORY_BUTTON = """
        QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 15px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #5a6268;
        }
        QPushButton:pressed {
            background-color: #454d55;
        }
        QPushButton:disabled {
            background-color: #cccccc;
            color: #666666;
        }
    """

    RESOLUTION_INPUT = """
        QLineEdit {
            border: 1px solid #4c4c4c;
            border-radius: 3px;
            padding: 5px;
            font-size: 20px;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            font-weight: 500;
            background-color: #3c3c3c;
            color: white;
        }
        QLineEdit:focus {
            border: 1px solid #5c5c5c;
            background-color: #464646;
        }
    """

    RESOLUTION_COMBO = """
        QComboBox {
            border: 1px solid #4c4c4c;
            border-radius: 3px;
            padding: 5px;
            font-size: 20px;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            font-weight: 500;
            background-color: #3c3c3c;
            color: white;
        }
        QComboBox:hover {
            background-color: #464646;
        }
        QComboBox::drop-down {
            width: 24px;
            border: 0px;
        }
        QComboBox::down-arrow {
            image: url(path/to/your/down_arrow_icon.png);
        }
        QComboBox QAbstractItemView {
            border: 1px solid #4c4c4c;
            border-radius: 3px;
            background-color: #3c3c3c;
            color: white;
            selection-background-color: #5c5c5c;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            font-weight: 500;
        }
    """

    TOOLTIP_LABEL = """
        QLabel {
            background-color: #2c2c2c;
            padding: 1px;
            border: 1px solid #2c2c2c;
            border-radius: 1px;
            font-size: 15px;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            font-weight: 500;
            color: white;
        }
    """
    
    TITLE_BAR = """
        QWidget#titleBar {
            background-color: #1e1e1e;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            min-height: 35px;
            max-height: 35px;
        }
    """
    
    TITLE_LABEL = """
        QLabel {
            color: white;
            font-size: 30px;
            font-weight: 900;
            font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
            padding: 5px;
        }
    """
    
    WINDOW_BUTTON = """
        QPushButton {
            background-color: transparent;
            border: none;
            border-radius: 0px;
        }
        QPushButton:hover {
            background-color: #404040;
        }
        QPushButton#closeButton:hover {
            background-color: #e81123;
        }
    """
