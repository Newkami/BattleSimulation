import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, 'data')
LOG_PATH = os.path.join(ROOT_PATH, 'logs')

TASK_CONFIG = {
    "total_num": 11,  # 保证下面的设置数量要和total_num相等 不然会发生aseert错误
    "jammers": {
        "easy": 2,
        "medium": 1,
        "hard": 0
    },
    "missile_vehicles": {
        "easy": 1,
        "medium": 1,
        "hard": 0
    },
    "radars": {
        "easy": 1,
        "medium": 1,
        "hard": 1
    },
    "antiairturrents": {
        "easy": 1,
        "medium": 1,
        "hard": 1
    },
    "init_commandpost_x": 40,
    "init_commandpost_y": 40
}
