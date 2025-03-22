import asyncio
from typing import Callable

class Tweens:
    """A class for creating background functions that will change some property over time.
    """
    tweens: list = []

    def __init__(self):
        self.tweens = []

    def add(self, target: any,
            property: str,
            fr: float,
            to: float,
            repeat: int = 0,
            duration: int = 1000,
            delay: int = 0,
            after_tween: Callable | None = None,
            update_tween: Callable | None = None):
        """Add new tween.

        Args:
            target          Object that will be changed.
            property        Property that will be changed. Must be float.
            fr              Value to start from.
            to              Value to end on.
            repeat          Amount of times to repeat.
            duration        Duration of the change.
            after_tween     Function that will be called after the tween is ended.
            update_tween    Function that will be called every tick while the tween is on going.
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self.start_tween(target, property, fr, to, repeat, duration, delay, after_tween, update_tween))
        
    async def start_tween(self, target: any,
            property: str | None = None,
            fr: float | None = None,
            to: float | None = None,
            repeat: int = 0,
            duration: int = 1000,
            delay: int = 0,
            after_tween: Callable | None = None,
            update_tween: Callable | None = None):
        await asyncio.sleep(delay)
        cnt = (1, repeat + 1)[repeat != -1]
        while cnt > 0:
            for i in range(60 * duration):
                if update_tween:
                    update_tween()
                else:
                    setattr(target, property, fr + (to - fr) * (i / (60 * duration)))
                await asyncio.sleep(1 / 60)

            if repeat != -1:
                cnt -= 1

        if after_tween:
            after_tween()
 
