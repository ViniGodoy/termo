from pygame import Color, Rect, Surface, Vector2
import pygame.draw
from pygame.math import lerp

from game.constants import ATTEMPTS
from game.util import write_small


class Stats:
    def __init__(self, pos: Vector2):
        self._pos = pos
        self._stats = [0, 0, 0, 0, 0, 0, 0]
        self._prev_stats = [0, 0, 0, 0, 0, 0, 0]
        self._updated = -1
        self._s = 0.0

    def count(self, attempt: int) -> None:
        self._prev_stats = self._stats.copy()
        self._stats[attempt] += 1
        self._updated = attempt
        self._s = 0.0

    def paint(self, canvas: Surface) -> None:
        lerp_time = min(self._s / 2, 1)  # 2 secs
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
        success_rate = 0 if games == 0 else (games - self._stats[-1]) * 100 / games
        write_small(
            canvas=canvas,
            pos=self._pos,
            text=f"Partidas: {games:3}  Sucesso: {success_rate:5.1f}%",
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
            prev_top_most = max(self._prev_stats)
            for i in range(len(self._stats)):
                max_bar_height = 150
                percent = self._stats[i] / top_most
                prev_percent = (
                    0 if prev_top_most == 0 else self._prev_stats[i] / prev_top_most
                )
                percent = lerp(prev_percent, percent, lerp_time)

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
                    bar_color = bright_color.lerp(bar_color, lerp_time)
                pygame.draw.rect(
                    surface=canvas,
                    color=bar_color,
                    rect=Rect(bar_pos.x, bar_pos.y, 25, bar_size),
                )

    def update(self, dt: float) -> None:
        self._s += dt
