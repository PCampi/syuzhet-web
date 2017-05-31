"""Lemmatization module."""

import treetaggerwrapper as ttw


class Lemmatizer():
    """Sentence lemmatizer."""

    def __init__(self, tagger):
        self.tagger = tagger

    def lemmatize(self, sentence):
        """Lemmatize a sentence using TreeTagger.

        Parameters
        ----------
        sentence: list of strings
            a sentence as a list of strings, each of which is a word

        Returns
        -------
        lemmas: list
            a list with the same length as sentence, with each word substituted
            by its lemma
        """
        raw_tags = self.tagger.tag_text(sentence, tagonly=True)
        return [tag.lemma for tag in ttw.make_tags(raw_tags)]
