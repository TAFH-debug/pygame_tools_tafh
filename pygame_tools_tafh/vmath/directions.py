from .angle import *
from .modx import *
from .vector import *

class Direction(Modx):
    def __init__(self, value: int = 0) -> None:
        super().__init__(value)

    def to_angle(self) -> Angle:
        return Angle(self.value * pi / 2)

    @staticmethod
    def from_angle(ang: Angle) -> "Direction":
        return Direction((ang.get() + pi / 4) // (pi / 2))

    def to_vector(self) -> Vector2d:
        return Directions.AsVector2D[self.value]


class Directions:
    RIGHT = Direction(0)
    UP = Direction(1)
    LEFT = Direction(2)
    DOWN = Direction(3)

    AsVector2D = (
        Vector2d(1, 0),
        Vector2d(0, -1),
        Vector2d(-1, 0),
        Vector2d(0, 1)
    )