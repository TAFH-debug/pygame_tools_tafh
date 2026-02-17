from typing import TypeVar
from ..vmath import Vector2d, Angle

import pygame as pg

class Component:
    """Base class for all components.

    game_object     Associated GameObject.
    """
    game_object: "GameObject"

    def init(self, go: "GameObject"):
        self.game_object = go

    def draw(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass 

T = TypeVar("T")

class GameObject:
    """Base of this engine. Every object in the game must be implemented by creating a game object and adding necessary components.

    active      If false, this game object won't be displayed and updated. The same is true for it's childs.
    tag         Tag of the object. There can't be two game objects with the same tag.
    """
    components: list[Component]
    active: bool
    tag: str
    parent: "GameObject | None"
    position: Vector2d
    childs: list["GameObject"]
    z_index: int

    tag_objects: dict[str, "GameObject"] = {}
    objects: list["GameObject"] = []

    def __init__(self, tag: str):
        self.components = []
        self.childs = []
        self.active = True
        self.tag = tag
        self.parent = None
        self.position = Vector2d(0, 0)
        self.z_index = 0

        if (self.tag in GameObject.tag_objects.keys()):
            raise Exception(f"Tried to create two object with same tag: {self.tag}")
        GameObject.objects.append(self)
            
        GameObject.tag_objects[self.tag] = self

    def draw(self):
        if (not self.active): return

        for component in self.components:
            component.draw()

    def update(self):
        if (not self.active): return
        
        for i in self.components:
            i.update()

    def on_destroy(self):
        for i in self.components:
            i.destroy()

        for i in self.childs:
            GameObject.destroy(i)

    def add_component(self, component: Component):
        component.init(self)
        self.components.append(component)
        return self

    def get_component(self, component: type[T]) -> T:
        for i in self.components:
            if isinstance(i, component):
                return i
        raise Exception(f"No such component: {component}")
    
    def contains_component(self, component: type[T]) -> T:
        for i in self.components:
            if isinstance(i, component):
                return True
        return False
    
    def add_child(self, child: "GameObject"):
        child.parent = self
        self.childs.append(child)
        return self

    def set_active(self, active: bool):
        self.active = active

    def clone(self) -> "GameObject":
        # TODO
        raise NotImplemented()

    def get_absolute_coords(self):
        """Function to get absolute game_object's coordinates.

        Returns:
            game_object's absolute coordinates.
        """
        if not self.parent:
            return self.position
        
        return self.parent.get_absolute_coords() + self.position
    
    def get_relative_coords(self):
        """Function to get game_object's coordinates relative to center of viewport.

        Returns:
            game_object's relative coordinates.
        """
        return self.get_absolute_coords() - GameObject.get_by_tag("camera").position + Vector2d.from_tuple(pg.display.get_window_size()) // 2

    @staticmethod
    def get_by_tag(tag: str) -> "GameObject":
        if not tag in GameObject.tag_objects.keys():
            raise KeyError(f"No object with tag: {tag}")
        return GameObject.tag_objects[tag]

    @staticmethod
    def destroy(obj: "GameObject"):
        GameObject.objects.remove(obj)
        GameObject.tag_objects.pop(obj.tag)
        obj.on_destroy()

    def __str__(self):
        return f"GameObject {self.tag}"
