"""General IO utilities."""

import os

from .constants import FILES, FOLDERS


def get_data_shakespeare() -> str:
    """Returns the naked string of the text file."""
    file_path: str = os.path.join(FOLDERS.DATA, FILES.SHAKESPEARE)
    if not os.path.exists(file_path):
        print(
            f"Warning: {file_path} does not exist. Please run the 'get_data.sh' script to download the data."
        )
        return ""

    with open(file_path, encoding="utf-8") as f:
        _str = f.read()

    return _str


def get_data_shakespeare_processed() -> list[str]:
    """Returns a list of (nonempty) rows of theshakespeare.txt file."""
    _str = get_data_shakespeare()
    return [row for row in _str.split("\n") if row != ""]
