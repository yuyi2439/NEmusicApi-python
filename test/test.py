import os
import unittest


current_path = os.path.dirname(__file__)
suite = unittest.TestSuite()

suite.addTest(unittest.defaultTestLoader.discover(current_path, pattern='test_*.py'))


runner = unittest.TextTestRunner()
runner.run(suite)

