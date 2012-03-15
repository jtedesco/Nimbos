import re

__author__ = 'Roman'

def parse(logFilePath, logKeys, delim="\s+", skipFirstLines=0, warnings=False, lineWarnings=False):
    """
      Parses the log data, using regular expressions (regex) to pull out information

      @param logFilePath the full path for the log file
      @param logKeys a list of pairs, where in each pair, the first entry denotes the name
      of the field, and the second entry denotes its regular expression (regex)
      @param delim the regex for spaces between keys
      @param skipFirstLines skips the first x number of lines from this log file
      @param warnings prints warnings for skipped lines that the regular expressions could not match
      @param lineWarnings prints warnings for every line for which the regular expression did not match.
      If there are many of these, you may want to fine-tune your regular expression better.

      @return a list of dictionaries of the log data
    """

    #create regular expression
    regex_string = "^"
    for name, elem_regex in logKeys:
        if regex_string != "^":
            regex_string += delim
        regex_string += "(?P<" + name + ">" + elem_regex + ")"

    #compile regex
    regex_string += "$"
    regex = re.compile(regex_string)

    log = []
    lineNumber = 0
    skippedLines = 0

    #iterate over lines in file
    with open(logFilePath, "rb") as logFile:
        #skip first lines
        for i in range(skipFirstLines):
            lineNumber += 1
            logFile.readline()

        #read log data
        for line in logFile:
            lineNumber += 1
            m = regex.match(line.strip())

            if m is not None:
                #found a match, add to logs
                log.append(m.groupdict())

            elif warnings and len(line.strip()) > 1:
                #regex did not match this line
                skippedLines += 1
                if lineWarnings:
                    print "Warning: line", lineNumber, "skipped:"
                    print line.strip()

    if warnings and skippedLines > 0:
        print "Warning:", skippedLines, "lines skipped"

    return log