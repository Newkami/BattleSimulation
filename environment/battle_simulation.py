import atexit
import enum
from enum import Enum, unique
import random

import numpy as np
from environment.enemy import *
from absl import logging
logging.set_verbosity(logging.INFO)
from environment.data_generation import Task_Generator
from environment.arguments import get_multirotor_args
from matplotlib import pyplot as plt

@unique
class Objective(enum.IntEnum):
    EMPTY = 0
    JAMMER = 1  #
    MISSILEVEHICLE = 2
    RADAR = 3
    ANTIAIRTURRENT = 4
    COMMANDPOST = 5
    MULTIROTOR = 6


@unique
class Direction(enum.IntEnum):
    FORWARD = 0
    BACK = 1
    LEFT = 2
    RIGHT = 3


class Multirotor:
    def __init__(self, args, id):
        self.id = id
        self.args = args
        self.x_cord = args.x_cord
        self.y_cord = args.y_cord
        self.isAlive = 1
        self.attack_range = args.attack_range
        self.sight_range = args.sight_range
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
                logging.info(
                    "warn in execute_move ({},{}),该点附近没有可选点了".format(
                        act_x,
                        act_y, )
                )
                return
            option = random.sample(options, 1)[0]
            act_x, act_y = option[0], option[1]

        # 执行移动指令
        g_map[self.x_cord][self.y_cord] = Objective.EMPTY
        self.x_cord, self.y_cord = act_x, act_y
        g_map[act_x][act_y] = Objective.MULTIROTOR

    def execute_attack(self, target, g_map):
        """
            若目标在攻击范围内 返回可进行攻击
            若目标在攻击范围外， 但在探测范围内 则执行移动到目标附近指令
        """
        can_attack = False
        distance = utils.distance_between_objects_in_2d(self, target)
        if distance <= self.attack_range:
            can_attack = True
        elif distance > self.attack_range and distance <= self.sight_range:
            options = utils.get_MatrixWithNoObjs(target.x_cord, target.y_cord, g_map, 2)  # 获取两圈更稳健
            assert len(options) != 0, f"({target.x_cord},{target.y_cord})errro in execute_attack: 该点附近没有可选点了"
            intend_pos = random.sample(options, 1)[0]
            act_x, act_y = intend_pos[0], intend_pos[1]
            g_map[self.x_cord][self.y_cord] = Objective.EMPTY
            self.x_cord, self.y_cord = act_x, act_y
            g_map[act_x][act_y] = Objective.MULTIROTOR
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

    def get_sight_range(self):
        return self.sight_range


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
    def get_obs_size(self):
        """Returns the size of the observation."""
        raise NotImplementedError

    #
    def get_state(self):
        """Returns the global state."""
        raise NotImplementedError

    #
    def get_state_size(self):
        """Returns the size of the global state."""
        raise NotImplementedError

    #
    def get_avail_actions(self):
        """Returns the available actions of all agents in a list."""
        raise NotImplementedError

    def get_avail_agent_actions(self, agent_id):
        """Returns the available actions for agent_id."""
        raise NotImplementedError

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
        self.n_actions = 1 + 4 + self.n_enemies  # 动作空间大小
        self.min_destroy_cp_num = args.min_destroy_cp_num  # 击毁指挥所所需的最少无人机数量
        self.move_reward_coef = args.move_reward_coef  # 移动产生的奖励系数
        self.attack_reward_coef = args.attack_reward_coef  # 攻击产生的奖励系数
        self.jammers = []
        self.missile_vehicles = []
        self.radars = []
        self.antiAirturrents = []
        self.commandpost = []
        self.multirotors = []
        self.target_map = {}
        self.sight_range = args.sight_range  # 无人机视野范围
        # 地图变量
        self.g_map = None
        self.u_map = None  # 无人机所用的map

        # 训练所需要的变量
        self.rl_args = rl_args
        self.reward_death_value = rl_args.reward_death_value
        self.reward_win = rl_args.reward_win
        self.episode_limit = rl_args.episode_limit
        # self.step_mul = rl_args.step_mul
        self.max_reward = {
            self.n_enemies * self.reward_death_value + self.reward_win
        }
        self.destroyed_value = rl_args.destroyed_value

        self.n_agents = rl_args.n_agents
        # 在程序执行结束前执行close
        # atexit.register(lambda: self.close())
        # self.map = None

        # private var
        self._total_steps = 0
        self._episode_steps = 0

        self.is_plot = args.is_plot
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
        for v in self.multirotors:
            map_t[v.x_cord][v.y_cord] = Objective.MULTIROTOR
        map_t[self.commandpost.x_cord][self.commandpost.y_cord] = Objective.COMMANDPOST

        return map_t

    def reset(self):
        # 重置环境状态
        self.clearEnv()
        self.initializeEnemy()
        self.initializeMultirotors(self.args.mapX)
        self.g_map = self.generate_map()
        # utils.visualizeMapIn2d(self.g_map)
        obs = self.get_obs()
        self._episode_steps = 0
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

    def initializeMultirotors(self, mapX):
        uav_args = get_multirotor_args()
        uav_args.sight_range = self.sight_range
        start_x = 1
        end_x = mapX - 25
        start_y = 0
        end_y = 3
        sampled_points = []
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if x <= end_x and y <= end_y:
                    sampled_points.append((x, y))

        start_x = 0
        end_x = 3
        start_y = 3
        end_y = 25
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if x <= end_x and y <= end_y:
                    sampled_points.append((x, y))

        for i in range(self.n_agents):
            val = Multirotor(uav_args, 'u' + str(i + 1))
            tmp = random.sample(sampled_points, k=1)[0]
            sampled_points.remove(tmp)
            val.y_cord = tmp[1]
            val.x_cord = tmp[0]
            self.multirotors.append(val)

    def step(self, actions):
        """
            每个时间步 获得action_list
            每架无人机可选择的动作分为移动和攻击
            Returns reward, terminated, info.
             IDEA 0 留给no-op 1-n_enemies 留给朝除指挥所外的目标直接移动
             IDEA 20 特殊移动 指的是 朝向指挥所移动 但不能一步到达
             IDEA 21-40 指攻击 0-n_enemies
             IDEA 移动指令产生的奖励值可以为移动距离产生的负奖励和距离指挥所的距离的正奖励
            思路二：
            每个智能体的动作空间为0：no-op
            和前后左右四个方向的移动：表示一种探索 1 2 3 4
            和攻击某种目标 值设置为11~11+n_enemies 若目标不在攻击范围内的处理情况：
                1.移动到目标附近位置，并给予一定的负奖励
                2.不动 
        """
        self._total_steps += 1
        self._episode_steps += 1
        rewards = []
        assert len(actions) == len(self.multirotors), "actions num error!"
        for idx, action in enumerate(actions):
            reward = 0
            assert action in self.get_total_actions_list(), f"the invalid action value is -{action}-,the avail options are {self.get_total_actions_list()}"
            agent = self.get_agent_by_id(idx)

            if action == 0:
                assert agent.isAlive == 0, "no-op is available only for dead uav!"
                rewards.append(reward)
                continue
            elif action in [1, 2, 3, 4]:  # 朝前后左右移动
                x_last, y_last = agent.x_cord, agent.y_cord
                agent.execute_move(action, self.g_map)
                reward = self.get_move_reward(x_last, y_last, agent.x_cord, agent.y_cord, self.commandpost)
                rewards.append(reward)
            else:
                target = self.get_target_by_act(action)
                pos_last = (agent.x_cord, agent.y_cord)
                can_atk = agent.execute_attack(target, self.g_map)
                reward = self.get_attack_reward(can_atk, target, pos_last, (agent.x_cord, agent.y_cord))
                # utils.visualizeMapIn2d(self.g_map)
                rewards.append(reward)
        # print("---------------开启反制阶段-------------------")
        for _, item in self.target_map.items():
            # for uav in self.multirotors:
            #     print(uav)
            # utils.visualizeMapIn2d(self.g_map)
            idxs = item.counter_strike(self.g_map, self.multirotors)
            # utils.visualizeMapIn2d(self.g_map)  #  测试反制是否有效果
            # for uav in self.multirotors:
            #    print(uav)
            if isinstance(idxs, list):
                if len(idxs) > 0:
                    for idx in idxs:
                        idx = idx[1:]
                        idx = int(idx)
                        rewards[idx - 1] -= self.destroyed_value

        fi_reward = np.mean(rewards)
        terminated, win_tag = self.isDone()
        if win_tag:
            fi_reward += self.reward_win
        # fi_reward -= 5  # 每经过一个回合奖励值降低
        info = {"battle_won": win_tag}

        # count units that are still alive
        dead_allies, dead_enemies = 0, 0
        for i in self.multirotors:
            if i.isAlive == 0:
                dead_allies += 1
        for i, v in self.target_map.items():
            if v.isAlive == 0:
                dead_enemies += 1

        info["dead_allies"] = dead_allies
        info["dead_enemies"] = dead_enemies
        if self._episode_steps >= self.episode_limit:
            fi_reward -= self.args.exceed_episode_limit_reward
        # self.print_info_step()

        return fi_reward, terminated, info

    def clearEnv(self):
        self.jammers.clear()
        self.antiAirturrents.clear()
        self.radars.clear()
        self.missile_vehicles.clear()
        self.multirotors.clear()

    def get_agent_by_id(self, id) -> Multirotor:
        assert id >= 0 and id < self.n_agents, "访问id不合法"
        return self.multirotors[id]

    def get_total_actions(self):
        return 5 + self.n_enemies

    def get_total_actions_list(self):
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
            total_actions.append(5 + i)
        # return self.n_enemies + 5
        return total_actions

    def get_target_by_act(self, act):
        act = act - 4
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

    def isDone(self):
        # return terminated, wintag
        terminated = False
        wintag = False
        uav_alive = [i for i in self.multirotors if i.isAlive == True]
        target_alive = [v for _, v in self.target_map.items() if v.isAlive == True]

        if self.commandpost.isAlive == False:
            wintag = True
            terminated = True
        if len(uav_alive) <= self.min_destroy_cp_num:
            terminated = True
        return terminated, wintag

    def get_move_reward(self, x_last, y_last, x, y, target: CommandPost):
        """
            计算移动产生的损失和奖励
            与上次位置相比，产生的位移为损失
            用上次位置和本次位置分别计算和指挥所的距离做差，更近则为正奖励，更远则为负奖励
        """
        loss = -utils.distance_between_objects_in_2d((x_last, y_last), (x, y))
        loss = round(loss / 2, 2)
        dis_last = utils.distance_between_objects_in_2d((x_last, y_last), (target.x_cord, target.y_cord))
        dis_now = utils.distance_between_objects_in_2d((x, y), (target.x_cord, target.y_cord))
        reward = round(dis_last - dis_now, 2) * self.move_reward_coef
        return loss + reward

    def get_attack_reward(self, can_atk, target, pos_last, pos_now):
        # 计算攻击动作产生的奖励值
        reward = 0
        if can_atk:
            base_damage = self.get_base_damage(target)
            actual_damage = self.get_actual_damage(target, base_damage)
            alive_st = target.BeAttacked(actual_damage, self.g_map)  # 返回存活状态
            reward += actual_damage
            if target.target_type in [Enemy.JAMMER, Enemy.MISSILEVEHICLE]:  # 若攻击的目标是干扰机或导弹车
                reward *= self.attack_reward_coef
            elif target.target_type == Enemy.COMMANDPOST:
                reward *= self.attack_reward_coef + 0.3  # 如果是指挥所奖励值更多一些
                if not alive_st:
                    reward += self.reward_death_value
        else:  # 如果不能攻击，就产生移动损失
            reward -= utils.distance_between_objects_in_2d(pos_last, pos_now)
        return reward

    # env info

    def get_state_size(self):
        return self.n_agents * 3 + self.n_enemies * 4

    def get_obs_size(self):
        return utils.get_size_by_n(self.sight_range) + 3

    def get_obs_agent(self, agent_id):
        """
        :param agent_id:无人机id
        :return: 无人机的观测空间
        """
        obs = []
        uav = self.get_agent_by_id(agent_id)
        # otherwise dead, return all zeros
        if uav.isAlive:
            obs.extend([uav.isAlive, uav.x_cord, uav.y_cord])  # 添加存活状态和坐标
            cords = utils.get_rangeBySpiralMatrix(uav.x_cord, uav.y_cord, uav.sight_range, False)
            for cord in cords:
                if not utils.IsInMap(cord[0], cord[1], self.args.mapX, self.args.mapY):
                    obs.append(-1)
                else:
                    obs.append(self.g_map[cord[0]][cord[1]])
        else:
            obs = [0] * self.get_obs_size()
        return obs

    def get_obs(self):
        agents_obs = [self.get_obs_agent(i) for i in range(self.n_agents)]
        return agents_obs

    def get_state(self):
        state = []
        for i in self.multirotors:
            state.extend([i.isAlive, i.x_cord, i.y_cord])
        for _, i in self.target_map.items():
            state.extend([i.HP, i.isAlive, i.x_cord, i.y_cord])
        return state

    def can_move(self, uav, direction):
        if direction == Direction.FORWARD:
            return uav.y_cord != self.args.mapY
        elif direction == Direction.BACK:
            return uav.y_cord != 0
        elif direction == Direction.LEFT:
            return uav.x_cord != 0
        else:
            return uav.x_cord != self.args.mapX

    def get_avail_agent_actions(self, agent_id):
        """
            :param agent_id: 智能体id
            :return: 返回可选择的动作
        """
        agent = self.get_agent_by_id(agent_id)
        if agent.isAlive:
            avail_actions = [0] * self.n_actions  # 禁止0值被选择
            if self.can_move(agent, Direction.FORWARD):
                avail_actions[1] = 1
            if self.can_move(agent, Direction.BACK):
                avail_actions[2] = 1
            if self.can_move(agent, Direction.LEFT):
                avail_actions[3] = 1
            if self.can_move(agent, Direction.RIGHT):
                avail_actions[4] = 1
            sight_range = agent.get_sight_range()
            target_items = self.target_map.items()
            for k, v in target_items:
                if utils.distance_between_objects_in_2d(agent, v) <= sight_range:
                    avail_actions[4 + v.battle_id] = 1
            return avail_actions
        else:
            return [1] + [0] * (self.n_actions - 1)

    def get_avail_actions(self):
        avail_actions = []
        for agent_id in range(self.multirotors):
            avail_agent = self.get_avail_agent_actions(agent_id)
            avail_actions.append(avail_agent)
        return avail_actions

    def print_info_step(self):
        print(f'-------回合{self._episode_steps}信息汇总---------')
        print()
        print('--------无人机状态信息-----------')
        for i in self.multirotors:
            print(i)
        print('--------敌军目标状态信息-----------')
        for _, v in self.target_map.items():
            print(v)

    def get_env_info(self):
        difficulty = {
            0: 'easy',
            1: 'medium',
            2: 'hard',
            3: 'custom'
        }
        env_info = super().get_env_info()
        env_info["difficulty"] = difficulty[self.args.difficulty]
        env_info["map"] = f"x_{self.args.mapX}_y_{self.args.mapY}_" + env_info["difficulty"]
        return env_info

    def close(self):
        self.clearEnv()
        exit(0)