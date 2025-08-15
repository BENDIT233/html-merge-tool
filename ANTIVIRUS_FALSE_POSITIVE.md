# 防病毒软件误报解决方案

## 问题概述

我们的应用程序在某些防病毒软件中可能被误报为恶意软件。这是PyInstaller打包的应用程序常见的问题，尤其是在没有数字签名的情况下。

## 已实施的解决方案

为了减少误报，我们已经在项目中实施了以下措施：

### 1. 打包配置优化

- **禁用UPX压缩**：UPX压缩可能会导致某些防病毒软件误报
- **使用onedir模式**：生成目录而不是单个文件，减少误报风险
- **增加优化级别**：设置为1级优化，平衡性能和安全性
- **排除敏感模块**：排除了可能被误报的加密和系统模块
- **启用noarchive模式**：不将所有模块打包成一个归档文件
- **添加运行时钩子**：提供更明确的应用程序信息

### 2. 构建流程优化

- **使用最新版本的PyInstaller**：包含最新的误报修复
- **清理构建缓存**：使用--clean参数确保每次构建都是干净的
- **添加数字签名支持**：提供了本地签名的参考步骤

## 进一步减少误报的建议

### 1. 数字签名

为可执行文件添加数字签名是减少误报最有效的方法：

1. 获取代码签名证书 (可从Digicert、GlobalSign等提供商处购买)
2. 使用signtool或其他签名工具签名可执行文件：
   ```powershell
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist/app/html_merge_tool.exe
   ```

### 2. 添加到防病毒白名单

指导用户将应用程序添加到他们防病毒软件的信任列表中：

- **Windows Defender**：设置 > 更新和安全 > Windows安全 > 病毒和威胁防护 > 病毒和威胁防护设置 > 排除项 > 添加或删除排除项
- **Avast**：菜单 > 设置 > 防护 > 病毒扫描 > 排除项
- **Kaspersky**：设置 > 威胁和排除项 > 排除项 > 添加

### 3. 本地构建

建议用户在本地环境构建应用程序，而不是直接下载可执行文件：

```powershell
# 克隆仓库
git clone https://github.com/yourusername/html-merge-tool.git
cd html-merge-tool

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 构建应用程序
pyinstaller --onedir --windowed --noupx --clean app.py

# 运行应用程序
dist\app\app.exe
```

## 报告误报

如果应用程序仍然被误报，请向相应的防病毒供应商报告误报：

- **Windows Defender**：https://www.microsoft.com/en-us/wdsi/filesubmission
- **Avast**：https://www.avast.com/false-positive-file-form
- **Kaspersky**：https://virusdesk.kaspersky.com/
- **McAfee**：https://www.mcafee.com/enterprise/en-us/support/submit-sample.html

## 联系我们

如果您有任何问题或需要进一步的帮助，请联系我们的支持团队。