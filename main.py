"""Main file containing some example code to test the tokenizer."""

import ujson

from src.io import get_data_shakespeare
from src.tokenizer import Tokenizer

if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokenizer.train(get_data_shakespeare())
    tokenizer.save_alphabet()
