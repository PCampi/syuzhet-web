"""Read the EmoLEx CSV and return a dictionary word-emotions."""

import pandas as pd
import numpy as np
import pickle

it_path = "data/EmoLex_it.pickle"
en_path = "data/EmoLex_en.pickle"


def _load_emolex_in_dataframe(emolex_path):
    """Load the EmoLex lexicon into a Pandas DataFrame.

    Returns
    -------
    pandas.DataFrame:
        a table containing a row for each word
    """
    emolex = pd.read_csv(emolex_path,
                         dtype={'Positive': np.int16,
                                'Negative': np.int16,
                                'Anger': np.int16,
                                'Anticipation': np.int16,
                                'Disgust': np.int16,
                                'Fear': np.int16,
                                'Joy': np.int16,
                                'Sadness': np.int16,
                                'Surprise': np.int16,
                                'Trust': np.int16})
    return emolex


# TODO: test che salvi in modo corretto!!!
def italian_column_to_dict(dataframe, column_name='Italian'):
    """Collapse a dataframe into a dictionary."""
    result = dict()

    i = 0
    dataframe_length = dataframe.shape[0]

    while i < dataframe_length:
        current_word = dataframe[column_name][i]
        values = dataframe.iloc[i].values[2:].astype(np.int16)

        word_emotions = [values]

        # if the next word is the same as the current one, append
        shift = 1
        while ((i + shift < dataframe_length) and
                dataframe.iloc[i + shift][column_name] == current_word):

            values_to_append = dataframe.iloc[i + shift]\
                .values[2:].astype(np.int16)
            word_emotions.append(values_to_append)
            shift = shift + 1

        result[current_word] = word_emotions
        i = i + shift

    return result


# TODO: test che salvi in modo corretto!!!
def english_column_to_dict(dataframe, column_name='English'):
    """Collapse a dataframe into a dictionary."""
    result = dict()

    i = 0
    dataframe_length = dataframe.shape[0]

    while i < dataframe_length:
        current_word = dataframe[column_name][i]
        values = dataframe.iloc[i].values[2:].astype(np.int16)

        word_emotions = [values]

        # if the next word is the same as the current one, append
        shift = 1
        while ((i + shift < dataframe_length) and
                dataframe.iloc[i + shift][column_name] == current_word):

            values_to_append = dataframe.iloc[i + shift]\
                .values[2:].astype(np.int16)
            word_emotions.append(values_to_append)
            shift = shift + 1

        result[current_word] = word_emotions
        i = i + shift

    return result


def save_emolex(emolex_dict, path):
    """Save EmoLex dictionary to a file."""
    return save_pickle_file(emolex_dict, path)


def load_emolex(path):
    """Load the EmoLex pickle file as dictionary."""
    if path == it_path or path == en_path:
        return load_pickle_file(path)
    else:
        return None


def save_pickle_file(object_to_save, path_to_file):
    """Save a pickle file."""
    with open(path_to_file, 'wb') as f:
        pickle.dump(object_to_save, f)


def load_pickle_file(path_to_file):
    """Load a pickle file."""
    with open(path_to_file, 'rb') as f:
        result = pickle.load(f)

    return result
