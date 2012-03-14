__author__ = 'jon'

def evaluateBinaryPredictions(correctLabels, predictions):
    """
      Utility method to evaluate the accuracy of the given predictions based on the test data

        @param  correctLabels   The list of correct True/False classifications
        @param  predictions     The list of predicted True/False classifications
    """

    if len(correctLabels) <= 0 or len(predictions) <= 0:
        raise Exception('Error evaluating binary predictions: empty correct label or prediction list!')
    elif len(correctLabels) != len(predictions):
        raise Exception('Error evaluating binary predictions: mismatched lengths for correct label & prediction lists!')

    # Tallies the possible outcomes of each prediction
    misPredictedFailures = 0
    predictedFailures = 0
    misPredictedNonFailures = 0
    predictedNonFailures = 0
    totalEvents = len(correctLabels)

    # Tally correct/incorrect predictions
    for correctLabel, prediction in zip(correctLabels, predictions):
        if correctLabel and prediction:
            predictedFailures += 1
        elif correctLabel and not prediction:
            misPredictedFailures += 1
        elif not correctLabel and not prediction:
            predictedNonFailures += 1
        else:
            misPredictedNonFailures += 1

    # Calculate interesting metrics
    totalAccuracy = float(predictedNonFailures + predictedFailures) / float(totalEvents)
    failureAccuracy = float(predictedFailures) / float(predictedFailures + misPredictedFailures)
    nonFailureAccuracy = float(predictedNonFailures) / float(predictedNonFailures + misPredictedNonFailures)
    totalFailures = misPredictedFailures + predictedFailures
    failurePercentage = float(totalFailures) / float(totalEvents)

    return {
        'percentages': {
            'totalAccuracy' : totalAccuracy,
            'failureAccuracy': failureAccuracy,
            'nonFailureAccuracy': nonFailureAccuracy,
            'failurePercentage': failurePercentage
        },
        'counts': {
            'mispredictedFailures': misPredictedFailures,
            'predictedFailures': predictedFailures,
            'misPredictedNonFailures': misPredictedNonFailures,
            'predictedNonFailures': predictedNonFailures,
            'totalFailures': totalFailures,
            'totalEvents': totalEvents,
        }
    }
