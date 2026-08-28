#----------------------------Imports-------------------------------#
import pygame as pg
pg.init()
import copy

from constants import *
from macros import *
from menu_classes_and_functions import *
from data_stuctures import *
from board_classes import *

#---------------------------Classes------------------------------#
class Game():
    def __init__(self, _size):
        self.board = Board(_size)
        self.board_input = BoardInput(self.board)
        self.turn = BLACKS_TURN

        self.black_captures = 0 #how many pieces of white that black has captured
        self.white_captures = 0 #how many pieces of black that white has captured

        self.already_visited_positions = [] #necessary variable so that double-checks do not happen in recursive algorithms
        self.turns_skipped_in_a_row = 0 #variable that tracks how many turns have been skipped in a row, necessary to tell when game ends
        self.queue_previous_board_states = Circular_Queue(KO_HOW_MANY_PREVIOUS_BOARD_STATES_TO_STORE) #queue that holds the last something board states (each themselves an array)

        self.game_state = STATE_PLAYING

    def draw_all(self, _surface):
        self.board.draw(_surface)
        self.board_input.draw(_surface)
        self.draw_stats(_surface)

    def draw_stats(self, _surface):

        #Displaying whose turn it is
        if self.turn == BLACKS_TURN:
            draw_text_to_surface(_surface, (SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.2), "Black's Turn", BLACK, DEFAULT_FONT_NAME, 40)
        elif self.turn == WHITES_TURN:
            draw_text_to_surface(_surface, (SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.2), "White's Turn", WHITE, DEFAULT_FONT_NAME, 40)

        #Displaying current number of captures
        draw_text_to_surface(_surface, (SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.6), "Black: " + str(self.black_captures), BLACK, DEFAULT_FONT_NAME, 30)
        draw_text_to_surface(_surface, (SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.67), "White: " + str(self.white_captures), WHITE, DEFAULT_FONT_NAME, 30)

        #Displaying Game Over if necessary
        if self.game_state == STATE_GAME_OVER:
            draw_text_to_surface(_surface, (CX, CY), "GAME OVER!", RED, DEFAULT_FONT_NAME, 100)

        
    def attempt_move(self, _grid_pos, _stone):
        move_validated = self.validate_move(_grid_pos, _stone) # Returns "valid" if move is valid, returns error message if not.
        if move_validated == True:
            self.board.set_stone(_grid_pos, _stone)
            return True
        else:
            print(move_validated)
        return False

    def validate_move(self, _grid_pos, _stone):
    
        enemy_stone = OPPOSITE_STONE(_stone)

        #-----------------Ensuring space is empty------------------#
        if self.board.get_stone((_grid_pos[0], _grid_pos[1])) != EMPTY_STONE:
            return "Invalid! Not an empty space!"
    

        #----------------Ensuring space is not suicide----------------#
        #Add the stone to the space to test if its suicidal
        self.board.set_stone(_grid_pos, _stone)
        #Checking if it is surrounded (for suicide)
        suicidal = False
        if self.recursive_check_if_surrounded(_grid_pos): #if surrounded
            suicidal = True
            #checking if this move will remove other pieces thus making it non-suicidal in the end
            spaces_to_check = get_four_adjacent_spaces(self.board, _grid_pos)
            for space in spaces_to_check:
                if space["stone"] == enemy_stone:
                    if self.recursive_check_if_surrounded(space["pos"]):
                        suicidal = False
                        break
        
        #Reverting board to normal
        self.board.set_stone(_grid_pos, EMPTY_STONE)

        #Returning
        if suicidal:
            return "Invalid! Move is suicidal!"
        
        #--------------------Ensuring space is not ko-------------------------#
        ko = False
        superko = False
        orig_board_array = copy.deepcopy( self.board.get_array() )
        #placing the stone on the board to test if its ko
        self.board.set_stone(_grid_pos, _stone)

        #Removing pieces as necessary:  
        spaces_to_check = get_four_adjacent_spaces(self.board, _grid_pos)
        for space in spaces_to_check:
            if space["stone"] == enemy_stone:
                if self.recursive_check_if_surrounded(space["pos"]):
                    self.recursive_fill_empty(space["pos"])

        #Checking if ko
        board_states = self.queue_previous_board_states.get_array_of_items()
        for i in range( len(board_states) ):
            board_state = board_states[i]
            if board_state == self.board.get_array():
                if i == 1:
                    ko = True
                else:
                    superko = True
                break
        
        #Reverting board back to normal
        self.board.set_array(orig_board_array)

        #Returning
        if superko:
            return "Invalid! Move is superko!"
        if ko:
            return "Invalid! Move is ko!"
                        

        return True
    
    def recursive_fill_empty_and_capture_pieces(self, _grid_pos): # grid pos represents first stone where the empty fill will be applied 
        stone = self.board.get_stone(_grid_pos)
        spaces_to_check = get_four_adjacent_spaces(self.board, _grid_pos)
        
        if not stone == EMPTY_STONE:
            #Fill self with empty
            self.board.set_stone(_grid_pos, EMPTY_STONE)
            #Add to captures
            if stone == WHITE_STONE: # If black captured white's stone
                self.black_captures += 1
            else: # If white captured black's stone
                self.white_captures += 1

            #Recursive Algorithm
            for space in spaces_to_check:
                if space["stone"] == stone:
                    self.recursive_fill_empty_and_capture_pieces(space["pos"])

    
    def recursive_fill_empty(self, _grid_pos): # grid pos represents first stone where the empty fill will be applied 
        stone = self.board.get_stone(_grid_pos)
        spaces_to_check = get_four_adjacent_spaces(self.board, _grid_pos)
        
        if not stone == EMPTY_STONE:
            #Fill self with empty
            self.board.set_stone(_grid_pos, EMPTY_STONE)

            #Recursive Algorithm
            for space in spaces_to_check:
                if space["stone"] == stone:
                    self.recursive_fill_empty(space["pos"])


    def recursive_check_if_surrounded(self, _grid_pos):
        self.already_visited_positions = []
        return self.recursive_check_if_surrounded_repeated(_grid_pos)
    

    def recursive_check_if_surrounded_repeated(self, _grid_pos): # do not call this function, call recursive_check_if_surrounded instead.
        self.already_visited_positions.append(_grid_pos)

        stone = self.board.get_stone(_grid_pos)
        spaces_to_check = get_four_adjacent_spaces(self.board, _grid_pos)

        #Ensuring it is not starting on an empty space:
        if stone == EMPTY_STONE:
            return False

        #Recursive Algorithm
        for space in spaces_to_check:
            if space["stone"] == EMPTY_STONE:
                return False
            
            if space["stone"] == stone:
                already_checked = False
                for pos in self.already_visited_positions:
                    if space["pos"] == pos:
                        already_checked = True
                        break

                if not already_checked:
                    if self.recursive_check_if_surrounded_repeated(space["pos"]) == False:
                        return False
        return True        


    def update(self, _mouse_pos, _mouse_down):

        #Checking for game over:
        if self.turns_skipped_in_a_row > 1:
            self.game_state = STATE_GAME_OVER
        
        if self.game_state == STATE_PLAYING:
            #-----Setting Turn-----#
            if self.turn == BLACKS_TURN:
                stone = BLACK_STONE
            else:
                stone = WHITE_STONE
        
            #----Setting Local Variables-----#
            enemy_stone = OPPOSITE_STONE(stone)

            #------Ending Game if turn was skipped twice-----#


            #-----Receiving Inputs-----#
            #Board Input 
            player_input = self.board_input.update(_mouse_pos, _mouse_down) # is None if no input was pressed, is a the grid coordinate is one was pressed
            if player_input != None:

                if self.attempt_move( player_input, stone ): # Attempts move, returning True is successful
                    
                    #Resetting turns skipped in a row to 0
                    self.turns_skipped_in_a_row = 0
                    
                    #Removing pieces as necessary:
                    spaces_to_check = get_four_adjacent_spaces(self.board, player_input)
                    for space in spaces_to_check:
                        if space["stone"] == enemy_stone:
                            if self.recursive_check_if_surrounded(space["pos"]):
                                self.recursive_fill_empty_and_capture_pieces(space["pos"])


                    #Record board state
                    if self.queue_previous_board_states.get_is_full():
                        self.queue_previous_board_states.dequeue()
                    self.queue_previous_board_states.enqueue( copy.deepcopy(self.board.get_array()) )


                    #Change whose turn it is
                    self.turn = OPPOSITE_TURN(self.turn)



        if self.game_state == STATE_GAME_OVER:
            pass
                
    
    def get_turn(self):
        return self.turn
    
    def skip_turn(self):
        self.turn = OPPOSITE_TURN(self.turn)
        self.turns_skipped_in_a_row += 1




