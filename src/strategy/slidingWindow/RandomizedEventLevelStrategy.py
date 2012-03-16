from src.strategy.slidingWindow.EventLevelStrategy import EventLevelStrategy

__author__ = 'jon'

class RandomizedEventLevelStrategy(EventLevelStrategy):
    """
      Randomized adaptation of event level sliding window strategy, where we randomly select some subset of negative
        training examples so that there an equal number of positive and negative training examples.
    """
