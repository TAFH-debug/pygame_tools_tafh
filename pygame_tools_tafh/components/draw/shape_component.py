from ...core.game_object import Component
from ...vmath.vector import Vector2d


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