import unittest
import random
from helpers import AlibabaProductScraper as BB
from constant_store import uastrings as uas
from utils import logging as log

class TestScraper(unittest.TestCase):
    
    def test_rotate_UA(self):
        self.uas = uas
        result = BB.rotate_UA(self)

        self.assertIsNotNone(result)
        self.assertIn(result, uas)

        return

    def test_parse_url(self):
        ''' testing types of urls '''
        self.uas = uas

        url = 'https://google.com'
        headers = {'User-Agent': random.choice(uas)}
        result = BB.parse_url(self, url, headers)
        self.assertLogs(log,level='WARNING')
        self.assertRaises(Exception)

        url = 'alibaba.com/xyz'
        headers = {'User-Agent': random.choice(uas)}
        result = BB.parse_url(self, url, headers)
        self.assertLogs(log,level='WARNING')
        self.assertRaises(Exception)

        url = 'https://www.alibaba.com/catalog/cooking-tools_cid100004817'
        headers = {'User-Agent': random.choice(uas)}
        result = BB.parse_url(self, url, headers)
        
        # results -  tuple
        # content - bytes
        # ct - bool
        self.assertIsInstance(result, tuple)

if __name__ == "__main__":
    unittest.main() 