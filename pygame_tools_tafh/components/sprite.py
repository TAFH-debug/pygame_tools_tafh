import pygame
import os

from ..game_object import Component

DEBUG = True

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

    def draw(self):
        display = self.game_object.surface.pg_surf
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

        rect = cropped.get_rect()

        if DEBUG:
            pygame.draw.rect(display, (255, 0, 0), rect, 1)
            
        display.blit(blit_image, rect)
    