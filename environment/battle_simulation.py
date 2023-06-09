import atexit
import enum
from enum import Enum, unique
import random

import numpy as np
from environment.enemy import *
from environment.arguments import *
from environment.data_generation import Task_Generator
from environment.arguments import get_multirotor_args
import matplotlib.pyplot as plt


@unique
class Objective(enum.IntEnum):
    EMPTY = 0
    JAMMER = 1  #
    MISSILEVEHICLE = 2
    RADAR = 3
    ANTIAIRTURRENT = 4
    COMMANDPOST = 5
    MULTIROTOR = 6


class Multirotor:
    def __init__(self, args, id):
        self.id = id
        self.args = args
        self.x_cord = args.x_cord
        self.y_cord = args.y_cord
        self.isAlive = 1
        self.attack_range = args.attack_range
        self.detect_range = args.detect_range
        self.steps = args.steps
        # 攻击范围目标处于该范围能才可以被选择

    def __str__(self):
        return '无人机id: {0} 所在位置：({1} , {2}) 当前是否存活：{3}'.format(self.id, self.x_cord, self.y_cord,
                                                                            self.isAlive)

    def execute_move(self, action, g_map):
        '''
             1. 先检测是否超出地图范围，若超出，则缩减移动的步数，最少为1, 到1 还是超出地图范围了 那么就不移动
             2. 再检测移动位置是否有其他对象，若有，就获取对象附近的八通点，随机挑选一个位置作为实际移动的点,若附近的点也没位置了 那么就不移动
        '''
        if action == 1:  # 向前移动
            act_x, act_y = self.move_forward_aux(g_map.shape[0], g_map.shape[1])
        elif action == 2:  # 向后移动
            act_x, act_y = self.move_back_aux(g_map.shape[0], g_map.shape[1])
        elif action == 3:  # 向左移动
            act_x, act_y = self.move_left_aux(g_map.shape[0], g_map.shape[1])
        else:  # 向右移动
            act_x, act_y = self.move_right_aux(g_map.shape[0], g_map.shape[1])

        if act_x == self.x_cord and act_y == self.y_cord:  # 说明没有合适的范围可供移动
            return

        if g_map[act_x][act_y] != 0:  # 说明位置上有其他对象
            options = utils.getEightPointswithNoobs(act_x, act_y, g_map)
            if len(options) == 0:
                print(f"({act_x},{act_y})该点附近没有可选点了")
                return
            option = random.sample(options, 1)[0]
            act_x, act_y = option[0], option[1]

        # 执行移动指令
        g_map[self.x_cord][self.y_cord] = Objective.EMPTY
        self.x_cord, self.y_cord = act_x, act_y
        g_map[act_x][act_y] = Objective.MULTIROTOR
        print(g_map[act_x][act_y])

    def execute_attack(self, target, g_map):
        """
            若目标在攻击范围内 返回可进行攻击
            若目标在攻击范围外， 但在探测范围内 则执行移动到目标附近指令
        """
        can_attack = False
        distance = utils.distance_between_objects_in_2d(self, target)
        if distance <= self.attack_range:
            can_attack = True
        elif distance > self.attack_range and distance <= self.detect_range:
            options = utils.get_MatrixWithNoObjs(target.x_cord, target.y_cord, g_map, 2)  # 获取两圈更稳健
            assert len(options) != 0, f"({target.x_cord},{target.y_cord})errro in execute_attack: 该点附近没有可选点了"
            intend_pos = random.sample(options, 1)[0]
            act_x, act_y = intend_pos[0], intend_pos[1]
            g_map[self.x_cord][self.y_cord] = Objective.EMPTY
            self.x_cord, self.y_cord = act_x, act_y
            g_map[act_x][act_y] = Objective.MULTIROTOR
            print(g_map[act_x][act_y])
        else:
            # 超过detect_range的目标打算通过无效动作mask来遮蔽住
            pass
        return can_attack

    def move_forward_aux(self, mapX, mapY):
        for i in range(self.steps, -1, -1):  # 若不在范围内 则缩小移动的步数
            if i == 0:
                return self.x_cord, self.y_cord
            intend_pos_x = self.x_cord
            intend_pos_y = self.y_cord + i
            if utils.IsInMap(intend_pos_x, intend_pos_y, mapX, mapY):
                return intend_pos_x, intend_pos_y

    def move_back_aux(self, mapX, mapY):
        for i in range(self.steps, -1, -1):  # 若不在范围内 则缩小移动的步数
            if i == 0:
                return self.x_cord, self.y_cord
            intend_pos_x = self.x_cord
            intend_pos_y = self.y_cord - i
            if utils.IsInMap(intend_pos_x, intend_pos_y, mapX, mapY):
                return intend_pos_x, intend_pos_y

    def move_left_aux(self, mapX, mapY):
        for i in range(self.steps, -1, -1):  # 若不在范围内 则缩小移动的步数
            if i == 0:
                return self.x_cord, self.y_cord
            intend_pos_x = self.x_cord - i
            intend_pos_y = self.y_cord
            if utils.IsInMap(intend_pos_x, intend_pos_y, mapX, mapY):
                return intend_pos_x, intend_pos_y

    def move_right_aux(self, mapX, mapY):
        for i in range(self.steps, -1, -1):  # 若不在范围内 则缩小移动的步数
            if i == 0:
                return self.x_cord, self.y_cord
            intend_pos_x = self.x_cord + i
            intend_pos_y = self.y_cord
            if utils.IsInMap(intend_pos_x, intend_pos_y, mapX, mapY):
                return intend_pos_x, intend_pos_y


