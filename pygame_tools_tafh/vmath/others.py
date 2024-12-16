from .vector import *


def is_in_box(vec1: Vector2d, other1: "Vector2d", other2: "Vector2d") -> bool:
    return ((vec1 - other1) * (other2 - other1)).get_quarter() == 1 and (
            (other2 - other1) * (other2 - other1) - (vec1 - other1) * (vec1 - other1)).get_quarter() == 1

def complex_multiply(vec1: Vector2d, other: Vector2d) -> Vector2d:
    return Vector2d(vec1.x * other.x - vec1.y * other.y, vec1.y * other.x + vec1.x * other.y)