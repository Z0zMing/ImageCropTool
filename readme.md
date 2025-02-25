# Image Crop Tool

A versatile image cropping application with web import capabilities.

[中文](readme_zh.md)

## Features

- Load images from your computer
- Import images directly from popular websites
- Crop images to standard or custom resolutions
- Rotate images
- Preview crops before saving
- Modern, intuitive UI

## Web Image Import

The application allows importing images directly from popular websites:

1. Click the "Import from Web" button
2. Select a website from the available options
3. Browse the website or search for images
4. Click on an image to select it
5. The image will be automatically loaded into the application for editing

## Supported Websites

- Unsplash
- Pixiv
- Pexels
- Flickr

## Keyboard Shortcuts

- `Ctrl+O`: Open image
- `Ctrl+Return`: Crop image
- `Ctrl+Left`: Rotate left
- `Ctrl+Right`: Rotate right
- `Ctrl+P`: Preview crop

## Requirements

- Python 3.6+
- PySide6
- QtWebEngine support
- Requests library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Z0zMing/ImageCropTool.git
```

2. Install the required dependencies:
```bash
pip install PySide6 requests
```

3. Run the application:
```bash
python tools.py
```

## Directory Structure

```
ImageCropTool/
├── icons/                  # Application icons
├── widget/                 # UI components
│   ├── canvas.py          # Main image canvas
│   ├── preview_dialog.py  # Preview window
│   └── message_box.py     # Custom message boxes
├── tools.py               # Main application
├── styles.py             # UI styles
└── ToolTips.py          # Tooltip components
```

## Usage

1. Click the upload button or press `Ctrl+O` to open an image
2. Select a preset resolution from the dropdown or enter a custom resolution (e.g., 1920x1080)
3. Adjust the crop selection by dragging or resizing
4. Use the rotation buttons if needed
5. Preview the result with the preview button
6. Click the crop button to save the cropped image

## Output

Cropped images are automatically saved in the `output` directory with timestamps as filenames.

## TODO

- [ ] Add aspect ratio lock when resizing
- [ ] Implement custom preset resolution management
- [ ] Add image filters and basic adjustment features
- [ ] Support exporting to different file formats
- [ ] Add customizable keyboard shortcuts
- [ ] Implement image metadata preservation
- [ ] Add AI image expansion feature
- [ ] Support multiple language interface
- [ ] Support importing images from the internet (like Pixiv)
- [ ] Add smart repair features (denoising, deblurring, enhancing clarity)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT