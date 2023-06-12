import math
import random

from environment import utils
from bisect import bisect, bisect_left, bisect_right
import enum


class Enemy(enum.IntEnum):
    EMPTY = 0
    JAMMER = 1
    MISSILEVEHICLE = 2
    RADAR = 3
    ANTIAIRCRAFTTURRENT = 4
    COMMANDPOST = 5


class Jammer():
    """
    干扰机
    干扰机处于栅格地图中的某一点
    考虑是否加入以下因素：
        1.是否会在地图上位置产生变动
        2.生命值的表示并不符合实际状态
            2.1 考虑的改进建模设置：以损伤率代替生命值，在每回合后反制干扰机可在
                机场补给后进行损伤修复，修复其总耐久的20%或更多（），修复后下一回合考虑其
                出现的位置为原位置还是产生变动
            2.2 根据其损伤率低于一定大小不能起飞 继续在机场待命 若修复耐久度大于一定量可以考虑起飞
            2.3 干扰机是否也存在打击范围
    """

    def __init__(self, id, x_cord, y_cord, battle_id, args):
        # 定义相关属性
        self.args = args
        self.id = id  # id
        self.x_cord = x_cord  # x坐标
        self.y_cord = y_cord  # y坐标
        self.battle_id = battle_id  # 用于动作选择的battle_id
        self.mapX = args.mapX  # maxX
        self.mapY = args.mapY  # mapY
        self.jammer_strike_ability = args.jammer_strike_ability  # 打击能力
        self.maxHP = args.jm_maxHP  # 最大耐久度
        self.HP = args.jm_maxHP  # 当前耐久度
        self.repair_coef = args.repair_coef  # 恢复系数
        self.min_takeoff_hp = args.min_takeoff_hp  # 最小可起飞耐久度
        self.target_type = Enemy.JAMMER
        self.isAlive = True  # 存活状态
        self.isTakingoff = True  # 当前是否于起飞状态
        self.attack_range = args.attack_range

    def __str__(self):
        return '干扰机：{0} 所在位置：x:{1}  y:{2} 当前耐久值：{3} 索引id：{4}'.format(self.id, self.x_cord, self.y_cord,
                                                                                   self.HP, self.battle_id)

    def set_current_hp(self, val):
        self.HP = val

    @property
    def get_current_hp(self):
        return self.HP

    # 定义修复函数
    def jammer_repaired(self, x_last, y_last, map):
        if self.isAlive:
            tmp_HP = self.HP + self.repair_coef * self.maxHP  # 先加血量
            self.HP = tmp_HP if tmp_HP < self.HP else self.maxHP

            if self.isTakingoff:
                return
            if self.HP > self.min_takeoff_hp:
                # 后续需要加上检测位置是否超出地图界限 和地图上是否有其他东西
                # 如果达到起飞最小耐久，则随机选择飞机出现的位置
                avail_pos = utils.get_MatrixWithNoObjs(x_last, y_last, map, 2)
                intend_pos = random.sample(avail_pos, 1)[0]
                tmp_x = intend_pos[0]
                tmp_y = intend_pos[1]  # 根据上回合位置所在位置出现的一个上下浮动的随机值
                self.x_cord = tmp_x
                self.y_cord = tmp_y
                self.isTakingoff = True
            map[self.x_cord][self.y_cord] = Enemy.JAMMER

    # 受到无人机攻击
    def BeAttacked(self, damage, map):
        if self.isTakingoff and self.isAlive:  # 在起飞状态才可以被攻击
            self.set_current_hp(self.HP - damage)
            if self.HP <= 0:
                self.HP = 0
                self.isAlive = False
                self.isTakingoff = False
            elif self.HP < self.min_takeoff_hp and self.HP > 0:
                self.isTakingoff = False
            map[self.x_cord][self.y_cord] = Enemy.EMPTY
        return self.isAlive, self.target_type

    # 定义反制函数
    def counter_strike(self, map, multirotors):
        # 既存活又处于起飞状态才可反制
        if self.isTakingoff and self.isAlive:
            tmp_uavs = [uav for uav in multirotors if
                        utils.distance_between_objects_in_2d(uav, self) <= self.attack_range]  # attack_range需要设定
            if len(tmp_uavs) == 0:
                return [0]
            tmp_uavs = tmp_uavs if self.jammer_strike_ability >= len(tmp_uavs) \
                else random.sample(tmp_uavs, self.jammer_strike_ability)  # 如果反制能力超过攻击范围内的无人机数量就直接选所有
            # destroy_num = len(tmp_uavs)  # 设定击落数量
            for uav in tmp_uavs:
                uav.isAlive = False
                map[uav.x_cord][uav.y_cord] = Enemy.EMPTY
        self.jammer_repaired(self.x_cord, self.y_cord, map)  # 反制后进入修复函数阶段
        destroyed_idx = [uav.id for uav in tmp_uavs]
        return destroyed_idx


class MissileVehicle:
    """
        导弹车
        该类⽬标具有反制红⽅⽆⼈机集群的能⼒，可击毁红⽅指定⽆⼈机N架。
        并且在每波次对抗中，导弹⻋指定对哪架⽆⼈机
        可能需要改变的地方
            1.将生命值改为耐久度，基于百分比损伤来决定导弹车的反制能力
            eg:
            序号       剩余耐久百分比      反制能力
            1            0-20%            0
            2            20-30%           1
            3            30-50%           2
            4            50-80%           3
            5            80-100%          4


            2.考虑战场的复杂性，是否添加导弹车的弹药储备功能
            3.是否添加导弹车的攻击范围
    """

    def __init__(self, id, x_cord, y_cord, battle_id, args):
        self.id = id  # id
        self.x_cord = x_cord  # x坐标
        self.y_cord = y_cord  # y坐标
        self.battle_id = battle_id
        self.mapX = args.mapX
        self.mapY = args.mapY
        self.maxHP = args.mv_maxHP
        self.HP = args.mv_maxHP
        self.strike_ability = args.mv_strike_ability  # 导弹车打击能力
        self.attack_range = args.mv_attack_range  # 导弹车攻击范围
        self.target_type = Enemy.MISSILEVEHICLE
        self.isAlive = True  # 存活状态

    def __str__(self):
        return '导弹车_id:{0} 所在位置：x:{1}  y:{2} 当前耐久值：{3} 当前打击能力：{4}架 索引id：{5}'. \
            format(self.id, self.x_cord, self.y_cord, self.HP, self.strike_ability, self.battle_id)

    def set_current_hp(self, val):
        self.HP = val

    def get_current_hp(self):
        return self.HP

    def hp_to_strike_ability(self):
        breakpoints = [20, 30, 50, 80]
        ability = [0, 1, 2, 3, 4]
        self.strike_ability = ability[bisect_right(breakpoints, 100)]

    @property
    def get_current_strike_ability(self):
        return self.strike_ability

    def counter_strike(self, map, multirotors):
        # destroy_num = 0
        if self.isAlive:
            tmp_uavs = [uav for uav in multirotors if
                        utils.distance_between_objects_in_2d(uav, self) <= self.attack_range]  # 该值需要设定
            if len(tmp_uavs) == 0:
                return [0]
            tmp_uavs = tmp_uavs if self.get_current_strike_ability >= len(tmp_uavs) \
                else random.sample(tmp_uavs, self.get_current_strike_ability)  # 如果反制能力超过攻击范围内的无人机数量就直接选所有

            for uav in tmp_uavs:
                uav.isAlive = False
                map[uav.x_cord][uav.y_cord] = Enemy.EMPTY
        destroyed_idx = [uav.id for uav in tmp_uavs]  # 返回被击毁的无人机id
        return destroyed_idx

    def BeAttacked(self, damage, map):
        if self.get_current_hp() - damage <= 0:
            self.isAlive = False
            self.set_current_hp(0)
            map[self.x_cord][self.y_cord] = 0
        else:
            self.set_current_hp(self.HP - damage)
            self.hp_to_strike_ability()  # 设定击毁架数
        return self.isAlive


