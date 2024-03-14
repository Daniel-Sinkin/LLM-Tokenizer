"""
Tests the functionalit of the tokenizer class.
"""

from src.tokenizer import Tokenizer


def test_tokenizer_training_encoding() -> None:
    """
    After testing we return an encoded string, this tests that this string
    is the same as the one returned by the encode_string method.
    """
    for training_text in ["aaaaabab", "abababab"]:
        tokenizer = Tokenizer()
        encoded_training_text: list[int] = tokenizer.train(training_text)
        assert encoded_training_text == tokenizer.encode_string(training_text)


# @RFI: It would be better to have a general encode with alphabet map function
#       and have the tokenizer invoke it, that would allow us to test the
#       encoding functionality independent of training.
#       We can already pass an already trained alphabet into the tokenizer
#       so it might not be worth it.
def test_tokenizer_encode() -> None:
    """Tests if encoding works on a simple string."""
    tokenizer = Tokenizer()
    training_text = "aaaaabab"
    encoded_training_data: list[int] = tokenizer.train(training_text)
    Tokenizer.bytecode_to_text(encoded_training_data)

    test_cases: list[str, list[int]] = [
        ("aa", [256]),
        ("ab", [257]),
        ("aaaa", [256, 256]),
        ("abab", [257, 257]),
        ("ababa", [257, 257, 97]),
    ]

    for input_string, expected_output in test_cases:
        assert tokenizer.encode_string(input_string) == expected_output


def test_tokenizer_decode() -> None:
    """Tests if decoding works on a simple string."""
    tokenizer = Tokenizer()
    training_text = "aaaaabab"
    encoded_training_data: list[int] = tokenizer.train(training_text)
    assert training_text == Tokenizer.bytecode_to_text(
        tokenizer.decode(encoded_training_data)
    )
