import math
import os
import random

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
            ax.scatter(map_points_x[i], map_points_y[i], marker=marker_styles[i], c=color_styles[i], s=30))
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
                marker = markers[value - 1]
                color = colors[value - 1]
                ax.scatter(i + 0.5, j + 0.5, marker=marker, color=color, s=50)
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


def get_points_in_quadrants(origin, n_range):
    points = []

    # 第二象限
    for x in range(-n_range, -5):
        for y in range(-n_range, -5):
            points.append((origin[0] + x, origin[1] + y))

    # 第三象限
    for x in range(-n_range, -5):
        for y in range(5, n_range + 1):
            points.append((origin[0] + x, origin[1] - y))

    # 第四象限
    for x in range(5, n_range + 1):
        for y in range(5, n_range + 1):
            points.append((origin[0] + x, origin[1] - y))

    return points


def get_quadrantsPointwithNoObjs(x, y, map, n_circle=1) -> list:
    """
        :param x:
        :param y:
        :param mapX:
        :param mapY:
        :return: 获得以x y为中心的方阵n圈方阵，并且排除了多余的已存在的目标和(x,y)本身
    """

    cords = get_points_in_quadrants((x, y), n_circle)
    result = []
    for option in cords:
        if IsInMap(option[0], option[1], map.shape[0], map.shape[1]) and map[option[0]][option[1]] == 0:
            result.append(option)
    return result


def polar2XY(command, r, theta):
    """
    极坐标系转化为平面直角坐标系
    输入:
        command: 指挥所中心坐标[x,y]
        r: 半径
        theta: 角度
    输出:
        [x,y]: 平面直角坐标系

    """
    theta = theta * (np.pi / 180)
    x = command[0] + r * np.cos(theta)
    y = command[1] + r * np.sin(theta)
    return (int(x), int(y))


def generate_layer_node(node_num, layer_num):
    """
    生成求和数量为固定值,固定层数的节点列表
    输入:
        node_num: 节点总数
        layer_num: 防御层数
    输出:
        defense_layer_node: 每一层的节点数量
    """
    # 为了保证每一层都有防御节点,首先将每一层的节点数量初始化为1
    defense_layer_node = [1 for _ in range(layer_num)]
    # 计算初始化分配完成之后所剩下的节点总数
    remain_node = node_num - sum(defense_layer_node)
    # 计算均匀分配情况下,每一层可以得到多少的节点
    average_node = int(remain_node / layer_num)
    for i in range(layer_num - 1):
        # 计算当前层被分配的节点数量
        distrib = random.randint(average_node - 1, average_node)
        # 将节点数量添加其中
        defense_layer_node[i] += distrib
        # 计算剩余的节点数量
        remain_node -= distrib
    defense_layer_node[-1] += remain_node

    return defense_layer_node


def get_defend_pos_list(command, n, actual_num, mapX, mapY):
    """   第1步,参数配置   """
    # 防御层数
    defense_layer = 2
    # 层间的距离
    layer2layer_radius_min = 5
    layer2layer_radius_max = 6

    """   第2步,生成节点位置[X,Y]   """
    # 每一层的防御点数量
    defense_layer_node = generate_layer_node(n, defense_layer)
    # print(defense_layer_node)
    # 记录每一层所在的半径
    defense_layer_radius = []
    for i in range(defense_layer):
        # 层间的间隔不同
        layer2layer_radius = random.randint(layer2layer_radius_min, layer2layer_radius_max)
        if i == 0:
            defense_layer_radius.append(layer2layer_radius)
        else:
            radius = defense_layer_radius[-1] + layer2layer_radius
            defense_layer_radius.append(radius)

    # 防御点均匀分布,但是初始的角度不同
    defense_layer_theta = []
    for i in range(defense_layer):
        init_theta = random.randint(0, 90)
        defense_layer_theta.append(init_theta)

    defense_list = []
    # 遍历每一层
    for i in range(defense_layer):
        # 随机生成半径
        init_r = defense_layer_radius[i]
        # 初始的角度
        init_theta = defense_layer_theta[i]
        # 遍历每一层的作战对象
        for j in range(defense_layer_node[i]):
            """   生成防御点角度值   """
            # 生成单位角度
            unit_angle = int(360 / defense_layer_node[i])
            # 角度扰动
            float_angle = random.randint(-10, 10)
            # 生成角度
            theta = init_theta + j * unit_angle + float_angle
            """   生成防御点半径   """
            # 半径扰动
            float_radius = random.randint(-1, 1)
            # 生成半径
            r = init_r + float_radius
            # 生成防御点
            defense_pos = polar2XY(command, r, theta)
            defense_list.append(defense_pos)
    real_defend_list = []
    for i, point in enumerate(defense_list):
        if IsInMap(point[0], point[1], mapX, mapY):
            real_defend_list.append(point)
    # defense_list = np.array(defense_list)

    assert len(real_defend_list)>= actual_num, "合法的采样点数目小于实际需要的点个数"
    # plt.plot(defense_list[:, 0], defense_list[:, 1], "b*", label="防御点")
    # plt.plot(command[0], command[1], "r^", label="指挥所")
    # plt.xlim(0, 50)
    # plt.ylim(0, 50)
    # plt.legend()
    # plt.show()
    return random.sample(real_defend_list, actual_num)
