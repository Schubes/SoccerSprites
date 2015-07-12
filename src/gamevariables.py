import math
from display.displaymapper import convertYards2Pixels

__author__ = 'Thomas'

COLOR_GRASS = (40, 210, 40)
COLOR_TEAM_RED = (240, 30, 30)
COLOR_TEAM_BLUE = (30, 30, 240)
COLOR_BALL = (150, 150, 150)
COLOR_PAINT = (255, 255, 255)
COLOR_ORANGE = (240, 120, 0)
COLOR_TEAL = (0, 120, 240)

GRAPH_PLAYER_SIZE = [10, 10]
GRAPH_BALL_SIZE = [20, 20]

PAINT_WIDTH = 3

GAME_FPS = 30

STRAT_HOME_POS_SIZE = [convertYards2Pixels(30), convertYards2Pixels(30)]
STRAT_COVERAGE = 7**2 #Yards Squared
STRAT_BLOCKAGE = math.radians(5) #Theta difference in radians
STRAT_NEAR_BALL = 12**2 #Yards Squared

ATTR_PLAYER_SPEED = float(10)/GAME_FPS
ATTR_PLAYER_ACCEL = float(1)/GAME_FPS
ATTR_SHOOTING_RANGE = 200 #Abstract Units check its usage

MECH_TURNS_UNTOUCHABLE = GAME_FPS * 1/5
MECH_BALL_SPEED = 800/GAME_FPS

