from json import load
import os
import unittest
from src.parser import ParserUtil, TableParser

__author__ = 'Roman'

class TableParserTest(unittest.TestCase):
    """
      Unit tests for the TableParser class
    """

    #sample test keys
    tableKeys = [
        ('ID', 5),
        ('NAME', 10),
        ('TELEPHONE', 27)
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
        expectedSummarizedLog = load(open(self.projectRoot + '/test/parser/table/json/ExpectedSummarizedLog.json'))
        expectedParsedLog = load(open(self.projectRoot + '/test/parser/table/json/ExpectedParsedLog.json'))
        logPath = self.projectRoot + '/test/parser/table/log/SampleLog'
        self.maxDiff = 2000

        # Test
        parsedLog = TableParser.parse(logPath, self.tableKeys, skipFirstLines=2)
        summarizedLog = ParserUtil.summary(parsedLog)

        # Verify
        self.assertEqual(expectedParsedLog, parsedLog)
        self.assertEqual(expectedSummarizedLog, summarizedLog)