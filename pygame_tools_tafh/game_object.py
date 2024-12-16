from typing import TypeVar
from pygame_tools_tafh.vmath import Vector2d, Angle
from pygame import Surface

class Component:
    game_object: "GameObject"

    class ComponentData:
        component_type: type

        def __init__(self, ctp: type):
            self.component_type = ctp

    def init(self, go: "GameObject"):
        self.game_object = go

    def draw(self, display: Surface):
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


T = TypeVar("T", bound=Component)


class GameObject:
    """
    Inspired by Unity.
    """
    components: list[Component]
    active: bool
    tag: str
    transform: Transform
    childs: list["GameObject"]

    objects: list["GameObject"] = []

    def __init__(self, tag: str):
        self.components = []
        self.childs = []
        self.active = True
        self.tag = tag
        self.transform = Transform(self)
        GameObject.objects.append(self)

    def draw(self, display: Surface):
        for component in self.components:
            component.draw(display)
        if not "child" in self.__dir__():
            return 
        for child in self.childs:
            child.draw(display)

    def update(self):
        for i in self.components:
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

    def set_active(self, active: bool):
        self.active = active

    def clone(self) -> "GameObject":
        # TODO
        raise NotImplemented()

    @staticmethod
    def get_by_tag(tag: str) -> "GameObject":
        for i in GameObject.objects:
            if i.tag == tag:
                return i
        raise Exception("No such object")

    @staticmethod
    def destroy(obj: "GameObject"):
        obj.on_destroy()


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


