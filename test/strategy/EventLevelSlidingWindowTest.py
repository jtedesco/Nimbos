from json import load
import unittest
from src.strategy.EventLevelSlidingWindow import EventLevelSlidingWindow
from src.strategy.StrategyError import StrategyError

__author__ = 'jon'

class EventLevelSlidingWindowTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    def setUp(self):
        self.eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()


    def testEmpty(self):
        """
          Tests that no training data is returned when passed an empty log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData([])

        self.assertEqual([], actualTrainingData)


    def testNone(self):
        """
          Tests that no training data is returned when passed a null log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(None)

        self.assertEqual([], actualTrainingData)


    def testInvalid(self):
        """
          Tests that no training data is returned when passed an invalid log
        """

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[]])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data, found window with 0 sub-windows!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[[{}]]])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data, found window with 1 sub-windows!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.parseWindowedLogData([[[{}, {}], [], []]])
            self.fail('Trying to parse an invalid log should have thrown an exception!')
        except StrategyError, error:
            self.assertEqual('Error parsing windowed log data, could not find SEVERITY field!', error.message)


    def testFiveSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 5
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open('eventLevelSlidingWindow/json/SampleFiveWindowedEventLevelLog.json'))
        expectedTrainingData = [

            # Contains tuples of counts for (INFO,WARN,ERROR,FATAL) events for the first five sub-windows,
            #  and a True/False label to whether or not it contains a FATAL error in the sixth sub-window
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


    def testSixSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 6
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open('eventLevelSlidingWindow/json/SampleSixWindowedEventLevelLog.json'))
        expectedTrainingData = [

            # Contains tuples of counts for (INFO,WARN,ERROR,FATAL) events for the first five sub-windows,
            #  and a True/False label to whether or not it contains a FATAL error in the sixth sub-window
            ((2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)