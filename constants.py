#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BEIGE = (188, 159, 128)
ORANGE = (255, 95, 31)


#-----------Constants--------#
#Basic and Essential
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
CX = SCREEN_WIDTH/2
CY = SCREEN_HEIGHT/2

#Technical
KO_HOW_MANY_PREVIOUS_BOARD_STATES_TO_STORE = 20 # Variable that dictates how many previous board states (from recent) is necessary
                                               # to store and check in order to stop players from bringing back previous board state (Ko)

#Visual
BG_COLOR = BEIGE
DISPLAYED_BOARD_LENGTH = SCREEN_HEIGHT*0.8 # Length including stones
DISPLAYED_BOARD_THICKNESS = 2
STONE_HOVER_THICKNESS = 5
GRID_COLOR = BLUE
DISPLAYED_STONE_RADIUS_INDEX = 0.95 #number from 0 to 1
DISPLAYED_STONE_BUTTON_RADIUS_INDEX = 1.1*DISPLAYED_STONE_RADIUS_INDEX # number from 0 to 1

#Fonts
DEFAULT_FONT_NAME = 'Snap ITC'
