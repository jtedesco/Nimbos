import os
import re
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

    LOG_FILENAME = 'BlueGeneRAS.log'


    def __init__(self, logFilePath=None):
        """
          Constructs the parser for the Blue Gene/P RAS log data, opening the log file and returns list of log entry
            dictionaries defined by the log format.

            @param  logFilePath The absolute path to the log file to parse
        """

        super(IntrepidRASParser, self).__init__(logFilePath)

        # The log data and summarized description, lazily created
        self.log = None
        self.logSummary = None

        # Describes the order if columns in which the keys appear in the log
        self.logKeys = [
            ('RECID', "\w+", False),
            ('MSG_ID', "\w+", True),
            ('COMPONENT', "\w+", True),
            ('SUBCOMPONENT', "\w+", True),
            ('ERRCODE', "\w+", True),
            ('SEVERITY', "\w+", True),
            ('EVENT_TIME', "\w+", False),
            ('FLAGS', "\w+", True),
            ('PROCESSOR', "\w+", True),
            ('NODE', "\w+", True),
            ('BLOCK', "\w+", True),
            ('LOCATION', "\w+", True),
            ('SERIALNUMBER', "\w+", True),
            ('ECID', "\w+", True),
            ('MESSAGE', "[a-zA-Z0-9_ ]+", True)
        ]
        self.delim = "\s*"
        self.skipFirstLines = 2

        self.regex = ""
        for name, elem_regex, tracked in self.logKeys:
            self.regex += "(?P<" + name + ">" + elem_regex + ")" + self.delim

    def __parseLogData(self):
        """
          Parse the log data and summary
        """

        # Each entry is either 'None', in which case there is not really a set of possible values for the entry, or
        #   a set of all values found for that entry
        self.logSummary = {}
        for name, elem_regex, tracked in self.logKeys:
            if tracked:
                self.logSummary[name] = set([])
            else:
                self.logSummary[name] = None

        self.log = []

        #iterate over lines in file
        with open(self.logPath) as logFile:

            #skip first lines
            for i in range(self.skipFirstLines):
                logFile.readline()

            #read log data
            for line in logFile:
                m = re.search(self.regex, line.strip())

                if m is not None:
                    logEntry = m.groupdict()
                    for key, value in self.logSummary:
                        if value is not None:
                            value.add(logEntry[key])
                    self.log.append(logEntry)

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
    projectRoot = os.environ['PROJECT_ROOT']
    parser = IntrepidRASParser(projectRoot + '/log/BlueGeneRAS.log')
    summary = parser.summarize()
    log = parser.parse()
    for key in summary:
        if summary[key] is not None:
            print key + ": " + str(len(summary[key]))
    print summary['COMPONENT']
    print summary['SUBCOMPONENT']
    print summary['MSG_ID']
    print summary['ERRCODE']
