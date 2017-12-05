"""Test for the text splitting module."""
import unittest
from .text_splitting import text_to_sentences, sentence_to_words


class TextSplitterTest(unittest.TestCase):
    """Test for the splitting module."""

    @classmethod
    def setUpClass(cls):
        cls.language = "italian"


    def test_sentence_to_words(self):
        """Test for function `sentence_to_words`."""
        sent_str = "Buongiorno a tutti, sono Pietro,\
        molto lieto di conoscervi!"

        result = sentence_to_words(sent_str, language=self.language)
        expected_result = ["buongiorno", "a", "tutti", ",",
                           "sono", "pietro", ",", "molto", "lieto",
                           "di", "conoscervi", "!"]

        self.assertEqual(result, expected_result, "Results differ.")

        sentence = "Ciao, - disse il conte - come stai?"

        result = sentence_to_words(sentence, language=self.language)
        expected_result = ["ciao", ",", "-", "disse", "il", "conte", "-",
                           "come", "stai", "?"]

        self.assertEqual(result, expected_result, "Results differ")

        text = "Ho perso il mio anello di matrimonio. Sono distrutta."

        sentences = text_to_sentences(text, language=self.language)
        result = [sentence_to_words(s, language=self.language) for s in sentences]
        expected_result = [['ho', 'perso', 'il', 'mio', 'anello', 'di',
                            'matrimonio', '.'],
                           ['sono', 'distrutta', '.']]

        self.assertEqual(result, expected_result, "Results differ.")

    def test_text_to_sentences(self):
        """Test for the `text_to_sentences` function."""
        text = "Buongiorno a tutti, sono Pietro, " + \
               "molto lieto di conoscervi! Oggi mi sono alzato " + \
               "molto presto. Credo che farò così: la colazione! " + \
               "Avete del latte? No? Peccato."

        result = text_to_sentences(text, language=self.language)
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

        text = "Ciao, - disse il conte - come stai? " + \
               "Credo vossignoria stia bene, ha un bel colorito! " + \
               "Tuttavia - ritengo - sia caldo oggi. " + \
               "- Dite? Chiese lei."

        result = text_to_sentences(text, language=self.language)
        expected_result = ["Ciao, - disse il conte - come stai?",
                           "Credo vossignoria stia bene, " +
                           "ha un bel colorito!",
                           "Tuttavia - ritengo - sia caldo oggi.",
                           "- Dite?",
                           "Chiese lei."]

        self.assertEqual(result, expected_result, "Results differ.")

        text = "Ho perso il mio anello di matrimonio."

        result = text_to_sentences(text, language=self.language)
        expected_result = ['Ho perso il mio anello di matrimonio.']

        self.assertEqual(result, expected_result,
                         "Results differ.")

        text = "Ho perso il mio anello di matrimonio. Sono distrutta."
        result = text_to_sentences(text, language=self.language)
        expected_result = ["Ho perso il mio anello di matrimonio.",
                           "Sono distrutta."]

        self.assertEqual(result, expected_result,
                         "Results differ.")
