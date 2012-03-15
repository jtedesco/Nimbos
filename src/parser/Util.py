__author__ = 'Roman'


def isNumber(string):
    """
      Helper function to check whether a string represents a number
    """
    try:
        float(string)
        return True
    except ValueError:
        return False

def summary(log):
    """
        Aggregates all unique values for every key, and returns a list
         of such values.
    """
    if len(log) < 1:
        return {}

    #need to get the keys first, to make initial empty sets
    logSummary = {}
    for key in log[0].keys():
        logSummary[key] = set([])

    #add all values
    for logEntry in log:
        for key, value in logEntry.iteritems():
            logSummary[key].add(value)

    #turn sets into lists
    for key in logSummary.keys():
        logSummary[key] = list(logSummary[key])

    return logSummary