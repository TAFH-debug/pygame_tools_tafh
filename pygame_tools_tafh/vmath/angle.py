from math import *

from .vector import Vector2d


class Angle:
    """
    class that represent angles in radians
    """

    angle: float

    def __init__(self, angle: float = 0) -> None:
        self.angle = angle
        self.angle %= (2 * pi)

    def set(self, angle: float, is_degree: bool = False):
        if is_degree:
            angle = angle * pi / 180
        self.angle = angle
        self.angle %= (2 * pi)

    def get(self, is_degree: bool = False):
        if is_degree:
            return self.angle * 180 / pi
        return self.angle

    def to_vector(self) -> Vector2d:
        return Vector2d(cos(self.angle), sin(self.angle))

    def __add__(self, other: "Angle") -> "Angle":
        return Angle(self.get() + other.get())

    def __sub__(self, other: "Angle") -> "Angle":
        return Angle(self.get() - other.get())

    def __repr__(self) -> str:
        return str(self.angle)

    def __float__(self) -> float:
        return self.angle