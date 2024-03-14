"""
Looks at all pairs in the given string and checks which character pair appears
most often, if all pairs are unique then the algorithm terminates, otherwise
it recursively replaces that pair which is the most common by a new character
thus extending the alphabet by one character and reducing the sequence
lenght by 1/2 of the number of pars of that character.

See also https://en.wikipedia.org/wiki/Byte_pair_encoding
"""

from typing import Iterator, Optional


def get_pairs_in_string(text: str) -> Iterator[str]:
    """Returns an interator over the pairs of characters in the text."""
    assert isinstance(text, str)
    for i in range(len(text) - 1):
        yield text[i] + text[i + 1]


def get_pairs_in_string_occurence_map(text: str) -> dict[str, int]:
    """Get a dictionary of pairs and their number of occurences."""
    assert isinstance(text, str)
    pairs_counter: dict[str, int] = {}
    for pair in get_pairs_in_string(text):
        pairs_counter[pair] = pairs_counter.get(pair, 0) + 1
    return pairs_counter


# @RFI: Instead of adding them to the dict we could also track a current maximum
#       and then update it if we find a new maximum, so we don't have to
#       iterate through the entire hashmap again.
def pairs_argmax(text: str) -> tuple[str, int]:
    """Returns the most common pair and its count in the text."""
    assert isinstance(text, str)
    pairs_counter: dict[str, int] = get_pairs_in_string_occurence_map(text)
    max_: int = max(pairs_counter.values())
    # Goes through the items iterator and returns the first one that matches the condition
    argmax: str = next(pair for pair, count in pairs_counter.items() if count == max_)

    return argmax, max_


def get_byte_pair_encoding(text: str) -> tuple[str, dict[str, Optional[str]]]:
    """
    Returns the byte pair encoding of the given text and the alphabet map,
    where the alphabet map is a dictionary that maps the new characters to the
    pairs that they replaced and None for the characters that are not replaced.
    """
    # Gets the unique characters in the text
    alphabet = list(set(text))
    # The base alphabet is not derived from anything.
    alphabet_map: dict[str, Optional[str]] = {char: None for char in alphabet}

    replacement_chars: tuple[str] = ("Z", "Y", "X", "W", "V", "U")

    # @RFI: Maybe it's worth it to track the idxs of the occurences for the max
    #       so we can do an index based replacements instead of string based one.
    argmax, count = pairs_argmax(text)
    iteration = 0
    while count > 1:
        replacement_char: str = replacement_chars[iteration]
        text = text.replace(argmax, replacement_char)
        alphabet_map[replacement_char] = argmax

        alphabet += replacement_chars[iteration]

        argmax, count = pairs_argmax(text)
        iteration += 1
    return text, alphabet_map


if __name__ == "__main__":
    example_text: str = "aaabdaaabacab"
    encoded_example_text, example_alphabet_map = get_byte_pair_encoding(example_text)
    print(f"{example_text} -> {encoded_example_text}")
    print()
    print(
        "Started with sequence of length",
        len(example_text),
        f"and #alphabet = {len(set(example_text))}.",
    )
    print(
        "Got an encoded sequence of length",
        len(encoded_example_text),
        f"and #alphabet = {len(example_alphabet_map)}.",
    )
    print()
    primitives = list(set(example_text))
    print(f"{primitives=}")
    for example_char, replacement in example_alphabet_map.items():
        if replacement is not None:
            print(f"{example_char} = {replacement}")
