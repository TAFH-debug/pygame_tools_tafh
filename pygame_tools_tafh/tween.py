import pygame
import math
from typing import Callable, Any, Union, Optional
from enum import Enum

from .vmath.vector import Vector2d

class EaseType(Enum):
    """Easing function types"""
    LINEAR = 0
    IN_QUAD = 1
    OUT_QUAD = 2
    IN_OUT_QUAD = 3
    IN_CUBIC = 4
    OUT_CUBIC = 5
    IN_OUT_CUBIC = 6
    IN_BACK = 7
    OUT_BACK = 8
    IN_OUT_BACK = 9

class Easing:
    """Collection of easing functions"""
    @staticmethod
    def linear(t: float) -> float:
        return t

    @staticmethod
    def in_quad(t: float) -> float:
        return t * t

    @staticmethod
    def out_quad(t: float) -> float:
        return 1 - (1 - t) * (1 - t)

    @staticmethod
    def in_out_quad(t: float) -> float:
        if t < 0.5:
            return 2 * t * t
        return 1 - pow(-2 * t + 2, 2) / 2

    @staticmethod
    def in_cubic(t: float) -> float:
        return t * t * t

    @staticmethod
    def out_cubic(t: float) -> float:
        return 1 - pow(1 - t, 3)

    @staticmethod
    def in_out_cubic(t: float) -> float:
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def in_back(t: float) -> float:
        c1 = 1.70158
        return t * t * ((c1 + 1) * t - c1)

    @staticmethod
    def out_back(t: float) -> float:
        c1 = 1.70158
        return 1 + (t - 1) * t * ((c1 + 1) * (t - 1) + c1)

    @staticmethod
    def in_out_back(t: float) -> float:
        c1 = 1.70158
        c2 = c1 * 1.525
        if t < 0.5:
            return (pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
        return (pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2

    @staticmethod
    def get_ease_function(ease_type: EaseType) -> Callable[[float], float]:
        return {
            EaseType.LINEAR: Easing.linear,
            EaseType.IN_QUAD: Easing.in_quad,
            EaseType.OUT_QUAD: Easing.out_quad,
            EaseType.IN_OUT_QUAD: Easing.in_out_quad,
            EaseType.IN_CUBIC: Easing.in_cubic,
            EaseType.OUT_CUBIC: Easing.out_cubic,
            EaseType.IN_OUT_CUBIC: Easing.in_out_cubic,
            EaseType.IN_BACK: Easing.in_back,
            EaseType.OUT_BACK: Easing.out_back,
            EaseType.IN_OUT_BACK: Easing.in_out_back,
        }[ease_type]

class Tween:
    """A class for creating smooth transitions between values in Pygame"""
    active_tweens: list["Tween"] = []

    def __init__(
        self,
        target: Any,
        property: str,
        start_value: Any,
        end_value: Any,
        duration: int,  # in milliseconds
        ease_type: EaseType = EaseType.LINEAR,
        delay: int = 0,  # in milliseconds
        repeat: int = 0,  # -1 for infinite
        yoyo: bool = False,
        on_start: Optional[Callable] = None,
        on_update: Optional[Callable] = None,
        on_complete: Optional[Callable] = None
    ):
        self.target = target
        self.property = property
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.ease_function = Easing.get_ease_function(ease_type)
        self.delay = delay
        self.repeat = repeat
        self.yoyo = yoyo
        
        self.on_start = on_start
        self.on_update = on_update
        self.on_complete = on_complete

        self.elapsed_time = 0
        self.delay_elapsed = 0
        self.is_running = False
        self.is_complete = False
        self.current_repeat = 0

    def start(self):
        """Start the tween"""
        if not self.is_running and not self.is_complete:
            self.is_running = True
            Tween.active_tweens.append(self)
            if self.on_start:
                self.on_start()

    def stop(self):
        """Stop the tween"""
        if self.is_running:
            self.is_running = False
            if self in Tween.active_tweens:
                Tween.active_tweens.remove(self)

    def _interpolate_value(self, progress: float) -> Any:
        """Interpolate between start and end values based on progress"""
        if isinstance(self.start_value, pygame.Color):
            r = self.start_value.r + (self.end_value.r - self.start_value.r) * progress
            g = self.start_value.g + (self.end_value.g - self.start_value.g) * progress
            b = self.start_value.b + (self.end_value.b - self.start_value.b) * progress
            a = self.start_value.a + (self.end_value.a - self.start_value.a) * progress
            return pygame.Color(int(r), int(g), int(b), int(a))
        elif isinstance(self.start_value, tuple) and len(self.start_value) == 2:
            # For positions/vectors
            x = self.start_value[0] + (self.end_value[0] - self.start_value[0]) * progress
            y = self.start_value[1] + (self.end_value[1] - self.start_value[1]) * progress
            return (x, y)
        return self.start_value + (self.end_value - self.start_value) * progress

    def _set_property(self, value: Any):
        """Set the property value on the target object"""
        parts = self.property.split('.')
        obj = self.target
        for part in parts[:-1]:
            obj = getattr(obj, part)
        setattr(obj, parts[-1], value)

    def update(self, dt: int):
        """Update the tween with the time delta in milliseconds"""
        if not self.is_running or self.is_complete:
            return

        if self.delay > 0:
            self.delay_elapsed += dt
            if self.delay_elapsed < self.delay:
                return
            
        self.elapsed_time += dt
        progress = min(1.0, self.elapsed_time / self.duration)
        eased_progress = self.ease_function(progress)
        
        # Update the value
        current_value = self._interpolate_value(eased_progress)
        self._set_property(current_value)

        if self.on_update:
            self.on_update(current_value, eased_progress)

        if progress >= 1.0:
            if self.repeat == -1 or self.current_repeat < self.repeat:
                self.elapsed_time = 0
                self.current_repeat += 1
                if self.yoyo:
                    self.start_value, self.end_value = self.end_value, self.start_value
            else:
                self.is_complete = True
                self.is_running = False
                Tween.active_tweens.remove(self)
                if self.on_complete:
                    self.on_complete()

    @staticmethod
    def update_all(dt: int):
        """Update all active tweens"""
        # Create a copy of the list to avoid modification during iteration
        for tween in Tween.active_tweens[:]:
            tween.update(dt)

    @staticmethod
    def stop_all():
        """Stop all active tweens"""
        for tween in Tween.active_tweens[:]:
            tween.stop()
        Tween.active_tweens.clear()


 
