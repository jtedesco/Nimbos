from pprint import pprint
from src.strategy.SlidingWindow import SlidingWindow

__author__ = 'jon'

class EventLevelSlidingWindow(SlidingWindow):
    """
      Class that holds prediction strategies based on a sliding window of log events. Specifically, this strategy
        uses SVM based on the sliding windows of intervals of several hours. Based on features of the last 4 windows,
        this will predict whether or not there will be a fatal error.
      Specifically, the features we consider in this strategy are (for each window, all of these):
        - number of INFO events
        - number of WARN events
        - number of ERROR events
        - number of FATAL events
    """


    def parseWindowedLogData(self, windowedLogData):
        pprint(windowedLogData)

        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).parseWindowedLogData(windowedLogData)


    def train(self, examples):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).train(examples)


    def predict(self, features):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).predict(features)
