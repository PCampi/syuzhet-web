import pickle
import unittest
import numpy as np
import treetaggerwrapper as ttw

from configuration_manager import ConfigurationManager
from path_problem_resolver import get_absolute_path
from syuzhet import Syuzhet
from syuzhet.splitting import TextSplitter
from syuzhet.lemmatization import Lemmatizer


class SyuzhetDisambiguationUnitTest(unittest.TestCase):
    """Unit test case for the `Syuzhet` module."""

    @classmethod
    def setUpClass(cls):
        super(SyuzhetDisambiguationUnitTest, cls).setUpClass()
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
        cls.splitter = TextSplitter(cls.language)
        taglang = cls.language.lower()[0:2]
        cls.tagger = ttw.TreeTagger(TAGLANG=taglang,
                                    TAGDIR=cls.treetagger_dir)
        cls.lemmatizer = Lemmatizer(cls.tagger)

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

    def testThatItFiltersCorrectly(self):
        """Test that the function works correctly if filter is activated."""
