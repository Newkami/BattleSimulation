import logging
import re

# 用于删除ANSI转义序列的正则表达式
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('log_file.log')
handler.setLevel(logging.INFO)
# 自定义格式化器，可以在这里删除控制序列
class NoAnsiFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        return ansi_escape.sub('', message)

handler.setFormatter(NoAnsiFormatter())
logger.addHandler(handler)

# 现在使用logger记录日志，将不会包含控制序列
logger.info("\x1B[31mHello, World!\x1B[0m")