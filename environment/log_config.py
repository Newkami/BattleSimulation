from config import ROOT_PATH
import os
import logging
import re
import colorlog

LOG_PATH = os.path.join(ROOT_PATH, 'logs')

cmd_formatter = colorlog.ColoredFormatter(  # 控制台输出的默认formatter
    "%(log_color)s%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    log_colors={
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)


class FileOutputFormatter(logging.Formatter):  # 文件输出的默认formatter
    def __init__(self):
        super.__init__()
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def format(self, record):
        message = super().format(record)
        return self.ansi_escape.sub('', message)


class BattleLogger:
    def __init__(self, name, file, level = logging.DEBUG):
        self.fileformatter = FileOutputFormatter()
        self.cmd_formatter = cmd_formatter
        self.loglevel = level
        self.logger = logging.getLogger(name)
        self.file_hander = logging.FileHandler(LOG_PATH+'/{}'.format(file))
        self.file_hander.setLevel(self.loglevel)
        # 创建日志处理器并设置日志级别
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(self.loglevel)
    
