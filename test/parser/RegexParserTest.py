from json import load
import os
import unittest
from src.parser import ParserUtil, RegexParser

__author__ = 'Roman'

class RegexParserTest(unittest.TestCase):
    """
      Unit tests for the RegexParser class
    """

    #sample test keys
    regexKeys = [
        ('ID', "\d+"),
        ('NAME', "\w+"),
        ('TELEPHONE', "[0-9()-]+")
    ]

    def setUp(self):
        """
          Setup before each test
        """

        self.projectRoot = os.environ['PROJECT_ROOT']

    def testParseValidLog(self):
        """
          Test that parsing the 'SampleLog' file results in the expected log data
        """

        # Setup
        expectedSummarizedLog = load(open(self.projectRoot + '/test/parser/regex/json/ExpectedSummarizedLog.json'))
        expectedParsedLog = load(open(self.projectRoot + '/test/parser/regex/json/ExpectedParsedLog.json'))
        logPath = self.projectRoot + '/test/parser/regex/log/SampleLog'
        self.maxDiff = 2000

        # Test
        parsedLog = RegexParser.parse(logPath, self.regexKeys, skipFirstLines=2)
        summarizedLog = ParserUtil.summary(parsedLog)

        # Verify
        self.assertEqual(expectedParsedLog, parsedLog)
        self.assertEqual(expectedSummarizedLog, summarizedLog)

    def testParseInvalidLog(self):
        """
            Test that parsing a log file where the regex does not match returns an empty log
        """

        #Setup
        logPath = self.projectRoot + '/test/parser/regex/log/InvalidLog'

        #Test
        parsedLog = RegexParser.parse(logPath, self.regexKeys, skipFirstLines=2)
        summarizedLog = ParserUtil.summary(parsedLog)

        #Verify
        self.assertEqual([], parsedLog)
        self.assertEqual({}, summarizedLog)