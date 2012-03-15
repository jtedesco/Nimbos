import os
from src.parser import TableParser

__author__ = 'Roman'

def parse(logFilePath):
    """
      Parser for Blue Gene/P RAS log data from Intrepid. These logs are structured with the following fields
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
    """

    # Describes the order if columns in which the keys appear in the log
    logKeys = [
        ('RECID', 3),
        ('MSG_ID', 12),
        ('COMPONENT', 23),
        ('SUBCOMPONENT', 40),
        ('ERRCODE', 61),
        ('SEVERITY', 102),
        ('EVENT_TIME', 111),
        ('FLAGS', 138),
        ('PROCESSOR', 159),
        ('NODE', 171),
        ('BLOCK', 173),
        ('LOCATION', 206),
        ('SERIALNUMBER', 271),
        ('ECID', 291),
        ('MESSAGE', 323)
    ]
    return TableParser.parse(logFilePath, logKeys, skipFirstLines=5)

if __name__ == '__main__':
    projectRoot = os.environ['PROJECT_ROOT']
    log = parse(projectRoot + '/log/BlueGeneRAS.log')
    print len(log)
    for entry in log:
        print entry