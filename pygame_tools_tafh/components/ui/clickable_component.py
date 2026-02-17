from typing import Callable
import pygame

from ...vmath.vector import Vector2d
from ..draw.shape_component import ShapeComponent
from ...core.game_object import Component


class ClickableComponent(Component):
    """Clickable component with its own shape.

    cmd     Function that will be called when button is clicked.
    once    To call the function only once when clicked.
    """

    cmd: Callable
    once: bool
    _clicked: bool

    def __init__(self, cmd: Callable, once: bool, *args):
        self.cmd = cmd
        self.once = once
        self.args = args

    def update(self):
        if pygame.mouse.get_pressed(3)[0]: # 0 - Left Mouse Button
            pos = Vector2d.from_tuple(pygame.mouse.get_pos()) - self.game_object.get_relative_coords()

            if self.game_object.get_component(ShapeComponent).interception(pos) and not self._clicked:
                self.cmd(self.args)
            if self.once: 
                self._clicked = True
        else:
            self._clicked = False

    def draw(self):
        self.game_object.get_component(ShapeComponent).draw()

