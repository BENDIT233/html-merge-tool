#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HTML合并工具 - 资源转换模块

此模块提供将包含资源(图片、CSS、JS等)的HTML文件夹转换为单个HTML或MHTML文件的功能。
主要功能包括：
- 处理HTML文件中的图片资源，转换为base64编码
- 处理CSS资源，转换为内联样式
- 处理JavaScript资源，转换为内联脚本
- 支持单文件夹转换和批量转换
- 支持输出为HTML或MHTML格式
"""

import os
import re
import base64
import mimetypes
from pathlib import Path


def convert_folder_to_single_html(folder_path, output_format='html'):
    """
    将包含资源的HTML文件夹转换为单个HTML或MHTML文件

    此函数是HTML资源转换的主要入口，它会查找文件夹中的主HTML文件，
    处理其中的图片、CSS和JavaScript资源，并将其合并为单个文件。

    Args:
        folder_path (str): 包含HTML文件和相关资源的文件夹路径
        output_format (str, optional): 输出文件格式，可选值为'html'或'mhtml'，默认为'html'
    """
    # 获取文件夹名称作为输出文件名
    folder_name = os.path.basename(folder_path)
    output_file = os.path.join(os.path.dirname(folder_path), f"{folder_name}.{output_format}")

    # 查找主HTML文件（通常是index.html）
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    if not html_files:
        print(f"警告：文件夹 {folder_path} 中未找到HTML文件")
        return
        
    # 优先选择index.html作为主文件，如果不存在则选择第一个找到的HTML文件
    main_html = "index.html" if "index.html" in html_files else html_files[0]
    main_html_path = os.path.join(folder_path, main_html)
    print(f"找到主HTML文件: {main_html_path}")

    # 读取HTML内容
    try:
        with open(main_html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        print(f"已读取HTML内容，长度: {len(html_content)} 字符")
    except Exception as e:
        print(f"读取HTML文件失败: {str(e)}")
        return

    # 处理图片资源
    html_content = replace_images(html_content, folder_path)

    # 处理CSS资源
    html_content = replace_css(html_content, folder_path)

    # 处理JS资源
    html_content = replace_js(html_content, folder_path)

    # 保存为单个文件
    try:
        if output_format == 'mhtml':
            save_as_mhtml(html_content, output_file, folder_name)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        print(f"已成功转换并保存到: {output_file}")
    except Exception as e:
        print(f"保存文件失败: {str(e)}")

def replace_images(html_content, base_folder):
    """
    将HTML内容中的img标签的src属性替换为base64编码

    此函数会查找HTML中所有的img标签，将本地图片文件转换为base64编码并嵌入到HTML中，
    从而实现图片资源的内联。

    Args:
        html_content (str): HTML内容字符串
        base_folder (str): HTML文件所在的基础文件夹路径

    Returns:
        str: 处理后的HTML内容字符串
    """
    # 匹配img标签的正则表达式
    img_pattern = re.compile(r'<img[^>]*src="([^"]+)"[^>]*>')
    processed_count = 0

    def replace_func(match):
        nonlocal processed_count
        src = match.group(1)
        # 跳过绝对路径和已处理的base64图片
        if src.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        # 构建完整路径
        img_path = os.path.join(base_folder, src)
        img_path = os.path.normpath(img_path)

        if not os.path.exists(img_path):
            print(f"警告：图片文件不存在 {img_path}")
            return match.group(0)
            
        # 转换为base64
        mime_type, _ = mimetypes.guess_type(img_path)
        if not mime_type:
            mime_type = 'image/unknown'
            
        try:
            with open(img_path, 'rb') as f:
                base64_data = base64.b64encode(f.read()).decode('utf-8')
            processed_count += 1
            print(f"已处理图片: {img_path}")
            return f'<img{match.group(0)[4:-1].replace(src, f"data:{mime_type};base64,{base64_data}")}>'
        except Exception as e:
            print(f"处理图片失败 {img_path}: {str(e)}")
            return match.group(0)

    result = img_pattern.sub(replace_func, html_content)
    print(f"总计处理图片数量: {processed_count}")
    return result

def replace_css(html_content, base_folder):
    """
    将HTML内容中的link标签引用的CSS文件替换为内联style标签

    此函数会查找HTML中所有引用CSS文件的link标签，读取CSS文件内容，
    并将其替换为内联的style标签，从而实现CSS资源的内联。

    Args:
        html_content (str): HTML内容字符串
        base_folder (str): HTML文件所在的基础文件夹路径

    Returns:
        str: 处理后的HTML内容字符串
    """
    # 匹配link标签(stylesheet)的正则表达式
    css_pattern = re.compile(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>')
    processed_count = 0

    def replace_func(match):
        nonlocal processed_count
        href = match.group(1)
        # 跳过绝对路径和数据URL
        if href.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        # 构建完整路径
        css_path = os.path.join(base_folder, href)
        css_path = os.path.normpath(css_path)

        if not os.path.exists(css_path):
            print(f"警告：CSS文件不存在 {css_path}")
            return match.group(0)
            
        try:
            with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
                css_content = f.read()
            processed_count += 1
            print(f"已处理CSS文件: {css_path}")
            return f'<style>\n{css_content}\n</style>'
        except Exception as e:
            print(f"处理CSS文件失败 {css_path}: {str(e)}")
            return match.group(0)

    result = css_pattern.sub(replace_func, html_content)
    print(f"总计处理CSS文件数量: {processed_count}")
    return result

def replace_js(html_content, base_folder):
    """
    将HTML内容中的script标签引用的JS文件替换为内联脚本

    此函数会查找HTML中所有引用JS文件的script标签，读取JS文件内容，
    并将其替换为内联的script标签，从而实现JS资源的内联。

    Args:
        html_content (str): HTML内容字符串
        base_folder (str): HTML文件所在的基础文件夹路径

    Returns:
        str: 处理后的HTML内容字符串
    """
    # 匹配script标签的正则表达式
    js_pattern = re.compile(r'<script[^>]*src="([^"]+)"[^>]*></script>')
    processed_count = 0

    def replace_func(match):
        nonlocal processed_count
        src = match.group(1)
        # 跳过绝对路径和数据URL
        if src.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        # 构建完整路径
        js_path = os.path.join(base_folder, src)
        js_path = os.path.normpath(js_path)

        if not os.path.exists(js_path):
            print(f"警告：JS文件不存在 {js_path}")
            return match.group(0)
            
        try:
            with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
                js_content = f.read()
            processed_count += 1
            print(f"已处理JS文件: {js_path}")
            return f'<script>\n{js_content}\n</script>'
        except Exception as e:
            print(f"处理JS文件失败 {js_path}: {str(e)}")
            return match.group(0)

    result = js_pattern.sub(replace_func, html_content)
    print(f"总计处理JS文件数量: {processed_count}")
    return result

def save_as_mhtml(html_content, output_file, title):
    """
    将HTML内容保存为MHTML格式

    MHTML(MIME HTML)是一种将HTML文档及其所有资源(图片、CSS、JS等)
    打包成单个文件的格式。此函数将处理后的HTML内容保存为MHTML格式。

    Args:
        html_content (str): 处理后的HTML内容字符串
        output_file (str): 输出文件路径
        title (str): MHTML文件的标题
    """
    import time
    # 生成唯一的边界标识符
    boundary = "----=MHTMLBoundary" + base64.b64encode(os.urandom(16)).decode('utf-8')

    # 生成符合RFC 822格式的日期字符串
    date_str = time.strftime('%a, %d %b %Y %H:%M:%S %z', time.localtime())

    # 构建MHTML内容
    mhtml = f"""From: <saved by html_converter.py>
