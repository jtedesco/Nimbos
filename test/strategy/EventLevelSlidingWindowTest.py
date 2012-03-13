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


    def testParseTrainignDataEmpty(self):
        """
          Tests that no training data is returned when passed an empty log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData([])

        self.assertEqual([], actualTrainingData)


    def testParseTrainignDataNone(self):
        """
          Tests that no training data is returned when passed a null log
        """

        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(None)

        self.assertEqual([], actualTrainingData)


    def testParseTrainignDataInvalid(self):
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
        mockWindowedLogData = load(open('eventLevelSlidingWindow/parsedLog/FiveSubWindows.json'))
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
        mockWindowedLogData = load(open('eventLevelSlidingWindow/parsedLog/SixSubWindows.json'))
        expectedTrainingData = self.sixSubWindowTrainingData

        # Test
        actualTrainingData = self.eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(expectedTrainingData, actualTrainingData)


    def testBuildTrainingFileContentNone(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildTrainingFileContent(None)
            self.fail('Should have thrown a StrategyError given None for training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: no examples given!', error.message)


    def testBuildTrainingFileContentEmpty(self):

        try:
            self.eventLevelSlidingWindowStrategy.buildTrainingFileContent([])
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
            self.eventLevelSlidingWindowStrategy.buildTrainingFileContent(invalidTrainingData1)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)

        try:
            self.eventLevelSlidingWindowStrategy.buildTrainingFileContent(invalidTrainingData2)
            self.fail('Should have thrown a StrategyError given invalid training data!')
        except StrategyError, error:
            self.assertEqual('Error building training file content: Invalid training data!', error.message)


    def testBuildTrainingFileContentFiveWindow(self):

        # Setup
        trainingData = self.fiveSubWindowTrainingData
        expectedTrainingFileContent = open('eventLevelSlidingWindow/trainingFile/FiveSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy.buildTrainingFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)



    def testBuildTrainingFileContentSixWindow(self):

        # Setup
        trainingData = self.sixSubWindowTrainingData
        expectedTrainingFileContent = open('eventLevelSlidingWindow/trainingFile/SixSubWindows').read()

        # Test
        actualTrainingFileContent = self.eventLevelSlidingWindowStrategy.buildTrainingFileContent(trainingData)

        # Verify
        self.assertEqual(expectedTrainingFileContent, actualTrainingFileContent)
