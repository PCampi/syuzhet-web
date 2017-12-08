"""Configuration manager for the Syuzhet module."""

import platform
import json


class ConfigurationManager():
    """Manager of configuration objects."""

    def __init__(self, abs_path_to_file):
        """Init."""
        self.path_to_file = abs_path_to_file

        try:
            with open(self.path_to_file) as conf:
                self.conf_dict = json.load(conf)
        except IOError:
            print("configuration file not found at path: " + self.path_to_file)

    def load_config(self, abs_path_to_file):
        """Load the configuration file from the specified path."""
        if abs_path_to_file:
            self.path_to_file = abs_path_to_file

        try:
            with open(self.path_to_file) as conf:
                self.conf_dict = json.load(conf)
        except IOError:
            print("configuration file not found at path: " + self.path_to_file)

    def get_treetagger_path(self):
        """Get the path of the treetagger directory."""
        os_name = platform.system()

        if os_name == "Darwin":
            key = 'treetagger_dir_mac'
        elif os_name == "Linux" or os_name == "linux":
            key = 'treetagger_dir_linux'

        try:
            return self.conf_dict[key]
        except KeyError:
            raise

    def get_default_language(self):
        """Get the default language for text analysis."""
        try:
            return self.conf_dict['default_language']
        except KeyError:
            raise

    def get_secondary_language(self):
        """Get the secondary language."""
        try:
            return self.conf_dict['secondary_language']
        except Exception:
            raise

    def get_emotion_array_length(self):
        """Get the length of the emotions array."""
        try:
            return self.conf_dict['emotion_array_length']
        except Exception:
            raise

    def get_lexicon_filename(self, language):
        """Get the path of the EmoLex lexicon file for specified language."""
        if language == self.get_default_language():
            key = 'emolex_it_filename'
        elif language == self.get_secondary_language():
            key = 'emolex_en_filename'
        else:
            raise Exception("Invalid language '{}': only italian or english"
                            .format(language))

        try:
            return self.conf_dict[key]
        except Exception:
            raise

    def get_enhanced_lexicon_filename(self):
        """Get the path of the enhanced lexicon."""
        try:
            return self.conf_dict['emolex_enhanced_filename']
        except Exception:
            raise

    def get_data_dir(self):
        """Get the name of the data directory."""
        try:
            return self.conf_dict['data_dir']
        except Exception:
            raise

    def get_emotion_names(self):
        try:
            return self.conf_dict['emotion_names']
        except KeyError:
            raise
