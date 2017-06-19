"""Test for the app."""
import unittest
import numpy as np
from app import make_result_dict, make_error_response, _make_sent_result
from app import emotion_names


class AppTest(unittest.TestCase):
    """Test cases for the app module."""

    def setUp(self):
        self.emo_names = ['Positivo', 'Negativo',
                          'Rabbia', 'Anticipazione',
                          'Disgusto', 'Paura',
                          'Gioia', 'Tristezza',
                          'Sorpresa', 'Fiducia']

    def test_make_result_dict_new_version(self):
        """Test that the version with dict comprehension works."""
        data = [0, 1, 0, 0, 1, 1, 0, 1]
        res_dict = make_result_dict(data)
        expected_result = {'result': data}

        self.assertEqual(res_dict, expected_result,
                         "Results differ.")

    def test_make_result_dict(self):
        """Test that the version with dict comprehension works."""
        data = [0, 1, 0, 0, 1, 1, 0, 1]
        req_id = 13
        corp = "Corpus name"
        doc = 17
        emos = ["Rabbia", "Paura", "Gioia", "Fiducia"]

        res_dict = make_result_dict(data,
                                    request_id=req_id,
                                    corpus=corp,
                                    document=doc,
                                    emo_names=emos)

        expected_result = {'result': data,
                           'id': req_id,
                           'corpus': corp,
                           'document': doc,
                           'emotion_names': emos}

        self.assertEqual(res_dict, expected_result,
                         "Results differ.")

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

    def test__make_sent_result(self):
        """Test the `_make_sent_result` function."""
        sentences = [np.array([0, 1, 0, 0, 1, 1, 1, 0]),
                     np.array([1, 1, 0, 0, 0, 1, 0, 1])]

        expected_result = {emotion_names[0]: [0, 1],
                           emotion_names[1]: [1, 1],
                           emotion_names[2]: [0, 0],
                           emotion_names[3]: [0, 0],
                           emotion_names[4]: [1, 0],
                           emotion_names[5]: [1, 1],
                           emotion_names[6]: [1, 0],
                           emotion_names[7]: [0, 1]}

        computed = _make_sent_result(sentences)

        self.assertEqual(expected_result, computed, "Results differ.")

    def test__make_sent_result_empty_input(self):
        """Test with empty input."""
        sentences = []
        expected = None
        computed = _make_sent_result(sentences)

        self.assertEqual(expected, computed)

        sentences = None
        computed = _make_sent_result(sentences)

        self.assertEqual(expected, computed)
