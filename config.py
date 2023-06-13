import os

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, 'data')

TASK_CONFIG = {
    "total_num": 9,  # 保证下面的设置数量要和total_num相等
    "jammers": {
        "easy": 1,
        "medium": 0,
        "hard": 1
    },
    "missile_vehicles": {
        "easy": 1,
        "medium": 0,
        "hard": 1
    },
    "radars": {
        "easy": 1,
        "medium": 1,
        "hard": 1
    },
    "antiairturrents": {
        "easy": 1,
        "medium": 0,
        "hard": 1
    }
}