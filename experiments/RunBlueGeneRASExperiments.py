import os
from src.parser.IntrepidRASParser import IntrepidRASParser
from src.strategy.EventLevelSlidingWindow import EventLevelSlidingWindow

__author__ = 'jon'

if __name__ == '__main__':

    # Find the project root
    projectRoot = os.environ['PROJECT_ROOT']

    # The experiments to run (strategy, parser, model file name)
    experiments = [
        (EventLevelSlidingWindow('BlueGeneRAS'), IntrepidRASParser(projectRoot + '/log/BlueGeneRAS.log'))
    ]

    # Run each experiment, only learning the model if it doesn't already exist
    for strategy, parser in experiments:

        # If the model file doesn't exist, train the model and save it, otherwise open the learned model
        modelFilePath = projectRoot + '/' + strategy.dataSetName + ' - SVMFatalInLastWindowModel'
        if not os.path.exists(modelFilePath):

            parsedLogData = parser.parse()
            trainingData = strategy.parseTrainingData(parsedLogData)

            model = strategy.learn(trainingData)

            modelFile = open(modelFilePath, 'w')
            modelFile.write(model)
            modelFile.close()

        else:

            strategy.loadModel(modelFilePath)

        #
