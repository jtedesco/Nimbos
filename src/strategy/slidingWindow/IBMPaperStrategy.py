from datetime import timedelta
from src.strategy.SlidingWindowClassificationStrategy import SlidingWindowClassificationStrategy
from src.strategy.StrategyError import StrategyError
from numpy import array

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

        Note that in our implementation, we assume the sub-window delta (lower-case delta) evenly divides the window delta
        (upper-case delta).
    """

    STRATEGY_NAME = 'IBMPaperStrategy'

    def __init__(self, dataSetName, windowDelta=timedelta(hours=5), numberOfSubWindows=5, subWindowIntervalDelta=timedelta(hours=1),
                 severities=None, severityKeyword=None, negativeLabels=True, failureKey=None, failureValues=None):
        """
          Creates a strategy object:
            @param  dataSetName                 The name of the data set
            @param  windowDelta                 The time delta used to divide a window into subwindows
            @param  numberOfSubWindows          The number of sub-windows in a given window
            @param  severities                  The list of event log severities
            @param  severityKeyword             The dictionary key to get an even severity
            @param  negativeLabels              Whether or not to include negative labels
        """

        super(IBMPaperStrategy, self).__init__(windowDelta, numberOfSubWindows, subWindowIntervalDelta)

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


    def parseWindowEventLevelCounts(self, window, excludeLastEntry = True):
        """
          Parses counts for event levels from the given window

            @param  window              The window to parse
            @param  excludeLastEntry    Whether or not to include the information from the last window entry
                                        (to deal with data outside the observation period)
        """


        # Maintains total severity counts for entire observation period
        observationWindowEventCounts = {}
        for key in self.severities:
            observationWindowEventCounts[key] = 0

        # Iterate through each sub-window, skipping the last window (since the last is used for classification)
        subWindowData = []
        numberToSkip = 1 if excludeLastEntry else 0
        for subWindowIndex in xrange(0, len(window) - numberToSkip):
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

        return observationWindowEventCounts, subWindowData


    def parseWindowedLogData(self, windowedLogData, intervalWindowedLogData):
        """
          Helper function to parse the windowed log data (log data properly divided into sliding windows for learning)
            into training examples. The format of the parsed data is as follows (in this order):

                - 1 tuple for each subwindow, containing the number events of each severity
                - 1 entry containing the total count of events for each event severity
                - 1 tuple for each subwindow interval (for event distribution), containing the number events of each severity
                - 1 entry containing the time since the last fatal event
                - 1 entry containing the number of occurences for each entry data phrase, corresponding to the number of occurrences in this period

            @param  windowedLogData         The log data divided into sliding window format by window length
            @param  intervalWindowedLogData The log data divided into sliding window format by sliding sub-window interval length
        """

        # Handle case of invalid windowed log data
        if windowedLogData is None or len(windowedLogData) <= 0:
            return []

        else:
            trainingData = []

            # Iterate through each window, each of which will consist of a training example
            for window, windowInterval in zip(windowedLogData, intervalWindowedLogData):

                # Check that the windows evenly divide into window intervals
                numberOfIntervalsPerWindow = float(len(windowInterval)) / len(window)
                if numberOfIntervalsPerWindow != int(numberOfIntervalsPerWindow):
                    raise StrategyError()
                else:
                    windowInterval = windowInterval[:((-1) * int(numberOfIntervalsPerWindow))] # Skip the last window (since it is not in the observation period)

                # Remove all entries from 'windowInterval' that appear in the last sub-window (outside of the observation period)
                for event in window[-1]:
                    for interval in windowInterval:
                        if event in interval:
                            interval.remove(event)


                # Throw an exception if there is 1 or 0 sub-windows in a window --  the strategy doesn't make sense
                if len(window) <= 1:
                    raise StrategyError(
                        'Error parsing windowed log data, found window with %d sub-windows!' % len(window))

                # Parse the actual windowed log data
                observationWindowEventCounts, subWindowData = self.parseWindowEventLevelCounts(window)

                # Look for 'FATAL' events in the last window
                foundFatalEvent = False
                for logEvent in window[-1]:
                    if logEvent[self.failureKey] in self.failureValues:
                        foundFatalEvent = True
                        break

                # Parse the event level counts from the sub-window intervals
                observationWindowEventCounts2, subWindowIntervalData = self.parseWindowEventLevelCounts(windowInterval, False)

                # Check that the total event level counts retrieved are consistent
                if observationWindowEventCounts != observationWindowEventCounts2:
                    raise StrategyError('Error parsing windowed data, parsing same data twice yielded different total event counts!')

                # Create tuple of event level counts for entire observation period
                observationPeriodCounts = []
                for key in self.severities:
                    observationPeriodCounts.append(observationWindowEventCounts[key])

                # Tally the number of events of each level in separate numpy arrays
                eventLevelWindowIntervalCounts = []
                for severityIndex in xrange(0, len(self.severities)):
                    thisIntervalCounts = array(list(entry[severityIndex] for entry in subWindowIntervalData))
                    eventLevelWindowIntervalCounts.append(thisIntervalCounts)

                # Calculate the mean and standard deviation of counts of each event severity level
                means = []
                standardDeviations = []
                for severityCountsArray in eventLevelWindowIntervalCounts:
                    means.append(round(severityCountsArray.mean(),2))
                    standardDeviations.append(round(severityCountsArray.std(),2))

                # Add the training example
                trainingData.append(tuple(subWindowData) + tuple(observationPeriodCounts) +(tuple(subWindowIntervalData),)
                        + (tuple(means),) + (tuple(standardDeviations),) + (foundFatalEvent,))

            # Throw an exception if no training data could be parsed
            if len(trainingData) is 0:
                raise StrategyError('Error parsing windowed log data!')

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
            featureLabel = 1

            # Recursively format the features
            self.formatFeatures(featureLabel, features, featuresText)

            trainingFileLine += ' '.join(featuresText)
            trainingFileLines.append(trainingFileLine)

        # Join the lines of the training file
        trainingFileContent = '\n'.join(trainingFileLines)

        return trainingFileContent


    def formatFeatures(self, featureLabel, features, featuresText):
        """
          Helper function to recursively format the features into the training file text

            @param  featureLabel    The feature label number
            @param  features        The features to format
            @param  featuresText    The text of the feature file so far

            @return The next feature label, following those processed in this call
        """

        for featureIndex in xrange(0, len(features)):
            feature = features[featureIndex]
            if type(feature) == type(tuple()) or type(feature) == type(list()):
                featureLabel = self.formatFeatures(featureLabel, feature, featuresText)
            else:
                featuresText.append('%d:%1.2f' % (featureLabel, float(feature)))
                featureLabel += 1
        return featureLabel
