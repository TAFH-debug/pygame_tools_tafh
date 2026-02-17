import pygame
from ...core.game_object import GameObject
from ...vmath import Vector2d


def circle(go: GameObject, position: Vector2d, radius: int, color: tuple[int, int, int] = (255, 255, 255), width: int = 0):
    """Draws a circle relative to the game object position.
    """
    pygame.draw.circle(
        pygame.display.get_surface(),
        color,
        (go.get_relative_coords() + position).as_tuple(),
        radius,
        width
    )

def rect(go: GameObject, position: Vector2d, size: Vector2d, color: tuple[int, int, int] = (255, 255, 255), width: int = 0):
    """Draws a rectangle relative to the game object position.
    """
    pygame.draw.rect(
        pygame.display.get_surface(),
        color,
        (go.get_relative_coords() + position - size / 2).as_tuple() + size.as_tuple(),
        width
    )

def line(go: GameObject, start: Vector2d, end: Vector2d, color: tuple[int, int, int] = (255, 255, 255), width: int = 1):
    """Draws a line relative to the game object position.
    """
    pygame.draw.line(
        pygame.display.get_surface(),
        color,
        (go.get_relative_coords() + start).as_tuple(),
        (go.get_relative_coords() + end).as_tuple(),
        width
    )

def arc(go: GameObject, position: Vector2d, radius1: int, radius2: int, start_angle: float, end_angle: float, color: tuple[int, int, int] = (255, 255, 255), width: int = 0):
    """Draws an arc relative to the game object position.
    """
    pygame.draw.arc(
        pygame.display.get_surface(),
        color,
        (go.get_relative_coords() + position - Vector2d(radius1, radius2)).as_tuple() + (radius1 * 2, radius2 * 2),
        start_angle,
        end_angle,
        width
    )

def polygon(go: GameObject, points: list[Vector2d], color: tuple[int, int, int] = (255, 255, 255), width: int = 0):
    """Draws a polygon relative to the game object position.
    """
    pygame.draw.polygon(
        pygame.display.get_surface(),
        color,
        [(go.get_relative_coords() + point).as_tuple() for point in points],
        width
    )

def ellipse(go: GameObject, position: Vector2d, size: Vector2d, color: tuple[int, int, int] = (255, 255, 255), width: int = 0):
    """Draws an ellipse relative to the game object position.
    """
    pygame.draw.ellipse(
        pygame.display.get_surface(),
        color,
        (go.get_relative_coords() + position - size / 2).as_tuple() + size.as_tuple(),
        width
    )