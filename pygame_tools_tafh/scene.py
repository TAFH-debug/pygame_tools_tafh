from .core.game_object import GameObject


class Scene:
    """Base class for scenes.
    
    name    Name of the scene.
    """
    name: str

    def __init__(self, name: str):
        self.name = name
        
    def load(self, data: any):
        """Loads the scene, creates necessary game objects and components.
        
        Args:
            data    Data that was given to the scene.
        """
        pass

    def destroy(self):
        for i in GameObject.objects:
            GameObject.destroy(i)

        GameObject.objects = []
