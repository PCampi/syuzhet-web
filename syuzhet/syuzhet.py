"""Main Syuzhet module."""

from functools import reduce
import numpy as np

from .splitting import TextSplitter
from .lemmatization import lemmatize


class Syuzhet():
    """Syuzhet text analyzer class."""

    def __init__(self, language, tagger, emotions_array_length, emolex):
        """Initialize the class."""
        self.language = language
        self.tagger = tagger
        self.emotions_array_length = emotions_array_length
        self.emolex = emolex
        self.splitter = TextSplitter()

    def analyze_text(self, text: str):
        """Extract emotions from a text.

        Parameters
        ----------
        text:
            the text to extract emotions from

        Returns
        -------
        numpy.array:
            the sum of all emotions found in the text
        """
        # get the sentences first
        sentences = [self.splitter.sentence_to_words(s, self.language)
                     for s in
                     self.splitter.text_to_sentences(text, self.language)]

        # get the lemmatized sentences
        lemmatized_sentences = [lemmatize(s, self.tagger)
                                for s in sentences]

        # filter the lemmatized sentences: only words in EmoLex
        filtered_sentences = [[w for w in filter(self._filter_func, s)]
                              for s in lemmatized_sentences]

        sentence_emotions = [self.emotions_for_sentence(s)
                             for s in filtered_sentences]

        result = reduce((lambda x, y: x + y), sentence_emotions).tolist()
        return {'aggregate': result,
                'sentences': [arr.tolist() for arr in sentence_emotions]}

    def emotions_for_sentence(self, sentence):
        """Get the emotions in a sentence.
        Parameters
        ----------
        sentence:
            a list of word tokens (String) representing the sentence
        Returns
        -------
        numpy.array
            sum of the emotions of all the words in the sentence;
            may be empty
        """
        # for every word in the sentence, get its emotional valence
        result = np.zeros(self.emotions_array_length, dtype=np.int16)

        for word in sentence:
            emotions = self._get_emotions_for_word(word)

            if (emotions is not None):
                # FIXME: disambigua valenza emotiva
                # if there is more than 1 meaning, choose with context!
                # for now, just take the first
                if (len(emotions) > 1):
                    result = result + emotions[0]
                else:
                    result = result + emotions[0]

        return result

    def _get_emotions_for_word(self, word):
        """Get the emotional valence of a word from EmoLex.
        Parameters
        ----------
        word:
            the word to search for
        Returns
        -------
        numpy.array:
            the row of the word in EmoLex, None if word not found
        """
        emotions = None
        try:
            emotions = self.emolex[word]
        except KeyError as e:
            pass
        finally:
            return emotions

    def _filter_func(self, word):
        emotions, multiple = self._emolex_value_for_word(word)
        if not multiple:
            return np.sum(emotions[0]) > 0
        else:
            has_value = False
            i = 0
            while (i < len(emotions)) and (not has_value):
                has_value = np.sum(emotions[i]) > 0
                i = i + 1

            return has_value

    def _emolex_value_for_word(self, word):
        """Get the EmoLex value of the word.

        Parameters
        ----------
        word:
            the word to search for

        Returns
        -------
        (emotions, multiple): tuple
            the row of the word in EmoLex (a row of zeroes if the word isn't in
            EmoLex), and a boolean indicating if the word has multiple choices
            for the emotions array
        """
        try:
            emotions = self.emolex[word]
            if len(emotions) == 1:
                return (emotions, False)
            else:
                return (emotions, True)
        except KeyError as e:
            return ([np.zeros(self.emotions_array_length, dtype=np.int16)],
                    False)


# import the stopwords from nltk
# try:
#     _stopwords = nltk.corpus.stopwords.words(_default_language)
# except OSError:
#     raise Exception("Stopwords not found for language \"{}\""
#                     .format(_default_language))
