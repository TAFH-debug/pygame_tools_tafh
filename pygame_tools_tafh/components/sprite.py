import pygame
import os

from ..vmath import Vector2d
from ..game_object import Component, Transform, GameObject
from pygame import Surface

DEBUG = True

class SurfaceComponent(Component):
    layer: int
    pg_surf: pygame.Surface

    def __init__(self, tag, size: Vector2d, layer: int = -1):
        super().__init__(tag)
        self.pg_surf = pygame.Surface(size.as_tuple())
        self.layer = layer

    # def draw(self):
    #     if self.game_object.contains_component(Color):
    #         self.pg_surf.fill(self.game_object.get_component(Color).color)
    
    def blit(self):
        for child in self.game_object.childs:
            if child.contains_component(Surface):
                child.get_component(Surface).blit()

        if self.game_object.tag == "pygame_screen":
            return
        
        surf = self.game_object.parent.get_component(SurfaceComponent) 

        if self.game_object.tag in ("screen", "pygame_screen"):
            surf.pg_surf.blit(self.pg_surf, self.game_object.transform.position.as_tuple())
        else:
            surf.pg_surf.blit(self.pg_surf, (self.game_object.transform.position - GameObject.get_by_tag("camera").get_component(Transform).position).as_tuple())

class SpriteComponent(Component):
    path: str = ''
    loaded: dict = {}

    def __init__(self, sprite_name: str, size: tuple[int, int]) -> None:
        super().__init__()

        if sprite_name in SpriteComponent.loaded.keys():
            self.texture = SpriteComponent.loaded[sprite_name]
        else:
            self.texture = pygame.image.load(os.path.join(SpriteComponent.path, sprite_name)).convert_alpha()
            SpriteComponent.loaded[sprite_name] = self.texture

        self.size = size
        self.opacity = 255

    @staticmethod
    def set_path(path: str):
        SpriteComponent.path = path

    def draw(self, display: Surface):
        self.texture.set_alpha(self.opacity)
        blit_image = self.texture

        cropped = pygame.Surface(self.size)
        cropped.blit(blit_image, (0, 0))

        angle = self.game_object.transform.angle.get()
        scale = self.game_object.transform.scale

        if angle != 0:
            cropped = pygame.transform.rotate(cropped, angle)

        if scale != 1:
            cropped = pygame.transform.scale_by(cropped, scale)

        coords = self.game_object.transform.position - GameObject.get_by_tag("camera").transform.position
        rect = cropped.get_rect(center=coords)

        if DEBUG:
            pygame.draw.rect(display, (255, 0, 0), rect, 1)
        display.blit(blit_image, rect)
    