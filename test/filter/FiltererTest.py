from json import load
import unittest
import os
from src.filter import Filterer

__author__ = 'Roman'

class FiltererTest(unittest.TestCase):
    """
      Unit tests for the Filterer filter method
    """

    def setUp(self):
        """
          Setup before each test, creating a new parser
        """

        self.projectRoot = os.environ['PROJECT_ROOT']

    def testAllLogsSimilar(self):
        # Setup
        mockLog = load(open(self.projectRoot + '/test/filter/parsedLog/similarLogs.json'))
        mockDictionary = set(["instruction", "cache", "parity", "error", "correct", "some", "other", "words", "and", "stuff"])
        resultLog = Filterer.filter(mockLog, mockDictionary)
        self.assertEqual(len(resultLog), 1)

    def testAllLogsSimilarButSomeSpreadAprt(self):
        mockLog = load(open(self.projectRoot + '/test/filter/parsedLog/similarLogsSpreadApart.json'))
        mockDictionary = set(["instruction", "cache", "parity", "error", "correct", "some", "other", "words", "and", "stuff"])
        resultLog = Filterer.filter(mockLog, mockDictionary)
        self.assertEqual(len(resultLog), 2)

    def testUnsimilarLogs(self):
        mockLog = load(open(self.projectRoot + '/test/filter/parsedLog/unsimilarLogs.json'))
        mockDictionary = set(["instruction", "cache", "parity", "error", "correct", "generat", "core", "NUMBER", "lN", "edram", "detect", "and", "some", "other", "words", "and", "stuff"])
        resultLog = Filterer.filter(mockLog, mockDictionary)
        self.assertEqual(len(resultLog), 3)