#------------------------------------FUNCTIONS-=----------------------------------------#

def get_four_adjacent_spaces(_board, _grid_pos): #this function is only used by Game
        if _grid_pos[0] != _board.get_size()-1:
            right_space = {
                "pos" : (_grid_pos[0]+1, _grid_pos[1]),
                "stone" : _board.get_stone((_grid_pos[0]+1, _grid_pos[1]))
            }
        else:
            right_space = {
                "pos" : (_grid_pos[0]+1, _grid_pos[1]),
                "stone" : OUT_OF_BOUNDS_STONE
            }

        if _grid_pos[1] != 0:
            up_space = {
                "pos" : (_grid_pos[0], _grid_pos[1]-1),
                "stone" : _board.get_stone((_grid_pos[0], _grid_pos[1]-1))
            }
        else:
            up_space = {
                "pos" : (_grid_pos[0], _grid_pos[1]-1),
                "stone" : OUT_OF_BOUNDS_STONE
            }
        
        if _grid_pos[0] != 0:
            left_space = {
                "pos" : (_grid_pos[0]-1, _grid_pos[1]),
                "stone" : _board.get_stone((_grid_pos[0]-1, _grid_pos[1]))
            }
        else:
            left_space = {
                "pos" : (_grid_pos[0]-1, _grid_pos[1]),
                "stone" : OUT_OF_BOUNDS_STONE
            }

        if _grid_pos[1] != _board.get_size()-1:
            down_space = {
                "pos" : (_grid_pos[0], _grid_pos[1]+1),
                "stone" : _board.get_stone((_grid_pos[0], _grid_pos[1]+1))
            }
        else:
            down_space = {
                "pos" : (_grid_pos[0], _grid_pos[1]+1),
                "stone" : OUT_OF_BOUNDS_STONE
            }

        return[right_space, up_space, left_space, down_space]



#should i make recursive and flood fill functions, external functions as opposed to methods of the class Game? 
                
