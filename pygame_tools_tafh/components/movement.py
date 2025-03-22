from ..game_object import Component
from ..globals import camera
import pygame as pg

class MovementComponent(Component):
    """Binds position of the camera to the position of the game object. Also implements basic camera movement.
    """
    speed: float

    def __init__(self, speed):
        super().__init__()
        self.speed = speed

    def update(self):
        pressed = pg.key.get_pressed()

        if pressed[pg.K_w]:
            self.game_object.transform.position.y -= self.speed
        if pressed[pg.K_s]:
            self.game_object.transform.position.y += self.speed
        if pressed[pg.K_a]:
            self.game_object.transform.position.x -= self.speed
        if pressed[pg.K_d]:
            self.game_object.transform.position.x += self.speed

        camera.transform.position = self.game_object.transform.position