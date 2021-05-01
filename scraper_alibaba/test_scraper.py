import unittest
from helpers import AlibabaProductScraper as BB
from constant_store import uastrings as uas
from utils import logging as log

class TestScraper(unittest.TestCase):
    
    def test_rotate_UA(self):
        self.uas = uas
        result = BB.rotate_UA(self)

        self.assertIsNotNone(result)
        self.assertIn(result, uas)

    def test_parse_url(self):
        ''' testing types of urls '''
        self.uas = uas

        url = 'https://google.com'
        headers = {'User-Agent': uas}
        result = BB.parse_url(self, url, headers)
        self.assertLogs(log,level='WARNING')
        self.assertRaises(Exception)

        url = 'alibaba.com/'
        headers = {'User-Agent': uas}
        result = BB.parse_url(self, url, headers)
        self.assertLogs(log,level='WARNING')
        self.assertRaises(Exception)

        url = 'https://www.alibaba.com/catalog/floor-heating-systems-parts_cid100006537'
        headers = {'User-Agent': uas}
        result = BB.parse_url(self, url, headers)
        log.info('Result: %s', result)
        log.info('Result Type: %s', type(result))
        # self.assertIsInstance(content, bytes)

if __name__ == "__main__":
    unittest.main() 