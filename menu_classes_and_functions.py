import pygame as pg
pg.init()
from constants import *
from macros import *

#------------------------------------Classes------------------------------------#
"""class Button():
    def __init__(self, _pos, _dimensions, _color, _text, _func): # _dimensions is a tuple of width and height
        self.surface = pg.Surface(_dimensions, pg.SRCALPHA)
        self.rect = pg.Rect(_pos, _dimensions)"""

#-------------------------------Functions---------------------------------#
def draw_text_to_surface(_surface, _pos, _text, _colour, _font_name, _size, ):
    font = pg.font.SysFont(_font_name, _size)
    img = font.render(_text, True, _colour)
    #Automatically center it and blit it to surface
    width = img.get_width()
    height = img.get_height()
    _surface.blit(img, (_pos[0] - width/2, _pos[1] - height/2))