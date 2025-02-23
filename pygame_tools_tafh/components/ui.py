from typing import Callable
import pygame

from ..vmath import Vector2d
from ..game_object import Component

class Clicked:
    def __init__(self, color: tuple[int, int, int], border: "Border | None" = None):
        self.color = color
        self.border = border

    @staticmethod
    def get_default():
        return Clicked((0, 0, 0))


class Border:

    def __init__(self, width: int, color: tuple[int, int, int], radius: int):
        self.width = width
        self.color = color
        self.radius = radius

    @staticmethod
    def get_default():
        return Border(1, (0, 0, 0), -1)


class Text:

    def __init__(self, text: str,
                 font: pygame.font.Font | None = None,
                 color: tuple[int, int, int] = (0, 0, 0),
                 background_color: tuple[int, int, int] | None = None):
        font = font or pygame.font.SysFont("Arial", 20)
        self.text = text
        self.font = font
        self.color = color
        self.background_color = background_color

    def render(self):
        return self.font.render(self.text, False, self.color, self.background_color)
    

class LabelComponent(Component):

    def __init__(self, text: str, color: tuple[int, int, int]):
        self.font = pygame.font.SysFont("Arial", 50) # TODO: choosing fonts
        self.text = text
        self.scale_x = 1
        self.scale_y = 1
        self.color = color
        
    def draw(self, display: pygame.Surface):
        sum_height = 0
        for i in self.text.split("\n"):
            # TODO: Rework it so center of whole passage will be at right center.
            text = self.font.render(i, True, self.color)

            text = pygame.transform.scale(text, (text.get_width() * self.scale_x, text.get_height() * self.scale_y))
            display.blit(text, text.get_rect(center=
                (self.game_object.transform.position + Vector2d(0, sum_height)).as_tuple()))
            sum_height += text.get_height()


class ButtonComponent(Component):

    def __init__(self, cmd: Callable, interception: Callable[[Vector2d, Vector2d], bool], *args):
        self.cmd = cmd
        self.interception = interception
        self.args = args

    def update(self):
        if pygame.mouse.get_pressed(3)[0]:
            pos = Vector2d.from_tuple(pygame.mouse.get_pos())
            if self.interception(camera.normalize(self.game_object.transform.position), pos):
                self.cmd(self.args)


class RectButtonComponent(ButtonComponent):

    def __init__(self, cmd: Callable, size: Vector2d, *args):
        self.size = size
        def interception(center: Vector2d, position: Vector2d) -> bool:
            temp = (center - position).operation(size, lambda a, b: -b/2 <= a <= b/2)
            return bool(temp.x) and bool(temp.y)

        super().__init__(cmd, interception)

    def draw(self, display: pygame.Surface):
        if DEBUG:
            top_left = (self.game_object.transform.position - self.size / 2)
            pygame.draw.rect(display, (200, 200, 200), (top_left.x, top_left.y, self.size.x, self.size.y), width=1)

class CircleButtonComponent(ButtonComponent):

    def __init__(self, cmd: Callable, radius: float, *args):
        self.radius = radius
        def interception(center: Vector2d, position: Vector2d) -> bool:
            return (center - position).norm() <= radius

        super().__init__(cmd, interception)