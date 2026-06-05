import unicodedata

from pygame import Rect, Surface, Vector2
from pygame.color import Color
from pygame.font import Font, SysFont

from game.constants import FG_PRIMARY

FONT_BIG: Font | None = None
FONT_SMALL: Font | None = None


def _write(  # noqa: PLR0913
    canvas: Surface,
    font: Font,
    pos: Vector2,
    text: str,
    color: Color,
    dimensions: Vector2,
) -> None:
    text_surface = font.render(text, True, color)
    if dimensions is not None:
        box_rect = Rect(pos.x, pos.y, dimensions.x, dimensions.y)
        text_rect = text_surface.get_rect(center=box_rect.center)
        canvas.blit(text_surface, text_rect)
    else:
        canvas.blit(text_surface, pos)


def write(
    canvas: Surface,
    pos: Vector2,
    text: str,
    color: Color = FG_PRIMARY,
    dimensions: Vector2 | None = None,
) -> None:
    global FONT_BIG  # noqa: PLW0603
    if FONT_BIG is None:
        FONT_BIG = SysFont("arial", 40, bold=True)
    _write(canvas, FONT_BIG, pos, text, color, dimensions)


def write_small(
    canvas: Surface,
    pos: Vector2,
    text: str,
    color: Color = FG_PRIMARY,
    dimensions: Vector2 | None = None,
) -> None:
    global FONT_SMALL  # noqa: PLW0603
    if FONT_SMALL is None:
        FONT_SMALL = SysFont("arial", 20, bold=True)
    _write(canvas, FONT_SMALL, pos, text, color, dimensions)


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def replace_letter(text: str, idx: int, ch: str = " ") -> str:
    return text[:idx] + ch + text[idx + 1 :]
