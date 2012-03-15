import unittest
import os
from src.parser import Util

__author__ = 'Roman'

class UtilTest(unittest.TestCase):
    """
      Unit tests for the Util class in src.parser
    """

    def setUp(self):
        """
          Setup before each test, creating a new parser
        """

        self.projectRoot = os.environ['PROJECT_ROOT']

    def testIsNumberWithIntegers(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative integers
        """

        self.assertTrue(Util.isNumber('10'))
        self.assertTrue(Util.isNumber('-10'))
        self.assertTrue(Util.isNumber('+20'))
        self.assertTrue(Util.isNumber('-60'))


    def testIsNumberWithFloats(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative floats
        """

        self.assertTrue(Util.isNumber('1.0'))
        self.assertTrue(Util.isNumber('-1.0'))
        self.assertTrue(Util.isNumber('+2.0'))
        self.assertTrue(Util.isNumber('-6.0'))