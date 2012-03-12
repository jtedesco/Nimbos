import unittest
from src.strategy.SlidingWindow import SlidingWindow

__author__ = 'jon'

class SlidingWindowTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    def setUp(self):
        """
          Reconstruct a new sliding window strategy object each iteration
        """
        self.strategy = SlidingWindow()


    def testParseTrainingDataWithEmptyData(self):
        try:
            self.strategy.parseTrainingData([])
            self.fail("Should have thrown an assertion error")
        except AssertionError, error:
            self.assertEqual(error.message, 'Training data for SlidingWindow must be non-empty!')


    def testParseTrainingDataWithNoData(self):
        try:
            self.strategy.parseTrainingData(None)
            self.fail("Should have thrown an assertion error")
        except AssertionError, error:
            self.assertEqual(error.message, 'Training data for SlidingWindow must be non-empty!')

    def testParseLogWindows(self):
        pass
