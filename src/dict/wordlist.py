from pathlib import Path
import random

from game.util import strip_accents


def _loadfile(name: str) -> list[str]:
    print(f"Loading {name}...")
    path = Path(__file__).parent
    file = path / name
    with file.open(encoding="utf-8") as f:
        return [line.strip().split(",")[0] for line in f]


class WordList:
    def __init__(self) -> None:
        self._commons: list[str] = []
        self._words: list[str] = []

    def load(self) -> None:
        self._commons = _loadfile("palavras.csv")
        bad_words = set(_loadfile("negativas.txt"))
        self._commons = [word for word in self._commons if word not in bad_words]
        self._words = _loadfile("lexico.txt")

    def random(self) -> str:
        chance = random.randint(0, 100)
        n = len(self._commons)
        q = n // 4

        if chance < 50:
            return random.choice(self._commons[:q])
        if chance < 75:
            return random.choice(self._commons[q : 2 * q])
        if chance < 95:
            return random.choice(self._commons[2 * q : 3 * q])
        return random.choice(self._commons[3 * q :])

    def find(self, word: str) -> str | None:
        for w in self._words:
            if strip_accents(w) == word:
                return w
        return None
