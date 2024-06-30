import unittest
import requests

from agilecs_wordbank_service import get_response, get_random_word

class TestWordBank(unittest.TestCase):
    
    def test_random_response(self):
        self.assertEqual(get_response(), requests.get("https://agilec.cs.uh.edu/words").text)


    def test_get_random_word(self):
        wordbank = ['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD']
        self.assertIn(get_random_word(wordbank), wordbank)

    def test_get_random_word_twice(self):
        wordbank = ['FAVOR', 'SMART', 'GUIDE', 'TESTS', 'GRADE', 'BRAIN', 'SPAIN', 'SPINE', 'GRAIN', 'BOARD']
        seed = 100000
        self.assertNotEqual(get_random_word(wordbank, seed), get_random_word(wordbank, seed))
