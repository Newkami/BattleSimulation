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
