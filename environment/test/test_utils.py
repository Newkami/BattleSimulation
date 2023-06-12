import numpy

from environment.utils import *
import unittest


class TestTask_Generator(unittest.TestCase):
    def test_find_points_in_circle(self):
        print(find_integer_points_in_circle(0, 0, 2, 2, 1))

    def test_map(self):
        map = numpy.ones((20, 10))
        map[18][5] = 3
        visualizeMapIn2d(map)

    def test_for(self):
        for i in range(5, -1, -1):
            print(i)

    def test_get_rangeBySpiralMatrix(self):
        print(get_rangeBySpiralMatrix(3, 3, 1))

    def test_get_size(self):
        for i in range(5):
            print(f'{i}', get_size_by_n(i))
