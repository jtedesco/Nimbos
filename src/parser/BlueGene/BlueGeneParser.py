import os
from src.parser import RegexParser

__author__ = 'Roman'

def parse(logFilePath):
    """
        Parses Blue Gene Logs, found here: http://www.cs.sandia.gov/~jrstear/logs/
    """
    logKeys = [
        ('CAT', "\w+|-"),
        ('UTIME', "\d+"),
        ('DATE', "[\d.]+"),
        ('SOURCE', "\S+"),
        ('EVENT_TIME', "[\d.-]+"),
        ('SOURCE2', "\S+"),
        ('FIELD1', "\w+"),
        ('FIELD2', "\w+"),
        ('SEVERITY', "\w+"),
        ('MESSAGE', ".*")
    ]

    def input():
        """
            The input to parse. Note that we do not want to strip the lines
        """
        with open(logFilePath, "rb") as logFile:
            for line in logFile:
                yield line

    return RegexParser.parseInput(input(), logKeys)

if __name__ == '__main__':
    projectRoot = os.environ['PROJECT_ROOT']
    log = parse(projectRoot + '/log/bgl.log')
    print len(log)