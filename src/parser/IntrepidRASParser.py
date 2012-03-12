from src.Parser import Parser

__author__ = 'jon'


class IntrepidRASParser(Parser):
    """
      Parser class for Blue Gene/P RAS log data from Intrepid. These logs are structured with the following fields
        (the number of unique entries is shown next to each field).

        RECID:          Unique identifier for the log event (~1.5 million)
        MSG_ID:         Unique identifier for the message (only 415 unique events)
        COMPONENT:      The component producing the error  (7)
        SUBCOMPONENT:   The detailed component producing the error (DDR, cache, etc) (42 total)
        ERRCODE:        The full error code (199 total)
        SEVERITY:       The severity of the event (WARN/ERROR/INFO/FATAL)
        EVENT_TIME:     The exact timestamp (to the millisecond) of the event (~1.5 million)
        BLOCK:          Unknown meaning (~31,000)
        LOCATION:       Unknown meaning (~30,000)
        SERIALNUMBER:   Believed to be the associated component's serial number (~29,000)
        ECID:           Unknown meaning (~20,000)
        MESSAGE:        Descriptive error message (~31,000)
        NODE:           The node id associated with the event? (~33,000)
        PROCESSOR:      The processor id associated with the event? (~2,600)
        FLAGS:          Unknown (~2,000)

      Expects to find the Blue Gene/P RAS log in '../../log/BlueGeneRAS.log'
    """


    def __init__(self):
        """
          Constructs the parser for the Blue Gene/P RAS log data, opening the log file and returns list of log entry
            dictionaries defined by the log format.
        """

        super(IntrepidRASParser, self).__init__()

        # The path & handle on the log file
        self.logPath = self.logDirectoryPath + '/BlueGeneRAS.log'
        self.logFile = open(self.logPath)

        # The log data and summarized description, lazily created
        self.log = None
        self.logSummary = None

        # Describes the order if columns in which the keys appear in the log
        self.logKeys = [
            'RECID',
            'MSG_ID',
            'COMPONENT',
            'SUBCOMPONENT',
            'ERRCODE',
            'SEVERITY',
            'EVENT_TIME',
            'FLAGS',
            'PROCESSOR',
            'NODE',
            'BLOCK',
            'LOCATION',
            'SERIALNUMBER',
            'ECID',
            'MESSAGE'
        ]


    def __parseLogData(self):
        """
          Parse the log data and summary
        """

        # Each entry is either 'None', in which case there is not really a set of possible values for the entry, or
        #   a set of all values found for that entry
        self.logSummary = {
            'RECID': None,
            'MSG_ID': set([]),
            'COMPONENT': set([]),
            'SUBCOMPONENT': set([]),
            'ERRCODE': set([]),
            'SEVERITY': set([]),
            'EVENT_TIME': None,
            'FLAGS': set([]),
            'PROCESSOR': set([]),
            'NODE': set([]),
            'BLOCK': set([]),
            'LOCATION': set([]),
            'SERIALNUMBER': set([]),
            'ECID': set([]),
            'MESSAGE': set([])
        }

        # Simply a list of log entries
        self.log = []

        # Read through the log file and populate the log data
        lineNumber = 0
        linesSkipped = 0
        for line in self.logFile:
            # Skip empty & header lines
            line = line.strip()
            if len(line) > 0:
                lineNumber += 1
                if lineNumber >= 3:
                    # Add each entry that we're counting
                    splitLine = line.split()

                    # Check that the first entry is an integer
                    if len(splitLine) > len(self.logKeys) and self.isNumber(splitLine[0]):
                        logEntry = {}
                        for index in xrange(0, len(self.logKeys)):
                            if index < len(self.logKeys) - 1:
                                # Add this to the summary of the log
                                if self.logSummary[self.logKeys[index]] is not None and splitLine[index] != '-':
                                    self.logSummary[self.logKeys[index]].add(splitLine[index])

                                # Add this to the log data
                                if splitLine[index] == '-':
                                    logEntry[self.logKeys[index]] = None
                                else:
                                    logEntry[self.logKeys[index]] = splitLine[index]

                            else:
                                # Join the entire message (the remaining tokens on the line) and add it
                                message = ' '.join(splitLine[index:])
                                if self.logSummary[self.logKeys[index]] is not None:
                                    self.logSummary[self.logKeys[index]].add(message)
                                logEntry[self.logKeys[index]] = message

                        self.log.append(logEntry)
                    else:
                        linesSkipped += 1

        # Convert summary to use lists rather than sets
        for key in self.logSummary:
            if self.logSummary[key] is not None:
                self.logSummary[key] = list(self.logSummary[key])


    def parse(self):
        """
          Returns a list of dictionaries, representing the entries of the parsed log
        """

        # Only build data structures if we need to
        if self.log is None:
            self.__parseLogData()

        return self.log


    def summarize(self):
        """
          Returns a dictionary describing/summarizing the log format, with the list of constants possible for each entry
            or 'None' type for entries that contain arbitrary values.
        """

        # Only build data structure if we need to
        if self.logSummary is None:
            self.__parseLogData()

        return self.logSummary


    def isNumber(self, string):
        """
          Helper function to check whether a string represents a number
        """
        try:
            float(string)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    parser = IntrepidRASParser()
    summary = parser.summarize()
    log = parser.parse()
    for key in summary:
        if summary[key] is not None:
            print key + ": " + str(len(summary[key]))
    print summary['COMPONENT']
    print summary['SUBCOMPONENT']
    print summary['MSG_ID']
    print summary['ERRCODE']
