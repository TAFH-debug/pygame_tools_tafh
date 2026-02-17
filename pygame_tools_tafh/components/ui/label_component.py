import pygame
from ..draw.surface_component import SurfaceComponent


class LabelComponent(SurfaceComponent):
    """A component that represents one line of text.

    Attributes:
        font    Pygame font object.
        text    Content of thsis label.
        color   Color of the text.
    """

    font: pygame.font.Font
    text: str
    color: tuple[int, int, int]

    def __init__(self, text: str, color: tuple[int, int, int], font_name="Arial", size=50):
        self.font = pygame.font.SysFont(font_name, size)
        self.text = text
        self.color = color
        self.pg_surf = self.font.render(self.text, True, self.color)