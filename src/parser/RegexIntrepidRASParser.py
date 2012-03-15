import os
from src.parser import RegexParser

__author__ = 'jon'
__author__ = 'roman'

def parse(logFilePath):
    """
      An example parser using the RegexParser's parse function. Please see
      IntrepidRASParser#parse for full information about the expected fields
      for the log file. This parser is not well at handling all of the
      discrepancies in the BlueGenRAS log file, please use IntrepidRASParser#parse
      instead
    """

    # Describes the order if columns in which the keys appear in the log
    logKeys = [
        ('RECID', "\d+"),
        ('MSG_ID', "\w+"),
        ('COMPONENT', "\w+"),
        ('SUBCOMPONENT', "\w+"),
        ('ERRCODE', "\w+"),
        ('SEVERITY', "\w+"),
        ('EVENT_TIME', "[0-9.-]+"),
        ('FLAGS', "[ -]"),
        ('PROCESSOR', "\w+"),
        ('NODE', "[ -]"),
        ('BLOCK', "[a-zA-Z0-9_-]+"),
        ('LOCATION', "[a-zA-Z0-9_-]+"),
        ('SERIALNUMBER', "[0-9A-Z]+"),
        ('ECID', "[0-9A-Za-z']+| "),
        ('MESSAGE', ".+")
    ]
    return RegexParser.parse(logFilePath, logKeys, skipFirstLines=4)

if __name__ == '__main__':
    projectRoot = os.environ['PROJECT_ROOT']
    log = parse(projectRoot + '/log/BlueGeneRAS.log')
    print len(log)
    for entry in log:
        print entry
