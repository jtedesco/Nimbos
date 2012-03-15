from json import load
import os
import unittest
from src.parser import IntrepidRASParser, Util

__author__ = 'jon'

class IntrepidRASParserTest(unittest.TestCase):
    """
      Unit tests for the IntrepidRASParser class
    """

    def setUp(self):
        """
          Setup before each test, creating a new parser
        """

        self.projectRoot = os.environ['PROJECT_ROOT']


    def testParseEmpty(self):
        """
          Test that parsing an empty log results in empty summarized and log data
        """

        logPath = self.projectRoot + '/test/parser/intrepid/log/SampleEmptyLog'

        parsedData = IntrepidRASParser.parse(logPath)
        summarizedData = Util.summary(parsedData)

        self.assertEqual([], parsedData)
        self.assertEqual({}, summarizedData)


    def testParseInvalid(self):
        """
          Test that parsing an invalid log results in empty summarized and log data
        """

        logPath = self.projectRoot + '/test/parser/intrepid/log/SampleInvalidLog'

        parsedData = IntrepidRASParser.parse(logPath)
        summarizedData = Util.summary(parsedData)

        self.assertEqual([], parsedData)
        self.assertEqual({}, summarizedData)


    def testParseValidLog(self):
        """
          Test that parsing the 'SampleLog' file results in the expected log data
        """

        # Setup
        expectedSummarizedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedSummarizedLog.json'))
        expectedParsedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedParsedLog.json'))
        logPath = self.projectRoot + '/test/parser/intrepid/log/SampleLog'
        self.maxDiff = 2000

        # Test
        parsedLog = IntrepidRASParser.parse(logPath)
        summarizedLog = Util.summary(parsedLog)

        # Verify
        self.assertEqual(expectedParsedLog, parsedLog)
        self.assertEqual(expectedSummarizedLog, summarizedLog)

    def testRegressionTestEmptyFields(self):
        """
            Test the case where an row with fields missing is still captured correctly
        """

        #Setup
        expectedSummarizedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedSummarizedLog-Regression1.json'))
        expectedParsedLog = load(open(self.projectRoot + '/test/parser/intrepid/json/ExpectedParsedLog-Regression1.json'))
        logPath = self.projectRoot + '/test/parser/intrepid/log/SampleLog-Regression1'
        self.maxDiff = 2000

        #Test
        parsedLog = IntrepidRASParser.parse(logPath)

        self.assertEqual(expectedParsedLog, parsedLog)

if __name__ == '__main__':
    unittest.main()
