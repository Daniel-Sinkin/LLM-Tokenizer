"""Holds constants for the project."""

from dataclasses import dataclass


@dataclass
class FOLDERS:
    """Holds folder information based on root directory"""

    ROOT = "."
    DATA = "data"


@dataclass
class FILES:
    """Holds file names."""

    SHAKESPEARE = "shakespeare.txt"
