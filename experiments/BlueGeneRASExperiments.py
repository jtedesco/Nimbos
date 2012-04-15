from datetime import timedelta
import os
from experiments.EvaluationUtility import evaluateBinaryPredictions
from src.parser.BlueGene import BlueGeneParser
from src.strategy.slidingWindow.EventLevelStrategy import EventLevelStrategy
from src.strategy.slidingWindow.RandomizedEventLevelStrategy import RandomizedEventLevelStrategy

__author__ = 'jon'

if __name__ == '__main__':
    projectRoot = os.environ['PROJECT_ROOT']

    categories = set(['-','LINKBLL', 'APPTO', 'KERNSOCK', 'MONILL', 'KERNPOW', 'KERNFLOAT', 'MASNORM', 'MONPOW', 'KERNRTSP', 'APPBUSY', 'APPSEV', 'APPCHILD', 'KERNEXT', 'KERNRTSA', 'APPRES', 'APPREAD', 'LINKPAP', 'APPUNAV', 'KERNREC', 'KERNSERV', 'MONNULL', 'MASABNORM', 'MMCS', 'KERNDTLB', 'KERNSTOR', 'KERNPROG', 'APPOUT', 'KERNTERM', 'KERNTLBE', 'LINKDISC', 'KERNMICRO', 'APPALLOC', 'KERNNOETH', 'APPTORUS', 'KERNMNT', 'KERNPAN', 'LINKIAP', 'KERNBIT', 'KERNMNTF', 'KERNMC', 'KERNCON'])

    # The experiments to run
    experiments = [
#         EventLevelStrategy('PosNeg5SubWindows5Hours-Predict-KERNRTSP', severities=categories, severityKeyword="CAT", failureValues=set(["KERNRTSP"])),
#         EventLevelStrategy('PosNeg5SubWindows5Hours-Predict-KERNMNTF', severities=categories, severityKeyword="CAT", failureValues=set(["KERNMNTF"])),
#         RandomizedEventLevelStrategy('RandomizedPosNeg5SubWindows5Hours-Predict-KERNRTSP', severities=categories, severityKeyword="CAT", failureValues=set(["KERNRTSP"])),
         EventLevelStrategy('PosNeg5SubWindows12Hours', windowDelta=timedelta(hours=12) , severities=["INFO", "WARNING", "SEVERE", "ERROR", "FATAL",  "FAILURE"], failureValues=set(["FATAL", "FAILURE"])),
#        EventLevelStrategy('PosNeg3SubWindows5Hours', numberOfSubWindows=3),
#        EventLevelStrategy('PosNeg7SubWindows5Hours', numberOfSubWindows=7),
#        EventLevelStrategy('PosNeg5SubWindows3Hours', windowDelta=timedelta(hours=3)),
#        EventLevelStrategy('PosNeg3SubWindows3Hours', numberOfSubWindows=3, windowDelta=timedelta(hours=3)),
#        EventLevelStrategy('PosNeg7SubWindows3Hours', numberOfSubWindows=7, windowDelta=timedelta(hours=3)),
#        EventLevelStrategy('PosNeg5SubWindows7Hours', windowDelta=timedelta(hours=7)),
#        EventLevelStrategy('PosNeg3SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=3),
#        EventLevelStrategy('PosNeg7SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=7),
#        RandomizedEventLevelStrategy('RandomizedPosNeg5SubWindows5Hours'),
#        RandomizedEventLevelStrategy('RandomizedPosNeg3SubWindows5Hours', numberOfSubWindows=3),
#        RandomizedEventLevelStrategy('RandomizedPosNeg7SubWindows5Hours', numberOfSubWindows=7),
#        RandomizedEventLevelStrategy('RandomizedPosNeg5SubWindows3Hours', windowDelta=timedelta(hours=3)),
#        RandomizedEventLevelStrategy('RandomizedPosNeg3SubWindows3Hours', numberOfSubWindows=3, windowDelta=timedelta(hours=3)),
#        RandomizedEventLevelStrategy('RandomizedPosNeg7SubWindows3Hours', numberOfSubWindows=7, windowDelta=timedelta(hours=3)),
#        RandomizedEventLevelStrategy('RandomizedPosNeg5SubWindows7Hours', windowDelta=timedelta(hours=7)),
#        RandomizedEventLevelStrategy('RandomizedPosNeg3SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=3),
#        RandomizedEventLevelStrategy('RandomizedPosNeg7SubWindows7Hours', windowDelta=timedelta(hours=7), numberOfSubWindows=7),
    ]

    # The path to the log file to use
    logFilePath = projectRoot + '/log/bgl.log'

    # Run each experiment, only learning the model if it doesn't already exist
    for strategy in experiments:
        modelFilePath = projectRoot + '/model/' + strategy.dataSetName + ' - SVMFatalInLastWindowModel'

        # If the model hasn't been learned, learn it, otherwise just load it
        if not os.path.exists(modelFilePath):

            parsedLogData = BlueGeneParser.parse(logFilePath)
            testData = strategy.parseData(parsedLogData)
            model = strategy.learn(testData)

            # Save model file
            modelFile = open(modelFilePath, 'w')
            modelFile.write(model)
            modelFile.close()

        else:
            strategy.loadModel(modelFilePath)


        # Gather test data & use the model to predict labels
        parsedLogData = BlueGeneParser.parse(logFilePath)
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

        print correctLabels
        # Remove the predictions output file (cleanup)
        # os.remove(strategy.predictionsOutputFileName)

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