class MultiAgentEnv(object):
    # def step(self, actions):
    #     """Returns reward, terminated, info."""
    #     raise NotImplementedError
    #
    # def get_obs(self):
    #     """Returns all agent observations in a list."""
    #     raise NotImplementedError
    #
    # def get_obs_agent(self, agent_id):
    #     """Returns observation for agent_id."""
    #     raise NotImplementedError
    #
    # def get_obs_size(self):
    #     """Returns the size of the observation."""
    #     raise NotImplementedError
    #
    # def get_state(self):
    #     """Returns the global state."""
    #     raise NotImplementedError
    #
    # def get_state_size(self):
    #     """Returns the size of the global state."""
    #     raise NotImplementedError
    #
    # def get_avail_actions(self):
    #     """Returns the available actions of all agents in a list."""
    #     raise NotImplementedError
    #
    # def get_avail_agent_actions(self, agent_id):
    #     """Returns the available actions for agent_id."""
    #     raise NotImplementedError
    #
    def get_total_actions(self):
        """Returns the total number of actions an agent could ever take."""
        raise NotImplementedError

    def reset(self):
        """Returns initial observations and states."""
        raise NotImplementedError

    # def render(self):
    #     raise NotImplementedError
    #
    # def close(self):
    #     raise NotImplementedError
    #
    # def seed(self):
    #     raise NotImplementedError

    def get_env_info(self):
        env_info = {
            "state_shape": self.get_state_size(),
            "obs_shape": self.get_obs_size(),
            "n_actions": self.get_total_actions(),
            "n_agents": self.n_agents,
            "episode_limit": self.episode_limit,
        }
        return env_info


