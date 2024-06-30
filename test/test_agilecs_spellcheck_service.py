import unittest
from unittest.mock import patch
import sys

sys.path.append("src")
from agilecs_spellcheck_service import get_response, parse_response, is_spelling_correct


class TestSpellCheck(unittest.TestCase):
    def test_get_response_true(self):
        self.assertTrue(get_response("FAVOR") == "true")

    def test_get_response_false(self):
        self.assertTrue(get_response("FAVRO") == "false")

    def test_parse_value_true(self):
        self.assertTrue(parse_response("true"))

    def test_parse_value_false(self):
        self.assertFalse(parse_response("false"))

    def test_parse_value_error(self):
        self.assertRaisesRegex(ValueError, "No response found", parse_response, "")

    @patch('agilecs_spellcheck_service.get_response', return_value='true')
    @patch('agilecs_spellcheck_service.parse_response', return_value=True)
    def test_is_spelling_correct_true(self, mock_parse_response, mock_get_response):
        self.assertTrue(is_spelling_correct("FAVOR"))
        
        mock_get_response.assert_called_once_with("FAVOR")
        mock_parse_response.assert_called_once_with('true')
    
    @patch('agilecs_spellcheck_service.get_response', return_value='false')
    @patch('agilecs_spellcheck_service.parse_response', return_value=False)
    def test_is_spelling_correct_false(self, mock_parse_response, mock_get_response):
        result = is_spelling_correct("FAVRO")
        self.assertFalse(result)
        mock_get_response.assert_called_once()
        mock_parse_response.assert_called_once()

    @patch('agilecs_spellcheck_service.get_response', side_effect=Exception("Network Error"))
    def test_is_spelling_correct_exception(self, mock_get_response):
        self.assertRaisesRegex(Exception, "Network Error", is_spelling_correct, "FAVOR")
        mock_get_response.assert_called_once_with("FAVOR") 
