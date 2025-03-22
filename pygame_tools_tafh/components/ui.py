from typing import Callable
import pygame

from ..vmath import Vector2d
from ..game_object import Component, CoordinatesComponent, SurfaceComponent

class LabelComponent(Component):
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
        
    def draw(self):
        text = self.font.render(self.text, True, self.color)
        text = pygame.transform.scale(text, (text.get_width(), text.get_height()))
        self.game_object.surface.pg_surf.blit(
            text, 
            text.get_rect(center=(self.game_object.surface.pg_surf.get_width() // 2, 
                                  self.game_object.surface.pg_surf.get_height() // 2))
        )

class ShapeComponent(Component):
    """Generic class for the components that represent geometric shapes.

    color   Fill color of the shape.
    """
    def __init__(self, color: tuple[int, int, int]):
        self.color = color

    def draw(self):
        pass

    def interception(self, position: Vector2d) -> bool:
        """Checks if position is inside of the shape.
        
        Args:
            position: Position to check.
        
        Returns:
            True if the position is inside of the shape, False otherwise.
        """
        return False

class RectShapeComponent(ShapeComponent):

    def __init__(self, color: tuple[int, int, int], size: Vector2d):
        super().__init__(color)
        self.size = size

    def draw(self):
        pygame.draw.rect(self.game_object.surface.pg_surf, self.color, 
                        (self.game_object.surface.pg_surf.get_width() // 2 - self.size.x // 2, 
                                self.game_object.surface.pg_surf.get_height() // 2 - self.size.y // 2, 
                                self.size.x, self.size.y))

    def interception(self, position: Vector2d) -> bool:
        center = self.game_object.transform.position
        temp = (center - position).operation(self.size, lambda a, b: -b/2 <= a <= b/2)
        return bool(temp.x) and bool(temp.y)
    

class CircleShapeComponent(ShapeComponent):
    def __init__(self, color: tuple[int, int, int], radius: float):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.game_object.surface.pg_surf, self.color, 
                        (self.game_object.surface.pg_surf.get_width() // 2, 
                            self.game_object.surface.pg_surf.get_height() // 2), 
                        self.radius)

    def interception(self, position: Vector2d) -> bool:
        center = self.game_object.transform.position
        return (center - position).mod() <= self.radius


class ButtonComponent(Component):
    """Clickable component with its own shape.

    cmd     Function that will be called when button is clicked.
    """

    cmd: Callable

    def __init__(self, cmd: Callable, *args):
        self.cmd = cmd
        self.args = args

    def update(self):
        if pygame.mouse.get_pressed(3)[0]: # 0 - Left Mouse Button
            pos = self.game_object.get_component(CoordinatesComponent).get_cursor_coords()
            if self.game_object.get_component(ShapeComponent).interception(pos):
                self.cmd(self.args)

    def draw(self):
        self.game_object.get_component(ShapeComponent).draw()
