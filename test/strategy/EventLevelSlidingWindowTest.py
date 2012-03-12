from json import load
import unittest
from src.strategy.EventLevelSlidingWindow import EventLevelSlidingWindow

__author__ = 'jon'

class EventLevelSlidingWindowTest(unittest.TestCase):
    """
      Unit tests for the SlidingWindow class
    """

    def testEmpty(self):
        """
          Tests that no training data is returned when passed an empty log
        """

        eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()

        actualTrainingData = eventLevelSlidingWindowStrategy.parseWindowedLogData([])

        self.assertEqual(actualTrainingData, [])


    def testNone(self):
        """
          Tests that no training data is returned when passed a null log
        """

        eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()

        actualTrainingData = eventLevelSlidingWindowStrategy.parseWindowedLogData(None)

        self.assertEqual(actualTrainingData, [])


    def testNone(self):
        """
          Tests that no training data is returned when passed an invalid log
        """

        eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()

        actualTrainingData1 = eventLevelSlidingWindowStrategy.parseWindowedLogData([[]])
        actualTrainingData2 = eventLevelSlidingWindowStrategy.parseWindowedLogData([[{}]])
        actualTrainingData3 = eventLevelSlidingWindowStrategy.parseWindowedLogData([[{}, {}]])

        self.assertEqual(actualTrainingData1, [])
        self.assertEqual(actualTrainingData2, [])
        self.assertEqual(actualTrainingData3, [])


    def testFiveSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 5
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open('eventLevelSlidingWindow/json/SampleWindowedEventLevelLog.json'))
        expectedTrainingData = [

            # Contains tuples of counts for (INFO,WARN,ERROR,FATAL) events for the first five sub-windows,
            #  and a True/False label to whether or not it contains a FATAL error in the sixth sub-window
            ((2, 0, 1, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (1, 0, 0, 0), False)
        ]
        eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()

        # Test
        actualTrainingData = eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(actualTrainingData, expectedTrainingData)


    def testSixSubWindows(self):
        """
          Tests that the training data for the event level sliding window strategy is generated correctly for 6
            sub-window length windows
        """

        # Setup
        mockWindowedLogData = load(open('eventLevelSlidingWindow/json/SampleWindowedEventLevelLog.json'))
        expectedTrainingData = [

            # Contains tuples of counts for (INFO,WARN,ERROR,FATAL) events for the first five sub-windows,
            #  and a True/False label to whether or not it contains a FATAL error in the sixth sub-window
            ((2, 0, 1, 0), (0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), True),
            ((0, 0, 0, 0), (1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), False),
            ((1, 0, 1, 0), (0, 3, 0, 0), (0, 0, 0, 0), (1, 0, 0, 1), (1, 0, 0, 0), False)
        ]
        eventLevelSlidingWindowStrategy = EventLevelSlidingWindow()

        # Test
        actualTrainingData = eventLevelSlidingWindowStrategy.parseWindowedLogData(mockWindowedLogData)

        # Verify
        self.assertEqual(actualTrainingData, expectedTrainingData)