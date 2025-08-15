// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 初始化Eel
    eel.init('web')

    // 获取DOM元素
    const uploadArea = document.getElementById('upload-area');
    const folderPathInput = document.getElementById('folder-path');
    const browseBtn = document.getElementById('browse-btn');
    const outputFormatSelect = document.getElementById('output-format');
    const outputDirInput = document.getElementById('output-dir');
    const browseOutputBtn = document.getElementById('browse-output-btn');
    const progressContainer = document.querySelector('.progress-container');
    const progressBar = document.getElementById('progress-bar');
    const convertBtn = document.getElementById('convert-btn');
    const notification = document.getElementById('notification');

    // 浏览文件夹
    browseBtn.addEventListener('click', async function() {
        const path = await eel.browse_folder()();
        if (path) {
            folderPathInput.value = path;
            outputDirInput.value = path; // 默认输出目录为输入目录
        }
    });

    // 浏览输出目录
    browseOutputBtn.addEventListener('click', async function() {
        const path = await eel.browse_output_dir()();
        if (path) {
            outputDirInput.value = path;
        }
    });

    // 拖拽功能
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = '#0d6efd';
        this.style.backgroundColor = '#eef5ff';
    });

    uploadArea.addEventListener('dragleave', function() {
        this.style.borderColor = '#adb5bd';
        this.style.backgroundColor = 'transparent';
    });

    uploadArea.addEventListener('drop', async function(e) {
        e.preventDefault();
        this.style.borderColor = '#adb5bd';
        this.style.backgroundColor = 'transparent';

        if (e.dataTransfer.files.length) {
            const file = e.dataTransfer.files[0];
            if (file.type.includes('folder') || file.webkitRelativePath) {
                // 处理拖拽的文件夹
                const path = await eel.handle_drop(file.path)();
                if (path) {
                    folderPathInput.value = path;
                    outputDirInput.value = path; // 默认输出目录为输入目录
                }
            } else {
                showNotification('请拖拽一个文件夹，而非文件。', 'error');
            }
        }
    });

    // 点击上传区域也触发浏览文件夹
    uploadArea.addEventListener('click', function() {
        browseBtn.click();
    });

    // 开始转换
    convertBtn.addEventListener('click', async function() {
        const inputPath = folderPathInput.value.trim();
        const outputFormat = outputFormatSelect.value;
        const outputDir = outputDirInput.value.trim();

        if (!inputPath) {
            showNotification('请选择一个有效的输入文件夹。', 'error');
            return;
        }

        if (!outputDir) {
            outputDir = inputPath;
            outputDirInput.value = outputDir;
        }

        // 禁用转换按钮
        convertBtn.disabled = true;
        // 显示进度条
        progressContainer.style.display = 'block';
        progressBar.style.width = '0%';

        // 开始转换
        await eel.start_conversion(inputPath, outputFormat, outputDir)();
    });

    // 显示通知
    function showNotification(message, type) {
        notification.textContent = message;
        notification.className = 'notification ' + type + ' show';

        setTimeout(function() {
            notification.className = 'notification';
        }, 5000);
    }

    // 监听进度更新
    eel.expose(update_progress);
    function update_progress(value) {
        progressBar.style.width = value + '%';
    }

    // 监听转换完成
    eel.expose(on_conversion_finished);
    function on_conversion_finished(success, message) {
        // 启用转换按钮
        convertBtn.disabled = false;
        // 隐藏进度条
        progressContainer.style.display = 'none';

        if (success) {
            showNotification(message, 'success');
        } else {
            showNotification(message, 'error');
        }
    }
});