class BattleEnv(MultiAgentEnv):

    def __init__(self, args, rl_args):
        self.args = args

        self.n_jammer = args.n_jammer
        self.n_missilevehicle = args.n_missilevehicle
        self.n_radar = args.n_radar
        self.n_antiAirturrent = args.n_antiAirturrent
        self.n_commandpost = args.n_commandpost
        self.n_enemies = self.n_jammer + self.n_radar + self.n_missilevehicle + self.n_antiAirturrent + self.n_commandpost
        self.jammers = []
        self.missile_vehicles = []
        self.radars = []
        self.antiAirturrents = []
        self.commandpost = []
        self.multirotors = []
        self.target_map = {}

        # 地图变量
        self.g_map = None
        self.u_map = None  # 无人机所用的map

        # 训练所需要的变量
        self.rl_args = rl_args
        self.reward_death_value = rl_args.reward_death_value
        self.reward_win = rl_args.reward_win
        self.episode_limit = rl_args.episode_limit
        self.step_mul = rl_args.step_mul
        self.max_reward = {
            self.n_enemies * self.reward_death_value + self.reward_win
        }

        self.n_agents = rl_args.n_agents
        # 在程序执行结束前执行close
        # atexit.register(lambda: self.close())
        # self.map = None

    # 生成作战地图
    def generate_map(self):
        map_t = np.zeros(shape=(self.args.mapX, self.args.mapY))
        for v in self.jammers:
            map_t[v.x_cord][v.y_cord] = Objective.JAMMER
        for v in self.missile_vehicles:
            map_t[v.x_cord][v.y_cord] = Objective.MISSILEVEHICLE
        for v in self.radars:
            map_t[v.x_cord][v.y_cord] = Objective.RADAR
        for v in self.antiAirturrents:
            map_t[v.x_cord][v.y_cord] = Objective.ANTIAIRTURRENT
        map_t[self.commandpost.x_cord][self.commandpost.y_cord] = Objective.COMMANDPOST

        return map_t

    def reset(self):
        # 重置环境状态
        self.clearEnv()
        self.initializeEnemy()
        self.initializeMultirotors()
        self.g_map = self.generate_map()
        utils.visualizeMapIn2d(self.g_map)
        obs = []
        return obs

    """初始化敌军信息"""

    def initializeEnemy(self):
        self.jammers, self.missile_vehicles, self.radars, self.antiAirturrents, self.commandpost = Task_Generator().generate_task(
            self.args)
        for v in self.jammers:
            self.target_map[v.battle_id] = v
        for v in self.missile_vehicles:
            self.target_map[v.battle_id] = v
        for v in self.radars:
            self.target_map[v.battle_id] = v
        for v in self.antiAirturrents:
            self.target_map[v.battle_id] = v
        self.target_map[self.commandpost.battle_id] = self.commandpost

    """初始化无人机集群信息"""

    def initializeMultirotors(self):
        uav_args = get_multirotor_args()
        for i in range(self.n_agents):
            self.multirotors.append(Multirotor(uav_args, 'u' + str(i + 1)))

    def step(self, actions):
        """
            每个时间步 获得action_list
            每架无人机可选择的动作分为移动和攻击
            Returns reward, terminated, info.

            动作空间设计
            1.移动分为前后左右移动m格， 该设计认为地图信息不可知 需要带探索
              no-op(供阵亡无人机选择)， 攻击为范围内的目标[1,0,0,1,1,0,0,1,1,0] 1表示范围内的目标可选
              actions 的 可选动作值
            0 ：no-op 1-n_enemeis : 攻击
            2. 动作空间设计为朝九个目标移动， 移动即为朝该目标移动，并且一定能到达， 第十个动作表示朝指挥所移动n个单位
                攻击为10个可供选择的动作

             IDEA 0 留给no-op 1-n_enemies 留给朝除指挥所外的目标直接移动
             IDEA 20 特殊移动 指的是 朝向指挥所移动 但不能一步到达
             IDEA 21-40 指攻击 0-n_enemies
             IDEA 移动指令产生的奖励值可以为移动距离产生的负奖励和距离指挥所的距离的正奖励
        """
        """
            思路二：
            每个智能体的动作空间为0：no-op
            和前后左右四个方向的移动：表示一种探索 1 2 3 4
            和攻击某种目标 值设置为11~11+n_enemies 若目标不在攻击范围内的处理情况：
                1.移动到目标附近位置，并给予一定的负奖励
                2.不动 
        """
        rewards = []
        for idx, action in enumerate(actions):
            reward = 0
            assert action in self.get_total_actions(), "action value is invalid!"
            agent = self.get_agent_by_id(idx + 1)

            if action == 0:
                assert agent.isAlive == 0, "no-op is available only for dead uav!"
                rewards.append(reward)
                continue
            elif action in [1, 2, 3, 4]:  # todo: 朝前后左右移动
                agent.execute_move(action, self.g_map)
            else:
                # todo: 攻击指令 封装为一个执行攻击指令的函数
                target = self.get_target_by_act(action)
                can_atk = agent.execute_attack(target, self.g_map)
                if can_atk:
                    base_damage = self.get_base_damage(target)
                    actual_damage = self.get_actual_damage(target, base_damage)
                    alive_st = target.BeAttacked(actual_damage, self.g_map)  # 返回存活状态
                    reward += actual_damage
                    if not alive_st:
                        reward += self.reward_death_value
                # todo 该处奖励函数的设计方案还需优化
            rewards.append(reward)
        print("---------------开启反制阶段-------------------")
        for item in self.target_map:
            item.counter_strike(self.g_map, self.multirotors)

    def clearEnv(self):
        self.jammers.clear()
        self.antiAirturrents.clear()
        self.radars.clear()
        self.missile_vehicles.clear()
        self.multirotors.clear()

    @classmethod
    def getState(cls):
        pass

    def getAllobs(self):
        pass

    def get_agent_by_id(self, id) -> Multirotor:
        assert id > 0 and id <= self.n_agents, "访问id不合法"
        return self.multirotors[id - 1]

    def get_total_actions(self):
        """
            两种动作选择方案
            1st: 1+4+n_enemies
            2nd: 直接移动，朝除了指挥所外的目标直接移动到附近位置 大小为n_enemies-1
                 朝向移动 朝指挥所方向移动m个栅格点
                 攻击目标 为n_enemies
                 加上no-op
                 总大小为 2*enemies+1

            return: n_actions
        """
        total_actions = [0, 1, 2, 3, 4]
        for i in range(self.n_enemies):
            total_actions.append(11 + i)
        # return self.n_enemies + 5
        return total_actions

    def get_target_by_act(self, act):
        return self.target_map[act]

    def get_base_damage(self, target):
        # SECTION: 根据目标类型获取不同的基础伤害
        if target.target_type == Objective.JAMMER:
            return self.args.damage_to_jammer
        elif target.target_type == Objective.MISSILEVEHICLE:
            return self.args.damage_to_mv
        elif target.target_type == Objective.RADAR:
            return self.args.damage_to_rd
        elif target.target_type == Objective.ANTIAIRTURRENT:
            return self.args.damage_to_aat
        elif target.target_type == Objective.COMMANDPOST:
            return self.args.damage_to_cp

    def get_actual_damage(self, target, base_damage):
        dc_list = []  # defend_coef列表
        for v in self.antiAirturrents:
            v.cal_current_defend_coef(self.radars)  # 为每个防空炮设置防御系数
            if v.isProtected(target):
                dc_list.append(v.get_defend_coef())
        if len(dc_list) == 0:
            actual_damage = base_damage

        else:
            assert max(dc_list) >= 0 and max(dc_list) <= 1, "防卫系数不在合理范围内 请检查cal_current_defend_coef"
            actual_damage = (1 - max(dc_list)) * base_damage

        return actual_damage
