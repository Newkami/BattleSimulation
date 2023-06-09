import random
import time
import unittest

import matplotlib.pyplot as plt
import numpy as np

from environment.battle_simulation import BattleEnv, Multirotor
from environment.arguments import get_env_common_args, get_multirotor_args  # , get_rl_common_args
from common.arguments import get_rl_common_args
from environment.utils import visualizeMapIn2d, visualizeMap

args = get_env_common_args()
rl_args = get_rl_common_args()
env = BattleEnv(args, rl_args)


class TestBattleEnv(unittest.TestCase):

    def test_init(self):
        print(env)

    def test_reset(self):
        env.reset()
        # for k, v in env.target_map.items():
        #     print(v)
        print(args)
        env_info = env.get_env_info()
        print(env_info)

    def test_attacked(self):
        env.reset()
        target = env.get_target_by_act(5)
        print(target)
        target.BeAttacked(80, env.g_map)

        visualizeMapIn2d(env.g_map)

    def test_get_agent_by_id(self):
        env.reset()
        print(env.get_agent_by_id(25))

    def test_step(self):
        env.reset()
        actions = [random.randint(1, 14) for i in range(30)]
        # actions = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 4, 3]  # 测试移动
        env.step(actions=actions)

    def test_get_base_damage(self):
        env.reset()
        target = env.get_target_by_act(2)
        print(target)
        print(env.get_base_damage(target))
        target = env.get_target_by_act(5)
        print(target)
        print(env.get_base_damage(target))
        target = env.get_target_by_act(9)
        print(target)
        print(env.get_base_damage(target))

    def test_get_actual_damage(self):
        env.reset()
        target = env.get_target_by_act(2)
        base_damage = env.get_base_damage(target)
        ac_dmg = env.get_actual_damage(target, base_damage)
        print(ac_dmg)

    def test_get_obs(self):
        env.reset()
        obs = env.get_obs()
        obs = np.array(obs)
        print(obs)
        print(obs.shape)

    def test_get_move_reward(self):
        env.reset()
        agent = env.get_agent_by_id(2)
        x_last, y_last = agent.x_cord, agent.y_cord
        agent.execute_move(1, env.g_map)
        print(env.get_move_reward(x_last, y_last, agent.x_cord, agent.y_cord, env.commandpost))

    def test_get_avail_action(self):
        env.reset()
        x, y = env.commandpost.x_cord, env.commandpost.y_cord
        env.multirotors[0].x_cord = 4
        env.multirotors[0].y_cord = 0
        env.missile_vehicles[0].x_cord = 1
        env.missile_vehicles[0].y_cord = 0
        print(env.get_avail_agent_actions(0))



class TestMultiRotor(unittest.TestCase):
    def test_execute_move(self):
        map = np.zeros((10, 20))
        uav_args = get_multirotor_args()
        uav_args.sight_range = 3
        uav = Multirotor(uav_args, 1)
        uav.x_cord = 1
        uav.y_cord = 3
        uav.execute_move(8, map)
        print(uav.x_cord, uav.y_cord)
