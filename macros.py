#-----------Macros-----------#
EMPTY_STONE = 0
BLACK_STONE = 1
WHITE_STONE = 2
OUT_OF_BOUNDS_STONE = 3

BLACKS_TURN = 0
WHITES_TURN = 1

STATE_PLAYING = 0
STATE_GAME_OVER = 1

def OPPOSITE_STONE(_stone): 
    if _stone == BLACK_STONE:
        return WHITE_STONE
    if _stone == WHITE_STONE:
        return BLACK_STONE
    else:
        return _stone
    
def OPPOSITE_TURN(_turn):
    if _turn == BLACKS_TURN:
        return WHITES_TURN
    elif _turn == WHITES_TURN:
        return BLACKS_TURN
    else:
        return _turn
    
def DECREMENT_CIRCULAR(_index, _size):
    if _index != 0:
        return _index - 1
    else:
        return _size - 1
    
def INCREMENT_CIRCULAR(_index, _size):
    if _index != _size-1:
        return _index + 1
    else:
        return 0