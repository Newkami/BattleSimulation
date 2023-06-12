import math
import matplotlib

matplotlib.rc("font", family=' SimHei')
import matplotlib.pyplot as plt
import numpy as np


def distance_between_objects_in_2d(obj1, obj2):
    # SECTION:如果为元组之间的距离计算
    if isinstance(obj1, tuple) and isinstance(obj2, tuple):
        return math.sqrt((obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2)

    return math.sqrt((obj1.x_cord - obj2.x_cord) ** 2 + (obj1.y_cord - obj2.y_cord) ** 2)


def IsInMap(x, y, mapX, mapY):
    return x >= 0 and x <= mapX and y >= 0 and y <= mapY


def get_rangeBySpiralMatrix(x, y, mapX, mapY, n_circle):
    # SECTION:通过螺旋矩阵方式获得以x y为中心的方阵 n_circle为圈数
    square_cords = []

    for offset in range(1, n_circle + 1):
        start_x, start_y = x - offset, y - offset
        for i in range(1, 2 * offset + 1, 1):
            if IsInMap(start_x, start_y, mapX, mapY):
                square_cords.append((start_x, start_y))
            start_y += 1

        for i in range(1, 2 * offset + 1, 1):
            if IsInMap(start_x, start_y, mapX, mapY):
                square_cords.append((start_x, start_y))
            start_x += 1

        for i in range(1, 2 * offset + 1, 1):
            if IsInMap(start_x, start_y, mapX, mapY):
                square_cords.append((start_x, start_y))
            start_y -= 1

        for i in range(1, 2 * offset + 1, 1):
            if IsInMap(start_x, start_y, mapX, mapY):
                square_cords.append((start_x, start_y))
            start_x -= 1

    return square_cords


def get_MatrixWithNoObjs(x, y, map, n_circle=1) -> list:
    """
        :param x:
        :param y:
        :param mapX:
        :param mapY:
        :return: 获得以x y为中心的方阵n圈方阵，并且排除了多余的已存在的目标和(x,y)本身
    """

    cords = get_rangeBySpiralMatrix(x, y, map.shape[0], map.shape[1], n_circle)
    result = []
    for option in cords:
        if map[option[0]][option[1]] == 0:
            result.append(option)
    return result


def getEightPointswithNoobs(x, y, map) -> list:
    """
    (x-1,y+1) (x,y+1) (x+1,y+1)
    (x-1,y) (x,y) (x+1,y)
    (x-1,y-1) (x,y-1) (x+1,y-1)
    """
    avail_options = [(x - 1, y + 1),
                     (x, y + 1),
                     (x + 1, y + 1),
                     (x - 1, y),
                     (x + 1, y),
                     (x - 1, y - 1),
                     (x, y - 1),
                     (x + 1, y - 1)
                     ]
    result = []
    for option in avail_options:
        if IsInMap(option[0], option[1], map.shape[0], map.shape[1]) \
                and map[option[0]][option[1]] == 0:
            result.append(option)
    return result


def visualizeMapIn2d(map):
    # bplt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    marker_styles = {1: 's', 2: 'o', 3: '^', 4: 'D', 5: '*', 6: '.'}
    color_styles = {1: 'blue', 2: 'green', 3: 'aquamarine', 4: 'yellow', 5: 'red', 6: 'darkviolet'}
    # 获取矩阵的行数和列数
    rows, cols = map.shape
    # 创建一个空的图形对象
    fig, ax = plt.subplots()
    # 遍历矩阵，绘制散点图
    for i in range(rows):
        for j in range(cols):
            if map[i, j] != 0:
                # 绘制非零元素的散点图
                ax.scatter(j + 0.5, i + 0.5, marker=marker_styles[map[i, j]], c=color_styles[map[i, j]],
                           s=100)

    # 设置坐标轴范围和刻度
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks(np.arange(cols, step=5))
    ax.set_yticks(np.arange(rows, step=5))
    ax.set_title(u"战场分布图")
    ax.set_xlabel('Y Coordinate')
    ax.set_ylabel('X Coordinate')
    # 隐藏坐标轴刻度线
    ax.tick_params(axis='both', which='both', length=0)

    # 显示网格线
    # ax.grid(linewidth=1, color='gray', linestyle='--')
    # 显示图形
    plt.show()


def find_integer_points_in_circle(x, y, mapX, mapY, r):
    """
    :param x:  x_cord
    :param y:  y_cord
    :param r:  radius
    :return:   满足在半径为r内的所有整数点集合
    """
    points = []
    for i in range(x - r, x + r + 1):
        for j in range(y - r, y + r + 1):
            if math.sqrt((i - x) ** 2 + (j - y) ** 2) <= r and IsInMap(i, j, mapX, mapY):
                points.append((i, j))
    return points
