from enum import IntEnum, auto

from pygame import Color, Surface, Vector2
import pygame.draw

from game.constants import (
    BG_PRIMARY,
    BG_SECONDARY,
    BG_SLOT,
    BG_SUCCESS,
    BG_WRONG,
    FG_CURSOR_BORDER,
    FG_KEY_BORDER,
    FG_PRIMARY,
)
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


_LetterColors: dict[int, Color] = {
    LetterStates.SLOT: BG_SLOT,
    LetterStates.KEY: FG_KEY_BORDER,
    LetterStates.CURSOR: FG_CURSOR_BORDER,
    LetterStates.MISPLACED: BG_SECONDARY,
    LetterStates.CORRECT: BG_SUCCESS,
    LetterStates.WRONG: BG_WRONG,
    LetterStates.DISCARDED: BG_SLOT,
}

_BorderStates = [LetterStates.KEY, LetterStates.CURSOR]


class Letter:
    def __init__(self, pos: Vector2, letter: str = "") -> None:
        self._state = LetterStates.SLOT if not letter else LetterStates.KEY
        self._prev_state = self._state
        self.pos = pos
        self.letter = letter
        self._s = 0.0

    @property
    def state(self) -> LetterStates:
        return self._state

    @state.setter
    def state(self, value: LetterStates) -> None:
        self._state = value
        self._s = 0

    @property
    def dimensions(self) -> Vector2:
        return Vector2(60, 60)

    def paint(self, canvas: Surface) -> None:
        lerp_time = min(self._s, 1)
        cur_color = _LetterColors[self._state]
        prev_color = _LetterColors[self._prev_state]
        color = prev_color.lerp(cur_color, lerp_time)
        width = 3 if self._state in _BorderStates else 0
        pygame.draw.rect(
            surface=canvas,
            color=cur_color if self._state in _BorderStates else color,
            rect=pygame.Rect(self.pos, self.dimensions),
            border_radius=15,
            width=width,
        )
        font_color = (
            FG_PRIMARY.lerp(BG_PRIMARY, lerp_time)
            if self._state == LetterStates.DISCARDED
            else FG_PRIMARY
        )
        if self.letter:
            write(
                canvas=canvas,
                pos=self.pos,
                text=self.letter.upper(),
                color=font_color,
                dimensions=self.dimensions,
            )

    def update(self, dt: float) -> None:
        self._s += dt
