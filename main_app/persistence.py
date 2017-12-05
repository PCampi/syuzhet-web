"""Persistency functions"""

import numpy as np
from path_problem_resolver import get_absolute_path


class PersistencyManager:
    def __init__(self):
        self.__cache_name = ""
        self.cache_time = ""

    def save_cache(self, ndarray, text_id: str):
        """Save a ndarray to disk and store the cache name."""
        self.cache_time = text_id
        self.__cache_name = "cache-" + text_id
        np.save(get_absolute_path(self.__cache_name), ndarray)

    def load_cache(self):
        """Load a ndarray from file"""
        try:
            if self.__cache_name == "":
                raise IOError("File does not exist yet!")
            return np.load(get_absolute_path(self.__cache_name) + ".npy")
        except IOError:
            raise
