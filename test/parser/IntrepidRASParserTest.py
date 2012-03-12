from src.parser.IntrepidRASParser import IntrepidRASParser

__author__ = 'jon'

import unittest

class IntrepidRASParserTest(unittest.TestCase):
    """
      Unit tests for the IntrepidRASParser class
    """

    # The expected empty summarized log
    emptySummarizedLog = {
        'RECID': None,
        'MSG_ID': [],
        'COMPONENT': [],
        'SUBCOMPONENT': [],
        'ERRCODE': [],
        'SEVERITY': [],
        'EVENT_TIME': None,
        'FLAGS': [],
        'PROCESSOR': [],
        'NODE': [],
        'BLOCK': [],
        'LOCATION': [],
        'SERIALNUMBER': [],
        'ECID': [],
        'MESSAGE': []
    }


    def setUp(self):
        """
          Setup before each test, creating a new parser
        """

        self.parser = IntrepidRASParser()


    def testIsNumberWithIntegers(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative integers
        """

        self.assertTrue(self.parser.isNumber('10'))
        self.assertTrue(self.parser.isNumber('-10'))
        self.assertTrue(self.parser.isNumber('+20'))
        self.assertTrue(self.parser.isNumber('-60'))


    def testIsNumberWithFloats(self):
        """
          Test that 'isNumber' works with explicit and implicit positive and negative floats
        """

        self.assertTrue(self.parser.isNumber('1.0'))
        self.assertTrue(self.parser.isNumber('-1.0'))
        self.assertTrue(self.parser.isNumber('+2.0'))
        self.assertTrue(self.parser.isNumber('-6.0'))


    def testParseEmpty(self):
        """
          Test that parsing an empty log results in empty summarized and log data
        """

        self.parser.logFile = open('SampleEmptyLog')

        parsedData = self.parser.parse()
        summarizedData = self.parser.summarize()

        self.assertEqual(parsedData, [])
        self.assertEqual(summarizedData, IntrepidRASParserTest.emptySummarizedLog)


    def testParseInvalid(self):
        """
          Test that parsing an invalid log results in empty summarized and log data
        """

        self.parser.logFile = open('SampleInvalidLog')

        parsedData = self.parser.parse()
        summarizedData = self.parser.summarize()

        self.assertEqual(parsedData, [])
        self.assertEqual(summarizedData, IntrepidRASParserTest.emptySummarizedLog)


    def testParseValidLog(self):
        """
          Test that parsing the 'SampleLog' file results in the expected log data
        """

        # Setup
        expectedSummarizedLog = {
            'RECID': None,
            'MSG_ID': ['KERN_0802', 'KERN_0804'],
            'COMPONENT': ['KERNEL'],
            'SUBCOMPONENT': ['_bgp_unit_ddr'],
            'ERRCODE': ['_bgp_err_ddr_single_symbol_error', '_bgp_err_ddr_chipkill_error'],
            'SEVERITY': ['WARN'],
            'EVENT_TIME': None,
            'FLAGS': [],
            'PROCESSOR': ['0'],
            'NODE': [],
            'BLOCK': ['ANL-R46-M0-512', 'ANL-R20-R37-16384'],
            'LOCATION': ['R21-M0-N10-J05', 'R46-M0-N01-J33'],
            'SERIALNUMBER': ['44V3572YL12K73050CT', '44V3575YL12M80156ZH'],
            'ECID': ["x'02405004902DA518080377D308AE'", "x'02407D34C1045713100B674608A2'"],
            'MESSAGE': [
                'ECC-correctable single symbol error: DDR Controller 0, failing SDRAM address 0x00466e2a0, BPC pin ER118, transfer 0, bit 157, BPC module pin L04, compute trace MEMORY0DATA157, DRAM chip U01, DRAM pin D9.'
                ,
                'ECC-correctable chipkill error: DDR Controller 1, failing SDRAM address 0x03afb4180, chipkill location 0x008, either X8 compute DRAM chip U15 or U34.'
            ]
        }
        expectedParsedLog = [{
            'RECID': '26123930',
            'MSG_ID': 'KERN_0802',
            'COMPONENT': 'KERNEL',
            'SUBCOMPONENT': '_bgp_unit_ddr',
            'ERRCODE': '_bgp_err_ddr_single_symbol_error',
            'SEVERITY': 'WARN',
            'EVENT_TIME': '2009-01-05-00.02.51.162211',
            'FLAGS': None,
            'PROCESSOR': '0',
            'NODE': None,
            'BLOCK': 'ANL-R46-M0-512',
            'LOCATION': 'R46-M0-N01-J33',
            'SERIALNUMBER': '44V3575YL12M80156ZH',
            'ECID': "x'02405004902DA518080377D308AE'",
            'MESSAGE': 'ECC-correctable single symbol error: DDR Controller 0, failing SDRAM ' +\
                       'address 0x00466e2a0, BPC pin ER118, transfer 0, bit 157, BPC module pin L04,' +\
                       ' compute trace MEMORY0DATA157, DRAM chip U01, DRAM pin D9.'
        }, {
            'RECID': '26123943',
            'MSG_ID': 'KERN_0804',
            'COMPONENT': 'KERNEL',
            'SUBCOMPONENT': '_bgp_unit_ddr',
            'ERRCODE': '_bgp_err_ddr_chipkill_error',
            'SEVERITY': 'WARN',
            'EVENT_TIME': '2009-01-05-00.06.44.106651',
            'FLAGS': None,
            'PROCESSOR': '0',
            'NODE': None,
            'BLOCK': 'ANL-R20-R37-16384',
            'LOCATION': 'R21-M0-N10-J05',
            'SERIALNUMBER': '44V3572YL12K73050CT',
            'ECID': "x'02407D34C1045713100B674608A2'",
            'MESSAGE': 'ECC-correctable chipkill error: DDR Controller 1, failing SDRAM address 0x03afb4180, chipkill ' +\
                       'location 0x008, either X8 compute DRAM chip U15 or U34.'
        }]
        self.parser.logFile = open('SampleLog')
        self.maxDiff = 2000

        # Test
        parsedLog = self.parser.parse()
        summarizedLog = self.parser.summarize()

        # Verify
        self.assertEqual(summarizedLog, expectedSummarizedLog)
        self.assertEqual(parsedLog, expectedParsedLog)


if __name__ == '__main__':
    unittest.main()
