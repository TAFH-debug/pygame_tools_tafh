from .game_object import GameObject


class Scene:

    def __init__(self):
        pass

    def load(self, data: any):
        pass

    def destroy(self):
        for i in GameObject.objects:
            GameObject.destroy(i)

        GameObject.objects = []
