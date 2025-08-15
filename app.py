#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""HTML合并工具 - 主应用程序入口

此文件是HTML合并工具的主入口，使用PyQt5创建现代化的桌面GUI界面。
"""

import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QComboBox, 
                             QLineEdit, QProgressBar, QTextEdit, QFileDialog,
                             QFrame, QGridLayout, QMessageBox, QGroupBox, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QDragEnterEvent, QDropEvent
from html_converter import convert_single_folder, batch_convert

class ConversionWorker(QThread):
    """转换工作线程"""
    progress_updated = pyqtSignal(int)
    conversion_finished = pyqtSignal(bool, str, str)
    
    def __init__(self, folder_path, output_format, output_dir, is_batch=False):
        super().__init__()
        self.folder_path = folder_path
        self.output_format = output_format
        self.output_dir = output_dir
        self.is_batch = is_batch
        
    def run(self):
        try:
            if self.is_batch:
                # 批量转换
                progress_results = []
                def progress_callback(progress):
                    progress_results.append(progress)
                    self.progress_updated.emit(progress)
                
                batch_convert(self.folder_path, self.output_format, self.output_dir, progress_callback)
                self.conversion_finished.emit(True, "批量转换完成", f"处理了 {len(progress_results)} 个项目")
            else:
                # 单个转换
                self.progress_updated.emit(50)
                result = convert_single_folder(self.folder_path, self.output_format, self.output_dir)
                if result:
                    self.progress_updated.emit(100)
                    self.conversion_finished.emit(True, "转换成功", result)
                else:
                    self.conversion_finished.emit(False, "转换失败", "无法处理指定文件夹")
        except Exception as e:
            self.conversion_finished.emit(False, "转换出错", str(e))

class DragDropWidget(QFrame):
    """支持拖拽的组件"""
    file_dropped = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.Box)
        self.setMinimumHeight(140)
        self.setStyleSheet("""
            QFrame {
                border: 3px dashed #667eea;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e8f0ff);
                padding: 25px;
                margin: 15px;
            }
            QFrame:hover {
                border-color: #5a6fd8;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f0ff, stop:1 #d4e3ff);
            }
        """)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    border: 3px dashed #28a745;
                    border-radius: 15px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #d4edda, stop:1 #c3e6cb);
                    padding: 25px;
                    margin: 15px;
                }
            """)
            
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QFrame {
                border: 3px dashed #667eea;
                border-radius: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e8f0ff);
                padding: 25px;
                margin: 15px;
            }
            QFrame:hover {
                border-color: #5a6fd8;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e8f0ff, stop:1 #d4e3ff);
            }
        """)
            
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            path = urls[0].toLocalFile()
            if os.path.isdir(path):
                self.file_dropped.emit(path)
        self.dragLeaveEvent(event)

class ModernButton(QPushButton):
    """现代化按钮样式"""
    def __init__(self, text, color="#667eea", icon=None, size="medium"):
        super().__init__(text)
        if icon:
            self.setIcon(icon)
        
        # 根据尺寸设置不同的样式
        if size == "large":
            padding = "15px 30px"
            font_size = "16px"
            min_height = "50px"
        elif size == "small":
            padding = "8px 16px"
            font_size = "12px"
            min_height = "35px"
        else:  # medium
            padding = "12px 24px"
            font_size = "14px"
            min_height = "42px"
            
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {self._darken_color(color)});
                color: white;
                border: none;
                border-radius: 10px;
                padding: {padding};
                font-size: {font_size};
                font-weight: 600;
                min-height: {min_height};
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self._lighten_color(color)}, stop:1 {color});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self._darken_color(color, 0.3)}, stop:1 {self._darken_color(color, 0.5)});
            }}
            QPushButton:disabled {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cccccc, stop:1 #bbbbbb);
                color: #666666;
            }}
        """)
        
    def _darken_color(self, color, factor=0.1):
        """使颜色变暗"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(0, int(c * (1 - factor))) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _lighten_color(self, color, factor=0.1):
        """使颜色变亮"""
        if color.startswith('#'):
            color = color[1:]
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c * (1 + factor))) for c in rgb)
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

class HTMLMergeTool(QMainWindow):
    """HTML合并工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.selected_folder = None
        self.conversion_worker = None
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("HTML合并工具")
        self.setGeometry(100, 100, 950, 750)
        self.setMinimumSize(850, 650)
        
        # 设置窗口图标
        if os.path.exists('app_icon.ico'):
            self.setWindowIcon(QIcon('app_icon.ico'))
        
        # 设置现代化样式
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: white;
                font-size: 14px;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #495057;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #495057;
                font-size: 13px;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QLineEdit, QComboBox {
                padding: 12px 18px;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-size: 13px;
                background: white;
                min-height: 25px;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #667eea;
                background: #f8f9ff;
            }
            QTextEdit {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background: white;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                padding: 12px;
            }
            QProgressBar {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                text-align: center;
                background: #f8f9fa;
                font-weight: bold;
                min-height: 30px;
                font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 6px;
            }
        """)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #f1f3f4;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c1c1c1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a8a8a8;
            }
        """)
        
        # 主布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(35, 35, 35, 35)
        
        # 标题区域
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 15px;
                padding: 25px;
                margin: 15px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("HTML合并工具")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: white;
            margin: 10px 0;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("将HTML文件夹合并为单个文件")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 10px;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        """)
        title_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(title_frame)
        
        # 文件夹选择区域
        folder_group = QGroupBox("选择文件夹")
        folder_layout = QVBoxLayout(folder_group)
        
        # 拖拽区域
        self.drag_drop_widget = DragDropWidget()
        drag_label = QLabel("📁 拖拽文件夹到这里\n或点击下方按钮选择")
        drag_label.setAlignment(Qt.AlignCenter)
        drag_label.setStyleSheet("""
            font-size: 16px; 
            color: #667eea; 
            margin: 20px;
            font-weight: 600;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        """)
        self.drag_drop_widget.layout = QVBoxLayout(self.drag_drop_widget)
        self.drag_drop_widget.layout.addWidget(drag_label)
        
        # 选择按钮
        self.select_button = ModernButton("选择文件夹", "#667eea", size="large")
        self.select_button.clicked.connect(self.select_folder)
        self.drag_drop_widget.layout.addWidget(self.select_button)
        
        self.drag_drop_widget.file_dropped.connect(self.on_folder_dropped)
        folder_layout.addWidget(self.drag_drop_widget)
        
        # 选中的文件夹显示
        self.folder_label = QLabel("未选择文件夹")
        self.folder_label.setStyleSheet("""
            padding: 18px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e9ecef, stop:1 #dee2e6);
            border-radius: 8px;
            color: #6c757d;
            font-weight: 600;
            margin: 15px;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        """)
        folder_layout.addWidget(self.folder_label)
        
        main_layout.addWidget(folder_group)
        
        # 设置区域
        settings_group = QGroupBox("转换设置")
        settings_layout = QGridLayout(settings_group)
        settings_layout.setSpacing(20)
        
        # 输出格式
        settings_layout.addWidget(QLabel("输出格式:"), 0, 0)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["HTML (.html)", "MHTML (.mhtml)"])
        settings_layout.addWidget(self.format_combo, 0, 1)
        
        # 输出目录
        settings_layout.addWidget(QLabel("输出目录:"), 1, 0)
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("留空使用默认目录")
        settings_layout.addWidget(self.output_dir_edit, 1, 1)
        
        self.output_dir_button = ModernButton("浏览", "#17a2b8", size="small")
        self.output_dir_button.clicked.connect(self.select_output_dir)
        settings_layout.addWidget(self.output_dir_button, 1, 2)
        
        main_layout.addWidget(settings_group)
        
        # 操作按钮
        button_frame = QFrame()
        button_frame.setStyleSheet("QFrame { background: transparent; }")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(25)
        
        self.convert_button = ModernButton("🚀 开始转换", "#28a745", size="large")
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setEnabled(False)
        
        self.batch_button = ModernButton("📦 批量转换", "#17a2b8", size="large")
        self.batch_button.clicked.connect(self.start_batch_conversion)
        self.batch_button.setEnabled(False)
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.batch_button)
        button_layout.addStretch()
        
        main_layout.addWidget(button_frame)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # 日志区域
        log_group = QGroupBox("转换日志")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(220)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        # 设置滚动区域
        scroll_area.setWidget(main_widget)
        self.setCentralWidget(scroll_area)
        
    def select_folder(self):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(self, "选择包含HTML文件的文件夹")
        if folder:
            self.set_selected_folder(folder)
            
    def select_output_dir(self):
        """选择输出目录"""
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_dir_edit.setText(folder)
            
    def on_folder_dropped(self, folder_path):
        """处理文件夹拖拽"""
        self.set_selected_folder(folder_path)
        
    def set_selected_folder(self, folder_path):
        """设置选中的文件夹"""
        self.selected_folder = folder_path
        self.folder_label.setText(f"✅ 已选择: {os.path.basename(folder_path)}")
        self.folder_label.setStyleSheet("""
            padding: 18px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #d4edda, stop:1 #c3e6cb);
            border-radius: 8px;
            color: #155724;
            font-weight: 600;
            margin: 15px;
            font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        """)
        self.convert_button.setEnabled(True)
        self.batch_button.setEnabled(True)
        self.log_message(f"已选择文件夹: {folder_path}")
        
    def start_conversion(self):
        """开始转换"""
        if not self.selected_folder:
            QMessageBox.warning(self, "警告", "请先选择文件夹")
            return
            
        self.start_conversion_worker(False)
        
    def start_batch_conversion(self):
        """开始批量转换"""
        if not self.selected_folder:
            QMessageBox.warning(self, "警告", "请先选择文件夹")
        return
            
        self.start_conversion_worker(True)
        
    def start_conversion_worker(self, is_batch):
        """启动转换工作线程"""
        output_format = 'html' if self.format_combo.currentText().startswith('HTML') else 'mhtml'
        output_dir = self.output_dir_edit.text() if self.output_dir_edit.text() else None
        
        self.conversion_worker = ConversionWorker(
            self.selected_folder, output_format, output_dir, is_batch
        )
        self.conversion_worker.progress_updated.connect(self.update_progress)
        self.conversion_worker.conversion_finished.connect(self.conversion_finished)
        
        # 禁用按钮
        self.convert_button.setEnabled(False)
        self.batch_button.setEnabled(False)
        self.select_button.setEnabled(False)
        
        # 显示进度条
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 记录日志
        operation = "批量转换" if is_batch else "转换"
        self.log_message(f"开始{operation}...")
        
        # 启动线程
        self.conversion_worker.start()
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        
    def conversion_finished(self, success, title, message):
        """转换完成处理"""
        # 恢复按钮状态
        self.convert_button.setEnabled(True)
        self.batch_button.setEnabled(True)
        self.select_button.setEnabled(True)
        
        # 隐藏进度条
        self.progress_bar.setVisible(False)
        
        # 记录日志
        if success:
            self.log_message(f"✅ {title}: {message}")
            QMessageBox.information(self, "成功", f"{title}\n{message}")
        else:
            self.log_message(f"❌ {title}: {message}")
            QMessageBox.critical(self, "错误", f"{title}\n{message}")
            
    def log_message(self, message):
        """添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.ensureCursorVisible()
        
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 根据窗口大小调整字体
        width = self.width()
        if width < 900:
            font_size = "12px"
        elif width < 1200:
            font_size = "13px"
        else:
            font_size = "14px"
        
        # 更新样式
        self.setStyleSheet(self.styleSheet().replace(
            "font-size: 13px;", f"font-size: {font_size};"
        ))

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("HTML合并工具")
    app.setApplicationVersion("1.0.0")
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    # 创建并显示主窗口
    window = HTMLMergeTool()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()