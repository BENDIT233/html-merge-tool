import os
import re
import base64
from pathlib import Path
import mimetypes

def convert_folder_to_single_html(folder_path, output_format='html'):
    """
    将包含资源的HTML文件夹转换为单个HTML或MHTML文件
    :param folder_path: 文件夹路径
    :param output_format: 输出格式，'html'或'mhtml'
    """
    # 获取文件夹名称作为输出文件名
    folder_name = os.path.basename(folder_path)
    output_file = os.path.join(os.path.dirname(folder_path), f"{folder_name}.{output_format}")
    
    # 查找主HTML文件（通常是index.html）
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    if not html_files:
        print(f"警告：文件夹 {folder_path} 中未找到HTML文件")
        return
        
    # 通常第一个HTML文件或index.html是主文件
    main_html = "index.html" if "index.html" in html_files else html_files[0]
    main_html_path = os.path.join(folder_path, main_html)
    
    # 读取HTML内容
    with open(main_html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
    
    # 处理图片资源
    html_content = replace_images(html_content, folder_path)
    
    # 处理CSS资源
    html_content = replace_css(html_content, folder_path)
    
    # 处理JS资源
    html_content = replace_js(html_content, folder_path)
    
    # 保存为单个文件
    if output_format == 'mhtml':
        save_as_mhtml(html_content, output_file, folder_name)
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"已转换: {output_file}")

def replace_images(html_content, base_folder):
    """将img标签的src替换为base64编码"""
    img_pattern = re.compile(r'<img[^>]*src="([^"]+)"[^>]*>')
    
    def replace_func(match):
        src = match.group(1)
        # 跳过绝对路径和已处理的base64
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
            
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read()).decode('utf-8')
            
        return f'<img{match.group(0)[4:-1].replace(src, f"data:{mime_type};base64,{base64_data}")}>'
    
    return img_pattern.sub(replace_func, html_content)

def replace_css(html_content, base_folder):
    """将link标签的CSS替换为内联style"""
    css_pattern = re.compile(r'<link[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>')
    
    def replace_func(match):
        href = match.group(1)
        if href.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        css_path = os.path.join(base_folder, href)
        css_path = os.path.normpath(css_path)
        
        if not os.path.exists(css_path):
            print(f"警告：CSS文件不存在 {css_path}")
            return match.group(0)
            
        with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
            css_content = f.read()
            
        return f'<style>\n{css_content}\n</style>'
    
    return css_pattern.sub(replace_func, html_content)

def replace_js(html_content, base_folder):
    """将script标签的JS替换为内联脚本"""
    js_pattern = re.compile(r'<script[^>]*src="([^"]+)"[^>]*></script>')
    
    def replace_func(match):
        src = match.group(1)
        if src.startswith(('http://', 'https://', 'data:')):
            return match.group(0)
            
        js_path = os.path.join(base_folder, src)
        js_path = os.path.normpath(js_path)
        
        if not os.path.exists(js_path):
            print(f"警告：JS文件不存在 {js_path}")
            return match.group(0)
            
        with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
            js_content = f.read()
            
        return f'<script>\n{js_content}\n</script>'
    
    return js_pattern.sub(replace_func, html_content)

def save_as_mhtml(html_content, output_file, title):
    """保存为MHTML格式"""
    import time
    boundary = "----=MHTMLBoundary" + base64.b64encode(os.urandom(16)).decode('utf-8')
    
    # 使用time模块替代pandas来生成日期
    date_str = time.strftime('%a, %d %b %Y %H:%M:%S %z', time.localtime())
    
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
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(mhtml)

def convert_single_folder(folder_path, output_format='html', output_dir=None):
    """
    转换单个文件夹为HTML或MHTML文件
    :param folder_path: 文件夹路径
    :param output_format: 输出格式，'html'或'mhtml'
    :param output_dir: 输出目录，默认为None（保存在输入文件夹的同级目录）
    :return: 输出文件路径
    """
    # 获取文件夹名称作为输出文件名
    folder_name = os.path.basename(folder_path)
    
    # 确定输出目录
    if output_dir:
        output_path = output_dir
    else:
        output_path = os.path.dirname(folder_path)
        
    output_file = os.path.join(output_path, f"{folder_name}.{output_format}")
    
    # 查找主HTML文件（通常是index.html）
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    if not html_files:
        print(f"警告：文件夹 {folder_path} 中未找到HTML文件")
        return None
        
    # 通常第一个HTML文件或index.html是主文件
    main_html = "index.html" if "index.html" in html_files else html_files[0]
    main_html_path = os.path.join(folder_path, main_html)
    
    # 读取HTML内容
    with open(main_html_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
    
    # 处理图片资源
    html_content = replace_images(html_content, folder_path)
    
    # 处理CSS资源
    html_content = replace_css(html_content, folder_path)
    
    # 处理JS资源
    html_content = replace_js(html_content, folder_path)
    
    # 保存为单个文件
    if output_format == 'mhtml':
        save_as_mhtml(html_content, output_file, folder_name)
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"已转换: {output_file}")
    return output_file

def batch_convert(folder_path, output_format='html', output_dir=None, progress_callback=None):
    """
    批量转换文件夹中的所有子文件夹或当前文件夹
    :param folder_path: 文件夹路径
    :param output_format: 输出格式，'html'或'mhtml'
    :param output_dir: 输出目录，默认为None（保存在输入文件夹的同级目录）
    :param progress_callback: 进度回调函数
    """
    # 检查是否存在子文件夹
    subfolders = [item for item in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, item))]
    
    # 检查当前文件夹是否包含HTML文件
    current_folder_has_html = any(f.endswith('.html') for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    
    if subfolders and not current_folder_has_html:
        # 如果有子文件夹且当前文件夹没有HTML文件，则转换所有子文件夹
        items = subfolders
        total = len(items)
        
        for i, item in enumerate(items):
            item_path = os.path.join(folder_path, item)
            convert_single_folder(item_path, output_format, output_dir)
            
            # 更新进度
            if progress_callback:
                progress_callback(int((i + 1) / total * 100))
    else:
        # 如果没有子文件夹或当前文件夹有HTML文件，则转换当前文件夹
        convert_single_folder(folder_path, output_format, output_dir)
        if progress_callback:
            progress_callback(100)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='将带资源的HTML文件夹转换为单个HTML或MHTML文件')
    parser.add_argument('folder', help='包含多个HTML文件夹的父目录')
    parser.add_argument('-f', '--format', choices=['html', 'mhtml'], default='html',
                      help='输出文件格式，默认为html')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"错误：{args.folder} 不是有效的目录")
    else:
        batch_convert(args.folder, args.format)
        print("转换完成！")
