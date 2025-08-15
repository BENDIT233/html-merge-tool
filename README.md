# HTML合并工具

一个将文件夹中的所有HTML、CSS、JavaScript和图片文件合并为单个HTML或MHTML文件的工具。采用现代化PyQt5桌面GUI技术构建，提供直观美观的用户界面。

## ✨ 功能特性

- 🎨 **现代化界面**: 基于PyQt5的桌面GUI，具有现代化设计风格
- 📁 **拖拽支持**: 支持文件夹拖拽操作，操作更便捷
- 🔄 **多种格式**: 支持HTML和MHTML输出格式
- 📦 **批量处理**: 支持批量转换多个文件夹
- 🚀 **便携运行**: 无需安装，即开即用
- 🛡️ **安全可靠**: 本地处理，不上传数据
- 📊 **实时进度**: 显示转换进度和详细日志
- 📱 **响应式设计**: 适配不同窗口尺寸

## 🏗️ 技术架构

- **后端**: Python 3.8+
- **前端**: PyQt5 (现代化桌面GUI框架)
- **打包**: PyInstaller
- **界面**: 现代化桌面应用程序，支持拖拽操作

## 📦 使用方法

### 方法一：使用打包好的exe文件（推荐）

1. 访问 [GitHub Releases](https://github.com/BENDIT233/html-merge-tool/releases) 页面
2. 下载最新版本的 `html_merge_tool_portable.zip`
3. 解压文件到任意目录
4. 双击 `html_merge_tool.exe` 启动程序

### 方法二：从源码运行

1. 克隆仓库：
   ```bash
   git clone https://github.com/BENDIT233/html-merge-tool.git
   cd html-merge-tool
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```bash
   python app.py
   ```

### 方法三：本地构建

1. 确保已安装Python 3.8+和pip
2. 运行构建脚本：
   ```bash
   # Windows
   build.bat
   
   # 或手动构建
   python -m PyInstaller app.spec --clean
   ```

## 🎯 使用说明

1. **启动程序**: 双击exe文件或运行Python脚本
2. **选择文件夹**: 将包含HTML文件的文件夹拖拽到界面，或点击"选择文件夹"按钮
3. **设置选项**: 选择输出格式（HTML或MHTML）和输出目录
4. **开始转换**: 点击"开始转换"或"批量转换"按钮
5. **查看结果**: 转换完成后，结果文件会保存在指定位置

## 📁 项目结构

```
html-merge-tool/
├── app.py                 # 主应用程序入口 (PyQt5 GUI)
├── html_converter.py      # HTML转换核心逻辑
├── requirements.txt       # Python依赖
├── app.spec              # PyInstaller配置
├── build.bat             # Windows构建脚本
├── create_icon.py        # 图标生成脚本
└── .github/workflows/    # GitHub Actions配置
    └── build.yml         # 自动构建工作流
```

## 🔧 构建说明

### 自动构建（GitHub Actions）

项目配置了GitHub Actions自动构建流程：

1. 推送代码到main分支
2. GitHub Actions自动构建Windows可执行文件
3. 生成便携式ZIP包并创建Release

### 手动构建

```bash
# 安装依赖
pip install -r requirements.txt

# 构建可执行文件
python -m PyInstaller app.spec --clean

# 生成的文件在 dist/ 目录中
```

## 🐛 故障排除

### 常见问题

1. **程序无法启动**
   - 确保已安装Python 3.8+
   - 检查依赖是否正确安装
   - 尝试运行 `python app.py` 检查环境

2. **PyQt5安装失败**
   - 使用Python 3.8-3.11版本
   - 创建虚拟环境
   - 更新pip: `pip install --upgrade pip`

3. **防病毒软件误报**
   - 将程序添加到防病毒软件白名单
   - 参考 `ANTIVIRUS_FALSE_POSITIVE.md` 文件

4. **转换失败**
   - 检查文件夹是否包含HTML文件
   - 确保文件路径不包含特殊字符
   - 查看程序日志信息

### 日志和调试

程序运行时会显示详细的日志信息，包括：
- 启动过程
- 文件处理进度
- 错误信息

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 现代化桌面GUI框架
- [PyInstaller](https://pyinstaller.org/) - Python应用打包工具

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/BENDIT233/html-merge-tool/issues)
- 发送邮件至项目维护者

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！
