#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""创建应用程序图标

此脚本用于生成应用程序的图标文件。
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """创建应用程序图标"""
    # 创建256x256的图像
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    margin = 20
    circle_bbox = (margin, margin, size - margin, size - margin)
    draw.ellipse(circle_bbox, fill=(102, 126, 234, 255))  # #667eea
    
    # 绘制HTML标签图标
    # 绘制 < >
    tag_color = (255, 255, 255, 255)
    tag_size = 80
    tag_x = size // 2 - tag_size // 2
    tag_y = size // 2 - tag_size // 2
    
    # 绘制 <
    draw.line([(tag_x, tag_y + tag_size//2), (tag_x + 20, tag_y)], 
              fill=tag_color, width=8)
    draw.line([(tag_x, tag_y + tag_size//2), (tag_x + 20, tag_y + tag_size)], 
              fill=tag_color, width=8)
    
    # 绘制 >
    draw.line([(tag_x + tag_size - 20, tag_y), (tag_x + tag_size, tag_y + tag_size//2)], 
              fill=tag_color, width=8)
    draw.line([(tag_x + tag_size - 20, tag_y + tag_size), (tag_x + tag_size, tag_y + tag_size//2)], 
              fill=tag_color, width=8)
    
    # 绘制中间的斜杠
    draw.line([(tag_x + 30, tag_y + 20), (tag_x + tag_size - 30, tag_y + tag_size - 20)], 
              fill=tag_color, width=6)
    
    # 保存为ICO文件
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    icon_images = []
    
    for icon_size in icon_sizes:
        resized_image = image.resize(icon_size, Image.Resampling.LANCZOS)
        icon_images.append(resized_image)
    
    # 保存ICO文件
    icon_images[0].save('app_icon.ico', format='ICO', 
                       sizes=[(size[0], size[1]) for size in icon_sizes],
                       append_images=icon_images[1:])
    
    print("图标文件已创建: app_icon.ico")

if __name__ == '__main__':
    create_icon()
