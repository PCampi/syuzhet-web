import inspect
import os


def get_absolute_path(file_path):
    """Get the absolute path of the file, using the current folder as root."""
    current_file = inspect.getframeinfo(inspect.currentframe()).filename
    current_dir = os.path.dirname(os.path.abspath(current_file))

    return current_dir + "/" + file_path
