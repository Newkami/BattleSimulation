import logging



import logging
import unittest
import colorlog
from config import LOG_PATH
from colorlog.escape_codes import escape_codes

# 创建colorlog格式化器
class CustomFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        message = super().format(record)
        message = colorlog.escape_codes.strip_ansi(message)  # 移除ANSI转义序列
        return message

# 创建日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建日志处理器并设置日志级别
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_PATH+'/log_file.log')
file_handler.setLevel(logging.INFO)
# 创建日志格式化器
formatter_file = colorlog.ColoredFormatter(
    "%(asctime)s:%(levelname)s:%(name)s:%(message)s",

)

formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
# 将格式化器应用于处理器
console_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(console_handler)

# 将格式化器应用于处理器
file_handler.setFormatter(formatter_file)

# 将处理器添加到日志记录器
logger.addHandler(file_handler)
class TestLogging(unittest.TestCase):
    def test_log(self):
        a = 1
        logger.debug(f"这是一条{a}调试级别的日志消息")
        logger.info("这是一条信息级别的日志消息")
        logger.warning("这是一条警告级别的日志消息")
        logger.error("这是一条错误级别的日志消息")
        logger.critical("这是一条严重级别的日志消息")
        # 关闭文件处理器并刷新
        file_handler.close()
        file_handler.flush()