from pygame import Rect, Surface, Vector2
import pygame.draw

from game.constants import ATTEMPTS
from game.util import write_small


class Stats:
    def __init__(self, pos: Vector2):
        self._pos = pos
        self._stats = [0, 0, 0, 0, 0, 0, 0]

    def count(self, attempt: int) -> None:
        self._stats[attempt] += 1

    def paint(self, canvas: Surface) -> None:
        pygame.draw.rect(
            surface=canvas,
            color=(29, 21, 22),
            rect=Rect(self._pos.x + 5, self._pos.y + 5, 300, 300),
        )
        pygame.draw.rect(
            surface=canvas,
            color=(49, 43, 45),
            rect=Rect(self._pos.x, self._pos.y, 300, 300),
        )
        write_small(
            canvas=canvas,
            pos=self._pos,
            text="Seus acertos",
            dimensions=Vector2(300, 40),
        )
        for i in range(len(self._stats)):
            write_small(
                canvas=canvas,
                pos=self._pos + Vector2(20 + 40 * i, 250),
                text=f"{'X' if i == ATTEMPTS else i + 1}",
            )

        total = max(sum(self._stats), 30)
        if total > 0:
            for i in range(len(self._stats)):
                max_bar_height = 180
                percent = self._stats[i] / total
                bar_size = max_bar_height * percent
                bar_pos = self._pos + Vector2(
                    15 + 40 * i, 230 - max_bar_height * percent
                )
                pygame.draw.rect(
                    surface=canvas,
                    color=(211, 173, 105),
                    rect=Rect(bar_pos.x, bar_pos.y, 25, bar_size),
                )
