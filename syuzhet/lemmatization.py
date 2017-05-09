# coding: utf-8

"""Lemmatization module."""

import treetaggerwrapper as ttw


def lemmatize(sentence, tagger):
    """Lemmatize a sentence using TreeTagger.

    Parameters
    ----------
    sentence: list of strings
        a sentence represented as a list of strings, each of which is a word

    Returns
    -------
    lemmas: list
        a list with the same length as sentence, with each word substituted
        by its lemma
    """
    raw_tags = tagger.tag_text(sentence, tagonly=True)
    return [tag.lemma for tag in ttw.make_tags(raw_tags)]
