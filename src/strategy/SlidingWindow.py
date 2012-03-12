from datetime import timedelta, datetime
from src.PredictionStrategy import PredictionStrategy

__author__ = 'jon'

class SlidingWindow(PredictionStrategy):
    """
      Class that holds prediction strategies based on a sliding window of log events. Specifically, this strategy
        uses SVM based on the sliding windows of intervals of several hours. Based on features of the last 4 windows,
        this will predict whether or not there will be a fatal error.
    """

    def __init__(self, windowDelta=timedelta(hours=5), numberOfSubWindows=5):
        """
          Constructs the properties of the sliding window strategy
            @param  windowDelta         The time delta for each sub-window
            @param  numberOfSubWindows  The number of sub-windows to use in a sliding window
        """

        super(SlidingWindow, self).__init__()

        # The format to which timestamps are expected to adhere
        self.TIMESTAMP_FORMAT = "%Y-%m-%d-%H.%M.%S.%f"

        self.windowDelta = windowDelta
        self.numberOfSubWindows = numberOfSubWindows


    def parseTrainingData(self, data):
        """
          Parse the training log data. All log entries are expected to contain an EVENT_TIME entry, which contains a
           timestamp of the event formatted as "%Y-%m-%d-%H.%M.%S.%f", or Year-Month-Day-Hour.Minute.Second.Millisecond.
        """

        if data is None or len(data) <= 0:
            raise AssertionError('Training data for SlidingWindow must be non-empty!')
        else:
            # Parse the training data into windows
            trainingData = self.parseLogWindows(data)

            # The training data, where each entry is a tuple of tuples
            #   organized by windows, then sub-windows, then data
            return None


    def parseLogWindows(self, data):
        """
          Helper function to take the log data and parse it into windows of windows
            @param  data    The original training data
        """

        # The end timestamp of the the next sub-window, initialized to first timestamp plus time delta
        endSubWindowTimestamp = datetime.strptime(data[0]['EVENT_TIME'], self.TIMESTAMP_FORMAT) + self.windowDelta

        # The list of list of lists of lists (log entries broken into windows and sub windows)
        windowedLogData = []
        dataIndex = 0
        while dataIndex < len(data):
            windowData = []
            subWindowIndex = 0

            # Iterate across all sub-windows (or gracefully handle when we run out of data)
            while subWindowIndex < self.numberOfSubWindows and dataIndex < len(data):
                subWindowData = []
                nextTimestamp = datetime.strptime(data[dataIndex]['EVENT_TIME'], self.TIMESTAMP_FORMAT)

                # Iterate across all log entries in this sub window (or gracefully handle when we run out of data)
                while nextTimestamp < endSubWindowTimestamp and dataIndex < len(data):
                    subWindowData.append(data[dataIndex])

                    dataIndex += 1
                    if dataIndex < len(data):
                        nextTimestamp = datetime.strptime(data[dataIndex]['EVENT_TIME'], self.TIMESTAMP_FORMAT)

                windowData.append(subWindowData)
                subWindowIndex += 1

                endSubWindowTimestamp += self.windowDelta

            windowedLogData.append(windowData)

        return windowedLogData
