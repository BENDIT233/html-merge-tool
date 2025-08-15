# HTML Merge Tool

一个将文件夹中的所有HTML、CSS、JavaScript和图片文件合并为单个HTML或MHTML文件的工具。采用现代化Web技术栈构建，提供直观美观的用户界面。

## 功能

- 将HTML文件中的图片转换为base64编码并嵌入
- 将CSS和JavaScript文件内容嵌入到HTML文件中
- 支持HTML和MHTML两种输出格式
- 支持拖拽文件夹到界面
- 实时进度显示
- 响应式设计，适配不同屏幕尺寸
- 基于Web技术栈的现代化UI

## 技术架构

- **前端**：HTML5, CSS3, JavaScript
- **后端**：Python 3.8+
- **通信**：Eel库 (Python与Web前端通信)
- **打包**：PyInstaller

## 使用方法

### 方法一：使用打包好的exe文件（推荐）

1. 访问 [GitHub Actions](https://github.com/BENDIT233/html-merge-tool/actions) 页面
2. 找到并运行"Build Windows Executable"工作流
3. 下载生成的exe文件
4. 双击运行html_merge_tool.exe

### 方法二：从源码运行

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
2. 运行应用：
   ```
   python app.py
   ```

## 项目结构

- `app.py`：应用入口，使用Eel连接前端和后端
- `html_converter.py`：HTML转换核心逻辑
- `web/`：Web前端目录
  - `index.html`：前端页面
  - `style.css`：样式文件
  - `app.js`：前端逻辑
- `requirements.txt`：项目依赖
- `build_exe.bat`：构建可执行文件的批处理脚本
- `.github/workflows/build_exe.yml`：GitHub Actions工作流配置

## 构建说明

1. 确保已安装所有依赖：
   ```
   pip install -r requirements.txt
   ```
2. 运行构建脚本：
   ```
   build_exe.bat
   ```
3. 构建成功后，可执行文件位于`dist/html_merge_tool.exe`

## 许可证

MIT
