#--------------------------Imports-------------------------------#
import pygame as pg
pg.init()
from constants import *
from macros import *
from game_classes_and_functions import *

#--------------------------Initialization-----------------------#
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True
dt = 0.1

game = Game(13)

#--------------------------------Game Loop---------------------------------------#

while running:

    #----------------Events-------------#
    for event in pg.event.get():
        #QUIT GAME
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                pass

    #--------------Mouse---------------#
    mouse_pos = pg.mouse.get_pos()
    mouse_down = pg.mouse.get_pressed()[0]


    #---------------Updating--------------#
    game.update(mouse_pos, mouse_down)

    #--------------Drawing--------------#
    screen.fill(BG_COLOR)
    game.draw_all(screen)
    pg.display.flip()
    
    #-------------Delta Time--------------#
    dt = clock.tick(60) / 1000
    dt = max(0.001, min(0.1, dt))


