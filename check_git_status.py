import subprocess
import os

def check_git_repo():
    try:
        # 检查当前目录是否是git仓库
        subprocess.run(['git', 'rev-parse', '--git-dir'], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_git_status():
    try:
        # 获取git状态
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def get_current_branch():
    try:
        # 获取当前分支
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def main():
    if not check_git_repo():
        print("当前目录不是git仓库")
        return
    
    branch = get_current_branch()
    status = get_git_status()
    
    print(f"当前分支: {branch}")
    if status:
        print("未提交的更改:")
        print(status)
    else:
        print("工作目录干净，没有未提交的更改")

if __name__ == '__main__':
    main()