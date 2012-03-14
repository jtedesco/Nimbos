import unittest
from test.parser.IntrepidRASParserTest import IntrepidRASParserTest
from test.strategy.EventLevelSlidingWindowTest import EventLevelSlidingWindowTest
from test.strategy.SlidingWindowTest import SlidingWindowTest

__author__ = 'jon'


suite = unittest.TestLoader().loadTestsFromTestCase(SlidingWindowTest)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EventLevelSlidingWindowTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(IntrepidRASParserTest))

unittest.TextTestRunner(verbosity=2).run(suite)