from src.parser.IntrepidRASParser import IntrepidRASParser
from src.strategy.ComponentSlidingWindow import ComponentSlidingWindow
from src.strategy.EventLevelSlidingWindow import EventLevelSlidingWindow

__author__ = 'jon'

if __name__ == '__main__':
    # The experiments to run
    experiments = [
        (ComponentSlidingWindow(), IntrepidRASParser()),
        (EventLevelSlidingWindow(), IntrepidRASParser())
    ]

    for strategy, parser in experiments:
        # Parse logs & training data
        parsedLogData = parser.parse()
        trainingData = strategy.parseTrainingData(parsedLogData)

        # Learn a model based on the data
        strategy.train(trainingData)
        strategy.learn()

        # TODO: Evaluate strategy based on accuracy -- show accuracy plus false positives, missed failures, and correctly predicted failures
