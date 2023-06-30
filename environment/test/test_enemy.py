import unittest

import numpy as np

from environment.battle_simulation import BattleEnv, Multirotor
from environment.arguments import get_env_common_args, get_multirotor_args  # , get_rl_common_args
from common.arguments import get_rl_common_args
from environment.utils import visualizeMapIn2d
from environment.enemy import *

args = get_env_common_args()
rl_args = get_rl_common_args()
env = BattleEnv(args, rl_args)
env.reset()


class TestJammer(unittest.TestCase):
    def test_counter(self):
        for i in env.jammers:
            print(i)
            print('---------------------')
            i.isTakingoff = False
            print(i.counter_strike(env.g_map, env.multirotors))
            print(i)

    def test_be_attacked(self):
        for i in env.jammers:
            i.BeAttacked(120, env.g_map)
        visualizeMapIn2d(env.g_map)

    def test_repair(self):
        for i in env.jammers:
            i.HP = 20
            i.isTakingoff = False
            print(i)
            i.jammer_repaired(i.x_cord, i.y_cord, env.g_map)
            print(i)
        visualizeMapIn2d(env.g_map)

class TestRadar(unittest.TestCase):
    def test_be_attacked(self):
        for i in env.radars:
            i.BeAttacked(100, env.g_map)
        visualizeMapIn2d(env.g_map)


class TestMissile_Vehicle(unittest.TestCase):
    def test_be_attacked(self):
        for i in env.missile_vehicles:
            i.BeAttacked(100, env.g_map)
        visualizeMapIn2d(env.g_map)