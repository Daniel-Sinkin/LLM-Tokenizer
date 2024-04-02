from _collections_abc import dict_items
import json


class Vocabulary:
    def __init__(
        self,
        tokens: str | list[str] = None,
        min_freq: int = 0,
        reserved_tokens: list[str] = None,
    ):
        reserved_tokens = reserved_tokens or []
        tokens = tokens or []

        assert not any(
            token in reserved_tokens for token in tokens
        ), "Reserved Tokens and Tokens are mixed!"
        assert "<unk>" not in reserved_tokens, "<unk> is always implicitly availiable"

        token_freq_map: dict[str, int] = {}
        for t in tokens:
            token_freq_map[t] = token_freq_map.get(t, 0) + 1
        self.token_freq: list[tuple[str, int]] = sorted(
            token_freq_map.items(), key=lambda x: x[1], reverse=True
        )

        self.stoi: dict[str, int] = {"<unk>": 0}

        n_predefined: int = len(self.stoi)

        # [s]tring [t][o] [i]ndex
        self.stoi.update(
            {rt: idx + n_predefined for idx, rt in enumerate(reserved_tokens)}
        )
        self.stoi.update(
            {
                t: idx + n_predefined + len(reserved_tokens)
                for idx, t in enumerate(token_freq_map)
            }
        )

        # [i]ndex [t][o] [s]tring
        self.itos: dict[int, str] = {idx: t for t, idx in self.stoi.items()}

    def __str__(self) -> str:
        print(f"Vocabulary({json.dumps(self.itos, indent = 4)})")

    def __repr__(self) -> str:
        print(f"Vocabulary({json.dumps(self.itos, indent = 4)})")

    def __getitem__(
        self, slicer: str | int | list[str] | list[int]
    ) -> str | int | list[str] | list[int]:
        if isinstance(slicer, str):
            return self.stoi.get(slicer, self.stoi["<unk>"])
        elif isinstance(slicer, int):
            return self.itos.get(slicer, "<unk>")
        elif isinstance(slicer, list):
            return list(map(self.__getitem__, slicer))
        else:
            raise TypeError(f"{type(slicer)=} not supported as __getitem__ indicing.")

    def __len__(self) -> int:
        return len(self.itos)

    def items(self) -> dict_items[str, int]:
        return self.stoi.items()


if __name__ == "__main__":
    vocab = Vocabulary("this is the war of the worlds by h g wells.")
    vocab[vocab[["a", "1", "b", "2"]]]
