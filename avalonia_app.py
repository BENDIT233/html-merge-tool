#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Avalonia UI 启动器

此文件负责加载Avalonia UI程序集并启动Avalonia UI界面，
是Python代码与.NET Avalonia UI之间的桥梁。
"""

import sys
import os
import subprocess
import clr

# 添加Avalonia UI项目的输出目录到搜索路径
# 这个路径指向Avalonia UI项目构建后的输出目录
avalonia_output_dir = os.path.join(os.path.dirname(__file__), 'avalonia_ui', 'bin', 'Debug', 'net8.0-windows')

# 检查Avalonia UI输出目录是否存在
if os.path.exists(avalonia_output_dir):
    sys.path.append(avalonia_output_dir)
    print(f"已添加Avalonia UI输出目录到搜索路径: {avalonia_output_dir}")
else:
    print(f"警告: 未找到Avalonia UI输出目录: {avalonia_output_dir}")
    print("请先构建Avalonia UI项目")

# 尝试加载Avalonia UI程序集
has_avalonia = False
Program = None

try:
    # 添加对HtmlMergeTool.AvaloniaUI程序集的引用
    clr.AddReference('HtmlMergeTool.AvaloniaUI')
    # 导入Program类
    from HtmlMergeTool.AvaloniaUI import Program
    has_avalonia = True
    print("成功加载Avalonia UI程序集")
except Exception as e:
    print(f"加载Avalonia UI失败: {str(e)}")
    has_avalonia = False

def run_avalonia_ui():
    """
    运行Avalonia UI界面

    此函数负责启动Avalonia UI应用程序，调用Avalonia UI项目中的Program.Main方法。

    Returns:
        bool: 如果Avalonia UI成功启动并运行返回True，否则返回False
    """
    if not has_avalonia or Program is None:
        print("无法运行Avalonia UI: 程序集加载失败")
        return False

    try:
        # 启动Avalonia UI应用程序，传入空参数列表
        print("正在启动Avalonia UI应用程序...")
        Program.Main([])
        return True
    except Exception as e:
        print(f"运行Avalonia UI时出错: {str(e)}")
        return False

def check_dotnet_sdk():
    """
    检查是否安装了.NET SDK

    Returns:
        bool: 如果已安装.NET SDK返回True，否则退出程序
    """
    try:
        result = subprocess.run(['dotnet', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("错误: 未安装.NET SDK")
            print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
            sys.exit(1)
        else:
            print(f".NET SDK版本: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        print("错误: 未找到dotnet命令，可能未安装.NET SDK")
        print("请从官方网站下载并安装.NET SDK: https://dotnet.microsoft.com/download")
        sys.exit(1)

def build_avalonia_project():
    """
    构建Avalonia UI项目

    如果Avalonia UI项目尚未构建，则尝试构建它。

    Returns:
        bool: 如果构建成功返回True，否则退出程序
    """
    dll_path = os.path.join(avalonia_output_dir, 'HtmlMergeTool.AvaloniaUI.dll')
    if not os.path.exists(dll_path):
        print(f"未找到Avalonia UI程序集: {dll_path}")
        print("尝试构建Avalonia UI项目...")
        try:
            project_path = os.path.join(os.path.dirname(__file__), 'avalonia_ui', 'HtmlMergeTool.AvaloniaUI.csproj')
            # 构建Avalonia UI项目
            subprocess.run([
                'dotnet', 'build',
                project_path,
                '-c', 'Debug'
            ], check=True)
            print("Avalonia UI项目构建成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"构建Avalonia UI项目失败: {str(e)}")
            sys.exit(1)
    else:
        print(f"已找到Avalonia UI程序集: {dll_path}")
        return True


if __name__ == '__main__':
    """当作为脚本直接运行时，检查依赖并启动Avalonia UI"""
    # 检查是否安装了.NET SDK
    check_dotnet_sdk()

    # 检查是否需要构建Avalonia UI项目
    build_avalonia_project()

    # 重新加载Avalonia UI程序集（因为可能刚刚构建完成）
    try:
        clr.AddReference('HtmlMergeTool.AvaloniaUI')
        from HtmlMergeTool.AvaloniaUI import Program
        has_avalonia = True
        print("成功重新加载Avalonia UI程序集")
    except Exception as e:
        print(f"重新加载Avalonia UI失败: {str(e)}")
        has_avalonia = False
        sys.exit(1)

    # 运行Avalonia UI
    success = run_avalonia_ui()

    if not success:
        print("Avalonia UI启动失败")
        sys.exit(1)

    # 应用程序退出后的提示
    print("Avalonia UI应用程序已退出")
    print("提示: 要完成完整集成，需要实现Avalonia UI与Python转换功能的交互")
    print("这通常涉及到在Avalonia UI项目中添加对Python代码的调用，或通过事件回调进行交互。")