from environment.data_generation import Task_Generator
from environment.arguments import get_env_common_args
import unittest

args = get_env_common_args()
tg = Task_Generator()
class TestTask_Generator(unittest.TestCase):
    def test_generator_task(self):
        a, b, c, d, e = tg.generate_task(args)
        for i in a:
            print(i)
        for i in b:
            print(i)
        for i in c:
            print(i)
        for i in d:
            print(i)
        print(e)
