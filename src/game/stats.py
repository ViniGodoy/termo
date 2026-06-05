from pygame import Rect, Surface, Vector2
import pygame.draw
from pygame.math import lerp

from game.constants import (
    ATTEMPTS,
    BG_DARK,
    BG_FAIL,
    BG_SECONDARY,
    BG_SHADOW,
    BG_SUCCESS,
    FG_SECONDARY,
)
from game.util import write_small


class Stats:
    def __init__(self, pos: Vector2, stats: list[int]):
        self._pos = pos
        self._stats = stats
        self._prev_stats = [0, 0, 0, 0, 0, 0, 0]
        self._updated = -1
        self._s = 0.0

    @property
    def stats(self) -> list[int]:
        return self._stats.copy()

    def count(self, attempt: int) -> None:
        self._prev_stats = self._stats.copy()
        self._stats[attempt] += 1
        self._updated = attempt
        self._s = 0.0

    def paint(self, canvas: Surface) -> None:
        lerp_time = min(self._s / 1.2, 1)  # 2 secs
        # background
        pygame.draw.rect(
            surface=canvas,
            color=BG_SHADOW,
            rect=Rect(self._pos.x + 5, self._pos.y + 5, 300, 300),
            border_radius=10,
        )
        pygame.draw.rect(
            surface=canvas,
            color=BG_DARK,
            rect=Rect(self._pos.x, self._pos.y, 300, 300),
            border_radius=10,
        )

        # counts
        curr_games = sum(self._stats)
        prev_games = sum(self._prev_stats)

        curr_success_rate = (
            0 if curr_games == 0 else (curr_games - self._stats[-1]) * 100 / curr_games
        )
        prev_sucess_rate = (
            0
            if prev_games == 0
            else (prev_games - self._prev_stats[-1]) * 100 / prev_games
        )

        games = lerp(prev_games, curr_games, lerp_time)
        success_rate = lerp(prev_sucess_rate, curr_success_rate, lerp_time)

        write_small(
            canvas=canvas,
            pos=self._pos,
            text=f"Partidas: {games:3.0f}  Sucesso: {success_rate:5.1f}%",
            color=FG_SECONDARY,
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

        top_most = max(self._stats)
        if top_most > 0:
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
                bar_color = BG_SECONDARY
                if i == self._updated:
                    bright_color = BG_SUCCESS if self._updated != ATTEMPTS else BG_FAIL
                    bar_color = bright_color.lerp(bar_color, lerp_time)
                pygame.draw.rect(
                    surface=canvas,
                    color=bar_color,
                    rect=Rect(bar_pos.x, bar_pos.y, 25, bar_size),
                )

    def update(self, dt: float) -> None:
        self._s += dt
