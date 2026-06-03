from enum import IntEnum, auto

from pygame import Surface, Vector2

from game.constants import WORD_SIZE
from game.letter import Letter, LetterStates
from game.util import strip_accents


class WordStates(IntEnum):
    SLOTS = auto()
    TYPING = auto()
    REVEALED = auto()


class Word:
    def __init__(self, pos: Vector2) -> None:
        self._state = WordStates.SLOTS
        self._typed = ""
        self._letters = [Letter(pos + Vector2(65 * i, 0)) for i in range(WORD_SIZE)]

    @property
    def state(self) -> WordStates:
        return self._state

    @property
    def typed(self) -> str:
        return self._typed

    def paint(self, canvas: Surface) -> None:
        for i in range(WORD_SIZE):
            self._letters[i].paint(canvas)

    def set_typing(self) -> None:
        self._state = WordStates.TYPING
        for letter in self._letters:
            letter.letter = ""
            letter.state = LetterStates.KEY
        self._letters[0].state = LetterStates.CURSOR

    def type(self, ch: str) -> None:
        s = len(self._typed)
        if s == WORD_SIZE:
            return
        letter = self._letters[s]
        letter.letter = ch
        letter.state = LetterStates.KEY
        if s < len(self._letters) - 1:
            self._letters[s + 1].state = LetterStates.CURSOR
        self._typed += ch

    def backspace(self) -> None:
        s = len(self._typed)
        if s == 0:
            return
        letter = self._letters[s - 1]
        letter.state = LetterStates.CURSOR
        letter.letter = ""
        if s < WORD_SIZE:
            self._letters[s].state = LetterStates.KEY
        self._typed = self._typed[:-1]

    def reveal(self, word: str, correct: str) -> None:
        if len(self.typed) != WORD_SIZE:
            return

        correct_plain = strip_accents(correct)
        self._state = WordStates.REVEALED
        for i in range(WORD_SIZE):
            ch = self._typed[i]
            if ch == correct_plain[i]:
                self._letters[i].state = LetterStates.CORRECT
            elif ch in correct_plain:
                self._letters[i].state = LetterStates.MISPLACED
            else:
                self._letters[i].state = LetterStates.WRONG
            self._letters[i].letter = word[i]

    def update(self, dt: float) -> None:
        pass
