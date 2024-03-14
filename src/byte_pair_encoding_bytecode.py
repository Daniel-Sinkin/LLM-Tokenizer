"""
Functionaly equivalent to the `byte_pair_encoding` module, but implemented for
utf-8 bytecode encodings of a string.
"""

from typing import Iterator


def get_pairs_in_bytecodes(bytecodes: list[int]) -> Iterator[str]:
    """Returns an interator over the pairs of characters in the text."""
    assert isinstance(bytecodes, list)
    assert all(isinstance(bc, int) for bc in bytecodes)
    for i in range(len(bytecodes) - 1):
        yield (bytecodes[i], bytecodes[i + 1])


def get_pairs_in_bytecodes_occurence_map(bytecodes: list[int]) -> dict[str, int]:
    """Get a dictionary of pairs and their number of occurences."""
    pairs_counter: dict[tuple[int, int], int] = {}
    for pair in get_pairs_in_bytecodes(bytecodes):
        pairs_counter[pair] = pairs_counter.get(pair, 0) + 1
    return pairs_counter


# @RFI: Instead of adding them to the dict we could also track a current maximum
#       and then update it if we find a new maximum, so we don't have to
#       iterate through the entire hashmap again.
def pairs_argmax(bytecodes: list[int]) -> tuple[tuple[int, int], int]:
    """Returns the most common pair and its count in the text."""
    pairs_counter: dict[str, int] = get_pairs_in_bytecodes_occurence_map(bytecodes)
    max_: int = max(pairs_counter.values())
    # Goes through the items iterator and returns the first one that matches the condition
    _argmax: tuple[int, int] = next(
        pair for pair, count in pairs_counter.items() if count == max_
    )

    return _argmax, max_


def get_byte_pair_encoding(
    bytecodes: list[int],
) -> tuple[list[int], dict[str, tuple[int, int]]]:
    _bytecodes: list[int] = bytecodes.copy()
    argmax, argmax_count = pairs_argmax(_bytecodes)

    iteration = 0
    alphabat_map = {}
    while argmax_count > 1:
        i = 0
        while True:
            if (_bytecodes[i], _bytecodes[i + 1]) == argmax:
                alphabat_map[255 + iteration] = argmax
                _bytecodes[i] = 255 + iteration
                del _bytecodes[i + 1]

            i += 1
            if i >= len(_bytecodes) - 1:
                break
        iteration += 1

        argmax, argmax_count = pairs_argmax(_bytecodes)

    return _bytecodes, alphabat_map


def print_example() -> None:
    """Basic example for the functionality"""
    example_text = "abracadabra"
    example_bytecodes: list[int] = [int(x) for x in example_text.encode("utf-8")]
    print("".join(chr(x) for x in example_bytecodes))

    bc_encoded, alphabet = get_byte_pair_encoding(example_bytecodes)

    print("".join(chr(x) for x in bc_encoded))
    print({chr(k): (chr(v[0]), chr(v[1])) for k, v in alphabet.items()})


if __name__ == "__main__":
    print_example()
