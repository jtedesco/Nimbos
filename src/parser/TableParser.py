__author__ = 'Roman'

def parse(logFilePath, logKeys, skipFirstLines=0):
    with open(logFilePath, "rb") as logFile:
        return _parse(logFile, logKeys, skipFirstLines)


def _parse(input, logKeys, skipFirstLines=0):
    """
      Parses the log data, expecting that every field starts at the same index on every
      line. This is good for log files organized as a table, where the spacing between
      fields may be variable, but the beginning index of every field is always constant.

      @param logKeys a list of pairs, where in each pair, the first entry denotes the name
      of the field, and the second entry denotes which index in every line thefield begins at.
      Note that we use 0-based indices.
      @param skipFirstLines skips the first x number of lines from this log file

      @return a list of dictionaries of the log data
    """
    log = []
    lineNumber = 0

    for line in input:
        lineNumber += 1

        #skip first lines
        if lineNumber <= skipFirstLines:
            continue

        logEntry = {}

        for i in range(len(logKeys)):
            name, startIndex = logKeys[i]

            if i == len(logKeys) - 1:
                endIndex = len(line)
            else:
                endIndex = logKeys[i + 1][1]

            #if this condition occurs, the line is probably an empty line
            if endIndex > len(line):
                break

            logEntry[name] = line[startIndex:endIndex].strip()
        else:
            log.append(logEntry)

    return log