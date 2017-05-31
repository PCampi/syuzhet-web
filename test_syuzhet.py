import pickle
import unittest
import numpy as np
import treetaggerwrapper as ttw

from configuration_manager import ConfigurationManager
from path_problem_resolver import get_absolute_path
from syuzhet import Syuzhet
from syuzhet.splitting import TextSplitter
from syuzhet.lemmatization import Lemmatizer


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

    def test_filter_func(self):
        """Test that it filters all the words which have zero emotions."""
        with open("test_data/Ragazzo da parete - cap 1.txt", "r") as f:
            text = f.read()

        sentences = [self.splitter.sentence_to_words(sentence)
                     for sentence in self.splitter.text_to_sentences(text)]

        lemmatized_sentences = [self.lemmatizer.lemmatize(s)
                                for s in sentences]
        words_in_emolex = [[w for w in sent if w in self.emolex]
                           for sent in lemmatized_sentences]
        words_with_valence = [[w for w in sent
                               if self.emotion_count_for_word(w) > 0]
                              for sent in words_in_emolex]
        result = self.analyzer.filter_sentences(lemmatized_sentences)

        self.assertEqual(words_with_valence, result,
                         "Filtered words are different.")

    def test_emotions_for_sentence(self):
        self.fail("Write test.")
        # sentence = ['amico', ',', 'avere', 'voglia', 'di', 'gelato']

    def emotion_count_for_word(self, word):
        emos = self.emolex[word]
        if len(emos) == 1:
            return np.sum(emos[0])
        else:
            is_valid = 0
            i = 0
            while i < len(emos) and is_valid == 0:
                is_valid = np.sum(emos[i])
                i = i + 1

            return is_valid
