from .game_object import GameObject


class Scene:

    name: str

    def __init__(self, name: str):
        self.name = name
        
    def load(self, data: any):
        pass

    def destroy(self):
        for i in GameObject.objects:
            GameObject.destroy(i)

        GameObject.objects = []
