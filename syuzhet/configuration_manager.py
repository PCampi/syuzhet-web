"""Configuration manager for the Syuzhet module."""

import json
from .path_problem_resolver import get_absolute_path

config_file = "config.json"


class ConfigurationManager():
    """Manager of configuration objects."""

    def __init__(self, path_to_file=config_file):
        """Init."""
        self.path_to_file = get_absolute_path(path_to_file)
        self.conf_dict = dict()

    def load_config(self):
        """Load the configuration file from the specified path."""
        try:
            with open(self.path_to_file) as conf:
                self.conf_dict = json.load(conf)
        except IOError:
            print("configuration file not found at path: " + self.path_to_file)

    def get_treetagger_path(self):
        """Get the path of the treetagger directory."""
        try:
            return self.conf_dict['treetagger_dir']
        except KeyError as e:
            raise e

    def get_default_language(self):
        """Get the default language for text analysis."""
        try:
            return self.conf_dict['default_language']
        except KeyError as e:
            raise e

    def get_secondary_language(self):
        """Get the secondary language."""
        try:
            return self.conf_dict['secondary_language']
        except Exception as e:
            raise e

    def get_emotion_array_length(self):
        """Get the length of the emotions array."""
        try:
            return self.conf_dict['emotion_array_length']
        except Exception as e:
            raise e

    def get_emolex_path(self, language):
        """Get the path of the EmoLex lexicon file for specified language."""
        if language == self.get_default_language():
            key = 'emolex_it_path'
        elif language == self.get_secondary_language():
            key = 'emolex_en_path'
        else:
            raise Exception("Invalid language '{}': only italian or english"
                            .format(language))

        try:
            return self.conf_dict[key]
        except Exception as e:
            raise e
