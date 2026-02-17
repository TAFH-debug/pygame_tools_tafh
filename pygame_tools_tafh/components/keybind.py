from ..core.game_object import GameObject, Component
from typing import Callable, Any
import pygame as pg


class KeybindComponent(Component):
    cmd: Callable[[GameObject, list[int]], Any]
    listen: list[int]
    listen_for_hold: bool
    on_press: bool
    previous: list[int]


    def __init__(self, listen: list[int], cmd: Callable[[GameObject, list[int]], Any], listen_for_hold: bool = False, on_press: bool = True):
        self.listen = listen
        self.listen_for_hold = listen_for_hold
        self.on_press = on_press
        self.cmd = cmd
    
    def update(self):
        keys = pg.key.get_pressed()
        listen_keys = []
        
        for i in self.listen:
            if keys[i]: listen_keys.append(i)

        active_keys = []
        if not self.listen_for_hold:
            for i in self.listen:
                if (self.on_press == (i in listen_keys) == (not (i in self.previous))):
                    active_keys.append(i)
            self.previous = listen_keys.copy()
        else:
            active_keys = listen_keys
        
        if len(active_keys) != 0:
            self.cmd(self.game_object, active_keys)