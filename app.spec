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
    pathex=[],
    # 需要包含的二进制文件列表
    binaries=[],
    # 需要包含的数据文件列表 (源路径, 目标路径) 元组
    datas=[],
    # 隐藏的导入模块列表，这些模块不会被自动检测到
# 添加更多必要的导入以确保在未安装Python的系统上运行
hiddenimports=['eel', 'eel.browsers', 'eel.chrome', 'pkg_resources'],
# 额外的搜索路径列表，用于查找模块和依赖
pathex=['.'],
# 需要包含的数据文件列表 (源路径, 目标路径) 元组
datas=[],
    # 自定义钩子文件的路径列表
    hookspath=[],
    # 钩子配置字典
    hooksconfig={},
    # 运行时钩子文件列表，这些脚本会在应用启动时执行
    # 添加一个运行时钩子来减少误报
    runtime_hooks=['runtime_hook.py'],
    # 钩子配置字典
    hooksconfig={'distutils': {'noarchive': True}},
    # 要排除的模块列表
    # 排除一些可能被误报为病毒的模块
    # 排除一些可能被误报为病毒的模块
    excludes=['cryptography', 'pycrypto', 'pycryptodome', 'pynacl', 'win32api', 'win32con', 'win32gui'],
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
    # Python 字节码归档文件
    pyz,
    # 脚本列表
    a.scripts,
    # 二进制文件列表
    a.binaries,
    # 数据文件列表
    a.datas,
    # 额外的运行时库列表
    [],
    # 生成的可执行文件名称
    name='app',
    # 是否启用调试模式
    debug=False,
    # 引导加载程序是否忽略信号
    bootloader_ignore_signals=False,
    # 是否去除符号表 (仅适用于非 Windows 系统)
    strip=False,
    # 是否使用 UPX 压缩可执行文件
    upx=False,
    # UPX 压缩时要排除的文件列表
    upx_exclude=[],
    # 运行时临时目录，None 表示使用系统默认临时目录
    runtime_tmpdir=None,
    # 是否显示控制台窗口
    # False 表示创建窗口应用程序 (无控制台)
    console=False,
    # 是否禁用窗口应用程序的回溯信息
    disable_windowed_traceback=False,
    # 是否模拟 argv (仅适用于 Mac OS X)
    argv_emulation=False,
    # 目标架构 (如 x86_64, arm64 等)
    target_arch=None,
    # 代码签名标识 (仅适用于 Mac OS X)
    codesign_identity=None,
    # 权限文件路径 (仅适用于 Mac OS X)
    entitlements_file=None,
)
