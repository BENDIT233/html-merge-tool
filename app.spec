#!/usr/bin/env python3
# -*- mode: python ; coding: utf-8 -*-

"""PyInstaller 配置文件

此文件用于配置 PyInstaller 打包应用程序的参数和选项。
通过此文件可以控制打包过程中的各种行为，如包含的模块、
生成的可执行文件类型、是否使用压缩等。
"""

# Analysis 类用于分析 Python 脚本及其依赖关系
# 它会找出所有需要包含的模块、库和资源

a = Analysis(
    # 需要打包的主 Python 文件列表
    ['app.py'],
    # 额外的搜索路径列表，用于查找模块和依赖
    pathex=['.'],
    # 需要包含的二进制文件列表
    binaries=[],
    # 需要包含的数据文件列表 (源路径, 目标路径) 元组
    datas=[],
    # 隐藏的导入模块列表，这些模块不会被自动检测到
    # 添加更多必要的导入以确保在未安装Python的系统上运行
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        'pkg_resources',
    ],
    # 自定义钩子文件的路径列表
    hookspath=[],
    # 运行时钩子文件列表，这些脚本会在应用启动时执行
    # 添加一个运行时钩子来减少误报
    runtime_hooks=['runtime_hook.py'],
    # 钩子配置字典
    hooksconfig={'distutils': {'noarchive': True}},
    # 要排除的模块列表
    # 排除一些可能被误报为病毒的模块
    excludes=[
        'cryptography', 
        'pycrypto', 
        'pycryptodome', 
        'pynacl', 
        'win32api', 
        'win32con', 
        'win32gui',
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'eel',
        'bottle',
        'gevent',
        'clr_loader',
        'cffi'
    ],
    # 不将所有 Python 模块打包成一个归档文件
    # 非归档模式可以减少误报率
    noarchive=True,
    # 优化级别 (0=无优化, 1=基本优化, 2=额外优化)
    # 低优化级别可以减少误报率
    optimize=1,
)

# 创建一个 Python 字节码归档文件 (PYZ)
# 这个文件包含了所有的 Python 模块的字节码
pyz = PYZ(a.pure)

# 创建可执行文件 (EXE)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='html_merge_tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 禁用UPX压缩以减少误报
    console=False,  # 设置为False以隐藏控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico' if os.path.exists('app_icon.ico') else None,
)

# 创建目录模式的可执行文件
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,  # 禁用UPX压缩
    upx_exclude=[],
    name='html_merge_tool',
)
