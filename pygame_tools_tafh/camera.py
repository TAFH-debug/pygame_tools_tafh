from pygame_tools_tafh.vmath import *


class Camera:
    x: float
    y: float
    zoom: float

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.zoom = 0

    def _normalize(self, pos: Vector2d) -> Vector2d:
        """
        Normalizes pos coordinates to relative to camera coordinates.
        """

        # TODO: Zoom in/out
        return Vector2d(pos.x - self.x, pos.y - self.y)

    def normalize(self, pos: Vector2d | tuple[float, float]) -> Vector2d:
        if isinstance(pos, tuple):
            return self._normalize(Vector2d.from_tuple(pos))
        return self._normalize(pos)

    def set_x(self, x: float):
        self.x = x

    def set_y(self, y: float):
        self.y = y

    def set_position(self, pos: Vector2d | tuple[float, float]):
        if isinstance(pos, tuple):
            pos = Vector2d.from_tuple(pos)
        self.x = pos.x
        self.y = pos.y

    def add_x(self, x: float):
        self.x += x

    def add_y(self, y: float):
        self.y += y

    def add_pos(self, pos: Vector2d | tuple[float, float]):
        if isinstance(pos, tuple):
            pos = Vector2d.from_tuple(pos)
        self.x += pos.x
        self.y += pos.y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_pos(self):
        return Vector2d(self.x, self.y)
