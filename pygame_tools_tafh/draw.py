import pygame as pg

from .globals import camera

def text(display: pg.Surface, 
         text: str, 
         pos: tuple[int, int], 
         font: pg.font.Font, 
         color: tuple[int, int, int], 
         background: tuple[int, int, int] = None):
    text_surface = font.render(text, True, color, background)
    new_pos = camera.normalize((pos[0], pos[1])).as_tuple()
    text_rect = (new_pos[0], new_pos[1], text_surface.get_width(), text_surface.get_height())

    display.blit(text_surface, text_rect)

def rect(display: pg.Surface, rect: pg.Rect, color: tuple[int, int, int], width: int = 0):
    new_pos = camera.normalize((rect.x, rect.y)).as_tuple()
    rect = (new_pos[0], new_pos[1], rect.width, rect.height)
    pg.draw.rect(display, color, rect, width)

def circle(display: pg.Surface, pos: tuple[int, int], radius: int, color: tuple[int, int, int], width: int = 0):
    new_pos = camera.normalize(pos)
    pg.draw.circle(display, color, new_pos, radius, width)

def ellipse(display: pg.Surface, rect: pg.Rect, color: tuple[int, int, int], width: int = 0):
    new_pos = camera.normalize((rect.x, rect.y)).as_tuple()
    rect = (new_pos[0], new_pos[1], rect.width, rect.height)
    pg.draw.ellipse(display, color, rect, width)

def line(display: pg.Surface, start_pos: tuple[int, int], end_pos: tuple[int, int], color: tuple[int, int, int], width: int = 1):
    new_start_pos = camera.normalize(start_pos)
    new_end_pos = camera.normalize(end_pos)
    pg.draw.line(display, color, new_start_pos, new_end_pos, width)
