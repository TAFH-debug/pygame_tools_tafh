from typing import Callable, TypeVar
from .vmath import Vector2d, Angle
import pygame as pg

class Component:
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
    game_object: "GameObject"
    position: Vector2d  # position of CENTER
    angle: Angle
    scale: float
    childs: list["Transform"]

    def __init__(self, obj: "GameObject"):
        self.game_object = obj
        self.position = Vector2d(0, 0)
        self.angle = Angle()
        self.scale = 1
        self.childs = []

    def translate(self, trn: Vector2d):
        self.position += trn
        for child in self.childs:
            child.translate(trn)

    def rotate(self, angle: Angle):
        self.angle += angle
        # TODO rotate all of the childs relative to center of this transform.

    def add_child(self, child: "Transform"):
        self.childs.append(child)

class SurfaceComponent(Component):
    layer: int 
    pg_surf: pg.Surface

    def __init__(self, size: Vector2d, layer: int = 0):
        self.pg_surf = pg.Surface(size.as_tuple(), pg.SRCALPHA, 32)
        if False:
            self.pg_surf.set_alpha(128)
        self.layer = layer

    def blit(self):
        surf = pg.display.get_surface()
        if self.game_object.parent:
            surf = self.game_object.parent.surface.pg_surf
        
        pos = self.game_object.transform.position
        if not self.game_object.parent:
            pos -= GameObject.get_by_tag("camera").transform.position

        surf.blit(self.pg_surf, pos.as_tuple())


class OnClick(Component):
    
    def get_cursor_coords(self):
        if not self.game_object.parent:
            return Vector2d.from_tuple(pg.mouse.get_pos()) - Vector2d.from_tuple(pg.display.get_window_size()) // 2 + GameObject.get_by_tag("camera").transform.position
        
        return self.game_object.parent.get_component(OnClick).get_cursor_coords() - self.game_object.parent.transform.position


T = TypeVar("T")

class GameObject:
    """
    Inspired by Unity.
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

    def __init__(self, tag: str, root: bool = True):
        self.components = []
        self.surface = SurfaceComponent(Vector2d(800, 600))
        self.add_component(self.surface)
        self.add_component(OnClick())

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


class Prefab:
    """
    Saves all the data about the object. Can be saved or loaded from the file.
    """
    components: list[Component.ComponentData]

    def __init__(self, game_object: GameObject):
        self.components = []
        for i in game_object.components:
            self.components.append(i.get_data())

    def load(self, filename: str):
        raise NotImplemented

    def save(self):
        raise NotImplemented


class GameObjectData:
    """
    Shorthand way to register a prefab to scene.
    """
    position: Vector2d
    angle: Angle
    components: list[Component]

    def __init__(self, pos=Vector2d(), angle=Angle(), *args: Component):
        self.position = pos
        self.angle = angle
        self.components = list(args)


