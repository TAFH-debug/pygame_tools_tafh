import traceback
from .scene import Scene
from .core.game_object import GameObject
from .tween import Tween
import pygame as pg
import logging


class Engine:
    """Root class of the engine. Can't be instantiated more than once.

    display     Basically pygame.display.get_display()
    scene       Current loaded scene
    scenes      List of all registered scenes
    """
    instance = None

    scenes: list[Scene]
    scene: Scene
    logger: logging.Logger
    scene: Scene
    display: pg.Surface
    fps: int

    def __init__(self, app_name: str, fps: int, resolution: tuple[int, int] = (800, 600)):
        self.fps = fps
        self.scenes = []
        self.scene = None
        self.app_name = app_name
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("[%(levelname)s][%(name)s]: %(message)s"))
        self.logger.addHandler(handler)
        self.init(resolution)

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Engine, cls).__new__(cls)
        return cls.instance

    def init(self, resolution: tuple[int, int] = (800, 600)):
        pg.init()
        pg.font.init()
        logging.basicConfig()
        self.display = pg.display.set_mode(resolution)
        pg.display.set_caption(self.app_name)
        logging.info("Engine initialized.")
        GameObject("camera")

    def register(self, scene: Scene):
        self.scenes.append(scene)

    async def load_scene(self, scene_name: str, data: any):
        scene = next((x for x in self.scenes if x.name == scene_name), None)

        if not scene:
            logging.error(f"Scene {scene_name} not found.")
            return
        
        if self.scene:
            scene.destroy()
            
        self.scene = scene
        scene.load(data)
        
        logging.info(f"Scene {scene.name} loaded")
        try:
            clock = pg.time.Clock()
            while True:
                dt = clock.tick(self.fps)
                await self.iteration(dt)
        except Exception as e:
            logging.critical(traceback.format_exc())
            exit(1)

    def event_processing(self, event: pg.event.Event):
        if event.type == pg.QUIT:
            logging.info("Quitting")
            exit()

    async def iteration(self, dt: int):
        events = pg.event.get()
        
        for event in events:
            self.event_processing(event)
        
        for i in GameObject.objects:
            i.update()

        Tween.update_all(dt)
        self.display.fill((0, 0, 0))
        for i in sorted(GameObject.objects, key=lambda x: -x.z_index):
            i.draw()

        pg.display.flip()
            
