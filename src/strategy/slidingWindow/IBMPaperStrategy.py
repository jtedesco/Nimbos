from datetime import timedelta
from src.strategy.SlidingWindowClassificationStrategy import SlidingWindowClassificationStrategy
from src.strategy.StrategyError import StrategyError

__author__ = 'jon'

class IBMPaperStrategy(SlidingWindowClassificationStrategy):
    """
      Implementation of the prediction strategy from 'Failure Prediction in IBM Bluegene-L event logs'. This strategy
        trains an SVM to predict whether or not a fatal error would occur in the next time window. The features include:

          - Number of events of each severity that occur in each subwindow
          - Number of events accumulated over the entire observation window
          - The distribution information for failures across the observation period
          - The inter-failure times
          - Number of times each entry data phrase occurred during the current period (semantic filter)
    """

    STRATEGY_NAME = 'IBMPaperStrategy'

    def __init__(self, dataSetName, windowDelta=timedelta(hours=5), numberOfSubWindows=5, severities=None,
                 severityKeyword=None, negativeLabels=True, failureKey=None, failureValues=None):
        super(IBMPaperStrategy, self).__init__(windowDelta, numberOfSubWindows)

        self.severities = severities or ["INFO", "WARN", "ERROR", "FATAL"]
        self.severityKey = severityKeyword or 'SEVERITY'
        self.failureKey = failureKey or self.severityKey
        self.failureValues = failureValues or {"FATAL", "FAILURE"}

        self.negativeLabels = negativeLabels

        self.trainingFileName = dataSetName + ' - ' + IBMPaperStrategy.STRATEGY_NAME + 'Training'
        self.modelFileName = dataSetName + ' - ' + IBMPaperStrategy.STRATEGY_NAME + 'Model'
        self.predictionsInputFileName = dataSetName + ' - ' + IBMPaperStrategy.STRATEGY_NAME + 'PredictionsIn'
        self.predictionsOutputFileName = dataSetName + ' - ' + IBMPaperStrategy.STRATEGY_NAME + 'PredictionsOut'

        self.dataSetName = dataSetName


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

                # Maintains total severity counts for entire observation period
                observationWindowEventCounts = {}
                for key in self.severities:
                    observationWindowEventCounts[key] = 0

                # Iterate through each sub-window, skipping the last window (since the last is used for classification)
                subWindowData = []
                for subWindowIndex in xrange(0, len(window) - 1):
                    subWindow = window[subWindowIndex]

                    # Counts the number of events of each severity
                    eventCounts = {}
                    for key in self.severities:
                        eventCounts[key] = 0

                    for logEvent in subWindow:
                        # Fail to parse the log data if it's invalid (in that it doesn't contain the expected 'SEVERITY' field)
                        if self.severityKey not in logEvent:
                            raise  StrategyError(
                                'Error parsing windowed log data, could not find %s field!' % self.severityKey)

                        # Tally an event of this severity for this subwindow & the total count
                        eventCounts[logEvent[self.severityKey]] += 1
                        observationWindowEventCounts[logEvent[self.severityKey]] += 1

                    # Append the counts for this sub-window
                    supportVector = []
                    for key in self.severities:
                        supportVector.append(eventCounts[key])
                    subWindowData.append(tuple(supportVector))

                # Look for 'FATAL' events in the last window
                foundFatalEvent = False
                for logEvent in window[-1]:
                    if logEvent[self.failureKey] in self.failureValues:
                        foundFatalEvent = True
                        break

                # Create tuple of event level counts for entire observation period
                observationPeriodCounts = []
                for key in self.severities:
                    observationPeriodCounts.append(observationWindowEventCounts[key])

                # Add the training example
                trainingData.append(tuple(subWindowData) + tuple(observationPeriodCounts) + (foundFatalEvent,))

            return trainingData


    def buildDataFileContent(self, examples):
        """
          Helper function to build the content to be dumped to the training file for SVM light. Assumes all training
            examples are in the proper format.

            @param  examples    The training examples created from <code>parseWindowedLogData</code>
            @return A string representing the content to be output to the training file for SVM light
        """

        # Handle error case of no examples
        if examples is None or len(examples) <= 0:
            raise StrategyError('Error building training file content: no examples given!')

        # Get the expected number of features per example, to make sure each example has the same number
        expectedNumberOfFeatures = (len(examples[0]) - self.numberOfSubWindows) \
            + ((self.numberOfSubWindows-1) * len(examples[0][0]))
        print expectedNumberOfFeatures


        trainingFileLines = []
        for window in examples:

            # Take the counts from all sub-windows as features
            features = []
            for subWindowIndex in xrange(0, self.numberOfSubWindows):
                if subWindowIndex < len(window):
                    subWindow = window[subWindowIndex]
                    if type(subWindow) == type(tuple([])):
                        for entry in subWindow:
                            features.append(entry)

            # Take all attributes from the observation window as a whole
            for featureIndex in xrange(self.numberOfSubWindows-1, len(window)-1):
                feature = window[featureIndex]
                features.append(feature)

            print features

            # Handle the error case where
            if len(features) != expectedNumberOfFeatures:
                raise StrategyError('Error building training file content: Invalid training data!')

            # Determine whether this is a positive or negative example
            hasFatalEvent = window[len(window) - 1]
            if hasFatalEvent:
                trainingFileLine = '+1 '
            else:

                # Determine whether to label non-failure examples as negative or neutral examples
                if  self.negativeLabels:
                    trainingFileLine = '-1 '
                else:
                    trainingFileLine = '0 '

            # Build the text for this line of the training file
            featuresText = []
            for featureIndex in xrange(0, len(features)):
                featuresText.append('%d:%1.2f' % (featureIndex + 1, float(features[featureIndex])))

            trainingFileLine += ' '.join(featuresText)
            trainingFileLines.append(trainingFileLine)

        # Join the lines of the training file
        trainingFileContent = '\n'.join(trainingFileLines)

        return trainingFileContent
