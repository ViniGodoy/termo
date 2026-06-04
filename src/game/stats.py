from math import cos

from pygame import Color, Rect, Surface, Vector2
import pygame.draw

from game.constants import ATTEMPTS
from game.util import write_small


class Stats:
    def __init__(self, pos: Vector2):
        self._pos = pos
        self._stats = [0, 0, 0, 0, 0, 0, 0]
        self._updated = -1
        self._s = 0.0

    def count(self, attempt: int) -> None:
        self._stats[attempt] += 1
        self._updated = attempt

    def paint(self, canvas: Surface) -> None:
        # background
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

        # counts
        games = sum(self._stats)
        sucesses = 0 if games == 0 else (games - self._stats[-1]) * 100 / games
        write_small(
            canvas=canvas,
            pos=self._pos,
            text=f"Partidas: {games:3}  Sucesso: {sucesses:5.1f}%",
            color=(211, 173, 105),
            dimensions=Vector2(300, 40),
        )

        # distribution bars
        write_small(
            canvas=canvas,
            pos=self._pos,
            text="Distribuição",
            dimensions=Vector2(300, 120),
        )
        for i in range(len(self._stats)):
            write_small(
                canvas=canvas,
                pos=self._pos + Vector2(20 + 40 * i, 270),
                text=f"{'X' if i == ATTEMPTS else i + 1}",
            )

        if self._updated != -1:
            top_most = max(self._stats)
            for i in range(len(self._stats)):
                max_bar_height = 150
                percent = self._stats[i] / top_most
                bar_size = max_bar_height * percent
                bar_pos = self._pos + Vector2(
                    15 + 40 * i, 250 - max_bar_height * percent
                )
                bar_color = Color(211, 173, 105)
                if i == self._updated:
                    bright_color = (
                        Color(58, 163, 148)
                        if self._updated != ATTEMPTS
                        else Color(163, 60, 58)
                    )
                    bar_color = bar_color.lerp(bright_color, abs(cos(self._s)))
                pygame.draw.rect(
                    surface=canvas,
                    color=bar_color,
                    rect=Rect(bar_pos.x, bar_pos.y, 25, bar_size),
                )

    def update(self, dt: float) -> None:
        self._s += dt / 2
