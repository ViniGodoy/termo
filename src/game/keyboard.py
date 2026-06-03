from pygame import Surface, Vector2

from game.constants import WORD_SIZE
from game.letter import Letter, LetterStates
from game.util import strip_accents


class Keyboard:
    def __init__(self, pos: Vector2) -> None:
        self._keys: dict[str, Letter] = {}
        self._create_key_line("qwertyuiop", pos)
        self._create_key_line("asdfghjkl", pos + Vector2(30, 65))
        self._create_key_line("zxcvbnm", pos + Vector2(60, 65 * 2))

    def _create_key_line(self, line: str, pos: Vector2) -> None:
        for i in range(len(line)):
            letter = line[i]
            letter_pos = Vector2(65 * i, 0)
            key = Letter(pos + letter_pos, letter)
            self._keys[letter] = key

    def paint(self, canvas: Surface) -> None:
        for letter in self._keys.values():
            letter.paint(canvas)

    def reveal(self, word: str, correct: str) -> None:
        word = strip_accents(word)
        correct = strip_accents(correct)
        for i in range(WORD_SIZE):
            ch = word[i]
            if ch == correct[i]:
                self._keys[ch].state = LetterStates.CORRECT
            elif ch in correct and self._keys[ch].state != LetterStates.CORRECT:
                self._keys[ch].state = LetterStates.MISPLACED
            elif self._keys[ch].state == LetterStates.KEY:
                self._keys[ch].state = LetterStates.DISCARDED

    def update(self, dt: float) -> None:
        pass
