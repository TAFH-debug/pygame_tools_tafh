from typing import TypeVar
from .vmath import Vector2d, Angle

import pygame as pg

class Component:
    """Base class for all components.

    game_object     Associated GameObject.
    """
    game_object: "GameObject"

    class ComponentData:
        component_type: type

        def __init__(self, ctp: type):
            self.component_type = ctp

    def init(self, go: "GameObject"):
        self.game_object = go

    def draw(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

    def get_data(self) -> ComponentData:
        return self.ComponentData(Component)


class Transform:
    """Contains all of the necessary data about GameObject's location.

    game_object     Associated game object.
    position        Position of the center of the game_object.
    angle           Angle for which game_object is rotated.

    """
    game_object: "GameObject"
    position: Vector2d  # position of CENTER
    angle: Angle
    scale: float

    def __init__(self, obj: "GameObject"):
        self.game_object = obj
        self.position = Vector2d(0, 0)
        self.angle = Angle()
        self.scale = 1
        self.childs = []

    def rotate(self, angle: Angle):
        self.angle += angle
        # TODO rotate all of the childs relative to center of this transform.

    def add_child(self, child: "Transform"):
        self.childs.append(child)

class SurfaceComponent(Component):
    """Necessary component to handle everything with game_object's display

    pg_surf     Associated pygame.Surface 
    """
    pg_surf: pg.Surface

    def __init__(self, size: Vector2d):
        self.pg_surf = pg.Surface(size.as_tuple(), pg.SRCALPHA, 32)

    def blit(self):
        surf = pg.display.get_surface()
        if self.game_object.parent:
            surf = self.game_object.parent.surface.pg_surf
        
        pos = self.game_object.transform.position
        if not self.game_object.parent:
            pos -= GameObject.get_by_tag("camera").transform.position

        surf.blit(self.pg_surf, (pos + Vector2d.from_tuple(surf.get_size()) / 2 - Vector2d.from_tuple(self.pg_surf.get_size()) / 2).as_tuple())


class CoordinatesComponent(Component):
    """Necessary component to get global object's coordinates.
    """

    def get_cursor_coords(self):
        """Function to get cursor's coordinates in appropriate coordinate system.
        
        Returns:
            Coordinates of the cursor relative to the center of the game object.
        """
        if not self.game_object.parent:
            return Vector2d.from_tuple(pg.mouse.get_pos()) - Vector2d.from_tuple(pg.display.get_window_size()) // 2 + GameObject.get_by_tag("camera").transform.position
        
        return self.game_object.parent.get_component(CoordinatesComponent).get_cursor_coords() - self.game_object.parent.transform.position
    
    def get_absolute_coords(self):
        """Function to get absolute game_object's coordinates.

        Returns:
            game_object's absolute coordinates.
        """
        if not self.game_object.parent:
            return self.game_object.transform.position
        
        return self.game_object.parent.get_component(CoordinatesComponent).get_absolute_coords() + self.game_object.transform.position
    

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
    transform: Transform
    surface: SurfaceComponent
    childs: list["GameObject"]

    tag_objects: dict[str, "GameObject"] = {}
    objects: list["GameObject"] = []

    def __init__(self, tag: str, root: bool = True, surf_size: Vector2d = Vector2d(800, 600)):
        self.components = []
        self.surface = SurfaceComponent(surf_size)
        self.add_component(self.surface)
        self.add_component(CoordinatesComponent())

        self.childs = []
        self.active = True
        self.tag = tag
        self.parent = None
        self.transform = Transform(self)

        if (self.tag in GameObject.tag_objects.keys()):
            raise Exception(f"Tried to create two object with same tag: {self.tag}")

        if root:
            GameObject.objects.append(self)
            
        GameObject.tag_objects[self.tag] = self

    def draw(self):
        center = self.get_component(CoordinatesComponent).get_absolute_coords()
        screen_tl = GameObject.get_by_tag("camera").transform.position - Vector2d.from_tuple(pg.display.get_window_size()) / 2
        screen_br = GameObject.get_by_tag("camera").transform.position + Vector2d.from_tuple(pg.display.get_window_size()) / 2
        obj_tl = center - Vector2d.from_tuple(self.surface.pg_surf.get_size()) / 2
        obj_br = center + Vector2d.from_tuple(self.surface.pg_surf.get_size()) / 2

        # Draw optimization. No need to draw the object if it is out of screen's bounds.
        if ((screen_br.x < obj_tl.x or screen_tl.x > obj_br.x) or (screen_br.y < obj_tl.y or screen_tl.y > obj_br.y)):
            return

        for component in self.components:
            component.draw()
        for child in self.childs:
            child.draw()
            child.surface.blit()

    def update(self):
        for i in self.components:
            i.update()
        for i in self.childs:
            i.update()

    def on_destroy(self):
        for i in self.childs:
            GameObject.destroy(i)

    def add_component(self, component: Component):
        component.init(self)
        self.components.append(component)

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

    def set_active(self, active: bool):
        self.active = active

    def clone(self) -> "GameObject":
        # TODO
        raise NotImplemented()
    
    def clear_surface(self):
        for i in self.childs:
            i.clear_surface()
        self.surface.pg_surf.fill((0, 0, 0, 0))

    @staticmethod
    def get_by_tag(tag: str) -> "GameObject":
        if not tag in GameObject.tag_objects.keys():
            raise KeyError(f"No object with tag: {tag}")
        return GameObject.tag_objects[tag]

    @staticmethod
    def destroy(obj: "GameObject"):
        obj.on_destroy()

    def __str__(self):
        return f"GameObject {self.tag}"
