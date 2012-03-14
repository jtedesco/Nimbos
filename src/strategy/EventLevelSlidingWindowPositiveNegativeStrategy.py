from datetime import timedelta
import os
import subprocess
from src.strategy.SlidingWindowStrategy import SlidingWindowStrategy
from src.strategy.StrategyError import StrategyError

__author__ = 'jon'

class EventLevelSlidingWindowStrategyPositiveNegativeStrategy(SlidingWindowStrategy):
    """
      Class that holds prediction strategies based on a sliding window of log events. Specifically, this strategy
        uses SVM based on the sliding windows of intervals of several hours. Based on features of the last 4 windows,
        this will predict whether or not there will be a fatal error.
      Specifically, the features we consider in this strategy are (for each window, all of these):
        - number of INFO events
        - number of WARN events
        - number of ERROR events
        - number of FATAL events

      Note: This expects svm_learn and svm_classify to be on your path
    """

    STRATEGY_NAME = 'EventLevelSlidingWindow'

    def __init__(self, dataSetName, windowDelta=timedelta(hours=5), numberOfSubWindows=5, severities=None, severityKeyword=None):

        super(EventLevelSlidingWindowStrategyPositiveNegativeStrategy, self).__init__(windowDelta, numberOfSubWindows)

        self.severities = severities or ['INFO', 'WARN', 'ERROR', 'FATAL']
        self.severityKey = severityKeyword or 'SEVERITY'

        self.trainingFileName = dataSetName + ' - ' + EventLevelSlidingWindowStrategyPositiveNegativeStrategy.STRATEGY_NAME + 'Training'
        self.modelFileName = dataSetName + ' - ' + EventLevelSlidingWindowStrategyPositiveNegativeStrategy.STRATEGY_NAME + 'Model'
        self.predictionsInputFileName = dataSetName + ' - ' + EventLevelSlidingWindowStrategyPositiveNegativeStrategy.STRATEGY_NAME + 'PredictionsIn'
        self.predictionsOutputFileName = dataSetName + ' - ' + EventLevelSlidingWindowStrategyPositiveNegativeStrategy.STRATEGY_NAME + 'PredictionsOut'

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

                # Iterate through each sub-window, skipping the last window (since the last is used for classification)
                subWindowData = []
                for subWindowIndex in xrange(0, len(window) - 1):
                    subWindow = window[subWindowIndex]

                    # Counts the number of events of each severity
                    eventCounts = {
                        self.severities[0]: 0,
                        self.severities[1]: 0,
                        self.severities[2]: 0,
                        self.severities[3]: 0
                    }

                    for logEvent in subWindow:
                        # Fail to parse the log data if it's invalid (in that it doesn't contain the expected 'SEVERITY' field)
                        if self.severityKey not in logEvent:
                            raise  StrategyError(
                                'Error parsing windowed log data, could not find %s field!' % self.severityKey)

                        # Tally an event of this severity
                        eventCounts[logEvent[self.severityKey]] += 1

                    # Append the counts for this sub-window
                    subWindowData.append(
                        (eventCounts[self.severities[0]], eventCounts[self.severities[1]],
                         eventCounts[self.severities[2]], eventCounts[self.severities[3]]))

                # Look for 'FATAL' events in the last window
                foundFatalEvent = False
                for logEvent in window[-1]:
                    if logEvent[self.severityKey] == self.severities[3]:
                        foundFatalEvent = True
                        break

                # Add the training example
                trainingData.append(tuple(subWindowData) + (foundFatalEvent,))

            return trainingData


    def learn(self, examples):
        """
          Trains SVM light based on the given training examples. Assumes all training examples are in the proper format.

            @param  examples    The training examples, given in the training data format, where each entry is a tuple of
                                event severity counts for each sub-window, followed by T/F based on whether or not the
                                last window had a fatal event
        """

        # Throw an exception if the 'scratch' training file already exists
        if os.path.exists(self.trainingFileName):
            raise IOError('Error training EventLevelSlidingWindow strategy: %s already exists!' % self.trainingFileName)

        # Remove the model file if it already exists
        if os.path.exists(self.modelFileName):

            print "Removing SVM model file '%s'" % self.modelFileName
            os.remove(self.modelFileName)


        # Build the training file
        trainingFileContent = self.buildDataFileContent(examples)
        trainingFile = open(self.trainingFileName, 'w')
        trainingFile.write(trainingFileContent)
        trainingFile.close()

        # Train a model based on the training file
        subprocess.call('svm_learn "' + self.trainingFileName + '" "' + self.modelFileName + '"', shell=True)

        # Read the learned model and store the string
        modelFile = open(self.modelFileName)
        self.model = modelFile.read()
        modelFile.close()

        # Cleanup
        os.remove(self.trainingFileName)
        os.remove(self.modelFileName)

        # Return the model
        return self.model


    def predict(self, data):
        """
          Uses SVM light to predict the classification for the given features

            @param   data   The data entry to classify, given as a list of data entries in training example format
            @return A list of True/False, each entry representing the prediction for whether or not the next window will
                    have a FATAL error (corresponding to entries in the data)
        """

        # Throw an exception if the 'scratch' training and/or test files already exist
        if os.path.exists(self.predictionsInputFileName):
            raise IOError('Error predicting with EventLevelSlidingWindow strategy: %s already exists!' % self.predictionsInputFileName)
        if os.path.exists(self.predictionsOutputFileName):
            raise IOError('Error predicting EventLevelSlidingWindow strategy: %s already exists!' % self.predictionsOutputFileName)

        # Write the model file if it doesn't already exist
        if not os.path.exists(self.modelFileName):

            modelFile = open(self.modelFileName, 'w')
            modelFile.write(self.model)
            modelFile.close()


        # Create the predictions input file (test data)
        predictionsInputFileContent = self.buildDataFileContent(data)
        predictionsInputFile = open(self.predictionsInputFileName, 'w')
        predictionsInputFile.write(predictionsInputFileContent)
        predictionsInputFile.close()


        # Use SVM light to predict classifications for all data entries
        subprocess.call('svm_classify "' + self.predictionsInputFileName + '" "' + self.modelFileName + '" "' +
                        self.predictionsOutputFileName + '"', shell=True)

        # Cleanup
        os.remove(self.predictionsInputFileName)

        return None


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
        numberOfFeatures = (len(examples[0]) - 1) * len(examples[0][0])

        trainingFileLines = []
        for window in examples:
            # Take the counts from all sub-windows as features
            features = []
            for subWindowIndex in xrange(0, len(window) - 1):
                subWindow = window[subWindowIndex]
                for entry in subWindow:
                    features += [entry]

            # Handle the error case where
            if len(features) != numberOfFeatures:
                raise StrategyError('Error building training file content: Invalid training data!')

            # Determine whether this is a positive or negative example
            hasFatalEvent = window[len(window) - 1]
            if hasFatalEvent:
                trainingFileLine = '+1 '
            else:
                trainingFileLine = '-1 '

            # Build the text for this line of the training file
            featuresText = []
            for featureIndex in xrange(0, len(features)):
                featuresText.append('%d:%1.2f' % (featureIndex + 1, float(features[featureIndex])))

            trainingFileLine += ' '.join(featuresText)
            trainingFileLines.append(trainingFileLine)

        # Join the lines of the training file
        trainingFileContent = '\n'.join(trainingFileLines)

        return trainingFileContent
