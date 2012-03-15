from datetime import timedelta
import os
from experiments.EvaluationUtility import evaluateBinaryPredictions
from src.parser import IntrepidRASParser
from src.strategy.slidingWindow.EventLevelStrategy import EventLevelStrategy

__author__ = 'jon'

if __name__ == '__main__':
    projectRoot = os.environ['PROJECT_ROOT']

    # The experiments to run
    experiments = [
        EventLevelStrategy('BlueGeneRASPosNeg5SubWindows5Hours'),
        EventLevelStrategy('BlueGeneRASPosNeut5SubWindows5Hours', negativeLabels=False),
        EventLevelStrategy('BlueGeneRASPosNeg3SubWindows5Hours', numberOfSubWindows=3),
        EventLevelStrategy('BlueGeneRASPosNeut3SubWindows5Hours', negativeLabels=False, numberOfSubWindows=3),
        EventLevelStrategy('BlueGeneRASPosNeg7SubWindows5Hours', numberOfSubWindows=7),
        EventLevelStrategy('BlueGeneRASPosNeg5SubWindows3Hours', windowDelta=timedelta(hours=3)),
        EventLevelStrategy('BlueGeneRASPosNeg3SubWindows3Hours', numberOfSubWindows=3, windowDelta=timedelta(hours=3)),
        EventLevelStrategy('BlueGeneRASPosNeg7SubWindows3Hours', numberOfSubWindows=7, windowDelta=timedelta(hours=3)),
        EventLevelStrategy('BlueGeneRASPosNeg5SubWindows7Hours', windowDelta=timedelta(hours=7)),
        EventLevelStrategy('BlueGeneRASPosNeg3SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=3),
        EventLevelStrategy('BlueGeneRASPosNeg7SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=7),
    ]

    # The path to the log file to use
    logFilePath = projectRoot + '/log/BlueGeneRAS.log'

    # Run each experiment, only learning the model if it doesn't already exist
    for strategy in experiments:
        modelFilePath = projectRoot + '/model/' + strategy.dataSetName + ' - SVMFatalInLastWindowModel'

        # If the model hasn't been learned, learn it, otherwise just load it
        if not os.path.exists(modelFilePath):

            parsedLogData = IntrepidRASParser.parse(logFilePath)
            testData = strategy.parseData(parsedLogData)
            model = strategy.learn(testData)

            # Save model file
            modelFile = open(modelFilePath, 'w')
            modelFile.write(model)
            modelFile.close()

        else:
            strategy.loadModel(modelFilePath)


        # Gather test data & use the model to predict labels
        parsedLogData = IntrepidRASParser.parse(logFilePath)
        testData = strategy.parseData(parsedLogData)

        strategy.predict(testData)

        # Gather correct T/F labels for data
        correctLabels = []
        for testDataEntry in testData:
            correctLabels.append(testDataEntry[-1])

        # Gather T/F labels for predictions
        predictionsValues = open(strategy.predictionsOutputFileName).read().split('\n')
        predictions = []
        for predictionValue in predictionsValues:
            if len(predictionValue) > 0:
                if float(predictionValue) < 0:
                    predictions.append(False)
                else:
                    predictions.append(True)

        # Remove the predictions output file (cleanup)
        os.remove(strategy.predictionsOutputFileName)

        # Gather basic percentages & counts of performance of model
        evaluations = evaluateBinaryPredictions(correctLabels, predictions)

        # Gather stats about the prediction accuracy
        resultsOutput = "Percentages:\n"
        resultsOutput += "------------\n"
        for percentageMetric in evaluations['percentages']:
            resultsOutput += "\t%s:  %2.2f%%\n" % (percentageMetric, evaluations['percentages'][percentageMetric] * 100)
        resultsOutput += "\n"
        resultsOutput += "Raw Counts:\n"
        resultsOutput += "-----------\n"
        for countMetric in evaluations['counts']:
            resultsOutput += "\t%s:  %d\n" % (countMetric, evaluations['counts'][countMetric])

        # Dump the results for this experiment
        resultsFilePath = projectRoot + '/experiments/BlueGeneRASResults/' + strategy.dataSetName + 'Results'
        resultsFile = open(resultsFilePath, 'w')
        resultsFile.write(resultsOutput)
        resultsFile.close()

        print "Analyzed results for '%s'" % strategy.dataSetName

        # Force Python to free the memory for these items, or the program will crash
        del strategy
