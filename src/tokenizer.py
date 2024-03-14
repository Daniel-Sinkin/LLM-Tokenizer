"""The main tokenizer class."""

from typing import Optional

from .byte_pair_encoding_bytecode import get_byte_pair_encoding


class Tokenizer:
    """
    Tokenizer class for tokenizing the input string into tokens.

    Has to either be passed an already defined byte pair encoding alphabet
    or can be trained on training data in form of a string.
    """

    def __init__(self, alphabet_map: Optional[dict[str, tuple[int, int]]] = None):
        self.alphabet_map: Optional[dict[str, tuple[int, int]]] = alphabet_map

    @staticmethod
    def text_to_bytecode(text: str) -> list[int]:
        """Converts a string to a utf-8 bytecode list."""
        return [int(x) for x in text.encode("utf-8")]

    @staticmethod
    def bytecode_to_text(bytecode: list[int]) -> str:
        """Converts a utf-8 bytecode list to a string."""
        return "".join(chr(x) for x in bytecode)

    @staticmethod
    def _validate_and_clean_training_data(training_data: list[int] | str) -> None:
        """Validates the training data and returns it as a list of integers."""
        if isinstance(training_data, str):
            training_data: list[int] = Tokenizer.text_to_bytecode(training_data)
        if not isinstance(training_data, list):
            raise TypeError("Training data has to be a string or a list of integers.")
        if not all(isinstance(bc, int) for bc in training_data):
            raise TypeError("Training data has to be a list of integers.")

        if not all(0 <= x <= 255 for x in training_data):
            raise ValueError("Ints in the list represent invalid byte values.")

        return training_data

    def remove_trained_alphabet(self) -> None:
        """Removes the already trained alphabet."""
        self.alphabet_map = None

    def is_trained(self) -> bool:
        """Whether the tokenizer has been trained, i.e. has an alphabet map."""
        return self.alphabet_map is not None

    def train(self, training_data: str | list[int]) -> list[int]:
        """
        Trains the tokenizer on the training data, i.e. defines the alphabet.

        Returns the encoded text as a list of integers.
        """
        if self.alphabet_map is not None:
            raise ValueError("Alphabet already defined.")
        training_data = Tokenizer._validate_and_clean_training_data(training_data)

        encoded_text, alphabet_map = get_byte_pair_encoding(training_data)
        self.alphabet_map = alphabet_map
        return encoded_text

    def encode_string(self, text: str) -> list[int]:
        """
        Encodes the text using the alphabet_map if the tokenizer has been trained before.

        If it hasn't then it raises a RuntimeError.
        """
        if self.alphabet_map is None:
            raise RuntimeError("Alphabet not defined.")

        bytecode: list[int] = Tokenizer.text_to_bytecode(text)
        return self.encode(bytecode)

    def encode(self, bytecode: list[int]) -> list[int]:
        """
        Encodes the bytecode using the alphabet_map if the tokenizer has been trained before.

        If it hasn't then it raises a RuntimeError.
        """
        raise NotImplementedError()

    def decode(self, bytecode: list[int]) -> list[int]:
        """
        Decodes the bytecode using the alphabet_map if the tokenizer has been trained before.

        If it hasn't then it raises a RuntimeError.
        """
        if self.alphabet_map is None:
            raise RuntimeError("Alphabet not defined.")

        _bytecode: list[int] = bytecode.copy()

        for key, val in self.alphabet_map:
            if val is not None:
                try:
                    while True:
                        idx = _bytecode.index(key)
                        _bytecode = _bytecode[:idx] + list(val) + bytecode[idx + 1 :]
                except ValueError:  # Exhausted all occurences in the list
                    pass

        return bytecode