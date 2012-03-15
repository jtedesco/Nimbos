import unittest
from test.parser.RegexParserTest import RegexParserTest
from test.parser.TableParserTest import TableParserTest
from test.parser.UtilTest import UtilTest
from test.parser.IntrepidRASParserTest import IntrepidRASParserTest
from test.strategy.EventLevelSlidingWindowTest import EventLevelSlidingWindowTest
from test.strategy.SlidingWindowTest import SlidingWindowTest

__author__ = 'jon'


suite = unittest.TestLoader().loadTestsFromTestCase(SlidingWindowTest)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(EventLevelSlidingWindowTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(IntrepidRASParserTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(UtilTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TableParserTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RegexParserTest))

unittest.TextTestRunner(verbosity=2).run(suite)