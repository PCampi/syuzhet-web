"""Test for the lemmatization module."""
import unittest
import treetaggerwrapper as ttw

from ..persistence import configuration_manager
from .splitting import TextSplitter
from .lemmatization import Lemmatizer


class LemmatizerUnitTest(unittest.TestCase):
    """Unit test case for the `Syuzhet` module."""

    @classmethod
    def setUpClass(cls):
        super(LemmatizerUnitTest, cls).setUpClass()
        cmgr = configuration_manager.ConfigurationManager("config.json")
        cmgr.load_config()

        cls.language = cmgr.get_default_language()
        cls.emo_arr_len = cmgr.get_emotion_array_length()
        cls.emo_names = cmgr.get_emotion_names()
        cls.treetagger_dir = cmgr.get_treetagger_path()
        taglang = cls.language.lower()[0:2]

        cls.tagger = ttw.TreeTagger(TAGLANG=taglang,
                                    TAGDIR=cls.treetagger_dir)

        cls.splitter = TextSplitter('italian')
        cls.lemmatizer = Lemmatizer(cls.tagger)

    def test_lemmatize(self):
        """Test for the `lemmatize` function."""
        text = "Ho perso il mio anello di matrimonio. Sono distrutta."

        sentences_list = self.splitter.text_to_sentences(text)
        sentences = [self.splitter.sentence_to_words(s)
                     for s in sentences_list]

        result = [self.lemmatizer.lemmatize(s) for s in sentences]
        expected_result = [['avere', 'perdere', 'il', 'mio', 'anello',
                            'di', 'matrimonio', '.'],
                           ['essere', 'distruggere', '.']]

        self.assertEqual(result, expected_result,
                         "Lemmatization results differ.")
