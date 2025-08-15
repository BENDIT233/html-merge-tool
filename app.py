#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HTML合并工具 - 主应用程序入口

此文件是HTML合并工具的主入口，负责初始化应用程序、解析命令行参数
并启动Avalonia UI界面。
"""

import os
import sys
import subprocess
from html_converter import convert_single_folder

# 检查是否安装了pythonnet库，用于Python与.NET交互
HAS_PYTHONNET = True

# 尝试导入pythonnet
try:
    import clr
except ImportError:
    HAS_PYTHONNET = False
    print("警告: 未安装pythonnet库，Avalonia UI界面将无法启动。")


def run_avalonia_interface():
    """
    运行Avalonia UI界面

    此函数负责检查运行Avalonia UI所需的依赖（pythonnet和.NET SDK），
    如果依赖满足，则导入并运行avalonia_app.py中的run_avalonia_ui函数。

    Returns:
        bool: 如果Avalonia UI成功启动返回True，否则返回False
    """
    # 检查pythonnet库是否安装
    if not HAS_PYTHONNET:
        print("错误: 未安装pythonnet库，无法启动Avalonia UI界面。")
        print("请运行 'pip install pythonnet' 安装依赖。")
        return False

    try:
        # 检查是否安装了.NET SDK
        try:
            result = subprocess.run(['dotnet', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("错误: 未安装.NET SDK")
                print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
                return False
            else:
                print(f".NET SDK版本: {result.stdout.strip()}")
        except FileNotFoundError:
            print("错误: 未找到dotnet命令，可能未安装.NET SDK")
            print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
            return False

        # 导入并运行avalonia_app.py中的run_avalonia_ui函数
        from avalonia_app import run_avalonia_ui
        return run_avalonia_ui()
    except Exception as e:
        print(f"启动Avalonia UI界面时出错: {str(e)}")
        return False

def main():
    """
    主函数，负责解析命令行参数并启动应用程序

    此函数处理命令行参数，根据参数显示帮助信息或启动Avalonia UI界面。
    目前只支持avalonia界面类型。
    """
    # 解析命令行参数
    show_help = False
    interface_type = 'avalonia'  # 默认使用avalonia界面

    # 遍历所有命令行参数
    for arg in sys.argv[1:]:
        if arg in ['--help', '-h']:
            show_help = True
        elif arg.startswith('--interface='):
            # 解析--interface=avalonia格式的参数
            specified_type = arg.split('=', 1)[1].lower()
            if specified_type != 'avalonia':
                print("警告: 只支持avalonia界面类型，将使用默认界面")
        elif arg in ['--interface', '-i']:
            # 解析--interface avalonia格式的参数
            idx = sys.argv.index(arg) + 1
            if idx < len(sys.argv):
                specified_type = sys.argv[idx].lower()
                if specified_type != 'avalonia':
                    print("警告: 只支持avalonia界面类型，将使用默认界面")
            else:
                print("错误: '--interface' 参数需要指定界面类型 (avalonia)")
                show_help = True

    # 如果请求显示帮助信息
    if show_help:
        print("""HTML合并工具
使用方法:
  python app.py                       # 启动应用 (默认使用avalonia界面)
  python app.py --help                # 显示此帮助信息
  python app.py --interface=avalonia  # 启动Avalonia UI界面
  python app.py -i avalonia           # 简短形式启动Avalonia UI界面""")
        return 0

    # 启动avalonia界面
    print("启动Avalonia UI界面...")
    success = run_avalonia_interface()

    # 处理启动失败的情况
    if not success:
        print("avalonia界面启动失败！")
        print("请确保已安装必要的依赖库:")
        print("  - pythonnet: pip install pythonnet")
        print("  - .NET SDK: 从官方网站下载并安装 https://dotnet.microsoft.com/download")
        return

if __name__ == '__main__':
    """当作为脚本直接运行时，执行main函数"""
    main()