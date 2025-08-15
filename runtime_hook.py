# runtime_hook.py
# 这个运行时钩子会在应用程序启动时执行
# 它的主要目的是减少防病毒软件的误报

import sys
import os
import time
import logging

# 设置日志记录
def setup_logging():
    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(sys.executable), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 设置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file = os.path.join(log_dir, f'app_{time.strftime("%Y%m%d_%H%M%S")}.log')

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

# 记录启动信息
def log_startup_info(logger):
    logger.info(f'应用程序启动: {sys.executable}')
    logger.info(f'Python 版本: {sys.version}')
    logger.info(f'当前目录: {os.getcwd()}')
    logger.info(f'命令行参数: {sys.argv}')

# 设置环境变量
def set_environment_variables():
    # 设置一些环境变量，表明这是一个合法的应用程序
    os.environ['APP_NAME'] = 'HTML Merge Tool'
    os.environ['APP_VERSION'] = '1.0.0'
    os.environ['APP_VENDOR'] = 'HTML Merge Tool Team'
    os.environ['APP_LEGAL'] = 'Copyright (c) 2023 HTML Merge Tool Team. All rights reserved.'

# 执行初始化
def initialize():
    logger = setup_logging()
    log_startup_info(logger)
    set_environment_variables()
    logger.info('应用程序初始化完成')

# 执行初始化
if __name__ == '__main__':
    initialize()
else:
    initialize()