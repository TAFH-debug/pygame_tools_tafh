import asyncio
from .scene import Scene
from .game_object import GameObject
from .globals import events

import pygame as pg
import logging


class Engine:

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

    def register(self, scene: Scene):
        self.scenes.append(scene)

    async def run_engine(self, data: any):
        if len(self.scenes) == 0:
            logging.error("No scenes registered.")
            return

        first_scene = self.scenes[0]
            
        self.scene = first_scene
        self.scene.load(data)
        
        logging.info(f"Scene {first_scene.name} loaded")
        
        try:
            while True:
                await self.iteration()
                await asyncio.sleep(1 / self.fps)
        except Exception as e:
            logging.critical(e.with_traceback(None))
            exit(1)

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
            while True:
                await self.iteration()
                await asyncio.sleep(1 / self.fps)
        except Exception as e:
            logging.critical(e.with_traceback(None))
            exit(1)

    def event_processing(self, event: pg.event.Event):
        if event.type == pg.QUIT:
            logging.info("Quitting")
            exit()

    async def iteration(self):
        
        events = pg.event.get()
        
        for event in events:
            self.event_processing(event)
        
        for i in GameObject.objects:
            i.update()

        self.display.fill((0, 0, 0))
        for i in GameObject.objects:
            i.draw()
            i.surface.blit()

        pg.display.flip()
            
