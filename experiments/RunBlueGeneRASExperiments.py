import os
from experiments.EvaluationUtility import evaluateBinaryPredictions
from src.parser.IntrepidRASParser import IntrepidRASParser
from src.strategy.EventLevelSlidingWindow import EventLevelSlidingWindow

__author__ = 'jon'

if __name__ == '__main__':

    # Find the project root
    projectRoot = os.environ['PROJECT_ROOT']

    # The experiments to run (strategy, parser, model file name)
    experiments = [
        (EventLevelSlidingWindow('BlueGeneRAS'), IntrepidRASParser(projectRoot + '/log/BlueGeneRAS.log'), IntrepidRASParser(projectRoot + '/log/BlueGeneRAS.log'))
    ]

    # Run each experiment, only learning the model if it doesn't already exist
    for strategy, parser, testFileParser in experiments:

        # If the model file doesn't exist, train the model and save it, otherwise open the learned model
        modelFilePath = projectRoot + '/model/' + strategy.dataSetName + ' - SVMFatalInLastWindowModel'
        if not os.path.exists(modelFilePath):

            parsedLogData = parser.parse()
            testData = strategy.parseData(parsedLogData)

            model = strategy.learn(testData)

        else:
            strategy.loadModel(modelFilePath)

        parsedLogData = testFileParser.parse()
        testData = strategy.parseData(parsedLogData)

        testData = testData[:20]

        strategy.predict(testData)

        # Gather correct T/F labels for data
        correctLabels = []
        for testDataEntry in testData:
            correctLabels.append(testDataEntry[-1])

        # Gather T/F labels for predictions
        predictionsValues = open(strategy.predictionsOutputFileName).read().split('\n')
        predictions = []
        for predictionValue in predictionsValues:
            if float(predictionValue) < 0:
                predictions.append(False)
            else:
                predictions.append(True)

        os.remove(strategy.predictionsOutputFileName)

        evaluations = evaluateBinaryPredictions(correctLabels, predictions)

        # Print stats about the prediction accuracy
        print "Percentages:"
        print "------------"
        for percentage in evaluations['percentages']:
            print "\t%2.2f" % percentage
        print
        print "Raw Counts:"
        print "-----------"
        for count in evaluations['counts']:
            print "\t%d" % count