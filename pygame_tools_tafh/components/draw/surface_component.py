from ...core.game_object import Component, GameObject
import pygame as pg
from ...vmath import Vector2d

class SurfaceComponent(Component):
    """Necessary component to handle everything with game_object's display

    pg_surf     Associated pygame.Surface 
    """
    pg_surf: pg.Surface

    def __init__(self, surface: pg.Surface, pos: Vector2d = Vector2d(0, 0)):
        super().__init__()
        self.pg_surf = surface

    def draw(self):
        display = pg.display.get_surface()

        pos = self.game_object.get_absolute_coords() - GameObject.get_by_tag("camera").position + Vector2d.from_tuple(pg.display.get_window_size()) / 2
        top_left = pos - Vector2d(self.pg_surf.get_width() / 2, self.pg_surf.get_height() / 2)
        display.blit(
            self.pg_surf, 
            top_left.as_tuple() + (self.pg_surf.get_width(), self.pg_surf.get_height())
        )