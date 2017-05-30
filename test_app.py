"""Test for the app."""
import unittest
from app import make_result_dict, make_error_response


class AppTest(unittest.TestCase):
    """Test cases for the app module."""

    def setUp(self):
        self.emo_names = ['Positivo', 'Negativo',
                          'Rabbia', 'Anticipazione',
                          'Disgusto', 'Paura',
                          'Gioia', 'Tristezza',
                          'Sorpresa', 'Fiducia']

    def test_make_result_dict_only_data(self):
        """Test for the `make_result_dict` function."""
        data = [0, 1, 0, 0, 1, 2, 5, 0, 7, 2]
        res_dict = make_result_dict(data)
        expected_result = {'result': data}

        self.assertEqual(res_dict, expected_result,
                         "Results differ.")

    def test_make_result_dict_empty_data(self):
        """Test the `make_result_dict` function with no data input."""
        data = []
        res_dict = make_result_dict(data)
        expected_result = make_error_response("Empty analysis result.")

        self.assertEqual(res_dict, expected_result,
                         "Results differ.")

        data = None
        res_dict = make_result_dict(data)
        expected_result = make_error_response("Empty analysis result.")

        self.assertEqual(res_dict, expected_result,
                         "Results differ.")
        self.assertTrue(res_dict is not None)
