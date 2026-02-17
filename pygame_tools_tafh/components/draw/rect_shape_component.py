import pygame

from .draw import rect
from .shape_component import ShapeComponent
from ...core.game_object import GameObject
from ...vmath.vector import Vector2d


class RectShapeComponent(ShapeComponent):

    def __init__(self, color: tuple[int, int, int], size: Vector2d):
        super().__init__(color)
        self.size = size

    def draw(self):
        rect(self.game_object, Vector2d(0, 0), self.size, self.color)

    def interception(self, position: Vector2d) -> bool:
        temp = position.operation(self.size, lambda a, b: -b/2 <= a <= b/2)
        return bool(temp.x) and bool(temp.y)