import pygame

from gamevariables import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_FPS
from match import Match
from resources.FpsClock import FpsClock


__author__ = 'Thomas'

window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) #makes the window
pygame.display.set_caption("FootSim") #sets the game caption

timer = FpsClock(GAME_FPS)

match = Match(window)

while True:
    match.playMatchTurn()
    pygame.display.update()
    timer.tick()




