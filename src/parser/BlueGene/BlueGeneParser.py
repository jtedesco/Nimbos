import os
from src.parser import RegexParser, ParserUtil

__author__ = 'Roman'

def cleanse(parsed, key, values):
    ret = []
    for line in parsed:
        if line[key] in values:
            ret.append(line)
    return ret

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

    severityKeys = ["INFO", "FAILURE", "SEVERE", "WARNING", "ERROR", "FATAL"]

    def input():
        """
            The input to parse. Note that we do not want to strip the lines
        """
        with open(logFilePath, "rb") as logFile:
            for line in logFile:
                yield line

    parsed = RegexParser.parseInput(input(), logKeys)
    return cleanse(parsed, "SEVERITY", severityKeys);

def main():
    projectRoot = os.environ['PROJECT_ROOT']
    log = parse(projectRoot + '/log/bg.log')

    result = set()
    for line in log:
        for word in line["MESSAGE"].split(" "):
            result.add(word)

    print len(result)

if __name__ == '__main__':
    main()