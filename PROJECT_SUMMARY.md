# 项目总结

## 项目概述

HTML Merge Tool是一个将文件夹中的所有HTML、CSS、JavaScript和图片文件合并为单个HTML文件的工具。该工具提供了一个简单的图形用户界面，用户可以通过拖拽文件夹到界面来执行合并操作。

## 技术实现

### 核心功能

1. **HTML文件处理**：解析HTML文件，识别其中引用的CSS、JavaScript和图片文件。
2. **资源嵌入**：
   - 将图片文件转换为base64编码并嵌入到HTML中
   - 将CSS和JavaScript文件内容直接嵌入到HTML的`<style>`和`<script>`标签中
3. **GUI界面**：使用PyQt5创建用户友好的图形界面，支持文件夹拖拽功能。

### 项目结构

- `gui.py`：图形用户界面实现
- `html_converter.py`：HTML转换核心逻辑
- `create_icon.py`：创建应用图标
- `requirements.txt`：项目依赖
- `run_gui.bat`：运行GUI的批处理文件

### 依赖项

- PyQt5==5.15.7

## 打包与分发

### 云端打包

1. 访问 [GitHub Actions](https://github.com/BENDIT233/html-merge-tool/actions) 页面
2. 找到并运行"Build Windows Executable"工作流
3. 下载生成的exe文件

## 使用说明

1. 运行`gui.exe`文件
2. 将包含HTML文件的文件夹拖拽到GUI界面
3. 工具将自动处理文件夹中的所有HTML文件，并在同级目录生成合并后的HTML文件

## 未来改进

- 支持更多资源类型
- 增加配置选项
- 改进错误处理和用户反馈

## 许可证

MIT
