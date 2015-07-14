import math
from display.displaymapper import convertYards2Pixels

__author__ = 'Thomas'

COLOR_GRASS = (40, 210, 40)
COLOR_TEAM_RED = (240, 30, 30)
COLOR_TEAM_BLUE = (30, 30, 240)
COLOR_BALL = (0, 0, 0)
COLOR_PAINT = (255, 255, 255)
COLOR_ORANGE = (240, 120, 0)
COLOR_TEAL = (0, 120, 240)

GRAPH_PLAYER_SIZE = [10, 10]
GRAPH_BALL_SIZE = [15, 15]
GRAPH_GOAL_SIZE = [convertYards2Pixels(8),1]

PAINT_WIDTH = 3

GAME_FPS = 30

STRAT_HOME_POS_SIZE = [convertYards2Pixels(25), convertYards2Pixels(25)]
STRAT_COVERAGE = 3**2 #Yards Squared
STRAT_BLOCKAGE = math.radians(20) #Theta difference in radians
STRAT_NEAR_BALL = 12**2 #Yards Squared
STRAT_MIN_PASS = 12

ATTR_PLAYER_SPEED = float(500)/GAME_FPS
ATTR_PLAYER_ACCEL = float(5)/GAME_FPS
ATTR_SHOOTING_RANGE = 30 #Abstract Units check its usage

MECH_TURNS_UNTOUCHABLE = max(float(GAME_FPS)/5,3)
MECH_BALL_SPEED = 1200/GAME_FPS

