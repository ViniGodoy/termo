import unicodedata

from pygame import Rect, Surface, Vector2
from pygame.font import Font, SysFont

_FONT_ARIAL_B: Font | None = None


def write(
    canvas: Surface,
    pos: Vector2,
    text: str,
    color: str | tuple[int, int, int] = "WHITE",
    dimensions: Vector2 | None = None,
) -> None:
    global _FONT_ARIAL_B  # noqa: PLW0603
    if _FONT_ARIAL_B is None:
        _FONT_ARIAL_B = SysFont("arial", 40, bold=True)

    text_surface = _FONT_ARIAL_B.render(text, True, color)
    if dimensions is not None:
        box_rect = Rect(pos.x, pos.y, dimensions.x, dimensions.y)
        text_rect = text_surface.get_rect(center=box_rect.center)
        canvas.blit(text_surface, text_rect)
    else:
        canvas.blit(text_surface, pos)


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(c for c in normalized if not unicodedata.combining(c))


def replace_letter(text: str, idx: int, ch: str = " ") -> str:
    return text[:idx] + ch + text[idx + 1 :]