class Radar:
    """
        雷达类
        雷达可发现探测半径内的⽆⼈机⻜⾏位置。以雷达为中⼼，具有⼀定的探测半径，可对探测半径内出现的⽆⼈机探测
    """

    def __init__(self, id, x_cord, y_cord, battle_id, args):
        self.id = id  # id
        self.x_cord = x_cord  # x坐标
        self.y_cord = y_cord  # y坐标
        self.battle_id = battle_id
        self.mapX = args.mapX
        self.mapY = args.mapY
        self.maxHP = args.rd_maxHP
        self.HP = args.rd_maxHP
        self.detect_radius = args.detect_radius
        self.target_type = Enemy.RADAR
        self.isAlive = True

    def __str__(self):
        return '雷达_id:{0} 所在位置：x:{1}  y:{2} 当前受损程度：{3}% 当前探测范围：{4} 索引id：{5}'. \
            format(self.id, self.x_cord, self.y_cord, self.cal_damage_degree() * 100, self.detect_radius,
                   self.battle_id)

    @property
    def get_current_hp(self):
        return self.HP

    def set_current_hp(self, val):
        self.HP = val

    # 计算受损程度
    def cal_damage_degree(self) -> float:
        # 若所有建筑耐久统一为100
        return (self.maxHP - self.HP) / self.maxHP

    def get_detect_radius(self):
        return self.detect_radius

    # 计算当前的探测范围减少程度
    def get_detect_range_decr_degree(self):
        p = self.cal_damage_degree()
        degrees = [0, 0.2, 0.5, 1.0]
        breakpoints = [0, 0.2, 0.5]
        return degrees[bisect_left(breakpoints, p)]
        # if p == 0:
        #     return 0
        # elif p > 0 and p <= 0.2:
        #     return 0.2
        # elif p > 0.2 and p <= 0.5:
        #     return 0.5
        # elif p > 0.5 and p <= 1:
        #     return 1.0

    def get_current_detect_radius(self):
        # 获取当前探测半径
        return self.get_detect_radius() * (1.0 - self.get_detect_range_decr_degree())

    def get_detect_cordination(self):
        # 该函数返回的是矩阵点集 获得当前可探测点集[(x1,y1),....(xn,yn)]
        current_dect_range = self.get_current_detect_radius()
        detect_cords = utils.find_integer_points_in_circle( \
            self.x_cord, self.y_cord, self.mapX, self.mapY, current_dect_range)
        return detect_cords

    def counter_strike(self, a, b):
        pass

    def BeAttacked(self, damage, map):
        if self.get_current_hp() - damage <= 0:
            self.isAlive = False
            self.set_current_hp(0)
            map[self.x_cord][self.y_cord] = Enemy.EMPTY
        else:
            self.set_current_hp(self.HP - damage)
            self.hp_to_strike_ability()  # 设定击毁架数
        return self.isAlive