Subject: {title}
Date: {date_str}
MIME-Version: 1.0
Content-Type: multipart/related;
    boundary="{boundary}";
    type="text/html"

--{boundary}
Content-Type: text/html; charset="utf-8"
Content-Transfer-Encoding: 8bit
Content-Location: index.html

{html_content}

--{boundary}--
"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(mhtml)
        print(f"已保存为MHTML格式: {output_file}")
    except Exception as e:
        print(f"保存MHTML文件失败: {str(e)}")

def convert_single_folder(folder_path, output_format='html', output_dir=None):
    """
    转换单个文件夹为HTML或MHTML文件

    此函数与convert_folder_to_single_html功能相似，但增加了输出目录的选项，
    并返回输出文件路径。

    Args:
        folder_path (str): 包含HTML文件和相关资源的文件夹路径
        output_format (str, optional): 输出文件格式，可选值为'html'或'mhtml'，默认为'html'
        output_dir (str, optional): 输出目录路径，默认为None（保存在输入文件夹的同级目录）

    Returns:
        str or None: 成功转换后返回输出文件路径，失败则返回None
    """
    # 获取文件夹名称作为输出文件名
    folder_name = os.path.basename(folder_path)

    # 确定输出目录
    if output_dir:
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        output_path = output_dir
    else:
        output_path = os.path.dirname(folder_path)
        
    output_file = os.path.join(output_path, f"{folder_name}.{output_format}")
    print(f"准备转换文件夹: {folder_path} 到 {output_file}")

    # 查找主HTML文件（通常是index.html）
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    if not html_files:
        print(f"警告：文件夹 {folder_path} 中未找到HTML文件")
        return None
        
    # 优先选择index.html作为主文件，如果不存在则选择第一个找到的HTML文件
    main_html = "index.html" if "index.html" in html_files else html_files[0]
    main_html_path = os.path.join(folder_path, main_html)
    print(f"找到主HTML文件: {main_html_path}")

    # 读取HTML内容
    try:
        with open(main_html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        print(f"已读取HTML内容，长度: {len(html_content)} 字符")
    except Exception as e:
        print(f"读取HTML文件失败: {str(e)}")
        return None

    # 处理图片资源
    html_content = replace_images(html_content, folder_path)

    # 处理CSS资源
    html_content = replace_css(html_content, folder_path)

    # 处理JS资源
    html_content = replace_js(html_content, folder_path)

    # 保存为单个文件
    try:
        if output_format == 'mhtml':
            save_as_mhtml(html_content, output_file, folder_name)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        print(f"已成功转换并保存到: {output_file}")
        return output_file
    except Exception as e:
        print(f"保存文件失败: {str(e)}")
        return None

def batch_convert(folder_path, output_format='html', output_dir=None, progress_callback=None):
    """
    批量转换文件夹中的所有子文件夹或当前文件夹

    此函数可以批量处理多个文件夹，根据情况自动选择转换子文件夹或当前文件夹。
    支持进度回调，可以实时获取转换进度。

    Args:
        folder_path (str): 要处理的文件夹路径
        output_format (str, optional): 输出文件格式，可选值为'html'或'mhtml'，默认为'html'
        output_dir (str, optional): 输出目录路径，默认为None（保存在输入文件夹的同级目录）
        progress_callback (callable, optional): 进度回调函数，接受一个0-100的整数参数表示进度
    """
    print(f"开始批量转换: {folder_path}")
    # 检查是否存在子文件夹
    subfolders = [item for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item))]

    # 检查当前文件夹是否包含HTML文件
    current_folder_has_html = any(f.endswith('.html') for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))

    if subfolders and not current_folder_has_html:
        # 如果有子文件夹且当前文件夹没有HTML文件，则转换所有子文件夹
        items = subfolders
        total = len(items)
        print(f"发现 {total} 个子文件夹需要转换")

        for i, item in enumerate(items):
            item_path = os.path.join(folder_path, item)
            convert_single_folder(item_path, output_format, output_dir)
            
            # 更新进度
            progress = int((i + 1) / total * 100)
            if progress_callback:
                progress_callback(progress)
            print(f"批量转换进度: {progress}%")
    else:
        # 如果没有子文件夹或当前文件夹有HTML文件，则转换当前文件夹
        print("转换当前文件夹")
        convert_single_folder(folder_path, output_format, output_dir)
        if progress_callback:
            progress_callback(100)
        print("批量转换完成")

if __name__ == "__main__":
    """当作为脚本直接运行时的入口点"""
    import argparse

    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将带资源的HTML文件夹转换为单个HTML或MHTML文件')
    parser.add_argument('folder', help='包含HTML文件的目录路径')
    parser.add_argument('-f', '--format', choices=['html', 'mhtml'], default='html',
                      help='输出文件格式，默认为html')
    parser.add_argument('-o', '--output-dir', help='输出文件目录，默认为输入文件夹的同级目录')

    # 解析命令行参数
    args = parser.parse_args()

    # 验证输入目录是否有效
    if not os.path.isdir(args.folder):
        print(f"错误：{args.folder} 不是有效的目录")
        exit(1)
    else:
        # 执行批量转换
        batch_convert(args.folder, args.format, args.output_dir)
        print("转换完成！")

# 版本信息
__version__ = '1.0.0'
__author__ = 'HTML Merge Tool Project Team'
__copyright__ = 'Copyright 2023 HTML Merge Tool Project'
