# Image Crop Tool

Transform your images with precision and style using this elegant image cropping tool! Built with PySide6, this application combines powerful functionality with a modern, dark-themed interface. Whether you're preparing images for social media, web design, or professional work, this tool makes it effortless to achieve pixel-perfect crops with its intuitive controls and real-time preview features. From quick presets to custom dimensions, rotate with ease and see your changes instantly – all wrapped in a sleek, user-friendly package.

[中文](readme_zh.md)

## Features

- 🎯 Precise image cropping with customizable dimensions
- 📏 Preset resolution options (720p, 1K, 2K)
- 🔄 Image rotation (90° clockwise/counterclockwise)
- 👁️ Real-time preview of crop selection
- 🖼️ Preview dialog for checking the final result
- ⌨️ Keyboard shortcuts for quick operations
- 🎨 Modern dark theme UI
- 🖱️ Drag-and-drop window movement
- 🔍 Interactive selection box with resize handles

## Keyboard Shortcuts

- `Ctrl+O`: Open image
- `Ctrl+Return`: Crop image
- `Ctrl+Left`: Rotate left
- `Ctrl+Right`: Rotate right
- `Ctrl+P`: Preview crop

## Requirements

- Python 3.7+
- PySide6

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Z0zMing/ImageCropTool.git
```

2. Install the required dependencies:
```bash
pip install PySide6
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

[MIT License](LICENSE)