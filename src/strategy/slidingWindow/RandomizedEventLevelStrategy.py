from random import sample
from src.strategy.slidingWindow.EventLevelStrategy import EventLevelStrategy

__author__ = 'jon'

class RandomizedEventLevelStrategy(EventLevelStrategy):
    """
      Randomized adaptation of event level sliding window strategy, where we randomly select some subset of negative
        training examples so that there an equal number of positive and negative training examples.
    """

    def parseWindowedLogData(self, windowedLogData, intervalWindowedLogData):
        """
          Parse the windowed log data, removing random entries so that the counts of positive & negative examples match
        """

        fullTrainingData = super(RandomizedEventLevelStrategy, self).parseWindowedLogData(windowedLogData)

        positiveTrainingExamples = []
        negativeTrainingExamples = []

        # Iterate through the training data, separating into positive & negative examples
        for trainingEntry in fullTrainingData:
            trainingExampleList = positiveTrainingExamples if trainingEntry[-1] else negativeTrainingExamples
            trainingExampleList.append(trainingEntry)

        # Pull out the proper number of random examples and combine it back into mixed training examples
        randomNegativeTrainingExamples = sample(negativeTrainingExamples, len(positiveTrainingExamples))
        trainingData = positiveTrainingExamples + randomNegativeTrainingExamples

        return trainingData