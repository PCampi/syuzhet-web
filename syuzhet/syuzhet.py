# coding: utf-8

"""Main Syuzhet module."""

from functools import reduce

import numpy as np
import treetaggerwrapper as ttw

from . import emolex_persistence
from .configuration_manager import ConfigurationManager
from . import splitting
from . import lemmatization


# get useful variables
_configuration_manager = ConfigurationManager("config.json")
_configuration_manager.load_config()

_default_language = _configuration_manager.get_default_language()
_emotions_array_length = _configuration_manager.get_emotion_array_length()
_emolex_path = _configuration_manager.get_emolex_path(_default_language)

# Import the whole lexicon into a Python dictionary
emolex = emolex_persistence.load_emolex(_emolex_path)
_tagger = ttw.TreeTagger(TAGLANG=_default_language.lower()[0:2],
                         TAGDIR=_configuration_manager.get_treetagger_path())

# import the stopwords from nltk
# try:
#     _stopwords = nltk.corpus.stopwords.words(_default_language)
# except OSError:
#     raise Exception("Stopwords not found for language \"{}\""
#                     .format(_default_language))


def get_emotions_in_text(text, ranking=False, n_emo=3,
                         language=_default_language,
                         tagger=_tagger):
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
    sentences = [splitting.sentence_to_words(sentence, language)
                 for sentence in splitting.text_to_sentences(text, language)]

    # get the lemmatized sentences
    lemmatized_sentences = [lemmatization.lemmatize(s, tagger)
                            for s in sentences]

    # filter the lemmatized sentences: only words in EmoLex
    filtered_sentences = [[w for w in filter(_filter_func, s)]
                          for s in lemmatized_sentences]

    sentence_emotions = [emotions_for_sentence(s) for s in filtered_sentences]

    result = reduce((lambda x, y: x + y), sentence_emotions)

    return {'aggregate': result, 'sentences': sentence_emotions}


def _filter_func(word):
    emotions, multiple = _emolex_value_for_word(word)
    if not multiple:
        return np.sum(emotions[0]) > 0
    else:
        has_value = False
        i = 0
        while (i < len(emotions)) and (not has_value):
            has_value = np.sum(emotions[i]) > 0
            i = i + 1

        return has_value


def emotions_for_sentence(sentence):
    """Get the emotions in a sentence.
    Parameters
    ----------
    sentence:
        a list of word tokens (String) representing the sentence
    Returns
    -------
    numpy.array
        sum of the emotions of all the words in the sentence; may be empty
    """
    # for every word in the sentence, get its emotional valence
    result = np.zeros(_emotions_array_length, dtype=np.int16)

    for word in sentence:
        emotions = _get_emotions_for_word(word)

        if (emotions is not None):
            # FIXME: disambigua valenza emotiva
            # if there is more than 1 meaning, choose with context!
            # for now, just take the first
            if (len(emotions) > 1):
                result = result + emotions[0]
            else:
                result = result + emotions[0]

    return result


def _get_emotions_for_word(word):
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
        emotions = emolex[word]
    except KeyError as e:
        pass
    finally:
        return emotions


def _emolex_value_for_word(word):
    """Get the EmoLex value of the word.

    Parameters
    ----------
    word:
        the word to search for

    Returns
    -------
    (emotions, multiple): tuple
        the row of the word in EmoLex (a row of zeroes if the word is not in
        EmoLex), and a boolean indicating if the word has multiple choices
        for the emotions array
    """
    try:
        emotions = emolex[word]
        if len(emotions) == 1:
            return (emotions, False)
        else:
            return (emotions, True)
    except KeyError as e:
        return ([np.zeros(_emotions_array_length, dtype=np.int16)], False)
