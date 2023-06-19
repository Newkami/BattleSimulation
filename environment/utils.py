import math
import os

import matplotlib

matplotlib.rc("font", family=' SimHei')
import matplotlib.pyplot as plt
import numpy as np
from config import DATA_PATH


def distance_between_objects_in_2d(obj1, obj2):
    # SECTION:如果为元组之间的距离计算
    if isinstance(obj1, tuple) and isinstance(obj2, tuple):
        return math.sqrt((obj1[0] - obj2[0]) ** 2 + (obj1[1] - obj2[1]) ** 2)

    return math.sqrt((obj1.x_cord - obj2.x_cord) ** 2 + (obj1.y_cord - obj2.y_cord) ** 2)


def IsInMap(x, y, mapX, mapY):
    return x >= 0 and x < mapX and y >= 0 and y < mapY


def get_rangeBySpiralMatrix(x, y, n_circle, need_center=False):
    # SECTION:通过螺旋矩阵方式获得以x y为中心的方阵 n_circle为圈数
    square_cords = []
    if n_circle == 0:
        return square_cords
    for offset in range(1, n_circle + 1):
        start_x, start_y = x - offset, y - offset
        for i in range(1, 2 * offset + 1, 1):
            square_cords.append((start_x, start_y))
            start_y += 1

        for i in range(1, 2 * offset + 1, 1):
            square_cords.append((start_x, start_y))
            start_x += 1

        for i in range(1, 2 * offset + 1, 1):
            square_cords.append((start_x, start_y))
            start_y -= 1

        for i in range(1, 2 * offset + 1, 1):
            square_cords.append((start_x, start_y))
            start_x -= 1

    if need_center:  # 如果不需要中心点
        square_cords.append((x, y))

    return square_cords


def get_MatrixWithNoObjs(x, y, map, n_circle=1) -> list:
    """
        :param x:
        :param y:
        :param mapX:
        :param mapY:
        :return: 获得以x y为中心的方阵n圈方阵，并且排除了多余的已存在的目标和(x,y)本身
    """

    cords = get_rangeBySpiralMatrix(x, y, n_circle)
    result = []
    for option in cords:
        if IsInMap(option[0], option[1], map.shape[0], map.shape[1]) and map[option[0]][option[1]] == 0:
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


def visualizeMapIn2d(map, first=False):  # 旧版画图函数 已被弃用
    # bplt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    marker_styles = {1: 's', 2: 'o', 3: '^', 4: 'D', 5: '*', 6: '.'}
    color_styles = {1: 'blue', 2: 'green', 3: 'aquamarine', 4: 'yellow', 5: 'red', 6: 'darkviolet'}
    # 获取矩阵的行数和列数
    rows, cols = map.shape
    # 创建一个空的图形对象
    fig, ax = plt.subplots()

    # 遍历矩阵，绘制散点图
    map_points_x, map_points_y = plot_aux(map, len(marker_styles))

    ax.clear()
    scatters = []
    for i in range(1, len(marker_styles) + 1):
        map_points_x[i] = (np.array(map_points_x[i]) + 0.5).tolist()
        map_points_y[i] = (np.array(map_points_y[i]) + 0.5).tolist()
        scatters.append(
            ax.scatter(map_points_x[i], map_points_y[i], marker=marker_styles[i], c=color_styles[i], s=50))
    labels = ['干扰机', '导弹车', '雷达', '防空炮', '指挥所', '无人机']
    ax.legend(scatters, labels, loc="lower right")
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
    # plt_path = os.path.join(DATA_PATH, 'tmp')
    # plt.savefig(plt_path + '/plt.png', format="png")
    plt.show()
    plt.close()


def visualizeMap(map, fig, ax, step):
    # bplt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
    markers = ['s', 'o', '^', 'D', '*', '.']
    colors = ['blue', 'green', 'aquamarine', 'yellow', 'red', 'darkviolet']
    # 获取矩阵的行数和列数
    rows, cols = map.shape
    # 创建一个空的图形对象
    # 遍历矩阵，绘制散点图
    ax.cla()
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            value = int(map[i, j])
            if value != 0:
                marker = markers[value-1]
                color = colors[value-1]
                ax.scatter(i+0.5, j+0.5, marker=marker, color=color, s=50)
    legend_elements = [plt.Line2D([0], [0], marker=marker, color='w', markerfacecolor=color, markersize=10)
                       for marker, color in zip(markers, colors)]
    legend_labels = ['干扰机', '导弹车', '雷达', '防空炮', '指挥所', '无人机']
    ax.legend(legend_elements, legend_labels, title='Legend', loc="upper left")
    # 设置坐标轴范围和刻度
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks(np.arange(cols, step=5))
    ax.set_yticks(np.arange(rows, step=5))
    ax.set_title(u"战场分布图_step{}".format(step))
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    # 隐藏坐标轴刻度线
    ax.tick_params(axis='both', which='both', length=0)
    plt.pause(0.1)
    # 显示网格线
    # ax.grid(linewidth=1, color='gray', linestyle='--')


def plot_aux(map, length):
    rows, cols = map.shape
    map_points_x = {}
    map_points_y = {}
    for i in range(length):
        map_points_x[i + 1] = []
        map_points_y[i + 1] = []
    for i in range(rows):
        for j in range(cols):
            if map[i, j] == 1:
                map_points_x[1].append(i)
                map_points_y[1].append(j)
            elif map[i, j] == 2:
                map_points_x[2].append(i)
                map_points_y[2].append(j)
            elif map[i, j] == 3:
                map_points_x[3].append(i)
                map_points_y[3].append(j)
            elif map[i, j] == 4:
                map_points_x[4].append(i)
                map_points_y[4].append(j)
            elif map[i, j] == 5:
                map_points_x[5].append(i)
                map_points_y[5].append(j)
            elif map[i, j] == 6:
                map_points_x[6].append(i)
                map_points_y[6].append(j)
    return map_points_x, map_points_y


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


def get_size_by_n(sight_range):
    if sight_range == 0:
        return 0
    return get_size_by_n(sight_range - 1) + 8 * sight_range
