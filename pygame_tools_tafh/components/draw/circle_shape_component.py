from .draw import circle
from .shape_component import ShapeComponent
from ...core.game_object import GameObject
from ...vmath.vector import Vector2d
import pygame


class CircleShapeComponent(ShapeComponent):
    def __init__(self, color: tuple[int, int, int], radius: float):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        circle(self.game_object, Vector2d(0, 0), self.radius, self.color)

    def interception(self, position: Vector2d) -> bool:
        return position.mod() <= self.radius