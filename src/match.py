import pygame
from gamevariables import COLOR_TEAM_BLUE, COLOR_TEAM_RED, WINDOW_HEADER_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, \
    COLOR_GRASS
from pitchObjects.ball import Ball
from pitchObjects.fieldPlayer import FieldPlayer
from team import Team

__author__ = 'Thomas'

class Match:
    """Handles match gameplay"""
    def __init__(self, window):
        self.window = window

        self.pitchSurface = self.createPitchSurface()
        self.fieldBackground = self.createPitchSurface()

        self.team1 = Team(True, COLOR_TEAM_BLUE)
        self.team2 = Team(False, COLOR_TEAM_RED)

        self.ball = Ball(self.pitchSurface)

        teamPlayers = self.team1.setStartingLineUp((4, 4, 2), self.ball, window)
        self.allsprites = pygame.sprite.LayeredDirty(teamPlayers)
        teamPlayers = self.team2.setStartingLineUp((4, 3, 3), self.ball, window)
        self.allsprites.add(teamPlayers)

    def playMatchTurn(self):
        self.allsprites.update()
        self.allsprites.draw(self.pitchSurface)
        self.allsprites.clear(self.pitchSurface, self.fieldBackground)
        self.window.blit(self.pitchSurface, (0, WINDOW_HEADER_HEIGHT))


    def createPitchSurface(self):
        pitchSurface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT-WINDOW_HEADER_HEIGHT))
        pitchSurface.fill(COLOR_GRASS)
        return pitchSurface
