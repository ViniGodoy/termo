from enum import IntEnum, auto

from pygame import Surface, Vector2
import pygame.draw

from game.constants import BG_COLOR
from game.util import write


class LetterStates(IntEnum):
    SLOT = auto()
    KEY = auto()
    CURSOR = auto()
    TYPED = auto()
    MISPLACED = auto()
    CORRECT = auto()
    WRONG = auto()
    DISCARDED = auto()


_LetterColors: dict[int, tuple[int, int, int]] = {
    LetterStates.SLOT: (97, 84, 88),
    LetterStates.KEY: (76, 68, 70),
    LetterStates.CURSOR: (76 * 2, 68 * 2, 70 * 2),
    LetterStates.MISPLACED: (211, 173, 105),
    LetterStates.CORRECT: (58, 163, 148),
    LetterStates.WRONG: (0, 0, 0),
    LetterStates.DISCARDED: (97, 84, 88),
}

_BorderStates = [LetterStates.KEY, LetterStates.CURSOR]


class Letter:
    def __init__(self, pos: Vector2, letter: str = "") -> None:
        self.state = LetterStates.SLOT if not letter else LetterStates.KEY
        self.pos = pos
        self.letter = letter

    def paint(self, canvas: Surface) -> None:
        color = _LetterColors[self.state]
        width = 3 if self.state in _BorderStates else 0
        pygame.draw.rect(
            surface=canvas,
            color=color,
            rect=pygame.Rect(self.pos, self.dimensions),
            border_radius=15,
            width=width,
        )
        font_color = BG_COLOR if self.state == LetterStates.DISCARDED else "WHITE"
        if self.letter:
            write(
                canvas=canvas,
                pos=self.pos,
                text=self.letter.upper(),
                color=font_color,
                dimensions=self.dimensions,
            )

    @property
    def dimensions(self) -> Vector2:
        return Vector2(60, 60)

    def update(self, dt: float) -> None:
        pass
