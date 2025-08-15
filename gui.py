import sys
import os
import warnings
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, QMessageBox, 
                             QGroupBox, QComboBox, QProgressBar, QFrame, QStyle)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent, QColor
from html_converter import batch_convert

# 忽略DeprecationWarning警告
warnings.filterwarnings("ignore", category=DeprecationWarning)

class ConvertThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, input_path, output_format, output_dir, parent=None):
        super().__init__(parent)
        self.input_path = input_path
        self.output_format = output_format
        self.output_dir = output_dir
    
    def run(self):
        try:
            batch_convert(self.input_path, self.output_format, self.output_dir, self.report_progress)
            self.finished.emit(True, "转换完成！")
        except Exception as e:
            self.finished.emit(False, f"转换失败: {str(e)}")
    
    def report_progress(self, value):
        self.progress.emit(value)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口样式 - WPF + Fluent Design精简版
        self.setWindowTitle('HTML合并工具')
        self.setGeometry(100, 100, 700, 450)
        self.setStyleSheet('''
            QMainWindow { 
                background-color: #f8f9fa; 
                border-radius: 8px; 
                margin: 10px; 
            }
            QWidget { 
                background-color: transparent; 
            }
            QGroupBox { 
                border: 1px solid #e9ecef; 
                border-radius: 8px; 
                margin-top: 10px; 
                padding: 10px; 
                background-color: white; 
            }
            QGroupBox::title { 
                subcontrol-origin: margin; 
                left: 10px; 
                padding: 0 3px 0 3px; 
                color: #343a40; 
                font-weight: 600; 
            }
            QLabel { 
                color: #495057; 
                font-size: 14px; 
            }
            QLineEdit { 
                border: 1px solid #ced4da; 
                border-radius: 12px; 
                padding: 8px 12px; 
                background-color: white; 
                font-size: 14px; 
                min-height: 40px; 
                min-width: 400px; 
                transition: border-color 0.3s, box-shadow 0.3s; 
            }
            QLineEdit:focus { 
                border-color: #4dabf7; 
                box-shadow: 0 0 0 2px rgba(77, 171, 247, 0.25); 
                outline: none; 
            }
            QPushButton { 
                background-color: #4dabf7; 
                color: white; 
                border-radius: 8px; 
                border: none; 
                padding: 6px 12px; 
                font-size: 14px; 
                transition: background-color 0.3s; 
            }
            QPushButton:hover { 
                background-color: #339af0; 
            }
            QPushButton:pressed { 
                background-color: #228be6; 
            }
            QComboBox { 
                border: 1px solid #ced4da; 
                border-radius: 8px; 
                padding: 6px 30px 6px 12px; 
                background-color: white; 
                font-size: 14px; 
                appearance: none; 
            }
            QProgressBar { 
                border: 1px solid #e9ecef; 
                border-radius: 10px; 
                background-color: #f8f9fa; 
                height: 10px; 
                text-align: center; 
            }
            QProgressBar::chunk { 
                background-color: #4dabf7; 
                border-radius: 8px; 
                animation: progress 2s infinite linear; 
            }
            @keyframes progress { 
                0% { 
                    background-color: #4dabf7; 
                } 
                50% { 
                    background-color: #74c0fc; 
                } 
                100% { 
                    background-color: #4dabf7; 
                } 
            }
        ''')

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 输入设置
        input_group = QGroupBox("输入设置")
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(15, 15, 15, 15)
        input_layout.setSpacing(10)

        # 拖入框
        drag_drop_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("点击或拖拽文件夹到此处")
        self.path_input.setReadOnly(False)
        self.browse_btn = QPushButton("浏览")
        self.browse_btn.clicked.connect(self.browse_folder)
        drag_drop_layout.addWidget(self.path_input, 1)
        drag_drop_layout.addWidget(self.browse_btn)
        input_layout.addLayout(drag_drop_layout)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # 输出设置
        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(15, 15, 15, 15)
        output_layout.setSpacing(10)

        # 输出格式
        format_layout = QHBoxLayout()
        format_layout.setSpacing(10)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["html", "mhtml"])
        format_layout.addWidget(QLabel("输出格式:"), 0, Qt.AlignRight)
        format_layout.addWidget(self.format_combo)
        format_layout.addStretch(1)
        output_layout.addLayout(format_layout)

        # 输出目录
        output_dir_layout = QHBoxLayout()
        output_dir_layout.setSpacing(10)
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("输出文件保存位置")
        self.browse_output_btn = QPushButton("选择目录")
        self.browse_output_btn.clicked.connect(self.browse_output_dir)
        output_dir_layout.addWidget(QLabel("输出目录:"), 0, Qt.AlignRight)
        output_dir_layout.addWidget(self.output_dir_input, 1)
        output_dir_layout.addWidget(self.browse_output_btn)
        output_layout.addLayout(output_dir_layout)

        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 转换按钮
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setStyleSheet("font-size: 14px; padding: 9px 18px; font-weight: 600;")
        self.convert_btn.clicked.connect(self.start_conversion)
        main_layout.addWidget(self.convert_btn, alignment=Qt.AlignCenter)

        # 设置拖拽支持
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            # 拖拽进入时改变边框颜色
            self.path_input.setStyleSheet("border-color: #4dabf7; box-shadow: 0 0 0 2px rgba(77, 171, 247, 0.25); border-radius: 12px; padding: 8px 12px; background-color: white; font-size: 14px; min-height: 40px; min-width: 400px;")
            
    def dragLeaveEvent(self, event):
        # 拖拽离开时恢复边框颜色
        self.path_input.setStyleSheet("border-color: #ced4da; border-radius: 12px; padding: 8px 12px; background-color: white; font-size: 14px; min-height: 40px; min-width: 400px;")
            
    def dropEvent(self, event: QDropEvent):
        # 拖放完成后恢复边框颜色
        self.path_input.setStyleSheet("border-color: #ced4da; border-radius: 12px; padding: 8px 12px; background-color: white; font-size: 14px; min-height: 40px; min-width: 400px;")
        
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            path = url.toLocalFile()
            if os.path.isdir(path):
                self.path_input.setText(path)
            else:
                QMessageBox.warning(self, "无效路径", "请选择一个文件夹")
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            self.path_input.setText(folder)
            # 默认将输出目录设置为输入目录的父目录
            parent_dir = os.path.dirname(folder)
            if parent_dir:
                self.output_dir_input.setText(parent_dir)
        
    def browse_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_dir_input.setText(folder)
        
    def start_conversion(self):
        input_path = self.path_input.text().strip()
        if not input_path or not os.path.isdir(input_path):
            QMessageBox.warning(self, "无效路径", "请选择一个有效的文件夹")
            return
            
        output_format = self.format_combo.currentText()
        output_dir = self.output_dir_input.text().strip()
        
        # 检查输出目录是否有效
        if output_dir and not os.path.isdir(output_dir):
            QMessageBox.warning(self, "无效路径", "请选择一个有效的输出目录")
            return
            
        # 禁用按钮并显示进度条
        self.convert_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # 启动转换线程
        self.thread = ConvertThread(input_path, output_format, output_dir)
        self.thread.progress.connect(self.progress_bar.setValue)
        self.thread.finished.connect(self.on_conversion_finished)
        self.thread.start()
        
    def on_conversion_finished(self, success, message):
        # 恢复按钮并隐藏进度条
        self.convert_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "成功", message)
        else:
            QMessageBox.critical(self, "错误", message)

def main():
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        # 设置标准输出编码为utf-8，以支持中文
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        print("HTML合并工具")
        print("使用方法:")
        print("  gui.exe           # 启动图形界面")
        print("  gui.exe --help    # 显示此帮助信息")
        return 0
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())