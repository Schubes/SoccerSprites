import math

__author__ = 'Thomas'

FIELD_LENGTH = 120 #this is horizontal dimension when displayed
FIELD_WIDTH = 80 #this is vertical dimension when displayed

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_HEADER_HEIGHT = WINDOW_HEIGHT-600

GAME_FPS = 5

COLOR_GRASS = (40, 210, 40)
COLOR_TEAM_RED = (240, 30, 30)
COLOR_TEAM_BLUE = (30, 30, 240)
COLOR_BALL = (150, 150, 150)
COLOR_PAINT = (255, 255, 255)

PAINT_WIDTH = 3

STRAT_COVERAGE = 25 #Yards Squared
STRAT_BLOCKAGE = math.radians(5) #Theta difference in radians
STRAT_NEARBALL = 100 #Yards Squared
STRAT_SHOOTINGRANGE = 200 #Abstract Units check its usage

ATTR_PLAYERSPEED = 5/GAME_FPS

MECH_TURNSUNTOUCHABLE = 2


