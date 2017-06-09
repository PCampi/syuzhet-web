"""Test for the TextSplitter class."""
import unittest
from .splitting import TextSplitter


class TextSplitterTest(unittest.TestCase):
    """Test for the `TextSplitter` class in `splitting.py`."""

    @classmethod
    def setUpClass(cls):
        cls.splitter = TextSplitter('italian')

    def test_sentence_to_words(self):
        """Test for function `sentence_to_words`."""
        sent_str = "Buongiorno a tutti, sono Pietro,\
        molto lieto di conoscervi!"

        result = self.splitter.sentence_to_words(sent_str)
        expected_result = ["buongiorno", "a", "tutti", ",",
                           "sono", "pietro", ",", "molto", "lieto",
                           "di", "conoscervi", "!"]

        self.assertEqual(result, expected_result, "Results differ.")

    def test_sentence_to_words_difficult(self):
        """Difficult test for `sentence_to_words`."""
        sentence = "Ciao, - disse il conte - come stai?"

        result = self.splitter.sentence_to_words(sentence)
        expected_result = ["ciao", ",", "-", "disse", "il", "conte", "-",
                           "come", "stai", "?"]

        self.assertEqual(result, expected_result, "Results differ")

    def test_text_to_sentences(self):
        """Test for the `text_to_sentences` function."""
        text = "Buongiorno a tutti, sono Pietro, " + \
               "molto lieto di conoscervi! Oggi mi sono alzato " + \
               "molto presto. Credo che farò così: la colazione! " + \
               "Avete del latte? No? Peccato."

        result = self.splitter.text_to_sentences(text)
        expected_result = ["Buongiorno a tutti, sono Pietro, " +
                           "molto lieto di conoscervi!",
                           "Oggi mi sono alzato molto presto.",
                           "Credo che farò così: la colazione!",
                           "Avete del latte?",
                           "No?",
                           "Peccato."]

        self.assertEqual(len(result), len(expected_result),
                         "Results length differ.")

        self.assertEqual(result, expected_result,
                         "Results differ.")

    def test_text_to_sentences_difficult(self):
        """Difficult test for `text_to_sentences`."""
        text = "Ciao, - disse il conte - come stai? " + \
               "Credo vossignoria stia bene, ha un bel colorito! " + \
               "Tuttavia - ritengo - sia caldo oggi. " + \
               "- Dite? Chiese lei."

        result = self.splitter.text_to_sentences(text)
        expected_result = ["Ciao, - disse il conte - come stai?",
                           "Credo vossignoria stia bene, " +
                           "ha un bel colorito!",
                           "Tuttavia - ritengo - sia caldo oggi.",
                           "- Dite?",
                           "Chiese lei."]

        self.assertEqual(result, expected_result, "Results differ.")

    def test_text_to_sentences_fersini(self):
        text = "Ho perso il mio anello di matrimonio."

        result = self.splitter.text_to_sentences(text)
        expected_result = ['Ho perso il mio anello di matrimonio.']

        self.assertEqual(result, expected_result,
                         "Results differ.")

        text = "Ho perso il mio anello di matrimonio. Sono distrutta."
        result = self.splitter.text_to_sentences(text)
        expected_result = ["Ho perso il mio anello di matrimonio.",
                           "Sono distrutta."]

        self.assertEqual(result, expected_result,
                         "Results differ.")

    def test_sentence_to_words_fersini(self):
        """Test with the sentence by Fersini."""
        text = "Ho perso il mio anello di matrimonio. Sono distrutta."

        sentences = self.splitter.text_to_sentences(text)
        result = [self.splitter.sentence_to_words(s)
                  for s in sentences]
        expected_result = [['ho', 'perso', 'il', 'mio', 'anello', 'di',
                           'matrimonio', '.'],
                           ['sono', 'distrutta', '.']]

        self.assertEqual(result, expected_result, "Results differ.")
