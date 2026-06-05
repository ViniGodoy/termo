import pygame
from pygame import Event, Rect, Surface, Vector2

from dict.wordlist import WordList
from game.constants import (
    ATTEMPTS,
    BG_FAIL,
    BG_SUCCESS,
    FG_PRIMARY,
    SCREEN_SIZE,
    WORD_SIZE,
)
from game.game_file import GameFile
from game.keyboard import Keyboard
from game.stats import Stats
from game.util import strip_accents, write, write_small
from game.word import Word


class GameScreen:
    def __init__(self, word_list: WordList) -> None:
        self._game_file = GameFile().load()
        self._stats = Stats(Vector2(600, 150), stats=self._game_file.stats)
        self._word_list = word_list
        self._correct = ""
        self._win = False
        self._reset()

    def _reset(self) -> None:
        self._last_word = self._correct
        self._correct = self._word_list.random()
        self._attempt = 0
        self._words = [Word(Vector2(150, 20 + 65 * (i + 1))) for i in range(ATTEMPTS)]
        self._words[0].set_typing()
        self._keyboard = Keyboard(Vector2(150, 20 + 65 * 8))
        if self._game_file.cheat:
            print(self._correct)
            self._keyboard.reveal(self._correct, self._correct)

    def paint(self, canvas: Surface) -> None:
        write(canvas, Vector2(0, 10), "TERMO", FG_PRIMARY, Vector2(SCREEN_SIZE[0], 65))
        for word in self._words:
            word.paint(canvas)
        self._keyboard.paint(canvas)
        self._stats.paint(canvas)
        if self._last_word:
            pygame.draw.rect(
                surface=canvas,
                color=BG_SUCCESS if self._win else BG_FAIL,
                rect=Rect(670, 120, 150, 30),
            )
            write_small(
                canvas=canvas,
                pos=Vector2(670, 120),
                text=f"{self._last_word.upper()}",
                dimensions=Vector2(150, 30),
            )

    def update(self, dt: float) -> None:
        for word in self._words:
            word.update(dt)
        self._keyboard.update(dt)
        self._stats.update(dt)

    def _count(self, attempt: int) -> None:
        self._stats.count(attempt)
        self._game_file.stats = self._stats.stats
        self._game_file.save()
        self._win = attempt != ATTEMPTS
        self._reset()

    def on_key_down(self, evt: Event) -> None:
        curr_word = self._words[self._attempt]
        typed = curr_word.typed
        if pygame.K_a <= evt.key <= pygame.K_z:
            curr_word.type(pygame.key.name(evt.key))
        elif evt.key == pygame.K_BACKSPACE:
            curr_word.backspace()
        elif evt.key == pygame.K_RETURN and len(typed) == WORD_SIZE:
            w = self._word_list.find(typed)
            if not w:
                return

            curr_word.reveal(w, self._correct)
            self._keyboard.reveal(curr_word.typed, self._correct)

            # Victory
            if strip_accents(w) == strip_accents(self._correct):
                self._count(self._attempt)
                return

            if self._attempt < ATTEMPTS - 1:
                self._attempt += 1
                self._words[self._attempt].set_typing()
            else:
                self._count(ATTEMPTS)