# 防空炮 和雷达配合
class AntiAircraftTurret:
    def __init__(self, id, x_cord, y_cord, battle_id, args):
        self.id = id  # id
        self.x_cord = x_cord  # x坐标
        self.y_cord = y_cord  # y坐标
        self.battle_id = battle_id
        self.mapX = args.mapX
        self.mapY = args.mapY
        self.maxHP = args.aat_maxHP
        self.HP = args.aat_maxHP
        self.defend_radius = args.defend_radius
        self.target_type = Enemy.ANTIAIRCRAFTTURRENT
        self.defend_coef = args.defend_coef
        self.base_defend_coef = self.defend_coef  # SECTION:基础的防卫系数 const
        self.isAlive = True

    def __str__(self):
        return '防空炮台_id:{0} 所在位置：x:{1}  y:{2} 当前是否存活:{3} 当前防卫半径：{4} 当前防卫系数：{5} 索引id：{6}'. \
            format(self.id, self.x_cord, self.y_cord, self.isAlive, self.defend_radius, self.defend_coef,
                   self.battle_id)

    @property
    def get_current_hp(self):
        return self.HP

    def set_current_hp(self, val):
        self.HP = val

    def get_defend_radius(self):
        return self.defend_radius

    def get_defend_coef(self):
        return self.defend_coef

    def get_base_defend_coef(self):
        return self.base_defend_coef

    # 计算受损程度
    def cal_damage_degree(self) -> float:
        # 若所有建筑耐久统一为100 采用该方法计算受损程度
        return (self.maxHP - self.HP) / self.maxHP

    # 获得最大的雷达覆盖半径
    def get_max_radar_radius(self, radars) -> float:
        temp_radars = []
        for radar in radars:
            if utils.distance_between_objects_in_2d(self, radar) <= \
                    radar.get_current_detect_radius():
                temp_radars.append(radar.get_detect_radius())
        if len(temp_radars) == 0:
            return 0
        return max(temp_radars)

    def cal_current_defend_coef(self, radars) -> float:
        detect_radius = self.get_max_radar_radius(radars)
        damage_degree = self.cal_damage_degree()
        hp_breakpoints = [0.1, 0.3, 0.7]
        derc_degree = 0  # 防护系数下降程度
        if detect_radius < 0:
            raise Exception('detect radius should not be a minus val!')
        if detect_radius == 0:
            return derc_degree
        if detect_radius > 0 and detect_radius <= 5:
            derc_degrees = [0.5, 0.6, 0.8, 1]
        elif detect_radius > 5 and detect_radius <= 10:
            derc_degrees = [0.3, 0.4, 0.7, 1]
        elif detect_radius > 10 and detect_radius <= 15:
            derc_degrees = [0.1, 0.3, 0.5, 1]
        else:
            derc_degrees = [0.1, 0.2, 0.4, 1]
        # 获得防护系数下降程度
        derc_degree = derc_degrees[bisect_left(hp_breakpoints, damage_degree)]
        self.defend_coef = self.get_base_defend_coef() * (1.0 - derc_degree)

    def isProtected(self, object):
        """
        :param object: 该目标是否在防空炮的保护范围内
        :return: True or False
        """
        return utils.distance_between_objects_in_2d(object, self) <= self.get_defend_radius()

    def counter_strike(self, a, b):
        pass

    def BeAttacked(self, damage, map):
        if self.get_current_hp() - damage <= 0:
            self.isAlive = False
            self.set_current_hp(0)
            map[self.x_cord][self.y_cord] = Enemy.EMPTY
        else:
            self.set_current_hp(self.HP - damage)

        return self.isAlive


# 指挥所
class CommandPost:
    def __init__(self, id, x_cord, y_cord, battle_id, args):
        self.id = id  # id
        self.x_cord = x_cord  # x坐标
        self.y_cord = y_cord  # y坐标
        self.battle_id = battle_id
        self.mapX = args.mapX
        self.mapY = args.mapY
        self.maxHP = args.cp_maxHP
        self.HP = args.cp_maxHP
        self.target_type = Enemy.COMMANDPOST
        self.isAlive = True

    def __str__(self):
        return '指挥所_id:{0} 所在位置：x:{1}  y:{2} 当前耐久：{3}% 是否存活：{4}, 索引id：{5}'. \
            format(self.id, self.x_cord, self.y_cord, self.HP, self.isAlive, self.battle_id)

    def counter_strike(self, a, b):
        pass

    @property
    def get_current_hp(self):
        return self.HP

    def set_current_hp(self, val):
        self.HP = val

    def BeAttacked(self, damage, map):
        if self.get_current_hp() - damage <= 0:
            self.isAlive = False
            self.set_current_hp(0)
            map[self.x_cord][self.y_cord] = Enemy.EMPTY
        else:
            self.set_current_hp(self.HP - damage)
            self.hp_to_strike_ability()  # 设定击毁架数
        return self.isAlive
