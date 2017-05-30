import pickle
import unittest
import treetaggerwrapper as ttw

from configuration_manager import ConfigurationManager
from path_problem_resolver import get_absolute_path
from syuzhet import Syuzhet


class SyuzhetUnitTest(unittest.TestCase):
    """Unit test case for the `Syuzhet` module."""

    @classmethod
    def setUpClass(cls):
        super(SyuzhetUnitTest, cls).setUpClass()
        cmgr = ConfigurationManager("config.json")
        cmgr.load_config()

        cls.language = cmgr.get_default_language()
        cls.emo_arr_len = cmgr.get_emotion_array_length()
        cls.emo_names = cmgr.get_emotion_names()
        cls.treetagger_dir = cmgr.get_treetagger_path()
        data_dir = cmgr.get_data_dir()
        emolex_filename = cmgr.get_emolex_filename(cls.language)
        emolex_abs_path = get_absolute_path('syuzhet/' + data_dir +
                                            '/' + emolex_filename)
        taglang = cls.language.lower()[0:2]
        cls.tagger = ttw.TreeTagger(TAGLANG=taglang,
                                    TAGDIR=cls.treetagger_dir)

        with open(emolex_abs_path, 'rb') as f:
            cls.emolex = pickle.load(f)

    def setUp(self):
        """Setup before tests.
        Initialize a new Syuzhet object."""
        # to initialize a Syuzhet object I need:
        # - language -> config
        # - a treetaggerwrapper instance
        # - length of emotion array -> config
        # - emolex -> emolex_persistence

        self.analyzer = Syuzhet(self.language,
                                self.tagger,
                                self.emo_arr_len,
                                self.emolex)

    def tearDown(self):
        self.analyzer = None

    @classmethod
    def tearDownClass(cls):
        pass

    def test_emolex_value_for_word(self):
        """Test for the `_emolex_value_for_word` function."""
        self.fail("Write test.")

    def test_get_emotions_for_word(self):
        """Test for the `_get_emotions_for_word` function."""
        # self.fail("Write test.")

        for word in self.emolex:
            self.assertIn(word, self.emolex)

        test_words = ['ciao', 'come', 'stare', 'gioia', 'paura']
        for word in test_words:
            if word in self.emolex:
                self.assertIsNotNone(self.analyzer._get_emotions_for_word(
                    word),
                                     "Reporting wrong None for word {}"
                                     .format(word))
            else:
                self.assertIsNone(self.analyzer._get_emotions_for_word(word),
                                  "Reporting not None for word \"{}\""
                                  .format(word))
