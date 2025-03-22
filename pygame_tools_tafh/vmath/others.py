from .vector import *


def is_in_box(vec1: Vector2d, other1: "Vector2d", other2: "Vector2d") -> bool:
    """Checks if the position is inside of the box.

    Args:
        vec1    Position to check.
        other1  Position of the one vertex of the box.
        other2  Position of the diametrically opposed vertex of the box.

    Returns:
        True if the position is inside of the box, False otherwise.
    """
    return ((vec1 - other1) * (other2 - other1)).get_quarter() == 1 and (
            (other2 - other1) * (other2 - other1) - (vec1 - other1) * (vec1 - other1)).get_quarter() == 1

def complex_multiply(vec1: Vector2d, other: Vector2d) -> Vector2d:
    return Vector2d(vec1.x * other.x - vec1.y * other.y, vec1.y * other.x + vec1.x * other.y)