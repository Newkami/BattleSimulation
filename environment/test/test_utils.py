import matplotlib.pyplot as plt
import numpy
import numpy as np

from environment.utils import *
import unittest
from matplotlib import animation


class TestTask_Generator(unittest.TestCase):
    def test_find_points_in_circle(self):
        print(find_integer_points_in_circle(0, 0, 2, 2, 1))

    def test_map(self):
        fig, ax = plt.subplots()
        for i in range(10):
            map = numpy.random.randint(0, 6, (20, 20))
            visualizeMap(map, fig, ax)
        plt.show()
        plt.close()

    def test_for(self):
        for i in range(5, -1, -1):
            print(i)

    def test_get_rangeBySpiralMatrix(self):
        print(get_rangeBySpiralMatrix(3, 3, 1))

    def test_get_size(self):
        for i in range(5):
            print(f'{i}', get_size_by_n(i))

    def test_get_points_in_quadrants(self):
        print(get_points_in_quadrants((0, 0), 5))

    def test_get_quadrantsPointwithNoObjs(self):
        options = get_quadrantsPointwithNoObjs(5, 5, np.zeros((50, 50)), 5)
        print(len(options))
        print(options)

    def test_get_defind_list(self):
        command = [35, 35]
        n = 30
        actual_points = 10
        a = get_defend_pos_list(command, n, actual_points, 50, 50)
        # print(a)

    def test_IsInMap(self):
        test = [(47, 49), (46, 49), (44, 48), (41, 48), (39, 48), (41, 44), (41, 43), (41, 42), (44, 41), (45, 40),
                (46, 39), (48, 41), (48, 43), (48, 46), (51, 52), (45, 55), (37, 54), (34, 48), (35, 46), (34, 39),
                (37, 35), (43, 35), (45, 34), (54, 38)]
        for k, v in enumerate(test):
            print(v, IsInMap(v[0], v[1], 50, 50))
            # del[test[k]]

        print(test)
