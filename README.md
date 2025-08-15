# HTML Merge Tool

一个将文件夹中的所有HTML、CSS、JavaScript和图片文件合并为单个HTML文件的工具。

## 功能

- 将HTML文件中的图片转换为base64编码并嵌入
- 将CSS和JavaScript文件内容嵌入到HTML文件中
- 支持拖拽文件夹到GUI界面
- 生成单个可执行文件

## 使用方法

### 使用打包好的exe文件（推荐）

1. 访问 [GitHub Actions](https://github.com/BENDIT233/html-merge-tool/actions) 页面
2. 找到并运行"Build Windows Executable"工作流
3. 下载生成的exe文件

## 项目结构

- `gui.py`：图形用户界面
- `html_converter.py`：HTML转换核心逻辑
- `create_icon.py`：创建应用图标
- `requirements.txt`：项目依赖
- `run_gui.bat`：运行GUI的批处理文件
- `.github/workflows/build_exe.yml`：GitHub Actions工作流配置

## 许可证

MIT
