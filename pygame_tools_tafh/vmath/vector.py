from typing import Callable
from .angle import *

class Vector2d:
    """
    Class to represent a pair of floats.
    """

    x: float
    y: float

    def __init__(self, a: float = 0, b: float = 0):
        self.x = a
        self.y = b

    @staticmethod
    def from_tuple(tpl: tuple[float, float]) -> "Vector2d":
        return Vector2d(tpl[0], tpl[1])

    def as_tuple(self) -> tuple[float, float]:
        return self.x, self.y

    def norm(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2))

    def intx(self) -> int:
        return int(self.x)

    def inty(self) -> int:
        return int(self.y)

    def to_angle(self) -> "Angle":
        return Angle(atan2(-self.y, self.x))

    def get_quarter(self) -> int:
        if self.x >= 0 and self.y >= 0:
            return 1
        elif self.x <= 0 and self.y <= 0:
            return 3
        elif self.x < 0:
            return 2
        elif self.y < 0:
            return 4
        
    def operation(self, other: "Vector2d", operation: Callable[[float, float], float]) -> "Vector2d":
        return Vector2d(operation(self.x, other.x), operation(self.y, other.y))
    
    def __add__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: "float | Vector2d") -> "Vector2d":
        if isinstance(other, Vector2d):
            return Vector2d(self.x * other.x, self.y * other.y)
        else:
            return Vector2d(self.x * other, self.y * other)

    def __floordiv__(self, other: float):
        return Vector2d(self.x // other, self.y // other)

    def __truediv__(self, other: float) -> "Vector2d":
        return Vector2d(self.x / other, self.y / other)

    def __mod__(self, other: float) -> "Vector2d":
        return Vector2d(self.x % other, self.y % other)

    def __repr__(self) -> str:  # for debugging
        return f"<{self.x}, {self.y}>"

    def __eq__(self, other: "Vector2d") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Vector2d") -> bool:
        return self.x != other.x or self.y != other.y
