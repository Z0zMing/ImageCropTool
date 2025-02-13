# 图片裁剪工具

一款基于PySide6构建的现代化、用户友好的图片裁剪应用程序。该工具允许用户轻松地将图片裁剪至特定分辨率，同时保持简洁的暗色主题界面。

![ZH_EN](readme.md)

## 特性

- 🎯 精确的图片裁剪，支持自定义尺寸
- 📏 预设分辨率选项（720p、1K、2K）
- 🔄 图片旋转（顺时针/逆时针90°）
- 👁️ 实时预览裁剪选区
- 🖼️ 预览对话框查看最终效果
- ⌨️ 快捷键操作
- 🎨 现代化暗色主题界面
- 🖱️ 拖拽移动窗口
- 🔍 可交互的选区框，支持调整大小

## 键盘快捷键

- `Ctrl+O`: 打开图片
- `Ctrl+Return`: 裁剪图片
- `Ctrl+Left`: 向左旋转
- `Ctrl+Right`: 向右旋转
- `Ctrl+P`: 预览裁剪效果

## 系统要求

- Python 3.7+
- PySide6

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/Z0zMing/ImageCropTool.git
```

2. 安装依赖：
```bash
pip install PySide6
```

3. 运行应用：
```bash
python tools.py
```

## 目录结构

```
ImageCropTool/
├── icons/                  # 应用图标
├── widget/                 # UI组件
│   ├── canvas.py          # 主图片画布
│   ├── preview_dialog.py  # 预览窗口
│   └── message_box.py     # 自定义消息框
├── tools.py               # 主程序
├── styles.py              # UI样式
└── ToolTips.py           # 工具提示组件
```

## 使用说明

1. 点击上传按钮或按 `Ctrl+O` 打开图片
2. 从下拉菜单选择预设分辨率或输入自定义分辨率（如：1920x1080）
3. 通过拖动或调整大小来设置裁剪区域
4. 根据需要使用旋转按钮
5. 使用预览按钮查看效果
6. 点击裁剪按钮保存裁剪后的图片

## 输出

裁剪后的图片会自动保存在 `output` 目录下，文件名包含时间戳。

## 参与贡献

欢迎提交拉取请求。对于重大更改，请先开issue讨论您想要改变的内容。

## 许可证

[MIT许可证](LICENSE)