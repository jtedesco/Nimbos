import os
from datetime import datetime
from src.filter import PearsonCorrelation
from src.parser.BlueGene.BlueGeneParser import parse

__author__ = 'Roman'

def getRequiredCorrelation(seconds):
    if seconds > 20 * 60:
        return 1.0
    if seconds > 10 * 60:
        return 0.9
    if seconds > 5 * 60:
        return 0.8
    if seconds > 60:
        return 0.7
    #if seconds > 30:
    #    return 0.0
    #return -1.0
    return 0.0

def filter(log, dictionary=None):
    if dictionary == None:
        dictionary = set()
        for line in log:
            for word in line["MESSAGE"].split(" "):
                dictionary.add(word)

    TIMESTAMP_FORMAT = "%Y-%m-%d-%H.%M.%S.%f"
    result = []

    step = len(log)/1000
    percent = -0.1
    for i in xrange(0,len(log)-1):
        if i % step == 0:
            percent += 0.1
            print percent, "% complete"

        if (log[i]['CAT'] == "ignore"):
            continue
        else:
            result.append(log[i])

        logIDate = datetime.strptime(log[i]['EVENT_TIME'], TIMESTAMP_FORMAT)
        for j in xrange(i+1,len(log)-1):
            if (log[j]['CAT'] == "ignore"):
                continue

            logJDate = datetime.strptime(log[j]['EVENT_TIME'], TIMESTAMP_FORMAT)
            timeDiff = (logJDate - logIDate).total_seconds()
            if (timeDiff > 20 * 60):
                break

            requiredCorr = getRequiredCorrelation(timeDiff)
            corr = PearsonCorrelation.correlation(log[i], log[j], dictionary)
            if (corr > requiredCorr):
                log[j]['CAT'] = "ignore" # deleting this log

    return result


def main():
    projectRoot = os.environ['PROJECT_ROOT']
    log = parse(projectRoot + '/log/bg.comb')

    dictionary = set()
    for line in log:
        for word in line["MESSAGE"].split(" "):
            dictionary.add(word)

    print len(dictionary)
    print len(log)
    newLog = filter(log, dictionary)
    print len(newLog)

if __name__ == '__main__':
    main()