import sys
import os
import clr

# 添加Avalonia UI项目的输出目录到搜索路径
# 注意：这个路径需要根据实际的构建输出目录进行调整
avalonia_output_dir = os.path.join(os.path.dirname(__file__), 'avalonia_ui', 'bin', 'Debug', 'net8.0-windows')
if os.path.exists(avalonia_output_dir):
    sys.path.append(avalonia_output_dir)
else:
    print(f"警告: 未找到Avalonia UI输出目录: {avalonia_output_dir}")
    print("请先构建Avalonia UI项目")

# 尝试加载Avalonia UI程序集
try:
    clr.AddReference('HtmlMergeTool.AvaloniaUI')
    from HtmlMergeTool.AvaloniaUI import Program
    has_avalonia = True
except Exception as e:
    print(f"加载Avalonia UI失败: {str(e)}")
    has_avalonia = False

def run_avalonia_ui():
    """
    运行Avalonia UI界面
    """
    if not has_avalonia:
        print("无法运行Avalonia UI: 程序集加载失败")
        return False

    try:
        # 启动Avalonia UI应用程序
        Program.Main([])
        return True
    except Exception as e:
        print(f"运行Avalonia UI时出错: {str(e)}")
        return False

if __name__ == '__main__':
    # 检查是否安装了.NET SDK
    try:
        import subprocess
        result = subprocess.run(['dotnet', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("错误: 未安装.NET SDK")
            print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
            sys.exit(1)
        else:
            print(f".NET SDK版本: {result.stdout.strip()}")
    except FileNotFoundError:
        print("错误: 未找到dotnet命令，可能未安装.NET SDK")
        print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
        sys.exit(1)

    # 检查是否需要构建Avalonia UI项目
    if not os.path.exists(os.path.join(avalonia_output_dir, 'HtmlMergeTool.AvaloniaUI.dll')):
        print("Avalonia UI项目尚未构建，尝试构建...")
        try:
            # 构建Avalonia UI项目
            subprocess.run([
                'dotnet', 'build',
                os.path.join(os.path.dirname(__file__), 'avalonia_ui', 'HtmlMergeTool.AvaloniaUI.csproj'),
                '-c', 'Debug'
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"构建Avalonia UI项目失败: {str(e)}")
            sys.exit(1)

    # 运行Avalonia UI
    run_avalonia_ui()

    # 集成Python的HTML转换功能
    # 注意：这里需要实现Avalonia UI与Python转换功能的交互
    # 例如，可以通过事件或回调函数来调用html_converter.py中的功能
    # 由于时间关系，这里只提供框架，具体实现需要进一步开发
    print("Avalonia UI应用程序已退出")
    print("提示: 要完成完整集成，需要实现Avalonia UI与Python转换功能的交互")