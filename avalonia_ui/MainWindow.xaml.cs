using Avalonia;
using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Markup.Xaml;
using System.IO;

namespace HtmlMergeTool.AvaloniaUI
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            // 注册拖拽事件
            var dropArea = this.Find<Border>("dropArea");
            if (dropArea != null)
            {
                dropArea.DragEnter += DropArea_DragEnter;
                dropArea.DragLeave += DropArea_DragLeave;
                dropArea.Drop += DropArea_Drop;
            }
        }

        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }

        private void DropArea_DragEnter(object sender, DragEventArgs e)
        {
            e.DragEffects = DragDropEffects.Copy;
            var dropArea = sender as Border;
            if (dropArea != null)
            {
                dropArea.Background = Avalonia.Media.Brushes.LightBlue;
            }
        }

        private void DropArea_DragLeave(object sender, DragEventArgs e)
        {
            var dropArea = sender as Border;
            if (dropArea != null)
            {
                dropArea.Background = Avalonia.Media.Brushes.Parse("#f8f9fa");
            }
        }

        private void DropArea_Drop(object sender, DragEventArgs e)
        {
            var dropArea = sender as Border;
            if (dropArea != null)
            {
                dropArea.Background = Avalonia.Media.Brushes.Parse("#f8f9fa");
            }

            if (e.Data.Contains(DataFormats.FileNames))
            {
                var files = e.Data.GetFileNames();
                if (files != null && files.Count > 0)
                {
                    var path = files[0];
                    if (Directory.Exists(path))
                    {
                        var inputBox = this.Find<TextBox>("inputPath");
                        if (inputBox != null)
                        {
                            inputBox.Text = path;
                            // 默认输出目录为输入目录
                            var outputBox = this.Find<TextBox>("outputPath");
                            if (outputBox != null)
                            {
                                outputBox.Text = path;
                            }
                        }
                    }
                }
            }
        }
    }
}