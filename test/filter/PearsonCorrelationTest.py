from src.filter import PearsonCorrelation

__author__ = 'Roman'

import unittest

__author__ = 'Roman'

class PearsonCorrelationTest(unittest.TestCase):
    """
      Unit tests PearsonCorrelation correlation method
    """

    def testEqualLogs(self):
        log1 = {'MESSAGE':"hello I am a log file"}
        log2 = {'MESSAGE':"hello I am a log file"}
        dictionary = set(["hello", "I", "am", "a", "log", "file", "these", "are", "some", "other", "words"])
        corr = PearsonCorrelation.correlation(log1, log2, dictionary)
        self.assertEqual(corr, 1.0)

    def testEqualUnorderedLogs(self):
        log1 = {'MESSAGE':"hello I am a log file"}
        log2 = {'MESSAGE':"I log a file hello am log file"}
        dictionary = set(["hello", "I", "am", "a", "log", "file", "these", "are", "some", "other", "words"])
        corr = PearsonCorrelation.correlation(log1, log2, dictionary)
        self.assertEqual(corr, 1.0)

    def testUnequalLogs(self):
        log1 = {'MESSAGE':"hello I am a log file"}
        log2 = {'MESSAGE':"Bobby likes ice cream"}
        dictionary = set(["hello", "I", "am", "a", "log", "file", "these", "are", "some", "other", "words", "Bobby", "likes", "ice", "cream"])
        corr = PearsonCorrelation.correlation(log1, log2, dictionary)
        self.assertLess(corr, 0.0)

    def testSomewhatSimilarLogs(self):
        log1 = {'MESSAGE':"hello I am a log file"}
        log2 = {'MESSAGE':"hello I am something else"}
        dictionary = set(["hello", "I", "am", "a", "log", "file", "these", "are", "some", "other", "words", "something", "else"])
        corr = PearsonCorrelation.correlation(log1, log2, dictionary)
        self.assertGreater(corr, 0.0)