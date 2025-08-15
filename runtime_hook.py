#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""PyInstaller 运行时钩子

此文件在应用程序启动时执行，用于减少误报和优化运行环境。
"""

import os
import sys
import platform

def setup_environment():
    """设置运行环境"""
    # 设置应用程序信息
    os.environ['HTML_MERGE_TOOL_VERSION'] = '1.0.0'
    os.environ['HTML_MERGE_TOOL_BUILD'] = 'release'
    
    # 设置平台信息
    os.environ['PLATFORM'] = platform.system()
    os.environ['ARCHITECTURE'] = platform.architecture()[0]
    
    # 设置Python路径
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller打包后的路径
        os.environ['APP_PATH'] = sys._MEIPASS
    else:
        # 开发环境路径
        os.environ['APP_PATH'] = os.path.dirname(os.path.abspath(__file__))

def reduce_false_positives():
    """减少误报"""
    # 设置一些环境变量来减少误报
    os.environ['PYTHONHASHSEED'] = '0'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    # 禁用一些可能导致误报的功能
    if hasattr(sys, 'setdlopenflags'):
        try:
            import ctypes
            sys.setdlopenflags(ctypes.RTLD_GLOBAL)
        except:
            pass

def main():
    """主函数"""
    try:
        setup_environment()
        reduce_false_positives()
        print("Runtime hook executed successfully")
    except Exception as e:
        print(f"Runtime hook error: {e}")

if __name__ == '__main__':
    main()
