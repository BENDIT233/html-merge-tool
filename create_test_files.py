import os

def create_test_files():
    # 创建测试文件结构
    test_dir = 'test_files'
    test_folder = os.path.join(test_dir, 'test_folder')
    sub_folder = os.path.join(test_folder, 'sub_folder')
    
    # 创建目录
    os.makedirs(sub_folder, exist_ok=True)
    
    # 创建示例HTML文件
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>测试页面</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>测试页面</h1>
    <img src="image.png" alt="测试图片">
    <script src="script.js"></script>
</body>
</html>'''
    
    with open(os.path.join(test_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # 创建示例CSS文件
    css_content = '''body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
}

h1 {
    color: #333;
}'''
    
    with open(os.path.join(test_folder, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # 创建示例JS文件
    js_content = '''console.log('测试JavaScript文件');

function testFunction() {
    alert('Hello, World!');
}'''
    
    with open(os.path.join(test_folder, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # 创建示例图片文件（创建一个简单的文本表示）
    with open(os.path.join(test_folder, 'image.png'), 'w') as f:
        f.write('This is a placeholder for an image file.')
    
    print(f"测试文件已创建在 {test_dir} 目录中")

if __name__ == '__main__':
    create_test_files()