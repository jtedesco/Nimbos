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
    mispredictedFailures = 0
    predictedFailures = 0
    mispredictedNonFailures = 0
    predictedNonFailures = 0
    totalEvents = len(correctLabels)

    # Tally correct/incorrect predictions
    for correctLabel, prediction in zip(correctLabels, predictions):
        if correctLabel and prediction:
            predictedFailures += 1
        elif correctLabel and not prediction:
            mispredictedFailures += 1
        elif not correctLabel and notprediction:
            predictedNonFailures += 1
        else:
            mispredictedNonFailures += 1

    # Calculate interesting metrics
    totalAccuracy = float(predictedNonFailures + predictedFailures) / float(totalEvents)
    failureAccuracy = float(predictedFailures) / float(predictedFailures + mispredictedFailures)
    nonFailureAccuracy = float(predictedNonFailures) / float(predictedNonFailures + mispredictedNonFailures)
    totalFailures = mispredictedFailures + predictedFailures
    failurePercentage = float(totalFailures) / float(totalEvents)

    return {
        'percentages': {
            'totalAccuracy' : totalAccuracy,
            'failureAccuracy': failureAccuracy,
            'nonFailureAccuracy': nonFailureAccuracy,
            'failurePercentage': failurePercentage
        },
        'counts': {
            'mispredictedFailures': mispredictedFailures,
            'predictedFailures': predictedFailures,
            'misPredictedNonFailures': mispredictedNonFailures,
            'predictedNonFailures': predictedNonFailures,
            'totalFailures': totalFailures,
            'totalEvents': totalEvents,
        }
    }
