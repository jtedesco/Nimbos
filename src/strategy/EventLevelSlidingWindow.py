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

            # Iterate through each window, each of which will consist of a training example
            for window in windowedLogData:
                # Throw an exception if there is 1 or 0 sub-windows in a window --  the strategy doesn't make sense
                if len(window) <= 1:
                    raise StrategyError(
                        'Error parsing windowed log data, found window with %d sub-windows!' % len(window))

                # Iterate through each sub-window, skipping the last window (since the last is used for classification)
                subWindowData = []
                for subWindowIndex in xrange(0, len(window) - 1):
                    subWindow = window[subWindowIndex]

                    # Counts the number of events of each severity
                    eventCounts = {
                        'INFO': 0,
                        'WARN': 0,
                        'ERROR': 0,
                        'FATAL': 0
                    }

                    for logEvent in subWindow:
                        # Fail to parse the log data if it's invalid (in that it doesn't contain the expected 'SEVERITY' field)
                        if 'SEVERITY' not in logEvent:
                            raise  StrategyError('Error parsing windowed log data, could not find SEVERITY field!')

                        # Tally an event of this severity
                        eventCounts[logEvent['SEVERITY']] += 1

                    # Append the counts for this sub-window
                    subWindowData.append(
                        (eventCounts['INFO'], eventCounts['WARN'], eventCounts['ERROR'], eventCounts['FATAL']))

                # Look for 'FATAL' events in the last window
                foundFatalEvent = False
                for logEvent in window[-1]:
                    if logEvent['SEVERITY'] == 'FATAL':
                        foundFatalEvent = True
                        break

                # Add the training example
                trainingData.append(tuple(subWindowData) + (foundFatalEvent,))

            return trainingData


    def train(self, examples):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).train(examples)


    def predict(self, features):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).predict(features)
