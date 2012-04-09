from json import load
import os
import unittest
from src.strategy.slidingWindow.EventLevelStrategy import EventLevelStrategy
from src.strategy.StrategyError import StrategyError

__author__ = 'jon'

class IBMPaperStrategyTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    def setUp(self):
        self.eventLevelSlidingWindowStrategy = EventLevelStrategy('TestData')

        # Parsed training data for five sub-window example
        self.fiveSubWindowTrainingData = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]

        # Parsed training data for six sub-window example
        self.sixSubWindowTrainingData = [
            ((2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]
        self.projectRoot = os.environ['PROJECT_ROOT']


    def testParseTrainingDataEmpty(self):
        """
          Tests that no training data is returned when passed an empty log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData([])

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataNone(self):
        """
          Tests that no training data is returned when passed a null log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(None)

        self.assertEqual([], actualTrainingData)


    def testParseTrainingDataInvalid(self):
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


    def testParseTrainingDataFiveSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 5
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/eventLevelSlidingWindow/parsedLog/FiveSubWindows.json'))
        expectedTrainingData = self.fiveSubWindowTrainingData

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


    def testParseTrainingDataSixSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 6
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open(self.projectRoot + '/test/strategy/eventLevelSlidingWindow/parsedLog/SixSubWindows.json'))
        expectedTrainingData = self.sixSubWindowTrainingData

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


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


    def testBuildTrainingFileContentInvalid(self):

        invalidTrainingData1 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]
        invalidTrainingData2 = [
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (0, 0, 0, 0), False)
        ]

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(invalidTrainingData1)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.buildDataFileContent(invalidTrainingData2)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)


    def testBuildTrainingFileContentFiveWindow(self):

        # Setup
        trainingData = self.fiveSubWindowTrainingData
        expectedTrainingFileContent = open(self.projectRoot + '/test/strategy/ibmPaperStrategy/trainingFile/FiveSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy.buildDataFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)



    def testBuildTrainingFileContentSixWindow(self):

        # Setup
        trainingData = self.sixSubWindowTrainingData
        expectedTrainingFileContent = open(self.projectRoot + '/test/strategy/ibmPaperStrategy/trainingFile/SixSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy.buildDataFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)
