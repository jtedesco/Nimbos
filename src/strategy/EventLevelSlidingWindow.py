from src.strategy.SlidingWindow import SlidingWindow
from src.strategy.StrategyError import StrategyError

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
        """
          Helper function to parse the windowed log data (log data properly divided into sliding windows for learning)
            into training examples.

            @param  windowedLogData The log data divided into sliding window format
        """

        # Handle case of invalid windowed log data
        if windowedLogData is None or len(windowedLogData) <= 0:
            return []

        else:
            trainingData = []

            for window in windowedLogData:
                # Throw an exception if there is 1 or 0 sub-windows in a window --  the strategy doesn't make sense
                print window
                if len(window) <= 1:
                    raise StrategyError(
                        'Error parsing windowed log data, found window with %d sub-windows!' % len(window))

                for subWindow in window:
                    for logEvent in subWindow:
                        if 'SEVERITY' not in logEvent:
                            raise  StrategyError('Error parsing windowed log data, could not find SEVERITY field!')

            return trainingData


    def train(self, examples):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).train(examples)


    def predict(self, features):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).predict(features)
