"""Test for the main app module, because I'm sick of Postman."""

import unittest

import requests


class MainAppUnitTest(unittest.TestCase):
    """Test case for the whole app."""

    def setUp(self):
        """Executed before each test case."""
        self.url_base = "http://localhost:5000"

    def test_lemmatize(self):
        """Test for the analyze endpoint."""
        url = self.url_base + "/lemmatize"
        payload = self.input_for_lemmatize("Questo è il testo da lemmatizzare. " +
                                           "Dovresti ritornarlo con i lemmi soltanto, grazie.")
        req = requests.post(url, json=payload)
        req.raise_for_status()

        computed = req.json()
        expected = {
            "sentences": [
                ["essere", "testo", "lemmatizzare"],
                ["dovere", "ritornare", "lemma", "soltanto", "grazie"]
            ]
        }

        self.assertDictEqual(expected, computed)

    def test_lemmatize_2(self):
        """Lemmatize test with stopwords and punctuation."""
        text = "Ciao, caro amico. Io sono impegnato oggi."
        url = self.url_base + "/lemmatize"

        payload_no_stopwords = self.input_for_lemmatize(text)
        req_no_stopwords = requests.post(url, json=payload_no_stopwords)
        req_no_stopwords.raise_for_status()

        computed = req_no_stopwords.json()
        expected = {
            "sentences": [
                ["ciao", "caro", "amico"],
                ["essere", "impegnare", "oggi"]
            ]
        }

        self.assertDictEqual(expected, computed)

        payload_with_stopwords = self.input_for_lemmatize(
            text, delete_stopwords=False)
        req_with_stopwords = requests.post(url, json=payload_with_stopwords)
        req_with_stopwords.raise_for_status()

        computed = req_with_stopwords.json()
        expected = {
            "sentences": [
                ["ciao", ",", "caro", "amico", "."],
                ["io", "essere", "impegnare", "oggi", "."]
            ]
        }

        self.assertDictEqual(expected, computed)

    def input_for_lemmatize(self, text, delete_stopwords=True):
        """Prepare the body of the input."""
        return {
            "text": text,
            "delete_stopwords": delete_stopwords
        }
