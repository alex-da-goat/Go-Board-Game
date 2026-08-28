#----------------------------Imports-------------------------------#
import pygame as pg
pg.init()
import copy

from constants import *
from macros import *
from macros import *

class Board():
    def __init__(self, _size):
        self.size = _size
        self.array = [ [EMPTY_STONE]*self.get_size() for i in range(self.get_size())]
        

    def draw_stones(self, _surface):
        stone_length = DISPLAYED_BOARD_LENGTH / self.get_size() # The length (both width and height) of a stone or empty space is the screen height divided by the length of one stone
        starting_pos = (CX - DISPLAYED_BOARD_LENGTH/2 + stone_length/2, CY - DISPLAYED_BOARD_LENGTH/2 + stone_length/2)
        radius = stone_length/2 * DISPLAYED_STONE_RADIUS_INDEX
        #Loop through all spaces on board
        for x in range(self.get_size()):
            for y in range(self.get_size()):
                if self.array[x][y] == BLACK_STONE: # if black stone
                    pg.draw.circle( _surface, BLACK, (starting_pos[0] + x*stone_length, starting_pos[1] + y*stone_length), radius )
                elif self.array[x][y] == WHITE_STONE: # if white stone
                    pg.draw.circle( _surface, WHITE, (starting_pos[0] + x*stone_length, starting_pos[1] + y*stone_length), radius)


    def draw_grid(self, _surface):
        stone_length = DISPLAYED_BOARD_LENGTH / self.get_size() # The length (both width and height) of a stone or empty space is the screen height divided by the length of one stone
        starting_pos = (CX - DISPLAYED_BOARD_LENGTH/2 + stone_length/2, CY - DISPLAYED_BOARD_LENGTH/2 + stone_length/2)
        grid_length = DISPLAYED_BOARD_LENGTH - stone_length # represents the length of just the grid, not the entire board since the stone lie on the corners thus the grid is slightly smaller
        #Draw vertical lines
        for i in range(self.get_size()):
            pg.draw.line(_surface, GRID_COLOR, (starting_pos[0] + i*stone_length, starting_pos[1]), (starting_pos[0] + i*stone_length, starting_pos[1] + grid_length), DISPLAYED_BOARD_THICKNESS)
        #Draw horizontal lines
        for i in range(self.get_size()):
            pg.draw.line(_surface, GRID_COLOR, (starting_pos[0], starting_pos[1] + i*stone_length), (starting_pos[0] + grid_length, starting_pos[1] + i*stone_length), DISPLAYED_BOARD_THICKNESS)

    def draw(self, _surface):
        self.draw_grid(_surface)
        self.draw_stones(_surface)
        
    def get_size(self):
        return self.size
    
    def set_stone(self, _grid_pos, _stone): #(grid pos from top-left)
        self.array[_grid_pos[0]][_grid_pos[1]] = _stone

    def get_stone(self, _grid_pos):
        return self.array[_grid_pos[0]][_grid_pos[1]]
    
    def get_array(self):
        return self.array # DONT ABUSE THIS CHANGE ARRAY WITHOUT GOING THROUGH THE RIGHT METHODS
    
    def set_array(self, _array):
        self.array = copy.deepcopy(_array)
    


class StoneButton(): # Includes empty spaces
    def __init__(self, _board, _length, _pos, _grid_pos):
        self.rect = pg.Rect( (_pos[0] - _length/2, _pos[1] - _length/2), (_length, _length)) 
        self.length = _length
        self.grid_pos = _grid_pos
        self.hover = None
        self.board = _board

        self.about_to_be_clicked = False

    def draw(self, _surface):
        if self.hover != None:
            radius = self.length/2 * DISPLAYED_STONE_BUTTON_RADIUS_INDEX
            pg.draw.circle(_surface, self.hover, self.rect.center, radius, STONE_HOVER_THICKNESS)

    def check_for_hover(self, _mouse_pos): # Check if mouse is hovering and update button if so change colour
        if self.rect.collidepoint(_mouse_pos):
            self.hover = GREEN
        else:
            self.hover = None

    def check_for_click(self, _mouse_pos, _mouse_down): # Return true if clicked
        #If mouse is down whilst hovering over button
        if self.rect.collidepoint(_mouse_pos) and _mouse_down:
            self.about_to_be_clicked = True
        
        #If mouse is up whilst hovering over button
        if self.rect.collidepoint(_mouse_pos) and not _mouse_down:
            if self.about_to_be_clicked:
                self.about_to_be_clicked = False
                return True

        #If mouse is not hovering over button and is up
        if not self.rect.collidepoint(_mouse_pos) and not _mouse_down:
            self.about_to_be_clicked = False

        return False
    
    def get_grid_pos(self):
        return self.grid_pos

                 
class BoardInput(): #Represents entire input system of the board
    def __init__(self, _board):
        #-------Initialize stone buttons------#
        stone_length = DISPLAYED_BOARD_LENGTH / _board.get_size() # The length (both width and height) of a stone or empty spac#e is the screen height divided by the length of one stone
        starting_pos = (CX - DISPLAYED_BOARD_LENGTH/2 + stone_length/2, CY - DISPLAYED_BOARD_LENGTH/2 + stone_length/2) 
        self.stone_buttons = []
        #Loop through all spaces on board
        for x in range(_board.get_size()):
            for y in range(_board.get_size()):
                self.stone_buttons.append( StoneButton(self, stone_length, (starting_pos[0] + x*stone_length, starting_pos[1] + y*stone_length), (x, y) ) )

    def update(self, _mouse_pos, _mouse_down): # return chosen grid space if one is chosen
        chosen_grid_space = None
        for btn in self.stone_buttons:
            btn.check_for_hover(_mouse_pos)
            if btn.check_for_click(_mouse_pos, _mouse_down):
                chosen_grid_space = btn.get_grid_pos()
        return chosen_grid_space
            
    def draw(self, _surface):
        for btn in self.stone_buttons:
            btn.draw(_surface)