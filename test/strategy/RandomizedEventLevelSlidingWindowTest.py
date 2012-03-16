from json import load
import os
import unittest
from src.strategy.StrategyError import StrategyError
from src.strategy.slidingWindow.RandomizedEventLevelStrategy import RandomizedEventLevelStrategy

__author__ = 'jon'

class RandomizedEventLevelSlidingWindowTest(unittest.TestCase):
    """
      Tests the randomized prediction strategy based on EventLevelSlidingWindow that randomly selects negative examples
        to match the number of positive training examples.
    """

    def setUp(self):

        self.eventLevelSlidingWindowStrategy = RandomizedEventLevelStrategy('TestData')

        # Possibilities for the parsed training data for five sub-window example
        self.fiveSubWindowTrainingData1 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]
        self.fiveSubWindowTrainingData2 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False)
        ]

        # Possibilities for the parsed training data for six sub-window example
        self.sixSubWindowTrainingData1 = [
            ((2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]
        self.sixSubWindowTrainingData2 = [
            ((2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False)
        ]
        self.projectRoot = os.environ['PROJECT_ROOT']


    def testParseTrainingDataEmpty(self):

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData([])

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataNone(self):

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(None)

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataInvalid(self):

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


    def testParseTrainingDataFiveSubWindows(self):

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/eventLevelSlidingWindow/parsedLog/FiveSubWindows.json'))
        expectedTrainingData1 = self.fiveSubWindowTrainingData1
        expectedTrainingData2 = self.fiveSubWindowTrainingData2

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify that the actual output matches one of the two possibilities
        try:
            self.assertEqual(expectedTrainingData1, actualTrainingData)
        except AssertionError:
            self.assertEqual(expectedTrainingData2, actualTrainingData)

    def testParseTrainingDataSixSubWindows(self):

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/eventLevelSlidingWindow/parsedLog/SixSubWindows.json'))
        expectedTrainingData1 = self.sixSubWindowTrainingData1
        expectedTrainingData2 = self.sixSubWindowTrainingData2

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify that the actual output matches one of the two possibilities
        try:
            self.assertEqual(expectedTrainingData1, actualTrainingData)
        except AssertionError:
            self.assertEqual(expectedTrainingData2, actualTrainingData)


    def testBuildTrainingFileContentNone(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(None)
            self.fail('Should have thrown a StrategyError given None for training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: no examples given!', error.message)


    def testBuildTrainingFileContentEmpty(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent([])
            self.fail('Should have thrown a StrategyError given empty training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: no examples given!', error.message)
