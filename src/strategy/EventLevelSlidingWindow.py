from datetime import timedelta
import os
import subprocess
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

    def __init__(self, windowDelta=timedelta(hours=5), numberOfSubWindows=5, severities=None, severityKeyword=None,
                 trainingFileName='trainingFile', modelFileName='modelFile', svmLightPath='/opt/svm-light/'):
        super(EventLevelSlidingWindow, self).__init__(windowDelta, numberOfSubWindows)

        self.severities = severities or ['INFO', 'WARN', 'ERROR', 'FATAL']
        self.severityKey = severityKeyword or 'SEVERITY'

        self.trainingFileName = trainingFileName
        self.modelFileName = modelFileName
        self.svmLightPath = svmLightPath


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


    def train(self, examples):
        """
          Trains SVM light based on the given training examples. Assumes all training examples are in the proper format.

            @param  examples    The training examples, given in the training data format, where each entry is a tuple of
                                event severity counts for each sub-window, followed by T/F based on whether or not the
                                last window had a fatal event
        """

        # Build the training file
        trainingFileContent = self.buildTrainingFileContent(examples)
        trainingFile = open(self.trainingFileName, 'w')
        trainingFile.write(trainingFileContent)
        trainingFile.close()

        # Train a model based on the training file
        subprocess.call(self.svmLightPath + 'svm_learn ' + self.trainingFileName + ' ' + self.modelFileName, shell=True)

        # Read the learned model and store the string
        modelFile = open(self.modelFileName)
        self.model = modelFile.read()
        modelFile.close()

        # Cleanup
        os.remove(self.trainingFileName)
        os.remove(self.modelFileName)


    def predict(self, features):
        # TODO: Implement me!
        super(EventLevelSlidingWindow, self).predict(features)


    def buildTrainingFileContent(self, examples):
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
