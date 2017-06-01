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
                               if self._emotion_count_for_word(w) > 0]
                              for sent in words_in_emolex]
        result = self.analyzer.filter_sentences(lemmatized_sentences)

        self.assertEqual(words_with_valence, result,
                         "Filtered words are different.")

    def test_emotions_for_sentence1(self):
        text = "Ho perso il mio anello di matrimonio."
        result, expected_result = self._compute_emotions_for_text(text)
        self.assertListOfNdarrayEqual(result, expected_result,
                                      "Results differ")

    def test_emotions_for_sentence2(self):
        text = "Ho perso il mio anello di matrimonio. Sono distrutta."
        result, expected_result = self._compute_emotions_for_text(text)
        self.assertListOfNdarrayEqual(result, expected_result,
                                      "Computed emotions differ.")

    def test_analyze_text_compare(self):
        text1 = "Ho perso il mio anello di matrimonio."
        text2 = "Ho perso il mio anello di matrimonio. Sono distrutta."

        result1, expected_result1 = self._compute_emotions_for_text(text1)

        result2, expected_result2 = self._compute_emotions_for_text(text2)

        self.assertSumOfNdarrayListsNotEqual(result1, result2)
        self.assertSumOfNdarrayListsNotEqual(expected_result1,
                                             expected_result2)

    def _emotion_count_for_word(self, word):
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

    def _compute_emotions_for_text(self, text):
        sentences = [self.splitter.sentence_to_words(s)
                     for s in self.splitter.text_to_sentences(text)]
        lemmatized = [self.lemmatizer.lemmatize(s) for s in sentences]
        computed_result = [self.analyzer.emotions_for_sentence(s)
                           for s in lemmatized]
        expected_result = []

        for sentence in lemmatized:
            sent_result = np.zeros((10,), dtype=np.int16)
            for word in sentence:
                try:
                    emo = self.emolex[word]
                    sent_result = sent_result + emo[0]
                except KeyError:
                    pass
            expected_result.append(sent_result)

        return computed_result, expected_result

    def assertListOfNdarrayEqual(self, l1, l2, msg=""):
        """Same as assertEqual but for numpy arrays."""
        if not isinstance(l1, list):
            raise TypeError("First argument is not a list")

        if not isinstance(l2, list):
            raise TypeError("Second argument is not a list")

        self.assertEqual(len(l1), len(l2), msg +
                         " Lengths of lists are different.")

        n = len(l1)
        i = 0
        while i < n:
            self.assertEqual(l1[i].dtype, l2[i].dtype,
                             "Different dtypes at position {}".format(i))
            i = i + 1

        i = 0
        arr_equal = True
        while i < n and arr_equal:
            arr_equal = np.array_equal(l1[i], l2[i])
            i = i + 1

        if not arr_equal:
            raise AssertionError(msg +
                                 " Arrays at position {} differ".format(i - 1))

    def checkInstance(self, o, etype):
        if not isinstance(o, etype):
            raise TypeError("Expected type {}, found {}"
                            .format(str(etype), str(type(o))))

    def assertSumOfNdarrayListsNotEqual(self, l1, l2):
        """Assert that the sum of the two lists is different."""
        self.checkInstance(l1, list)
        self.checkInstance(l2, list)

        self.checkInstance(l1[0], np.ndarray)
        self.checkInstance(l2[0], np.ndarray)

        result1 = np.zeros(l1[0].shape)
        result2 = np.zeros(l2[0].shape)

        for arr in l1:
            result1 = result1 + arr

        for arr in l2:
            result2 = result2 + arr

        if np.array_equal(result1, result2):
            raise AssertionError("Results differ:\n{}\n{}"
                                 .format(result1, result2))
