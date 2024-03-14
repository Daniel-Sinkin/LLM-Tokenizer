"""Unit tests for the byte pair encoding module."""

from src.byte_pair_encoding_strings import get_byte_pair_encoding


def test_get_byte_pair_encoding() -> None:
    """Unit test for the test_get_byte_pair_encoding function."""
    # Example from Wikipedia, note this is a bit different because we iterate
    # through the pairs from left to right and in the wiki article they iterate
    # in some other way.
    text: str = "aaabdaaabacab"
    encoded_text, alphabet_map = get_byte_pair_encoding(text)
    assert encoded_text == "XdXacY"
    assert set(alphabet_map.keys()) == set("abcdXYZ")
    for char in ["a", "b", "c", "d"]:
        assert alphabet_map[char] is None
    for char in ["X", "Y", "Z"]:
        assert alphabet_map[char] is not None
        assert len(alphabet_map[char]) == 2
    assert alphabet_map["Z"] == "aa"
    assert alphabet_map["Y"] == "ab"
    assert alphabet_map["X"] == "ZY"

    # Example without pairs
    text = "abcdef"
    encoded_text, alphabet_map = get_byte_pair_encoding(text)
    assert encoded_text == text
    assert set(alphabet_map.keys()) == set("abcdef")
    for char in alphabet_map:
        assert alphabet_map[char] is None
    assert len(alphabet_map) == len(text)

    # Example with only one char in the word
    pairs: list[tuple[int, str]] = [
        (2, "aa"),
        (3, "Za"),
        (4, "ZZ"),
        (5, "ZZa"),
        (6, "YZ"),
        (8, "YY"),
    ]
    for count, pair in pairs:
        text = "a" * count
        encoded_text, _ = get_byte_pair_encoding(text)
        assert encoded_text == pair
