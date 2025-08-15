import eel
import os
import sys
import time
from html_converter import convert_single_folder

# 初始化Eel
# 设置web文件夹为前端资源目录
@eel.expose
def browse_folder():
    """
    打开文件夹选择对话框
    :return: 选中的文件夹路径
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        folder_path = filedialog.askdirectory(title="选择文件夹")
        root.destroy()
        return folder_path
    except Exception as e:
        print(f"浏览文件夹出错: {str(e)}")
        return None

@eel.expose
def browse_output_dir():
    """
    打开输出目录选择对话框
    :return: 选中的目录路径
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        folder_path = filedialog.askdirectory(title="选择输出目录")
        root.destroy()
        return folder_path
    except Exception as e:
        print(f"浏览输出目录出错: {str(e)}")
        return None

@eel.expose
def handle_drop(path):
    """
    处理拖拽的文件夹
    :param path: 拖拽的文件夹路径
    :return: 有效的文件夹路径或None
    """
    if os.path.isdir(path):
        return path
    return None

@eel.expose
def start_conversion(input_path, output_format, output_dir):
    """
    开始转换过程
    :param input_path: 输入文件夹路径
    :param output_format: 输出格式 ('html' 或 'mhtml')
    :param output_dir: 输出目录
    """
    try:
        # 模拟进度更新
        for i in range(101):
            eel.update_progress(i)
            time.sleep(0.02)

        # 调用转换函数
        output_file = convert_single_folder(input_path, output_format, output_dir)

        if output_file:
            eel.on_conversion_finished(True, f"转换成功！输出文件位于:\n{output_file}")
        else:
            eel.on_conversion_finished(False, "转换失败: 未找到HTML文件或处理出错")
    except Exception as e:
        eel.on_conversion_finished(False, f"转换失败: {str(e)}")

def main():
    """
    主函数，启动应用
    """
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("HTML合并工具\n使用方法:\n  python app.py           # 启动应用\n  python app.py --help    # 显示此帮助信息")
        return 0

    # 初始化Eel
    eel.init('web')

    # 启动应用
    eel.start('index.html', size=(700, 800), port=0, mode='default')

if __name__ == '__main__':
    main()